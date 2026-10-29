import { useLayoutEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import {
  ArrowDown,
  ArrowLeft,
  Loader2,
  MessageCircle,
  Send,
  Swords,
} from "lucide-react";
import { Avatar } from "./SocialUI";
import { useMobileViewport } from "../lib/useMobileViewport";
import "./direct-chat.css";

export default function DirectChat({
  conversation,
  draft,
  onDraft,
  onSend,
  onBack,
  onChallenge,
  onProfile,
  message,
  timestamp,
}) {
  const mobile = useMobileViewport();
  const [sending, setSending] = useState(false);
  const [atBottom, setAtBottom] = useState(true);
  const viewport = useRef(null);
  const history = useRef(null);
  const followLatest = useRef(true);
  const sendLock = useRef(false);
  const back = useRef(null);
  const person = conversation.otherParticipant;
  const messages = conversation.messages || [];
  const latest = messages[messages.length - 1];

  useLayoutEffect(() => {
    if (!mobile) return;
    // The portal escapes the app shell's animated/translated page container.
    // Lock the background while leaving dialogs in their own portals usable.
    const root = document.getElementById("root");
    const previousInert = root?.inert;
    const previousBody = {
      position: document.body.style.position,
      top: document.body.style.top,
      width: document.body.style.width,
      overflow: document.body.style.overflow,
    };
    const previousOverflow = document.documentElement.style.overflow;
    const scrollY = window.scrollY;
    const previousFocus = document.activeElement;
    if (root) root.inert = true;
    Object.assign(document.body.style, {
      position: "fixed",
      top: `-${scrollY}px`,
      width: "100%",
      overflow: "hidden",
    });
    document.documentElement.style.overflow = "hidden";
    const resize = () => {
      const visual = window.visualViewport;
      viewport.current?.style.setProperty(
        "--chat-height",
        `${visual?.height ?? window.innerHeight}px`,
      );
      viewport.current?.style.setProperty(
        "--chat-top",
        `${visual?.offsetTop ?? 0}px`,
      );
      if (followLatest.current && history.current)
        history.current.scrollTop = history.current.scrollHeight;
    };
    resize();
    back.current?.focus({ preventScroll: true });
    window.visualViewport?.addEventListener("resize", resize);
    window.visualViewport?.addEventListener("scroll", resize);
    window.addEventListener("resize", resize);
    return () => {
      window.visualViewport?.removeEventListener("resize", resize);
      window.visualViewport?.removeEventListener("scroll", resize);
      window.removeEventListener("resize", resize);
      if (root) root.inert = previousInert;
      Object.assign(document.body.style, previousBody);
      document.documentElement.style.overflow = previousOverflow;
      window.scrollTo({ top: scrollY, behavior: "instant" });
      if (previousFocus?.isConnected)
        previousFocus.focus({ preventScroll: true });
    };
  }, [mobile]);

  useLayoutEffect(() => {
    if (followLatest.current || latest?.isOwnMessage) {
      if (history.current)
        history.current.scrollTop = history.current.scrollHeight;
      followLatest.current = true;
      setAtBottom(true);
    }
  }, [latest?.id, latest?.isOwnMessage, mobile]);

  const jumpToLatest = () => {
    history.current?.scrollTo({
      top: history.current.scrollHeight,
      behavior: "instant",
    });
    followLatest.current = true;
    setAtBottom(true);
  };
  const submit = async (event) => {
    event.preventDefault();
    if (sendLock.current || !draft.trim()) return;
    sendLock.current = true;
    setSending(true);
    try {
      await onSend(event);
    } finally {
      sendLock.current = false;
      setSending(false);
    }
  };

  const chat = (
    <section
      ref={viewport}
      className={`direct-chat ${mobile ? "direct-chat-mobile" : ""}`}
      aria-label={`Conversation with ${person?.name || "learner"}`}
    >
      <header className="direct-chat-header">
        <button
          ref={back}
          type="button"
          className="direct-chat-icon"
          aria-label="Back to personal inbox"
          onClick={onBack}
        >
          <ArrowLeft size={22} />
        </button>
        <button
          type="button"
          className="direct-chat-person"
          onClick={() => onProfile(person?.id)}
          aria-label={`View ${person?.name || "learner"}'s profile`}
        >
          <Avatar name={person?.name} src={person?.profileImageUrl} />
          <span>
            <strong>{person?.name || "Direct chat"}</strong>
            <small>{person?.medicalCollege || "Personal inbox"}</small>
          </span>
        </button>
        <button
          type="button"
          className="direct-chat-challenge"
          disabled={!person?.id}
          onClick={() => onChallenge(person)}
        >
          <Swords size={18} />
          <span>1v1 challenge</span>
        </button>
      </header>
      {message && (
        <p className="direct-chat-notice" role="status">
          {message}
        </p>
      )}
      <div className="direct-chat-body direct-chat-wallpaper">
        <div
          ref={history}
          className="direct-chat-history"
          role="log"
          aria-label="Messages"
          aria-live="polite"
          aria-relevant="additions"
          tabIndex={0}
          onScroll={(event) => {
            const list = event.currentTarget;
            const nearBottom =
              list.scrollHeight - list.clientHeight - list.scrollTop < 80;
            followLatest.current = nearBottom;
            setAtBottom(nearBottom);
          }}
        >
          <div className="direct-chat-messages">
            {!messages.length && (
              <div className="direct-chat-empty">
                <MessageCircle size={30} />
                <strong>Start the conversation</strong>
                <p>
                  Say hello or invite {person?.name || "your study partner"} to
                  a 1v1 challenge.
                </p>
              </div>
            )}
            {messages.map((item) => (
              <div
                key={item.id}
                className={`direct-chat-row ${item.isOwnMessage ? "direct-chat-row-own" : ""}`}
              >
                <div
                  className={`direct-chat-bubble ${item.type === "challenge" ? "direct-chat-bubble-challenge" : ""}`}
                >
                  {item.type === "challenge" && (
                    <span className="direct-chat-challenge-label">
                      <Swords size={14} />
                      1v1 challenge
                    </span>
                  )}
                  <p>{item.text}</p>
                  <time dateTime={item.createdAt}>
                    {timestamp(item.createdAt)}
                  </time>
                </div>
              </div>
            ))}
          </div>
        </div>
        {!atBottom && (
          <button
            type="button"
            className="direct-chat-latest"
            onClick={jumpToLatest}
            aria-label="Jump to latest messages"
          >
            <ArrowDown size={18} />
            Latest messages
          </button>
        )}
      </div>
      <form className="direct-chat-composer" onSubmit={submit}>
        <input
          type="text"
          aria-label="Message"
          placeholder="Message…"
          value={draft}
          disabled={sending}
          onChange={(event) => onDraft(event.target.value)}
          autoComplete="off"
          enterKeyHint="send"
        />
        <button
          type="submit"
          aria-label={sending ? "Sending message" : "Send message"}
          disabled={sending || !draft.trim()}
        >
          {sending ? (
            <Loader2 size={20} className="animate-spin" />
          ) : (
            <Send size={20} />
          )}
        </button>
      </form>
    </section>
  );

  return mobile ? createPortal(chat, document.body) : chat;
}
