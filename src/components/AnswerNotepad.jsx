import { useCallback, useLayoutEffect, useRef, useState } from "react";
import * as Dialog from "@radix-ui/react-dialog";
import { ArrowRight, Check, Eraser, Hand, Minus, Plus, NotebookPen, PenLine, Redo2, RotateCcw, Undo2, X } from "lucide-react";
import "./AnswerNotepad.css";

const WIDTH = 1200;
const HEIGHT = 1600;
const inks = [["Midnight", "#25334d"], ["Blue", "#295cc9"], ["Violet", "#7950b8"], ["Green", "#17785f"]];
const MAX_PAGES = 8;
const emptyPage = () => ({ strokes: [], paper: "ruled" });
const emptyDraft = () => ({ pages: [emptyPage()], pageIndex: 0 });

function readDraft(key) {
  try {
    const stored = JSON.parse(localStorage.getItem(key));
    const pages = stored?.version === 1 ? [stored] : stored?.version === 2 ? stored.pages : null;
    if (Array.isArray(pages) && pages.length && pages.length <= MAX_PAGES && pages.every(page =>
      Array.isArray(page.strokes) && page.strokes.every(stroke =>
        ["pen", "eraser"].includes(stroke.tool) && typeof stroke.color === "string" && Number.isFinite(stroke.size)
        && Array.isArray(stroke.points) && stroke.points.length && stroke.points.every(point =>
          [point.x, point.y, point.pressure].every(Number.isFinite))))) {
      return { pages: pages.map(page => ({ strokes: page.strokes.map(stroke => stored.version === 1 && stroke.tool === "eraser" ? { ...stroke, size: 38 } : stroke), paper: ["ruled", "dotted", "plain"].includes(page.paper) ? page.paper : "ruled" })),
        pageIndex: Math.max(0, Math.min(pages.length - 1, Number.isInteger(stored.pageIndex) ? stored.pageIndex : 0)) };
    }
  } catch { /* Preserve legacy drafts when possible; unavailable storage starts a fresh sheet. */ }
  return emptyDraft();
}

function drawSegment(context, stroke, from, to) {
  context.save();
  context.globalCompositeOperation = stroke.tool === "eraser" ? "destination-out" : "source-over";
  context.strokeStyle = stroke.color;
  context.fillStyle = stroke.color;
  const style = stroke.style || "ballpoint";
  const pressure = Math.max(0.15, to.pressure);
  context.lineWidth = stroke.tool === "eraser" ? stroke.size : stroke.size *
    (style === "brush" ? 0.3 + pressure * 2.5 : style === "fountain" ? 0.5 + pressure * 1.4 : style === "pencil" ? 0.8 : 1);
  if (style === "pencil" && stroke.tool !== "eraser") context.globalAlpha = 0.65;
  context.lineCap = "round";
  context.lineJoin = "round";
  context.beginPath();
  if (from.x === to.x && from.y === to.y) {
    context.arc(to.x, to.y, context.lineWidth / 2, 0, Math.PI * 2);
    context.fill();
  } else {
    context.moveTo(from.x, from.y);
    context.lineTo(to.x, to.y);
    context.stroke();
  }
  context.restore();
}

function redraw(canvas, strokes) {
  const context = canvas?.getContext("2d");
  if (!context) return;
  context.clearRect(0, 0, WIDTH, HEIGHT);
  for (const stroke of strokes) {
    if (stroke.clear) { context.clearRect(0, 0, WIDTH, HEIGHT); continue; }
    if (stroke.style === "highlighter" && stroke.tool !== "eraser") {
      context.save(); context.globalAlpha = 0.25; context.strokeStyle = stroke.color;
      context.lineWidth = stroke.size * 4; context.lineCap = "round"; context.lineJoin = "round";
      context.beginPath(); context.moveTo(stroke.points[0].x, stroke.points[0].y);
      for (const point of stroke.points) context.lineTo(point.x, point.y);
      if (stroke.points.length === 1) context.lineTo(stroke.points[0].x + 0.01, stroke.points[0].y);
      context.stroke(); context.restore(); continue;
    }
    stroke.points.forEach((point, index) => drawSegment(context, stroke, stroke.points[Math.max(0, index - 1)], point));
  }
}

