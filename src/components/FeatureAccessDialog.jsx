import { LockKeyhole } from 'lucide-react';
import { Dialog, DialogContent, DialogDescription, DialogTitle } from './ui/dialog';
import { FEATURE_NAMES, requiredPlans } from '../data/planAccess';
import { UNIVERSITY_PREP_SAMPLE_LIMIT } from '../data/universityPrep';

export default function FeatureAccessDialog({ feature, onClose, onPlans }) {
  const isUniversityPrep = feature === 'universityPrep';
  return <Dialog open={Boolean(feature)} onOpenChange={open => { if (!open) onClose(); }}>
    <DialogContent>
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-sky-100 text-sky-700 dark:bg-sky-950 dark:text-sky-300"><LockKeyhole size={24} aria-hidden="true" /></div>
      <DialogTitle>{isUniversityPrep ? 'Unlock all short notes' : `Unlock ${FEATURE_NAMES[feature] || 'this feature'}`}</DialogTitle>
      <DialogDescription>{isUniversityPrep
        ? `You can open ${UNIVERSITY_PREP_SAMPLE_LIMIT} free samples per subject. Buy a subscription to unlock the rest of University Prep.`
        : `This feature is included with ${requiredPlans(feature)}. Choose a plan to get access, or keep exploring the available features.`}</DialogDescription>
      <div className="mt-5 flex flex-wrap gap-3">
        <button type="button" className="button button-primary" onClick={onPlans}>{isUniversityPrep ? 'View subscription plans' : 'View Plans'}</button>
        <button type="button" className="button button-secondary" onClick={onClose}>Keep Exploring</button>
      </div>
    </DialogContent>
  </Dialog>;
}
