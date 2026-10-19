// Keep readable page dimensions; never chase a byte target by progressively
// lowering quality. Prefer lossless PNG when lossy encoding saves very little.
export function imageBytes(dataUrl) {
  const base64 = dataUrl.split(',')[1] || '';
  return Math.floor(base64.length * 3 / 4) - (base64.endsWith('==') ? 2 : base64.endsWith('=') ? 1 : 0);
}

export function encodeTheoryPage(canvas, original = null) {
  const png = canvas.toDataURL('image/png');
  let best = png;
  for (const type of ['image/webp', 'image/jpeg']) {
    const candidate = canvas.toDataURL(type, 0.94);
    if (candidate.startsWith(`data:${type};`) && imageBytes(candidate) < imageBytes(best)) best = candidate;
  }
  // Small savings do not justify losing any detail from a clean ink drawing.
  if (imageBytes(best) > imageBytes(png) * 0.9) best = png;
  if (original && /^data:image\/(png|jpeg|webp);base64,/.test(original)
    && imageBytes(original) <= 5 * 1024 * 1024 && imageBytes(original) <= imageBytes(best) * 1.1) best = original;
  return { dataUrl: best, bytes: imageBytes(best), width: canvas.width, height: canvas.height,
    extension: best.startsWith('data:image/webp') ? 'webp' : best.startsWith('data:image/jpeg') ? 'jpg' : 'png' };
}

export async function prepareTheoryImage(file) {
  if (!file.type.startsWith('image/')) throw new Error('Choose a photo of your written answer.');
  if (file.size > 12 * 1024 * 1024) throw new Error('Choose an image smaller than 12 MB.');
  const url = URL.createObjectURL(file);
  try {
    const image = await new Promise((resolve, reject) => {
      const value = new Image();
      value.onload = () => resolve(value);
      value.onerror = () => reject(new Error('This image could not be opened. Try JPG, PNG, or WebP.'));
      value.src = url;
    });
    if (!image.naturalWidth || !image.naturalHeight || image.naturalWidth * image.naturalHeight > 60000000) {
      throw new Error('This photo is too large to prepare. Crop it to the answer page first.');
    }
    const scale = Math.min(1, 2560 / Math.max(image.naturalWidth, image.naturalHeight));
    const canvas = document.createElement('canvas');
    canvas.width = Math.max(1, Math.round(image.naturalWidth * scale));
    canvas.height = Math.max(1, Math.round(image.naturalHeight * scale));
    const context = canvas.getContext('2d');
    if (!context) throw new Error('This device could not prepare the image.');
    context.fillStyle = '#fff'; context.fillRect(0, 0, canvas.width, canvas.height);
    context.imageSmoothingQuality = 'high';
    context.drawImage(image, 0, 0, canvas.width, canvas.height);
    let original = null;
    if (scale === 1 && ['image/png', 'image/jpeg', 'image/webp'].includes(file.type)) {
      original = await new Promise((resolve, reject) => {
        const reader = new FileReader(); reader.onload = () => resolve(reader.result); reader.onerror = reject; reader.readAsDataURL(file);
      });
    }
    const result = encodeTheoryPage(canvas, original);
    if (result.bytes > 5 * 1024 * 1024) throw new Error('This page is still larger than 5 MB. Crop to the answer instead of reducing handwriting quality.');
    return { ...result, name: `${(file.name || 'Answer page').replace(/\.[^.]+$/, '')}.${result.extension}` };
  } finally { URL.revokeObjectURL(url); }
}
