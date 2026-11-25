import {
  Activity, ArrowUpRight, Baby, Bone, Ear, Eye, FlaskConical,
  GraduationCap, HeartPulse, PersonStanding, Scissors, Stethoscope,
} from "lucide-react";
import { UNIVERSITY_PREP_SAMPLE_LIMIT, UNIVERSITY_PREP_SUBJECTS } from "../data/universityPrep";
import "./university-prep.css";

const subjectIcons = {
  anatomy: PersonStanding,
  physiology: Activity,
  biochemistry: FlaskConical,
  "general-medicine": Stethoscope,
  "general-surgery": Scissors,
  obgyn: HeartPulse,
  pediatrics: Baby,
  orthopedics: Bone,
  ent: Ear,
  ophthalmology: Eye,
};

export default function UniversityPrep({ subscribed, onSelectSubject }) {
  return (
    <section className="university-prep" aria-labelledby="university-prep-title">
      <header className="university-prep-header">
        <span className="university-prep-icon"><GraduationCap size={24} aria-hidden="true" /></span>
        <div>
          <h2 id="university-prep-title">UNIVERSITY PREP</h2>
          <p>Short notes and handwritten model answers for MBBS theory exams.</p>
        </div>
        {!subscribed && <span className="university-prep-samples">{UNIVERSITY_PREP_SAMPLE_LIMIT} free samples per subject</span>}
      </header>
      <ul className="university-prep-grid">
        {UNIVERSITY_PREP_SUBJECTS.map(subject => {
          const Icon = subjectIcons[subject.id];
          return (
            <li key={subject.id}>
              <button className="university-prep-subject" type="button" onClick={() => onSelectSubject(subject)}>
                <span className="university-prep-subject-icon"><Icon size={19} aria-hidden="true" /></span>
                <span>{subject.title}</span>
                <ArrowUpRight className="university-prep-arrow" size={16} aria-hidden="true" />
              </button>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
