import * as Tabs from "@radix-ui/react-tabs";
import FmgePracticeTests from './FmgePracticeTests';
import { useCallback, useState } from 'react';

const testTypes = [
  { id: "practice", title: "Practice Tests" },
  { id: "grand", title: "Grand Tests" },
];

export default function TestSections({ title, onBack, exam, onSessionChange }) {
  const [inSession, setInSession] = useState(false);
  const sessionChanged = useCallback(value => { setInSession(value); onSessionChange?.(value); }, [onSessionChange]);
  return <section className="app-view" aria-labelledby="practice-tests-title">
    <div className="view-header" style={inSession ? { display: 'none' } : undefined}>
      <h2 id="practice-tests-title">{title}</h2>
      <button type="button" className="button button-secondary" onClick={onBack}>
        Back to Practice
      </button>
    </div>
    <Tabs.Root defaultValue="practice">
      <Tabs.List className="test-section-tabs" style={inSession ? { display: 'none' } : undefined} aria-label={`${title} categories`}>
        {testTypes.map(type => <Tabs.Trigger key={type.id} value={type.id} className="test-section-tab">{type.title}</Tabs.Trigger>)}
      </Tabs.List>
      <Tabs.Content value="practice" className="test-section-content">
        {exam === 'fmge' ? <FmgePracticeTests onSessionChange={sessionChanged} /> : <div className="test-card-stack">
          {[1, 2, 3].map(number => <article className="exam-test-card" key={number}>
            <span className="exam-test-number" aria-hidden="true">0{number}</span>
            <div className="exam-test-copy">
              <p className="exam-test-label">Practice test</p>
              <h3>TEST{number}</h3>
            </div>
          </article>)}
        </div>}
      </Tabs.Content>
      <Tabs.Content value="grand" className="test-section-content">
        <div className="test-card-stack">
          <article className="exam-test-card exam-test-card-grand">
            <span className="exam-test-number" aria-hidden="true">01</span>
            <div className="exam-test-copy">
              <p className="exam-test-label">Grand test</p>
              <h3>GRAND TEST 1</h3>
            </div>
            <div className="exam-test-date">
              <span>Scheduled date</span>
              <time dateTime="2026-10-27T14:00:00+05:30">27/10/2026 · 2:00 pm IST</time>
            </div>
          </article>
        </div>
      </Tabs.Content>
    </Tabs.Root>
  </section>;
}
