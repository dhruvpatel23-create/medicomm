export function publicGoogleConfig(value, projectId) {
  if (value?.projectId !== projectId || !/^AIza[A-Za-z0-9_-]{20,}$/.test(value.apiKey || '') ||
      !/^1:\d+:web:[a-f0-9]+$/i.test(value.appId || '') ||
      !/^[a-z0-9][a-z0-9.-]+$/i.test(value.authDomain || '')) throw new Error('Invalid Firebase web configuration.');
  return { apiKey: value.apiKey, authDomain: value.authDomain, projectId, appId: value.appId };
}

export async function discoverGoogleConfig(firebase, env = process.env, fetchImpl = fetch) {
  if (!firebase) return null;
  const { projectId } = firebase;
  if (env.FIREBASE_WEB_API_KEY && env.FIREBASE_WEB_APP_ID) return publicGoogleConfig({
    apiKey: env.FIREBASE_WEB_API_KEY, appId: env.FIREBASE_WEB_APP_ID,
    authDomain: env.FIREBASE_AUTH_DOMAIN || `${projectId}.firebaseapp.com`, projectId,
  }, projectId);
  const { access_token } = await firebase.app.options.credential.getAccessToken();
  const request = async resource => {
    const r = await fetchImpl(`https://firebase.googleapis.com/v1beta1/${resource}`, {
      headers: { Authorization: `Bearer ${access_token}` }, signal: AbortSignal.timeout(15000),
    });
    if (!r.ok) throw new Error('Firebase web configuration is unavailable.');
    return r.json();
  };
  let appId = env.FIREBASE_WEB_APP_ID;
  if (!appId) {
    const result = await request(`projects/${encodeURIComponent(projectId)}/webApps`);
    const apps = result.apps || [];
    if (apps.length !== 1) throw new Error('Set FIREBASE_WEB_APP_ID to choose the registered web app.');
    appId = apps[0].appId;
  }
  return publicGoogleConfig(await request(`projects/${encodeURIComponent(projectId)}/webApps/${encodeURIComponent(appId)}/config`), projectId);
}
