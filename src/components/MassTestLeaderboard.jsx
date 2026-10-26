import { useEffect, useState } from 'react';
import { apiRequest } from '../lib/api';

export default function MassTestLeaderboard({ testId, releasesAt }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [offset, setOffset] = useState(0);
  const [retry, setRetry] = useState(0);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    let alive = true, timer;
    async function refresh() {
      try {
        const response = await apiRequest(`/api/practice/fmge-tests/${testId}/leaderboard?offset=${offset}&limit=50`, { timeoutMs: 20000 });
        if (!alive) return;
        const board = response.leaderboard;
        setData(board); setError(''); setLoading(false);
        // Use the server's release status and time, including after a local
        // clock change. Stagger requests from the result-screen crowd.
        const delay = board.released ? 30000 : Math.min(60000, Math.max(1000, Date.parse(board.releasesAt) - board.serverNow + 500));
        timer = setTimeout(refresh, delay + Math.random() * 1000);
      } catch (e) {
        if (!alive) return;
        setError(e.message); setLoading(false);
        timer = setTimeout(refresh, 30000 + Math.random() * 3000);
      }
    }
    setData(null); setLoading(true);
    refresh();
    return () => { alive = false; clearTimeout(timer); };
  }, [testId, offset, retry]);

  const releaseLabel = new Date(releasesAt).toLocaleString('en-IN', {
    timeZone: 'Asia/Kolkata', day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: '2-digit', hour12: true,
  });
  return <section className="ft-leaderboard" aria-label="Grand test leaderboard">
    <h3>Grand test leaderboard</h3>
    {!data?.released && <p>Your individual result is available immediately after submission. Ranks and the leaderboard unlock on <strong>{releaseLabel} IST</strong>.</p>}
    {loading && <p className="ft-muted" role="status">Checking rank availability…</p>}
    {error && <p className="ft-error" role="alert">{error} <button className="ft-text-button" onClick={() => setRetry(value => value + 1)}>Retry</button></p>}
    {data?.released && <>
      <div className="ft-rank-summary">
        <p>{data.yourRank ? <>Your rank: <strong>{data.yourRank.rank}</strong> of {data.completedCount} completed attempts · {data.yourRank.score}/300</> : 'Your rank will appear here after your completed attempt is included in the next update.'}</p>
        <p className="ft-muted">Equal scores share a rank. Only completed attempts are ranked. Updates automatically as participants finish.</p>
      </div>
      {!data.entries.length ? <p className="ft-muted">No completed attempts yet.</p> : <div className="ft-leaderboard-scroll"><table>
        <caption>Ranked results · updated {new Date(data.asOf).toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata' })} IST</caption>
        <thead><tr><th scope="col">Rank</th><th scope="col">Participant</th><th scope="col">Score</th></tr></thead>
        <tbody>{data.entries.map((entry, index) => <tr key={`${offset}-${index}`} className={entry.isYou ? 'ft-leaderboard-you' : undefined}>
          <td>{entry.rank}</td><td>{entry.name}{entry.isYou && <strong> (You)</strong>}</td><td>{entry.score}/{entry.total}</td>
        </tr>)}</tbody>
      </table></div>}
      <div className="ft-leaderboard-pages">
        <button className="button button-secondary" disabled={offset === 0 || loading} onClick={() => setOffset(value => Math.max(0, value - 50))}>Previous</button>
        <span>{data.completedCount ? `${offset + 1}–${Math.min(offset + data.entries.length, data.completedCount)} of ${data.completedCount}` : '0 completed'}</span>
        <button className="button button-secondary" disabled={!data.hasMore || loading} onClick={() => setOffset(value => value + 50)}>Next</button>
      </div>
    </>}
  </section>;
}
