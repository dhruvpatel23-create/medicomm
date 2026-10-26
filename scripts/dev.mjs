import { spawn, spawnSync } from "node:child_process";
import { acquireDevLock } from './dev-lock.mjs';
import net from "node:net";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");
const windowsCommandShell = process.env.ComSpec || "C:\\Windows\\System32\\cmd.exe";

function isPortInUse(port) {
  return new Promise((resolve) => {
    // A slow first page load still means the port is occupied. Do not launch a
    // second frontend that could fall back onto the API's port.
    const socket = net.createConnection({ host: "127.0.0.1", port });
    const finish = (inUse) => { socket.destroy(); resolve(inUse); };
    socket.setTimeout(1000);
    socket.once("connect", () => finish(true));
    socket.once("error", () => finish(false));
    socket.once("timeout", () => finish(true));
  });
}

function spawnClient() {
  return process.platform === "win32"
    ? spawn(windowsCommandShell, ["/d", "/s", "/c", "npm run client -- --host 127.0.0.1 --port 4173"], {
        cwd: rootDir,
        stdio: "inherit",
      })
    : spawn("npm", ["run", "client", "--", "--host", "127.0.0.1", "--port", "4173"], {
        cwd: rootDir,
        stdio: "inherit",
      });
}

let serverProcess = null;
let clientProcess = null;
let shuttingDown = false;

function stopChild(child) {
  if (!child || child.exitCode !== null || child.killed) return;
  if (process.platform === 'win32') {
    // Killing only cmd.exe or the watch supervisor leaves its Node children
    // listening on the same ports after Ctrl+C on Windows.
    spawnSync('taskkill', ['/PID', String(child.pid), '/T', '/F'], { stdio: 'ignore', windowsHide: true });
  } else child.kill();
}

function shutdown(exitCode = 0) {
  if (shuttingDown) return;
  shuttingDown = true;
  stopChild(serverProcess);
  stopChild(clientProcess);
  process.exit(exitCode);
}

async function main() {
  const release = acquireDevLock(path.join(rootDir, '.tmp', 'medulla-dev.lock'));
  if (!release) {
    console.log('Medulla development is already running. Open http://127.0.0.1:4173, or stop the original terminal with Ctrl+C before restarting.');
    return;
  }
  process.once('exit', release);
  const hasExistingServer = await isPortInUse(4174);
  const hasExistingClient = await isPortInUse(4173);

  if (!hasExistingServer) {
    serverProcess = spawn(process.execPath, ["--watch", "server.mjs"], {
      cwd: rootDir,
      stdio: "inherit",
    });
    serverProcess.on('error', error => { console.error('Could not start the API:', error.message); shutdown(1); });

    serverProcess.on("exit", (code) => {
      if (code && code !== 0) shutdown(code);
    });
  } else {
    console.log("Reusing existing local API on http://127.0.0.1:4174");
  }

  if (!hasExistingClient) {
    clientProcess = spawnClient();
    clientProcess.on('error', error => { console.error('Could not start Vite:', error.message); shutdown(1); });
    clientProcess.on("exit", (code) => {
      if (code && code !== 0) shutdown(code);
    });
  } else {
    console.log("Reusing existing Vite client on http://127.0.0.1:4173");
  }

  if (!serverProcess && !clientProcess) {
    console.log("Both local services are already running.");
  }
}

process.on("SIGINT", () => shutdown(0));
process.on("SIGTERM", () => shutdown(0));

await main();
