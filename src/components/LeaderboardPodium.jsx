import { Crown, Medal } from 'lucide-react';
import { initials, number } from './SocialUI';

const places = [
  { rank: 2, label: '2nd', height: 'h-24 sm:h-28', face: 'from-slate-200 to-slate-100 border-slate-300 dark:from-slate-700 dark:to-slate-800 dark:border-slate-600', ink: 'text-slate-500 dark:text-slate-300', avatar: 'border-slate-300 bg-slate-100 text-slate-600 dark:border-slate-500 dark:bg-slate-800 dark:text-slate-200', top: 'bg-slate-300/60 dark:bg-slate-600/70' },
  { rank: 1, label: '1st', height: 'h-36 sm:h-44', face: 'from-amber-200 to-amber-50 border-amber-300 dark:from-amber-800/70 dark:to-amber-950/50 dark:border-amber-600/60', ink: 'text-amber-700 dark:text-amber-200', avatar: 'border-amber-300 bg-amber-50 text-amber-800 dark:border-amber-500 dark:bg-amber-950 dark:text-amber-200', top: 'bg-amber-300/70 dark:bg-amber-600/60' },
  { rank: 3, label: '3rd', height: 'h-16 sm:h-20', face: 'from-orange-200/80 to-orange-50 border-orange-300/70 dark:from-orange-900/60 dark:to-orange-950/40 dark:border-orange-700/60', ink: 'text-orange-800 dark:text-orange-200', avatar: 'border-orange-300 bg-orange-50 text-orange-800 dark:border-orange-700 dark:bg-orange-950 dark:text-orange-200', top: 'bg-orange-300/60 dark:bg-orange-700/60' },
];

export default function LeaderboardPodium({ players, onProfile }) {
  return <div className="relative isolate overflow-hidden px-3 pt-10 sm:px-8" role="group" aria-label="Top three standings">
    <div aria-hidden="true" className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_50%_90%,rgba(251,191,36,0.12),transparent_65%)] dark:bg-[radial-gradient(ellipse_at_50%_90%,rgba(251,191,36,0.08),transparent_65%)]" />
    <div className="mx-auto grid max-w-xl grid-cols-3 items-end gap-2 sm:gap-4">
      {places.map(place => {
        const player = players[place.rank - 1];
        return <div key={place.rank} className="min-w-0 text-center">
          <button type="button" disabled={!player} onClick={() => onProfile(player.id)} aria-label={player ? `${place.label} place: ${player.name}, ${number(player.score)} rating. View profile` : `${place.label} place is unclaimed`} className="group relative mb-4 flex w-full min-w-0 flex-col items-center rounded-xl px-1 pb-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500 focus-visible:ring-offset-4 disabled:cursor-default dark:focus-visible:ring-offset-slate-900">
            {place.rank === 1 && <Crown aria-hidden="true" size={24} strokeWidth={1.6} className="absolute -top-7 text-amber-500 dark:text-amber-300" />}
            <span className={`relative mb-3 flex h-12 w-12 items-center justify-center rounded-full border-2 text-sm font-bold shadow-sm transition-transform group-enabled:group-hover:-translate-y-1 sm:h-14 sm:w-14 sm:text-base motion-reduce:transition-none ${place.avatar}`}>
              {player ? initials(player.name) : <Medal size={22} strokeWidth={1.3} />}
              <span className={`absolute -bottom-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full border-2 border-white text-[9px] font-bold dark:border-slate-900 ${place.top} ${place.ink}`}>{place.rank}</span>
            </span>
            <span className="block w-full truncate text-xs font-semibold text-slate-800 group-enabled:group-hover:text-cyan-700 dark:text-slate-100 dark:group-enabled:group-hover:text-cyan-300 sm:text-sm" title={player?.name}>{player ? player.isCurrentUser ? `${player.name} (you)` : player.name : 'Your spot?'}</span>
            <span className="mt-1 block w-full truncate text-[10px] text-slate-500 dark:text-slate-400 sm:text-xs" title={player?.state}>{player?.state || 'Not yet ranked'}</span>
            <span className="mt-2 text-base font-bold tabular-nums tracking-tight sm:text-xl">{player ? number(player.score) : '—'}<span className="ml-1 text-[9px] font-normal tracking-normal text-slate-500 dark:text-slate-400 sm:text-[10px]">rating</span></span>
          </button>
          <div aria-hidden="true" className={`relative overflow-hidden rounded-t-xl border-x border-t bg-gradient-to-b pt-4 shadow-[inset_-6px_0_0_rgba(0,0,0,0.025)] motion-safe:animate-in motion-safe:fade-in motion-safe:slide-in-from-bottom-4 motion-safe:duration-700 ${place.height} ${place.face}`}>
            <div className={`absolute inset-x-0 top-0 h-2 border-b border-white/30 ${place.top}`} />
            <div className={`flex items-baseline justify-center ${place.ink}`}><span className="text-4xl font-semibold tracking-tighter sm:text-5xl">{place.rank}</span><span className="ml-0.5 text-xs font-semibold sm:text-sm">{place.label.slice(1)}</span></div>
          </div>
        </div>;
      })}
    </div>
    <div aria-hidden="true" className="mx-auto h-2 max-w-xl rounded-t-sm bg-slate-200/80 dark:bg-slate-700/70" />
  </div>;
}
