import { useMemo, useRef, useState } from 'react';
import { ArrowDown, ArrowDownUp, ArrowRight, ArrowUpRight, BookOpen, Brain, Check, ChevronDown, ChevronRight, Compass, FlaskConical, HeartPulse, Loader2, MessageCircle, MessagesSquare, Plus, RefreshCw, Search, Stethoscope, Users } from 'lucide-react';
import { Avatar, EmptyState, SearchField, field, initials, number, socialPage } from './SocialUI';
import { Button } from './ui/button';
import { AddFriendDialog, FriendsPanel, useFriends } from './CommunityFriends';
import { Dialog, DialogContent, DialogDescription, DialogTitle, DialogTrigger } from './ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { DropdownMenu, DropdownMenuContent, DropdownMenuRadioGroup, DropdownMenuRadioItem, DropdownMenuTrigger } from './ui/dropdown-menu';

const palettes = [
  { cover: 'bg-[#e0eeea] text-[#406e63] dark:bg-[#193d38] dark:text-teal-200', icon: Stethoscope, badge: 'bg-teal-50 text-teal-800 dark:bg-teal-900/40 dark:text-teal-200' },
  { cover: 'bg-[#ebe6f3] text-[#80719e] dark:bg-[#352e48] dark:text-violet-200', icon: Brain, badge: 'bg-violet-50 text-violet-800 dark:bg-violet-900/40 dark:text-violet-200' },
  { cover: 'bg-[#f4ead4] text-[#9e8450] dark:bg-[#413820] dark:text-amber-200', icon: BookOpen, badge: 'bg-amber-50 text-amber-800 dark:bg-amber-900/40 dark:text-amber-200' },
  { cover: 'bg-[#f2e3df] text-[#a57669] dark:bg-[#442f30] dark:text-rose-200', icon: HeartPulse, badge: 'bg-rose-50 text-rose-800 dark:bg-rose-900/40 dark:text-rose-200' },
  { cover: 'bg-[#dfeaf3] text-[#597e9b] dark:bg-[#24374b] dark:text-sky-200', icon: FlaskConical, badge: 'bg-sky-50 text-sky-800 dark:bg-sky-900/40 dark:text-sky-200' },
];
const panel = 'min-w-0 rounded-2xl border border-slate-200/80 bg-white dark:border-slate-800 dark:bg-slate-900';
const secondaryText = 'text-sm leading-relaxed text-slate-500 dark:text-slate-400';
const sortLabels = { recent: 'Recent activity', members: 'Most members', name: 'Name A–Z' };
const latestActivity = room => Math.max(new Date(room.createdAt || 0).getTime() || 0, ...(room.messages || []).map(message => new Date(message.createdAt).getTime() || 0));

function roomPalette(room) {
  const topic = `${room.name} ${room.topic}`.toLowerCase();
  if (/clinical|surgery|medicine/.test(topic)) return palettes[0];
  if (/anatomy|neuro|psych/.test(topic)) return palettes[1];
  if (/neet|exam|revision|pg/.test(topic)) return palettes[2];
  if (/physio|cardio|final/.test(topic)) return palettes[3];
  return palettes[[...room.id].reduce((sum, char) => sum + char.charCodeAt(0), 0) % palettes.length];
}

function MemberStack({ members = [], count, dark = false }) {
  return <div className="flex items-center gap-2.5">
    <div className="flex -space-x-2" aria-hidden="true">
      {members.slice(0, 3).map((member) => <span key={member.id} className={`flex h-7 w-7 items-center justify-center overflow-hidden rounded-full border-2 text-[9px] font-bold ${dark ? 'border-[#174b44] bg-teal-100 text-teal-900' : 'border-white bg-slate-100 text-slate-600 dark:border-slate-900 dark:bg-slate-700 dark:text-slate-200'}`}>{member.profileImageUrl ? <img src={member.profileImageUrl} alt="" className="h-full w-full object-cover" /> : initials(member.name)}</span>)}
      {!members.length && <Users size={15} className={dark ? 'text-teal-200' : 'text-slate-400'} />}
    </div>
    <span className={`text-xs ${dark ? 'text-teal-100/80' : 'text-slate-500 dark:text-slate-400'}`}>{number(count)} members</span>
  </div>;
}

