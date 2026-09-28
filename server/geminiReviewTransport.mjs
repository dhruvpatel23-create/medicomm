// Review requests have a bounded budget below the client's 150-second timeout.
// Switch models only for availability failures, never to bypass auth or quota errors.
export function createGeminiReviewTransport({ fetchImpl = fetch, sleep = ms => new Promise(resolve => setTimeout(resolve, ms)), now = Date.now, random = Math.random, attemptTimeoutMs = 30000, totalTimeoutMs = 125000 } = {}) {
  const unavailableUntil = new Map();
  const transient = status => status === 408 || status === 500 || status === 502 || status === 503 || status === 504;
  return async function fetchReview(url, options) {
    const primary = new URL(url).pathname.match(/\/models\/([^:]+):generateContent$/)?.[1];
    if (!primary) throw new Error('Invalid Gemini review endpoint.');
    const fallback = (process.env.GEMINI_REVIEW_FALLBACK_MODEL || 'gemini-3.5-flash-lite').trim().replace(/^models\//, '');
    const candidates = [...new Set([primary, fallback].filter(Boolean))];
    const models = [...candidates.filter(model => (unavailableUntil.get(model) || 0) <= now()), ...candidates.filter(model => (unavailableUntil.get(model) || 0) > now())];
    const deadline = now() + totalTimeoutMs;
    const originalBody = JSON.parse(options.body);
    let lastResponse;
    let lastError;
    let quotaModel = null;
    let retryAfterMs = 0;
    const missing = new Set();
    for (let round = 0; round < 2; round++) {
      if (round > 0) {
        const delay = Math.max(1200 + Math.floor(random() * 400), retryAfterMs);
        if (now() + delay >= deadline) break;
        await sleep(delay);
      }
      for (const model of quotaModel ? [quotaModel] : models) {
        if (missing.has(model) || now() >= deadline) continue;
        const payload = structuredClone(originalBody);
        payload.generationConfig ??= {};
        // Gemini 2.5 and 3 use different thinking controls; preserve all content/schema.
        delete payload.generationConfig.thinkingConfig;
        if (model.startsWith('gemini-3')) payload.generationConfig.thinkingConfig = { thinkingLevel: 'low' };
        else if (model.startsWith('gemini-2.5')) payload.generationConfig.thinkingConfig = { thinkingBudget: 0 };
        const requestUrl = new URL(url);
        requestUrl.pathname = requestUrl.pathname.replace(`/models/${primary}:`, `/models/${model}:`);
        try {
          const timeoutSignal = AbortSignal.timeout(Math.max(1, Math.min(attemptTimeoutMs, deadline - now())));
          const signal = options.signal ? AbortSignal.any([options.signal, timeoutSignal]) : timeoutSignal;
          const response = await fetchImpl(requestUrl.toString(), { ...options, body: JSON.stringify(payload), signal });
          // Read within the timeout as an upstream response can stall after headers.
          const body = await response.text();
          lastResponse = new Response(body, { status: response.status, headers: response.headers });
          Object.defineProperty(lastResponse, 'geminiModel', { value: model });
          if (response.ok) { unavailableUntil.delete(model); return lastResponse; }
          if (response.status === 429) {
            quotaModel = model;
            const header = response.headers.get('retry-after');
            const seconds = header === null ? NaN : Number(header);
            retryAfterMs = Number.isFinite(seconds) ? seconds * 1000 : Math.max(0, Date.parse(header) - now()) || 0;
            if (!retryAfterMs) {
              try {
                const retry = JSON.parse(body).error?.details?.find(detail => detail['@type']?.endsWith('RetryInfo'))?.retryDelay;
                retryAfterMs = Number.parseFloat(retry) * 1000 || 0;
              } catch { /* Use bounded backoff if the provider omits retry guidance. */ }
            }
            break;
          }
          if (response.status === 404) { missing.add(model); continue; }
          if (!transient(response.status)) return lastResponse;
          unavailableUntil.set(model, now() + 60000);
        } catch (error) {
          if (options.signal?.aborted) throw error;
          lastError = error;
          unavailableUntil.set(model, now() + 60000);
        }
      }
    }
    if (lastResponse) return lastResponse;
    throw new Error('Gemini could not be reached after automatic recovery attempts. Your answer is still here; please try again shortly.', { cause: lastError });
  };
}

export const fetchGeminiReviewWithFallback = createGeminiReviewTransport();
