import { useMemo, useRef, useState } from 'react';
import { ArrowLeft, ArrowUpRight, BookOpen, Check, ChevronDown, ImagePlus, Link, Loader2, MessageCircle, MessagesSquare, Plus, Search, Send, ShieldCheck, Users, X } from 'lucide-react';
import { Avatar, EmptyState, SearchField, field, socialPage, surface } from './SocialUI';
import { Button } from './ui/button';

const words = text => text.trim().split(/\s+/).filter(Boolean).length;
const muted = 'text-sm leading-6 text-slate-500 dark:text-slate-400';
const accent = 'bg-[#174b44] text-white hover:bg-[#206257] dark:bg-teal-300 dark:text-teal-950 dark:hover:bg-teal-200';
const entry = 'motion-safe:animate-in motion-safe:fade-in motion-safe:slide-in-from-bottom-2 motion-safe:duration-300';

export default function CommunityThreads(p) {
  const { room, user } = p;
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('all');
  const [sort, setSort] = useState('latest');
  const [pending, setPending] = useState({});
  const locks = useRef(new Set());
  const composer = useRef(null);
  const replyInputs = useRef({});
  const { threads, replies } = useMemo(() => {
    const ids = new Set(room.messages.map(message => message.id));
    const replies = {};
    room.messages.forEach(message => { if (message.parentMessageId) (replies[message.parentMessageId] ||= []).push(message); });
    Object.values(replies).forEach(items => items.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt)));
    return { threads: room.messages.filter(message => !message.parentMessageId || !ids.has(message.parentMessageId)), replies };
  }, [room.messages]);
  const unanswered = threads.filter(message => !replies[message.id]?.length).length;
  const visible = threads.filter(message => {
    const matches = `${message.text || ''} ${message.userName || ''} ${(replies[message.id] || []).map(reply => `${reply.text} ${reply.userName}`).join(' ')}`.toLowerCase().includes(query.trim().toLowerCase());
    return matches && (filter !== 'unanswered' || !replies[message.id]?.length) && (filter !== 'mine' || message.isOwnMessage || message.userId === user?.id);
  }).sort((a, b) => {
    if (sort === 'discussed') return (replies[b.id]?.length || 0) - (replies[a.id]?.length || 0) || new Date(b.createdAt) - new Date(a.createdAt);
    if (sort === 'active') return new Date(replies[b.id]?.at(-1)?.createdAt || b.createdAt) - new Date(replies[a.id]?.at(-1)?.createdAt || a.createdAt);
    return new Date(b.createdAt) - new Date(a.createdAt);
  });
  const submit = async (event, id = null) => {
    event.preventDefault();
    const key = id || 'new';
    if (locks.current.has(key)) return;
    locks.current.add(key); setPending(current => ({ ...current, [key]: true }));
    try { await p.onSend(event, id); } finally { locks.current.delete(key); setPending(current => ({ ...current, [key]: false })); }
  };
  const focusComposer = () => { composer.current?.focus(); composer.current?.scrollIntoView({ block: 'center', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' }); };
  const author = message => <div className="flex min-w-0 flex-wrap items-center gap-x-2 gap-y-1 text-xs"><button type="button" disabled={!message.userId} className="break-words text-left font-semibold text-slate-800 hover:text-teal-700 dark:text-slate-100 dark:hover:text-teal-300" onClick={() => p.onProfile(message.userId)}>{message.userName || 'Learner'}</button>{message.isOwnMessage && <span className="rounded bg-teal-50 px-1.5 py-0.5 text-[10px] text-teal-700 dark:bg-teal-950 dark:text-teal-300">You</span>}<time dateTime={message.createdAt} className="text-slate-400">{p.timestamp(message.createdAt)}</time></div>;

  return <section className={`${socialPage} !space-y-6`} aria-label="Community discussions">
    <nav className="flex items-center justify-between gap-3"><Button variant="ghost" className="-ml-3 text-slate-500" onClick={p.onBack}><ArrowLeft size={16} />All communities</Button><span className="flex items-center gap-2 text-xs text-slate-500"><MessagesSquare size={15} />Study circle</span></nav>
    <header className="relative overflow-hidden rounded-[24px] bg-[#174b44] px-5 py-7 text-white sm:px-8">
      <div aria-hidden="true" className="pointer-events-none absolute -right-12 -top-24 h-80 w-80 rounded-full border-[45px] border-white/[0.04]" />
      <div className="relative flex flex-wrap items-start justify-between gap-6"><div className="min-w-0 max-w-2xl"><p className="mb-3 flex items-center gap-2 text-[10px] font-semibold uppercase tracking-[0.18em] text-[#d9e8bc]"><BookOpen size={14} />{room.topic || 'Learn together'}</p><h2 className="break-words text-3xl font-semibold tracking-tight sm:text-4xl">{room.name}</h2><p className="mt-3 max-w-xl text-sm leading-6 text-teal-50/75">{room.description}</p></div><Button className="bg-[#d9e8bc] text-[#174b44] hover:bg-[#e8f1d6]" onClick={room.isMember ? focusComposer : () => p.onJoin(room.id)}><Plus size={16} />{room.isMember ? 'Start a thread' : 'Join this circle'}</Button></div>
      <div className="relative mt-6 flex flex-wrap items-center gap-x-5 gap-y-3 border-t border-white/15 pt-4 text-xs text-teal-50/75"><span className="flex items-center gap-2"><Users size={14} />{room.memberCount} members</span><span className="flex items-center gap-2"><MessagesSquare size={14} />{threads.length} threads</span>{room.isMember && <span className="flex items-center gap-1.5 text-[#d9e8bc]"><Check size={14} />You’re a member</span>}{room.isAdmin && <button className="flex items-center gap-2 underline-offset-4 hover:underline sm:ml-auto" onClick={() => p.onInvite(room.id)}><Link size={14} />Copy invite link</button>}</div>
    </header>
    {p.message && <p role="status" className="rounded-xl border border-teal-200 bg-teal-50 p-4 text-sm text-teal-900 dark:border-teal-800 dark:bg-teal-950 dark:text-teal-100">{p.message}</p>}
    <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_270px]">
      <main className="min-w-0 space-y-5">
        {room.isMember ? <form onSubmit={event => submit(event)} className={`${surface} p-4 shadow-sm sm:p-5`}>
          <div className="mb-4 flex items-center gap-3"><Avatar name={user?.name} src={user?.profileImageUrl} /><div><h3 className="text-sm font-semibold">What are you working through?</h3><p className="mt-0.5 text-xs text-slate-500">A good question can help the whole circle.</p></div></div>
          <textarea ref={composer} className={`${field} min-h-[112px] resize-y !bg-transparent leading-7`} aria-label="New discussion thread" placeholder="Ask a question, explain a tricky concept, or share a study insight…" value={p.draft} disabled={pending.new} onChange={event => p.onDraft(event.target.value)} />
          {p.image && <div className="relative mt-3 w-fit max-w-full rounded-xl border border-slate-200 p-2 dark:border-slate-700"><img src={p.image.dataUrl} alt="Thread attachment preview" className="max-h-48 rounded-lg" /><Button type="button" variant="secondary" size="icon" className="absolute right-3 top-3 h-8 w-8" disabled={pending.new} onClick={p.onRemoveImage} aria-label="Remove attached image"><X size={15} /></Button><p className="mt-2 truncate text-xs text-slate-500">{p.image.name}</p></div>}
          <div className="mt-3 flex flex-wrap items-center justify-between gap-3"><label className="relative flex min-h-10 cursor-pointer items-center gap-2 rounded-lg px-2 text-xs font-medium text-slate-500 hover:bg-slate-50 focus-within:ring-2 focus-within:ring-teal-500 dark:hover:bg-slate-800"><ImagePlus size={17} />Attach image<input aria-label="Attach thread image" disabled={pending.new} type="file" accept="image/png,image/jpeg,image/webp,image/gif" onChange={p.onImage} className="absolute inset-0 w-full cursor-pointer opacity-0" /></label><div className="flex items-center gap-3"><span aria-live="polite" className={`text-[11px] ${words(p.draft) > p.limit ? 'text-red-600' : 'text-slate-400'}`}>{words(p.draft)}/{p.limit} words</span><Button type="submit" className={accent} disabled={pending.new || (!p.draft.trim() && !p.image) || words(p.draft) > p.limit}>{pending.new ? <Loader2 size={15} className="motion-safe:animate-spin" /> : <Send size={15} />}{pending.new ? 'Posting…' : 'Post thread'}</Button></div></div>
        </form> : <div className={`${surface} flex flex-wrap items-center justify-between gap-4 p-5`}><div><h3 className="text-sm font-semibold">There’s a place for your perspective.</h3><p className={muted}>Join the circle to ask questions and reply.</p></div><Button className={accent} onClick={() => p.onJoin(room.id)}>Join community<ArrowUpRight size={15} /></Button></div>}

        <div className={`${surface} overflow-hidden`}>
          <div className="border-b border-slate-100 p-4 dark:border-slate-800 sm:p-5"><div className="mb-4 flex items-center justify-between"><h3 className="text-lg font-semibold tracking-tight">The conversation</h3><span className="text-xs text-slate-400" role="status">{visible.length} {visible.length === 1 ? 'thread' : 'threads'}</span></div><SearchField value={query} onChange={setQuery} placeholder="Search discussions, replies, or people" /><div className="mt-4 flex flex-wrap items-center justify-between gap-3"><div className="flex flex-wrap gap-1" role="group" aria-label="Filter threads">{[['all', 'All threads', threads.length], ['unanswered', 'Unanswered', unanswered], ['mine', 'My threads', null]].map(([value, label, count]) => <button key={value} aria-pressed={filter === value} onClick={() => setFilter(value)} className={`min-h-9 rounded-lg px-3 text-xs font-medium transition-colors motion-reduce:transition-none ${filter === value ? 'bg-teal-50 text-teal-800 dark:bg-teal-950 dark:text-teal-200' : 'text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-800'}`}>{label}{count !== null && <span className="ml-1.5 opacity-60">{count}</span>}</button>)}</div><select aria-label="Sort threads" value={sort} onChange={event => setSort(event.target.value)} className="min-h-9 max-w-full rounded-lg border border-slate-200 bg-transparent px-2 text-xs text-slate-600 focus:ring-2 focus:ring-teal-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300"><option value="latest">Newest first</option><option value="active">Recent activity</option><option value="discussed">Most discussed</option></select></div></div>
          <div className="divide-y divide-slate-100 dark:divide-slate-800">
            {visible.map(message => {
              const responses = replies[message.id] || [];
              const expanded = Boolean(p.expanded[message.id]);
              const draft = p.replyDrafts[message.id] || '';
              return <article key={message.id} className={`p-4 sm:p-5 ${entry}`}>
                <div className="flex items-start gap-3"><Avatar name={message.userName} src={message.profileImageUrl} /><div className="min-w-0 flex-1"><div className="pt-1">{author(message)}</div><p className="mt-1 text-[10px] text-slate-400">{responses.length ? 'Discussion' : 'Start the conversation'}</p></div>{!responses.length && <span className="hidden rounded-full bg-amber-50 px-2 py-1 text-[10px] text-amber-800 dark:bg-amber-950/40 dark:text-amber-200 sm:block">Awaiting a reply</span>}</div>
                {message.text && <p className="mt-4 whitespace-pre-wrap break-words text-sm leading-7 text-slate-700 dark:text-slate-200">{message.text}</p>}
                {message.imageUrl && <a href={message.imageUrl} target="_blank" rel="noreferrer" className="mt-4 block w-fit max-w-full overflow-hidden rounded-xl border border-slate-100 dark:border-slate-800"><img loading="lazy" className="max-h-96 max-w-full object-contain" src={message.imageUrl} alt={`Image shared by ${message.userName}`} /></a>}
                <div className="mt-4 flex flex-wrap items-center gap-2"><Button variant="ghost" size="sm" className="text-teal-700 dark:text-teal-300" aria-expanded={expanded} aria-controls={`replies-${message.id}`} onClick={() => p.onToggle(message.id)}><MessageCircle size={15} />{responses.length ? `${responses.length} ${responses.length === 1 ? 'reply' : 'replies'}` : 'View discussion'}<ChevronDown size={13} className={`transition-transform motion-reduce:transition-none ${expanded ? 'rotate-180' : ''}`} /></Button>{room.isMember && <Button variant="ghost" size="sm" className="text-slate-500" onClick={() => { p.onToggle(message.id, true); requestAnimationFrame(() => replyInputs.current[message.id]?.focus()); }}>Reply<ArrowUpRight size={13} /></Button>}</div>
                {expanded && <div id={`replies-${message.id}`} className="mt-3 space-y-4 rounded-xl bg-slate-50 p-3 dark:bg-slate-950/50 sm:p-4 motion-safe:animate-in motion-safe:fade-in motion-safe:slide-in-from-top-1 motion-safe:duration-200">
                  {responses.map(reply => <div key={reply.id} className="flex gap-3"><Avatar name={reply.userName} src={reply.profileImageUrl} /><div className="min-w-0 flex-1">{author(reply)}<p className="mt-2 whitespace-pre-wrap break-words text-sm leading-6 text-slate-600 dark:text-slate-300">{reply.text}</p></div></div>)}
                  {!responses.length && <p className="text-xs leading-6 text-slate-500">No replies yet. Share your reasoning or ask a follow-up question.</p>}
                  {room.isMember ? <form onSubmit={event => submit(event, message.id)} className="space-y-2 border-t border-slate-200 pt-3 dark:border-slate-800"><textarea ref={node => { replyInputs.current[message.id] = node; }} className={`${field} resize-y`} rows={2} aria-label={`Reply to ${message.userName}`} placeholder="Add your explanation or a helpful reference…" value={draft} disabled={pending[message.id]} onChange={event => p.onReplyDraft(message.id, event.target.value)} /><div className="flex items-center justify-between gap-2"><span className={`text-[11px] ${words(draft) > p.limit ? 'text-red-600' : 'text-slate-400'}`}>{words(draft)}/{p.limit} words</span><Button type="submit" size="sm" className={accent} disabled={pending[message.id] || !draft.trim() || words(draft) > p.limit}>{pending[message.id] ? <Loader2 size={14} className="motion-safe:animate-spin" /> : <Send size={14} />}{pending[message.id] ? 'Sending…' : 'Send reply'}</Button></div></form> : <Button variant="outline" size="sm" onClick={() => p.onJoin(room.id)}>Join to reply</Button>}
                </div>}
              </article>;
            })}
            {!visible.length && <EmptyState icon={query ? Search : MessagesSquare} title={query ? 'No matching conversations' : filter === 'unanswered' ? 'Every thread has a reply' : filter === 'mine' ? 'Your first thread starts here' : 'Let’s get the conversation started'}><p>{query ? 'Try a different keyword or clear your filters.' : 'Ask something you’re studying or share an insight with your circle.'}</p><Button variant="ghost" className="mt-3 text-teal-700 dark:text-teal-300" onClick={() => { if (query || filter !== 'all') { setQuery(''); setFilter('all'); } else if (room.isMember) focusComposer(); else p.onJoin(room.id); }}>{query || filter !== 'all' ? 'Show all threads' : room.isMember ? 'Start a thread' : 'Join the circle'}<ArrowUpRight size={14} /></Button></EmptyState>}
          </div>
        </div>
      </main>
      <aside className="min-w-0 space-y-5 lg:sticky lg:top-6">
        <div className="rounded-2xl border border-[#dce6d4] bg-[#eef3e9] p-5 dark:border-teal-900 dark:bg-teal-950/30"><span className="mb-3 flex h-9 w-9 items-center justify-center rounded-xl bg-white/80 text-teal-800 dark:bg-teal-900 dark:text-teal-200"><MessageCircle size={18} /></span><h3 className="font-semibold text-teal-950 dark:text-teal-100">A little help goes a long way.</h3><p className="mt-2 text-xs leading-6 text-teal-800/75 dark:text-teal-200/70">{unanswered ? `${unanswered} ${unanswered === 1 ? 'thread is' : 'threads are'} waiting for a first reply. Your explanation could make something click.` : 'Share how you reached an answer. The reasoning is often the most useful part.'}</p>{unanswered > 0 && <Button variant="ghost" size="sm" className="-ml-2 mt-2 text-teal-800 dark:text-teal-200" onClick={() => { setQuery(''); setFilter('unanswered'); }}>Explore unanswered<ArrowUpRight size={14} /></Button>}</div>
        <section className={`${surface} p-5`}><div className="flex items-center justify-between"><h3 className="flex items-center gap-2 text-sm font-semibold"><Users size={16} />In this circle</h3><span className="text-xs text-slate-400">{room.memberCount}</span></div><div className="mt-4 max-h-80 space-y-4 overflow-y-auto">{room.members.map(member => <div key={member.id}><button className="flex w-full items-center gap-3 rounded-lg text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500" onClick={() => p.onProfile(member.id)}><Avatar name={member.name} src={member.profileImageUrl} /><span className="min-w-0"><strong className="block truncate text-xs font-semibold">{member.name}</strong><span className="mt-1 block truncate text-[10px] text-slate-400">{member.id === room.adminUserId ? 'Circle admin' : member.medicalCollege || 'Community member'}</span></span></button>{member.id !== user?.id && <div className="ml-[52px] mt-1 flex gap-3"><button className="min-h-7 text-[11px] text-teal-700 hover:underline dark:text-teal-300" onClick={() => p.onDirect(member.id)}>Message</button>{room.isAdmin && member.id !== room.adminUserId && <button className="min-h-7 text-[11px] text-slate-400 hover:text-red-600" onClick={() => p.onRemoveMember(room.id, member.id)}>Remove</button>}</div>}</div>)}</div></section>
        <section className="px-2"><h3 className="flex items-center gap-2 text-xs font-semibold text-slate-600 dark:text-slate-300"><ShieldCheck size={15} />Make this a helpful space</h3><ul className="mt-3 space-y-2 text-xs leading-6 text-slate-500 dark:text-slate-400"><li>Give your question a little context.</li><li>Explain your reasoning and cite sources.</li><li>Keep patient details anonymous.</li><li>Be kind. Everyone is learning.</li></ul></section>
      </aside>
    </div>
  </section>;
}
