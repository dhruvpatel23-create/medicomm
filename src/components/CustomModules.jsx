import { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, BookOpen, Check, CheckCircle2, Clock3, Flag, Layers3, Search, SlidersHorizontal } from 'lucide-react';
import { buildCustomModuleCatalog, customModulePool, customModuleResult, CUSTOM_TEST_SIZES, readCustomModuleSession, sampleCustomModule } from '../lib/customModules';
import './custom-modules.css';

function timeLabel(seconds) {
  const value = Math.max(0, seconds);
  return `${Math.floor(value / 60).toString().padStart(2, '0')}:${(value % 60).toString().padStart(2, '0')}`;
}

function QuestionDetails({ question }) {
  return <>
    <p className="custom-question-prompt">{question.prompt}</p>
    {question.laboratoryFindings?.length > 0 && <div className="custom-labs"><table><caption>Laboratory findings</caption><thead><tr><th>Test</th><th>Result</th><th>Reference</th></tr></thead><tbody>{question.laboratoryFindings.map((lab, index) => <tr key={index}><th>{lab.test}</th><td>{lab.value}</td><td>{lab.reference}</td></tr>)}</tbody></table></div>}
    {question.leadIn && <p className="custom-question-prompt">{question.leadIn}</p>}
    <div className="custom-images">{[...new Set([...(question.imageUrls ?? []), ...(question.images ?? [])])].map((url, index) => <img key={url} src={url} alt={`Question visual ${index + 1}`} />)}</div>
  </>;
}

