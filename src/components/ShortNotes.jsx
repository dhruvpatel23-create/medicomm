import { prepareTheoryImage, imageBytes } from "../lib/theoryImages";
import { useEffect, useRef, useState } from "react";
import { ArrowLeft, ArrowRight, BookOpen, Camera, Check, CheckCircle2, ChevronRight, FileText, GitFork, Layers3, Loader2, PenSquare, PenTool, Plus, Search, Sparkles, Star, Trash2, Upload, X } from "lucide-react";
import { apiRequest } from "../lib/api";
import "./ShortNotes.css";
import AnswerNotepad from "./AnswerNotepad";
import TextbookSources from "./TextbookSources";
import SavedTheoryAnswer from "./SavedTheoryAnswer";

async function loadReviewPages(path, active) {
  const reviews = new Map();
  let offset = 0;
  do {
    const data = await apiRequest(`${path}${path.includes('?') ? '&' : '?'}offset=${offset}`);
    if (!active()) return { reviews: [] };
    for (const review of data.reviews || []) if (!reviews.has(review.id)) reviews.set(review.id, review);
    offset = data.nextOffset;
  } while (offset != null);
  return { reviews: [...reviews.values()] };
}

const typeLabel = (kind) => kind === "long-answer" ? "Long answer" : "Short note";

function loadDrafts(key) {
  try { const value = JSON.parse(localStorage.getItem(key) || "{}"); return value && typeof value === "object" && !Array.isArray(value) ? value : {}; }
  catch { return {}; }
}

function loadCustomNotes(key) {
  try {
    const value = JSON.parse(localStorage.getItem(key) || "[]");
    return Array.isArray(value) ? value : [];
  } catch {
    return [];
  }
}

