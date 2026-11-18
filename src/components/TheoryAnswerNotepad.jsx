import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";
import * as Dialog from "@radix-ui/react-dialog";
import { ArrowLeft, ArrowRight, BookOpen, Check, Columns3, Eraser, Hand, Highlighter, Minus, PenLine, Plus, Redo2, RotateCcw, Rows3, Undo2, X } from "lucide-react";
import "./AnswerNotepad.css";
import { drawSmoothStroke } from "./notepadInk.js";

const WIDTH = 1200;
const HEIGHT = 1700;

const penInks = [
  ["Midnight", "#1e293b"],
  ["Blue", "#2563eb"],
  ["Red", "#dc2626"],
  ["Violet", "#7c3aed"],
  ["Green", "#16a34a"],
];

const highlighterColors = [
  ["Yellow", "#facc15"],
  ["Neon Green", "#4ade80"],
  ["Pink", "#f472b6"],
  ["Sky Blue", "#38bdf8"],
  ["Purple", "#c084fc"],
];

function readAnnotations(key, pageCount) {
  try {
    const stored = JSON.parse(localStorage.getItem(key));
    if (stored && Array.isArray(stored.pages)) {
      return {
        pages: Array.from({ length: pageCount }, (_, i) => stored.pages[i] || { strokes: [] }),
        pageIndex: Math.max(0, Math.min(pageCount - 1, Number.isInteger(stored.pageIndex) ? stored.pageIndex : 0)),
      };
    }
  } catch {
    /* fallback to fresh */
  }
  return {
    pages: Array.from({ length: pageCount }, () => ({ strokes: [] })),
    pageIndex: 0,
  };
}

function drawSegment(context, stroke, from, to) {
  context.save();
  context.globalCompositeOperation = stroke.tool === "eraser" ? "destination-out" : "source-over";
  context.strokeStyle = stroke.color;
  context.fillStyle = stroke.color;
  const style = stroke.style || "ballpoint";
  const pressure = Math.max(0.15, to.pressure);
  context.lineWidth =
    stroke.tool === "eraser"
      ? stroke.size
      : stroke.size *
        (style === "brush"
          ? 0.3 + pressure * 2.5
          : style === "fountain"
          ? 0.5 + pressure * 1.4
          : style === "pencil"
          ? 0.8
          : 1);
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
  context.setTransform(canvas.width / WIDTH, 0, 0, canvas.height / HEIGHT, 0, 0);
  context.clearRect(0, 0, WIDTH, HEIGHT);
  for (const stroke of strokes) {
    if (stroke.clear) {
      context.clearRect(0, 0, WIDTH, HEIGHT);
      continue;
    }
    if (stroke.smooth) {
      drawSmoothStroke(context, stroke);
      continue;
    }
    if (stroke.style === "highlighter" && stroke.tool !== "eraser") {
      context.save();
      context.globalAlpha = 0.28;
      context.strokeStyle = stroke.color;
      context.lineWidth = stroke.size * 4;
      context.lineCap = "round";
      context.lineJoin = "round";
      context.beginPath();
      context.moveTo(stroke.points[0].x, stroke.points[0].y);
      for (const point of stroke.points) context.lineTo(point.x, point.y);
      if (stroke.points.length === 1) context.lineTo(stroke.points[0].x + 0.01, stroke.points[0].y);
      context.stroke();
      context.restore();
      continue;
    }
    stroke.points.forEach((point, index) =>
      drawSegment(context, stroke, stroke.points[Math.max(0, index - 1)], point)
    );
  }
}

function StaticPageCanvas({ strokes, width, height }) {
  const canvasRef = useRef(null);
  useLayoutEffect(() => {
    if (canvasRef.current) redraw(canvasRef.current, strokes);
  }, [strokes]);
  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      className="an-canvas relative block w-full h-full pointer-events-none"
    />
  );
}

