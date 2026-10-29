import { useRef } from "react";
import {
  ChevronRight,
  LockKeyhole,
  MessageCircle,
  MessagesSquare,
  Plus,
  Search,
} from "lucide-react";
import { initials } from "./SocialUI";
import { Button } from "./ui/button";

export default function CommunityInbox(p) {
  const searchField = useRef(null);
  return (
    <article className="hub-inbox">
      <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4 dark:border-neutral-800">
        <h3 className="flex items-center gap-2 text-sm font-bold text-slate-900 dark:text-white">
          <MessageCircle
            size={16}
            className="text-teal-600 dark:text-teal-400"
          />
          <span>Personal inbox</span>
          {p.locked && <LockKeyhole size={14} aria-label="Plan required" />}
          {p.conversations?.length > 0 && (
            <span className="text-[11px] font-normal px-1.5 py-0.5 rounded-full bg-teal-50 dark:bg-teal-950/60 text-teal-700 dark:text-teal-300">
              {p.conversations.length}
            </span>
          )}
        </h3>
        <Button
          variant="ghost"
          size="icon"
          className="-mr-2 h-8 w-8 text-slate-500 hover:text-slate-900 dark:text-neutral-400 dark:hover:text-white"
          aria-label="Find a study partner"
          onClick={() =>
            p.locked
              ? p.onUnlock("inbox")
              : searchField.current?.querySelector("input")?.focus()
          }
        >
          <Plus size={16} />
        </Button>
      </div>
      <div className="hub-inbox-content px-4 pb-3 pt-4">
        {p.mobile && (
          <p className="hub-inbox-intro">
            Your conversations, all in one place.
          </p>
        )}
        {p.locked && (
          <button
            type="button"
            className="mb-3 flex items-center gap-2 text-sm text-teal-700 dark:text-teal-300"
            onClick={() => p.onUnlock("inbox")}
          >
            <LockKeyhole size={16} />
            Unlock Personal Inbox
          </button>
        )}
        <div ref={searchField} className="relative min-w-0">
          <Search
            size={14}
            className="pointer-events-none absolute left-3 top-3 text-slate-400"
            aria-hidden="true"
          />
          <input
            type="search"
            aria-label="Find a study partner"
            value={p.search}
            onChange={(e) => p.onSearch(e.target.value)}
            placeholder="Search people to start a chat…"
            className="w-full bg-slate-100 dark:bg-neutral-900 border border-slate-200/80 dark:border-neutral-800 rounded-xl pl-9 pr-3 py-2 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-neutral-700"
          />
        </div>
        {p.searchBusy ? (
          <p role="status" className="px-1 py-3 text-xs text-slate-400">
            Searching learners…
          </p>
        ) : p.search.trim().length === 1 ? (
          <p className="px-1 py-3 text-xs text-slate-400">
            Type at least 2 characters to search.
          </p>
        ) : p.search.trim().length >= 2 && !p.results.length ? (
          <p role="status" className="px-1 py-3 text-xs text-slate-400">
            No learners found. Try another name.
          </p>
        ) : null}
        {p.results.length > 0 && (
          <div className="hub-inbox-results mt-2 max-h-64 space-y-1 overflow-y-auto border-b border-slate-100 pb-3 dark:border-neutral-800">
            {p.results.map((person) => (
              <button
                key={person.id}
                className="flex w-full items-center gap-2.5 rounded-lg p-2 text-left hover:bg-slate-50 dark:hover:bg-neutral-900/60 transition"
                onClick={() => p.onDirect(person.id)}
              >
                <div className="w-8 h-8 shrink-0 rounded-full overflow-hidden bg-slate-200 dark:bg-neutral-800 flex items-center justify-center font-bold text-slate-700 dark:text-neutral-200 text-xs select-none">
                  {person.profileImageUrl ? (
                    <img
                      src={person.profileImageUrl}
                      alt=""
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    initials(person.name)
                  )}
                </div>
                <span className="min-w-0 flex-1">
                  <strong className="block truncate text-xs font-semibold text-slate-900 dark:text-white">
                    {person.name}
                  </strong>
                  <span className="block truncate text-[11px] text-slate-400">
                    {person.medicalCollege || "Medical Student"}
                  </span>
                </span>
                <span className="text-xs font-semibold text-teal-600 dark:text-teal-400">
                  Message
                </span>
              </button>
            ))}
          </div>
        )}
        <div className="hub-inbox-conversations mt-2 max-h-80 overflow-y-auto divide-y divide-slate-100 dark:divide-neutral-800/60">
          {p.directBusy ? (
            <p
              role="status"
              className="py-4 text-xs text-slate-400 text-center"
            >
              Loading messages…
            </p>
          ) : p.conversations.length ? (
            p.conversations.map((conversation) => {
              const person = conversation.otherParticipant;
              const latest = conversation.messages.at(-1);
              return (
                <button
                  key={conversation.id}
                  className="hub-conversation group flex w-full items-center gap-2.5 py-2.5 px-1 text-left rounded-lg hover:bg-slate-50 dark:hover:bg-neutral-900/60 transition"
                  onClick={() => p.onConversation(conversation.id)}
                >
                  <div className="w-9 h-9 shrink-0 rounded-full overflow-hidden bg-slate-200 dark:bg-neutral-800 flex items-center justify-center font-bold text-slate-700 dark:text-neutral-200 text-xs select-none">
                    {person?.profileImageUrl ? (
                      <img
                        src={person.profileImageUrl}
                        alt=""
                        className="h-full w-full object-cover"
                      />
                    ) : (
                      initials(person?.name)
                    )}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-1">
                      <strong className="block truncate text-xs font-semibold text-slate-900 dark:text-white group-hover:text-teal-600 dark:group-hover:text-teal-400 transition">
                        {person?.name || "Private chat"}
                      </strong>
                      <time className="text-[10px] text-slate-400 shrink-0">
                        {p.timestamp(latest?.createdAt)}
                      </time>
                    </div>
                    <span className="hub-conversation-preview mt-0.5 block truncate text-[11px] text-slate-500 dark:text-neutral-400">
                      {latest?.text || "Start the conversation"}
                    </span>
                  </div>
                  <ChevronRight
                    size={14}
                    className="shrink-0 text-slate-300 group-hover:text-teal-600 transition"
                  />
                </button>
              );
            })
          ) : (
            <div className="px-2 py-6 text-center">
              <MessagesSquare
                size={22}
                className="mx-auto mb-2 text-slate-400 opacity-60"
              />
              <p className="text-xs leading-5 text-slate-500 dark:text-neutral-400">
                No conversations yet.
                <br />
                Find a study partner above and say hello.
              </p>
            </div>
          )}
        </div>
      </div>
    </article>
  );
}
