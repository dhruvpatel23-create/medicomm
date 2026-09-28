import { useCallback, useRef, useState } from "react";
import * as Dialog from "@radix-ui/react-dialog";
import { ArrowRight, Check, Eraser, NotebookPen, PenLine, Redo2, RotateCcw, Undo2, X } from "lucide-react";
import "./AnswerNotepad.css";

const WIDTH = 1200;
const HEIGHT = 1600;
const inks = [["Midnight", "#25334d"], ["Blue", "#295cc9"], ["Violet", "#7950b8"], ["Green", "#17785f"]];
const emptyDraft = () => ({ strokes: [], paper: "ruled" });

function readDraft(key) {
  try {
    const draft = JSON.parse(localStorage.getItem(key));
    if (draft?.version === 1 && Array.isArray(draft.strokes) && draft.strokes.every(stroke =>
      ["pen", "eraser"].includes(stroke.tool) && typeof stroke.color === "string" && Number.isFinite(stroke.size)
      && Array.isArray(stroke.points) && stroke.points.length && stroke.points.every(point =>
        [point.x, point.y, point.pressure].every(Number.isFinite)))) {
      return { strokes: draft.strokes, paper: ["ruled", "dotted", "plain"].includes(draft.paper) ? draft.paper : "ruled" };
    }
  } catch { /* A missing or unavailable local draft starts a fresh sheet. */ }
  return emptyDraft();
}