function CommunityIllustration() {
  return <div aria-hidden="true" className="relative mx-auto hidden h-[290px] w-[350px] shrink-0 lg:block">
    <div className="absolute inset-4 rounded-full border border-white/10" />
    <div className="absolute inset-12 rounded-full border border-dashed border-white/15" />
    <svg className="absolute inset-0 h-full w-full text-teal-200/30" viewBox="0 0 350 290" fill="none"><path d="M46 74C210 15 122 251 306 218M36 228C114 115 226 226 294 60" stroke="currentColor" strokeDasharray="4 6" /><circle cx="46" cy="74" r="5" fill="#d9e8bc" /><circle cx="306" cy="218" r="5" fill="#d9e8bc" /><circle cx="294" cy="60" r="4" fill="#b1d6ca" /></svg>
    <div className="absolute left-14 top-14 h-44 w-56 -rotate-[9deg] rounded-2xl border border-white/20 bg-[#82a99b] shadow-xl" />
    <div className="absolute left-16 top-12 w-56 rotate-[5deg] rounded-2xl bg-[#f8f5ec] p-5 text-[#214a42] shadow-2xl transition-transform duration-500 hover:rotate-0 motion-reduce:transition-none">
      <div className="flex items-center justify-between"><span className="text-[9px] font-bold uppercase tracking-[0.2em]">The study circle</span><BookOpen size={16} /></div>
      <div className="mt-5 text-[25px] font-semibold leading-[1.15] tracking-tight">Big questions.<br />Better answers.</div>
      <div className="mt-4 flex gap-1.5"><span className="h-1.5 w-16 rounded-full bg-[#d5ded3]" /><span className="h-1.5 w-9 rounded-full bg-[#d5ded3]" /></div>
      <div className="mt-5 flex items-center gap-2 border-t border-[#dfe3d7] pt-3 text-[10px] font-medium"><span className="flex h-5 w-5 items-center justify-center rounded-full bg-[#dce6c4]"><Check size={11} /></span>Made for learning together</div>
    </div>
    <div className="absolute -left-1 bottom-9 flex -rotate-[6deg] items-center gap-2 rounded-xl border border-white/20 bg-[#b6d4c7] px-4 py-3 text-[#214a42] shadow-lg"><MessageCircle size={17} /><span className="text-xs font-semibold">Ask. Discuss. Understand.</span></div>
    <span className="absolute right-3 top-6 flex h-12 w-12 rotate-12 items-center justify-center rounded-2xl border border-white/20 bg-[#d9e8bc] text-[#34564a] shadow-lg motion-safe:animate-[arena-float_7s_ease-in-out_infinite]"><Users size={23} /></span>
  </div>;
}

