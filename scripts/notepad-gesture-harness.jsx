import React from 'react';
import { createRoot } from 'react-dom/client';
import AnswerNotepad from '../src/components/AnswerNotepad.jsx';
import '../src/styles.css';

createRoot(document.getElementById('root')).render(
  <AnswerNotepad draftId="gesture-test" prompt="Gesture test" onSave={() => {}} />,
);
