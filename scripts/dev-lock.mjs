import { closeSync, mkdirSync, openSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import path from 'node:path';

function isAlive(pid) {
  try { process.kill(pid, 0); return true; }
  catch (error) { return error.code !== 'ESRCH'; }
}

// Acquire before checking HTTP ports: database initialization and watch restarts
// can leave the API port temporarily free while a launcher still owns it.
export function acquireDevLock(file, { pid = process.pid, alive = isAlive } = {}) {
  mkdirSync(path.dirname(file), { recursive: true });
  for (let attempt = 0; attempt < 3; attempt++) {
    let descriptor;
    try {
      descriptor = openSync(file, 'wx');
      writeFileSync(descriptor, String(pid));
      closeSync(descriptor);
      return () => {
        try { if (readFileSync(file, 'utf8') === String(pid)) unlinkSync(file); }
        catch (error) { if (error.code !== 'ENOENT') console.warn('Could not release development lock:', error.code); }
      };
    } catch (error) {
      if (descriptor !== undefined) closeSync(descriptor);
      if (error.code !== 'EEXIST') throw error;
      let owner;
      try { owner = Number(readFileSync(file, 'utf8')); }
      catch (error) { if (error.code === 'ENOENT') continue; throw error; }
      // An empty file may be another launcher still writing its PID.
      if (!Number.isSafeInteger(owner) || owner <= 0 || alive(owner)) return null;
      try { unlinkSync(file); } catch (error) { if (error.code !== 'ENOENT') throw error; }
    }
  }
  return null;
}