export default function CustomModules({ subjects, userId, onBack, onComplete, syncMessage }) {
  const catalog = useMemo(() => buildCustomModuleCatalog(subjects), [subjects]);
  const [selected, setSelected] = useState([]);
  const [count, setCount] = useState(10);
  const [query, setQuery] = useState('');
  const storageKey = `medulla-custom-module:${userId}`;
  const [session, setSession] = useState(() => readCustomModuleSession(storageKey));
  const [now, setNow] = useState(Date.now);
  const [confirmSubmit, setConfirmSubmit] = useState(false);
  const [storageWarning, setStorageWarning] = useState('');
  const submitted = useRef(session?.status === 'complete');
  const pool = useMemo(() => customModulePool(catalog, selected), [catalog, selected]);
  const selectedSet = new Set(selected);
  const selectedSubjects = catalog.filter(subject => subject.chapters.some(chapter => selectedSet.has(chapter.key))).length;

  useEffect(() => {
    try {
      if (session) sessionStorage.setItem(storageKey, JSON.stringify(session));
      else sessionStorage.removeItem(storageKey);
      setStorageWarning('');
    } catch { setStorageWarning('Keep this page open: this browser could not save your test for resuming.'); }
  }, [session, storageKey]);
  useEffect(() => {
    if (session?.status !== 'active') return;
    setNow(Date.now());
    const timer = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, [session?.status, session?.startedAt]);

  function toggleChapter(key) { setSelected(current => current.includes(key) ? current.filter(value => value !== key) : [...current, key]); }
  function toggleSubject(subject) {
    const keys = subject.chapters.map(chapter => chapter.key);
    setSelected(current => keys.every(key => current.includes(key)) ? current.filter(key => !keys.includes(key)) : [...new Set([...current, ...keys])]);
  }
  function start() {
    if (pool.length < count) return;
    const startedAt = Date.now();
    submitted.current = false;
    setNow(startedAt); setConfirmSubmit(false);
    setSession({ version: 1, id: crypto.randomUUID(), status: 'active', startedAt, questions: sampleCustomModule(pool, count), answers: {}, flags: [], index: 0 });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  function finish() {
    if (submitted.current || session?.status !== 'active') return;
    submitted.current = true;
    const result = { ...session, status: 'complete', finishedAt: Date.now() };
    setSession(result); setConfirmSubmit(false);
    onComplete?.(result);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  function reset() { submitted.current = false; setSession(null); setConfirmSubmit(false); }
  const elapsed = session ? Math.max(0, Math.floor(((session.finishedAt ?? now) - session.startedAt) / 1000)) : 0;
  const answered = session ? Object.keys(session.answers).length : 0;

  if (session?.status === 'complete') {
    const result = customModuleResult(session);
    return <section className="app-view custom-module">
      <header className="custom-hero"><span className="custom-eyebrow"><CheckCircle2 size={18} />Test complete</span><h2>Your results, in focus.</h2><p>Review your answers and use each explanation to guide your next session.</p><div className="custom-result-stats"><div><strong>{result.correct} / {result.total}</strong><span>Score · no negative marking</span></div><div><strong>{result.incorrect}</strong><span>Incorrect</span></div><div><strong>{result.skipped}</strong><span>Skipped</span></div><div><strong>{timeLabel(elapsed)}</strong><span>Time taken</span></div></div><div className="custom-actions"><button className="button button-primary" onClick={reset}>Build another test</button><button className="button button-secondary" onClick={onBack}>All practice paths</button></div></header>
      {syncMessage && <p role="status">{syncMessage}</p>}
      <h3>Answer review</h3><div className="custom-review-list">{session.questions.map((question, index) => {
        const answer = session.answers[question.id];
        const status = answer === undefined ? 'Skipped' : answer === question.answerIndex ? 'Correct' : 'Incorrect';
        return <details className="custom-review" key={question.id} open={index === 0}><summary><span>Question {index + 1}<small>{question.subjectTitle} · {question.chapterTitle}</small></span><span className={`custom-status custom-status-${status.toLowerCase()}`}>{status}</span></summary><QuestionDetails question={question} /><ol className="custom-review-options">{question.options.map((option, optionIndex) => <li className={optionIndex === question.answerIndex ? 'is-correct' : optionIndex === answer ? 'is-incorrect' : ''} key={optionIndex}><span>{String.fromCharCode(65 + optionIndex)}. {option}</span>{optionIndex === question.answerIndex && <strong>Correct answer</strong>}{optionIndex === answer && <small>Your answer</small>}</li>)}</ol><div className="custom-explanation"><h4>Explanation</h4><p>{question.explanation || 'No explanation is available yet.'}</p>{question.explanationImageUrls?.map((url, imageIndex) => <img key={url} src={url} alt={`Explanation visual ${imageIndex + 1}`} />)}</div></details>;
      })}</div>
    </section>;
  }

  if (session) {
    const question = session.questions[session.index];
    const flagged = session.flags.includes(question.id);
    return <section className="app-view custom-module">
      <header className="custom-test-header"><div><span className="custom-eyebrow">Custom module</span><h2>Your focused test</h2><p>Answers and explanations unlock after submission.</p></div><div className="custom-timer" aria-label="Elapsed time"><Clock3 size={20} /><span>{timeLabel(elapsed)}</span><small>elapsed</small></div></header>
      {storageWarning && <p role="status">{storageWarning}</p>}
      <div className="custom-test-layout"><article className="custom-panel custom-question">
        <div className="custom-question-meta"><span>Question {session.index + 1} of {session.questions.length}</span><span>{question.subjectTitle}</span></div>
        <QuestionDetails question={question} />
        <div className="custom-answer-options" role="radiogroup" aria-label="Choose an answer">{question.options.map((option, index) => <button type="button" role="radio" aria-checked={session.answers[question.id] === index} className={session.answers[question.id] === index ? 'is-selected' : ''} disabled={session.answers[question.id] !== undefined} onClick={() => setSession(current => current.status !== 'active' || current.answers[question.id] !== undefined ? current : ({ ...current, answers: { ...current.answers, [question.id]: index } }))} key={index}><span className="custom-option-letter">{String.fromCharCode(65 + index)}</span><span>{option}</span>{session.answers[question.id] === index && <Check size={18} />}</button>)}</div>
        <div className="custom-question-tools"><button type="button" aria-pressed={flagged} onClick={() => setSession(current => ({ ...current, flags: flagged ? current.flags.filter(id => id !== question.id) : [...current.flags, question.id] }))}><Flag size={16} />{flagged ? 'Marked for review' : 'Mark for review'}</button>{session.answers[question.id] !== undefined && <span role="status">Answer locked</span>}</div>
        <div className="custom-question-navigation"><button className="button button-secondary" disabled={session.index === 0} onClick={() => setSession(current => ({ ...current, index: current.index - 1 }))}><ArrowLeft size={16} />Previous</button><button className="button button-primary" disabled={session.index === session.questions.length - 1} onClick={() => setSession(current => ({ ...current, index: current.index + 1 }))}>Next<ArrowRight size={16} /></button></div>
      </article><aside className="custom-panel custom-test-sidebar"><h3>Your progress</h3><p>{answered} of {session.questions.length} answered</p><div className="custom-progress-track"><span style={{ width: `${answered / session.questions.length * 100}%` }} /></div><nav className="custom-question-grid" aria-label="Question navigator">{session.questions.map((entry, index) => <button key={entry.id} aria-label={`Go to question ${index + 1}${session.answers[entry.id] !== undefined ? ', answered' : ', unanswered'}${session.flags.includes(entry.id) ? ', marked for review' : ''}`} aria-current={index === session.index ? 'step' : undefined} className={`${session.answers[entry.id] !== undefined ? 'is-answered' : ''} ${session.flags.includes(entry.id) ? 'is-flagged' : ''}`} onClick={() => setSession(current => ({ ...current, index }))}>{index + 1}</button>)}</nav><small>Filled: answered · Gold border: review</small>
        {confirmSubmit ? <div className="custom-submit-confirm" role="region" aria-label="Submit confirmation"><strong>Finish this test?</strong><p>{session.questions.length - answered} unanswered. You cannot change answers after submitting.</p><button className="button button-primary" onClick={finish}>Submit and reveal answers</button><button className="button button-secondary" onClick={() => setConfirmSubmit(false)}>Keep working</button></div> : <button className="button button-primary custom-submit" onClick={() => setConfirmSubmit(true)}>Submit test</button>}
        <button className="custom-text-button" onClick={onBack}>Return to practice · test stays saved</button>
      </aside></div>
    </section>;
  }

  const search = query.trim().toLowerCase();
  const shown = catalog.filter(subject => subject.title.toLowerCase().includes(search) || subject.chapters.some(chapter => chapter.title.toLowerCase().includes(search)));
  return <section className="app-view custom-module">
    <header className="custom-hero"><div className="custom-hero-top"><span className="custom-eyebrow"><SlidersHorizontal size={18} />Custom modules</span><button className="custom-text-button" onClick={onBack}><ArrowLeft size={16} />All practice paths</button></div><h2>A test built around you.</h2><p>Mix subjects or pick individual chapters from your prepared topic-wise questions.</p><div className="custom-hero-tags"><span><Layers3 size={16} />Mix as many chapters as you like</span><span><Clock3 size={16} />Timed from the first question</span><span><BookOpen size={16} />Answers at the end</span></div></header>
    <div className="custom-setup-layout"><div className="custom-panel"><div className="custom-section-heading"><div><span className="custom-step">01 · Your syllabus</span><h3>Choose your subjects & chapters</h3></div><div className="custom-actions"><button className="custom-text-button" onClick={() => setSelected(catalog.flatMap(subject => subject.chapters.map(chapter => chapter.key)))}>Select all</button><button className="custom-text-button" disabled={!selected.length} onClick={() => setSelected([])}>Clear</button></div></div>
      <label className="custom-search"><Search size={18} /><input type="search" aria-label="Search subjects or chapters" placeholder="Search subjects or chapters" value={query} onChange={event => setQuery(event.target.value)} /></label>
      <div className="custom-subject-list">{shown.map(subject => {
        const picked = subject.chapters.filter(chapter => selectedSet.has(chapter.key)).length;
        const all = subject.chapters.length > 0 && picked === subject.chapters.length;
        const chapters = subject.title.toLowerCase().includes(search) ? subject.chapters : subject.chapters.filter(chapter => chapter.title.toLowerCase().includes(search));
        return <div className={`custom-subject ${picked ? 'has-selection' : ''}`} key={subject.id}><div className="custom-subject-heading"><label><input type="checkbox" aria-label={`Select all ${subject.title} chapters`} disabled={!subject.chapters.length} checked={all} ref={input => { if (input) input.indeterminate = picked > 0 && !all; }} onChange={() => toggleSubject(subject)} /><span>{subject.title}<small>{subject.chapters.length ? `${picked} / ${subject.chapters.length} chapters selected` : 'Coming soon'}</small></span></label>{subject.chapters.length > 0 && <span className="custom-subject-count">{subject.chapters.reduce((sum, chapter) => sum + chapter.questions.length, 0)} Qs</span>}</div>
          {subject.chapters.length > 0 && <details open={search ? true : undefined}><summary>Choose individual chapters</summary><div className="custom-chapters">{chapters.map(chapter => <label key={chapter.key}><input type="checkbox" checked={selectedSet.has(chapter.key)} onChange={() => toggleChapter(chapter.key)} /><span>{chapter.title}</span><small>{chapter.questions.length} Qs</small></label>)}</div></details>}
        </div>;
      })}{shown.length === 0 && <p className="custom-empty">No matching subjects or chapters. Try a different search.</p>}</div>
    </div><aside className="custom-panel custom-builder-summary"><span className="custom-step">02 · Test length</span><h3>Make it your session</h3><fieldset className="custom-size-picker"><legend>Number of questions</legend>{CUSTOM_TEST_SIZES.map(size => <label key={size} className={count === size ? 'is-selected' : ''}><input type="radio" name="custom-size" value={size} checked={count === size} onChange={() => setCount(size)} /><strong>{size}</strong><span>questions</span></label>)}</fieldset><div className="custom-selection-summary"><div><span>Subjects</span><strong>{selectedSubjects}</strong></div><div><span>Chapters</span><strong>{selected.length}</strong></div><div><span>Available questions</span><strong>{pool.length.toLocaleString('en-IN')}</strong></div></div><p className="custom-start-hint" role="status">{pool.length >= count ? `${count} unique questions will be randomly selected from your filters.` : `Select chapters with at least ${count} questions to begin.`}</p><button className="button button-primary custom-start" disabled={pool.length < count} onClick={start}>Start {count}-question test<ArrowRight size={17} /></button><p className="custom-fine-print">The timer tracks elapsed time with no time limit. Selecting an option locks your answer immediately. Each correct answer earns 1 point; there is no negative marking.</p></aside></div>
  </section>;
}
