import { useState } from 'react';
import { Swords, Trophy, Zap, Clock, Target, ArrowRight, ShieldCheck, Flame, Users, Sparkles, Bot } from 'lucide-react';

export default function HomeBattleSection({ onCompete, onLeaderboard, userRating }) {
  const [activeTab, setActiveTab] = useState('matchmaking'); // 'matchmaking' | 'gameplay' | 'ranking'

  const tabs = [
    {
      id: 'matchmaking',
      label: 'Live Matchmaking',
      icon: Swords,
      badge: 'Live P2P',
      eyebrow: 'REAL-TIME PEER CHALLENGE',
      title: 'Head-to-head live clinical duels',
      description: 'Enter the arena to match synchronously with verified MBBS students across India. Answer identical, high-yield NEET PG / INICET questions simultaneously under real-time pacing.',
      features: [
        {
          icon: Target,
          title: '5 High-Yield Clinical MCQs',
          desc: 'Carefully calibrated clinical doubt and diagnosis MCQs per round.'
        },
        {
          icon: Zap,
          title: 'Instant Matchmaking',
          desc: 'Instant peer pairing with automatic AI challenger fallback so you never wait.'
        },
        {
          icon: ShieldCheck,
          title: 'Synchronous Locks',
          desc: 'Simultaneous answer locks and anti-cheat reveals protect competition integrity.'
        }
      ]
    },
    {
      id: 'gameplay',
      label: 'Speed & Instinct',
      icon: Clock,
      badge: 'Exam-Paced',
      eyebrow: 'EXAM-SPEED RECALL',
      title: 'Build split-second clinical reflexes',
      description: 'Eliminate hesitation under true exam pressure. Watch your opponent’s progress bar update in real time as each clinical decision is locked in.',
      features: [
        {
          icon: Clock,
          title: 'Live Countdown Pacing',
          desc: 'Strict per-question timer pushes active recall under true clinical stress.'
        },
        {
          icon: Users,
          title: 'Live Opponent Progress',
          desc: 'Feel the adrenaline as you track your rival’s answer pace and locks live.'
        },
        {
          icon: Sparkles,
          title: 'Post-Duel Rationales',
          desc: 'In-depth clinical pearls and textbook citations immediately after the match.'
        }
      ]
    },
    {
      id: 'ranking',
      label: 'Rating & Leaderboards',
      icon: Trophy,
      badge: 'Ranked Elo',
      eyebrow: 'ELO RATING SYSTEM',
      title: 'Climb state and national leaderboards',
      description: 'Earn +1 Elo for each practice MCQ answered correctly on your very first attempt. Your rating updates live when the answer is saved. Climb state-wise and all-India leaderboards through practice and rated duels.',
      features: [
        {
          icon: Trophy,
          title: '1st attempt · +1 Elo',
          desc: 'A correct first answer earns a “1st attempt” badge and +1 Elo, once per question. Wrong first, right later? No badge or extra rating.'
        },
        {
          icon: ShieldCheck,
          title: 'Saved & synced live',
          desc: 'Your first result stays saved to your account. Confirmed rating changes sync across open tabs and devices; retries never earn extra points.'
        },
        {
          icon: Swords,
          title: '1v1 Direct Duels',
          desc: 'Rated duel results also change your Elo. Challenge study partners from community circles and your inbox to climb the rankings.'
        }
      ]
    }
  ];

  const current = tabs.find(t => t.id === activeTab) || tabs[0];
  const CurrentIcon = current.icon;

  return (
    <section className="home-battle-section my-8 w-full" aria-label="1v1 Battle Learning Arena">
      <div className="rounded-3xl border border-cyan-500/30 dark:border-neutral-800 bg-gradient-to-br from-white via-cyan-50/30 to-sky-50/20 dark:from-neutral-950 dark:via-black dark:to-neutral-900 p-6 sm:p-8 shadow-xl shadow-cyan-950/5 dark:shadow-none overflow-hidden relative transition-colors">

        {/* Subtle decorative glow elements */}
        <div className="pointer-events-none absolute -right-20 -top-20 w-80 h-80 rounded-full bg-cyan-400/10 dark:bg-cyan-500/10 blur-3xl" aria-hidden="true" />
        <div className="pointer-events-none absolute -left-20 -bottom-20 w-80 h-80 rounded-full bg-sky-400/10 dark:bg-sky-500/10 blur-3xl" aria-hidden="true" />

        {/* Section Header */}
        <div className="relative z-10 flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-200/80 dark:border-neutral-800">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-cyan-100 dark:bg-cyan-950/80 border border-cyan-300 dark:border-cyan-800 text-[10px] font-bold uppercase tracking-wider text-cyan-800 dark:text-cyan-300">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
                Live 1v1 Arena
              </span>
              <span className="text-xs text-slate-400 dark:text-neutral-500 font-medium">· Gamified Medical Learning</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">
              1v1 Battle Learning
            </h2>
            <p className="mt-1 text-xs sm:text-sm text-slate-600 dark:text-neutral-400 max-w-xl leading-relaxed">
              Sharpen your medical diagnostic instincts under real-time duel pressure against peers nationwide.
            </p>
          </div>

          {/* Quick rating indicator */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 rounded-2xl bg-white dark:bg-neutral-900 border border-slate-200 dark:border-neutral-800 px-3.5 py-2 shadow-sm">
              <Trophy size={16} className="text-amber-500" />
              <div className="text-left">
                <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">Your Rating</p>
                <p className="text-sm font-bold text-slate-900 dark:text-white tabular-nums" aria-live="polite">{userRating ?? 1480} Elo</p>
              </div>
            </div>
          </div>
        </div>

        {/* Interactive Tabs */}
        <div className="relative z-10 mt-6 flex flex-wrap gap-2" role="tablist" aria-label="1v1 Battle Features">
          {tabs.map(tab => {
            const active = activeTab === tab.id;
            const TabIcon = tab.icon;
            return (
              <button
                key={tab.id}
                role="tab"
                type="button"
                aria-selected={active}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all ${
                  active
                    ? 'bg-slate-900 text-white dark:bg-cyan-400 dark:text-slate-950 shadow-md shadow-slate-900/10'
                    : 'bg-white/80 dark:bg-neutral-900/80 text-slate-600 dark:text-neutral-400 hover:text-slate-900 dark:hover:text-white border border-slate-200 dark:border-neutral-800 hover:border-slate-300 dark:hover:border-neutral-700'
                }`}
              >
                <TabIcon size={15} />
                <span>{tab.label}</span>
                <span className={`text-[10px] px-1.5 py-0.5 rounded-md font-bold uppercase tracking-wider ${
                  active
                    ? 'bg-white/20 dark:bg-black/20 text-white dark:text-black'
                    : 'bg-slate-100 dark:bg-neutral-800 text-slate-500 dark:text-neutral-400'
                }`}>
                  {tab.badge}
                </span>
              </button>
            );
          })}
        </div>

        {/* Tab Detail & Action Grid */}
        <div className="relative z-10 mt-6 grid gap-6 lg:grid-cols-[1fr_320px] items-stretch">

          {/* Active Tab Info Box */}
          <div className="flex flex-col justify-between rounded-2xl bg-white/90 dark:bg-neutral-900/90 border border-slate-200 dark:border-neutral-800 p-5 sm:p-6 shadow-sm">
            <div>
              <p className="text-[11px] font-bold uppercase tracking-wider text-cyan-600 dark:text-cyan-400 mb-1 flex items-center gap-1.5">
                <CurrentIcon size={14} />
                <span>{current.eyebrow}</span>
              </p>
              <h3 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white leading-snug">
                {current.title}
              </h3>
              <p className="mt-2 text-xs sm:text-sm text-slate-600 dark:text-neutral-300 leading-relaxed">
                {current.description}
              </p>

              {/* 3 Key Feature Items */}
              <div className="mt-5 grid sm:grid-cols-3 gap-3">
                {current.features.map(feat => {
                  const FeatIcon = feat.icon;
                  return (
                    <div
                      key={feat.title}
                      className="rounded-xl border border-slate-100 dark:border-neutral-800 bg-slate-50/70 dark:bg-black/40 p-3.5 flex flex-col justify-start"
                    >
                      <div className="w-7 h-7 rounded-lg bg-cyan-100 dark:bg-cyan-950/80 text-cyan-700 dark:text-cyan-300 flex items-center justify-center mb-2.5 shrink-0">
                        <FeatIcon size={14} />
                      </div>
                      <h4 className="text-xs font-bold text-slate-900 dark:text-white leading-tight">
                        {feat.title}
                      </h4>
                      <p className="mt-1 text-[11px] text-slate-500 dark:text-neutral-400 leading-normal">
                        {feat.desc}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="mt-5 pt-3 border-t border-slate-100 dark:border-neutral-800/80 flex items-center gap-2 text-[11px] text-slate-500 dark:text-neutral-400">
              <Bot size={14} className="text-cyan-600 dark:text-cyan-400 shrink-0" />
              <span>Smart bot challenger available immediately if no peer is in queue.</span>
            </div>
          </div>

          {/* Action Card */}
          <div className="rounded-2xl border border-cyan-300/60 dark:border-cyan-800/80 bg-gradient-to-b from-cyan-500/10 via-white dark:via-neutral-900 to-sky-50 dark:to-neutral-950 p-5 sm:p-6 flex flex-col justify-between shadow-sm">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-700 dark:text-cyan-300 bg-cyan-100/70 dark:bg-cyan-950 px-2 py-0.5 rounded">
                  Live Arena
                </span>
                <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-ping" />
              </div>
              <h3 className="text-lg font-bold text-slate-900 dark:text-white leading-snug">
                Step into the Compete Arena
              </h3>
              <p className="mt-2 text-xs text-slate-600 dark:text-neutral-400 leading-relaxed">
                Launch a 1v1 battle now. 5 questions, split-second choices, real-time feedback.
              </p>
            </div>

            <div className="mt-6 space-y-2.5">
              {/* PRIMARY COMPETE BUTTON */}
              <button
                type="button"
                onClick={() => {
                  window.scrollTo({ top: 0, left: 0, behavior: "instant" });
                  const mainEl = document.getElementById("main-content");
                  if (mainEl) mainEl.scrollTop = 0;
                  const workspaceEl = document.querySelector(".shell-workspace");
                  if (workspaceEl) workspaceEl.scrollTop = 0;
                  if (onCompete) onCompete();
                }}
                className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-cyan-600 to-sky-600 hover:from-cyan-500 hover:to-sky-500 text-white font-bold py-3.5 px-4 text-xs sm:text-sm shadow-md shadow-cyan-600/25 active:scale-[0.98] transition group cursor-pointer"
                title="Enter Compete Arena"
              >
                <Swords size={17} className="transition-transform group-hover:rotate-12" />
                <span>Enter Compete Arena</span>
                <ArrowRight size={16} className="transition-transform group-hover:translate-x-0.5" />
              </button>

              {/* SECONDARY LEADERBOARD BUTTON */}
              <button
                type="button"
                onClick={() => {
                  window.scrollTo({ top: 0, left: 0, behavior: "instant" });
                  const mainEl = document.getElementById("main-content");
                  if (mainEl) mainEl.scrollTop = 0;
                  const workspaceEl = document.querySelector(".shell-workspace");
                  if (workspaceEl) workspaceEl.scrollTop = 0;
                  if (onLeaderboard) onLeaderboard();
                }}
                className="w-full inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 dark:border-neutral-800 bg-white/80 dark:bg-neutral-900 hover:bg-slate-50 dark:hover:bg-neutral-800 text-slate-700 dark:text-neutral-200 text-xs font-semibold py-2.5 px-3 transition cursor-pointer"
              >
                <Trophy size={14} className="text-amber-500" />
                <span>View National Leaderboard</span>
              </button>
            </div>
          </div>
        </div>

      </div>
    </section>
  );
}
