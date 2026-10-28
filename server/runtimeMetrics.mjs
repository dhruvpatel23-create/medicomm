import { monitorEventLoopDelay, performance } from 'node:perf_hooks';

// Structured logs let operators distinguish CPU/event-loop stalls from slow I/O.
export function startRuntimeMetrics({ intervalMs = 30000, log = console.log } = {}) {
  const delay = monitorEventLoopDelay({ resolution: 20 });
  delay.enable();
  let previousCpu = process.cpuUsage(), previousTime = performance.now();
  const timer = setInterval(() => {
    const time = performance.now(), cpu = process.cpuUsage();
    const elapsed = time - previousTime, memory = process.memoryUsage();
    log(JSON.stringify({ event: 'process_metrics', pid: process.pid,
      rssMb: Math.round(memory.rss / 1048576), heapUsedMb: Math.round(memory.heapUsed / 1048576),
      cpuPercent: Math.round((cpu.user + cpu.system - previousCpu.user - previousCpu.system) / (elapsed * 10)),
      eventLoopP99Ms: Math.round(delay.percentile(99) / 1e6), eventLoopMaxMs: Math.round(delay.max / 1e6) }));
    previousCpu = cpu; previousTime = time; delay.reset();
  }, intervalMs);
  timer.unref();
  return () => { clearInterval(timer); delay.disable(); };
}
