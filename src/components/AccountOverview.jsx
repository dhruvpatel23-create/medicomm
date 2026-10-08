import { useState } from 'react';
import { ArrowUpRight, Camera, Check, CheckCircle2, Flame, GraduationCap, LogOut, MapPin, RefreshCw, Target, Trophy, X } from 'lucide-react';

const panel = 'rounded-2xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-[#101827]';
const secondary = 'inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800';
const primary = 'inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-600/15 transition hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 disabled:opacity-50';
const label = 'text-xs font-semibold uppercase tracking-[0.18em] text-blue-600 dark:text-sky-400';
const muted = 'text-sm leading-relaxed text-slate-500 dark:text-slate-400';
const value = number => number == null ? '—' : Number(number).toLocaleString('en-IN');

export function AccountStatus({ overview, guest }) {
  if (guest) return <p className={muted}>You’re exploring as a guest. Sign in to save activity and see your ranking.</p>;
  if (overview.error) return <div role="alert" className="flex flex-wrap items-center gap-3 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">{overview.error}<button className={secondary} type="button" onClick={overview.reload}>Try again</button></div>;
  if (overview.loading) return <p role="status" className={muted}>Loading your saved activity…</p>;
  return null;
}

export function DashboardSummary({ user, overview, guest, onContinue }) {
  const stats = overview.data?.stats;
  const cards = [
    { label: 'Current streak', number: stats ? `${stats.streak} ${stats.streak === 1 ? 'day' : 'days'}` : '—', detail: 'Keep your momentum', icon: Flame, tint: 'bg-orange-50 text-orange-600 dark:bg-orange-400/10 dark:text-orange-300' },
    { label: 'Accuracy', number: stats?.accuracy == null ? '—' : `${stats.accuracy}%`, detail: stats?.attempted ? 'Across all MCQ attempts' : 'Answer a question to begin', icon: Target, tint: 'bg-emerald-50 text-emerald-600 dark:bg-emerald-400/10 dark:text-emerald-300' },
    { label: 'Questions attempted', number: value(stats?.attempted), detail: 'Your saved progress', icon: GraduationCap, tint: 'bg-sky-50 text-sky-600 dark:bg-sky-400/10 dark:text-sky-300' },
    { label: 'Correct answers', number: value(stats?.correct), detail: 'Knowledge put into practice', icon: CheckCircle2, tint: 'bg-violet-50 text-violet-600 dark:bg-violet-400/10 dark:text-violet-300' },
    { label: 'National rank', number: stats?.nationalRank ? `#${value(stats.nationalRank)}` : '—', detail: 'Overall rating leaderboard', icon: Trophy, tint: 'bg-amber-50 text-amber-600 dark:bg-amber-400/10 dark:text-amber-300' },
  ];
  return <div data-testid="dashboard-summary" className="mb-7 space-y-5 text-slate-900 dark:text-slate-100">
    <header className="flex flex-wrap items-end justify-between gap-5 py-2">
      <div><p className={label}>Your learning, at a glance</p><h2 className="!mb-2 !mt-3 !text-3xl !font-semibold !tracking-tight sm:!text-4xl">Welcome back, {user?.name?.split(' ')[0] || 'learner'}<span className="text-blue-500">.</span></h2><p className={muted}>Every question is another step forward.</p></div>
      <div className="flex gap-2"><button type="button" className={secondary} aria-label="Refresh dashboard" onClick={overview.reload} disabled={overview.loading || guest}><RefreshCw size={17} /></button><button type="button" className={primary} onClick={onContinue}>Continue practice <ArrowUpRight size={17} /></button></div>
    </header>
    <AccountStatus overview={overview} guest={guest} />
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-5 lg:gap-4" aria-busy={overview.loading}>
      {cards.map(({ label: title, number, detail, icon: Icon, tint }) => <article key={title} className={`${panel} p-4 sm:p-5 last:col-span-2 lg:last:col-span-1`}>
        <span className={`mb-5 inline-flex h-10 w-10 items-center justify-center rounded-xl ${tint}`}><Icon size={20} strokeWidth={1.7} /></span>
        <p className="text-xs font-medium text-slate-500 dark:text-slate-400">{title}</p><strong className="mt-2 block text-3xl font-semibold tracking-tight tabular-nums">{number}</strong><p className="mt-2 text-[11px] leading-relaxed text-slate-500 dark:text-slate-400">{detail}</p>
      </article>)}
    </div>
  </div>;
}

