import { randomUUID } from "node:crypto";

// Use the same database and session authentication as the rest of the app.
export function createReviewHandler({ readDatabase, writeDatabase, getSessionUser, parseRequestBody, sendJson }) {
  function reviewSummary(database, user, page = 1) {
    const users = new Map(database.users.map(entry => [entry.id, entry]));
    const reviews = (database.websiteReviews ?? [])
      .filter(review => users.has(review.userId))
      .sort((a, b) => b.createdAt.localeCompare(a.createdAt));
    const serialize = review => ({
      id: review.id,
      name: users.get(review.userId)?.name || "MediComm learner",
      rating: review.rating,
      comment: review.comment,
      createdAt: review.createdAt,
      updatedAt: review.updatedAt,
    });
    const distribution = [0, 0, 0, 0, 0];
    reviews.forEach(review => { distribution[review.rating - 1] += 1; });
    const ownReview = reviews.find(review => review.userId === user?.id);
    return {
      total: reviews.length,
      average: reviews.length ? reviews.reduce((sum, review) => sum + review.rating, 0) / reviews.length : 0,
      distribution,
      reviews: reviews.slice((page - 1) * 12, page * 12).map(serialize),
      myReview: ownReview ? serialize(ownReview) : null,
      page,
      hasMore: page * 12 < reviews.length,
    };
  }

  return async function handleReviews(request, response, url) {
    if (request.method === "GET") {
      const database = readDatabase();
      const page = Number(url.searchParams.get("page") ?? 1);
      if (!Number.isSafeInteger(page) || page < 1 || page > 100000) {
        return sendJson(response, 400, { message: "Invalid review page." });
      }
      return sendJson(response, 200, reviewSummary(database, getSessionUser(request, database), page));
    }
    if (!["PUT", "DELETE"].includes(request.method)) {
      return sendJson(response, 405, { message: "Method not allowed." }, { Allow: "GET, PUT, DELETE" });
    }
    // Authenticate before reading a body, and read fresh state after that await.
    if (!getSessionUser(request, readDatabase())) {
      return sendJson(response, 401, { message: "Please sign in to rate MediComm." });
    }
    let payload;
    if (request.method === "PUT") {
      try { payload = await parseRequestBody(request); }
      catch { return sendJson(response, 400, { message: "Please send a valid review." }); }
      if (!payload || !Number.isInteger(payload.rating) || payload.rating < 1 || payload.rating > 5) {
        return sendJson(response, 400, { message: "Choose a rating from 1 to 5 stars." });
      }
      if (payload.comment !== undefined && typeof payload.comment !== "string") {
        return sendJson(response, 400, { message: "Your review must be text." });
      }
      if ((payload.comment ?? "").length > 1000) {
        return sendJson(response, 400, { message: "Keep your review within 1,000 characters." });
      }
    }
    const database = readDatabase();
    const user = getSessionUser(request, database);
    if (!user) return sendJson(response, 401, { message: "Please sign in to rate MediComm." });
    database.websiteReviews ??= [];
    const existing = database.websiteReviews.find(review => review.userId === user.id);
    database.websiteReviews = database.websiteReviews.filter(review => review.userId !== user.id);
    if (request.method === "PUT") {
      const now = new Date().toISOString();
      database.websiteReviews.push({
        id: existing?.id ?? randomUUID(),
        userId: user.id,
        rating: payload.rating,
        comment: (payload.comment ?? "").trim(),
        createdAt: existing?.createdAt ?? now,
        updatedAt: now,
      });
    }
    await writeDatabase(database);
    return sendJson(response, 200, reviewSummary(database, user));
  };
}
