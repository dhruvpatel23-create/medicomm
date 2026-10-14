import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import AnswerNotepad from '../src/components/AnswerNotepad.jsx';
import ShortNotes from '../src/components/ShortNotes.jsx';
import '../src/styles.css';

function Harness() {
  const [question, setQuestion] = useState('gesture-test');
  const prepareImage = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve({ dataUrl: reader.result, name: file.name });
    reader.onerror = reject; reader.readAsDataURL(file);
  });
  if (new URLSearchParams(location.search).has('review')) return <ShortNotes subjectId="anatomy" subjectTitle="Anatomy" userId="gesture-user" prepareImage={prepareImage} onBack={() => {}} onNavigate={() => {}} />;
  return <>
    <button onClick={() => setQuestion('gesture-test')}>Question one</button>
    <button onClick={() => setQuestion('other-question')}>Question two</button>
    <AnswerNotepad key={question} draftId={question} prompt={question} onSave={() => {}} />
  </>;
}

createRoot(document.getElementById('root')).render(<Harness />);
