// Schedule the next refresh after the previous request settles. Hidden tabs
// pause completely and refresh immediately when the user returns.
export function startVisiblePolling(task, intervalMs) {
  let stopped = false;
  let running = false;
  let timer;

  const run = async () => {
    if (stopped || running || document.hidden) return;
    running = true;
    try {
      await task();
    } catch {
      // Callers own their error UI; one failure must not stop future refreshes.
    } finally {
      running = false;
      if (!stopped && !document.hidden)
        timer = window.setTimeout(run, intervalMs);
    }
  };

  const onVisibilityChange = () => {
    window.clearTimeout(timer);
    if (!document.hidden) void run();
  };

  document.addEventListener("visibilitychange", onVisibilityChange);
  void run();

  return () => {
    stopped = true;
    window.clearTimeout(timer);
    document.removeEventListener("visibilitychange", onVisibilityChange);
  };
}
