import { useRef, useState } from 'react';
import { Check, Clock3, Loader2, UserPlus } from 'lucide-react';
import { useFriends } from './CommunityFriends';
import { Avatar, muted, primary } from './SocialUI';

export default function DuelOpponentCard({ opponent }) {
  const model = useFriends();
  const pending = useRef(false);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState('');
  const [error, setError] = useState('');
  const isFriend = model.friends.some(person => person.id === opponent.id);
  const requested = model.outgoingRequests.some(request => request.user?.id === opponent.id);
  const incoming = model.incomingRequests.find(request => request.user?.id === opponent.id);

  async function connect() {
    if (pending.current) return;
    pending.current = true;
    setSaving(true);
    setNotice('');
    setError('');
    try {
      const result = incoming
        ? await model.acceptRequest(incoming.id, opponent.id)
        : await model.sendRequest(opponent.id);
      setNotice(incoming || result.accepted
        ? `You and ${opponent.name} are now friends!`
        : `Friend request sent to ${opponent.name}.`);
    } catch (err) {
      setError(err.message || 'Could not connect. Please try again.');
    } finally {
      pending.current = false;
      setSaving(false);
    }
  }

  const Icon = saving || model.busy ? Loader2 : isFriend || incoming ? Check : requested ? Clock3 : UserPlus;
  return <section aria-label="Opponent profile" className="mt-6 rounded-2xl border border-slate-200 p-4 dark:border-slate-700 sm:p-5">
    <p className="mb-4 text-[10px] font-bold uppercase tracking-widest text-slate-500 dark:text-slate-400">Your opponent</p>
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
      <div className="flex min-w-0 flex-1 items-center gap-3">
        <Avatar name={opponent.name} src={opponent.profileImageUrl} />
        <div className="min-w-0">
          <h4 className="break-words text-base font-bold">{opponent.name}</h4>
          <p className={`${muted} break-words`}>{opponent.medicalCollege || 'College not added'}</p>
          {Number.isFinite(opponent.rating) && <p className="mt-1 text-xs text-cyan-700 dark:text-cyan-300">{opponent.rating.toLocaleString()} Elo at match start</p>}
        </div>
      </div>
      <button type="button" className={`${primary} shrink-0`} onClick={connect}
        disabled={saving || model.busy || Boolean(model.error) || isFriend || (requested && !incoming)}>
        <Icon size={16} className={saving || model.busy ? 'motion-safe:animate-spin' : ''} />
        {saving ? 'Saving...' : model.busy ? 'Loading...' : isFriend ? 'Friends' : incoming ? 'Accept friend request' : requested ? 'Request sent' : 'Add friend'}
      </button>
    </div>
    {notice && <p role="status" className="mt-3 text-sm text-emerald-700 dark:text-emerald-300">{notice}</p>}
    {error && <p role="alert" className="mt-3 text-sm text-red-600 dark:text-red-400">{error}</p>}
    {model.error && <p role="alert" className="mt-3 text-sm text-red-600 dark:text-red-400">{model.error} <button type="button" className="underline" onClick={model.retry}>Retry loading friends</button></p>}
  </section>;
}
