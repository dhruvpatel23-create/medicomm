import { useEffect, useRef, useState } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { ArrowLeft, ArrowRight, Check, Clock3, Flag, Loader2, LockKeyhole, Play, RotateCcw, ShieldCheck, X } from 'lucide-react';
import { apiRequest } from '../lib/api';
import { createTestAnswerQueue } from '../lib/testAnswerQueue';
import MassTestLeaderboard from './MassTestLeaderboard';
import './fmge-tests.css';

const endpoint = '/api/practice/fmge-tests';
const clockText = seconds => `${Math.floor(seconds / 3600)}:${String(Math.floor(seconds % 3600 / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;

function ConfirmDialog({ open, onOpenChange, title, children, action, onConfirm, busy, error }) {
  return <Dialog.Root open={open} onOpenChange={value => !busy && onOpenChange(value)}>
    <Dialog.Portal><Dialog.Overlay className="ft-dialog-overlay" /><Dialog.Content className="ft-dialog">
      <Dialog.Title>{title}</Dialog.Title>
      <Dialog.Description className="ft-muted">{children}</Dialog.Description>
      {error && <p className="ft-error" role="alert">{error}</p>}
      <div className="ft-dialog-actions"><Dialog.Close className="button button-secondary" disabled={busy}>Cancel</Dialog.Close><button className="button button-primary" disabled={busy} onClick={onConfirm}>{busy ? 'Please wait…' : action}</button></div>
      <Dialog.Close className="ft-dialog-close" aria-label="Close" disabled={busy}><X size={18} /></Dialog.Close>
    </Dialog.Content></Dialog.Portal>
  </Dialog.Root>;
}

export default function FmgePracticeTests({ onSessionChange, category = 'practice', onUnlockPractice }) {
  const [catalog, setCatalog] = useState(null);
  const [waitingRoom, setWaitingRoom] = useState(null);
  const [attempt, setAttempt] = useState(null);
  const [instructions, setInstructions] = useState(null);
  const [confirmFinish, setConfirmFinish] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [busy, setBusy] = useState(false);
  const [saving, setSaving] = useState(false);
  const [now, setNow] = useState(Date.now());
  const [offset, setOffset] = useState(0);
  const [reviewFilter, setReviewFilter] = useState('all');
  const busyRef = useRef(false);
  const alive = useRef(true);
  const startKey = useRef(null);
  const questionTop = useRef(null);
  const serverClock = useRef(null);
  const answerQueue = useRef(null);
  if (!answerQueue.current) answerQueue.current = createTestAnswerQueue({
    send: async (base, change) => {
      const data = await apiRequest(`${endpoint}/attempts/${base.id}`, { method: 'PATCH',
        body: JSON.stringify({ ...change, revision: base.revision }), timeoutMs: 20000 });
      if (data.message && alive.current) setNotice(data.message);
      return data.attempt;
    },
    onChange: value => { if (alive.current) {
      setAttempt(value);
      if (value.serverNow !== serverClock.current) {
        serverClock.current = value.serverNow; setOffset(value.serverNow - Date.now());
      }
    } },
    onSaving: value => { if (alive.current) setSaving(value); },
    onError: e => { if (alive.current) setError(`${e.message} Your latest changes are not confirmed saved. Reload your saved attempt to continue.`); },
  });

  useEffect(() => {
    onSessionChange?.(attempt?.status === 'active' || attempt?.status === 'break');
  }, [attempt?.status, onSessionChange]);
  useEffect(() => () => onSessionChange?.(false), [onSessionChange]);

  useEffect(() => {
    alive.current = true;
    const timer = setInterval(() => setNow(Date.now()), 1000);
    return () => { alive.current = false; clearInterval(timer); };
  }, []);

  async function request(path, options = {}) {
    if (busyRef.current) return;
    busyRef.current = true; setBusy(true); setError(''); setNotice('');
    try {
      await answerQueue.current.flush();
      const data = await apiRequest(`${endpoint}${path}`, { ...options, timeoutMs: 20000 });
      if (!alive.current) return data;
      if (data.attempt) {
        answerQueue.current.reset(data.attempt);
        serverClock.current = data.attempt.serverNow;
        setWaitingRoom(null);
        setAttempt(data.attempt); setOffset(data.attempt.serverNow - Date.now());
        setNow(Date.now());
        if (data.message) setNotice(data.message);
      } else if (data.waitingRoom) {
        setWaitingRoom(data.waitingRoom);
        setOffset(data.waitingRoom.serverNow - Date.now());
      } else {
        setCatalog(data);
        if (Number.isFinite(data.serverNow)) setOffset(data.serverNow - Date.now());
      }
      return data;
    } catch (e) {
      if (alive.current) setError(`${e.message} ${options.method === 'PATCH' ? 'This change was not confirmed saved. Reload your saved attempt before continuing.' : ''}`);
    } finally {
      busyRef.current = false;
      if (alive.current) setBusy(false);
    }
  }
  useEffect(() => { request(''); }, []);

  useEffect(() => {
    if (category !== 'grand' || attempt) return;
    // Stagger requests so a waiting-room crowd does not poll in lockstep.
    const refresh = () => {
      if (!busyRef.current && document.visibilityState === 'visible') {
        request(waitingRoom ? `/${waitingRoom.testId}/waiting-room` : '');
      }
    };
    const timer = setInterval(refresh, waitingRoom ? 5000 + Math.random() * 2000 : 30000 + Math.random() * 5000);
    document.addEventListener('visibilitychange', refresh);
    window.addEventListener('online', refresh);
    return () => { clearInterval(timer); document.removeEventListener('visibilitychange', refresh); window.removeEventListener('online', refresh); };
  }, [category, attempt?.id, waitingRoom?.testId]);

  const remaining = attempt?.deadline ? Math.max(0, Math.ceil((attempt.deadline - now - offset) / 1000)) : 0;
  useEffect(() => {
    if (attempt?.status !== 'active') return;
    const sync = () => { if (!busyRef.current && !answerQueue.current.pending) request(`/attempts/${attempt.id}`); };
    const interval = setInterval(sync, remaining === 0 ? 5000 : 30000);
    if (remaining === 0) sync();
    const visible = () => { if (document.visibilityState === 'visible') sync(); };
    document.addEventListener('visibilitychange', visible);
    window.addEventListener('online', sync);
    return () => { clearInterval(interval); document.removeEventListener('visibilitychange', visible); window.removeEventListener('online', sync); };
  }, [attempt?.id, attempt?.status, remaining === 0]);

  useEffect(() => {
    if (attempt?.status !== 'active') return;
    const beforeUnload = event => { event.preventDefault(); event.returnValue = ''; };
    window.addEventListener('beforeunload', beforeUnload);
    return () => window.removeEventListener('beforeunload', beforeUnload);
  }, [attempt?.status]);

  useEffect(() => {
    // The start dialog disappears when the attempt opens. Move focus into the
    // exam instead of leaving it on a removed start button or the skip link.
    if (attempt?.status === 'active') questionTop.current?.focus({ preventScroll: true });
  }, [attempt?.id, attempt?.part, attempt?.status]);

  const save = body => { setNotice(''); answerQueue.current.enqueue(body); };
  async function navigate(index) {
    save({ currentIndex: index });
    questionTop.current?.scrollIntoView({ behavior: 'auto', block: 'start' });
  }
  async function leave() {
    if (busyRef.current) return;
    setBusy(true);
    try { await answerQueue.current.flush(); }
    catch { setBusy(false); return; }
    setAttempt(null); setReviewFilter('all'); setConfirmFinish(false);
    setBusy(false);
    await request('');
  }
  const statusMessage = <>
    {error && <div className="ft-error" role="alert"><p>{error}</p><button className="button button-secondary" disabled={busy || saving} onClick={() => { answerQueue.current.reset(attempt); request(attempt ? `/attempts/${attempt.id}` : ''); }}>{attempt ? 'Reload saved attempt' : 'Retry'}</button></div>}
    {notice && <p className="ft-notice" role="status">{notice}</p>}
  </>;

  const tests = catalog?.tests.filter(test => (test.category ?? 'practice') === category) ?? [];

  if (!attempt && waitingRoom) {
    const untilStart = Math.max(0, Math.ceil((Date.parse(waitingRoom.startsAt) - now - offset) / 1000));
    const unlocked = waitingRoom.stage === 'open';
    return <div className="fmge-tests ft-waiting-room">
      {statusMessage}
      <p className="eyebrow">FMGE / Grand test waiting room</p>
      <h3>{waitingRoom.title}</h3>
      <p>Test opens on 27 October 2026 at 2:00 pm IST.</p>
      <p className="ft-wait-countdown" role="timer" aria-label="Time until test opens">{clockText(untilStart)}</p>
      <p>{unlocked ? 'The test is now open. Start Part 1 when you are ready.' : 'You are in the waiting room. Questions unlock at the scheduled start. Keep this page open; availability updates automatically.'}</p>
      <p className="ft-muted">300 questions · Two parts of 150 questions · 150 minutes per part · One official attempt</p>
      <div className="ft-break-actions">
        <button className="button button-secondary" disabled={busy} onClick={() => { setWaitingRoom(null); request(''); }}>Back to tests</button>
        <button className="button button-primary" disabled={busy || !unlocked} onClick={() => {
          startKey.current = crypto.randomUUID();
          setInstructions({ id: waitingRoom.testId, title: waitingRoom.title });
        }}>{unlocked ? 'Start test' : 'Waiting for 2:00 pm IST'} <ArrowRight size={16} /></button>
      </div>
      <ConfirmDialog open={Boolean(instructions)} onOpenChange={open => !open && setInstructions(null)} title={`${waitingRoom.title} — ready to begin?`} busy={busy} error={error} action="Start Part 1" onConfirm={async () => {
        const data = await request(`/${waitingRoom.testId}/start`, { method: 'POST', body: JSON.stringify({ startKey: startKey.current }) });
        if (data) setInstructions(null);
      }}>Each part contains 150 questions with 150 minutes. Your timer begins when you start each part and continues if you leave. Answers save as you select them. You have one official attempt; reopening the test resumes that attempt.</ConfirmDialog>
    </div>;
  }

  if (!attempt) return <div className="fmge-tests">
    <div className="ft-intro"><div><p className="eyebrow">FMGE / {category === 'grand' ? 'Grand tests' : 'Full-length practice'}</p><h3>One exam. Two parts. Your next milestone.</h3><p>300 questions across 20 subjects, following your FMGE subject-wise guide.</p></div><span className="ft-rule"><ShieldCheck size={17} /> No negative marking</span></div>
    <div className="ft-metrics"><span><strong>300</strong> questions</span><span><strong>2 × 150 min</strong> timed parts</span><span><strong>150 / 300</strong> to pass</span></div>
    {statusMessage}
    {!catalog && <p role="status" className="ft-muted">{busy ? 'Loading your tests…' : 'Tests are unavailable. Please retry.'}</p>}
    <div className="test-card-stack">{tests.map((test, index) => {
      const active = test.attempts.find(a => a.status !== 'completed');
      const latest = test.attempts.find(a => a.status === 'completed');
      const scheduledStage = test.waitingRoomOpensAt
        ? now + offset < Date.parse(test.waitingRoomOpensAt) ? 'locked' : now + offset < Date.parse(test.startsAt) ? 'waiting' : 'open'
        : 'open';
      return <article className={`exam-test-card ft-test-card${category === 'grand' ? ' exam-test-card-grand' : ''}`} key={test.id}>
        <span className="exam-test-number" aria-hidden="true">0{index + 1}</span>
        <div className="exam-test-copy"><p className="exam-test-label">{category === 'grand' ? `Grand test${test.access === 'free' ? ' • Free' : ''}` : 'Full syllabus • FMGE'}</p><h3>{test.title}</h3><p className="ft-card-meta">300 questions · 300 marks{active ? ` · ${active.status === 'break' ? 'Between parts' : `Part ${active.part} in progress`}` : latest ? ` · Last score ${latest.score}/300` : ''}</p></div>
        {test.startsAt && <div className="exam-test-date"><span>Scheduled date</span><time dateTime={test.startsAt}>{new Date(test.startsAt).toLocaleDateString('en-GB', { timeZone: 'Asia/Kolkata' })} · {new Date(test.startsAt).toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour: 'numeric', minute: '2-digit', hour12: true })} IST</time></div>}
        <div className="ft-card-actions">{latest && <button className="ft-text-button" disabled={busy} onClick={() => request(`/attempts/${latest.id}`)}>View result</button>}
          {test.waitingRoomOpensAt && <p className="ft-muted">Waiting room: 1:00 pm IST · Test: 2:00 pm IST</p>}
          {!(test.singleAttempt && latest && !active) && <button className="button button-primary" disabled={busy || scheduledStage === 'locked'} onClick={() => {
            if (test.locked) { onUnlockPractice?.(); return; }
            if (scheduledStage === 'waiting') { request(`/${test.id}/waiting-room`, { method: 'POST', body: '{}' }); return; }
            if (active) request(`/attempts/${active.id}`);
            else { startKey.current = crypto.randomUUID(); setInstructions(test); }
          }}>{test.locked ? 'Unlock Practice Tests' : scheduledStage === 'locked' ? 'Waiting room opens at 1:00 pm IST' : scheduledStage === 'waiting' ? 'Enter waiting room' : active ? 'Resume' : latest ? 'Retake test' : 'Start test'} {test.locked ? <LockKeyhole size={16} /> : <ArrowRight size={16} />}</button>}</div>
      </article>;
    })}</div>
    {category === 'grand' && tests.filter(test => test.rankReleaseAt).map(test => <MassTestLeaderboard key={test.id} testId={test.id} releasesAt={test.rankReleaseAt} />)}
    {catalog && <details className="ft-blueprint"><summary>View the subject-wise blueprint</summary><div className="ft-blueprint-grid">{catalog.blueprint.map(s => <div key={s.id}><span>{s.title}</span><strong>{s.count}</strong></div>)}</div><p className="ft-muted">100 preclinical/paraclinical + 200 clinical questions. Subject counts apply to the full test, not separately to each part.</p></details>}
    {tests.some(t => t.attempts.some(a => a.status === 'completed')) && <details className="ft-blueprint"><summary>Previous attempts</summary>{tests.flatMap(t => t.attempts.filter(a => a.status === 'completed').map(a => <div className="ft-history" key={a.id}><span>{t.title} · {new Date(a.completedAt).toLocaleDateString('en-IN')} · {a.score}/300</span><button className="ft-text-button" disabled={busy} onClick={() => request(`/attempts/${a.id}`)}>Review attempt</button></div>))}</details>}
    <ConfirmDialog open={Boolean(instructions)} onOpenChange={open => !open && setInstructions(null)} title={`${instructions?.title ?? ''} — ready to begin?`} busy={busy} error={error} action="Start Part 1" onConfirm={async () => {
      const data = await request(`/${instructions.id}/start`, { method: 'POST', body: JSON.stringify({ startKey: startKey.current }) });
      if (data) setInstructions(null);
    }}>
      Each part has 150 questions and a 150-minute timer. Answers save as you select them. You may change answers and mark questions for review within the active part. Submitting a part locks its answers. The clock keeps running if you leave or close the page. Take a break after Part 1, then start Part 2 when ready. Each correct answer earns one mark; wrong and unanswered questions earn zero. Results unlock after both parts. {instructions?.singleAttempt && 'You have one official attempt; reopening resumes that attempt.'}
    </ConfirmDialog>
  </div>;

  if (attempt.status === 'break') return <div className="fmge-tests ft-break">
    {statusMessage}<span className="ft-break-icon"><Check size={30} /></span><p className="eyebrow">Part 1 submitted</p><h3>Take a breath. You’re halfway there.</h3>
    <p>Your first 150 questions are locked and saved. Part 2 has another 150 questions and a fresh 150-minute timer. The break is untimed in this practice test.</p>
    <div className="ft-break-actions"><button className="button button-secondary" disabled={busy} onClick={leave}>Back to tests</button><button className="button button-primary" disabled={busy} onClick={() => request(`/attempts/${attempt.id}/next-part`, { method: 'POST', body: '{}' })}><Play size={16} /> Start Part 2</button></div>
  </div>;

  if (attempt.status === 'completed') {
    const result = attempt.result;
    const passed = result.score >= result.passMark;
    const review = attempt.questions.filter(q => reviewFilter === 'all' || (reviewFilter === 'marked' ? attempt.marked[q.id] : reviewFilter === 'unanswered' ? attempt.answers[q.id] == null : reviewFilter === 'incorrect' ? attempt.answers[q.id] != null && attempt.answers[q.id] !== q.answerIndex : attempt.answers[q.id] === q.answerIndex));
    return <div className="fmge-tests">
      {statusMessage}<button className="ft-text-button" disabled={busy} onClick={leave}><ArrowLeft size={16} /> All FMGE tests</button>
      <div className={`ft-result ${passed ? 'ft-result-pass' : ''}`}><div><p className="eyebrow">{attempt.title} / Test complete</p><h3>{passed ? 'Qualifying score achieved.' : 'Your next improvement starts here.'}</h3><p>{passed ? 'You met the practice-test qualifying score of 150.' : 'Review the gaps below and build towards 150.'}</p></div><div className="ft-score"><strong>{result.score}</strong><span>/ 300</span></div></div>
      <div className="ft-metrics"><span><strong>{result.correct}</strong> correct</span><span><strong>{result.incorrect}</strong> incorrect</span><span><strong>{result.unanswered}</strong> unanswered</span></div>
      {attempt.rankReleaseAt && <MassTestLeaderboard testId={attempt.testId} releasesAt={attempt.rankReleaseAt} />}
      <h3 className="ft-subheading">Your subject breakdown</h3><div className="ft-subject-results">{result.subjects.map(s => <div key={s.id}><span>{s.title}</span><strong>{s.correct}/{s.total}</strong><progress value={s.correct} max={s.total} aria-label={`${s.title}: ${s.correct} out of ${s.total}`} /></div>)}</div>
      <div className="ft-review-heading"><h3>Review every answer</h3><label>Show <select value={reviewFilter} onChange={e => setReviewFilter(e.target.value)}><option value="all">All questions</option><option value="incorrect">Incorrect</option><option value="unanswered">Unanswered</option><option value="correct">Correct</option><option value="marked">Marked for review</option></select></label></div>
      {!review.length && <p className="ft-muted">No questions in this category.</p>}
      <div className="ft-review-list">{review.map(q => {
        const selected = attempt.answers[q.id];
        const state = selected == null ? 'unanswered' : selected === q.answerIndex ? 'correct' : 'incorrect';
        return <details key={q.id} className="ft-review-item"><summary><span>Question {q.number} · {q.subjectTitle}</span><span className={`ft-verdict ft-${state}`}>{state}</span></summary><h4>{q.prompt}</h4>{q.imageUrls?.map((url, i) => <div key={i} className="ft-image-wrap" style={{ margin: '10px 0' }}><img src={url} alt={`Visual ${i+1}`} style={{ maxWidth: '100%', maxHeight: '320px', borderRadius: '8px', objectFit: 'contain' }} /></div>)}<ol>{q.options.map((o,i) => <li key={i} className={i === q.answerIndex ? 'ft-correct-option' : i === selected ? 'ft-wrong-option' : ''}><b>{String.fromCharCode(65+i)}.</b> {o}{i === q.answerIndex && <small>Correct answer</small>}{i === selected && <small>Your answer</small>}</li>)}</ol><div className="ft-explanation"><strong>Explanation</strong><p>{q.explanation}</p></div><p className="ft-muted">Source: {q.sourceExam || 'FMGE Practice'}</p></details>;
      })}</div>
    </div>;
  }

  const question = attempt.questions[attempt.currentIndex] ?? attempt.questions[0];
  const answered = attempt.questions.filter(q => attempt.answers[q.id] != null).length;
  const marked = attempt.questions.filter(q => attempt.marked[q.id]).length;
  const blocked = busy || remaining === 0 || Boolean(error);
  return <div className="fmge-tests">
    {statusMessage}
    <div className="ft-runbar"><div><p className="eyebrow">{attempt.title} / Part {attempt.part} of 2</p><strong>{answered} of 150 answered</strong></div><div className={`ft-timer ${remaining < 300 ? 'ft-timer-urgent' : ''}`} role="timer" aria-label="Time remaining"><Clock3 size={18} />{clockText(remaining)}</div><button className="button button-secondary" disabled={busy} onClick={leave}>Save & exit</button></div>
    <p className="ft-save-status" role="status">{busy || saving ? <><Loader2 size={14} className="ft-spin" /> Saving / syncing…</> : error ? 'Connection or save problem — reload your saved attempt to continue.' : <><ShieldCheck size={14} /> Answers saved on server · Timer continues if you leave</>}</p>
    <div className="ft-exam-layout"><div className="ft-question" ref={questionTop} tabIndex={-1} aria-label={`Question ${question.number}`}>
      <div className="ft-question-top"><span>QUESTION {question.number} / 300</span><span>+1 mark · No negative marking</span></div>
      <h3>{question.prompt}</h3>
      {question.imageUrls?.map((url, i) => <div key={i} className="ft-image-wrap" style={{ margin: '12px 0' }}><img src={url} alt={`Visual ${i+1}`} style={{ maxWidth: '100%', maxHeight: '360px', borderRadius: '8px', objectFit: 'contain' }} /></div>)}
      <div className="ft-options" role="group" aria-label="Answer options">{question.options.map((option, index) => <button type="button" key={index} disabled={blocked} aria-pressed={attempt.answers[question.id] === index} className={`ft-option ${attempt.answers[question.id] === index ? 'ft-option-selected' : ''}`} onClick={() => save({ questionId: question.id, optionIndex: index })}><span>{String.fromCharCode(65+index)}</span><span>{option}</span>{attempt.answers[question.id] === index && <Check size={18} />}</button>)}</div>
      <div className="ft-question-tools"><button className={`ft-text-button ${attempt.marked[question.id] ? 'ft-marked-text' : ''}`} disabled={blocked} aria-pressed={Boolean(attempt.marked[question.id])} onClick={() => save({ questionId: question.id, marked: !attempt.marked[question.id] })}><Flag size={16} /> {attempt.marked[question.id] ? 'Marked for review' : 'Mark for review'}</button><button className="ft-text-button" disabled={blocked || attempt.answers[question.id] == null} onClick={() => save({ questionId: question.id, optionIndex: null })}><RotateCcw size={15} /> Clear answer</button></div>
      <div className="ft-question-navigation"><button className="button button-secondary" disabled={blocked || attempt.currentIndex === 0} onClick={() => navigate(attempt.currentIndex-1)}><ArrowLeft size={16} /> Previous</button>{attempt.currentIndex < 149 ? <button className="button button-primary" disabled={blocked} onClick={() => navigate(attempt.currentIndex+1)}>Next question <ArrowRight size={16} /></button> : <button className="button button-primary" disabled={blocked} onClick={() => setConfirmFinish(true)}>Review & submit part</button>}</div>
    </div><aside className="ft-palette"><h4>Question navigator</h4><div className="ft-palette-legend"><span><i className="answered" /> Answered</span><span><i className="marked" /> Review</span><span><i /> Unanswered</span></div><div className="ft-question-grid">{attempt.questions.map((q,index) => <button type="button" key={q.id} disabled={blocked} className={`${attempt.answers[q.id] != null ? 'answered' : ''} ${attempt.marked[q.id] ? 'marked' : ''} ${index === attempt.currentIndex ? 'current' : ''}`} aria-label={`Question ${q.number}, ${attempt.answers[q.id] != null ? 'answered' : 'unanswered'}${attempt.marked[q.id] ? ', marked for review' : ''}`} aria-current={index === attempt.currentIndex ? 'step' : undefined} onClick={() => navigate(index)}>{q.number}</button>)}</div><p className="ft-muted">{150-answered} unanswered · {marked} marked</p><button className="button button-primary" disabled={blocked} onClick={() => setConfirmFinish(true)}>Submit Part {attempt.part}</button></aside></div>
    <ConfirmDialog open={confirmFinish} onOpenChange={setConfirmFinish} title={`Submit Part ${attempt.part}?`} busy={busy} error={error} action={`Submit Part ${attempt.part}`} onConfirm={async () => {
      const data = await request(`/attempts/${attempt.id}/finish-part`, { method: 'POST', body: JSON.stringify({ part: attempt.part }) });
      if (data) setConfirmFinish(false);
    }}>You have answered {answered} of 150 questions. {150-answered} are unanswered and {marked} are marked for review. Answers marked for review are still scored. After submission, you cannot return to this part.{attempt.part === 1 ? ' You can take a break before starting Part 2.' : ' Your final score and explanations will be available immediately.'}</ConfirmDialog>
  </div>;
}
