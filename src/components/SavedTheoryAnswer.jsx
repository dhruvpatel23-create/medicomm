import { useState } from 'react';
import { ArrowLeft, ArrowRight, FileText } from 'lucide-react';

export default function SavedTheoryAnswer({ review }) {
  const [pageIndex, setPageIndex] = useState(0);
  const [failed, setFailed] = useState(false);
  const pages = review.answerPages || [];
  const page = pages[pageIndex];
  return <section className="sn-saved-answer" aria-label="Your saved answer">
    <p className="sn-eyebrow"><FileText size={15} /> Your answer library</p>
    <h3>Your saved answer</h3>
    {review.submittedAt && <p className="sn-saved-date">Saved {new Date(review.submittedAt).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' })}</p>}
    {review.answer && <div className="sn-saved-text">{review.answer}</div>}
    {page && <>
      <div className="sn-saved-page-nav">
        <button type="button" className="sn-back" disabled={pageIndex === 0} onClick={() => { setPageIndex(index => index - 1); setFailed(false); }}><ArrowLeft size={16} /> Previous page</button>
        <span aria-live="polite">Page {pageIndex + 1} of {pages.length}</span>
        <button type="button" className="sn-back" disabled={pageIndex === pages.length - 1} onClick={() => { setPageIndex(index => index + 1); setFailed(false); }}>Next page <ArrowRight size={16} /></button>
      </div>
      <figure className="sn-saved-page">
        {failed ? <p role="alert">This page could not load. <button type="button" onClick={() => setFailed(false)}>Try again</button></p>
          : <a href={page.imageUrl} target="_blank" rel="noreferrer" aria-label={`Open saved answer page ${pageIndex + 1} at full size`}><img src={page.imageUrl} alt={`Saved answer page ${pageIndex + 1}`} onError={() => setFailed(true)} /></a>}
        <figcaption>{page.source === 'notepad' ? 'Notepad' : 'Uploaded answer'} · Page {pageIndex + 1} · Open the page to view at full size</figcaption>
      </figure>
    </>}
    {review.hasImage && !pages.length && <p className="sn-notice">This earlier review did not store the submitted image. Any notepad draft still on this device can be opened below.</p>}
  </section>;
}
