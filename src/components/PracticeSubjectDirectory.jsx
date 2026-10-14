import { useId, useState } from "react";
import { ArrowLeft, ArrowRight, Search, X, Layers3, Microscope, Stethoscope, GraduationCap } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

const number = (value) => value.toLocaleString("en-IN");
const yearStyles = [
  { Icon: Layers3, icon: "bg-blue-100 text-blue-700 dark:bg-blue-400/10 dark:text-blue-300", line: "from-blue-500/70 via-sky-400/30 to-transparent", hover: "hover:border-blue-300 hover:shadow-blue-900/10 dark:hover:border-blue-500/50 dark:hover:shadow-blue-950/40" },
  { Icon: Microscope, icon: "bg-teal-100 text-teal-700 dark:bg-teal-400/10 dark:text-teal-300", line: "from-teal-500/70 via-emerald-400/30 to-transparent", hover: "hover:border-teal-300 hover:shadow-teal-900/10 dark:hover:border-teal-500/50 dark:hover:shadow-teal-950/40" },
  { Icon: Stethoscope, icon: "bg-violet-100 text-violet-700 dark:bg-violet-400/10 dark:text-violet-300", line: "from-violet-500/70 via-indigo-400/30 to-transparent", hover: "hover:border-violet-300 hover:shadow-violet-900/10 dark:hover:border-violet-500/50 dark:hover:shadow-violet-950/40" },
  { Icon: GraduationCap, icon: "bg-amber-100 text-amber-700 dark:bg-amber-400/10 dark:text-amber-300", line: "from-amber-500/70 via-orange-400/30 to-transparent", hover: "hover:border-amber-300 hover:shadow-amber-900/10 dark:hover:border-amber-500/50 dark:hover:shadow-amber-950/40" },
];

