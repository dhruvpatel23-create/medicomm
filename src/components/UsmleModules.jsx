import { ArrowLeft, ArrowRight, BookOpen, Globe2, Layers3 } from "lucide-react";

export default function UsmleModules({ onBack, modules = [], progress = {}, status, onRetry, onStart }) {
  const totalQuestions = modules.reduce((total, module) => total + module.questions.length, 0);
  const loading = status === "idle" || status === "loading";
  const unavailable = status === "error" || (!loading && !modules.length);
  return (
    <section className="app-view usmle-modules practice-path-red" aria-labelledby="usmle-modules-title">
      <header className="usmle-modules-hero">
        <div className="usmle-modules-topline">
          <span className="practice-path-icon"><Globe2 size={28} strokeWidth={1.7} aria-hidden="true" /></span>
          <button type="button" className="button button-secondary usmle-modules-back" onClick={onBack}><ArrowLeft size={16} aria-hidden="true" />Back</button>
        </div>
        <p className="usmle-modules-eyebrow">Your global pathway</p>
        <h2 id="usmle-modules-title">USMLE Step 1 <span>practice</span></h2>
        <p className="usmle-modules-intro">Build your foundation, one module at a time.</p>
        <div className="usmle-modules-summary"><span><Layers3 size={16} aria-hidden="true" />10 modules</span><span><BookOpen size={16} aria-hidden="true" />{loading ? "Loading questions…" : `${totalQuestions} questions`}</span></div>
      </header>
      <div className="usmle-modules-section-heading"><h3>Your modules</h3><p>Mixed concepts. Connected clinical reasoning.</p></div>
      {unavailable && <div className="card panel" role="status"><p>Unable to load the modules.</p><button className="button button-secondary" type="button" onClick={onRetry}>Retry</button></div>}
      <div className="usmle-module-grid">
        {Array.from({ length: 10 }, (_, index) => {
          const module = modules.find((entry) => entry.moduleNumber === index + 1);
          const count = module?.questions.length ?? 0;
          const answered = module?.questions.filter((question) => progress[question.id]).length ?? 0;
          return (
          <article className="usmle-module-card" key={index} aria-labelledby={`usmle-module-${index + 1}`}>
            <div className="usmle-module-topline"><span className="usmle-module-number" aria-hidden="true">{String(index + 1).padStart(2, "0")}</span><span className={`usmle-module-status${count ? " usmle-module-ready" : ""}`}>{count ? "Ready to practice" : loading ? "Loading…" : unavailable ? "Unavailable" : "Coming soon"}</span></div>
            <h4 id={`usmle-module-${index + 1}`}>Module {index + 1}</h4>
            {count > 0 && <p className="usmle-module-description">An integrated mix across basic sciences and clinical systems.</p>}
            <div className="usmle-module-footer"><span><BookOpen size={15} aria-hidden="true" />{count} questions</span><span>{count ? `${answered} / ${count} answered` : "No questions yet"}</span></div>
            {count > 0 && <button type="button" className="usmle-module-start" onClick={() => onStart(module.id)} aria-label={`${answered ? "Review" : "Start"} Module ${index + 1}`}>{answered ? "Review module" : "Start module"}<ArrowRight size={17} aria-hidden="true" /></button>}
          </article>
        );})}
      </div>
    </section>
  );
}
