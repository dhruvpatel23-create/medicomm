import { useCallback, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, Rows3, Columns3 } from 'lucide-react';

export default function TheoryAnswerDocument({ document }) {
  if (!document?.pages?.length) return null;

  const [pageIndex, setPageIndex] = useState(0);
  const [viewMode, setViewMode] = useState("swipe"); // "swipe" | "scroll"
  const touchRef = useRef(null);
  const containerRef = useRef(null);

  const pageCount = document.pages.length;

  const goTo = useCallback((idx) => {
    setPageIndex(Math.max(0, Math.min(pageCount - 1, idx)));
  }, [pageCount]);

  function handleTouchStart(e) {
    if (viewMode !== "swipe") return;
    const touch = e.touches[0];
    touchRef.current = { x: touch.clientX, y: touch.clientY, time: Date.now() };
  }

  function handleTouchEnd(e) {
    if (viewMode !== "swipe" || !touchRef.current) return;
    const touch = e.changedTouches[0];
    const dx = touch.clientX - touchRef.current.x;
    const dy = touch.clientY - touchRef.current.y;
    const dt = Date.now() - touchRef.current.time;
    touchRef.current = null;

    // Require horizontal swipe: dx > 60px, more horizontal than vertical, within 400ms
    if (Math.abs(dx) >= 60 && Math.abs(dx) > Math.abs(dy) * 1.5 && dt < 400) {
      if (dx < 0 && pageIndex < pageCount - 1) {
        goTo(pageIndex + 1);
      } else if (dx > 0 && pageIndex > 0) {
        goTo(pageIndex - 1);
      }
    }
  }

  function handlePointerSwipe(e) {
    if (viewMode !== "swipe" || e.pointerType === "touch") return;
    // Mouse/pen swipe handling via pointer events is handled through touch above
  }

  return (
    <section className="sn-answer-document" aria-label="Handwritten model answer">
      <header className="sn-answer-document-header">
        <div>
          <p className="sn-eyebrow">Exam-friendly answer</p>
          <h3>{document.title || "Model Answer"}</h3>
          <p>{document.description || "Methods of gene transfer & conjugation in detail"} · {document.pages.length} pages</p>
        </div>
        <div className="sn-doc-header-actions">
          {/* View mode toggle */}
          <div className="sn-view-toggle" role="radiogroup" aria-label="Page view mode">
            <button
              type="button"
              className={`sn-view-toggle-btn ${viewMode === "swipe" ? "is-active" : ""}`}
              aria-pressed={viewMode === "swipe"}
              onClick={() => setViewMode("swipe")}
              title="Swipe through pages"
            >
              <Columns3 size={14} />
              <span>Swipe</span>
            </button>
            <button
              type="button"
              className={`sn-view-toggle-btn ${viewMode === "scroll" ? "is-active" : ""}`}
              aria-pressed={viewMode === "scroll"}
              onClick={() => setViewMode("scroll")}
              title="Scroll through all pages"
            >
              <Rows3 size={14} />
              <span>Scroll</span>
            </button>
          </div>
          {document.pdf && (
            <a className="button button-secondary" href={document.pdf} target="_blank" rel="noreferrer">
              {document.managementPdf ? "Open original PDF" : "Open PDF"}
            </a>
          )}
          {document.managementPdf && (
            <a className="button button-secondary" href={document.managementPdf} target="_blank" rel="noreferrer">
              Open management PDF
            </a>
          )}
        </div>
      </header>

      {viewMode === "swipe" ? (
        /* ─── Swipe / Paginated View ─── */
        <div
          className="sn-answer-document-swipe"
          ref={containerRef}
          onTouchStart={handleTouchStart}
          onTouchEnd={handleTouchEnd}
        >
          <figure className="sn-swipe-page" key={pageIndex}>
            <a href={document.pages[pageIndex]} target="_blank" rel="noreferrer" aria-label={`Open answer page ${pageIndex + 1} at full size`}>
              <img
                src={document.pages[pageIndex]}
                alt={`Handwritten model answer: ${document.title || "Model Answer"}, page ${pageIndex + 1} of ${pageCount}`}
                width="2000"
                height="2828"
                loading="eager"
                decoding="async"
              />
            </a>
            <figcaption>Page {pageIndex + 1} of {pageCount} · Swipe or use arrows · Tap to enlarge</figcaption>
          </figure>

          {/* Page navigation controls */}
          <div className="sn-swipe-nav">
            <button
              type="button"
              className="sn-swipe-arrow"
              disabled={pageIndex === 0}
              onClick={() => goTo(pageIndex - 1)}
              aria-label="Previous page"
            >
              <ArrowLeft size={18} />
            </button>
            <span className="sn-swipe-counter" aria-live="polite">
              {pageIndex + 1} / {pageCount}
            </span>
            <button
              type="button"
              className="sn-swipe-arrow"
              disabled={pageIndex >= pageCount - 1}
              onClick={() => goTo(pageIndex + 1)}
              aria-label="Next page"
            >
              <ArrowRight size={18} />
            </button>
          </div>
        </div>
      ) : (
        /* ─── Vertical Scroll View ─── */
        <div className="sn-answer-document-pages sn-answer-scroll-view">
          {document.pages.map((src, index) => (
            <figure key={src}>
              <a href={src} target="_blank" rel="noreferrer" aria-label={`Open answer page ${index + 1} at full size`}>
                <img
                  src={src}
                  alt={`Handwritten model answer: ${document.title || "Model Answer"}, page ${index + 1} of ${document.pages.length}`}
                  width="2000"
                  height="2828"
                  loading={index === 0 ? "eager" : "lazy"}
                  decoding="async"
                />
              </a>
              <figcaption>Page {index + 1} of {document.pages.length} · Select the page to enlarge</figcaption>
            </figure>
          ))}
        </div>
      )}
    </section>
  );
}
