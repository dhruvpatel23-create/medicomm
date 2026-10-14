// Logical page coordinates stay independent of display resolution and export size.
const midpoint = (a, b) => ({ x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 });

export function drawSmoothStroke(context, stroke) {
  const points = stroke.points;
  if (!points.length) return;
  const style = stroke.style || 'ballpoint';
  const eraser = stroke.tool === 'eraser';
  const width = point => stroke.size * (eraser ? 1 : style === 'brush' ? .35 + point.pressure * 2.2
    : style === 'fountain' ? .65 + point.pressure * .9 : style === 'highlighter' ? 4 : style === 'pencil' ? .8 : 1);
  context.save();
  context.globalCompositeOperation = eraser ? 'destination-out' : 'source-over';
  context.strokeStyle = context.fillStyle = stroke.color;
  context.lineCap = context.lineJoin = 'round';
  context.globalAlpha = eraser ? 1 : style === 'highlighter' ? .25 : style === 'pencil' ? .7 : 1;
  context.lineWidth = width(points[0]);
  if (points.length === 1) {
    context.beginPath();
    context.arc(points[0].x, points[0].y, context.lineWidth / 2, 0, Math.PI * 2);
    context.fill();
  } else if (!eraser && ['brush', 'fountain'].includes(style)) {
    let from = points[0];
    let fromWidth = width(from);
    const outline = [{ ...from, radius: fromWidth / 2 }];
    for (let i = 0; i < points.length; i++) {
      const control = points[i];
      const to = i === points.length - 1 ? control : midpoint(control, points[i + 1]);
      const toWidth = i === points.length - 1 ? width(control) : (width(control) + width(points[i + 1])) / 2;
      const steps = Math.max(1, Math.ceil((Math.hypot(control.x - from.x, control.y - from.y) + Math.hypot(to.x - control.x, to.y - control.y)) / 2));
      for (let step = 1; step <= steps; step++) {
        const t = step / steps, u = 1 - t;
        outline.push({ x: u * u * from.x + 2 * u * t * control.x + t * t * to.x,
          y: u * u * from.y + 2 * u * t * control.y + t * t * to.y,
          radius: (u * u * fromWidth + 2 * u * t * width(control) + t * t * toWidth) / 2 });
      }
      from = to; fromWidth = toWidth;
    }
    // A single filled ribbon interpolates width continuously, without segment seams.
    const edges = outline.map((point, i) => {
      const before = outline[Math.max(0, i - 1)], after = outline[Math.min(outline.length - 1, i + 1)];
      const angle = Math.atan2(after.y - before.y, after.x - before.x) + Math.PI / 2;
      return { ...point, angle, dx: Math.cos(angle) * point.radius, dy: Math.sin(angle) * point.radius };
    });
    context.beginPath();
    edges.forEach((p, i) => i ? context.lineTo(p.x + p.dx, p.y + p.dy) : context.moveTo(p.x + p.dx, p.y + p.dy));
    const last = edges.at(-1), first = edges[0];
    context.arc(last.x, last.y, last.radius, last.angle, last.angle - Math.PI, true);
    for (let i = edges.length - 1; i >= 0; i--) context.lineTo(edges[i].x - edges[i].dx, edges[i].y - edges[i].dy);
    context.arc(first.x, first.y, first.radius, first.angle - Math.PI, first.angle - 2 * Math.PI, true);
    context.closePath(); context.fill();
  } else {
    // One continuous path prevents alpha buildup at pencil/highlighter joins.
    context.beginPath(); context.moveTo(points[0].x, points[0].y);
    for (let i = 1; i < points.length - 1; i++) {
      const to = midpoint(points[i], points[i + 1]);
      context.quadraticCurveTo(points[i].x, points[i].y, to.x, to.y);
    }
    const last = points.at(-1);
    context.lineTo(last.x, last.y); context.stroke();
  }
  context.restore();
}
