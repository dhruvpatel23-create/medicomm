import { spawn } from "node:child_process";
import http from "node:http";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");
const windowsCommandShell = process.env.ComSpec || "C:\\Windows\\System32\\cmd.exe";

function isPortResponsive(port) {
  return new Promise((resolve) => {
    const request = http.get(
      {
        host: "127.0.0.1",
        port,
        path: "/",
        timeout: 1000,
      },
      () => {
        request.destroy();
        resolve(true);
      },
    );

    request.on("error", () => resolve(false));
    request.on("timeout", () => {
      request.destroy();
      resolve(false);
    });
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

function shutdown(exitCode = 0) {
  if (serverProcess && !serverProcess.killed) serverProcess.kill();
  if (clientProcess && !clientProcess.killed) clientProcess.kill();
  process.exit(exitCode);
}

async function main() {
  const hasExistingServer = await isPortResponsive(4174);
  const hasExistingClient = await isPortResponsive(4173);

  if (!hasExistingServer) {
    serverProcess = spawn("node", ["server.mjs"], {
      cwd: rootDir,
      stdio: "inherit",
    });

    serverProcess.on("exit", (code) => {
      if (code && code !== 0) shutdown(code);
    });
  } else {
    console.log("Reusing existing local API on http://127.0.0.1:4174");
  }

  if (!hasExistingClient) {
    clientProcess = spawnClient();
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
