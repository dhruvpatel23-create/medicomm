import { open } from 'node:fs/promises';
import { pipeline } from 'node:stream/promises';

// Open asynchronously and stream with backpressure instead of blocking all
// requests while reading a multi-megabyte image into memory.
export async function servePublicImage(request, response, candidates, mimeType) {
  let file;
  let filePath;
  for (const candidate of candidates) {
    try {
      file = await open(candidate, 'r');
      filePath = candidate;
      break;
    } catch (error) {
      if (error.code !== 'ENOENT' && error.code !== 'ENOTDIR') throw error;
    }
  }
  if (!file) {
    response.writeHead(404);
    response.end('Not found');
    return;
  }
  try {
    const stat = await file.stat();
    const etag = `W/"${stat.size.toString(16)}-${stat.mtimeMs.toString(16)}"`;
    const headers = {
      'Content-Type': mimeType(filePath),
      // Filenames can be reused when an illustration is corrected.
      'Cache-Control': 'public, max-age=3600, must-revalidate',
      'ETag': etag,
      'Last-Modified': stat.mtime.toUTCString(),
    };
    const match = request.headers['if-none-match'];
    const unchanged = match
      ? match.split(',').some(value => value.trim() === '*' || value.trim().replace(/^W\//, '') === etag.replace(/^W\//, ''))
      : request.headers['if-modified-since'] && Math.floor(stat.mtimeMs / 1000) <= Math.floor(Date.parse(request.headers['if-modified-since']) / 1000);
    if (unchanged) {
      response.writeHead(304, headers);
      response.end();
      return;
    }
    response.writeHead(200, { ...headers, 'Content-Length': stat.size });
    if (request.method === 'HEAD') response.end();
    else await pipeline(file.createReadStream({ autoClose: false }), response);
  } finally {
    await file.close();
  }
}
