import { HttpError } from './security.mjs';

export function validateDraft(value) {
  if (!value || value.version !== 2 || !Array.isArray(value.pages) || !value.pages.length || value.pages.length > 8
    || !Number.isInteger(value.pageIndex) || value.pageIndex < 0 || value.pageIndex >= value.pages.length
    || Buffer.byteLength(JSON.stringify(value)) > 2 * 1024 * 1024) throw new HttpError(400, 'Invalid notepad draft (maximum 2 MB and 8 pages).');
  for (const page of value.pages) {
    if (!['ruled', 'dotted', 'plain'].includes(page.paper) || !Array.isArray(page.strokes)) throw new HttpError(400, 'Invalid notepad page.');
    for (const stroke of page.strokes) {
      if (!['pen', 'eraser'].includes(stroke.tool) || typeof stroke.color !== 'string' || stroke.color.length > 32
        || !Number.isFinite(stroke.size) || stroke.size <= 0 || stroke.size > 200 || !Array.isArray(stroke.points)
        || !stroke.points.length || !stroke.points.every(p => [p.x, p.y, p.pressure].every(Number.isFinite))) throw new HttpError(400, 'Invalid notepad stroke.');
    }
  }
  return value;
}

export function createNotepadStore({ url, key, namespace = 'medicomm', fetchImpl = fetch }) {
  const filter = value => encodeURIComponent(value);
  async function request(path, method = 'GET', body) {
    if (!url || !key) throw new HttpError(503, 'Cloud notepad storage is not configured. Your draft remains on this device.');
    const response = await fetchImpl(`${url}/rest/v1/${path}`, { method,
      headers: { apikey: key, Authorization: `Bearer ${key}`, 'Content-Type': 'application/json', Prefer: 'return=representation' },
      body: body === undefined ? undefined : JSON.stringify(body), signal: AbortSignal.timeout(15000) });
    if (!response.ok) throw new HttpError(response.status === 409 ? 409 : 503,
      response.status === 409 ? 'This draft changed on another device.' : 'Cloud notepad storage is unavailable. Check the notepad database migration.');
    return response.status === 204 ? null : response.json();
  }
  const scope = user => `namespace=eq.${filter(namespace)}&user_id=eq.${filter(user)}`;
  return {
    async getDraft(user, id) {
      const rows = await request(`notepad_drafts?${scope(user)}&draft_id=eq.${filter(id)}&limit=1`);
      return rows[0] ?? null;
    },
    async putDraft(user, id, draft, revision) {
      validateDraft(draft);
      if (!Number.isSafeInteger(revision) || revision < 0) throw new HttpError(400, 'Invalid draft revision.');
      const data = { namespace, user_id: user, draft_id: id, draft, revision: revision + 1, updated_at: new Date().toISOString() };
      const rows = revision === 0 ? await request('notepad_drafts', 'POST', data)
        : await request(`notepad_drafts?${scope(user)}&draft_id=eq.${filter(id)}&revision=eq.${revision}`, 'PATCH', data);
      if (!rows?.length) throw new HttpError(409, 'This draft changed on another device.');
      return rows[0];
    },
    async reviews(user, questionId = null, offset = 0, since = null) {
      return (await request(`notepad_reviews?${scope(user)}${questionId ? `&question_id=eq.${filter(questionId)}` : ''}${since ? `&submitted_at=gte.${filter(since)}` : ''}&order=submitted_at.desc,id.desc&offset=${offset}&limit=100`)).map(row => row.review);
    },
    async summaries(user, offset = 0) {
      return (await request(`notepad_review_summaries?${scope(user)}&order=submitted_at.desc,id.desc&offset=${offset}&limit=100`))
        .map(row => ({ ...row.review, attemptCount: row.attempt_count }));
    },
    async saveReview(review) {
      await request('notepad_reviews', 'POST', { namespace, user_id: review.userId, id: review.id, question_id: review.questionId,
        submitted_at: review.submittedAt, review });
    },
    async hasReview(user, id) {
      return (await request(`notepad_reviews?${scope(user)}&id=eq.${filter(id)}&select=id&limit=1`)).length > 0;
    },
    async ownsImage(user, name) {
      return (await request(`notepad_reviews?${scope(user)}&review->answerPages=cs.${filter(JSON.stringify([{ imagePath: name }]))}&select=id&limit=1`)).length > 0;
    },
  };
}

export function createDraftHandler({ store, readDatabase, requireSessionUser, parseRequestBody, sendJson }) {
  return async (request, response, url) => {
    const user = requireSessionUser(request, response, readDatabase());
    if (!user) return;
    const id = url.searchParams.get('id');
    if (!id || id.length > 200 || !/^[a-zA-Z0-9:_-]+$/.test(id)) throw new HttpError(400, 'Invalid draft identifier.');
    if (!id.startsWith(`short-notes:${user.id}:`)) throw new HttpError(403, 'This draft belongs to a different account.');
    if (request.method === 'GET') return sendJson(response, 200, { record: await store.getDraft(user.id, id) });
    if (request.method !== 'PUT') return sendJson(response, 405, { message: 'Method not allowed.' });
    const body = await parseRequestBody(request);
    return sendJson(response, 200, { record: await store.putDraft(user.id, id, body.draft, body.revision) });
  };
}