function RoomCard({ room, onOpen, onInvite }) {
  const palette = roomPalette(room);
  const Icon = palette.icon;
  return <article className={`${panel} group flex flex-col overflow-hidden transition duration-300 hover:border-slate-300 hover:shadow-[0_12px_28px_-12px_rgba(15,23,42,0.22)] dark:hover:border-slate-600 motion-safe:hover:-translate-y-1 motion-reduce:transition-none`}>
    <div className={`relative h-[112px] overflow-hidden ${palette.cover}`} aria-hidden="true">
      <div className="absolute -right-5 -top-14 h-52 w-52 rounded-full border-[22px] border-current opacity-[0.08]" />
      <div className="absolute -right-1 -top-10 h-44 w-44 rounded-full border border-current opacity-20" />
      <div className="absolute right-7 top-5 rotate-12 transition-transform duration-500 group-hover:rotate-0 motion-reduce:transition-none"><Icon size={76} strokeWidth={0.8} className="opacity-60" /></div>
      <div className="absolute left-5 top-5 flex items-center gap-1.5 text-[9px] font-bold uppercase tracking-[0.18em]"><span className="h-1 w-1 rounded-full bg-current" />Medulla circles</div>
      <span className="absolute bottom-4 left-5 max-w-[65%] truncate text-sm font-semibold tracking-tight">{room.topic || 'General discussion'}</span>
    </div>
    <div className="flex flex-1 flex-col p-5">
      <div className="mb-3 flex items-center justify-between gap-2"><span className={`rounded-md px-2 py-1 text-[10px] font-semibold ${palette.badge}`}>{room.isAdmin ? 'Your community' : room.isMember ? 'Your circle' : 'Open to everyone'}</span>{room.isMember && <span className="flex items-center gap-1 text-[10px] font-medium text-teal-700 dark:text-teal-300"><Check size={12} />Joined</span>}</div>
      <h4 className="text-lg font-semibold leading-snug tracking-tight"><button className="text-left transition-colors hover:text-teal-700 focus-visible:rounded focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 dark:hover:text-teal-300" onClick={() => onOpen(room.id)}>{room.name}</button></h4>
      <p className={`mb-5 mt-2 line-clamp-2 ${secondaryText}`}>{room.description}</p>
      <div className="mt-auto"><MemberStack members={room.members} count={room.memberCount} /><div className="mt-4 flex items-center justify-between gap-2 border-t border-slate-100 pt-3 dark:border-slate-800"><span className="flex items-center gap-1.5 text-xs text-slate-400"><MessageCircle size={13} />{number(room.messages?.length)} posts</span><div className="flex items-center gap-1">{room.isAdmin && <Button variant="ghost" size="sm" onClick={() => onInvite(room.id)}>Invite</Button>}<Button variant="ghost" size="sm" className="-mr-2 text-teal-800 hover:bg-teal-50 dark:text-teal-200 dark:hover:bg-teal-950" onClick={() => onOpen(room.id)}>{room.isMember ? 'Open room' : 'Explore room'}<ArrowUpRight size={15} className="transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5 motion-reduce:transform-none" /></Button></div></div></div>
    </div>
  </article>;
}

