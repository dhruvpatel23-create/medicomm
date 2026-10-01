import { Search, X } from 'lucide-react';

export const socialPage = 'mx-auto w-full max-w-[1200px] space-y-7 pb-10 pt-5 text-slate-900 dark:text-slate-100 motion-safe:animate-in motion-safe:fade-in motion-safe:slide-in-from-bottom-2 motion-safe:duration-300';
export const surface = 'min-w-0 rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900';
export const muted = 'text-sm leading-relaxed text-slate-500 dark:text-slate-400';
export const primary = 'inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-cyan-700 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-cyan-800 active:scale-[0.98] focus-visible:ring-2 focus-visible:ring-cyan-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-cyan-300 dark:text-slate-950 dark:hover:bg-cyan-200 motion-reduce:transition-none';
export const secondary = 'inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:border-cyan-500 hover:bg-slate-50 focus-visible:ring-2 focus-visible:ring-cyan-500 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800 motion-reduce:transition-none';
export const field = 'min-h-11 w-full min-w-0 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm font-normal text-slate-900 placeholder:text-slate-400 focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100';
export const pill = 'inline-flex items-center gap-1.5 rounded-md bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300';
export const avatar = 'flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden rounded-xl bg-cyan-50 text-sm font-bold text-cyan-800 dark:bg-cyan-400/10 dark:text-cyan-200';
export const initials = name => (name || 'Learner').split(' ').filter(Boolean).slice(0, 2).map(part => part[0]).join('').toUpperCase();
export const number = value => Number(value || 0).toLocaleString();

export function Avatar({ name, src }) {
  return <span className={avatar}>{src ? <img src={src} alt="" className="h-full w-full object-cover" /> : initials(name)}</span>;
}
export function SearchField({ value, onChange, placeholder, label }) {
  return <div className="relative min-w-0"><Search size={17} className="pointer-events-none absolute left-3 top-3.5 text-slate-400" aria-hidden="true" /><input type="search" aria-label={label || placeholder} value={value} onChange={e => onChange(e.target.value)} placeholder={placeholder} className={`${field} pl-10 pr-10 [&::-webkit-search-cancel-button]:appearance-none`} />{value && <button type="button" className="absolute right-1 top-1 flex h-9 w-9 items-center justify-center rounded-lg text-slate-500 hover:bg-slate-200 dark:hover:bg-slate-800" aria-label={`Clear ${label || 'search'}`} onClick={() => onChange('')}><X size={15} /></button>}</div>;
}
export function EmptyState({ icon: Icon, title, children }) {
  return <div className="flex flex-col items-center px-5 py-12 text-center"><span className="mb-4 rounded-2xl bg-slate-100 p-3 text-slate-400 dark:bg-slate-800"><Icon size={24} strokeWidth={1.5} /></span><h3 className="text-base font-semibold">{title}</h3><div className={`mt-2 max-w-sm ${muted}`}>{children}</div></div>;
}
