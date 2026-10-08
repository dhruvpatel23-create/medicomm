import { useEffect, useRef, useState } from "react";
import { ArrowLeft, ArrowRight, BookOpen, Camera, Check, CheckCircle2, ChevronRight, FileText, Layers3, Loader2, Search, Sparkles, Star, Upload, X } from "lucide-react";
import { apiRequest } from "../lib/api";
import "./ShortNotes.css";
import AnswerNotepad from "./AnswerNotepad";
import TextbookSources from "./TextbookSources";

const typeLabel = (kind) => kind === "long-answer" ? "Long answer" : "Short note";
function loadDrafts(key) {
  try { const value = JSON.parse(localStorage.getItem(key) || "{}"); return value && typeof value === "object" && !Array.isArray(value) ? value : {}; }
  catch { return {}; }
}

export default function ShortNotes({ subjectId, subjectTitle, userId, onBack, prepareImage, onNavigate }) {
  const [bank, setBank] = useState(null);
  const [loadError, setLoadError] = useState("");
  const [reload, setReload] = useState(0);
  const [topicId, setTopicId] = useState("");
  const [questionId, setQuestionId] = useState("");
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");
  const [starred, setStarred] = useState(false);
  const [reviews, setReviews] = useState({});
  const [reviewLoadError, setReviewLoadError] = useState("");
  const draftKey = `medicomm-short-note-drafts:${userId || "guest"}`;
  const [drafts, setDrafts] = useState(() => loadDrafts(draftKey));
  const [draftError, setDraftError] = useState("");
  const [answerImage, setAnswerImage] = useState(null);
  const [imageBusy, setImageBusy] = useState(false);
  const [busy, setBusy] = useState(false);
  const [privacyAccepted, setPrivacyAccepted] = useState(false);
  const [message, setMessage] = useState("");
  const mounted = useRef(true);
  const titleRef = useRef(null);
  const signedIn = Boolean(userId);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  useEffect(() => {
    const controller = new AbortController();
    setLoadError("");
    fetch("/short-notes.json", { signal: controller.signal }).then(response => {
      if (!response.ok) throw new Error("The question library could not be loaded.");
      return response.json();
    }).then(data => {
      if (!Array.isArray(data.subjects)) throw new Error("The question library is unavailable.");
      setBank(data);
    }).catch(error => { if (error.name !== "AbortError") setLoadError(error.message); });
    return () => controller.abort();
  }, [reload]);
  useEffect(() => {
    let active = true;
    if (signedIn) apiRequest("/api/short-notes/reviews").then(data => {
      if (active) { setReviews(Object.fromEntries((data.reviews || []).map(review => [review.questionId, review]))); setReviewLoadError(""); }
    }).catch(() => { if (active) setReviewLoadError("Saved reviews could not be loaded. You can still write an answer."); });
    return () => { active = false; };
  }, [signedIn, userId, reload]);
  useEffect(() => {
    try { localStorage.setItem(draftKey, JSON.stringify(drafts)); setDraftError(""); }
    catch { setDraftError("This browser could not save your draft. Keep this page open while writing."); }
  }, [draftKey, drafts]);
  useEffect(() => { onNavigate(); titleRef.current?.focus({ preventScroll: true }); }, [topicId, questionId]);

  const subject = bank?.subjects.find(item => item.id === subjectId);
  const topic = subject?.topics.find(item => item.id === topicId);
  const question = topic?.questions.find(item => item.id === questionId);
  const allQuestions = subject?.topics.flatMap(item => item.questions) ?? [];
  const totalReviewed = allQuestions.filter(item => reviews[item.id]).length;
  const topicReviewed = topic?.questions.filter(item => reviews[item.id]).length ?? 0;
  const review = question && !Object.hasOwn(drafts, question.id) && reviews[question.id];
  const draft = question && typeof drafts[question.id] === "string" ? drafts[question.id] : "";
  const locked = busy || imageBusy;
  const normalizedSearch = search.toLowerCase().trim();
  const visibleQuestions = topic?.questions.filter(item =>
    item.prompt.toLowerCase().includes(normalizedSearch)
    && (filter === "all" || filter === item.kind || (filter === "unreviewed" && !reviews[item.id]))
    && (!starred || item.emphasis > 0)) ?? [];
  const visibleTopics = subject?.topics.filter(item => item.title.toLowerCase().includes(normalizedSearch)
    || item.questions.some(q => q.prompt.toLowerCase().includes(normalizedSearch))) ?? [];

  function openQuestion(id) {
    if (locked) return;
    setQuestionId(id); setAnswerImage(null); setMessage(""); setPrivacyAccepted(false);
  }
  function backToList() { if (!locked) { setQuestionId(""); setAnswerImage(null); setMessage(""); } }
  async function pickImage(event) {
    const file = event.target.files?.[0]; event.target.value = "";
    if (!file || locked) return;
    setImageBusy(true); setMessage("");
    try { const image = await prepareImage(file); if (mounted.current) setAnswerImage(image); }
    catch (error) { if (mounted.current) setMessage(error.message); }
    finally { if (mounted.current) setImageBusy(false); }
  }
  async function submitAnswer(event) {
    event.preventDefault();
    if (!question || locked || !privacyAccepted || (!answerImage && draft.trim().length < 3)) return;
    setBusy(true); setMessage("");
    try {
      const data = await apiRequest("/api/short-notes/reviews", { method: "POST", timeoutMs: 150000,
        body: JSON.stringify({ questionId: question.id, answer: draft, answerImageDataUrl: answerImage?.dataUrl ?? null, privacyAccepted: true }) });
      if (mounted.current) {
        setReviews(current => ({ ...current, [question.id]: data.review })); setAnswerImage(null);
        setDrafts(current => { const next = { ...current }; delete next[question.id]; return next; });
        onNavigate();
      }
    } catch (error) { if (mounted.current) setMessage(error.message); }
    finally { if (mounted.current) setBusy(false); }
  }

  const backButton = <button className="sn-back" type="button" onClick={onBack} disabled={locked}><ArrowLeft size={16} /> Back to subjects</button>;
  if (!bank) return <section className="app-view short-notes-view">{backButton}<div className="sn-empty" role={loadError ? "alert" : "status"}>
    {loadError ? <><h2>Questions couldn't load</h2><p>{loadError}</p><button className="button button-primary" onClick={() => setReload(value => value + 1)}>Try again</button></> : <><Loader2 className="sn-spin" /><p>Opening your theory library...</p></>}
  </div></section>;
  if (!subject) return <section className="app-view short-notes-view">{backButton}<div className="sn-empty"><BookOpen size={32} /><h2>{subjectTitle} short notes</h2><p>Questions for this subject haven't been added yet.</p></div></section>;

  return <section className="app-view short-notes-view">
    <nav className="sn-breadcrumbs" aria-label="Short notes navigation">
      <button type="button" onClick={onBack} disabled={locked}>Theory</button><ChevronRight size={14} />
      <button type="button" disabled={locked} onClick={() => { setTopicId(""); setQuestionId(""); setSearch(""); setAnswerImage(null); }}>{subject.title}</button>
      <ChevronRight size={14} /><span>Short Notes</span>
      {topic && <><ChevronRight size={14} /><button type="button" onClick={backToList} disabled={locked}>{topic.title}</button></>}
    </nav>
    {reviewLoadError && <p className="sn-notice" role="status">{reviewLoadError} <button type="button" onClick={() => setReload(value => value + 1)}>Retry</button></p>}

    {question ? <>
      <div className="sn-answer-heading">
        <button className="sn-back" type="button" onClick={backToList} disabled={locked}><ArrowLeft size={16} /> Back to questions</button>
        <span>Question {topic.questions.indexOf(question) + 1} of {topic.questions.length}</span>
      </div>
      <article className="sn-prompt-card">
        <div className="sn-question-meta"><span className="sn-badge">{typeLabel(question.kind)}</span>{question.emphasis > 0 && <span className="sn-star-label"><Star size={13} /> Starred in source</span>}<span>{topic.title}</span></div>
        <h2 ref={titleRef} tabIndex={-1}>{question.prompt}</h2>
        <div className="sn-source"><BookOpen size={14} /> {(bank.sources?.find(source => source.id === subject.sourceId) || bank.source).title} · PDF page {question.sourcePage}<span>AI practice review / 10</span></div>
      </article>
      {review ? <article className="card panel sn-review" aria-live="polite">
        <div className="sn-review-top"><div className="sn-score"><strong>{review.score}</strong><span>/ 10</span></div><div><p className="sn-eyebrow"><Sparkles size={14} /> AI theory review</p><h3>{review.feedback}</h3></div></div>
        <div className="sn-feedback-grid"><section><h4><CheckCircle2 size={17} /> What you did well</h4>{review.strengths?.length ? <ul>{review.strengths.map((point, i) => <li key={i}>{point}</li>)}</ul> : <p>Use the suggestions alongside to build a stronger answer.</p>}</section><section><h4>How to improve</h4><ul>{review.improvements?.map((point, i) => <li key={i}>{point}</li>)}</ul></section></div>
        <section className="sn-model-answer"><p className="sn-eyebrow">Learn from your answer</p><h3>Exam-ready model answer</h3>{review.modelAnswerSections?.map((section, i) => <div key={i}><h4>{section.heading}</h4><ul>{section.points.map((point, index) => <li key={index}>{point}</li>)}</ul>{section.flowchart && <p className="sn-flowchart">{section.flowchart}</p>}</div>)}<small>AI-generated study feedback. Check important details against your textbook.</small></section>
        <TextbookSources sources={review.textbookSources} />
        <details className="sn-submitted"><summary>Your submitted answer</summary>{review.answer && <p>{review.answer}</p>}{review.hasImage && <p>Your written-answer photo was included in this review.</p>}</details>
        <AnswerNotepad key={question.id} draftId={`short-notes:${userId || "guest"}:${question.id}`} prompt={question.prompt} />
        <div className="sn-review-actions"><span><CheckCircle2 size={15} /> Review saved</span><button className="button button-secondary" type="button" onClick={() => { setDrafts(current => ({ ...current, [question.id]: "" })); setPrivacyAccepted(false); }}>Practise again</button></div>
      </article> : <form className="sn-writing-layout" onSubmit={submitAnswer}>
        <article className="sn-editor">
          <div className="sn-editor-heading"><h3><FileText size={19} /> Your answer</h3><span>{draftError ? "Draft not saved" : draft ? "Draft saved on this device" : "Make this concept yours"}</span></div>
          <label htmlFor="short-note-answer" className="sr-only">Your theory answer</label>
          <textarea id="short-note-answer" value={draft} onChange={event => setDrafts(current => ({ ...current, [question.id]: event.target.value }))} maxLength={8000} rows={15} disabled={locked} placeholder="Start with a brief introduction, then organise your answer under clear headings. Include a labelled diagram where asked." />
          <div className="sn-editor-footer"><span>Use headings, key points, and relevant examples.</span><span>{draft.length.toLocaleString()} / 8,000</span></div>
          {draftError && <p className="form-message" role="status">{draftError}</p>}
        </article>
        <aside className="sn-answer-aside">
          <section className="sn-upload-card"><span className="sn-aside-icon"><Camera size={22} /></span><h3>Prefer pen & paper?</h3><p>Write your answer, then upload a clear photo for the same AI review.</p>
            {answerImage ? <div className="sn-photo"><img src={answerImage.dataUrl} alt="Your handwritten answer" /><span>{answerImage.name}</span><button type="button" onClick={() => setAnswerImage(null)} disabled={locked}><X size={14} /> Remove photo</button></div> : <div className="sn-upload-actions">
              <label className={`button button-secondary ${locked ? "sn-disabled" : ""}`}><Upload size={15} /> Upload answer<input type="file" accept="image/jpeg,image/png,image/webp,image/heic,image/heif" onChange={pickImage} disabled={locked} /></label>
              <label className={`sn-camera-link ${locked ? "sn-disabled" : ""}`}><Camera size={15} /> Take a photo<input type="file" accept="image/*" capture="environment" onChange={pickImage} disabled={locked} /></label>
            </div>}
            {imageBusy && <p role="status"><Loader2 size={15} className="sn-spin" /> Preparing photo...</p>}<small>JPG, PNG or WebP · up to 12 MB</small>
          </section>
          <AnswerNotepad key={question.id} draftId={`short-notes:${userId || "guest"}:${question.id}`} prompt={question.prompt} disabled={locked} hasImage={Boolean(answerImage)} onSave={image => { setAnswerImage(image); setMessage("Notepad answer attached. You can now submit it for AI review."); }} />
          <section className="sn-review-info"><Sparkles size={19} /><h3>A little feedback goes a long way.</h3><p>Get a score, specific improvements, and a structured model answer.</p><span>Medical accuracy · Coverage · Structure</span></section>
        </aside>
        <div className="sn-submit-area">
          {!signedIn && <p className="sn-notice">You can write and save a draft as a guest. Sign in to submit it for AI review.</p>}
          <label className="sn-consent"><input type="checkbox" checked={privacyAccepted} onChange={event => setPrivacyAccepted(event.target.checked)} disabled={locked} /><span>I agree to send this answer and any photo to Gemini for review. I haven't included patient-identifying information.</span></label>
          {message && <p className="form-message" role="alert">{message}</p>}
          <div className="sn-submit-row"><span>{busy ? "Reviewing your answer. This can take a little time..." : "Your own words. A clearer understanding."}</span><button className="button button-primary sn-submit" type="submit" disabled={!signedIn || locked || !privacyAccepted || (!answerImage && draft.trim().length < 3)}>{busy ? <Loader2 className="sn-spin" size={17} /> : <Sparkles size={17} />}{busy ? "Reviewing answer..." : "Submit for AI review"}</button></div>
        </div>
      </form>}
      <div className="sn-question-pagination"><button className="sn-back" type="button" disabled={locked || topic.questions[0].id === question.id} onClick={() => openQuestion(topic.questions[topic.questions.indexOf(question) - 1].id)}><ArrowLeft size={16} /> Previous question</button><button className="sn-back" type="button" disabled={locked || topic.questions.at(-1).id === question.id} onClick={() => openQuestion(topic.questions[topic.questions.indexOf(question) + 1].id)}>Next question <ArrowRight size={16} /></button></div>
    </> : <>
      <header className="sn-hero">
        <div className="sn-hero-copy"><p className="sn-eyebrow"><BookOpen size={15} /> Theory / Short Notes</p><h2 ref={titleRef} tabIndex={-1}>{topic ? topic.title : <>{subject.title}<span>One concept at a time.</span></>}</h2><p>{topic ? "Choose a question. Write your answer. Get feedback that helps it stick." : "Build answers worth remembering. Choose a topic to begin your theory practice."}</p></div>
        <div className="sn-progress-summary"><span className="sn-progress-icon"><Layers3 size={24} /></span><strong>{topic ? topicReviewed : totalReviewed}<span> / {topic ? topic.questions.length : allQuestions.length}</span></strong><small>questions reviewed</small><div className="sn-progress-track"><span style={{ width: `${100 * (topic ? topicReviewed / topic.questions.length : totalReviewed / allQuestions.length)}%` }} /></div></div>
      </header>
      <div className="sn-section-heading"><div><h3>{topic ? "Theory questions" : "Explore topics"}</h3><p>{topic ? `${visibleQuestions.length} of ${topic.questions.length} questions` : `${subject.topics.length} topics · ${allQuestions.length} questions · ${(bank.sources?.find(source => source.id === subject.sourceId) || bank.source).title}`}</p></div><button className="sn-back" type="button" onClick={topic ? () => { setTopicId(""); setSearch(""); setFilter("all"); setStarred(false); } : onBack}><ArrowLeft size={15} /> {topic ? "All topics" : "Subjects"}</button></div>
      <div className="sn-toolbar"><label className="sn-search"><Search size={18} /><input aria-label={topic ? "Search questions" : "Search topics or questions"} value={search} onChange={event => setSearch(event.target.value)} placeholder={topic ? "Find a question in this topic..." : "Find a topic or concept..."} />{search && <button type="button" aria-label="Clear search" onClick={() => setSearch("")}><X size={16} /></button>}</label>
        {topic && <button className={`sn-filter-star ${starred ? "is-active" : ""}`} type="button" aria-pressed={starred} onClick={() => setStarred(value => !value)}><Star size={15} /> Starred in source</button>}
      </div>
      {topic ? <>
        <div className="sn-filters" aria-label="Filter questions">{[["all", "All questions"], ["short-note", "Short notes"], ["long-answer", "Long answers"], ["unreviewed", "To practise"]].map(([value, label]) => <button key={value} type="button" aria-pressed={filter === value} className={filter === value ? "is-active" : ""} onClick={() => setFilter(value)}>{label}</button>)}</div>
        <div className="sn-question-list">{visibleQuestions.map(item => <button className={`sn-question-row ${reviews[item.id] ? "is-reviewed" : ""}`} type="button" key={item.id} onClick={() => openQuestion(item.id)}>
          <span className="sn-row-number">{reviews[item.id] ? <Check size={19} /> : String(topic.questions.indexOf(item) + 1).padStart(2, "0")}</span>
          <span className="sn-row-body"><span className="sn-row-meta"><span>{typeLabel(item.kind)}</span>{item.emphasis > 0 && <span className="sn-star-label" title={`${item.emphasis} source stars`}><Star size={12} /> {item.emphasis > 1 ? `${item.emphasis} stars` : "Starred"}</span>}<span>PDF p. {item.sourcePage}</span></span><strong>{item.prompt}</strong></span>
          <span className="sn-row-action">{reviews[item.id] ? <span>{reviews[item.id].score}/10</span> : <span>{drafts[item.id] ? "Continue" : "Write answer"}</span>}<ArrowRight size={18} /></span>
        </button>)}</div>
        {!visibleQuestions.length && <div className="sn-empty"><Search size={28} /><h3>No matching questions</h3><p>Try another keyword or reset your filters.</p><button className="button button-secondary" onClick={() => { setSearch(""); setFilter("all"); setStarred(false); }}>Reset filters</button></div>}
      </> : <div className="sn-topic-grid">{visibleTopics.map((item) => {
        const reviewed = item.questions.filter(q => reviews[q.id]).length;
        return <button className="sn-topic-card" type="button" key={item.id} onClick={() => { setTopicId(item.id); setSearch(""); setFilter("all"); setStarred(false); }}><span className="sn-topic-top"><span className="sn-topic-number">{String(subject.topics.indexOf(item) + 1).padStart(2, "0")}</span><ArrowRight size={18} /></span><h4>{item.title}</h4><p>{item.questions.length} questions<span>{item.questions.filter(q => q.kind === "long-answer").length} long answers</span></p><div className="sn-progress-track"><span style={{ width: `${100 * reviewed / item.questions.length}%` }} /></div><small>{reviewed ? `${reviewed} reviewed` : "Ready when you are"}</small></button>;
      })}{!visibleTopics.length && <div className="sn-empty"><h3>No matching topics</h3><p>Try another topic or question keyword.</p></div>}</div>}
      <p className="sn-library-footer"><BookOpen size={14} /> Questions from {(bank.sources?.find(source => source.id === subject.sourceId) || bank.source).title}. Star markers follow the original PDF.</p>
    </>}
  </section>;
}
