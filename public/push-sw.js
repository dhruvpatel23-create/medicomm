self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => event.waitUntil(self.clients.claim()));
self.addEventListener('push', event => {
  let payload = {};
  try { payload = event.data?.json() || {}; } catch { /* Display a safe fallback. */ }
  event.waitUntil(self.registration.showNotification(payload.title || 'Medulla', {
    body: payload.body || 'You have a new update.', icon: '/icons/medulla-192.png',
    badge: '/icons/medulla-192.png', tag: payload.tag || 'medulla',
    renotify: false, data: { url: payload.url || '/' },
  }));
});
self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil((async () => {
    let target = new URL(event.notification.data?.url || '/', self.location.origin);
    if (target.origin !== self.location.origin) target = new URL('/', self.location.origin);
    const windows = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    for (const client of windows) {
      if (new URL(client.url).origin !== target.origin) continue;
      await client.navigate(target.href);
      await client.focus();
      return;
    }
    await self.clients.openWindow(target.href);
  })());
});
