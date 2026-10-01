import { useEffect, useState } from 'react';
import { Check, Loader2, MessageCircle, UserPlus, Users } from 'lucide-react';
import { apiRequest } from '../lib/api';
import { Avatar, EmptyState, SearchField } from './SocialUI';
import { Button } from './ui/button';
import { Dialog, DialogContent, DialogDescription, DialogTitle, DialogTrigger } from './ui/dialog';

export function useFriends() {
  const [friends, setFriends] = useState([]);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');
  const [version, setVersion] = useState(0);
  useEffect(() => {
    let cancelled = false;
    setBusy(true);
    setError('');
    apiRequest('/api/friends').then(data => {
      if (!cancelled) setFriends(data.friends ?? []);
    }).catch(err => {
      if (!cancelled) setError(err.message || 'Could not load friends.');
    }).finally(() => { if (!cancelled) setBusy(false); });
    return () => { cancelled = true; };
  }, [version]);
  const add = async userId => {
    const data = await apiRequest('/api/friends', { method: 'POST', body: JSON.stringify({ userId }) });
    setFriends(data.friends ?? []);
  };
  return { friends, busy, error, add, retry: () => setVersion(value => value + 1) };
}

export function AddFriendDialog({ model, open, onOpenChange }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [adding, setAdding] = useState(null);
  const [notice, setNotice] = useState('');
  const [retry, setRetry] = useState(0);
  const term = query.trim();

  useEffect(() => {
    let cancelled = false;
    setResults([]);
    setError('');
    if (!open || term.length < 2) { setBusy(false); return; }
    setBusy(true);
    const timer = setTimeout(async () => {
      try {
        const data = await apiRequest(`/api/users/search?q=${encodeURIComponent(term)}`);
        if (!cancelled) setResults(data.users ?? []);
      } catch (err) {
        if (!cancelled) setError(err.message || 'Could not search users.');
      } finally { if (!cancelled) setBusy(false); }
    }, 250);
    return () => { cancelled = true; clearTimeout(timer); };
  }, [term, open, retry]);

  const add = async person => {
    if (adding) return;
    setAdding(person.id);
    setNotice('');
    try { await model.add(person.id); setNotice(`${person.name} added to your friends.`); }
    catch (err) { setNotice(err.message || 'Could not add friend. Please try again.'); }
    finally { setAdding(null); }
  };

  return <Dialog open={open} onOpenChange={value => { onOpenChange(value); if (!value) { setQuery(''); setNotice(''); } }}>
    <DialogTrigger asChild><Button variant="ghost" size="sm" className="shrink-0 text-teal-700 dark:text-teal-200"><UserPlus size={15} />Add friend</Button></DialogTrigger>
    <DialogContent>
      <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-teal-50 text-teal-800 dark:bg-teal-950 dark:text-teal-200"><UserPlus size={23} /></div>
      <DialogTitle>Add friend</DialogTitle>
      <DialogDescription>Find learners by name or college and save them to your friends list.</DialogDescription>
      <div className="mt-5"><SearchField value={query} onChange={value => { setQuery(value); setResults([]); setNotice(''); }} placeholder="Search users by name or college" /></div>
      {notice && <p role="status" className="mt-3 rounded-lg bg-teal-50 p-3 text-sm text-teal-900 dark:bg-teal-950 dark:text-teal-100">{notice}</p>}
      {model.error && <p role="alert" className="mt-3 text-sm text-red-600 dark:text-red-400">{model.error} <button className="underline" onClick={model.retry}>Retry loading friends</button></p>}
      <div className="mt-3 max-h-80 overflow-y-auto">
        {term.length < 2 ? <EmptyState icon={Users} title="Find your study partners">Type at least 2 characters to search for other users.</EmptyState>
          : busy ? <p role="status" className="flex items-center justify-center gap-2 py-10 text-sm text-slate-500"><Loader2 size={17} className="motion-safe:animate-spin" />Searching users…</p>
          : error ? <div role="alert" className="py-6 text-center text-sm text-red-600 dark:text-red-400"><p>{error}</p><Button variant="ghost" className="mt-2" onClick={() => setRetry(value => value + 1)}>Try again</Button></div>
          : results.length ? <ul className="divide-y divide-slate-100 dark:divide-slate-800">{results.map(person => {
            const saved = model.friends.some(friend => friend.id === person.id);
            return <li key={person.id} className="flex items-center gap-3 py-4"><Avatar name={person.name} src={person.profileImageUrl} /><div className="min-w-0 flex-1"><p className="truncate text-sm font-semibold" title={person.name}>{person.name}</p><p className="mt-1 truncate text-xs text-slate-500 dark:text-slate-400" title={person.medicalCollege}>{person.medicalCollege}</p></div><Button size="sm" variant={saved ? 'secondary' : 'default'} disabled={saved || Boolean(adding) || model.busy || Boolean(model.error)} onClick={() => add(person)} aria-label={saved ? `${person.name} is added` : `Add ${person.name}`}>
              {saved ? <Check size={14} /> : adding === person.id ? <Loader2 size={14} className="motion-safe:animate-spin" /> : <UserPlus size={14} />}{saved ? 'Added' : adding === person.id ? 'Adding…' : 'Add'}
            </Button></li>;
          })}</ul> : <EmptyState icon={Users} title="No users found">Try another name or college.</EmptyState>}
      </div>
    </DialogContent>
  </Dialog>;
}

export function FriendsPanel({ model, onAdd, onMessage }) {
  const [query, setQuery] = useState('');
  const [opening, setOpening] = useState(null);
  const visible = model.friends.filter(person => `${person.name} ${person.medicalCollege}`.toLowerCase().includes(query.trim().toLowerCase()));
  if (model.busy) return <p role="status" className="flex items-center gap-2 py-8 text-sm text-slate-500"><Loader2 size={16} className="motion-safe:animate-spin" />Loading friends…</p>;
  if (model.error) return <div role="alert" className="rounded-xl border border-slate-200 p-5 dark:border-slate-800"><p className="text-sm">{model.error}</p><Button variant="outline" className="mt-3" onClick={model.retry}>Try again</Button></div>;
  if (!model.friends.length) return <div className="rounded-2xl border border-dashed border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900"><EmptyState icon={Users} title="Your study circle starts with a friend">Find other learners and keep your study partners close.<div><Button className="mt-4" onClick={onAdd}><UserPlus size={15} />Find friends</Button></div></EmptyState></div>;
  return <div className="space-y-4"><SearchField value={query} onChange={setQuery} placeholder="Search your friends" /><div className="grid gap-3 sm:grid-cols-2">{visible.map(person => <article key={person.id} className="flex min-w-0 items-center gap-3 rounded-2xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900"><Avatar name={person.name} src={person.profileImageUrl} /><div className="min-w-0 flex-1"><h4 className="truncate text-sm font-semibold" title={person.name}>{person.name}</h4><p className="mt-1 truncate text-xs text-slate-500 dark:text-slate-400" title={person.medicalCollege}>{person.medicalCollege}</p><Button variant="ghost" size="sm" className="-ml-3 mt-1 text-teal-700 dark:text-teal-200" disabled={Boolean(opening)} onClick={async () => { setOpening(person.id); try { await onMessage(person.id); } finally { setOpening(null); } }}><MessageCircle size={13} />{opening === person.id ? 'Opening…' : 'Message'}</Button></div></article>)}</div>{!visible.length && <p role="status" className="py-6 text-center text-sm text-slate-500">No friends match your search.</p>}</div>;
}
