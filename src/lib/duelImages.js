export function getDuelImageUrls(question) {
  const images = [...new Set([
    ...(Array.isArray(question?.imageUrls) ? question.imageUrls : []),
    ...(Array.isArray(question?.images) ? question.images : []),
    question?.imageUrl,
    question?.image,
  ].map(url => String(url ?? '').trim()).filter(Boolean))];
  // Source references and planned targets are not display assets. Older saved
  // duels may already have merged source images into the display arrays.
  const replacements = images.filter(url => /\/medicomm-(?:img1|atlas)-[^/]+\.(?:png|webp|jpe?g|svg)(?:[?#].*)?$/i.test(url));
  return replacements.length ? replacements : images;
}
