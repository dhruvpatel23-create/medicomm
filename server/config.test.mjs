import test from 'node:test';
import assert from 'node:assert/strict';
import { deploymentConfig } from './config.mjs';

const render = {
  NODE_ENV: 'production',
  RENDER_EXTERNAL_URL: 'https://example.onrender.com',
  SUPABASE_URL: 'https://example.supabase.co',
  SUPABASE_SECRET_KEY: 'test-only-key',
};

test('existing Render services use the platform origin and private upload bucket default', () => {
  const config = deploymentConfig(render);
  assert.deepEqual([...config.allowedOrigins], [render.RENDER_EXTERNAL_URL, 'https://medullaprep.com', 'https://www.medullaprep.com']);
  assert.equal(config.uploadBucket, 'medicomm-uploads');
});

test('explicit custom domains and bucket take precedence over Render defaults', () => {
  const config = deploymentConfig({ ...render, APP_ORIGINS: 'https://app.example, https://www.example', SUPABASE_UPLOAD_BUCKET: 'custom-private' });
  assert.deepEqual([...config.allowedOrigins], ['https://app.example', 'https://www.example']);
  assert.equal(config.uploadBucket, 'custom-private');
});

test('Render defaults never permit missing database credentials or unsafe origins', () => {
  assert.throws(() => deploymentConfig({ ...render, SUPABASE_SECRET_KEY: '' }), /Supabase server key/);
  for (const APP_ORIGINS of ['http://app.example', '*', 'https://app.example/path', 'https://app.example/']) {
    assert.throws(() => deploymentConfig({ ...render, APP_ORIGINS }), /exact HTTPS origins/);
  }
});

test('production outside Render still requires explicit origin and upload configuration', () => {
  assert.throws(() => deploymentConfig({ ...render, RENDER_EXTERNAL_URL: '' }), /SUPABASE_UPLOAD_BUCKET.*APP_ORIGINS/);
  const config = deploymentConfig({ NODE_ENV: 'test' });
  assert.ok(config.allowedOrigins.has('http://localhost:4173'));
  assert.equal(config.uploadBucket, '');
});
