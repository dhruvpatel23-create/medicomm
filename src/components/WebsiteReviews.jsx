import { useEffect, useState } from "react";
import { Star } from "lucide-react";
import { apiRequest } from "../lib/api";

const ratingLabels = ["Poor", "Fair", "Good", "Very good", "Excellent"];

function Stars({ rating }) {
  return <span className="review-stars" role="img" aria-label={`${Number(rating.toFixed(1))} out of 5 stars`}>
    {[1, 2, 3, 4, 5].map(value => <span className="review-star" key={value} aria-hidden="true"><Star size={16} /><span style={{ width: `${Math.max(0, Math.min(1, rating - value + 1)) * 100}%` }}><Star size={16} fill="currentColor" /></span></span>)}
  </span>;
}

export default function WebsiteReviews({ canReview, onSignIn, compact = false, onViewAll }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState("");
  const [editing, setEditing] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [retry, setRetry] = useState(0);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    apiRequest("/api/reviews").then(result => {
      if (!active) return;
      setData(result);
      setRating(result.myReview?.rating ?? 0);
      setComment(result.myReview?.comment ?? "");
    }).catch(err => { if (active) setError(err.message); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [retry, canReview]);

  async function save(event) {
    event.preventDefault();
    if (!rating || busy) return;
    setBusy(true); setError(""); setMessage("");
    try {
      const result = await apiRequest("/api/reviews", { method: "PUT", body: JSON.stringify({ rating, comment }) });
      setData(result); setEditing(false); setConfirmDelete(false);
      setComment(result.myReview.comment);
      setMessage("Thank you! Your rating has been saved.");
    } catch (err) { setError(err.message); }
    finally { setBusy(false); }
  }

  async function remove() {
    setBusy(true); setError(""); setMessage("");
    try {
      const result = await apiRequest("/api/reviews", { method: "DELETE" });
      setData(result); setRating(0); setComment(""); setEditing(false); setConfirmDelete(false);
      setMessage("Your review has been deleted.");
    } catch (err) { setError(err.message); }
    finally { setBusy(false); }
  }

  async function loadMore() {
    setLoadingMore(true); setError("");
    try {
      const result = await apiRequest(`/api/reviews?page=${data.page + 1}`);
      setData(previous => ({ ...result, reviews: [...new Map([...previous.reviews, ...result.reviews].map(review => [review.id, review])).values()] }));
    } catch (err) { setError(err.message); }
    finally { setLoadingMore(false); }
  }

  const reviews = compact ? data?.reviews.slice(0, 3) : data?.reviews;
  return <section className={`website-reviews${compact ? " website-reviews-home" : ""}`} aria-label="MediComm ratings and reviews">
    <div className="reviews-heading"><div><p className="eyebrow">From our learners</p><h2>Ratings & reviews</h2><p>Share your experience with MediComm.</p></div>
      {compact && <button className="button button-secondary" onClick={onViewAll}>View all reviews</button>}
    </div>
    {loading ? <p role="status" className="card reviews-notice">Loading reviews…</p> : !data ? <div className="card reviews-notice"><p role="alert">{error}</p><button className="button button-secondary" onClick={() => setRetry(value => value + 1)}>Try again</button></div> : <>
      <div className="reviews-overview">
        <div className="card reviews-summary">
          <div><strong className="reviews-average">{data.total ? data.average.toFixed(1) : "—"}</strong><Stars rating={data.average} /><p>{data.total ? `${data.total} ${data.total === 1 ? "rating" : "ratings"}` : "No ratings yet"}</p></div>
          <div className="reviews-distribution" aria-label="Rating distribution">{[5, 4, 3, 2, 1].map(value => <div key={value}><span>{value} <span aria-hidden="true">★</span></span><meter min="0" max={data.total || 1} value={data.distribution[value - 1]} aria-label={`${value} stars: ${data.distribution[value - 1]} ratings`} /><span>{data.distribution[value - 1]}</span></div>)}</div>
        </div>
        <div className="card reviews-compose">
          {!canReview ? <><h3>How is your experience?</h3><p>Sign in to leave a rating or write a review.</p><button className="button button-primary" onClick={onSignIn}>Sign in to review</button></> : data.myReview && !editing ? <>
            <h3>Your review</h3><Stars rating={data.myReview.rating} />{data.myReview.comment && <p className="review-comment">{data.myReview.comment}</p>}
            {confirmDelete ? <div className="reviews-actions"><span>Delete your rating and review?</span><button className="button button-secondary" disabled={busy} onClick={() => setConfirmDelete(false)}>Keep review</button><button className="button button-secondary" disabled={busy} onClick={remove}>{busy ? "Deleting…" : "Delete review"}</button></div> : <div className="reviews-actions"><button className="button button-secondary" disabled={loadingMore} onClick={() => setEditing(true)}>Edit review</button><button className="text-button" disabled={loadingMore} onClick={() => setConfirmDelete(true)}>Delete</button></div>}
          </> : <form onSubmit={save}>
            <h3>{data.myReview ? "Edit your review" : "Rate your experience"}</h3>
            <fieldset className="review-rating-picker" disabled={busy}><legend>Your rating</legend><div>{ratingLabels.map((label, index) => <label key={label} title={label}>
              <input type="radio" name="website-rating" value={index + 1} checked={rating === index + 1} onChange={() => setRating(index + 1)} required aria-label={`${index + 1} ${index === 0 ? "star" : "stars"}: ${label}`} />
              <Star size={26} fill={rating > index ? "currentColor" : "none"} aria-hidden="true" />
            </label>)}</div><span aria-live="polite">{rating ? ratingLabels[rating - 1] : "Choose 1–5 stars"}</span></fieldset>
            <label className="review-comment-field"><span>Your review <small>(optional)</small></span><textarea value={comment} onChange={event => setComment(event.target.value)} maxLength={1000} rows={3} disabled={busy} placeholder="What’s working well? What could be better?" /><small>{comment.length}/1,000 characters</small></label>
            <p className="reviews-public-note">Your name, rating and review will be public. One rating per account.</p>
            <div className="reviews-actions"><button className="button button-primary" disabled={!rating || busy}>{busy ? "Saving…" : data.myReview ? "Save changes" : "Submit rating"}</button>{data.myReview && <button type="button" className="button button-secondary" disabled={busy} onClick={() => { setEditing(false); setRating(data.myReview.rating); setComment(data.myReview.comment); }}>Cancel</button>}</div>
          </form>}
        </div>
      </div>
      {error && <p role="alert" className="reviews-error">{error}</p>}
      {message && <p role="status" className="reviews-message">{message}</p>}
      {reviews.length ? <div className="reviews-list">{reviews.map(review => <article className="card review-card" key={review.id}>
        <div className="review-author"><span className="review-avatar" aria-hidden="true">{review.name.slice(0, 1).toUpperCase()}</span><div><strong>{review.name}</strong><time dateTime={review.createdAt}>{new Date(review.createdAt).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" })}{review.updatedAt !== review.createdAt ? " · Edited" : ""}</time></div></div>
        <Stars rating={review.rating} />{review.comment ? <p className="review-comment">{review.comment}</p> : <p className="reviews-public-note">Rated MediComm</p>}
      </article>)}</div> : <p className="reviews-empty">Be the first to share your experience.</p>}
      {!compact && data.hasMore && <button className="button button-secondary reviews-load-more" disabled={loadingMore || busy || editing || confirmDelete} onClick={loadMore}>{loadingMore ? "Loading…" : "Load more reviews"}</button>}
    </>}
  </section>;
}
