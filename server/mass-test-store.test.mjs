import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { promises as fs } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { createMassTestStore } from "./massTestStore.mjs";

test(
  "Windows lock-owner read retries a delete-pending file without losing the update",
  { skip: process.platform !== "win32" },
  async (t) => {
    const directory = await fs.mkdtemp(
      path.join(tmpdir(), "medulla-lock-test-"),
    );
    t.after(() => fs.rm(directory, { recursive: true, force: true }));
    const event = { id: "lock-test", eventId: "event" };
    const userId = "learner";
    const key = createHash("sha256")
      .update(JSON.stringify([event.id, event.eventId, userId]))
      .digest("hex");
    const lockPath = path.join(directory, `${key}.json.lock`);
    await fs.writeFile(lockPath, String(process.pid));
    const readFile = fs.readFile.bind(fs);
    let simulated = false;
    t.mock.method(fs, "readFile", async (file, ...options) => {
      if (file === lockPath && !simulated) {
        simulated = true;
        await fs.unlink(lockPath);
        throw Object.assign(new Error("delete pending"), { code: "EPERM" });
      }
      return readFile(file, ...options);
    });

    const store = createMassTestStore({ directory });
    const result = await store.transact(event, userId, (record) => {
      record.waitingJoinedAt = 123;
      return { changed: true, value: "saved" };
    });
    assert.equal(simulated, true);
    assert.equal(result, "saved");
    assert.equal((await store.get(event, userId)).waitingJoinedAt, 123);
    await assert.rejects(fs.access(lockPath), { code: "ENOENT" });
  },
);
