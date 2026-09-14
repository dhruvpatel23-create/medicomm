import assert from "node:assert/strict";
import { createServer } from "node:http";
import { randomUUID } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync, unlinkSync } from "node:fs";
import path from "node:path";
import { createReviewHandler } from "../server/reviews.mjs";

// Isolated storage: no app accounts, sessions, or reviews are changed.
mkdirSync("tmp", { recursive: true });
const filename = path.resolve("tmp", `reviews-check-${randomUUID()}.json`);
writeFileSync(filename, JSON.stringify({ users: [{ id: "a", name: "Learner A", email: "private@example.test" }, { id: "b", name: "Learner B" }], websiteReviews: [] }));
const handler = createReviewHandler({
  readDatabase: () => JSON.parse(readFileSync(filename, "utf8")),
  writeDatabase: async database => writeFileSync(filename, JSON.stringify(database)),
  getSessionUser: (request, database) => database.users.find(user => `Bearer test-${user.id}` === request.headers.authorization),
  parseRequestBody: async request => { const chunks = []; for await (const chunk of request) chunks.push(chunk); return JSON.parse(Buffer.concat(chunks).toString()); },
  sendJson: (response, status, data, headers = {}) => { response.writeHead(status, { "Content-Type": "application/json", ...headers }); response.end(JSON.stringify(data)); },
});
const server = createServer((request, response) => handler(request, response, new URL(request.url, "http://localhost")).catch(error => { response.writeHead(500); response.end(error.message); }));
await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
const base = `http://127.0.0.1:${server.address().port}/api/reviews`;
async function call(method = "GET", payload, user, query = "") {
  const response = await fetch(base + query, { method, headers: { "Content-Type": "application/json", ...(user ? { Authorization: `Bearer test-${user}` } : {}) }, ...(payload !== undefined ? { body: JSON.stringify(payload) } : {}) });
  return { status: response.status, data: await response.json() };
}
try {
  let result = await call();
  assert.equal(result.data.total, 0);
  assert.equal(result.data.average, 0);
  assert.equal((await call("PUT", { rating: 5 })).status, 401);
  assert.equal((await call("DELETE")).status, 401);
  for (const rating of [0, 6, 1.5, "5", null]) assert.equal((await call("PUT", { rating }, "a")).status, 400);
  assert.equal((await call("PUT", { rating: 5, comment: 42 }, "a")).status, 400);
  assert.equal((await call("PUT", { rating: 5, comment: "x".repeat(1001) }, "a")).status, 400);
  assert.equal((await call("GET", undefined, undefined, "?page=0")).status, 400);
  assert.equal((await call("POST", {}, "a")).status, 405);
  result = await call("PUT", { rating: 5, comment: "  Helpful practice.  ", userId: "b" }, "a");
  assert.equal(result.status, 200);
  assert.equal(result.data.total, 1);
  assert.equal(result.data.myReview.name, "Learner A");
  assert.equal(result.data.myReview.comment, "Helpful practice.");
  const reviewId = result.data.myReview.id;
  const createdAt = result.data.myReview.createdAt;
  // A fresh read from disk confirms persistence rather than component-only state.
  assert.equal(JSON.parse(readFileSync(filename)).websiteReviews[0].userId, "a");
  result = await call("PUT", { rating: 3, comment: "Updated feedback." }, "a");
  assert.equal(result.data.total, 1);
  assert.equal(result.data.myReview.id, reviewId);
  assert.equal(result.data.myReview.createdAt, createdAt);
  await call("PUT", { rating: 5 }, "b");
  result = await call();
  assert.equal(result.data.average, 4);
  assert.deepEqual(result.data.distribution, [0, 0, 1, 0, 1]);
  assert.equal(result.data.myReview, null);
  assert.ok(!JSON.stringify(result.data).includes("private@example.test"));
  assert.ok(result.data.reviews.every(review => !("userId" in review)));
  // DELETE always addresses the authenticated user's own review.
  await call("DELETE", { id: reviewId, userId: "a" }, "b");
  result = await call();
  assert.equal(result.data.total, 1);
  assert.equal(result.data.reviews[0].id, reviewId);
  await call("DELETE", undefined, "a");
  assert.equal((await call()).data.total, 0);
  const database = JSON.parse(readFileSync(filename));
  for (let i = 0; i < 15; i++) {
    database.users.push({ id: `page-${i}`, name: `Learner ${i}` });
    database.websiteReviews.push({ id: `review-${i}`, userId: `page-${i}`, rating: 4, comment: "", createdAt: new Date(2026, 0, i + 1).toISOString(), updatedAt: new Date(2026, 0, i + 1).toISOString() });
  }
  writeFileSync(filename, JSON.stringify(database));
  const first = (await call()).data;
  const second = (await call("GET", undefined, undefined, "?page=2")).data;
  assert.equal(first.reviews.length, 12);
  assert.equal(first.hasMore, true);
  assert.equal(second.reviews.length, 3);
  assert.equal(second.hasMore, false);
  assert.equal(new Set([...first.reviews, ...second.reviews].map(review => review.id)).size, 15);
  assert.equal(second.average, 4);
  console.log("Reviews API passed: authentication, validation, create/edit/delete, ownership, persistence, averages, privacy, and pagination.");
} finally {
  await new Promise(resolve => server.close(resolve));
  unlinkSync(filename);
}
