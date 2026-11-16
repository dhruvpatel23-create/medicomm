export default function TheoryAnswerDocument({ document }) {
  if (!document?.pages?.length) return null;
  return <section className="sn-answer-document" aria-label="Handwritten model answer">
    <header className="sn-answer-document-header">
      <div><p className="sn-eyebrow">Exam-friendly answer</p><h3>{document.title || "Gene Transfer in Bacteria"}</h3><p>{document.description || "Methods of gene transfer & conjugation in detail"} · {document.pages.length} pages</p></div>
      <a className="button button-secondary" href={document.pdf} target="_blank" rel="noreferrer">Open / download PDF</a>
    </header>
    <div className="sn-answer-document-pages">{document.pages.map((src, index) => <figure key={src}>
      <a href={src} target="_blank" rel="noreferrer" aria-label={`Open answer page ${index + 1} at full size`}><img src={src} alt={`Handwritten model answer: ${document.title || "Gene Transfer in Bacteria"}, page ${index + 1} of ${document.pages.length}`} width="2000" height="2828" loading={index === 0 ? "eager" : "lazy"} decoding="async" /></a>
      <figcaption>Page {index + 1} of {document.pages.length} · Select the page to enlarge</figcaption>
    </figure>)}</div>
  </section>;
}