function renderModelAnswerPoint(point, index) {
  const isDiagram = point.includes("[DIAGRAM") || point.includes("[DIAGRAM TO DRAW:") || point.startsWith("Diagram:");
  if (isDiagram) {
    const clean = point.replace(/^\[DIAGRAM(?:\s+TO\s+DRAW)?:\s*/i, "");
    const bracketIdx = clean.indexOf("]");
    const title = bracketIdx !== -1 ? clean.slice(0, bracketIdx).trim() : clean;
    let desc = bracketIdx !== -1 ? clean.slice(bracketIdx + 1).trim() : "";
    desc = desc.replace(/^Description:\s*/i, "").trim();
    if (!desc && point.includes("Description:")) {
      desc = point.split(/Description:\s*/i)[1]?.trim() || "";
    }
    return (
      <div key={index} className="sn-model-diagram-card">
        <div className="sn-model-diagram-badge">
          <PenTool size={14} />
          <span>DIAGRAM & LABELS TO DRAW IN EXAM</span>
        </div>
        <h5 className="sn-model-diagram-title">{title || "Labelled Diagram"}</h5>
        {desc && <p className="sn-model-diagram-desc">{desc}</p>}
      </div>
    );
  }

  const colonIdx = point.indexOf(":");
  const hasHeading = colonIdx > 2 && colonIdx < 45 && !point.slice(0, colonIdx).includes("\n");

  return (
    <div key={index} className="sn-model-point-row">
      <span className="sn-point-bullet">•</span>
      <p className="sn-point-text">
        {hasHeading ? (
          <>
            <strong>{point.slice(0, colonIdx + 1)}</strong>
            {point.slice(colonIdx + 1)}
          </>
        ) : (
          point
        )}
      </p>
    </div>
  );
}

export default function ShortNotes({ subjectId, subjectTitle, userId, onBack, onNavigate }) {
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
  const draftOwner = useRef(draftKey);
  const [draftError, setDraftError] = useState("");
  const [answerImages, setAnswerImages] = useState([]);
  const [editing, setEditing] = useState(false);
  const [attempts, setAttempts] = useState([]);
  const [attemptIndex, setAttemptIndex] = useState(0);
  const [historyError, setHistoryError] = useState("");
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyReload, setHistoryReload] = useState(0);
  const [imageBusy, setImageBusy] = useState(false);
  const [busy, setBusy] = useState(false);
  const [privacyAccepted, setPrivacyAccepted] = useState(false);
  const [message, setMessage] = useState("");
  const mounted = useRef(true);
  const titleRef = useRef(null);
  const signedIn = Boolean(userId);

  // Custom notes state
  const customNotesKey = `medicomm-custom-short-notes:${userId || "guest"}`;
  const [customQuestions, setCustomQuestions] = useState(() => loadCustomNotes(customNotesKey));
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newPrompt, setNewPrompt] = useState("");
  const [newKind, setNewKind] = useState("short-note");
  const [newTopic, setNewTopic] = useState("");
  const [createBusy, setCreateBusy] = useState(false);
  const [generatePromptBusy, setGeneratePromptBusy] = useState(false);
  const [createError, setCreateError] = useState("");

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
    setReviews({}); setReviewLoadError("");
    if (signedIn) loadReviewPages("/api/short-notes/reviews", () => active).then(data => {
      if (active) { setReviews(Object.fromEntries((data.reviews || []).map(review => [review.questionId, review]))); setReviewLoadError(""); }
    }).catch(() => { if (active) setReviewLoadError("Saved reviews could not be loaded. You can still write an answer."); });
    return () => { active = false; };
  }, [signedIn, userId, reload]);

  // Load & sync custom short notes from server
  useEffect(() => {
    let active = true;
    if (signedIn) {
      apiRequest(`/api/short-notes/custom?subjectId=${encodeURIComponent(subjectId)}`).then(data => {
        if (!active || !Array.isArray(data.questions)) return;
        setCustomQuestions(current => {
          const map = new Map();
          for (const item of data.questions) map.set(item.id, item);
          for (const item of current) {
            if (!map.has(item.id) && item.subjectId === subjectId) {
              map.set(item.id, item);
              apiRequest("/api/short-notes/custom", {
                method: "POST",
                body: JSON.stringify({
                  subjectId: item.subjectId,
                  subjectTitle: item.subjectTitle || subjectTitle,
                  prompt: item.prompt,
                  kind: item.kind,
                }),
              }).catch(() => {});
            }
          }
          const merged = [...map.values()];
          try { localStorage.setItem(customNotesKey, JSON.stringify(merged)); } catch {}
          return merged;
        });
      }).catch(() => {});
    }
    return () => { active = false; };
  }, [signedIn, userId, subjectId, reload]);

  useEffect(() => {
    try { localStorage.setItem(customNotesKey, JSON.stringify(customQuestions)); } catch {}
  }, [customNotesKey, customQuestions]);

  useEffect(() => {
    let active = true;
    setAttempts([]); setAttemptIndex(0); setHistoryError("");
    if (!questionId || !signedIn) { setHistoryLoading(false); return; }
    setHistoryLoading(true);
    loadReviewPages(`/api/short-notes/reviews?questionId=${encodeURIComponent(questionId)}`, () => active).then(data => {
      if (active) setAttempts((data.reviews || []).filter(item => item.questionId === questionId));
    }).catch(() => { if (active) setHistoryError("Earlier attempts could not load."); })
      .finally(() => { if (active) setHistoryLoading(false); });
    return () => { active = false; };
  }, [questionId, userId, signedIn, historyReload]);

  useEffect(() => {
    if (draftOwner.current !== draftKey) {
      draftOwner.current = draftKey;
      setDrafts(loadDrafts(draftKey));
      setAnswerImages([]); setEditing(false);
      return;
    }
    try { localStorage.setItem(draftKey, JSON.stringify(drafts)); setDraftError(""); }
    catch { setDraftError("This browser could not save your draft. Keep this page open while writing."); }
  }, [draftKey, drafts]);

  useEffect(() => { onNavigate(); titleRef.current?.focus({ preventScroll: true }); }, [topicId, questionId]);

  const subject = bank?.subjects.find(item => item.id === subjectId);
  const subjectCustomQuestions = customQuestions.filter(q => !q.subjectId || q.subjectId === subjectId);
  const customReviewed = subjectCustomQuestions.filter(q => reviews[q.id]).length;

  const isCustomTopic = topicId === "custom-notes";
  const customTopic = isCustomTopic ? {
    id: "custom-notes",
    title: "Custom Notes",
    isCustom: true,
    questions: subjectCustomQuestions,
  } : null;

  const topic = customTopic || subject?.topics.find(item => item.id === topicId);
  const question = topic?.questions.find(item => item.id === questionId) || subjectCustomQuestions.find(item => item.id === questionId);

  const allQuestions = subject?.topics.flatMap(item => item.questions) ?? [];
  const totalReviewed = allQuestions.filter(item => reviews[item.id]).length;
  const topicReviewed = topic?.isCustom ? customReviewed : (topic?.questions.filter(item => reviews[item.id]).length ?? 0);

  const savedReview = question && (attempts[attemptIndex] || reviews[question.id]);
  const review = !editing && savedReview;
  const draft = question && typeof drafts[question.id] === "string" ? drafts[question.id] : "";
  const locked = busy || imageBusy;
  const normalizedSearch = search.toLowerCase().trim();

  const visibleQuestions = topic?.questions.filter(item =>
    item.prompt.toLowerCase().includes(normalizedSearch)
    && (filter === "all" || filter === item.kind || (filter === "unreviewed" && !reviews[item.id]) || (filter === "saved" && reviews[item.id]))
    && (!starred || (item.emphasis ?? 0) > 0)) ?? [];

  const visibleTopics = subject?.topics.filter(item => item.title.toLowerCase().includes(normalizedSearch)
    || item.questions.some(q => q.prompt.toLowerCase().includes(normalizedSearch))) ?? [];

  function openQuestion(id) {
    if (locked) return;
    setQuestionId(id); setAnswerImages([]); setMessage(""); setPrivacyAccepted(false); setEditing(false); setAttempts([]); setAttemptIndex(0);
  }

  function backToList() {
    if (!locked) { setQuestionId(""); setAnswerImages([]); setMessage(""); setEditing(false); }
  }

  async function pickImage(event) {
    const files = [...(event.target.files || [])]; event.target.value = "";
    if (!files.length || locked) return;
    if (answerImages.length + files.length > 8) { setMessage("Attach up to 8 pages per answer."); return; }
    setImageBusy(true); setMessage("");
    try {
      const images = [];
      for (const file of files) images.push({ ...await prepareTheoryImage(file), source: "upload" });
      const next = [...answerImages, ...images];
      if (next.reduce((bytes, image) => bytes + imageBytes(image.dataUrl), 0) > 5 * 1024 * 1024) throw new Error("Prepared answer pages must total 5 MB or less. Try smaller photos.");
      if (mounted.current) setAnswerImages(next);
    }
    catch (error) { if (mounted.current) setMessage(error.message); }
    finally { if (mounted.current) setImageBusy(false); }
  }

  async function submitAnswer(event) {
    event.preventDefault();
    if (!question || locked || !privacyAccepted || (!answerImages.length && draft.trim().length < 3)) return;
    setBusy(true); setMessage("");
    try {
      const payload = {
        questionId: question.id,
        answer: draft,
        answerPages: answerImages.map(({ dataUrl, name, source }) => ({ dataUrl, name, source })),
        privacyAccepted: true,
        ...(question.isCustom ? {
          customQuestion: {
            prompt: question.prompt,
            kind: question.kind,
            subjectId,
            subjectTitle: subject?.title || subjectTitle,
          },
        } : {}),
      };
      const data = await apiRequest("/api/short-notes/reviews", {
        method: "POST",
        timeoutMs: 150000,
        body: JSON.stringify(payload),
      });
      if (mounted.current) {
        setReviews(current => ({ ...current, [question.id]: data.review }));
        setAnswerImages([]);
        setEditing(false);
        setAttempts(current => [data.review, ...current]);
        setAttemptIndex(0);
        setHistoryReload(value => value + 1);
        setDrafts(current => { const next = { ...current }; delete next[question.id]; return next; });
        onNavigate();
      }
    } catch (error) { if (mounted.current) setMessage(error.message); }
    finally { if (mounted.current) setBusy(false); }
  }

  async function handleCreateCustomNote(event) {
    if (event) event.preventDefault();
    const prompt = newPrompt.trim();
    if (prompt.length < 3) {
      setCreateError("Please write a question with at least 3 characters.");
      return;
    }
    setCreateBusy(true);
    setCreateError("");
    try {
      let createdQuestion = null;
      if (signedIn) {
        const data = await apiRequest("/api/short-notes/custom", {
          method: "POST",
          body: JSON.stringify({
            subjectId,
            subjectTitle: subject?.title || subjectTitle,
            prompt,
            kind: newKind,
          }),
        });
        createdQuestion = data?.question;
      }
      if (!createdQuestion) {
        createdQuestion = {
          id: `custom-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
          userId: userId || "guest",
          subjectId,
          subjectTitle: subject?.title || subjectTitle,
          topicTitle: "Custom Notes",
          prompt,
          kind: newKind,
          isCustom: true,
          createdAt: new Date().toISOString(),
        };
      }
      setCustomQuestions(current => [createdQuestion, ...current.filter(q => q.id !== createdQuestion.id)]);
      setNewPrompt("");
      setNewTopic("");
      setShowCreateModal(false);
      setTopicId("custom-notes");
      openQuestion(createdQuestion.id);
    } catch (err) {
      setCreateError(err.message || "Could not create custom short note.");
    } finally {
      setCreateBusy(false);
    }
  }

  async function handleDeleteCustomNote(id, event) {
    if (event) event.stopPropagation();
    if (!window.confirm("Remove this custom question from your library?")) return;
    try {
      if (signedIn) {
        await apiRequest(`/api/short-notes/custom?questionId=${encodeURIComponent(id)}`, { method: "DELETE" });
      }
    } catch { /* proceed locally */ }
    setCustomQuestions(current => current.filter(q => q.id !== id));
    if (questionId === id) backToList();
  }

  async function handleGeneratePrompt() {
    const topicText = newTopic.trim();
    if (!topicText) {
      setCreateError("Enter a topic or disease keyword first.");
      return;
    }
    setGeneratePromptBusy(true);
    setCreateError("");
    try {
      let promptText = "";
      if (signedIn) {
        const data = await apiRequest("/api/short-notes/generate-prompt", {
          method: "POST",
          body: JSON.stringify({
            subjectTitle: subject?.title || subjectTitle,
            topic: topicText,
            kind: newKind,
          }),
        });
        promptText = data?.prompt;
      }
      if (!promptText) {
        promptText = newKind === "long-answer"
          ? `${topicText} – Etiopathogenesis, Clinical Features, Investigations, and Management`
          : `${topicText} – Key Features, Pathophysiology, and Applied Clinical Significance`;
      }
      setNewPrompt(promptText);
    } catch {
      setNewPrompt(newKind === "long-answer"
        ? `${topicText} – Etiopathogenesis, Clinical Features, Investigations, and Management`
        : `${topicText} – Key Features, Pathophysiology, and Applied Clinical Significance`);
    } finally {
      setGeneratePromptBusy(false);
    }
  }

  const backButton = <button className="sn-back" type="button" onClick={onBack} disabled={locked}><ArrowLeft size={16} /> Back to subjects</button>;
  if (!bank) return <section className="app-view short-notes-view">{backButton}<div className="sn-empty" role={loadError ? "alert" : "status"}>
    {loadError ? <><h2>Questions couldn't load</h2><p>{loadError}</p><button className="button button-primary" onClick={() => setReload(value => value + 1)}>Try again</button></> : <><Loader2 className="sn-spin" /><p>Opening your theory library...</p></>}
  </div></section>;
  if (!subject) return <section className="app-view short-notes-view">{backButton}<div className="sn-empty"><BookOpen size={32} /><h2>{subjectTitle} short notes</h2><p>Questions for this subject haven't been added yet.</p></div></section>;

  return <section className="app-view short-notes-view">
    <nav className="sn-breadcrumbs" aria-label="Short notes navigation">
      <button type="button" onClick={onBack} disabled={locked}>Theory</button><ChevronRight size={14} />
      <button type="button" disabled={locked} onClick={() => { setTopicId(""); setQuestionId(""); setSearch(""); setAnswerImages([]); setEditing(false); }}>{subject.title}</button>
      <ChevronRight size={14} /><span>Short Notes</span>
      {topic && <><ChevronRight size={14} /><button type="button" onClick={backToList} disabled={locked}>{topic.isCustom ? "Custom Notes" : topic.title}</button></>}
      {question && <><ChevronRight size={14} /><span>Question</span></>}
    </nav>
    {reviewLoadError && <p className="sn-notice" role="status">{reviewLoadError} <button type="button" onClick={() => setReload(value => value + 1)}>Retry</button></p>}

    {question ? <>
      <div className="sn-answer-heading">
        <button className="sn-back" type="button" onClick={backToList} disabled={locked}><ArrowLeft size={16} /> Back to {topic?.isCustom ? "custom notes" : "questions"}</button>
        {topic && <span>Question {topic.questions.indexOf(question) + 1} of {topic.questions.length}</span>}
      </div>
      <article className="sn-prompt-card">
        <div className="sn-question-meta">
          <span className="sn-badge">{question.isCustom ? `Custom ${typeLabel(question.kind)}` : typeLabel(question.kind)}</span>
          {question.emphasis > 0 && <span className="sn-star-label"><Star size={13} /> Starred</span>}
          <span>{topic?.title || "Custom Notes"}</span>
        </div>
        <h2 ref={titleRef} tabIndex={-1}>{question.prompt}</h2>
        <div className="sn-source"><span>AI practice review / 10</span></div>
      </article>
      {historyLoading && !review && !editing ? <p className="sn-notice" role="status">Opening your saved answer...</p> : review ? <article className="card panel sn-review" aria-live="polite">
        {attempts.length > 1 && <label className="sn-attempt-picker">Saved attempts<select aria-label="Saved attempt" value={attemptIndex} onChange={event => setAttemptIndex(Number(event.target.value))}>{attempts.map((item, index) => <option key={item.id || item.submittedAt || index} value={index}>{index === 0 ? "Latest" : `Attempt ${attempts.length - index}`} · {item.submittedAt ? new Date(item.submittedAt).toLocaleDateString() : "Saved"} · {item.score}/10</option>)}</select></label>}
        {historyLoading && <p role="status">Loading saved attempts...</p>}
        {historyError && <p className="sn-notice" role="status">{historyError} <button type="button" onClick={() => setHistoryReload(value => value + 1)}>Retry</button></p>}
        <SavedTheoryAnswer key={`${question.id}:${review.id || review.submittedAt || attemptIndex}`} review={review} />
        {review.hasImage && !review.answerPages?.length && <AnswerNotepad key={question.id} draftId={`short-notes:${userId || "guest"}:${question.id}`} prompt={question.prompt} />}
        <div className="sn-review-top"><div className="sn-score"><strong>{review.score}</strong><span>/ 10</span></div><div><p className="sn-eyebrow"><Sparkles size={14} /> AI theory review</p><h3>{review.feedback}</h3></div></div>
        <div className="sn-feedback-grid"><section><h4><CheckCircle2 size={17} /> What you did well</h4>{review.strengths?.length ? <ul>{review.strengths.map((point, i) => <li key={i}>{point}</li>)}</ul> : <p>Use the suggestions alongside to build a stronger answer.</p>}</section><section><h4>How to improve</h4><ul>{review.improvements?.map((point, i) => <li key={i}>{point}</li>)}</ul></section></div>
        <section className="sn-model-answer">
          <div className="sn-model-answer-header">
            <div>
              <p className="sn-eyebrow"><Sparkles size={14} /> Learn from your answer</p>
              <h3>Exam-ready model answer</h3>
            </div>
            <span className="sn-model-answer-badge">10-Mark University Model Answer</span>
          </div>
          <div className="sn-model-answer-scrollable">
            {review.modelAnswerSections?.map((section, i) => (
              <div key={i} className="sn-model-section">
                <h4>{section.heading}</h4>
                <div className="sn-model-points-list">
                  {section.points.map((point, index) => renderModelAnswerPoint(point, index))}
                </div>
                {section.flowchart && (
                  <div className="sn-flowchart-card">
                    <div className="sn-flowchart-badge">
                      <GitFork size={14} />
                      <span>EXAM FLOWCHART / PATHWAY</span>
                    </div>
                    <div className="sn-flowchart">{section.flowchart}</div>
                  </div>
                )}
              </div>
            ))}
          </div>
          <small>AI-generated study feedback strictly based on standard MBBS textbooks. Check important details against your textbook.</small>
        </section>
        <TextbookSources sources={review.textbookSources} />
        <div className="sn-review-actions"><span><CheckCircle2 size={15} /> Answer and review saved</span><button className="button button-secondary" type="button" onClick={() => { setEditing(true); setDrafts(current => ({ ...current, [question.id]: current[question.id] || "" })); setPrivacyAccepted(false); }}>Practise again</button></div>
      </article> : <form className="sn-writing-layout" onSubmit={submitAnswer}>
        {savedReview && <button type="button" className="sn-back" onClick={() => setEditing(false)} disabled={locked}><ArrowLeft size={16} /> Back to saved answer</button>}
        <article className="sn-editor">
          <div className="sn-editor-heading"><h3><FileText size={19} /> Your answer</h3><span>{draftError ? "Draft not saved" : draft ? "Draft saved on this device" : "Make this concept yours"}</span></div>
          <label htmlFor="short-note-answer" className="sr-only">Your theory answer</label>
          <textarea id="short-note-answer" value={draft} onChange={event => setDrafts(current => ({ ...current, [question.id]: event.target.value }))} maxLength={8000} rows={15} disabled={locked} placeholder="Start with a brief introduction, then organise your answer under clear headings. Include a labelled diagram where asked." />
          <div className="sn-editor-footer"><span>Use headings, key points, and relevant examples.</span><span>{draft.length.toLocaleString()} / 8,000</span></div>
          {draftError && <p className="form-message" role="status">{draftError}</p>}
        </article>
        <aside className="sn-answer-aside">
          <section className="sn-upload-card"><span className="sn-aside-icon"><Camera size={22} /></span><h3>Prefer pen & paper?</h3><p>Write your answer, then upload a clear photo for the same AI review.</p>
            {answerImages.map((image, index) => <div className="sn-photo" key={`${index}:${image.name}`}><img src={image.dataUrl} alt={`Your handwritten answer page ${index + 1}`} /><span>Page {index + 1} · {image.name}</span><button type="button" onClick={() => setAnswerImages(current => current.filter((_, i) => i !== index))} disabled={locked}><X size={14} /> Remove page {index + 1}</button></div>)}
            {answerImages.length < 8 && <div className="sn-upload-actions">
              <label className={`button button-secondary ${locked ? "sn-disabled" : ""}`}><Upload size={15} /> {answerImages.length ? "Add pages" : "Upload answer"}<input type="file" multiple accept="image/jpeg,image/png,image/webp,image/heic,image/heif" onChange={pickImage} disabled={locked} /></label>
              <label className={`sn-camera-link ${locked ? "sn-disabled" : ""}`}><Camera size={15} /> Take a photo<input type="file" accept="image/*" capture="environment" onChange={pickImage} disabled={locked} /></label>
            </div>}
            {imageBusy && <p role="status"><Loader2 size={15} className="sn-spin" /> Preparing photo...</p>}<small>JPG, PNG or WebP · up to 12 MB</small>
          </section>
          <AnswerNotepad key={question.id} draftId={`short-notes:${userId || "guest"}:${question.id}`} prompt={question.prompt} disabled={locked} hasImage={Boolean(answerImages.length)} onSave={image => { setAnswerImages(image.pages || [{ ...image, source: "notepad" }]); setMessage("Notepad pages attached. Submit them to save your answer and review in your library."); }} />
          <section className="sn-review-info"><Sparkles size={19} /><h3>A little feedback goes a long way.</h3><p>Get a score, specific improvements, and a structured model answer.</p><span>Medical accuracy · Coverage · Structure</span></section>
        </aside>
        <div className="sn-submit-area">
          {!signedIn && <p className="sn-notice">You can write and save a draft as a guest. Sign in to submit it for AI review.</p>}
          <label className="sn-consent"><input type="checkbox" checked={privacyAccepted} onChange={event => setPrivacyAccepted(event.target.checked)} disabled={locked} /><span>I agree to send this answer and its pages to AI for review and save them privately in my answer library. I haven't included patient-identifying information.</span></label>
          {message && <p className="form-message" role="alert">{message}</p>}
          <div className="sn-submit-row"><span>{busy ? "Reviewing your answer. This can take a little time..." : "Your answer and review will be saved together."}</span><button className="button button-primary sn-submit" type="submit" disabled={!signedIn || locked || !privacyAccepted || (!answerImages.length && draft.trim().length < 3)}>{busy ? <Loader2 className="sn-spin" size={17} /> : <Sparkles size={17} />}{busy ? "Reviewing answer..." : "Review answer (10 tokens)"}</button></div>
        </div>
      </form>}
      {topic && topic.questions.length > 1 && (
        <div className="sn-question-pagination">
          <button className="sn-back" type="button" disabled={locked || topic.questions[0].id === question.id} onClick={() => openQuestion(topic.questions[topic.questions.indexOf(question) - 1].id)}>
            <ArrowLeft size={16} /> Previous question
          </button>
          <button className="sn-back" type="button" disabled={locked || topic.questions.at(-1).id === question.id} onClick={() => openQuestion(topic.questions[topic.questions.indexOf(question) + 1].id)}>
            Next question <ArrowRight size={16} />
          </button>
        </div>
      )}
    </> : topic?.isCustom ? <>
      {/* Custom Notes Section / Library View */}
      <header className="sn-hero">
        <div className="sn-hero-copy">
          <p className="sn-eyebrow"><Sparkles size={15} /> Theory / Custom Notes</p>
          <h2 ref={titleRef} tabIndex={-1}>{subject.title} Custom Notes</h2>
          <p>Write your own questions, generate custom short notes, and practice with AI grading, model answers, and textbook sources.</p>
        </div>
        <div className="sn-progress-summary">
          <span className="sn-progress-icon"><Layers3 size={24} /></span>
          <strong>{customReviewed}<span> / {subjectCustomQuestions.length}</span></strong>
          <small>custom notes reviewed</small>
          <div className="sn-progress-track">
            <span style={{ width: `${100 * (subjectCustomQuestions.length ? customReviewed / subjectCustomQuestions.length : 0)}%` }} />
          </div>
        </div>
      </header>

      <div className="sn-section-heading">
        <div>
          <h3>Custom Questions Library</h3>
          <p>{visibleQuestions.length} of {subjectCustomQuestions.length} questions</p>
        </div>
        <div className="sn-heading-actions">
          <button className="button button-primary sn-create-inline-btn" type="button" onClick={() => { setShowCreateModal(true); setCreateError(""); }}>
            <Plus size={15} /> New Short Note
          </button>
          <button className="sn-back" type="button" onClick={() => { setTopicId(""); setSearch(""); setFilter("all"); }}>
            <ArrowLeft size={15} /> All topics
          </button>
        </div>
      </div>

      <div className="sn-toolbar">
        <label className="sn-search">
          <Search size={18} />
          <input aria-label="Search custom questions" value={search} onChange={event => setSearch(event.target.value)} placeholder="Find a custom question or concept..." />
          {search && <button type="button" aria-label="Clear search" onClick={() => setSearch("")}><X size={16} /></button>}
        </label>
      </div>

      <div className="sn-filters" aria-label="Filter questions">
        {[["all", "All questions"], ["saved", "My answers"], ["unreviewed", "To practise"], ["short-note", "Short notes"], ["long-answer", "Long answers"]].map(([value, label]) => (
          <button key={value} type="button" aria-pressed={filter === value} className={filter === value ? "is-active" : ""} onClick={() => setFilter(value)}>{label}</button>
        ))}
      </div>

      <div className="sn-question-list">
        {visibleQuestions.map((item, idx) => (
          <div className={`sn-question-row sn-custom-question-row ${reviews[item.id] ? "is-reviewed" : ""}`} key={item.id}>
            <button type="button" className="sn-row-main" onClick={() => openQuestion(item.id)}>
              <span className="sn-row-number">{reviews[item.id] ? <Check size={19} /> : String(idx + 1).padStart(2, "0")}</span>
              <span className="sn-row-body">
                <span className="sn-row-meta">
                  <span className="sn-custom-badge"><Sparkles size={11} /> Custom {typeLabel(item.kind)}</span>
                  {item.createdAt && <span>Added {new Date(item.createdAt).toLocaleDateString()}</span>}
                </span>
                <strong>{item.prompt}</strong>
              </span>
              <span className="sn-row-action">
                {reviews[item.id] ? <span>{reviews[item.id].score}/10</span> : <span>{drafts[item.id] ? "Continue" : "Write answer"}</span>}
                <ArrowRight size={18} />
              </span>
            </button>
            <button type="button" className="sn-delete-btn" title="Delete custom note" aria-label="Delete custom note" onClick={(e) => handleDeleteCustomNote(item.id, e)}>
              <Trash2 size={16} />
            </button>
          </div>
        ))}
      </div>

      {!visibleQuestions.length && (
        <div className="sn-empty">
          <Sparkles size={32} />
          <h3>{search ? "No matching custom questions" : "Your custom notes library is empty"}</h3>
          <p>{search ? "Try another keyword or reset your filter." : "Create your own short note to test your knowledge with AI evaluation and model answers."}</p>
          <button className="button button-primary" type="button" onClick={() => { setShowCreateModal(true); setCreateError(""); }}>
            <Plus size={15} /> Write New Short Note
          </button>
        </div>
      )}
    </> : <>
      <header className="sn-hero">
        <div className="sn-hero-copy">
          <p className="sn-eyebrow"><BookOpen size={15} /> Theory / Short Notes</p>
          <h2 ref={titleRef} tabIndex={-1}>{topic ? topic.title : <>{subject.title}<span>One concept at a time.</span></>}</h2>
          <p>{topic ? "Choose a question. Write your answer. Get feedback that helps it stick." : "Build answers worth remembering. Choose a topic or create custom notes to begin your theory practice."}</p>
        </div>
        <div className="sn-progress-summary">
          <span className="sn-progress-icon"><Layers3 size={24} /></span>
          <strong>{topic ? topicReviewed : totalReviewed}<span> / {topic ? topic.questions.length : allQuestions.length}</span></strong>
          <small>questions reviewed</small>
          <div className="sn-progress-track">
            <span style={{ width: `${100 * (topic ? topicReviewed / topic.questions.length : totalReviewed / allQuestions.length)}%` }} />
          </div>
        </div>
      </header>

      {/* Featured Custom Notes Banner on Subject Page */}
      {!topic && (
        <section className="sn-custom-banner">
          <div className="sn-custom-banner-left">
            <div className="sn-custom-icon-wrapper">
              <Sparkles size={22} />
            </div>
            <div className="sn-custom-banner-content">
              <span className="sn-custom-eyebrow"><PenSquare size={12} /> Custom Notes</span>
              <h3>Create & Practice Custom Questions</h3>
              <p>Write your own custom question, generate short notes, and practice with the exact same AI scoring, review panel, and exam-ready model answers.</p>
            </div>
          </div>
          <div className="sn-custom-banner-actions">
            <button type="button" className="button button-secondary sn-custom-btn" onClick={() => { setShowCreateModal(true); setCreateError(""); }}>
              <Plus size={15} /> New Short Note
            </button>
            <button type="button" className="button button-primary sn-custom-btn" onClick={() => { setTopicId("custom-notes"); setSearch(""); setFilter("all"); }}>
              Custom Notes ({subjectCustomQuestions.length}) <ArrowRight size={15} />
            </button>
          </div>
        </section>
      )}

      <div className="sn-section-heading">
        <div>
          <h3>{topic ? "Theory questions" : "Explore topics"}</h3>
          <p>{topic ? `${visibleQuestions.length} of ${topic.questions.length} questions` : `${subject.topics.length + 1} topics · ${allQuestions.length + subjectCustomQuestions.length} questions`}</p>
        </div>
        <button className="sn-back" type="button" onClick={topic ? () => { setTopicId(""); setSearch(""); setFilter("all"); setStarred(false); } : onBack}>
          <ArrowLeft size={15} /> {topic ? "All topics" : "Subjects"}
        </button>
      </div>

      <div className="sn-toolbar">
        <label className="sn-search">
          <Search size={18} />
          <input aria-label={topic ? "Search questions" : "Search topics or questions"} value={search} onChange={event => setSearch(event.target.value)} placeholder={topic ? "Find a question in this topic..." : "Find a topic or concept..."} />
          {search && <button type="button" aria-label="Clear search" onClick={() => setSearch("")}><X size={16} /></button>}
        </label>
        {topic && <button className={`sn-filter-star ${starred ? "is-active" : ""}`} type="button" aria-pressed={starred} onClick={() => setStarred(value => !value)}><Star size={15} /> Starred</button>}
      </div>

      {topic ? <>
        <div className="sn-filters" aria-label="Filter questions">
          {[["all", "All questions"], ["saved", "My answers"], ["short-note", "Short notes"], ["long-answer", "Long answers"], ["unreviewed", "To practise"]].map(([value, label]) => (
            <button key={value} type="button" aria-pressed={filter === value} className={filter === value ? "is-active" : ""} onClick={() => setFilter(value)}>{label}</button>
          ))}
        </div>
        <div className="sn-question-list">
          {visibleQuestions.map(item => (
            <button className={`sn-question-row ${reviews[item.id] ? "is-reviewed" : ""}`} type="button" key={item.id} onClick={() => openQuestion(item.id)}>
              <span className="sn-row-number">{reviews[item.id] ? <Check size={19} /> : String(topic.questions.indexOf(item) + 1).padStart(2, "0")}</span>
              <span className="sn-row-body">
                <span className="sn-row-meta">
                  <span>{typeLabel(item.kind)}</span>
                  {item.emphasis > 0 && <span className="sn-star-label" title={`${item.emphasis} stars`}><Star size={12} /> {item.emphasis > 1 ? `${item.emphasis} stars` : "Starred"}</span>}
                </span>
                <strong>{item.prompt}</strong>
              </span>
              <span className="sn-row-action">
                {reviews[item.id] ? <span>{reviews[item.id].score}/10</span> : <span>{drafts[item.id] ? "Continue" : "Write answer"}</span>}
                <ArrowRight size={18} />
              </span>
            </button>
          ))}
        </div>
        {!visibleQuestions.length && (
          <div className="sn-empty">
            <Search size={28} />
            <h3>No matching questions</h3>
            <p>Try another keyword or reset your filters.</p>
            <button className="button button-secondary" onClick={() => { setSearch(""); setFilter("all"); setStarred(false); }}>Reset filters</button>
          </div>
        )}
      </> : <div className="sn-topic-grid">
        {/* Custom Notes Card inside Topic Grid */}
        <button className="sn-topic-card sn-custom-topic-card" type="button" onClick={() => { setTopicId("custom-notes"); setSearch(""); setFilter("all"); setStarred(false); }}>
          <span className="sn-topic-top">
            <span className="sn-topic-number sn-custom-number"><Sparkles size={14} /></span>
            <ArrowRight size={18} />
          </span>
          <h4>Custom Notes</h4>
          <p>{subjectCustomQuestions.length} custom {subjectCustomQuestions.length === 1 ? "note" : "notes"}<span>Your library</span></p>
          <div className="sn-progress-track">
            <span style={{ width: `${100 * (subjectCustomQuestions.length ? customReviewed / subjectCustomQuestions.length : 0)}%` }} />
          </div>
          <small>{customReviewed ? `${customReviewed} reviewed` : subjectCustomQuestions.length ? "Ready to practice" : "Create your first note"}</small>
        </button>

        {visibleTopics.map((item) => {
          const reviewed = item.questions.filter(q => reviews[q.id]).length;
          return <button className="sn-topic-card" type="button" key={item.id} onClick={() => { setTopicId(item.id); setSearch(""); setFilter("all"); setStarred(false); }}>
            <span className="sn-topic-top">
              <span className="sn-topic-number">{String(subject.topics.indexOf(item) + 1).padStart(2, "0")}</span>
              <ArrowRight size={18} />
            </span>
            <h4>{item.title}</h4>
            <p>{item.questions.length} questions<span>{item.questions.filter(q => q.kind === "long-answer").length} long answers</span></p>
            <div className="sn-progress-track"><span style={{ width: `${100 * reviewed / item.questions.length}%` }} /></div>
            <small>{reviewed ? `${reviewed} reviewed` : "Ready when you are"}</small>
          </button>;
        })}
        {!visibleTopics.length && <div className="sn-empty"><h3>No matching topics</h3><p>Try another topic or question keyword.</p></div>}
      </div>}
    </>}

    {/* New Short Note Modal */}
    {showCreateModal && (
      <div className="sn-modal-overlay" role="dialog" aria-modal="true" aria-labelledby="custom-modal-title">
        <div className="sn-modal-content">
          <div className="sn-modal-header">
            <div className="sn-modal-title-row">
              <span className="sn-custom-eyebrow"><PenSquare size={13} /> Custom Theory Practice</span>
              <h3 id="custom-modal-title">New Short Note · {subject.title}</h3>
            </div>
            <button type="button" className="sn-modal-close" aria-label="Close" onClick={() => setShowCreateModal(false)}>
              <X size={20} />
            </button>
          </div>
          <form onSubmit={handleCreateCustomNote} className="sn-modal-body">
            <div className="sn-form-group">
              <label htmlFor="custom-prompt">Write your custom question <span className="sn-required">*</span></label>
              <textarea
                id="custom-prompt"
                rows={4}
                maxLength={1000}
                value={newPrompt}
                onChange={e => setNewPrompt(e.target.value)}
                placeholder="e.g., Blood supply of the thyroid gland, clinical features of Goiter, and applied surgical anatomy."
                disabled={createBusy}
                required
              />
              <div className="sn-field-hint">
                <span>{newPrompt.length} / 1,000 characters (min 3)</span>
              </div>
            </div>

            <div className="sn-form-group">
              <label>Question Format</label>
              <div className="sn-kind-selector">
                <button
                  type="button"
                  className={`sn-kind-btn ${newKind === "short-note" ? "is-selected" : ""}`}
                  onClick={() => setNewKind("short-note")}
                >
                  <strong>Short Note (SAQ)</strong>
                  <span>Focused topic · 10 marks</span>
                </button>
                <button
                  type="button"
                  className={`sn-kind-btn ${newKind === "long-answer" ? "is-selected" : ""}`}
                  onClick={() => setNewKind("long-answer")}
                >
                  <strong>Long Answer (LAQ)</strong>
                  <span>Comprehensive discussion · 10 marks</span>
                </button>
              </div>
            </div>

            <div className="sn-ai-helper-card">
              <div className="sn-ai-helper-header">
                <Sparkles size={16} />
                <span>AI Exam Prompt Assistant</span>
              </div>
              <p>Have a topic in mind? Enter a keyword or topic and let AI formulate an authentic university exam prompt:</p>
              <div className="sn-ai-helper-input-row">
                <input
                  type="text"
                  value={newTopic}
                  onChange={e => setNewTopic(e.target.value)}
                  placeholder="e.g. Cushing syndrome, Inguinal hernia, Horner syndrome..."
                  disabled={generatePromptBusy || createBusy}
                  onKeyDown={e => { if (e.key === "Enter") { e.preventDefault(); handleGeneratePrompt(); } }}
                />
                <button
                  type="button"
                  className="button button-secondary sn-ai-generate-btn"
                  onClick={handleGeneratePrompt}
                  disabled={generatePromptBusy || !newTopic.trim()}
                >
                  {generatePromptBusy ? <Loader2 size={14} className="sn-spin" /> : <Sparkles size={14} />}
                  {generatePromptBusy ? "Drafting..." : "Generate Prompt"}
                </button>
              </div>
            </div>

            {createError && <p className="form-message" role="alert">{createError}</p>}

            <div className="sn-modal-footer">
              <button type="button" className="button button-secondary" onClick={() => setShowCreateModal(false)} disabled={createBusy}>
                Cancel
              </button>
              <button type="submit" className="button button-primary sn-generate-submit-btn" disabled={createBusy || newPrompt.trim().length < 3}>
                {createBusy ? <Loader2 size={16} className="sn-spin" /> : <Sparkles size={16} />}
                {createBusy ? "Generating Short Note..." : "Generate Short Note"}
              </button>
            </div>
          </form>
        </div>
      </div>
    )}
  </section>;
}
