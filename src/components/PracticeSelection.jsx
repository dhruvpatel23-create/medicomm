import { ArrowRight, BookOpen, Globe2, GraduationCap, ListTree, SlidersHorizontal, Stethoscope } from "lucide-react";

const practicePaths = [
  { id: "neet", title: "NEET PG / INICET", label: "Postgraduate entrance", description: "Build confidence for your next chapter in medicine.", icon: Stethoscope, color: "blue" },
  { id: "fmge", title: "FMGE", label: "Medical licensing", description: "Strengthen your foundations, one practice session at a time.", icon: GraduationCap, color: "teal" },
  { id: "theory", title: "THEORY", label: "Concepts & revision", description: "Deepen your understanding and connect the essentials.", icon: BookOpen, color: "violet" },
  { id: "usmle", title: "USMLE–STEP 1", label: "Your global pathway", description: "Make time for the core science behind clinical medicine.", icon: Globe2, color: "red" },
  { id: "topic-wise", title: "TOPIC WISE questions", label: "Focused revision", description: "Strengthen your understanding, one topic at a time.", icon: ListTree, color: "teal", standaloneTitle: true },
  { id: "custom-modules", title: "CUSTOM MODULES", label: "Your practice, your way", description: "Shape your practice around your learning goals.", icon: SlidersHorizontal, color: "violet", standaloneTitle: true },
];

export default function PracticeSelection({ onSelect }) {
  return (
    <section className="app-view practice-selection" aria-labelledby="practice-selection-title">
      <header className="practice-selection-heading">
        <p className="eyebrow">Practice • Your next step</p>
        <h2 id="practice-selection-title">What are you preparing for?</h2>
        <p>Choose your focus and make every practice session count.</p>
      </header>
      <div className="practice-path-grid">
        {practicePaths.map(({ id, title, label, description, icon: Icon, color, standaloneTitle }, index) => (
          <button key={id} type="button" className={`practice-path-card practice-path-${color}`} onClick={() => onSelect(title, id)}>
            <span className="practice-path-top"><span className="practice-path-icon"><Icon size={27} strokeWidth={1.7} aria-hidden="true" /></span><span className="practice-path-number" aria-hidden="true">0{index + 1}</span></span>
            <span className="practice-path-label">{label}</span>
            <span className="practice-path-title">{title}{!standaloneTitle && <> <span>practice</span></>}</span>
            <span className="practice-path-description">{description}</span>
            <span className="practice-path-action">Explore practice <ArrowRight size={18} aria-hidden="true" /></span>
          </button>
        ))}
      </div>
    </section>
  );
}