export default function CommunityHub(p) {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('all');
  const [sort, setSort] = useState('recent');
  const [creating, setCreating] = useState(false);
  const [createOpen, setCreateOpen] = useState(false);
  const [addFriendOpen, setAddFriendOpen] = useState(false);
  const friendsModel = useFriends();
  const directory = useRef(null);
  const inboxSearch = useRef(null);
  const joined = p.communities.filter(room => room.isMember);
  const rooms = useMemo(() => p.communities.filter(room => (filter === 'all' || room.isMember) && `${room.name} ${room.topic} ${room.description}`.toLowerCase().includes(query.trim().toLowerCase())).sort((a, b) => sort === 'members' ? b.memberCount - a.memberCount : sort === 'name' ? a.name.localeCompare(b.name) : latestActivity(b) - latestActivity(a)), [p.communities, filter, query, sort]);
  const discussions = useMemo(() => p.communities.flatMap(room => (room.messages || []).filter(message => !message.parentMessageId).map(message => ({ ...message, room }))).sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt)).slice(0, 3), [p.communities]);
  const resumeRoom = [...joined].sort((a, b) => latestActivity(b) - latestActivity(a))[0];
  const totalPosts = p.communities.reduce((sum, room) => sum + (room.messages?.length || 0), 0);
  const submit = async event => { event.preventDefault(); if (creating) return; setCreating(true); try { await p.onCreate(event); } finally { setCreating(false); } };
  const explore = () => { setFilter('all'); directory.current?.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start' }); };

  return <section className={`${socialPage} !space-y-8`} aria-label="Communities">
    <div className="flex items-center justify-between gap-3"><div className="flex items-center gap-2 text-sm"><span className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-100 text-teal-800 dark:bg-teal-900/50 dark:text-teal-200"><MessagesSquare size={17} /></span><span className="font-semibold">Community</span><span className="hidden text-slate-300 sm:inline">/</span><span className="hidden text-slate-500 dark:text-slate-400 sm:inline">Your space to connect</span></div>
      <Dialog open={createOpen} onOpenChange={setCreateOpen}>
        <DialogTrigger asChild><Button variant="outline"><Plus size={16} />Create a room</Button></DialogTrigger>
        <DialogContent onInteractOutside={event => { if (creating) event.preventDefault(); }}>
          <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-teal-50 text-teal-800 dark:bg-teal-950 dark:text-teal-200"><Users size={23} /></div>
          <DialogTitle>Start something good.</DialogTitle>
          <DialogDescription>A study group, a shared goal, a space for questions. Make it yours.</DialogDescription>
          <form className="mt-6 space-y-4" onSubmit={submit}>
            {[['name', 'Room name', 'e.g. Final Year Surgery'], ['topic', 'Topic', 'e.g. Clinical case discussions'], ['description', 'Description', 'What will you study together?']].map(([key, label, placeholder]) => <label key={key} className="block space-y-2 text-xs font-semibold"><span>{label}</span>{key === 'description' ? <textarea required rows={3} className={`${field} resize-y`} value={p.form[key]} onChange={e => p.onField(key, e.target.value)} placeholder={placeholder} /> : <input required className={field} value={p.form[key]} onChange={e => p.onField(key, e.target.value)} placeholder={placeholder} />}</label>)}
            {p.message && <p role="status" className="rounded-lg bg-slate-100 p-3 text-sm dark:bg-slate-800">{p.message}</p>}
            <div className="flex items-center gap-2 rounded-xl bg-teal-50 px-3 py-3 text-xs text-teal-800 dark:bg-teal-950 dark:text-teal-200"><Check size={15} />You’ll be the admin. Invite your peers after creating.</div>
            <Button className="w-full" disabled={creating || !p.form.name.trim() || !p.form.topic.trim() || !p.form.description.trim()} type="submit">{creating ? <Loader2 size={16} className="motion-safe:animate-spin" /> : <Plus size={16} />}{creating ? 'Creating room…' : 'Create room'}</Button>
          </form>
        </DialogContent>
      </Dialog>
    </div>

    <header className="relative isolate overflow-hidden rounded-[28px] bg-[#174b44] text-white shadow-[0_12px_35px_-20px_rgba(23,75,68,0.45)] dark:bg-[#123d38]">
      <div className="pointer-events-none absolute -right-24 -top-40 h-[580px] w-[580px] rounded-full border-[70px] border-white/[0.025]" aria-hidden="true" />
      <div className="relative flex items-center justify-between gap-4 px-6 py-9 sm:px-9 lg:py-6">
        <div className="max-w-lg"><p className="mb-5 flex items-center gap-2 text-[10px] font-semibold uppercase tracking-[0.22em] text-[#c4dcae]"><span className="h-px w-6 bg-[#c4dcae]" />The Medulla community</p><h2 className="text-[36px] font-semibold leading-[1.08] tracking-[-0.045em] sm:text-5xl">Good company.<br /><span className="font-serif italic text-[#d9e8bc]">Better learning.</span></h2><p className="mt-5 max-w-sm text-sm leading-7 text-teal-50/75">Find your people. Talk through the tough questions. Turn a solo study session into a shared breakthrough.</p><div className="mt-6 flex flex-wrap items-center gap-4"><Button className="bg-[#d9e8bc] text-[#22483b] hover:bg-[#e8f1d6] dark:bg-[#d9e8bc] dark:text-[#22483b]" onClick={explore}>Find your circle<ArrowDown size={15} /></Button><span className="text-xs text-teal-100/65">A space for every stage of your journey.</span></div></div>
        <CommunityIllustration />
      </div>
      <div className="relative flex flex-wrap items-center justify-between gap-4 border-t border-white/10 bg-black/10 px-6 py-4 sm:px-9"><div className="flex flex-wrap gap-x-6 gap-y-2 text-xs text-teal-100/65"><span><strong className="mr-1.5 text-sm font-semibold text-white">{number(p.communities.length)}</strong> study rooms</span><span><strong className="mr-1.5 text-sm font-semibold text-white">{number(totalPosts)}</strong> shared posts</span><span><strong className="mr-1.5 text-sm font-semibold text-white">{joined.length}</strong> circles joined</span></div><span className="hidden items-center gap-2 text-[10px] font-medium uppercase tracking-widest text-[#c4dcae] sm:flex"><BookOpen size={13} />Built around learning</span></div>
    </header>

    {(p.message || p.directMessage) && !createOpen && <div role="status" className="rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm text-teal-900 dark:border-teal-900 dark:bg-teal-950 dark:text-teal-100">{p.message && <p>{p.message}</p>}{p.directMessage && <p>{p.directMessage}</p>}</div>}

    <div className="grid items-start gap-7 xl:grid-cols-[minmax(0,1fr)_300px]">
      <div ref={directory} className="min-w-0 scroll-mt-24">
        <div className="mb-4 flex items-center justify-between gap-3"><div><p className="mb-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-teal-700 dark:text-teal-300">A little curiosity goes a long way</p><h3 className="text-2xl font-semibold tracking-tight">Discover your next circle</h3></div><Button variant="ghost" size="icon" aria-label="Refresh study rooms" onClick={() => p.onRefresh()} disabled={p.busy}><RefreshCw size={16} className={p.busy ? 'motion-safe:animate-spin' : ''} /></Button></div>
        <Tabs value={filter} onValueChange={setFilter}>
          <div className="flex items-center gap-3 overflow-x-auto border-b border-slate-200 dark:border-slate-800">
            <TabsList aria-label="Community sections" className="shrink-0 gap-3 border-0 sm:gap-5">
              <TabsTrigger value="all"><Compass size={15} />Explore<span className="rounded-md bg-slate-200/60 px-1.5 py-0.5 text-[10px] dark:bg-slate-800">{p.communities.length}</span></TabsTrigger>
              <TabsTrigger value="joined"><Users size={15} />My rooms<span className="rounded-md bg-slate-200/60 px-1.5 py-0.5 text-[10px] dark:bg-slate-800">{joined.length}</span></TabsTrigger>
              <TabsTrigger value="friends"><Users size={15} />Friends{friendsModel.friends.length > 0 && <span className="rounded-md bg-slate-200/60 px-1.5 py-0.5 text-[10px] dark:bg-slate-800">{friendsModel.friends.length}</span>}</TabsTrigger>
            </TabsList>
            <AddFriendDialog model={friendsModel} open={addFriendOpen} onOpenChange={setAddFriendOpen} />
          </div>
          {filter !== 'friends' && <div className="mt-5 flex flex-wrap items-center gap-2"><div className="min-w-0 flex-1 basis-48"><SearchField value={query} onChange={setQuery} placeholder="Search rooms, subjects, or topics" /></div>
            <DropdownMenu><DropdownMenuTrigger asChild><Button variant="ghost" size="sm" aria-label="Sort study rooms"><ArrowDownUp size={13} />{sortLabels[sort]}<ChevronDown size={13} /></Button></DropdownMenuTrigger><DropdownMenuContent align="end"><DropdownMenuRadioGroup value={sort} onValueChange={setSort}>{Object.entries(sortLabels).map(([value, label]) => <DropdownMenuRadioItem key={value} value={value}>{label}</DropdownMenuRadioItem>)}</DropdownMenuRadioGroup></DropdownMenuContent></DropdownMenu>
          </div>}
          <TabsContent value="friends"><FriendsPanel model={friendsModel} onAdd={() => setAddFriendOpen(true)} onMessage={p.onDirect} /></TabsContent>
          {['all', 'joined'].map(tab => <TabsContent value={tab} key={tab}>
            {p.busy && !p.communities.length ? <div role="status" className="grid grid-cols-1 gap-4 sm:grid-cols-2"><span className="sr-only">Loading study rooms</span>{[0, 1].map(item => <div key={item} className={`${panel} overflow-hidden`}><div className="h-28 bg-slate-200 dark:bg-slate-800 motion-safe:animate-pulse" /><div className="space-y-4 p-5"><div className="h-4 w-3/4 rounded bg-slate-100 dark:bg-slate-800" /><div className="h-16 rounded bg-slate-100 dark:bg-slate-800" /></div></div>)}</div> : rooms.length ? <div className="grid gap-5 sm:grid-cols-2">{rooms.map(room => <RoomCard key={room.id} room={room} onOpen={p.onOpen} onInvite={p.onInvite} />)}</div> : <div className={`${panel} border-dashed`}><EmptyState icon={query ? Search : Compass} title={query ? 'No matching rooms' : filter === 'joined' ? 'Your circle starts here' : 'Every great circle starts with someone.'}>{query ? 'Try a subject or a shorter search.' : filter === 'joined' ? 'Explore the rooms and join a discussion that interests you.' : 'Be the first to bring your study group together.'}<Button variant="ghost" className="mt-4" onClick={() => { if (query || filter === 'joined') { setQuery(''); setFilter('all'); } else setCreateOpen(true); }}>{query ? 'Clear search' : filter === 'joined' ? 'Explore rooms' : 'Create a room'}<ArrowRight size={14} /></Button></EmptyState></div>}
          </TabsContent>)}
        </Tabs>
        {filter !== 'friends' && <p role="status" className="mt-4 text-xs text-slate-400">{rooms.length} {rooms.length === 1 ? 'circle' : 'circles'}{query ? ` matching “${query}”` : filter === 'joined' ? ' you belong to' : ' to discover'}</p>}
        <button onClick={() => setCreateOpen(true)} className="mt-6 flex w-full items-center gap-4 rounded-2xl border border-dashed border-teal-800/20 bg-[#eef3e9] p-5 text-left transition hover:border-teal-700/50 hover:bg-[#e7efdf] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 dark:border-teal-600/30 dark:bg-teal-950/30 dark:hover:bg-teal-950/60 motion-reduce:transition-none"><span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-white/80 text-teal-800 dark:bg-teal-900 dark:text-teal-200"><Plus size={22} strokeWidth={1.5} /></span><span className="min-w-0 flex-1"><strong className="block text-sm font-semibold text-teal-950 dark:text-teal-100">Can’t find your people? Bring them together.</strong><span className="mt-1 block text-xs leading-relaxed text-teal-800/70 dark:text-teal-200/60">Start a room for your subject, exam, or study group.</span></span><ArrowUpRight size={20} className="shrink-0 text-teal-700 dark:text-teal-300" /></button>
      </div>

      <aside className="min-w-0 space-y-5">
        {resumeRoom && <button onClick={() => p.onOpen(resumeRoom.id)} className="group w-full rounded-2xl border border-teal-200/60 bg-[#e5eee9] p-5 text-left transition hover:border-teal-500 dark:border-teal-800 dark:bg-[#16332d] motion-reduce:transition-none"><span className="flex items-center gap-2 text-[10px] font-semibold uppercase tracking-[0.15em] text-teal-700 dark:text-teal-300"><span className="flex h-5 w-5 items-center justify-center rounded-full bg-white/70 dark:bg-teal-800"><ArrowRight size={11} /></span>Back to your circle</span><span className="mt-3 flex items-center justify-between gap-3"><strong className="text-base font-semibold leading-snug text-teal-950 dark:text-teal-100">{resumeRoom.name}</strong><ArrowUpRight size={19} className="shrink-0 text-teal-700 transition-transform group-hover:-translate-y-0.5 dark:text-teal-300" /></span><span className="mt-3 block text-xs text-teal-700/80 dark:text-teal-200/70">Pick up the conversation<ChevronRight size={12} className="ml-1 inline" /></span></button>}
        <article className={`${panel} overflow-hidden`}><div className="flex items-center justify-between border-b border-slate-100 px-5 py-4 dark:border-slate-800"><h3 className="flex items-center gap-2 text-sm font-semibold"><MessageCircle size={16} className="text-teal-700 dark:text-teal-300" />Personal inbox</h3><Button variant="ghost" size="icon" className="-mr-2 h-8 w-8" aria-label="Find a study partner" onClick={() => inboxSearch.current?.querySelector('input')?.focus()}><Plus size={16} /></Button></div><div className="px-4 pb-3 pt-4"><div ref={inboxSearch}><SearchField value={p.search} onChange={p.onSearch} placeholder="Find a study partner" /></div>
          {p.searchBusy ? <p role="status" className="px-1 py-3 text-xs text-slate-500">Searching learners…</p> : p.search.trim().length === 1 ? <p className="px-1 py-3 text-xs text-slate-500">Type at least 2 characters to search.</p> : p.search.trim().length >= 2 && !p.results.length ? <p role="status" className="px-1 py-3 text-xs text-slate-500">No learners found. Try another name.</p> : null}
          {p.results.length > 0 && <div className="mt-2 max-h-64 space-y-1 overflow-y-auto border-b border-slate-100 pb-3 dark:border-slate-800">{p.results.map(person => <button key={person.id} className="flex w-full items-center gap-3 rounded-xl p-2 text-left hover:bg-slate-50 dark:hover:bg-slate-800" onClick={() => p.onDirect(person.id)}><Avatar name={person.name} src={person.profileImageUrl} /><span className="min-w-0 flex-1"><strong className="block truncate text-sm">{person.name}</strong><span className="block truncate text-xs text-slate-500">{person.medicalCollege}</span></span><Plus size={15} className="shrink-0 text-teal-600" /></button>)}</div>}
          <div className="mt-2 max-h-80 overflow-y-auto">{p.directBusy ? <p role="status" className="py-4 text-sm text-slate-500">Loading messages…</p> : p.conversations.length ? p.conversations.map(conversation => { const person = conversation.otherParticipant; const latest = conversation.messages.at(-1); return <button key={conversation.id} className="group flex w-full items-center gap-3 rounded-xl px-1 py-3 text-left hover:bg-slate-50 dark:hover:bg-slate-800" onClick={() => p.onConversation(conversation.id)}><Avatar name={person?.name} src={person?.profileImageUrl} /><span className="min-w-0 flex-1"><strong className="block truncate text-sm font-semibold">{person?.name || 'Private chat'}</strong><span className="mt-1 block truncate text-xs text-slate-500 dark:text-slate-400">{latest?.text || 'Start the conversation'}</span><time className="mt-1 block text-[10px] text-slate-400">{p.timestamp(latest?.createdAt)}</time></span><ChevronRight size={14} className="shrink-0 text-slate-300 group-hover:text-teal-600" /></button>; }) : <div className="px-2 py-6 text-center"><MessagesSquare size={25} strokeWidth={1.3} className="mx-auto mb-3 text-slate-300" /><p className="text-xs leading-6 text-slate-500 dark:text-slate-400">Great study partnerships start<br />with a simple hello.</p></div>}</div>
        </div></article>
        <article className={`${panel} p-5`}><h3 className="mb-1 flex items-center gap-2 text-sm font-semibold"><MessagesSquare size={16} className="text-teal-700 dark:text-teal-300" />Around the community</h3><p className="mb-5 text-xs text-slate-400">The latest thoughts and questions.</p>
          {discussions.length ? <div className="space-y-5">{discussions.map((message, index) => <button key={`${message.room.id}-${message.id}`} onClick={() => p.onOpen(message.room.id)} className="group relative block w-full pl-5 text-left"><span className={`absolute left-0 top-1.5 h-1.5 w-1.5 rounded-full ${index === 0 ? 'bg-teal-600' : 'bg-slate-300 dark:bg-slate-600'}`} />{index !== discussions.length - 1 && <span className="absolute -bottom-5 left-[2.5px] top-5 w-px bg-slate-100 dark:bg-slate-800" />}<span className="block truncate text-[10px] font-semibold uppercase tracking-wide text-teal-700 dark:text-teal-300">{message.room.name}</span><span className="mt-2 line-clamp-2 text-sm leading-6 text-slate-700 group-hover:text-teal-800 dark:text-slate-200 dark:group-hover:text-teal-200">{message.text || (message.imageUrl ? 'Shared an image with the circle.' : 'Started a discussion.')}</span><span className="mt-2 block text-[10px] text-slate-400">{message.userName} · {p.timestamp(message.createdAt)}</span></button>)}</div> : <div className="rounded-xl bg-slate-50 p-4 text-xs leading-6 text-slate-500 dark:bg-slate-950/50 dark:text-slate-400">Something on your mind? Open a room and start the first discussion.</div>}
        </article>
        <div className="px-3 py-2"><p className="font-serif text-xl italic leading-relaxed text-slate-500 dark:text-slate-400">A little help today.<br />A better doctor tomorrow.</p><p className="mt-3 text-[9px] font-semibold uppercase tracking-[0.18em] text-slate-400">Learn generously. Grow together.</p></div>
      </aside>
    </div>
  </section>;
}
