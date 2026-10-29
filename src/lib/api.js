export async function apiRequest(path, options = {}) {
  localStorage.removeItem("medicomm-session-token");
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers ?? {}),
  };
  const controller = new AbortController();
  const timeoutMs =
    options.timeoutMs ??
    (/^\/api\/auth\/(?:login|signup|google)$/.test(path) ? 30000 : 8000);
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(path, {
      ...options,
      headers,
      credentials: "same-origin",
      signal: controller.signal,
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      const error = new Error(data.message ?? data.error ?? "Request failed.");
      error.status = response.status;
      error.retryAfter = Number(response.headers.get("Retry-After")) || 0;
      error.requestId = data.requestId;
      throw error;
    }

    const method = (options.method ?? "GET").toUpperCase();
    if (
      method !== "GET" &&
      method !== "HEAD" &&
      /^\/api\/(duels|short-notes|clinical-cases|verify-payment)/.test(path)
    ) {
      window.dispatchEvent(new Event("tokens-changed"));
    }

    return data;
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error("The server took too long to respond.");
    }

    throw error;
  } finally {
    window.clearTimeout(timeoutId);
  }
}
