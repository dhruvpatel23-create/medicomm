import { useEffect, useState } from 'react';
import { apiRequest } from '../lib/api';

const dateLabel = date => new Date(date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'Asia/Kolkata' });
const minutes = seconds => `${Math.floor(seconds / 60)} min`;

// Keep the existing dashboard card styles below the screenshot's summary area.
export default function DashboardActivity({ overview, guest, onPractice, onCompete, onProfile, sync }) {
  const data = overview.data;
  const [goal, setGoal] = useState({ exam: '', date: '', weeklyTarget: '' });
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  useEffect(() => { if (data?.goal) setGoal(data.goal); }, [data?.goal]);
  async function saveGoal(event) {
    event.preventDefault(); setBusy(true); setMessage('');
    try { await apiRequest('/api/dashboard/goal', { method: 'PATCH', body: JSON.stringify(goal) }); setEditing(false); overview.reload(); }
    catch (error) { setMessage(error.message); }
    finally { setBusy(false); }
  }
  if (guest) return <article className="card panel"><h3>Start your learning record</h3><p className="panel-copy">Sign in to keep your results, goals and activity across devices.</p><button className="button button-primary" onClick={onProfile}>Manage account</button></article>;
  if (!data) return null;
  const weekTotal = data.weekly.reduce((sum, day) => sum + day.attempts, 0);
  const max = Math.max(1, ...data.weekly.map(day => day.attempts));
  const daysLeft = data.goal ? Math.ceil((Date.parse(data.goal.date) - Date.parse(data.todayDate)) / 86400000) : null;
  return <>
    {sync.message && <p className="form-message" role="status">{sync.message} <button type="button" className="text-button" onClick={sync.retry}>Retry sync</button></p>}
    <div className="dashboard-priority-grid">
      <article className="card panel continue-card"><div className="panel-heading-split"><div><p className="eyebrow">Continue learning</p><h3>{data.resume?.subject || 'Your next question awaits'}</h3><p className="panel-copy">{data.resume ? `Last practised on ${dateLabel(data.resume.answeredAt)}. Continue with the next available question.` : 'Complete a practice question to start your saved learning history.'}</p></div></div><div className="continue-footer"><span>{data.today.attempts} answered today</span><button type="button" className="button button-primary" onClick={() => onPractice(data.resume)}>{data.resume ? 'Resume practice' : 'Start practice'}</button></div></article>
      <article className="card panel exam-countdown-card"><p className="eyebrow">Your study goal</p>
        {data.goal && !editing ? <><h3>{data.goal.exam}</h3><strong className="countdown-number">{Math.abs(daysLeft)}</strong><span>{daysLeft >= 0 ? 'days until your target date' : 'days since your target date'}</span><div className="countdown-footer"><span>Last 7 days</span><strong>{weekTotal} / {data.goal.weeklyTarget} questions</strong></div><button type="button" className="text-button" onClick={() => setEditing(true)}>Edit goal</button></> :
          <form className="profile-form" onSubmit={saveGoal}><h3>Set your next milestone</h3><label className="field"><span>Exam name</span><input required maxLength={80} value={goal.exam} onChange={event => setGoal({ ...goal, exam: event.target.value })} /></label><label className="field"><span>Target exam date</span><input required type="date" value={goal.date} onChange={event => setGoal({ ...goal, date: event.target.value })} /></label><label className="field"><span>Weekly question target</span><input required type="number" min="1" max="5000" value={goal.weeklyTarget} onChange={event => setGoal({ ...goal, weeklyTarget: event.target.value })} /></label><button className="button button-secondary" disabled={busy}>{busy ? 'Saving…' : 'Save goal'}</button>{data.goal && <button type="button" className="text-button" onClick={() => { setGoal(data.goal); setEditing(false); }}>Cancel</button>}</form>}
        {message && <p className="form-message" role="alert">{message}</p>}
      </article>
    </div>
    <div className="dashboard-insight-grid">
      <article className="card panel weekly-chart-card"><div className="panel-heading-split"><div><h3>Weekly progress</h3><p className="panel-copy">MCQs answered in the last 7 days</p></div><strong>{weekTotal} questions</strong></div><div className="weekly-bars" role="img" aria-label={data.weekly.map(day => `${dateLabel(day.date)}: ${day.attempts} questions`).join(', ')}>{data.weekly.map(day => <div key={day.date} title={`${dateLabel(day.date)}: ${day.attempts} questions`}><span style={{ height: day.attempts ? `${Math.max(4, day.attempts / max * 110)}px` : '0px', minHeight: 0 }} /><small>{new Date(day.date).toLocaleDateString('en-IN', { weekday: 'short' })}</small><small>{day.attempts}</small></div>)}</div>{!weekTotal && <p className="panel-copy">No recorded attempts this week yet.</p>}</article>
      <article className="card panel heatmap-card"><div className="panel-heading-split"><div><h3>Study consistency</h3><p className="panel-copy">Last 8 weeks · India time</p></div><strong>{data.stats.streak} {data.stats.streak === 1 ? 'day' : 'days'}</strong></div><div className="study-heatmap" aria-label="Recorded MCQ activity over the last eight weeks">{data.activity.map(day => <span key={day.date} data-level={day.attempts === 0 ? 0 : day.attempts < 10 ? 1 : day.attempts < 30 ? 2 : 3} title={`${dateLabel(day.date)}: ${day.attempts} questions`} />)}</div><div className="heatmap-legend"><span>Less</span><i data-level="0" /><i data-level="1" /><i data-level="2" /><i data-level="3" /><span>More</span></div><p className="panel-copy">Daily history starts with recorded practice. Older account totals are retained.</p></article>
    </div>
    <div className="dashboard-action-grid">
      <article className="card panel recommendation-card"><h3>Worth another look</h3><p className="panel-copy">Topics with missed answers in your saved practice</p><div className="recommendation-list">{data.recommendations.map((topic, index) => <button key={`${topic.mode}:${topic.subjectId}:${topic.topic}`} type="button" onClick={() => onPractice(topic)}><span className="recommendation-index">{index + 1}</span><span><strong>{topic.topic}</strong><small>{topic.subject} · {topic.attempts} attempts</small></span><em>{topic.accuracy}% correct</em></button>)}</div>{!data.recommendations.length && <p className="panel-copy">No missed topics in your recorded practice yet.</p>}</article>
      <article className="card panel recent-battles-card"><div className="panel-heading-split"><div><h3>Recent battles</h3><p className="panel-copy">Your completed 1v1 sessions</p></div><button type="button" className="text-button" onClick={onCompete}>Battle now</button></div><div className="battle-list">{data.battles.map(battle => <div key={battle.id}><span className={`battle-result ${battle.verdict === 'win' ? 'win' : 'loss'}`}>{battle.verdict === 'draw' ? 'D' : battle.verdict === 'win' ? 'W' : 'L'}</span><span><strong>{battle.userScore} – {battle.opponentScore}</strong><small>{dateLabel(battle.completedAt)} · {battle.mode === 'bot' ? 'Practice battle' : 'Rated battle'}</small></span><em>{battle.ratingChange > 0 ? '+' : ''}{battle.ratingChange} rating</em></div>)}</div>{!data.battles.length && <p className="panel-copy">Play your first battle to see your results here.</p>}</article>
    </div>
    <div className="content-grid"><article className="card panel"><h3>Today’s snapshot</h3><div className="stack-list">{[['Questions answered', data.today.attempts], ['Correct answers', data.today.correct], ['Recorded practice time', minutes(data.today.seconds)]].map(([title, value]) => <div className="stack-row" key={title}><span>{title}</span><strong>{value}</strong></div>)}</div></article><article className="card panel"><h3>Recent practice</h3><div className="feed-list">{data.recent.map(item => <div className="feed-item" key={item.id}><div><strong>{item.subject}</strong><p>{item.topic}</p></div><span>{item.correct ? 'Correct' : 'Needs review'} · {dateLabel(item.answeredAt)}</span></div>)}</div>{!data.recent.length && <p className="panel-copy">Your completed questions will appear here.</p>}</article></div>
  </>;
}