function drawSegment(context, stroke, from, to) {
  context.save();
  context.globalCompositeOperation = stroke.tool === "eraser" ? "destination-out" : "source-over";
  context.strokeStyle = stroke.color;
  context.fillStyle = stroke.color;
  context.lineWidth = stroke.tool === "eraser" ? 38 : stroke.size * (0.6 + to.pressure * 0.8);
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
  const [pencilOnly, setPencilOnly] = useState(false);
  const [storageError, setStorageError] = useState(false);
  const [message, setMessage] = useState("");
  const [confirmClear, setConfirmClear] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  const canvasRef = useRef(null);
  const activeStroke = useRef(null);
  const draftRef = useRef(draft);

  function persist(next) {
    draftRef.current = next;
    setDraft(next);
    try { localStorage.setItem(storageKey, JSON.stringify({ version: 1, ...next })); setStorageError(false); }
    catch { setStorageError(true); }
  }

  const attachCanvas = useCallback(canvas => {
    canvasRef.current = canvas;
    redraw(canvas, draft.strokes);
  }, [draft.strokes]);

  function point(event) {
    const bounds = canvasRef.current.getBoundingClientRect();
    return { x: Math.max(0, Math.min(WIDTH, (event.clientX - bounds.left) * WIDTH / bounds.width)),
      y: Math.max(0, Math.min(HEIGHT, (event.clientY - bounds.top) * HEIGHT / bounds.height)),
      pressure: event.pointerType === "pen" ? event.pressure || 0.5 : 0.5 };
  }
  function start(event) {
    if (activeStroke.current || (event.pointerType === "mouse" && event.button !== 0) || (pencilOnly && event.pointerType === "touch")) return;
    event.preventDefault();
    event.currentTarget.setPointerCapture(event.pointerId);
    if (event.pointerType === "pen") setPencilOnly(true);
    const stroke = { tool, color, size, points: [point(event)] };
    activeStroke.current = { pointerId: event.pointerId, stroke };
    drawSegment(canvasRef.current.getContext("2d"), stroke, stroke.points[0], stroke.points[0]);
    setMessage(""); setConfirmClear(false);
  }
  function move(event) {
    const active = activeStroke.current;
    if (!active || event.pointerId !== active.pointerId) return;
    event.preventDefault();
    const samples = event.nativeEvent.getCoalescedEvents?.() || [];
    for (const sample of samples.length ? samples : [event]) {
      const next = point(sample);
      const previous = active.stroke.points.at(-1);
      if (Math.hypot(next.x - previous.x, next.y - previous.y) < 0.5) continue;
      drawSegment(canvasRef.current.getContext("2d"), active.stroke, previous, next);
      active.stroke.points.push(next);
    }
  }
  function finish(event) {
    const active = activeStroke.current;
    if (!active || (event && event.pointerId !== active.pointerId)) return;
    activeStroke.current = null;
    persist({ ...draftRef.current, strokes: [...draftRef.current.strokes, active.stroke] });
    setRedo([]);
  }
  function undoStroke() {
    finish();
    const current = draftRef.current;
    if (!current.strokes.length) return;
    setRedo(items => [...items, current.strokes.at(-1)]);
    persist({ ...current, strokes: current.strokes.slice(0, -1) });
  }
  function redoStroke() {
    if (!redo.length) return;
    persist({ ...draftRef.current, strokes: [...draftRef.current.strokes, redo.at(-1)] });
    setRedo(items => items.slice(0, -1));
  }
  function save() {
    finish();
    const canvas = canvasRef.current;
    const pixels = canvas.getContext("2d").getImageData(0, 0, WIDTH, HEIGHT).data;
    let hasInk = false;
    for (let index = 3; index < pixels.length; index += 4) { if (pixels[index]) { hasInk = true; break; } }
    if (!hasInk) { setMessage("Write your answer on the sheet before saving."); return; }
    try {
      const output = document.createElement("canvas");
      output.width = WIDTH; output.height = HEIGHT;
      const context = output.getContext("2d");
      context.fillStyle = "#ffffff"; context.fillRect(0, 0, WIDTH, HEIGHT); context.drawImage(canvas, 0, 0);
      onSave({ dataUrl: output.toDataURL("image/png"), name: "Notepad answer.png", width: WIDTH, height: HEIGHT });
    } catch { setMessage("Your answer could not be attached. Please try saving again."); }
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
          <button type="button" className="an-tool" aria-label="Pen" aria-pressed={tool === "pen"} onClick={() => setTool("pen")}><PenLine size={19} /><span className="hidden sm:inline">Pen</span></button>
          <button type="button" className="an-tool" aria-label="Eraser" aria-pressed={tool === "eraser"} onClick={() => setTool("eraser")}><Eraser size={19} /><span className="hidden sm:inline">Eraser</span></button>
        </div>
        <div className="flex items-center" aria-label="Ink colour">{inks.map(([label, ink]) => <button type="button" key={ink} className="an-swatch" aria-label={`${label} ink`} aria-pressed={color === ink} onClick={() => { setColor(ink); setTool("pen"); }}><span style={{ background: ink }}>{color === ink && <Check size={13} color="white" />}</span></button>)}</div>
        <label className="an-select-label flex items-center gap-2 text-xs">Stroke<select aria-label="Pen thickness" value={size} onChange={event => setSize(Number(event.target.value))}><option value={2}>Fine</option><option value={3}>Medium</option><option value={5}>Bold</option></select></label>
        <div className="ml-auto flex gap-1">
          <button type="button" className="an-tool" aria-label="Undo" disabled={!draft.strokes.length} onClick={undoStroke}><Undo2 size={19} /></button>
          <button type="button" className="an-tool" aria-label="Redo" disabled={!redo.length} onClick={redoStroke}><Redo2 size={19} /></button>
          <button type="button" className="an-tool" aria-label="Clear sheet" disabled={!draft.strokes.length} onClick={() => setConfirmClear(true)}><RotateCcw size={18} /></button>
        </div>
      </div>
      <div className="an-options flex flex-wrap items-center justify-between gap-2 px-5 py-2 text-xs sm:px-7">
        <label className="flex items-center gap-2">Paper<select aria-label="Paper style" value={draft.paper} onChange={event => persist({ ...draftRef.current, paper: event.target.value })}><option value="ruled">Ruled</option><option value="dotted">Dotted</option><option value="plain">Plain</option></select></label>
        <label className="flex min-h-9 cursor-pointer items-center gap-2"><input type="checkbox" checked={pencilOnly} onChange={event => setPencilOnly(event.target.checked)} /> Pencil only · ignore finger touches</label>
      </div>
      {confirmClear && <div role="alert" className="an-clear flex flex-wrap items-center justify-center gap-3 px-4 py-2 text-sm">Clear this sheet? You can undo this.<button type="button" onClick={() => { persist({ ...draftRef.current, strokes: [...draftRef.current.strokes, { tool: "eraser", color, size: 38, points: [{ x: WIDTH / 2, y: HEIGHT / 2, pressure: 1 }], clear: true }] }); setRedo([]); setConfirmClear(false); }}>Clear</button><button type="button" onClick={() => setConfirmClear(false)}>Keep writing</button></div>}
      </aside>
      <div className="an-workspace">
        <div className={`an-paper an-paper-${draft.paper} relative mx-auto shadow-lg`}>
          {!draft.strokes.length && <div className="pointer-events-none absolute inset-x-0 top-20 text-center text-slate-400"><PenLine size={26} className="mx-auto mb-3 opacity-50" /><p className="text-sm">Every good answer starts here.</p><p className="mt-2 text-xs">Use your Pencil, finger, or mouse.</p></div>}
          <canvas ref={attachCanvas} width={WIDTH} height={HEIGHT} className="an-canvas relative block w-full" aria-label="Handwritten answer sheet" onPointerDown={start} onPointerMove={move} onPointerUp={finish} onPointerCancel={finish} onLostPointerCapture={finish} onContextMenu={event => event.preventDefault()} />
        </div>
        <p className="an-sheet-caption mt-4 text-center text-xs">One sheet · Scroll beside the paper to move down</p>
      </div>
      <footer className="an-footer">
        <div className="flex flex-wrap items-center justify-between gap-3"><div className="text-xs"><p className="flex items-center gap-1.5" role="status">{!storageError && <Check size={14} className="an-accent" />}{storageError ? "Draft could not save on this device. Keep this sheet open." : "Draft kept on this device"}</p><p className="sr-only">{hasImage ? "Saving replaces the currently attached image." : "Save, then submit your answer for AI review."}</p></div>
          <button type="button" className="an-save flex min-h-11 items-center justify-center gap-2 rounded-xl px-5 py-3 text-sm font-semibold" onClick={save}>Save answer <ArrowRight size={16} /></button></div>
        {message && <p className="an-save-error text-sm text-red-600" role="alert">{message}</p>}
      </footer>
    </Dialog.Content>
  </Dialog.Portal>;
}
