import { useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft, ArrowUpRight, BarChart2, Bookmark, Check, ChevronDown, ChevronRight,
  Crown, Heart, ImagePlus, Link2, Loader2, MessageCircle, MessagesSquare,
  MoreHorizontal, Plus, Repeat, Search, Send, Share, Shield, Sparkles, UserCheck, Users, X
} from 'lucide-react';
import { Button } from './ui/button';

const words = text => text.trim().split(/\s+/).filter(Boolean).length;

export default function CommunityThreads(p) {
  const { room, user } = p;
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('all'); // 'all' | 'unanswered' | 'mine'
  const [pending, setPending] = useState({});
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [memberSearch, setMemberSearch] = useState('');
  const [copiedLink, setCopiedLink] = useState(false);
  const [activeShareId, setActiveShareId] = useState(null);
  const [likedThreads, setLikedThreads] = useState({});

  const locks = useRef(new Set());
  const composer = useRef(null);
  const replyInputs = useRef({});

  // Ensure window scrolls smoothly to top on entering community
  useEffect(() => {
    window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
    document.getElementById('main-content')?.scrollTo?.({ top: 0, left: 0, behavior: 'instant' });
  }, [room?.id]);

  // Group threads and replies
  const { threads, replies } = useMemo(() => {
    const ids = new Set((room.messages || []).map(m => m.id));
    const repliesMap = {};
    (room.messages || []).forEach(m => {
      if (m.parentMessageId) {
        (repliesMap[m.parentMessageId] ||= []).push(m);
      }
    });
    Object.values(repliesMap).forEach(items =>
      items.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt))
    );
    return {
      threads: (room.messages || []).filter(
        m => !m.parentMessageId || !ids.has(m.parentMessageId)
      ),
      replies: repliesMap
    };
  }, [room.messages]);

  const unansweredCount = threads.filter(m => !replies[m.id]?.length).length;

  const visible = useMemo(() => {
    return threads.filter(message => {
      const responses = replies[message.id] || [];
      const matches = `${message.text || ''} ${message.userName || ''} ${responses.map(r => `${r.text} ${r.userName}`).join(' ')}`.toLowerCase().includes(query.trim().toLowerCase());
      return matches &&
        (filter !== 'unanswered' || !responses.length) &&
        (filter !== 'mine' || message.isOwnMessage || message.userId === user?.id);
    }).sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  }, [threads, replies, query, filter, user?.id]);

  const adminMember = useMemo(() => {
    return (room.members || []).find(m => m.id === room.adminUserId) || null;
  }, [room.members, room.adminUserId]);

  const filteredMembers = useMemo(() => {
    if (!memberSearch.trim()) return room.members || [];
    const q = memberSearch.toLowerCase();
    return (room.members || []).filter(m =>
      (m.name || '').toLowerCase().includes(q) ||
      (m.medicalCollege || '').toLowerCase().includes(q)
    );
  }, [room.members, memberSearch]);

  const submit = async (event, id = null) => {
    event.preventDefault();
    const key = id || 'new';
    if (locks.current.has(key)) return;
    locks.current.add(key);
    setPending(current => ({ ...current, [key]: true }));
    try {
      await p.onSend(event, id);
    } finally {
      locks.current.delete(key);
      setPending(current => ({ ...current, [key]: false }));
    }
  };

  const focusComposer = () => {
    composer.current?.focus();
    composer.current?.scrollIntoView({
      block: 'center',
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'
    });
  };

  const handleCopyInvite = async () => {
    p.onInvite(room.id);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2000);
  };

  const handleShareThread = async (messageId) => {
    const threadUrl = `${window.location.origin}?community=${encodeURIComponent(room.id)}&thread=${encodeURIComponent(messageId)}`;
    try {
      await navigator.clipboard.writeText(threadUrl);
      setActiveShareId(messageId);
      setTimeout(() => setActiveShareId(null), 2000);
    } catch {
      // fallback
    }
  };

  const toggleLike = (threadId) => {
    setLikedThreads(prev => ({ ...prev, [threadId]: !prev[threadId] }));
  };

  const wordCount = words(p.draft || '');
  const isOverLimit = wordCount > p.limit;

  // Initial avatar letter fallback
  const renderAvatarCircle = (name, src, size = 'w-10 h-10') => (
    <div className={`${size} shrink-0 rounded-full overflow-hidden bg-slate-200 dark:bg-neutral-800 flex items-center justify-center font-bold text-slate-700 dark:text-neutral-200 text-sm select-none`}>
      {src ? (
        <img src={src} alt={name || 'Learner'} className="w-full h-full object-cover" />
      ) : (
        (name || 'L').charAt(0).toUpperCase()
      )}
    </div>
  );

  const conversations = p.conversations || [];
  const communities = p.communities || [];
  const otherCommunities = communities.filter(c => c.id !== room?.id).slice(0, 4);

  return (
    <div className="community-threads-view flex w-full h-[calc(100vh-72px)] max-h-[calc(100vh-72px)] overflow-hidden bg-white dark:bg-black text-slate-900 dark:text-neutral-100 transition-colors">
      {/* =========================================================================
          LEFT PITCH DARK TWITTER TIMELINE (FAR LEFT TILL SLIDING BAR)
          ========================================================================= */}
      <div className="w-full lg:w-[600px] xl:w-[650px] shrink-0 h-full max-h-full bg-white dark:bg-black border-r border-slate-200 dark:border-neutral-800 flex flex-col overflow-hidden">
        
        {/* CLEAN TOP COMMUNITY HEADER - FIXED / STATIONARY */}
        <header className="shrink-0 relative bg-white/95 dark:bg-black/95 border-b border-slate-200 dark:border-neutral-800 transition-colors z-10">
          <div className="flex items-center justify-between px-4 py-2 gap-3 min-h-[53px]">
            {/* Back button */}
            <button
              type="button"
              onClick={p.onBack}
              className="p-2 -ml-2 rounded-full hover:bg-slate-100 dark:hover:bg-neutral-900 text-slate-700 dark:text-neutral-300 transition"
              aria-label="Back to communities"
              title="Back"
            >
              <ArrowLeft size={19} />
            </button>

            {/* Clickable Community Name & Subtitle */}
            <button
              type="button"
              onClick={() => setIsDetailsOpen(true)}
              className="flex-1 min-w-0 text-left px-1.5 py-0.5 rounded-lg hover:bg-slate-100/60 dark:hover:bg-neutral-900/60 transition group"
              title="Click for circle details, members, and admin"
            >
              <div className="flex items-center gap-1.5">
                <h1 className="text-base sm:text-[17px] font-bold tracking-tight text-slate-900 dark:text-white truncate">
                  {room.name}
                </h1>
                <ChevronDown size={14} className="text-slate-400 group-hover:text-slate-600 dark:group-hover:text-neutral-200 transition-transform group-hover:translate-y-0.5 shrink-0" />
              </div>
              <p className="text-[12px] text-slate-500 dark:text-neutral-400 truncate">
                <span>{room.memberCount || (room.members || []).length} members</span>
                <span className="mx-1">·</span>
                <span className="text-sky-600 dark:text-sky-400 font-medium">{room.topic || 'Medical discussion'}</span>
                <span className="hidden sm:inline text-slate-400"> · tap for info</span>
              </p>
            </button>

            {/* Right Header Actions */}
            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={() => setIsDetailsOpen(true)}
                className="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-neutral-900 text-slate-600 dark:text-neutral-300 transition"
                title="View members"
              >
                <Users size={18} />
              </button>

              {room.isMember ? (
                <button
                  type="button"
                  onClick={handleCopyInvite}
                  className="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-neutral-900 text-slate-600 dark:text-neutral-300 transition"
                  title="Copy invite link"
                >
                  {copiedLink ? <Check size={18} className="text-emerald-500" /> : <Link2 size={18} />}
                </button>
              ) : (
                <Button
                  size="sm"
                  className="rounded-full bg-slate-900 text-white dark:bg-white dark:text-black hover:bg-slate-800 dark:hover:bg-neutral-200 font-bold px-4 py-1 text-xs"
                  onClick={() => p.onJoin(room.id)}
                >
                  Join
                </Button>
              )}
            </div>
          </div>

          {/* TWITTER-STYLE TABS ("For you" / "Following" style) */}
          <div className="flex border-t border-slate-200 dark:border-neutral-800 text-[15px]" role="tablist">
            {[
              { id: 'all', label: 'All threads' },
              { id: 'unanswered', label: 'Unanswered', count: unansweredCount },
              { id: 'mine', label: 'My threads' }
            ].map(tab => {
              const active = filter === tab.id;
              return (
                <button
                  key={tab.id}
                  type="button"
                  role="tab"
                  aria-selected={active}
                  onClick={() => setFilter(tab.id)}
                  className="flex-1 py-3 px-2 flex justify-center items-center hover:bg-slate-100/60 dark:hover:bg-neutral-900/60 transition relative"
                >
                  <span className={`transition ${
                    active
                      ? 'font-bold text-slate-900 dark:text-white'
                      : 'font-medium text-slate-500 dark:text-neutral-500'
                  }`}>
                    {tab.label}
                    {tab.count !== undefined && tab.count > 0 && (
                      <span className="ml-1.5 text-xs opacity-75 font-normal">({tab.count})</span>
                    )}
                  </span>
                  {active && (
                    <div className="absolute bottom-0 h-[3.5px] w-12 sm:w-16 bg-sky-500 rounded-full" />
                  )}
                </button>
              );
            })}
          </div>
        </header>

        {/* =========================================================================
            FEED SECTION WITH DEDICATED SCROLLBAR (WINDOW DOES NOT MOVE)
            ========================================================================= */}
        <div className="flex-1 min-h-0 overflow-y-auto overscroll-contain pb-20 sm:pb-16 community-feed-scroll">
          {/* NOTIFICATION MESSAGE */}
          {p.message && (
            <div className="border-b border-sky-500/20 bg-sky-50 dark:bg-sky-950/40 px-4 py-2 text-xs text-sky-800 dark:text-sky-200">
              {p.message}
            </div>
          )}

          {/* TWEET COMPOSER (Twitter "What is happening?!") */}
        {room.isMember ? (
          <form onSubmit={event => submit(event)} className="border-b border-slate-200 dark:border-neutral-800 px-4 py-3 bg-white dark:bg-black">
            <div className="flex gap-3">
              {renderAvatarCircle(user?.name, user?.profileImageUrl)}
              <div className="flex-1 min-w-0 pt-1">
                <textarea
                  ref={composer}
                  value={p.draft}
                  disabled={pending.new}
                  onChange={event => p.onDraft(event.target.value)}
                  placeholder="What's happening in your prep? Share a doubt or insight…"
                  aria-label="What's happening"
                  rows={2}
                  className="w-full bg-transparent text-[16px] sm:text-[17px] leading-relaxed text-slate-900 dark:text-neutral-100 placeholder:text-slate-500 dark:placeholder:text-neutral-500 focus:outline-none resize-none"
                />

                {/* Attached image preview */}
                {p.image && (
                  <div className="relative mt-2 rounded-2xl border border-slate-200 dark:border-neutral-800 overflow-hidden bg-slate-50 dark:bg-neutral-900 max-h-72">
                    <img src={p.image.dataUrl} alt="Attached preview" className="w-full max-h-72 object-cover" />
                    <button
                      type="button"
                      onClick={p.onRemoveImage}
                      disabled={pending.new}
                      className="absolute top-2.5 right-2.5 h-7 w-7 rounded-full bg-black/70 hover:bg-black text-white flex items-center justify-center transition"
                      aria-label="Remove image"
                    >
                      <X size={15} />
                    </button>
                  </div>
                )}

                {/* Composer bottom toolbar */}
                <div className="flex items-center justify-between border-t border-slate-100 dark:border-neutral-900 mt-3 pt-2.5">
                  <div className="flex items-center gap-1 -ml-1 text-sky-500 dark:text-sky-400">
                    <label className="p-2 rounded-full hover:bg-sky-50 dark:hover:bg-sky-950/40 cursor-pointer transition">
                      <ImagePlus size={18} />
                      <input
                        type="file"
                        accept="image/*"
                        disabled={pending.new}
                        onChange={p.onImage}
                        className="sr-only"
                      />
                    </label>
                  </div>

                  <div className="flex items-center gap-3">
                    <span className={`text-[12px] font-mono ${isOverLimit ? 'text-red-500' : 'text-slate-400 dark:text-neutral-500'}`}>
                      {wordCount}/{p.limit}
                    </span>
                    <Button
                      type="submit"
                      disabled={pending.new || (!p.draft.trim() && !p.image) || isOverLimit}
                      className="rounded-full bg-sky-500 hover:bg-sky-600 text-white font-bold px-4 py-1.5 text-[14px] shadow-sm disabled:opacity-50 transition active:scale-95"
                    >
                      {pending.new ? <Loader2 size={14} className="animate-spin" /> : 'Post'}
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </form>
        ) : (
          <div className="border-b border-slate-200 dark:border-neutral-800 p-4 bg-slate-50/50 dark:bg-neutral-900/30 flex items-center justify-between gap-3">
            <div>
              <p className="font-bold text-sm text-slate-900 dark:text-white">Join {room.name}</p>
              <p className="text-xs text-slate-500 dark:text-neutral-400">Join to participate in medical discussions and share study pearls.</p>
            </div>
            <Button
              className="rounded-full bg-sky-500 hover:bg-sky-600 text-white font-bold text-xs px-4"
              onClick={() => p.onJoin(room.id)}
            >
              Join circle
            </Button>
          </div>
        )}

        {/* OPTIONAL SEARCH BAR (COLLAPSIBLE / MINIMAL) */}
        <div className="border-b border-slate-200 dark:border-neutral-800 px-4 py-2 bg-slate-50/40 dark:bg-neutral-950/40 flex items-center gap-2">
          <Search size={15} className="text-slate-400 dark:text-neutral-500 shrink-0" />
          <input
            type="search"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search discussions…"
            aria-label="Search discussions"
            className="w-full bg-transparent text-xs text-slate-900 dark:text-neutral-100 placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-none"
          />
          {query && (
            <button type="button" onClick={() => setQuery('')} className="text-slate-400 hover:text-slate-600 dark:hover:text-white">
              <X size={14} />
            </button>
          )}
        </div>

        {/* =========================================================================
            THE FEED: CONTINUOUS DIVIDE-Y TIMELINE (EXACT TWITTER POST LAYOUT)
            NO CURVED BOXES, NO FLOATING RECTANGLES!
            ========================================================================= */}
        <div className="divide-y divide-slate-200 dark:divide-neutral-800">
          {visible.map(message => {
            const responses = replies[message.id] || [];
            const expanded = Boolean(p.expanded[message.id]);
            const replyDraft = p.replyDrafts[message.id] || '';
            const isLiked = Boolean(likedThreads[message.id]);

            return (
              <article
                key={message.id}
                className="px-4 py-3.5 hover:bg-slate-50/70 dark:hover:bg-neutral-900/30 transition cursor-pointer"
                onClick={() => p.onToggle(message.id)}
              >
                <div className="flex gap-3">
                  {/* Avatar (Left) */}
                  <div className="flex flex-col items-center shrink-0">
                    <button
                      type="button"
                      disabled={!message.userId}
                      onClick={e => {
                        e.stopPropagation();
                        p.onProfile(message.userId);
                      }}
                      className="rounded-full hover:opacity-90 transition"
                    >
                      {renderAvatarCircle(message.userName, message.profileImageUrl)}
                    </button>
                    {/* Vertical Thread Connector line if replies expanded */}
                    {expanded && responses.length > 0 && (
                      <div className="w-[2px] bg-slate-200 dark:bg-neutral-800 flex-1 mt-2 mb-1" aria-hidden="true" />
                    )}
                  </div>

                  {/* Main Tweet Body (Right) */}
                  <div className="flex-1 min-w-0">
                    {/* Header Row: Name · Verified Badge · @handle · Time */}
                    <div className="flex items-center justify-between gap-1 leading-5">
                      <div className="flex items-center gap-1 min-w-0 flex-wrap">
                        {/* Display Name */}
                        <button
                          type="button"
                          disabled={!message.userId}
                          onClick={e => {
                            e.stopPropagation();
                            p.onProfile(message.userId);
                          }}
                          className="font-bold text-[15px] text-slate-900 dark:text-white hover:underline truncate"
                        >
                          {message.userName || 'Learner'}
                        </button>

                        {/* Own message pill */}
                        {message.isOwnMessage && (
                          <span className="text-[11px] font-semibold text-teal-700 dark:text-teal-400 bg-teal-50 dark:bg-teal-950/60 px-1.5 py-0.2 rounded">
                            You
                          </span>
                        )}

                        {/* Dot separator and timestamp */}
                        <span className="text-slate-500 dark:text-neutral-500 text-[14px]">·</span>
                        <time dateTime={message.createdAt} className="text-slate-500 dark:text-neutral-500 text-[14px]">
                          {p.timestamp(message.createdAt)}
                        </time>
                      </div>

                      {/* Right menu / more */}
                      <button
                        type="button"
                        onClick={e => {
                          e.stopPropagation();
                          handleShareThread(message.id);
                        }}
                        className="p-1 rounded-full text-slate-400 hover:text-sky-500 hover:bg-sky-50 dark:hover:bg-neutral-900 transition"
                        title="Share thread"
                      >
                        <MoreHorizontal size={16} />
                      </button>
                    </div>

                    {/* Tweet Content */}
                    {message.text && (
                      <p className="mt-1 text-[15px] leading-snug text-slate-900 dark:text-neutral-100 whitespace-pre-wrap break-words font-normal">
                        {message.text}
                      </p>
                    )}

                    {/* Attached Image / Quoted Media (Twitter rounded container) */}
                    {message.imageUrl && (
                      <div className="mt-3 rounded-2xl border border-slate-200 dark:border-neutral-800 overflow-hidden bg-slate-50 dark:bg-neutral-900">
                        <img
                          loading="lazy"
                          src={message.imageUrl}
                          alt="Thread media"
                          className="w-full max-h-[420px] object-cover"
                        />
                      </div>
                    )}

                    {/* TWITTER ACTION ROW (Chat, Retweet, Like, Views, Share) */}
                    <div className="mt-3 flex items-center justify-between text-slate-500 dark:text-neutral-500 text-[13px] max-w-[440px]">
                      {/* Replies */}
                      <button
                        type="button"
                        onClick={e => {
                          e.stopPropagation();
                          p.onToggle(message.id);
                        }}
                        className="group flex items-center gap-2 hover:text-sky-500 transition -ml-1.5"
                      >
                        <div className="p-1.5 rounded-full group-hover:bg-sky-50 dark:group-hover:bg-sky-950/50 transition">
                          <MessageCircle size={16} />
                        </div>
                        <span>{responses.length || ''}</span>
                      </button>

                      {/* Repost / Share */}
                      <button
                        type="button"
                        onClick={e => {
                          e.stopPropagation();
                          handleShareThread(message.id);
                        }}
                        className="group flex items-center gap-2 hover:text-emerald-500 transition"
                      >
                        <div className="p-1.5 rounded-full group-hover:bg-emerald-50 dark:group-hover:bg-emerald-950/50 transition">
                          {activeShareId === message.id ? <Check size={16} className="text-emerald-500" /> : <Repeat size={16} />}
                        </div>
                        <span className="text-[12px]">{activeShareId === message.id ? 'Copied' : ''}</span>
                      </button>

                      {/* Like */}
                      <button
                        type="button"
                        onClick={e => {
                          e.stopPropagation();
                          toggleLike(message.id);
                        }}
                        className={`group flex items-center gap-2 transition ${isLiked ? 'text-rose-500' : 'hover:text-rose-500'}`}
                      >
                        <div className="p-1.5 rounded-full group-hover:bg-rose-50 dark:group-hover:bg-rose-950/50 transition">
                          <Heart size={16} className={isLiked ? 'fill-current text-rose-500' : ''} />
                        </div>
                        <span>{isLiked ? 1 : ''}</span>
                      </button>

                      {/* Views / Analytics indicator */}
                      <div className="flex items-center gap-1.5 text-slate-400 dark:text-neutral-600">
                        <BarChart2 size={16} />
                        <span className="text-[11px]">{((message.text?.length || 10) * 7) + 12}</span>
                      </div>

                      {/* Bookmark */}
                      <button
                        type="button"
                        onClick={e => {
                          e.stopPropagation();
                          handleShareThread(message.id);
                        }}
                        className="group p-1.5 rounded-full hover:bg-sky-50 dark:hover:bg-sky-950/50 hover:text-sky-500 transition"
                        title="Bookmark"
                      >
                        <Bookmark size={16} />
                      </button>
                    </div>
                  </div>
                </div>

                {/* EXPANDED THREAD REPLIES (TWITTER IN-PLACE CONVERSATION) */}
                {expanded && (
                  <div className="mt-3 pt-3 border-t border-slate-100 dark:border-neutral-900 space-y-3.5 pl-6 sm:pl-10" onClick={e => e.stopPropagation()}>
                    {/* Replies list */}
                    {responses.map(reply => {
                      return (
                        <div key={reply.id} className="flex gap-2.5">
                          <button
                            type="button"
                            disabled={!reply.userId}
                            onClick={() => p.onProfile(reply.userId)}
                            className="shrink-0"
                          >
                            {renderAvatarCircle(reply.userName, reply.profileImageUrl, 'w-8 h-8')}
                          </button>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-1 flex-wrap">
                              <strong className="text-[13px] font-bold text-slate-900 dark:text-white">
                                {reply.userName || 'Learner'}
                              </strong>
                              {reply.isOwnMessage && (
                                <span className="text-[10px] text-teal-600 dark:text-teal-400 bg-teal-50 dark:bg-teal-950/60 px-1 rounded">
                                  You
                                </span>
                              )}
                              <span className="text-slate-400 dark:text-neutral-500 text-xs">·</span>
                              <time className="text-slate-400 dark:text-neutral-500 text-xs">{p.timestamp(reply.createdAt)}</time>
                            </div>
                            <p className="mt-0.5 text-[14px] leading-relaxed text-slate-800 dark:text-neutral-200 whitespace-pre-wrap break-words">
                              {reply.text}
                            </p>
                          </div>
                        </div>
                      );
                    })}

                    {/* Inline Reply Composer */}
                    {room.isMember ? (
                      <form
                        onSubmit={e => submit(e, message.id)}
                        className="flex gap-2.5 items-start pt-2 border-t border-slate-100 dark:border-neutral-900"
                      >
                        {renderAvatarCircle(user?.name, user?.profileImageUrl, 'w-8 h-8')}
                        <div className="flex-1 min-w-0">
                          <input
                            ref={node => { replyInputs.current[message.id] = node; }}
                            value={replyDraft}
                            disabled={pending[message.id]}
                            onChange={e => p.onReplyDraft(message.id, e.target.value)}
                            placeholder={`Reply to ${message.userName || 'post'}…`}
                            className="w-full bg-slate-100 dark:bg-neutral-900 border-none rounded-full px-3.5 py-1.5 text-xs sm:text-[13px] text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
                          />
                        </div>
                        <Button
                          type="submit"
                          size="sm"
                          disabled={pending[message.id] || !replyDraft.trim()}
                          className="rounded-full bg-sky-500 hover:bg-sky-600 text-white font-bold text-xs h-7 px-3 shrink-0"
                        >
                          {pending[message.id] ? <Loader2 size={12} className="animate-spin" /> : 'Reply'}
                        </Button>
                      </form>
                    ) : null}
                  </div>
                )}
              </article>
            );
          })}

          {/* Empty State */}
          {!visible.length && (
            <div className="p-10 text-center text-slate-500 dark:text-neutral-500">
              <p className="font-bold text-base text-slate-900 dark:text-white mb-1">
                {query ? 'No matching discussions' : filter === 'unanswered' ? 'All threads have replies' : filter === 'mine' ? 'No threads from you' : 'No posts yet'}
              </p>
              <p className="text-xs max-w-xs mx-auto mb-4">
                {query ? 'Try different search keywords.' : 'Be the first to share a high-yield question or revision pearl.'}
              </p>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  if (query || filter !== 'all') {
                    setQuery('');
                    setFilter('all');
                  } else if (room.isMember) {
                    focusComposer();
                  } else {
                    p.onJoin(room.id);
                  }
                }}
                className="rounded-full text-xs font-semibold"
              >
                {query || filter !== 'all' ? 'Clear filter' : room.isMember ? 'Write a post' : 'Join circle'}
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>

      {/* =========================================================================
          REMAINING SECTION (PERSONAL INBOX & COMMUNITY WIDGETS)
          ========================================================================= */}
      <aside className="flex-1 min-w-0 max-w-[540px] h-full max-h-full p-5 lg:p-6 space-y-6 hidden lg:block overflow-y-auto overscroll-contain bg-slate-50/50 dark:bg-black border-l border-slate-200/40 dark:border-neutral-900">
        
        {/* PERSONAL INBOX - MATCHING PITCH DARK STYLE */}
        <section className="rounded-2xl border border-slate-200 dark:border-neutral-800 bg-white dark:bg-black p-4 sm:p-5 shadow-sm">
          <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-100 dark:border-neutral-800">
            <h3 className="flex items-center gap-2 text-sm font-bold text-slate-900 dark:text-white">
              <MessageCircle size={16} className="text-teal-600 dark:text-teal-400" />
              <span>Personal inbox</span>
              {conversations.length > 0 && (
                <span className="text-[11px] font-normal px-1.5 py-0.5 rounded-full bg-teal-50 dark:bg-teal-950/60 text-teal-700 dark:text-teal-300">
                  {conversations.length}
                </span>
              )}
            </h3>
          </div>

          {/* Search study partner */}
          <div className="relative mb-3">
            <Search size={14} className="absolute left-3 top-3 text-slate-400" />
            <input
              type="search"
              value={p.directSearch || ''}
              onChange={e => p.onDirectSearch?.(e.target.value)}
              placeholder="Find a study partner…"
              className="w-full bg-slate-100 dark:bg-neutral-900 border border-slate-200/80 dark:border-neutral-800 rounded-xl pl-9 pr-3 py-2 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-neutral-700"
            />
          </div>

          {/* Search results if user is searching */}
          {p.directSearchBusy ? (
            <p className="py-2 text-xs text-slate-400">Searching learners…</p>
          ) : (p.directSearch || '').trim().length >= 2 && !(p.directResults || []).length ? (
            <p className="py-2 text-xs text-slate-400">No learners found matching “{p.directSearch}”.</p>
          ) : (p.directResults || []).length > 0 ? (
            <div className="mb-3 max-h-48 space-y-1 overflow-y-auto border-b border-slate-100 dark:border-neutral-800 pb-2">
              <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-1">Search results</p>
              {p.directResults.map(person => (
                <button
                  key={person.id}
                  type="button"
                  onClick={() => p.onDirect?.(person.id)}
                  className="flex w-full items-center gap-2.5 rounded-xl p-2 text-left hover:bg-slate-50 dark:hover:bg-neutral-800/80 transition"
                >
                  {renderAvatarCircle(person.name, person.profileImageUrl, 'w-8 h-8')}
                  <span className="min-w-0 flex-1">
                    <strong className="block truncate text-xs font-semibold text-slate-900 dark:text-white">{person.name}</strong>
                    <span className="block truncate text-[11px] text-slate-400">{person.medicalCollege || 'Medical Student'}</span>
                  </span>
                  <span className="text-[11px] font-semibold text-teal-600 dark:text-teal-400">Message</span>
                </button>
              ))}
            </div>
          ) : null}

          {/* Direct conversations list */}
          <div className="max-h-64 overflow-y-auto divide-y divide-slate-100 dark:divide-neutral-800/60">
            {p.directBusy ? (
              <p className="py-4 text-xs text-slate-400 text-center">Loading conversations…</p>
            ) : conversations.length ? (
              conversations.map(conv => {
                const person = conv.otherParticipant;
                const latest = conv.messages?.at?.(-1);
                return (
                  <button
                    key={conv.id}
                    type="button"
                    onClick={() => p.onConversation?.(conv.id)}
                    className="flex w-full items-center gap-2.5 py-2.5 px-1 text-left rounded-lg hover:bg-slate-50 dark:hover:bg-neutral-800/60 transition group"
                  >
                    {renderAvatarCircle(person?.name, person?.profileImageUrl, 'w-9 h-9')}
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center justify-between gap-1">
                        <strong className="block truncate text-xs font-semibold text-slate-900 dark:text-white group-hover:text-teal-600 dark:group-hover:text-teal-400 transition">
                          {person?.name || 'Private Chat'}
                        </strong>
                        <time className="text-[10px] text-slate-400 shrink-0">
                          {p.timestamp(latest?.createdAt)}
                        </time>
                      </div>
                      <p className="truncate text-[11px] text-slate-500 dark:text-neutral-400 mt-0.5">
                        {latest?.text || 'Start conversation…'}
                      </p>
                    </div>
                  </button>
                );
              })
            ) : (
              <div className="py-6 text-center">
                <MessagesSquare size={22} className="mx-auto text-slate-400 mb-2 opacity-60" />
                <p className="text-xs text-slate-500 dark:text-neutral-400">
                  Great study partnerships start with a simple hello.
                </p>
              </div>
            )}
          </div>
        </section>

        {/* CIRCLE DETAILS & ADMIN SPOTLIGHT */}
        <section className="rounded-2xl border border-slate-200 dark:border-neutral-800 bg-white dark:bg-black p-4 sm:p-5 shadow-sm space-y-3.5">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">About this circle</h3>
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-sky-50 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300">
              {room.topic || 'Medical discussion'}
            </span>
          </div>
          
          <h4 className="font-bold text-base text-slate-900 dark:text-white leading-snug">{room.name}</h4>
          {room.description && (
            <p className="text-xs text-slate-600 dark:text-neutral-300 leading-relaxed">{room.description}</p>
          )}

          {/* Admin card */}
          {adminMember && (
            <div className="rounded-xl p-3 bg-amber-500/10 border border-amber-500/20">
              <div className="flex items-center gap-1.5 text-[11px] font-bold text-amber-700 dark:text-amber-400 uppercase tracking-wider mb-2">
                <Crown size={13} />
                <span>Circle Administrator</span>
              </div>
              <div className="flex items-center justify-between gap-2.5">
                <button
                  type="button"
                  onClick={() => p.onProfile?.(adminMember.id)}
                  className="flex items-center gap-2 text-left min-w-0 group"
                >
                  {renderAvatarCircle(adminMember.name, adminMember.profileImageUrl, 'w-8 h-8')}
                  <div className="min-w-0">
                    <p className="text-xs font-bold text-slate-900 dark:text-white truncate group-hover:underline">{adminMember.name}</p>
                    <p className="text-[10px] text-slate-400 truncate">{adminMember.medicalCollege || 'Medical Student'}</p>
                  </div>
                </button>
                {adminMember.id !== user?.id && (
                  <button
                    type="button"
                    onClick={() => p.onDirect?.(adminMember.id)}
                    className="text-xs font-semibold text-teal-600 dark:text-teal-400 hover:underline shrink-0"
                  >
                    Message
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Member count & view all */}
          <div className="pt-1 flex items-center justify-between border-t border-slate-100 dark:border-neutral-800 text-xs">
            <span className="text-slate-500 dark:text-neutral-400">
              <strong>{room.memberCount || (room.members || []).length}</strong> learners enrolled
            </span>
            <button
              type="button"
              onClick={() => setIsDetailsOpen(true)}
              className="font-semibold text-sky-600 dark:text-sky-400 hover:underline"
            >
              View directory →
            </button>
          </div>
        </section>

        {/* OTHER CIRCLES QUICK SWITCHER */}
        {otherCommunities.length > 0 && (
          <section className="rounded-2xl border border-slate-200 dark:border-neutral-800 bg-white dark:bg-black p-4 sm:p-5 shadow-sm space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Explore other circles</h3>
            <div className="space-y-2">
              {otherCommunities.map(c => (
                <button
                  key={c.id}
                  type="button"
                  onClick={() => p.onOpenRoom?.(c.id)}
                  className="flex w-full items-center justify-between gap-3 p-2.5 rounded-xl hover:bg-slate-50 dark:hover:bg-neutral-800/80 transition text-left group"
                >
                  <div className="min-w-0">
                    <p className="text-xs font-semibold text-slate-900 dark:text-white truncate group-hover:text-teal-600 dark:group-hover:text-teal-400">
                      {c.name}
                    </p>
                    <p className="text-[11px] text-slate-400 truncate">
                      {c.memberCount || (c.members || []).length} members · {c.topic || 'Discussion'}
                    </p>
                  </div>
                  <ChevronRight size={14} className="text-slate-300 group-hover:text-teal-600 shrink-0" />
                </button>
              ))}
            </div>
          </section>
        )}
      </aside>

      {/* =========================================================================
          CIRCLE INFORMATION & MEMBERS MODAL (CLICKED ON HEADER)
          Shows: Community info, Admin with Crown, and Member list with Profiles
          ========================================================================= */}
      {isDetailsOpen && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/60 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          onClick={() => setIsDetailsOpen(false)}
        >
          <div
            className="w-full max-w-md rounded-2xl bg-white dark:bg-neutral-900 border border-slate-200 dark:border-neutral-800 shadow-2xl overflow-hidden flex flex-col max-h-[85vh] text-slate-900 dark:text-white"
            onClick={e => e.stopPropagation()}
          >
            {/* Modal Top Bar */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100 dark:border-neutral-800">
              <h2 className="font-bold text-base">Circle Details</h2>
              <button
                type="button"
                onClick={() => setIsDetailsOpen(false)}
                className="p-1.5 rounded-full hover:bg-slate-100 dark:hover:bg-neutral-800 text-slate-500 dark:text-neutral-400"
              >
                <X size={18} />
              </button>
            </div>

            {/* Modal Body */}
            <div className="overflow-y-auto p-4 space-y-4">
              {/* Group overview */}
              <div className="space-y-1.5">
                <h3 className="font-bold text-lg text-slate-900 dark:text-white">{room.name}</h3>
                <span className="inline-block text-xs font-semibold px-2 py-0.5 rounded bg-sky-50 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300">
                  {room.topic || 'Medical discussion'}
                </span>
                {room.description && (
                  <p className="text-xs text-slate-600 dark:text-neutral-300 pt-1 leading-relaxed">{room.description}</p>
                )}
                <div className="flex items-center gap-3 pt-2 text-xs text-slate-500 dark:text-neutral-400">
                  <span><strong>{room.memberCount || (room.members || []).length}</strong> members</span>
                  <span>·</span>
                  <span><strong>{threads.length}</strong> threads</span>
                </div>
              </div>

              {/* ADMIN SPOTLIGHT */}
              <div className="rounded-xl p-3 bg-amber-500/10 border border-amber-500/20">
                <div className="flex items-center gap-1.5 text-xs font-bold text-amber-700 dark:text-amber-400 uppercase tracking-wide mb-2">
                  <Crown size={14} />
                  <span>Circle Administrator</span>
                </div>
                {adminMember ? (
                  <div className="flex items-center justify-between gap-3">
                    <button
                      type="button"
                      onClick={() => {
                        setIsDetailsOpen(false);
                        p.onProfile(adminMember.id);
                      }}
                      className="flex items-center gap-2.5 text-left group"
                    >
                      {renderAvatarCircle(adminMember.name, adminMember.profileImageUrl, 'w-9 h-9')}
                      <div>
                        <p className="text-xs font-bold text-slate-900 dark:text-white group-hover:underline">
                          {adminMember.name}
                        </p>
                        <p className="text-[11px] text-slate-500 dark:text-neutral-400">
                          {adminMember.medicalCollege || 'Medical Student'}
                        </p>
                      </div>
                    </button>
                    {adminMember.id !== user?.id && (
                      <button
                        type="button"
                        onClick={() => {
                          setIsDetailsOpen(false);
                          p.onDirect(adminMember.id);
                        }}
                        className="text-xs font-semibold text-sky-600 dark:text-sky-400 hover:underline"
                      >
                        Message
                      </button>
                    )}
                  </div>
                ) : (
                  <p className="text-xs text-slate-500">Platform Admin</p>
                )}
              </div>

              {/* MEMBERS LIST */}
              <div>
                <p className="text-xs font-bold uppercase tracking-wide text-slate-500 dark:text-neutral-400 mb-2">
                  All Members ({room.memberCount || (room.members || []).length})
                </p>

                {/* Member Search input */}
                <div className="relative mb-2">
                  <Search size={14} className="absolute left-3 top-2.5 text-slate-400" />
                  <input
                    type="search"
                    placeholder="Search members…"
                    value={memberSearch}
                    onChange={e => setMemberSearch(e.target.value)}
                    className="w-full bg-slate-100 dark:bg-neutral-800 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none"
                  />
                </div>

                <div className="max-h-48 overflow-y-auto divide-y divide-slate-100 dark:divide-neutral-800">
                  {filteredMembers.map(member => {
                    const isAdmin = member.id === room.adminUserId;
                    const isSelf = member.id === user?.id;
                    return (
                      <div key={member.id} className="py-2 flex items-center justify-between gap-2">
                        <button
                          type="button"
                          onClick={() => {
                            setIsDetailsOpen(false);
                            p.onProfile(member.id);
                          }}
                          className="flex items-center gap-2 text-left min-w-0 group"
                        >
                          {renderAvatarCircle(member.name, member.profileImageUrl, 'w-8 h-8')}
                          <div className="min-w-0">
                            <div className="flex items-center gap-1">
                              <span className="text-xs font-bold text-slate-900 dark:text-white truncate group-hover:underline">
                                {member.name}
                              </span>
                              {isAdmin && (
                                <span className="text-[10px] font-semibold text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40 px-1 rounded">
                                  Admin
                                </span>
                              )}
                              {isSelf && (
                                <span className="text-[10px] font-semibold text-teal-600 dark:text-teal-400 bg-teal-50 dark:bg-teal-950/40 px-1 rounded">
                                  You
                                </span>
                              )}
                            </div>
                            <p className="text-[10px] text-slate-400 dark:text-neutral-500 truncate">
                              {member.medicalCollege || 'Member'}
                            </p>
                          </div>
                        </button>

                        <div className="flex items-center gap-2 shrink-0">
                          {!isSelf && (
                            <button
                              type="button"
                              onClick={() => {
                                setIsDetailsOpen(false);
                                p.onDirect(member.id);
                              }}
                              className="text-xs text-sky-600 dark:text-sky-400 hover:underline font-medium"
                            >
                              Message
                            </button>
                          )}
                          {room.isAdmin && !isAdmin && (
                            <button
                              type="button"
                              onClick={() => p.onRemoveMember(room.id, member.id)}
                              className="text-xs text-red-500 hover:underline"
                            >
                              Remove
                            </button>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Modal Bottom */}
            <div className="p-3 border-t border-slate-100 dark:border-neutral-800 bg-slate-50 dark:bg-neutral-950 flex justify-between items-center">
              {room.isMember ? (
                <button
                  type="button"
                  onClick={handleCopyInvite}
                  className="text-xs text-sky-600 dark:text-sky-400 hover:underline flex items-center gap-1 font-semibold"
                >
                  {copiedLink ? <Check size={14} className="text-emerald-500" /> : <Link2 size={14} />}
                  <span>{copiedLink ? 'Link copied' : 'Copy invite link'}</span>
                </button>
              ) : <div />}
              <Button
                variant="outline"
                size="sm"
                className="rounded-full text-xs"
                onClick={() => setIsDetailsOpen(false)}
              >
                Close
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
