import { useEffect, useState } from 'react';
import { Zap } from 'lucide-react';

export function TokenBalance({ user }) {
  const [tokens, setTokens] = useState(null);
  useEffect(() => {
    let active = true;
    let pending = false;
    setTokens(user?.tokens ?? null);
    if (!user?.id) return;
    const refresh = async () => {
      if (pending || document.hidden) return;
      pending = true;
      try {
        const response = await fetch('/api/tokens', { credentials: 'same-origin', cache: 'no-store' });
        if (response.ok) {
          const data = await response.json();
          if (active) setTokens(data.tokens);
        }
      } catch { /* Keep the last confirmed balance while offline. */ }
      finally { pending = false; }
    };
    refresh();
    const interval = window.setInterval(refresh, 15000);
    window.addEventListener('tokens-changed', refresh);
    window.addEventListener('focus', refresh);
    document.addEventListener('visibilitychange', refresh);
    return () => {
      active = false;
      window.clearInterval(interval);
      window.removeEventListener('tokens-changed', refresh);
      window.removeEventListener('focus', refresh);
      document.removeEventListener('visibilitychange', refresh);
    };
  }, [user?.id, user?.plan]);
  const reset = tokens?.resetsAt ? `Resets ${new Date(tokens.resetsAt).toLocaleString()}.` : 'Your 24-hour reset timer starts with first use.';
  return <div className="topbar-stat topbar-token-balance" title={`${tokens?.allowance ?? 20} tokens per 24 hours. ${reset} Battles: 5. Theory reviews: 10. Clinical cases: 10 each.`} aria-live="polite">
    <Zap size={16} /><strong>{tokens?.remaining ?? (user?.id ? '—' : 20)}</strong><span>tokens</span>
  </div>;
}