export function ProfileOverview({ user, overview, guest, previewImage, photoBusy, pendingPhoto, onPhoto, onSavePhoto, onCancelPhoto, onLogout, message }) {
  const [failedImage, setFailedImage] = useState('');
  const stats = overview.data?.stats;
  const initials = (user?.name || 'Learner').split(' ').filter(Boolean).slice(0, 2).map(part => part[0]).join('').toUpperCase();
  return <div data-testid="profile-overview" className="mb-6 space-y-5 text-slate-900 dark:text-slate-100">
    <header className="flex flex-wrap items-center justify-between gap-4 py-2"><div><p className={label}>Profile</p><h2 className="!mb-2 !mt-3 !text-3xl !font-semibold !tracking-tight sm:!text-4xl">Your space. Your progress.</h2><p className={muted}>Manage your photo and see where you stand.</p></div><button type="button" className={secondary} onClick={onLogout}><LogOut size={16} /> {guest ? 'Sign in' : 'Logout'}</button></header>
    <AccountStatus overview={overview} guest={guest} />
    <div className="grid gap-5 md:grid-cols-2">
      <article className={`${panel} overflow-hidden`}><div className="h-20 bg-gradient-to-r from-blue-600 via-sky-500 to-cyan-400 dark:from-blue-950 dark:via-blue-800 dark:to-cyan-700" />
        <div className="px-6 pb-6"><div className="-mt-10 mb-4 flex items-end justify-between gap-3"><span className={`${user?.hasPracticeAccess ? 'paid-avatar ' : ''}relative flex h-24 w-24 shrink-0 items-center justify-center overflow-hidden rounded-2xl border-4 border-white bg-blue-100 text-3xl font-semibold text-blue-800 shadow-sm dark:border-[#101827] dark:bg-blue-900 dark:text-blue-100`}>
          {previewImage && failedImage !== previewImage ? <img src={previewImage} onError={() => setFailedImage(previewImage)} alt={`${user?.name || 'Your'} profile picture`} className="h-full w-full object-cover" /> : initials}
        </span><span className="mb-1 inline-flex items-center gap-1.5 rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300"><Check size={12} /> {guest ? 'Guest' : user?.hasPracticeAccess ? 'Paid member' : 'Member'}</span></div>
          <h3 className="!m-0 !text-xl !font-semibold">{user?.name || 'Learner'}</h3><p className="mt-1 break-words text-sm text-slate-500 dark:text-slate-400">{guest ? 'Explore Medulla' : user?.email}</p>
          {user?.medicalCollege && <p className="mt-3 flex items-start gap-2 text-sm text-slate-500 dark:text-slate-400"><GraduationCap size={16} className="mt-0.5 shrink-0" /> {user.medicalCollege}</p>}
          <div className="mt-5 flex flex-wrap gap-2"><label className={`${secondary} relative cursor-pointer ${guest || photoBusy ? 'pointer-events-none opacity-50' : ''}`}><Camera size={16} /> Change photo<input className="absolute inset-0 w-full cursor-pointer opacity-0" aria-label="Change profile photo" type="file" accept="image/png,image/jpeg,image/webp,image/gif" onChange={onPhoto} disabled={guest || photoBusy} /></label>
            {pendingPhoto && <><button type="button" className={primary} disabled={photoBusy} onClick={onSavePhoto}>{photoBusy ? 'Saving…' : 'Save photo'}</button><button type="button" className={secondary} aria-label="Cancel new photo" disabled={photoBusy} onClick={onCancelPhoto}><X size={16} /></button></>}
          </div><p className="mt-3 text-xs text-slate-500 dark:text-slate-400">PNG, JPG, WebP or GIF · up to 5 MB</p>
          {message && <p role="status" className="mt-3 text-sm text-blue-700 dark:text-sky-300">{message}</p>}
        </div>
      </article>
      <article className={`${panel} p-6`}><div className="mb-6 flex items-center justify-between"><div><p className={label}>The bigger picture</p><h3 className="!mb-0 !mt-2 !text-xl !font-semibold">Your standing</h3></div><span className="rounded-xl bg-amber-50 p-3 text-amber-600 dark:bg-amber-400/10 dark:text-amber-300"><Trophy size={23} /></span></div>
        <dl className="divide-y divide-slate-100 dark:divide-slate-800">{[
          ['National rank', stats?.nationalRank ? `#${value(stats.nationalRank)}` : '—'],
          [`${stats?.state || 'State'} rank`, stats?.stateRank ? `#${value(stats.stateRank)}` : '—'],
          ['Rating', value(stats?.rating)], ['Current streak', stats ? `${stats.streak} ${stats.streak === 1 ? 'day' : 'days'}` : '—'],
        ].map(([title, number]) => <div key={title} className="flex items-center justify-between gap-4 py-4"><dt className="text-sm text-slate-500 dark:text-slate-400">{title}</dt><dd className="text-lg font-semibold tabular-nums">{number}</dd></div>)}</dl>
        <p className="mt-4 flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400"><MapPin size={13} /> State ranking follows your medical college.</p>
      </article>
    </div>
  </div>;
}
