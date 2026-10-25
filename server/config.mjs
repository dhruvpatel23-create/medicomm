export function deploymentConfig(env = process.env) {
  const production = env.NODE_ENV === 'production';
  const databaseProvider = env.DATABASE_PROVIDER || (env.SUPABASE_URL ? 'supabase' : 'local');
  if (!['supabase', 'firebase', 'local'].includes(databaseProvider)) throw new Error('Invalid DATABASE_PROVIDER.');
  // Render provides this trusted service URL; never infer allowed origins from
  // incoming Host / Origin headers. Include this app's known public domains.
  const renderOrigin = env.RENDER_EXTERNAL_URL || '';
  const renderOrigins = renderOrigin ?
    [renderOrigin, 'https://medullaprep.com', 'https://www.medullaprep.com'].join(',') : '';
  const origins = env.APP_ORIGINS || renderOrigins || (production ? '' :
    'http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173,http://localhost:4174,http://127.0.0.1:4174');
  const allowedOrigins = new Set(origins.split(',').map(value => value.trim()).filter(Boolean));
  const uploadStorage = databaseProvider === 'firebase' ? (env.UPLOAD_STORAGE || 'local') : 'supabase';
  if (!['local', 'firebase', 'supabase'].includes(uploadStorage)) throw new Error('Invalid UPLOAD_STORAGE.');
  const uploadBucket = databaseProvider === 'firebase'
    ? (uploadStorage === 'firebase' ? env.FIREBASE_STORAGE_BUCKET || '' : '')
    : env.SUPABASE_UPLOAD_BUCKET || (renderOrigin ? 'medicomm-uploads' : '');
  const hasDatabase = databaseProvider === 'firebase' ? Boolean(env.FIREBASE_PROJECT_ID) : databaseProvider === 'supabase' && Boolean(env.SUPABASE_URL &&
    (env.SUPABASE_SERVICE_ROLE_KEY || env.SUPABASE_SECRET_KEY || env.SUPABASE_SERVICE_KEY));
  if (production) {
    const missing = [];
    if (!hasDatabase) missing.push(databaseProvider === 'firebase' ? 'FIREBASE_PROJECT_ID' : 'SUPABASE_URL and a Supabase server key');
    if (databaseProvider === 'firebase') {
      if (!['local', 'firebase'].includes(env.UPLOAD_STORAGE)) missing.push('UPLOAD_STORAGE (local or firebase)');
      if (uploadStorage === 'local' && !env.RUNTIME_DATA_DIR) missing.push('RUNTIME_DATA_DIR for persistent private uploads');
      if (uploadStorage === 'firebase' && !uploadBucket) missing.push('FIREBASE_STORAGE_BUCKET');
    } else if (!uploadBucket) missing.push('SUPABASE_UPLOAD_BUCKET');
    if (!allowedOrigins.size) missing.push('APP_ORIGINS (or Render RENDER_EXTERNAL_URL)');
    if (missing.length) throw new Error(`Missing production configuration: ${missing.join('; ')}.`);
  }
  for (const origin of allowedOrigins) {
    let parsed;
    try { parsed = new URL(origin); } catch { /* Report configuration, not the value. */ }
    if (!parsed || parsed.origin !== origin || !['http:', 'https:'].includes(parsed.protocol) ||
        (production && parsed.protocol !== 'https:')) {
      throw new Error('APP_ORIGINS / RENDER_EXTERNAL_URL must contain exact HTTPS origins in production (no path or trailing slash).');
    }
  }
  return { production, allowedOrigins, uploadBucket, databaseProvider, uploadStorage };
}