export default function PracticeSubjectDirectory({ years, onSelect, onBack }) {
  const [query, setQuery] = useState("");
  const [selectedYear, setSelectedYear] = useState("all");
  const headingId = useId();
  const reduceMotion = useReducedMotion();
  const entrance = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0, transition: { duration: reduceMotion ? 0 : 0.28, ease: "easeOut" } },
  };
  const groups = [
    ...years.map((year) => ({ ...year, subjects: year.subjects.map((subject) => ({
      ...subject, pyqCount: subject.questions.length,
    })).filter(subject => subject.pyqCount > 0) })),
  ].filter((group) => group.subjects.length);
  const subjects = groups.flatMap((group) => group.subjects);
  const normalizedQuery = query.trim().toLowerCase();
  const visibleGroups = groups
    .filter((group) => selectedYear === "all" || group.id === selectedYear)
    .map((group) => ({ ...group, subjects: group.subjects.filter((subject) => subject.title.toLowerCase().includes(normalizedQuery)) }))
    .filter((group) => group.subjects.length);
  const visibleCount = visibleGroups.reduce((count, group) => count + group.subjects.length, 0);
  const reset = () => { setQuery(""); setSelectedYear("all"); };

  return (
    <div className="text-slate-900 dark:text-slate-100" data-testid="practice-subject-directory">
      <header className="mb-8 sm:mb-10">
        <button type="button" onClick={onBack} className="mb-7 inline-flex min-h-10 items-center gap-2 rounded-md text-sm font-medium text-slate-500 transition-colors hover:text-slate-900 dark:text-slate-400 dark:hover:text-white">
          <ArrowLeft size={16} aria-hidden="true" /> All practice paths
        </button>
        <div className="relative isolate overflow-hidden rounded-2xl border border-slate-200/80 bg-gradient-to-br from-white via-blue-50/70 to-slate-100/80 p-5 shadow-[0_8px_32px_-16px_rgba(30,64,175,0.2)] sm:p-7 dark:border-slate-700/60 dark:from-slate-900 dark:via-slate-900 dark:to-blue-950/60 dark:shadow-[0_12px_36px_-16px_rgba(0,0,0,0.5)]">
        <span aria-hidden="true" className="pointer-events-none absolute -right-16 -top-28 -z-10 h-80 w-80 rounded-full bg-blue-400/10 blur-3xl dark:bg-blue-500/10" />
        <p className="m-0 text-xs font-semibold uppercase tracking-[0.14em] text-blue-700 dark:text-blue-400">NEET PG / INI-CET</p>
        <div className="mt-3 flex flex-col justify-between gap-6 xl:flex-row xl:items-end">
          <div>
            <h2 id={headingId} className="m-0 text-3xl font-semibold tracking-tight sm:text-4xl">Choose a subject</h2>
            <p className="mb-0 mt-3 max-w-xl text-sm leading-6 text-slate-600 dark:text-slate-400">Choose a subject and exam year to practise NEET PG and INI-CET previous year questions.</p>
          </div>
          <dl className="m-0 flex shrink-0 gap-3 rounded-xl border border-white/70 bg-white/50 px-3 py-3 shadow-sm sm:gap-7 sm:px-4 dark:border-slate-700/50 dark:bg-slate-950/30 dark:shadow-inner">
            {[
              ["Subjects", subjects.length],
              ["Previous year questions", subjects.reduce((sum, subject) => sum + subject.pyqCount, 0)],
            ].map(([label, value]) => (
              <div key={label} className="flex flex-col gap-1">
                <dd className="m-0 text-xl font-semibold tabular-nums tracking-tight sm:text-2xl">{number(value)}</dd>
                <dt className="max-w-28 text-xs leading-5 text-slate-500 dark:text-slate-400">{label}</dt>
              </div>
            ))}
          </dl>
        </div>
        </div>
      </header>

      <div className="mb-8 border-y border-slate-200 py-4 dark:border-slate-800">
        <div className="flex flex-col-reverse justify-between gap-4 xl:flex-row xl:items-center">
          <div className="flex gap-1 overflow-x-auto pb-1 xl:pb-0" role="group" aria-label="Filter subjects by year">
            {[{ id: "all", title: "All subjects" }, ...groups].map((group) => (
              <button key={group.id} type="button" aria-pressed={selectedYear === group.id} onClick={() => setSelectedYear(group.id)}
                className={`min-h-10 shrink-0 rounded-lg px-3 text-sm font-medium transition-all duration-200 motion-reduce:transition-none ${selectedYear === group.id ? "bg-gradient-to-b from-blue-600 to-blue-700 text-white shadow-md shadow-blue-600/20 ring-1 ring-inset ring-white/15 dark:from-blue-500 dark:to-blue-600 dark:text-white dark:shadow-blue-950/50" : "text-slate-600 hover:bg-slate-100 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-slate-100"}`}>
                {group.title}
              </button>
            ))}
          </div>
          <div className="relative w-full xl:w-64 xl:shrink-0">
            <Search size={17} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" aria-hidden="true" />
            <input aria-label="Search subjects" type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search subjects"
              className="h-11 w-full rounded-lg border border-slate-300 bg-white pl-10 pr-10 text-sm text-slate-900 placeholder:text-slate-500 focus:border-blue-500 dark:border-slate-700 dark:bg-slate-900 dark:text-white dark:placeholder:text-slate-400 [&::-webkit-search-cancel-button]:appearance-none" />
            {query && <button type="button" onClick={() => setQuery("")} aria-label="Clear search" className="absolute right-0 top-0 flex h-11 w-10 items-center justify-center rounded-r-lg text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"><X size={16} /></button>}
          </div>
        </div>
      </div>

      <div aria-live="polite" className="sr-only">{visibleCount} subjects shown</div>
      <div className="space-y-10" aria-labelledby={headingId}>
        {visibleGroups.map((group) => {
          const style = yearStyles[Math.max(0, groups.findIndex((item) => item.id === group.id)) % yearStyles.length];
          const Icon = style.Icon;
          return (
          <motion.section key={group.id} aria-label={group.title} initial={reduceMotion ? false : "hidden"} animate={reduceMotion ? "visible" : undefined} whileInView="visible" viewport={{ once: true, amount: 0.05 }} variants={{ visible: { transition: { staggerChildren: reduceMotion ? 0 : 0.045 } } }} className="grid gap-4 lg:grid-cols-[155px_minmax(0,1fr)] lg:gap-7">
            <div className="flex items-baseline justify-between gap-3 lg:block lg:pt-4">
              <div>
                <span className={`mb-3 flex h-10 w-10 items-center justify-center rounded-xl ring-1 ring-inset ring-black/5 dark:ring-white/5 ${style.icon}`}><Icon size={20} strokeWidth={1.7} aria-hidden="true" /></span>
                <h3 className="m-0 text-base font-semibold tracking-tight">{group.title}</h3>
                <p className="mb-0 mt-1 text-xs leading-5 text-slate-500 dark:text-slate-400">{group.subtitle}</p>
              </div>
              <span className="mt-3 shrink-0 text-xs tabular-nums text-slate-500 dark:text-slate-400">{group.subjects.length} {group.subjects.length === 1 ? "subject" : "subjects"}</span>
            </div>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
              {group.subjects.map((subject) => (
                <motion.button key={subject.id} type="button" onClick={() => onSelect(subject.id)} aria-label={`Practice ${subject.title}`} variants={entrance} whileHover={reduceMotion ? undefined : { y: -3 }} whileTap={reduceMotion ? undefined : { scale: 0.985 }}
                  className={`group relative flex min-h-28 min-w-0 flex-col justify-between gap-5 overflow-hidden rounded-xl border border-slate-200 bg-gradient-to-br from-white to-slate-50/90 p-4 text-left shadow-[0_2px_6px_-2px_rgba(15,23,42,0.08),0_12px_24px_-20px_rgba(15,23,42,0.18)] transition-[border-color,box-shadow] duration-200 hover:shadow-lg focus-visible:outline-blue-500 motion-reduce:transition-none sm:min-h-32 sm:p-5 dark:border-slate-700/70 dark:from-slate-800/80 dark:to-slate-900 dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.025),0_8px_20px_-12px_rgba(0,0,0,0.5)] ${style.hover}`}>
                  <span aria-hidden="true" className={`absolute inset-x-4 top-0 h-px bg-gradient-to-r ${style.line}`} />
                  <span className="flex w-full items-start justify-between gap-3">
                    <span className="text-[15px] font-semibold leading-6 text-slate-900 dark:text-slate-100">{subject.title}</span>
                    <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-slate-100 text-slate-400 transition-colors group-hover:bg-blue-100 group-hover:text-blue-600 dark:bg-slate-800 dark:text-slate-500 dark:group-hover:bg-blue-500/15 dark:group-hover:text-blue-300"><ArrowRight size={15} aria-hidden="true" className="transition-transform duration-200 motion-safe:group-hover:translate-x-0.5 motion-reduce:transition-none" /></span>
                  </span>
                  <span className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs leading-5 text-slate-500 dark:text-slate-400">
                    {subject.pyqCount > 0 && <span><span className="font-medium tabular-nums text-slate-700 dark:text-slate-300">{number(subject.pyqCount)}</span> PYQs</span>}
                  </span>
                </motion.button>
              ))}
            </div>
          </motion.section>
        );})}
        {!visibleCount && <div className="rounded-lg border border-dashed border-slate-300 px-6 py-14 text-center dark:border-slate-700">
          <h3 className="m-0 text-lg font-semibold">No subjects found</h3>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Try another subject name or view all years.</p>
          <button type="button" onClick={reset} className="mt-3 min-h-11 rounded-md bg-slate-900 px-4 text-sm font-medium text-white dark:bg-slate-200 dark:text-slate-950">Reset filters</button>
        </div>}
      </div>
    </div>
  );
}
