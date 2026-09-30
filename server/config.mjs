export function deploymentConfig(env = process.env) {
  const production = env.NODE_ENV === 'production';
  // Render provides this trusted service URL; never infer allowed origins from
  // incoming Host / Origin headers. Custom domains remain explicitly configured.
  const renderOrigin = env.RENDER_EXTERNAL_URL || '';
  const origins = env.APP_ORIGINS || renderOrigin || (production ? '' :
    'http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173,http://localhost:4174,http://127.0.0.1:4174');
  const allowedOrigins = new Set(origins.split(',').map(value => value.trim()).filter(Boolean));
  const uploadBucket = env.SUPABASE_UPLOAD_BUCKET || (renderOrigin ? 'medicomm-uploads' : '');
  const hasDatabase = Boolean(env.SUPABASE_URL &&
    (env.SUPABASE_SERVICE_ROLE_KEY || env.SUPABASE_SECRET_KEY || env.SUPABASE_SERVICE_KEY));
  if (production) {
    const missing = [];
    if (!hasDatabase) missing.push('SUPABASE_URL and a Supabase server key');
    if (!uploadBucket) missing.push('SUPABASE_UPLOAD_BUCKET');
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
  return { production, allowedOrigins, uploadBucket };
}