export default function AnswerNotepad({ draftId, prompt, disabled, onSave, hasImage }) {
  const [open, setOpen] = useState(false);
  return <Dialog.Root open={open} onOpenChange={setOpen}>
    <Dialog.Trigger asChild>
      <button type="button" disabled={disabled} className="an-launch mt-4 flex w-full items-center gap-3 rounded-xl border p-4 text-left transition-colors">
        <span className="an-launch-icon flex h-10 w-10 shrink-0 items-center justify-center rounded-xl"><NotebookPen size={21} /></span>
        <span className="min-w-0 flex-1"><strong className="block text-sm">Notepad</strong><span className="mt-1 block text-xs">Write on your iPad or tablet</span></span><ArrowRight size={16} className="shrink-0" />
      </button>
    </Dialog.Trigger>
    {open && <NotepadSheet key={draftId} storageKey={`medicomm-notepad:${draftId}`} prompt={prompt} hasImage={hasImage}
      onSave={image => { onSave(image); setOpen(false); }} />}
  </Dialog.Root>;
}

function NotepadSheet({ storageKey, prompt, onSave, hasImage }) {
  const [draft, setDraft] = useState(() => readDraft(storageKey));
  const [redo, setRedo] = useState([]);
  const [tool, setTool] = useState("pen");
  const [color, setColor] = useState(inks[0][1]);
  const [size, setSize] = useState(3);
  const [eraserSize, setEraserSize] = useState(38);
  const [penStyle, setPenStyle] = useState("ballpoint");
  const [zoom, setZoom] = useState(1);
  const [pencilOnly, setPencilOnly] = useState(false);
  const [storageError, setStorageError] = useState(false);
  const [message, setMessage] = useState("");
  const [confirmClear, setConfirmClear] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  const canvasRef = useRef(null);
  const activeStroke = useRef(null);
  const workspaceRef = useRef(null);
  const panRef = useRef(null);
  const touchesRef = useRef(new Map());
  const pinchRef = useRef(null);
  const zoomRef = useRef(1);
  const zoomAnchorRef = useRef(null);
  const toolRef = useRef("pen");
  const draftRef = useRef(draft);
  const currentPage = draft.pages[draft.pageIndex];
  const pageRef = () => draftRef.current.pages[draftRef.current.pageIndex];

  function persist(next) {
    draftRef.current = next;
    setDraft(next);
    try { localStorage.setItem(storageKey, JSON.stringify({ version: 2, ...next })); setStorageError(false); }
    catch { setStorageError(true); }
  }

  const attachCanvas = useCallback(canvas => {
    canvasRef.current = canvas;
    const current = draftRef.current;
    redraw(canvas, current.pages[current.pageIndex].strokes);
  }, []);

  useLayoutEffect(() => {
    redraw(canvasRef.current, currentPage.strokes);
  }, [currentPage.strokes]);

  useLayoutEffect(() => {
    const anchor = zoomAnchorRef.current;
    if (!anchor) return;
    const bounds = canvasRef.current.getBoundingClientRect();
    const workspace = workspaceRef.current;
    workspace.scrollLeft += bounds.left + anchor.x * bounds.width - anchor.clientX;
    workspace.scrollTop += bounds.top + anchor.y * bounds.height - anchor.clientY;
    zoomAnchorRef.current = null;
  });

  function point(event) {
    const bounds = canvasRef.current.getBoundingClientRect();
    return { x: Math.max(0, Math.min(WIDTH, (event.clientX - bounds.left) * WIDTH / bounds.width)),
      y: Math.max(0, Math.min(HEIGHT, (event.clientY - bounds.top) * HEIGHT / bounds.height)),
      pressure: event.pointerType === "pen" ? event.pressure || 0.5 : 0.5 };
  }
  function updatePage(nextPage) {
    const current = draftRef.current;
    persist({ ...current, pages: current.pages.map((page, i) => i === current.pageIndex ? nextPage : page) });
  }
  function releasePointer(id) {
    if (workspaceRef.current?.hasPointerCapture(id)) workspaceRef.current.releasePointerCapture(id);
  }
  function chooseTool(next) { finish(); toolRef.current = next; setTool(next); setConfirmClear(false); }
  function touchPair() {
    const [a, b] = [...touchesRef.current.values()];
    return { clientX: (a.x + b.x) / 2, clientY: (a.y + b.y) / 2, distance: Math.max(1, Math.hypot(a.x - b.x, a.y - b.y)) };
  }
  function start(event) {
    if (event.pointerType === "touch") {
      // Ignore palms while a stylus is writing.
      if (activeStroke.current?.pointerType === "pen") return;
      touchesRef.current.set(event.pointerId, { x: event.clientX, y: event.clientY });
      event.currentTarget.setPointerCapture(event.pointerId);
      if (touchesRef.current.size >= 2) {
        event.preventDefault();
        // The first finger may have begun a stroke. A pinch must never leave ink or erase it.
        activeStroke.current = null;
        panRef.current = null;
        redraw(canvasRef.current, pageRef().strokes);
        if (!pinchRef.current) {
          const pair = touchPair();
          const bounds = canvasRef.current.getBoundingClientRect();
          pinchRef.current = { ...pair, zoom: zoomRef.current,
            x: (pair.clientX - bounds.left) / bounds.width, y: (pair.clientY - bounds.top) / bounds.height };
        }
        return;
      }
      if (pinchRef.current) return;
    }
    if (activeStroke.current || panRef.current || pinchRef.current || (event.pointerType === "mouse" && event.button !== 0)) return;
    if (toolRef.current === "pan" || (pencilOnly && event.pointerType === "touch") || event.target !== canvasRef.current) {
      event.preventDefault();
      event.currentTarget.setPointerCapture(event.pointerId);
      panRef.current = { id: event.pointerId, x: event.clientX, y: event.clientY,
        left: workspaceRef.current.scrollLeft, top: workspaceRef.current.scrollTop };
      return;
    }
    event.preventDefault();
    event.currentTarget.setPointerCapture(event.pointerId);
    if (event.pointerType === "pen") setPencilOnly(true);
    const selectedTool = event.pointerType === "pen" && (event.button === 5 || (event.buttons & 32)) ? "eraser" : toolRef.current;
    const stroke = { tool: selectedTool, style: penStyle, color, size: selectedTool === "eraser" ? eraserSize : size, points: [point(event)] };
    activeStroke.current = { pointerId: event.pointerId, pointerType: event.pointerType, stroke };
    if (stroke.style === "highlighter" && stroke.tool === "pen") redraw(canvasRef.current, [...pageRef().strokes, stroke]);
    else drawSegment(canvasRef.current.getContext("2d"), stroke, stroke.points[0], stroke.points[0]);
    setMessage(""); setConfirmClear(false);
  }
  function move(event) {
    if (touchesRef.current.has(event.pointerId)) {
      touchesRef.current.set(event.pointerId, { x: event.clientX, y: event.clientY });
      if (pinchRef.current) {
        event.preventDefault();
        if (touchesRef.current.size >= 2) {
          const pair = touchPair();
          const pinch = pinchRef.current;
          applyZoom(pinch.zoom * pair.distance / pinch.distance, { ...pinch, clientX: pair.clientX, clientY: pair.clientY });
        }
        return;
      }
    }
    const pan = panRef.current;
    if (pan?.id === event.pointerId) {
      event.preventDefault();
      workspaceRef.current.scrollLeft = pan.left + pan.x - event.clientX;
      workspaceRef.current.scrollTop = pan.top + pan.y - event.clientY;
      return;
    }
    const active = activeStroke.current;
    if (!active || event.pointerId !== active.pointerId) return;
    event.preventDefault();
    const samples = event.nativeEvent.getCoalescedEvents?.() || [];
    for (const sample of samples.length ? samples : [event]) {
      const next = point(sample);
      const previous = active.stroke.points.at(-1);
      if (Math.hypot(next.x - previous.x, next.y - previous.y) < 0.5) continue;
      active.stroke.points.push(next);
      if (active.stroke.style !== "highlighter" || active.stroke.tool === "eraser") drawSegment(canvasRef.current.getContext("2d"), active.stroke, previous, next);
    }
    if (active.stroke.style === "highlighter" && active.stroke.tool === "pen") redraw(canvasRef.current, [...pageRef().strokes, active.stroke]);
  }
  function finish(event) {
    if (event) {
      touchesRef.current.delete(event.pointerId);
      if (!touchesRef.current.size) pinchRef.current = null;
    } else {
      const ids = [...touchesRef.current.keys()];
      touchesRef.current.clear(); pinchRef.current = null;
      ids.forEach(releasePointer);
    }
    if (!event || panRef.current?.id === event.pointerId) {
      const pan = panRef.current;
      panRef.current = null;
      if (pan) releasePointer(pan.id);
    }
    const active = activeStroke.current;
    if (!active || (event && event.pointerId !== active.pointerId)) return;
    activeStroke.current = null;
    releasePointer(active.pointerId);
    updatePage({ ...pageRef(), strokes: [...pageRef().strokes, active.stroke] });
    setRedo([]);
  }
  function undoStroke() {
    finish();
    const page = pageRef();
    if (!page.strokes.length) return;
    setRedo(items => [...items, page.strokes.at(-1)]);
    updatePage({ ...page, strokes: page.strokes.slice(0, -1) });
  }
  function redoStroke() {
    finish();
    if (!redo.length) return;
    updatePage({ ...pageRef(), strokes: [...pageRef().strokes, redo.at(-1)] });
    setRedo(items => items.slice(0, -1));
  }
  function changePage(index, add = false) {
    finish();
    const current = draftRef.current;
    if (add && current.pages.length >= MAX_PAGES) return;
    persist({ ...current, pages: add ? [...current.pages, emptyPage()] : current.pages, pageIndex: index });
    setRedo([]); setConfirmClear(false); setMessage("");
    workspaceRef.current.scrollTo(0, 0);
  }
  function applyZoom(value, anchor) {
    const next = Math.max(0.5, Math.min(3, value));
    zoomRef.current = next;
    zoomAnchorRef.current = anchor;
    // A new anchor may also pan at the zoom limits.
    if (next === zoom) {
      const bounds = canvasRef.current.getBoundingClientRect();
      workspaceRef.current.scrollLeft += bounds.left + anchor.x * bounds.width - anchor.clientX;
      workspaceRef.current.scrollTop += bounds.top + anchor.y * bounds.height - anchor.clientY;
      zoomAnchorRef.current = null;
    }
    setZoom(next);
  }
  function changeZoom(value) {
    finish();
    const workspace = workspaceRef.current;
    const view = workspace.getBoundingClientRect();
    const bounds = canvasRef.current.getBoundingClientRect();
    const clientX = view.left + workspace.clientWidth / 2;
    const clientY = view.top + workspace.clientHeight / 2;
    applyZoom(value, { clientX, clientY, x: (clientX - bounds.left) / bounds.width, y: (clientY - bounds.top) / bounds.height });
  }
  function save() {
    finish();
    try {
      const pages = draftRef.current.pages;
      const scratch = document.createElement("canvas"); scratch.width = WIDTH; scratch.height = HEIGHT;
      let hasInk = false;
      for (const page of pages) {
        redraw(scratch, page.strokes);
        const pixels = scratch.getContext("2d").getImageData(0, 0, WIDTH, HEIGHT).data;
        for (let i = 3; i < pixels.length; i += 4) if (pixels[i]) { hasInk = true; break; }
        if (hasInk) break;
      }
      if (!hasInk) { setMessage("Write your answer on the sheet before saving."); return; }
      const columns = pages.length > 1 ? 2 : 1;
      const labelHeight = pages.length > 1 ? 32 : 0;
      const output = document.createElement("canvas");
      output.width = WIDTH * columns; output.height = (HEIGHT + labelHeight) * Math.ceil(pages.length / columns);
      const context = output.getContext("2d");
      context.fillStyle = "#ffffff"; context.fillRect(0, 0, output.width, output.height);
      pages.forEach((page, index) => {
        redraw(scratch, page.strokes);
        const x = (index % columns) * WIDTH; const y = Math.floor(index / columns) * (HEIGHT + labelHeight);
        if (labelHeight) { context.fillStyle = "#555555"; context.font = "20px sans-serif"; context.fillText(`Page ${index + 1}`, x + 16, y + 24); }
        context.drawImage(scratch, x, y + labelHeight);
      });
      const dataUrl = output.toDataURL("image/png");
      if (!dataUrl.startsWith("data:image/png") || (dataUrl.length - dataUrl.indexOf(",") - 1) * 0.75 > 5 * 1024 * 1024) {
        setMessage("These pages are too large to attach. Your draft is saved; reduce the amount of ink and try again."); return;
      }
      onSave({ dataUrl, name: "Notepad answer.png", width: output.width, height: output.height });
    } catch { setMessage("Your answer could not be attached. Your pages are still saved here. Please try again."); }
  }

  return <Dialog.Portal>
    <Dialog.Overlay className="an-overlay fixed inset-0 bg-slate-950/50 backdrop-blur-sm" />
    <Dialog.Content className="an-dialog fixed overflow-hidden shadow-2xl" onEscapeKeyDown={() => finish()}
      onInteractOutside={event => event.preventDefault()} onOpenAutoFocus={event => { event.preventDefault(); document.getElementById("an-close")?.focus(); }}>
      <header className="an-header">
        <NotebookPen size={20} className="an-accent" />
        <div className="an-heading"><Dialog.Title>Notepad</Dialog.Title><Dialog.Description title={prompt}>{prompt}</Dialog.Description></div>
        <button type="button" className="an-tool an-tools-toggle" aria-expanded={toolsOpen} aria-controls="an-controls" onClick={() => setToolsOpen(value => !value)}>Tools</button>
        <Dialog.Close asChild><button id="an-close" type="button" className="an-tool shrink-0" aria-label="Close notepad" onClick={() => finish()}><X size={20} /></button></Dialog.Close>
      </header>
      <aside id="an-controls" className={`an-controls${toolsOpen ? " an-controls-open" : ""}`} aria-label="Notepad controls">
      <div className="an-toolbar flex flex-wrap items-center gap-2 border-b px-4 py-3 sm:px-7" aria-label="Writing tools">
        <div className="an-tool-group flex gap-1 rounded-xl p-1">
          <button type="button" className="an-tool" aria-label="Pen" aria-pressed={tool === "pen"} onPointerDown={event => { if (event.button === 0) chooseTool("pen"); }} onClick={() => chooseTool("pen")}><PenLine size={19} /><span className="hidden sm:inline">Pen</span></button>
          <button type="button" className="an-tool" aria-label="Eraser" aria-pressed={tool === "eraser"} onPointerDown={event => { if (event.button === 0) chooseTool("eraser"); }} onClick={() => chooseTool("eraser")}><Eraser size={19} /><span className="hidden sm:inline">Eraser</span></button>
        </div>
        <div className="flex items-center" aria-label="Ink colour">{inks.map(([label, ink]) => <button type="button" key={ink} className="an-swatch" aria-label={`${label} ink`} aria-pressed={color === ink} onClick={() => { finish(); setColor(ink); }}><span style={{ background: ink }}>{color === ink && <Check size={13} color="white" />}</span></button>)}</div>
        <label className="an-select-label flex items-center gap-2 text-xs">Pen style<select aria-label="Pen style" value={penStyle} onChange={event => { finish(); setPenStyle(event.target.value); chooseTool("pen"); }}>
          <option value="ballpoint">Ballpoint</option><option value="fountain">Fountain</option><option value="brush">Brush</option><option value="pencil">Pencil</option><option value="highlighter">Highlighter</option>
        </select></label>
        <label className="an-thickness text-xs">{tool === "eraser" ? "Eraser size" : "Tip thickness"}<output>{tool === "eraser" ? eraserSize : size} px</output>
          <input type="range" aria-label={tool === "eraser" ? "Eraser size" : "Tip thickness"} min={tool === "eraser" ? 8 : 1} max={tool === "eraser" ? 96 : 20} step="1" value={tool === "eraser" ? eraserSize : size} onChange={event => { finish(); (tool === "eraser" ? setEraserSize : setSize)(Number(event.target.value)); }} />
        </label>
        <button type="button" className="an-tool" aria-label="Move page" aria-pressed={tool === "pan"} onClick={() => chooseTool("pan")}><Hand size={19} />Move page</button>
        <div className="an-zoom"><button className="an-tool" type="button" aria-label="Zoom out" disabled={zoom <= 0.5} onClick={() => changeZoom(zoom - 0.25)}><Minus size={18} /></button><button type="button" className="an-tool" aria-label="Reset zoom" onClick={() => changeZoom(1)}>{Math.round(zoom * 100)}%</button><button className="an-tool" type="button" aria-label="Zoom in" disabled={zoom >= 3} onClick={() => changeZoom(zoom + 0.25)}><Plus size={18} /></button></div>
        <div className="ml-auto flex gap-1">
          <button type="button" className="an-tool" aria-label="Undo" disabled={!currentPage.strokes.length} onClick={undoStroke}><Undo2 size={19} /></button>
          <button type="button" className="an-tool" aria-label="Redo" disabled={!redo.length} onClick={redoStroke}><Redo2 size={19} /></button>
          <button type="button" className="an-tool" aria-label="Clear sheet" disabled={!currentPage.strokes.length} onClick={() => setConfirmClear(true)}><RotateCcw size={18} /></button>
        </div>
      </div>
      <div className="an-options flex flex-wrap items-center justify-between gap-2 px-5 py-2 text-xs sm:px-7">
        <label className="flex items-center gap-2">Paper<select aria-label="Paper style" value={currentPage.paper} onChange={event => { finish(); updatePage({ ...pageRef(), paper: event.target.value }); }}><option value="ruled">Ruled</option><option value="dotted">Dotted</option><option value="plain">Plain</option></select></label>
        <label className="flex min-h-9 cursor-pointer items-center gap-2"><input type="checkbox" checked={pencilOnly} onChange={event => setPencilOnly(event.target.checked)} /> Pencil only · finger to move</label>
      </div>
      {confirmClear && <div role="alert" className="an-clear flex flex-wrap items-center justify-center gap-3 px-4 py-2 text-sm">Clear this sheet? You can undo this.<button type="button" onClick={() => { finish(); updatePage({ ...pageRef(), strokes: [...pageRef().strokes, { tool: "eraser", color, size: 38, points: [{ x: WIDTH / 2, y: HEIGHT / 2, pressure: 1 }], clear: true }] }); setRedo([]); setConfirmClear(false); }}>Clear</button><button type="button" onClick={() => setConfirmClear(false)}>Keep writing</button></div>}
      </aside>
      <div className={`an-workspace${tool === "pan" ? " an-panning" : ""}`} ref={workspaceRef}
        onPointerDown={start} onPointerMove={move} onPointerUp={finish} onPointerCancel={finish} onLostPointerCapture={finish}>
        <div className="an-page-scale" style={{ width: `${zoom * 100}%` }}>
        <div className={`an-paper an-paper-${currentPage.paper} relative mx-auto shadow-lg`}>
          {!currentPage.strokes.length && <div className="pointer-events-none absolute inset-x-0 top-20 text-center text-slate-400"><PenLine size={26} className="mx-auto mb-3 opacity-50" /><p className="text-sm">Every good answer starts here.</p><p className="mt-2 text-xs">Use your Pencil, finger, or mouse.</p></div>}
          <canvas ref={attachCanvas} width={WIDTH} height={HEIGHT} className="an-canvas relative block w-full" aria-label="Handwritten answer sheet" onContextMenu={event => event.preventDefault()} />
        </div>
        <p className="an-sheet-caption mt-4 text-center text-xs">Page {draft.pageIndex + 1} of {draft.pages.length} · Pinch with two fingers to zoom and move</p>
        </div>
      </div>
      <footer className="an-footer">
        <div className="flex flex-wrap items-center justify-between gap-3"><div className="an-page-navigation"><button className="an-tool" type="button" aria-label="Previous page" disabled={draft.pageIndex === 0} onClick={() => changePage(draft.pageIndex - 1)}>&lsaquo;</button><span>{draft.pageIndex + 1}/{draft.pages.length}</span><button className="an-tool" type="button" aria-label="Next page" disabled={draft.pageIndex === draft.pages.length - 1} onClick={() => changePage(draft.pageIndex + 1)}>&rsaquo;</button><button className="an-tool" type="button" aria-label="Add page" disabled={draft.pages.length >= MAX_PAGES} onClick={() => changePage(draft.pages.length, true)}><Plus size={16} /><span className="hidden sm:inline">Page</span></button></div><div className="an-draft-status text-xs"><p className="flex items-center gap-1.5" role="status">{!storageError && <Check size={14} className="an-accent" />}{storageError ? "Draft could not save on this device. Keep this sheet open." : "Draft kept on this device"}</p><p className="sr-only">{hasImage ? "Saving replaces the currently attached image." : "Save, then submit your answer for AI review."}</p></div>
          <button type="button" className="an-save flex min-h-11 items-center justify-center gap-2 rounded-xl px-5 py-3 text-sm font-semibold" onClick={save}>Save answer <ArrowRight size={16} /></button></div>
        {message && <p className="an-save-error text-sm text-red-600" role="alert">{message}</p>}
      </footer>
    </Dialog.Content>
  </Dialog.Portal>;
}
