import { useState } from "react";
import { ArrowLeft, ArrowRight, BookOpen, CalendarDays, GraduationCap } from "lucide-react";

const years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025];

export default function FmgeYears({ onBack, sessions = [], progress = {}, status, onRetry, onStart, initialYear = null }) {
  const [selectedYear, setSelectedYear] = useState(initialYear);
  const loading = status === "idle" || status === "loading";
  const total = sessions.reduce((sum, session) => sum + session.questions.length, 0);
  const yearSessions = sessions.filter((session) => session.year === selectedYear);
  const answeredCount = (questions) => questions.filter((question) => progress[question.id]).length;
  return (
    <section className="app-view usmle-modules practice-path-teal" aria-labelledby="fmge-years-title">
      <header className="usmle-modules-hero">
        <div className="usmle-modules-topline">
          <span className="practice-path-icon"><GraduationCap size={28} strokeWidth={1.7} aria-hidden="true" /></span>
          <button type="button" className="button button-secondary usmle-modules-back" onClick={() => selectedYear ? setSelectedYear(null) : onBack()}><ArrowLeft size={16} aria-hidden="true" />{selectedYear ? "All years" : "Back"}</button>
        </div>
        <p className="usmle-modules-eyebrow">Medical licensing</p>
        <h2 id="fmge-years-title">FMGE {selectedYear || ""} <span>practice</span></h2>
        <p className="usmle-modules-intro">{selectedYear ? "Choose your exam session and start practising." : "Strengthen your foundations, one year at a time."}</p>
        <div className="usmle-modules-summary">
          <span><CalendarDays size={16} aria-hidden="true" />{selectedYear ? `${yearSessions.length} exam sessions` : "8 years · 2018–2025"}</span>
          <span><BookOpen size={16} aria-hidden="true" />{loading ? "Loading questions…" : `${selectedYear ? yearSessions.reduce((sum, session) => sum + session.questions.length, 0) : total} questions`}</span>
        </div>
      </header>
      <div className="usmle-modules-section-heading"><h3>{selectedYear ? "Choose a session" : "Your years"}</h3><p>Recall questions with images and explanations.</p></div>
      {status === "error" && <div className="card panel" role="status"><p>Unable to load FMGE questions.</p><button type="button" className="button button-secondary" onClick={onRetry}>Retry</button></div>}
      <div className="usmle-module-grid">
        {selectedYear ? yearSessions.map((session) => {
          const count = session.questions.length;
          const answered = answeredCount(session.questions);
          const parts = [...new Set(session.questions.map((question) => question.part).filter(Boolean))];
          return <article className="usmle-module-card" key={session.id} aria-labelledby={`${session.id}-title`}>
            <div className="usmle-module-topline"><span className="usmle-module-number" aria-hidden="true"><CalendarDays size={20} /></span><span className="usmle-module-status usmle-module-ready">Ready to practice</span></div>
            <h4 id={`${session.id}-title`}>{session.month} {session.year}</h4>
            <p className="usmle-module-description">{parts.length > 1 ? `Parts ${parts.join(" & ")} · ` : parts.length ? `Part ${parts[0]} · ` : ""}Questions, images and answer explanations.</p>
            <div className="usmle-module-footer"><span><BookOpen size={15} aria-hidden="true" />{count} questions</span><span>{answered} / {count} answered</span></div>
            <button type="button" className="usmle-module-start" onClick={() => onStart(session.id)} aria-label={`Start ${session.month} ${session.year}`}>{answered ? "Review session" : "Start practice"}<ArrowRight size={17} aria-hidden="true" /></button>
          </article>;
        }) : years.map((year) => {
          const available = sessions.filter((session) => session.year === year);
          const questions = available.flatMap((session) => session.questions);
          const count = questions.length;
          return (
          <article className="usmle-module-card" key={year} aria-labelledby={`fmge-year-${year}`}>
            <div className="usmle-module-topline">
              <span className="usmle-module-number" aria-hidden="true"><CalendarDays size={20} /></span>
              <span className={`usmle-module-status${count ? " usmle-module-ready" : ""}`}>{count ? "Ready to practice" : loading ? "Loading…" : status === "error" ? "Unavailable" : "Coming soon"}</span>
            </div>
            <h4 id={`fmge-year-${year}`}>{year}</h4>
            <p className="usmle-module-description">{available.length ? available.map((session) => session.month).join(" · ") : "FMGE practice questions"}</p>
            <div className="usmle-module-footer"><span><BookOpen size={15} aria-hidden="true" />{count} questions</span><span>{count ? `${answeredCount(questions)} / ${count} answered` : "No questions yet"}</span></div>
            {count > 0 && <button type="button" className="usmle-module-start" onClick={() => available.length > 1 ? setSelectedYear(year) : onStart(available[0].id)} aria-label={`Explore ${year}`}>{available.length > 1 ? "Choose session" : "Start practice"}<ArrowRight size={17} aria-hidden="true" /></button>}
          </article>
        );})}
      </div>
    </section>
  );
}