export default function TheoryAnswerNotepad({
  question,
  document: doc,
  topicTitle,
  userId,
  isOpen = true,
  onClose,
  onPractice,
}) {
  const pages = doc?.pages || [];
  const pageCount = Math.max(1, pages.length);
  const storageKey = `medicomm-theory-annotations:${userId || "guest"}:${question?.id || "default"}`;

  const [data, setData] = useState(() => readAnnotations(storageKey, pageCount));
  const [redo, setRedo] = useState([]);
  const [tool, setTool] = useState("pen"); // "pen" | "highlighter" | "eraser" | "pan"
  const [penColor, setPenColor] = useState(penInks[0][1]);
  const [highlighterColor, setHighlighterColor] = useState(highlighterColors[0][1]);
  const [penStyle, setPenStyle] = useState("ballpoint");
  const [penSize, setPenSize] = useState(3);
  const [highlighterSize, setHighlighterSize] = useState(10);
  const [eraserSize, setEraserSize] = useState(42);
  const [zoom, setZoom] = useState(1);
  const [pencilOnly, setPencilOnly] = useState(true);
  const [confirmClear, setConfirmClear] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(true);
  const [viewMode, setViewMode] = useState("swipe"); // "swipe" | "scroll"

  const canvasRef = useRef(null);
  const inkFrameRef = useRef(null);
  const committedCanvasRef = useRef(null);
  const displayScale = useRef(Math.min(2, Math.max(1, window.devicePixelRatio || 1))).current;
  const activeStroke = useRef(null);
  const workspaceRef = useRef(null);
  const panRef = useRef(null);
  const touchesRef = useRef(new Map());
  const pinchRef = useRef(null);
  const zoomRef = useRef(1);
  const zoomAnchorRef = useRef(null);
  const toolRef = useRef("pen");
  const swipeRef = useRef(null);
  const pageScaleRef = useRef(null);
  const pageAnimationRef = useRef(null);
  const previousPageRef = useRef(data.pageIndex);
  const dataRef = useRef(data);
  const flushRef = useRef(null);

  const currentPageIndex = Math.min(data.pageIndex, pageCount - 1);
  const currentPage = data.pages[currentPageIndex] || { strokes: [] };
  const currentImgUrl = pages[currentPageIndex] || "";

  const activeColor = tool === "highlighter" ? highlighterColor : penColor;
  const activeSize = tool === "highlighter" ? highlighterSize : tool === "eraser" ? eraserSize : penSize;

  const pageRef = () => dataRef.current.pages[dataRef.current.pageIndex] || { strokes: [] };

  flushRef.current = () => {
    if (activeStroke.current) {
      finish();
    }
  };

  useEffect(() => {
    const flush = () => flushRef.current?.();
    const hide = () => {
      if (document.visibilityState === "hidden") flush();
    };
    window.addEventListener("pagehide", flush);
    document.addEventListener("visibilitychange", hide);
    return () => {
      flush();
      cancelAnimationFrame(inkFrameRef.current);
      pageAnimationRef.current?.cancel();
      window.removeEventListener("pagehide", flush);
      document.removeEventListener("visibilitychange", hide);
    };
  }, []);

  useLayoutEffect(() => {
    const previous = previousPageRef.current;
    previousPageRef.current = data.pageIndex;
    if (previous === data.pageIndex || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    pageAnimationRef.current?.cancel();
    pageAnimationRef.current = pageScaleRef.current?.animate(
      [
        { transform: `translateX(${data.pageIndex > previous ? "-" : ""}64px)`, opacity: 0.25 },
        { transform: "translateX(0)", opacity: 1 },
      ],
      { duration: 280, easing: "cubic-bezier(0.22, 1, 0.36, 1)" }
    );
  }, [data.pageIndex]);

  function persist(next) {
    dataRef.current = next;
    setData(next);
    try {
      localStorage.setItem(storageKey, JSON.stringify(next));
    } catch {
      /* ignore quota errors */
    }
  }

  const attachCanvas = useCallback((canvas) => {
    canvasRef.current = canvas;
    const current = dataRef.current;
    const page = current.pages[current.pageIndex] || { strokes: [] };
    redraw(canvas, page.strokes);
  }, []);

  useLayoutEffect(() => {
    redraw(canvasRef.current, currentPage.strokes);
  }, [currentPage.strokes]);

  useLayoutEffect(() => {
    const anchor = zoomAnchorRef.current;
    if (!anchor || !canvasRef.current || !workspaceRef.current) return;
    const bounds = canvasRef.current.getBoundingClientRect();
    const workspace = workspaceRef.current;
    workspace.scrollLeft += bounds.left + anchor.x * bounds.width - anchor.clientX;
    workspace.scrollTop += bounds.top + anchor.y * bounds.height - anchor.clientY;
    zoomAnchorRef.current = null;
  });

  function point(event) {
    const bounds = canvasRef.current.getBoundingClientRect();
    return {
      x: Math.max(0, Math.min(WIDTH, ((event.clientX - bounds.left) * WIDTH) / bounds.width)),
      y: Math.max(0, Math.min(HEIGHT, ((event.clientY - bounds.top) * HEIGHT) / bounds.height)),
      pressure: event.pointerType === "pen" ? event.pressure || 0.5 : 0.5,
    };
  }

  function paintActive() {
    inkFrameRef.current = null;
    const canvas = canvasRef.current;
    const active = activeStroke.current;
    if (!canvas || !active) return;
    const context = canvas.getContext("2d");
    context.setTransform(1, 0, 0, 1, 0, 0);
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(committedCanvasRef.current, 0, 0);
    context.setTransform(canvas.width / WIDTH, 0, 0, canvas.height / HEIGHT, 0, 0);
    drawSmoothStroke(context, active.stroke);
  }

  function scheduleInk() {
    if (inkFrameRef.current === null) inkFrameRef.current = requestAnimationFrame(paintActive);
  }

  function addSamples(event) {
    const active = activeStroke.current;
    const samples = event.nativeEvent?.getCoalescedEvents?.() || [];
    for (const sample of samples.length ? samples : [event]) {
      const next = point(sample);
      const previous = active.stroke.points.at(-1);
      if (event.type === "pointerup") next.pressure = previous.pressure;
      const distance = Math.hypot(next.x - previous.x, next.y - previous.y);
      if (distance < 0.15) continue;
      next.pressure = previous.pressure + (next.pressure - previous.pressure) * Math.min(0.65, 0.18 + distance / 24);
      active.stroke.points.push(next);
    }
  }

  function updatePage(nextPage) {
    const current = dataRef.current;
    persist({
      ...current,
      pages: current.pages.map((p, i) => (i === current.pageIndex ? nextPage : p)),
    });
  }

  function releasePointer(id) {
    if (workspaceRef.current?.hasPointerCapture(id)) workspaceRef.current.releasePointerCapture(id);
  }

  function chooseTool(next) {
    finish();
    toolRef.current = next;
    setTool(next);
    setConfirmClear(false);
  }

  function touchPair() {
    const [a, b] = [...touchesRef.current.values()];
    return {
      clientX: (a.x + b.x) / 2,
      clientY: (a.y + b.y) / 2,
      distance: Math.max(1, Math.hypot(a.x - b.x, a.y - b.y)),
    };
  }

  function start(event) {
    pageAnimationRef.current?.cancel();
    if (event.pointerType === "touch") {
      if (activeStroke.current?.pointerType === "pen") return;
      touchesRef.current.set(event.pointerId, { x: event.clientX, y: event.clientY });
      event.currentTarget.setPointerCapture(event.pointerId);
      if (touchesRef.current.size >= 2) {
        swipeRef.current = null;
        event.preventDefault();
        activeStroke.current = null;
        panRef.current = null;
        redraw(canvasRef.current, pageRef().strokes);
        if (!pinchRef.current) {
          const pair = touchPair();
          const bounds = canvasRef.current.getBoundingClientRect();
          pinchRef.current = {
            ...pair,
            zoom: zoomRef.current,
            x: (pair.clientX - bounds.left) / bounds.width,
            y: (pair.clientY - bounds.top) / bounds.height,
          };
        }
        return;
      }
      if (pinchRef.current) return;
      const bounds = workspaceRef.current.getBoundingClientRect();
      const edge = event.clientX - bounds.left < 32 || bounds.right - event.clientX < 32;
      if (zoomRef.current <= 1 && (edge || pencilOnly || toolRef.current === "pan")) {
        swipeRef.current = { id: event.pointerId, x: event.clientX, y: event.clientY };
        if (edge) {
          event.preventDefault();
          return;
        }
      }
    }
    if (activeStroke.current || panRef.current || pinchRef.current || (event.pointerType === "mouse" && event.button !== 0))
      return;
    if (toolRef.current === "pan" || (pencilOnly && event.pointerType === "touch") || event.target !== canvasRef.current) {
      event.preventDefault();
      event.currentTarget.setPointerCapture(event.pointerId);
      panRef.current = {
        id: event.pointerId,
        x: event.clientX,
        y: event.clientY,
        left: workspaceRef.current.scrollLeft,
        top: workspaceRef.current.scrollTop,
      };
      return;
    }
    event.preventDefault();
    event.currentTarget.setPointerCapture(event.pointerId);
    if (event.pointerType === "pen") setPencilOnly(true);

    const isStylusEraser = event.pointerType === "pen" && (event.button === 5 || (event.buttons & 32));
    const effectiveTool = isStylusEraser ? "eraser" : toolRef.current;
    const effectiveStyle = effectiveTool === "highlighter" ? "highlighter" : penStyle;
    const effectiveColor = effectiveTool === "highlighter" ? highlighterColor : penColor;
    const effectiveSize = effectiveTool === "eraser" ? eraserSize : effectiveTool === "highlighter" ? highlighterSize : penSize;

    const canvas = canvasRef.current;
    const base = committedCanvasRef.current || document.createElement("canvas");
    base.width = canvas.width;
    base.height = canvas.height;
    base.getContext("2d").drawImage(canvas, 0, 0);
    committedCanvasRef.current = base;

    const stroke = {
      tool: effectiveTool === "highlighter" ? "pen" : effectiveTool,
      style: effectiveStyle,
      smooth: true,
      color: effectiveColor,
      size: effectiveSize,
      points: [point(event)],
    };

    activeStroke.current = { pointerId: event.pointerId, pointerType: event.pointerType, stroke };
    paintActive();
    setConfirmClear(false);
  }

  function move(event) {
    if (touchesRef.current.has(event.pointerId)) {
      touchesRef.current.set(event.pointerId, { x: event.clientX, y: event.clientY });
      if (pinchRef.current) {
        event.preventDefault();
        if (touchesRef.current.size >= 2) {
          const pair = touchPair();
          const pinch = pinchRef.current;
          applyZoom((pinch.zoom * pair.distance) / pinch.distance, {
            ...pinch,
            clientX: pair.clientX,
            clientY: pair.clientY,
          });
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
    addSamples(event);
    scheduleInk();
  }

  function finish(event) {
    const swipe = swipeRef.current;
    if (viewMode === "swipe" && swipe && event?.pointerId === swipe.id && event.type === "pointerup" && !pinchRef.current) {
      const dx = event.clientX - swipe.x;
      const dy = event.clientY - swipe.y;
      if (Math.abs(dx) >= 40 && Math.abs(dx) > Math.abs(dy)) {
        swipeRef.current = null;
        if (dx < 0 && dataRef.current.pageIndex < pageCount - 1) {
          changePage(dataRef.current.pageIndex + 1);
          return;
        } else if (dx > 0 && dataRef.current.pageIndex > 0) {
          changePage(dataRef.current.pageIndex - 1);
          return;
        }
      }
    }
    if (!event || swipe?.id === event.pointerId) swipeRef.current = null;
    if (event) {
      touchesRef.current.delete(event.pointerId);
      if (!touchesRef.current.size) pinchRef.current = null;
    } else {
      const ids = [...touchesRef.current.keys()];
      touchesRef.current.clear();
      pinchRef.current = null;
      ids.forEach(releasePointer);
    }
    if (!event || panRef.current?.id === event.pointerId) {
      const pan = panRef.current;
      panRef.current = null;
      if (pan) releasePointer(pan.id);
    }
    const active = activeStroke.current;
    if (!active || (event && event.pointerId !== active.pointerId)) return;
    if (event?.type === "pointerup") addSamples(event);
    cancelAnimationFrame(inkFrameRef.current);
    inkFrameRef.current = null;
    activeStroke.current = null;
    releasePointer(active.pointerId);
    updatePage({ ...pageRef(), strokes: [...pageRef().strokes, active.stroke] });
    setRedo([]);
  }

  function undoStroke() {
    finish();
    const page = pageRef();
    if (!page.strokes.length) return;
    setRedo((items) => [...items, page.strokes.at(-1)]);
    updatePage({ ...page, strokes: page.strokes.slice(0, -1) });
  }

  function redoStroke() {
    finish();
    if (!redo.length) return;
    updatePage({ ...pageRef(), strokes: [...pageRef().strokes, redo.at(-1)] });
    setRedo((items) => items.slice(0, -1));
  }

  function changePage(index) {
    finish();
    if (index < 0 || index >= pageCount) return;
    persist({ ...dataRef.current, pageIndex: index });
    setRedo([]);
    setConfirmClear(false);
    workspaceRef.current?.scrollTo(0, 0);
  }

  function applyZoom(value, anchor) {
    const next = Math.max(0.5, Math.min(3, value));
    zoomRef.current = next;
    zoomAnchorRef.current = anchor;
    if (next === zoom && canvasRef.current && workspaceRef.current) {
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
    if (!workspace || !canvasRef.current) return;
    const view = workspace.getBoundingClientRect();
    const bounds = canvasRef.current.getBoundingClientRect();
    const clientX = view.left + workspace.clientWidth / 2;
    const clientY = view.top + workspace.clientHeight / 2;
    applyZoom(value, {
      clientX,
      clientY,
      x: (clientX - bounds.left) / bounds.width,
      y: (clientY - bounds.top) / bounds.height,
    });
  }

  return (
    <Dialog.Root open={isOpen} onOpenChange={(v) => !v && onClose?.()}>
      <Dialog.Portal>
        <Dialog.Overlay className="an-overlay fixed inset-0 bg-slate-950/60 backdrop-blur-sm" />
        <Dialog.Content
          className="an-dialog fixed overflow-hidden shadow-2xl"
          onEscapeKeyDown={() => {
            finish();
            onClose?.();
          }}
          onKeyDown={(event) => {
            if (!(event.ctrlKey || event.metaKey) || /INPUT|SELECT|TEXTAREA/.test(event.target.tagName)) return;
            const key = event.key.toLowerCase();
            if (key === "z" || key === "y") {
              event.preventDefault();
              if (key === "y" || event.shiftKey) redoStroke();
              else undoStroke();
            }
          }}
          onInteractOutside={(event) => event.preventDefault()}
          onOpenAutoFocus={(event) => {
            event.preventDefault();
            document.getElementById("an-theory-close")?.focus();
          }}
        >
          {/* Top Header */}
          <header className="an-header">
            <BookOpen size={20} className="an-accent" />
            <div className="an-heading">
              <Dialog.Title>Exam-Ready Model Answer</Dialog.Title>
              <Dialog.Description title={question?.prompt || doc?.title}>
                {question?.prompt || doc?.title}
              </Dialog.Description>
            </div>

            <div className="flex items-center gap-2">
              {onPractice && (
                <button
                  type="button"
                  className="button button-primary flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold"
                  style={{ minHeight: "36px", padding: "6px 14px", borderRadius: "8px" }}
                  onClick={() => {
                    finish();
                    onPractice();
                  }}
                  title="Test yourself by writing an answer for AI evaluation"
                >
                  <PenLine size={14} />
                  <span>Write answer</span>
                </button>
              )}

              <button
                type="button"
                className="an-tool an-tools-toggle"
                aria-expanded={toolsOpen}
                aria-controls="an-theory-controls"
                onClick={() => setToolsOpen((v) => !v)}
              >
                Tools
              </button>

              <button
                id="an-theory-close"
                type="button"
                className="an-tool shrink-0"
                aria-label="Close answer viewer"
                onClick={() => {
                  finish();
                  onClose?.();
                }}
              >
                <X size={20} />
              </button>
            </div>
          </header>

          {/* Left Toolbox */}
          <aside
            id="an-theory-controls"
            className={`an-controls${toolsOpen ? " an-controls-open" : ""}`}
            aria-label="Study & annotation controls"
          >
            <div className="px-4 py-2 text-xs font-medium text-slate-500" role="status">
              Study & Annotate
            </div>

            <div className="an-toolbar flex flex-col gap-3 px-3 py-2" aria-label="Toolbox">
              {/* Premium Stationer Tool Dock: Pen, Highlighter, Eraser */}
              <div className="tan-tools-dock" role="radiogroup" aria-label="Primary drawing tools">
                {/* 1. Pen Tool Button */}
                <button
                  type="button"
                  className={`tan-tool-btn ${tool === "pen" ? "is-active" : ""}`}
                  aria-pressed={tool === "pen"}
                  onClick={() => chooseTool("pen")}
                  title="Pen: Ballpoint, Fountain, Brush, Pencil"
                >
                  <div className="tan-tool-btn-icon-box">
                    <PenLine size={18} />
                  </div>
                  <div className="tan-tool-btn-info">
                    <span className="tan-tool-btn-label">Pen</span>
                    <span className="tan-tool-btn-sub capitalize">{penStyle}</span>
                  </div>
                  <span
                    className="tan-tool-btn-indicator"
                    style={{ background: penColor }}
                    title={`Current ink: ${penColor}`}
                  />
                </button>

                {/* 2. Highlighter Tool Button */}
                <button
                  type="button"
                  className={`tan-tool-btn ${tool === "highlighter" ? "is-active" : ""}`}
                  aria-pressed={tool === "highlighter"}
                  onClick={() => chooseTool("highlighter")}
                  title="Highlighter: Translucent textbook marker"
                >
                  <div className="tan-tool-btn-icon-box">
                    <Highlighter size={18} />
                  </div>
                  <div className="tan-tool-btn-info">
                    <span className="tan-tool-btn-label">Highlighter</span>
                    <span className="tan-tool-btn-sub">Marker</span>
                  </div>
                  <span
                    className="tan-tool-btn-indicator"
                    style={{
                      background: highlighterColor,
                      boxShadow: `0 0 8px ${highlighterColor}`,
                    }}
                    title={`Current highlighter: ${highlighterColor}`}
                  />
                </button>

                {/* 3. Eraser Tool Button */}
                <button
                  type="button"
                  className={`tan-tool-btn ${tool === "eraser" ? "is-active" : ""}`}
                  aria-pressed={tool === "eraser"}
                  onClick={() => chooseTool("eraser")}
                  title="Eraser: Precision erase annotations"
                >
                  <div className="tan-tool-btn-icon-box">
                    <Eraser size={18} />
                  </div>
                  <div className="tan-tool-btn-info">
                    <span className="tan-tool-btn-label">Eraser</span>
                    <span className="tan-tool-btn-sub">{eraserSize}px tip</span>
                  </div>
                  <span
                    className="tan-tool-btn-indicator"
                    style={{ background: "#94a3b8" }}
                    title="Eraser mode"
                  />
                </button>
              </div>

              {/* Color Swatches */}
              <div className="flex flex-col gap-1">
                <span className="text-[10.5px] font-semibold text-slate-500 uppercase tracking-wider">
                  {tool === "highlighter" ? "Highlighter Tint" : "Ink Colour"}
                </span>
                <div className="flex items-center justify-between" aria-label="Color Palette">
                  {(tool === "highlighter" ? highlighterColors : penInks).map(([label, colorVal]) => {
                    const isSelected = (tool === "highlighter" ? highlighterColor : penColor) === colorVal;
                    return (
                      <button
                        type="button"
                        key={colorVal}
                        className="an-swatch"
                        aria-label={`${label} ink`}
                        aria-pressed={isSelected}
                        onClick={() => {
                          finish();
                          if (tool === "highlighter") setHighlighterColor(colorVal);
                          else setPenColor(colorVal);
                        }}
                      >
                        <span style={{ background: colorVal }}>
                          {isSelected && <Check size={13} color={tool === "highlighter" ? "#1e293b" : "white"} />}
                        </span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Pen Style (only shown if pen) */}
              {tool === "pen" && (
                <label className="an-select-label flex flex-col gap-1 text-xs">
                  <span className="text-[10.5px] font-semibold text-slate-500 uppercase tracking-wider">Pen Style</span>
                  <select
                    aria-label="Pen style"
                    value={penStyle}
                    onChange={(event) => {
                      finish();
                      setPenStyle(event.target.value);
                    }}
                  >
                    <option value="ballpoint">Ballpoint</option>
                    <option value="fountain">Fountain</option>
                    <option value="brush">Brush</option>
                    <option value="pencil">Pencil</option>
                  </select>
                </label>
              )}

              {/* Stroke Preview */}
              <div className="an-ink-preview" aria-hidden="true">
                <svg viewBox="0 0 150 40" key={`${tool}-${penStyle}-${activeColor}-${activeSize}`}>
                  <path
                    d="M10 28 C25 28 30 8 44 12 S52 32 68 24 S84 6 96 16 S115 32 140 12"
                    fill="none"
                    stroke={tool === "eraser" ? "#abb2c0" : activeColor}
                    strokeWidth={
                      tool === "eraser"
                        ? 10
                        : tool === "highlighter"
                        ? highlighterSize * 2.2
                        : penStyle === "brush"
                        ? penSize * 1.5
                        : penSize
                    }
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    opacity={tool === "highlighter" ? 0.45 : penStyle === "pencil" ? 0.7 : 1}
                  />
                </svg>
              </div>

              {/* Tip Thickness / Eraser Size */}
              <label className="an-thickness text-xs">
                <span>{tool === "eraser" ? "Eraser Size" : tool === "highlighter" ? "Highlighter Width" : "Tip Thickness"}</span>
                <output>{activeSize} px</output>
                <input
                  type="range"
                  aria-label="Tip thickness"
                  min={tool === "eraser" ? 12 : tool === "highlighter" ? 4 : 1}
                  max={tool === "eraser" ? 96 : tool === "highlighter" ? 28 : 20}
                  step="1"
                  value={activeSize}
                  onChange={(event) => {
                    finish();
                    const val = Number(event.target.value);
                    if (tool === "eraser") setEraserSize(val);
                    else if (tool === "highlighter") setHighlighterSize(val);
                    else setPenSize(val);
                  }}
                />
              </label>

              {/* Move Page / Pan */}
              <button
                type="button"
                className="an-tool w-full justify-start gap-2"
                aria-label="Move page"
                aria-pressed={tool === "pan"}
                onClick={() => chooseTool("pan")}
              >
                <Hand size={18} />
                <span>Move page (Pan)</span>
              </button>

              {/* Zoom Controls */}
              <div className="flex flex-col gap-1">
                <span className="text-[10.5px] font-semibold text-slate-500 uppercase tracking-wider">Zoom</span>
                <div className="an-zoom">
                  <button
                    className="an-tool"
                    type="button"
                    aria-label="Zoom out"
                    disabled={zoom <= 0.5}
                    onClick={() => changeZoom(zoom - 0.25)}
                  >
                    <Minus size={16} />
                  </button>
                  <button type="button" className="an-tool text-xs" aria-label="Reset zoom" onClick={() => changeZoom(1)}>
                    {Math.round(zoom * 100)}%
                  </button>
                  <button
                    className="an-tool"
                    type="button"
                    aria-label="Zoom in"
                    disabled={zoom >= 3}
                    onClick={() => changeZoom(zoom + 0.25)}
                  >
                    <Plus size={16} />
                  </button>
                </div>
              </div>

              {/* Undo / Redo / Clear — scaled down */}
              <div className="an-compact-controls flex items-center justify-between pt-2 border-t border-slate-200 dark:border-slate-800">
                <div className="flex gap-1">
                  <button
                    type="button"
                    className="an-tool an-tool-compact"
                    aria-label="Undo"
                    disabled={!currentPage.strokes.length}
                    onClick={undoStroke}
                    title="Undo stroke (Ctrl+Z)"
                  >
                    <Undo2 size={13} />
                  </button>
                  <button
                    type="button"
                    className="an-tool an-tool-compact"
                    aria-label="Redo"
                    disabled={!redo.length}
                    onClick={redoStroke}
                    title="Redo stroke (Ctrl+Y)"
                  >
                    <Redo2 size={13} />
                  </button>
                </div>
                <button
                  type="button"
                  className="an-tool an-tool-compact text-red-600 dark:text-red-400"
                  aria-label="Clear page annotations"
                  disabled={!currentPage.strokes.length}
                  onClick={() => setConfirmClear(true)}
                  title="Clear annotations on this page"
                >
                  <RotateCcw size={11} />
                </button>
              </div>

              {/* Stylus / Pencil option - kept full size */}
              <label className="an-stylus-only-label flex items-center gap-2 pt-2 text-xs text-slate-700 dark:text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={pencilOnly}
                  onChange={(event) => setPencilOnly(event.target.checked)}
                />
                <span>Stylus only (finger to scroll)</span>
              </label>

              {confirmClear && (
                <div role="alert" className="an-clear flex flex-col gap-2 p-3 text-xs rounded-lg mt-2">
                  <span>Clear your highlights & notes on this page?</span>
                  <div className="flex gap-2">
                    <button
                      type="button"
                      className="font-bold underline"
                      onClick={() => {
                        finish();
                        updatePage({ strokes: [] });
                        setRedo([]);
                        setConfirmClear(false);
                      }}
                    >
                      Clear
                    </button>
                    <button type="button" onClick={() => setConfirmClear(false)}>
                      Cancel
                    </button>
                  </div>
                </div>
              )}
            </div>
          </aside>

          {/* Center Main Workspace */}
          <div
            className={`an-workspace${tool === "pan" ? " an-panning" : ""}`}
            ref={workspaceRef}
            onPointerDown={start}
            onPointerMove={move}
            onPointerUp={finish}
            onPointerCancel={finish}
            onLostPointerCapture={finish}
          >
            {viewMode === "scroll" ? (
              <div className="an-page-scroll-container flex flex-col items-center gap-6 py-4 w-full" style={{ width: `${zoom * 100}%`, margin: '0 auto' }}>
                {pages.map((imgSrc, pIdx) => (
                  <div
                    key={pIdx}
                    className={`an-paper relative mx-auto shadow-2xl rounded-sm overflow-hidden ${
                      pIdx === currentPageIndex ? "ring-2 ring-purple-600 shadow-purple-900/20" : "opacity-95"
                    }`}
                    style={{
                      width: "100%",
                      maxWidth: "960px",
                      aspectRatio: "1200 / 1700",
                      backgroundColor: "#ffffff",
                      position: "relative",
                    }}
                    onClick={() => {
                      if (pIdx !== currentPageIndex) changePage(pIdx);
                    }}
                  >
                    <img
                      src={imgSrc}
                      alt={`Model answer page ${pIdx + 1} of ${pageCount}`}
                      className="pointer-events-none absolute inset-0 h-full w-full object-contain select-none"
                      style={{ userSelect: "none", WebkitUserSelect: "none" }}
                      draggable={false}
                    />
                    {pIdx === currentPageIndex ? (
                      <canvas
                        ref={attachCanvas}
                        width={WIDTH * displayScale}
                        height={HEIGHT * displayScale}
                        className="an-canvas relative block w-full h-full"
                        aria-label={`Annotation canvas for page ${pIdx + 1}`}
                        onContextMenu={(event) => event.preventDefault()}
                      />
                    ) : (
                      <StaticPageCanvas
                        strokes={data.pages[pIdx]?.strokes || []}
                        width={WIDTH * displayScale}
                        height={HEIGHT * displayScale}
                      />
                    )}
                    <div className="absolute top-3 right-3 px-2.5 py-1 bg-slate-900/75 backdrop-blur-sm text-white text-[11px] font-bold rounded-md pointer-events-none shadow-md">
                      Page {pIdx + 1} / {pageCount}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="an-page-scale" ref={pageScaleRef} style={{ width: `${zoom * 100}%` }}>
                <div
                  className="an-paper relative mx-auto shadow-2xl rounded-sm overflow-hidden"
                  style={{
                    width: "100%",
                    maxWidth: "960px",
                    aspectRatio: "1200 / 1700",
                    backgroundColor: "#ffffff",
                    position: "relative",
                  }}
                >
                  {/* Underlying loaded theory answer page */}
                  {currentImgUrl && (
                    <img
                      src={currentImgUrl}
                      alt={`Handwritten model answer: ${doc?.title || question?.prompt || "Theory Answer"}, page ${
                        currentPageIndex + 1
                      } of ${pageCount}`}
                      className="pointer-events-none absolute inset-0 h-full w-full object-contain select-none"
                      style={{ userSelect: "none", WebkitUserSelect: "none" }}
                      draggable={false}
                      onLoad={() => setImageLoaded(true)}
                    />
                  )}

                  {/* Annotation Canvas Layer */}
                  <canvas
                    ref={attachCanvas}
                    width={WIDTH * displayScale}
                    height={HEIGHT * displayScale}
                    className="an-canvas relative block w-full h-full"
                    aria-label="Handwritten answer annotation canvas"
                    onContextMenu={(event) => event.preventDefault()}
                  />
                </div>

                <p className="an-sheet-caption mt-4 text-center text-xs">
                  Page {currentPageIndex + 1} of {pageCount} · Swipe left for next page · Tap with stylus to highlight and annotate
                </p>
              </div>
            )}
          </div>

          {/* Bottom Footer */}
          <footer className="an-footer">
            <div className="flex flex-wrap items-center justify-between gap-3 w-full">
              {/* Multi-page Navigation & View Toggle */}
              <div className="flex items-center gap-3">
                {viewMode === "swipe" && (
                  <div className="an-page-navigation">
                    <button
                      className="an-tool"
                      type="button"
                      aria-label="Previous page"
                      disabled={currentPageIndex === 0}
                      onClick={() => changePage(currentPageIndex - 1)}
                    >
                      &lsaquo;
                    </button>
                    <span className="font-semibold px-1 text-xs">
                      Page {currentPageIndex + 1} / {pageCount}
                    </span>
                    <button
                      className="an-tool"
                      type="button"
                      aria-label="Next page"
                      disabled={currentPageIndex >= pageCount - 1}
                      onClick={() => changePage(currentPageIndex + 1)}
                    >
                      &rsaquo;
                    </button>
                  </div>
                )}

                {/* View Mode Toggle: Swipe vs Vertical Scroll */}
                <div className="an-view-toggle" role="radiogroup" aria-label="Page display mode">
                  <button
                    type="button"
                    className={`an-view-toggle-btn ${viewMode === "swipe" ? "is-active" : ""}`}
                    aria-pressed={viewMode === "swipe"}
                    onClick={() => {
                      finish();
                      setViewMode("swipe");
                    }}
                    title="Swipe through pages (one at a time)"
                  >
                    <Columns3 size={13} />
                    <span>Swipe</span>
                  </button>
                  <button
                    type="button"
                    className={`an-view-toggle-btn ${viewMode === "scroll" ? "is-active" : ""}`}
                    aria-pressed={viewMode === "scroll"}
                    onClick={() => {
                      finish();
                      setViewMode("scroll");
                    }}
                    title="Vertical scroll through all pages"
                  >
                    <Rows3 size={13} />
                    <span>Vertical scroll</span>
                  </button>
                </div>
              </div>

              {/* Status */}
              <div className="an-draft-status text-xs flex items-center gap-1.5 text-slate-500">
                <Check size={14} className="an-accent" />
                <span>Annotations automatically saved</span>
              </div>

              {/* Footer Actions */}
              <div className="flex items-center gap-2">
                {onPractice && (
                  <button
                    type="button"
                    className="an-save flex items-center gap-1.5 px-4 py-2 text-xs font-semibold rounded-lg"
                    onClick={() => {
                      finish();
                      onPractice();
                    }}
                  >
                    <PenLine size={14} />
                    <span>Practise this answer</span>
                    <ArrowRight size={14} />
                  </button>
                )}
                <button
                  type="button"
                  className="button button-secondary px-3 py-1.5 text-xs font-semibold"
                  style={{ minHeight: "36px", borderRadius: "8px" }}
                  onClick={() => {
                    finish();
                    onClose?.();
                  }}
                >
                  Done
                </button>
              </div>
            </div>
          </footer>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
