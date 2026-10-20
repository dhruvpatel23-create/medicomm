import { useEffect, useState } from "react";
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "./ui/dialog";
import { apiRequest } from "../lib/api";

export default function FriendDuelSetup({ opponent, onClose, onSend }) {
  const [subjects, setSubjects] = useState([]);
  const [questionCount, setQuestionCount] = useState(5);
  const [subjectIds, setSubjectIds] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [retry, setRetry] = useState(0);
  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    apiRequest("/api/duels/challenge/options").then(data => {
      if (active) setSubjects(data.subjects);
    }).catch(error => { if (active) setError(error.message); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [retry]);
  const available = subjects.filter(subject => subjectIds === null || subjectIds.includes(subject.id))
    .reduce((sum, subject) => sum + subject.questionCount, 0);
  async function send(event) {
    event.preventDefault();
    if (sending || loading || available < questionCount) return;
    setSending(true);
    setError("");
    try { await onSend({ questionCount, subjectIds }); }
    catch (error) { setError(error.message || "Could not send the request."); }
    finally { setSending(false); }
  }
  return <Dialog open onOpenChange={open => { if (!open && !sending) onClose(); }}>
    <DialogContent>
      <DialogTitle>Challenge {opponent.name}</DialogTitle>
      <DialogDescription>Choose your questions and subjects, then send the 1v1 request. The match timer remains 3 minutes.</DialogDescription>
      <form onSubmit={send} className="mt-5 space-y-5">
        <fieldset disabled={sending}>
          <legend className="mb-2 text-sm font-semibold">Number of questions</legend>
          <div className="flex gap-3">{[5, 10, 15].map(count => <label key={count} className="flex flex-1 cursor-pointer items-center justify-center gap-2 rounded-lg border border-slate-300 p-3 dark:border-slate-700">
            <input type="radio" name="duel-question-count" value={count} checked={questionCount === count} onChange={() => setQuestionCount(count)} />{count}
          </label>)}</div>
        </fieldset>
        <fieldset disabled={loading || sending}>
          <legend className="mb-2 text-sm font-semibold">Subjects</legend>
          <label className="mb-3 flex items-center gap-2 font-medium">
            <input type="checkbox" checked={subjectIds === null} onChange={event => setSubjectIds(event.target.checked ? null : [])} />All subjects
          </label>
          <div className="grid max-h-60 gap-2 overflow-y-auto sm:grid-cols-2">{subjects.map(subject => <label key={subject.id} className="flex cursor-pointer items-center gap-2 rounded-lg border border-slate-200 p-2 text-sm dark:border-slate-700">
            <input type="checkbox" checked={subjectIds === null || subjectIds.includes(subject.id)} onChange={event => {
              setSubjectIds(current => current === null ? subjects.filter(entry => entry.id !== subject.id).map(entry => entry.id) : event.target.checked
                ? [...current, subject.id] : current.filter(id => id !== subject.id));
            }} />{subject.title}
          </label>)}</div>
        </fieldset>
        {loading && <p role="status">Loading subjects…</p>}
        {!loading && available < questionCount && <p className="text-sm text-amber-700 dark:text-amber-300">Select enough subjects for {questionCount} questions.</p>}
        {error && <p role="alert" className="text-sm text-red-600 dark:text-red-300">{error}</p>}
        {!loading && !subjects.length && <button type="button" className="button button-secondary" onClick={() => setRetry(value => value + 1)}>Retry</button>}
        <div className="flex gap-3">
          <button type="button" className="button button-secondary" disabled={sending} onClick={onClose}>Cancel</button>
          <button type="submit" className="button button-primary" disabled={loading || sending || available < questionCount}>{sending ? "Sending…" : "Send request"}</button>
        </div>
      </form>
    </DialogContent>
  </Dialog>;
}
