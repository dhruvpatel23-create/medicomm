import { useState } from 'react';

const questions = [
  { prompt: 'An increase in cell size is called:', options: ['Hypertrophy', 'Hyperplasia', 'Metaplasia'], answer: 0, note: 'Hypertrophy increases cell size; hyperplasia increases cell number.' },
  { prompt: 'Programmed cell death is called:', options: ['Necrosis', 'Apoptosis', 'Atrophy'], answer: 1, note: 'Apoptosis is a regulated process of cell death.' },
  { prompt: 'Replacement of one mature cell type by another is:', options: ['Dysplasia', 'Hypertrophy', 'Metaplasia'], answer: 2, note: 'Metaplasia is a change from one differentiated cell type to another.' },
];

export default function AuthPracticePreview({ onExplore }) {
  const [index, setIndex] = useState(0);
  const [choice, setChoice] = useState(null);
  const q = questions[index];
  const answered = index + (choice !== null ? 1 : 0);
  return <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-5 text-slate-900 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100" aria-label="Interactive practice preview">
    <div className="flex items-center justify-between gap-3 text-xs font-medium"><span className="text-slate-500 dark:text-slate-400">PRACTICE PREVIEW</span><span>{answered} of 3 answered</span></div>
    <div className="my-4 h-1.5 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800" role="progressbar" aria-label="Preview progress" aria-valuemin={0} aria-valuemax={3} aria-valuenow={answered}>
      <div className="h-full rounded-full bg-teal-600 transition-[width] motion-reduce:transition-none" style={{ width: `${answered / 3 * 100}%` }} />
    </div>
    <p className="!m-0 !text-sm !font-medium !leading-6 !text-inherit">{q.prompt}</p>
    <div className="mt-3 grid gap-2">{q.options.map((option, i) => <button key={`${index}-${i}`} type="button" disabled={choice !== null} onClick={() => setChoice(i)}
      className={`rounded-lg border px-3 py-2.5 text-left text-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 ${choice !== null && i === q.answer ? 'border-teal-600 bg-teal-50 text-teal-900 dark:bg-teal-950 dark:text-teal-100' : choice === i ? 'border-rose-400 bg-rose-50 text-rose-900 dark:bg-rose-950 dark:text-rose-100' : 'border-slate-200 hover:border-slate-400 dark:border-slate-700'}`}>
      {option}{choice !== null && i === q.answer ? ' · Correct' : choice === i ? ' · Your answer' : ''}
    </button>)}</div>
    <div className="mt-3 text-xs leading-5 text-slate-500 dark:text-slate-400" aria-live="polite">{choice !== null ? q.note : 'Try a question. Preview answers are not saved.'}</div>
    <div className="mt-4 flex items-center justify-between border-t border-slate-200 pt-4 dark:border-slate-700"><span className="text-xs text-slate-500">Pathology · Cell adaptations</span>
      <button type="button" disabled={choice === null} className="rounded px-2 py-1 text-sm font-semibold text-teal-700 focus-visible:ring-2 focus-visible:ring-teal-500 disabled:cursor-not-allowed disabled:opacity-40 dark:text-teal-400"
        onClick={() => { if (index < questions.length - 1) { setIndex(index + 1); setChoice(null); } else onExplore(); }}>
        {index === 2 && choice !== null ? 'Explore Medulla →' : 'Continue →'}
      </button>
    </div>
  </section>;
}
