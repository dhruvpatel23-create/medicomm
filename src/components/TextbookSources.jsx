import "./TextbookSources.css";

export default function TextbookSources({ sources }) {
  if (!sources?.length) return null;
  return <section className="theory-textbook-sources" aria-label="Textbook references">
    <h4>Textbook references</h4>
    <ul>{sources.map((source, index) => <li key={`${source.book}-${index}`}>
      <strong>{source.book}</strong>{source.topic && <span>{source.topic}</span>}
    </li>)}</ul>
    <small>AI-selected textbook basis. Specific editions and pages have not been verified.</small>
  </section>;
}
