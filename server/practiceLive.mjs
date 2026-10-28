import { practiceProgressData } from './dashboard.mjs';

// Publish only committed account state. Reconnecting clients receive a full snapshot.
export function createPracticeLive({ readDatabase, getSessionUser, sanitizeUser, heartbeatMs = 25000 }) {
  const clients = new Set();
  function send(client, database) {
    try {
      const user = getSessionUser(client.request, database);
      if (!user || user.id !== client.userId) { client.close(); return; }
      if (client.blockedAt) {
        if (Date.now() - client.blockedAt > 60000) client.close();
        return;
      }
      const payload = JSON.stringify({ user: sanitizeUser(user), progress: practiceProgressData(database, user.id) });
      if (payload !== client.last) {
        client.last = payload;
        if (!client.response.write(`event: account\ndata: ${payload}\n\n`)) client.blockedAt = Date.now();
      }
    } catch { client.close(); }
  }
  return {
    connect(request, response, user) {
      response.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache, no-transform',
        Connection: 'keep-alive', 'X-Accel-Buffering': 'no' });
      response.flushHeaders?.();
      const client = { request, response, userId: user.id, last: null };
      let timer;
      client.close = () => { clearInterval(timer); clients.delete(client); response.end(); };
      response.once('close', () => { clearInterval(timer); clients.delete(client); });
      response.on('drain', () => { client.blockedAt = null; });
      clients.add(client);
      timer = setInterval(() => {
        try { send(client, readDatabase()); if (clients.has(client) && !client.blockedAt && !response.write(': keep-alive\n\n')) client.blockedAt = Date.now(); }
        catch { client.close(); }
      }, heartbeatMs);
      timer.unref?.();
      send(client, readDatabase());
    },
    publish(database) {
      if (!clients.size) return;
      const snapshot = typeof database === 'function' ? database() : database;
      for (const client of clients) send(client, snapshot);
    },
  };
}
