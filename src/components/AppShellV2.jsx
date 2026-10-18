import { useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import * as Dialog from "@radix-ui/react-dialog";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import * as Tooltip from "@radix-ui/react-tooltip";
import {
  Activity, BarChart3, Bell, Bookmark, BookOpen, ChevronDown, CircleHelp, Command, CreditCard,
  Check, Home, LayoutDashboard, Menu, MessageCircle, Moon, Search, Settings, Sparkles,
  Megaphone, PanelLeftClose, PanelLeftOpen, Star, Sun, Swords, Trophy, UserPlus, UserRound, X, Zap,
} from "lucide-react";
import { BrandMark } from "./BrandMark";
import { TokenBalance } from './TokenBalance';

const iconMap = {
  Home, Dashboard: LayoutDashboard, Practice: BookOpen, Bookmarks: Bookmark, Analytics: BarChart3,
  Leaderboard: Trophy, Communities: MessageCircle, Reviews: Star, Compete: Swords,
  Pricing: CreditCard, Profile: UserRound, Settings,
};

const primaryMobileItems = ["Dashboard", "Practice", "Compete", "Communities"];

function NavButton({ active, item, onNavigate }) {
  const Icon = iconMap[item] ?? Activity;
  return (
    <button className={`shell-nav-link${active ? " shell-nav-link-active" : ""}`} type="button"
      onClick={() => onNavigate(item)} aria-current={active ? "page" : undefined}>
      <Icon size={18} strokeWidth={1.9} aria-hidden="true" />
      <span>{item}</span>
      {item === "Compete" ? <span className="nav-live-dot" aria-label="Live" /> : null}
    </button>
  );
}

function NotificationToast({ notification, onDismiss, onNavigate, onAccept, onDecline }) {
  const getIcon = () => {
    switch (notification.type) {
      case "challenge":
        return <Swords size={18} />;
      case "friend_request":
        return <UserPlus size={18} />;
      case "message":
        return <MessageCircle size={18} />;
      default:
        return <Megaphone size={18} />;
    }
  };

  const showActions = (notification.type === "challenge" || notification.type === "friend_request") && (onAccept || onDecline);

  return (
    <motion.div
      initial={{ opacity: 0, y: -16, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -12, scale: 0.95 }}
      transition={{ duration: 0.22, ease: "easeOut" }}
      className="notification-toast"
      onClick={() => onNavigate(notification)}
      role="alert"
    >
      <span className={`notification-toast-icon notification-type-${notification.type}`}>
        {getIcon()}
      </span>
      <div className="notification-toast-copy">
        <strong className="notification-toast-title">{notification.title}</strong>
        <p className="notification-toast-text">{notification.text}</p>
        {showActions && (
          <div className="notification-toast-actions" onClick={(e) => e.stopPropagation()}>
            {onAccept && (
              <button
                type="button"
                className="notification-action-btn notification-action-accept"
                onClick={() => onAccept(notification)}
              >
                <Check size={12} />
                Accept
              </button>
            )}
            {onDecline && (
              <button
                type="button"
                className="notification-action-btn notification-action-decline"
                onClick={() => onDecline(notification)}
              >
                <X size={12} />
                Decline
              </button>
            )}
          </div>
        )}
      </div>
      <button
        type="button"
        className="notification-toast-close"
        onClick={(e) => {
          e.stopPropagation();
          onDismiss(notification.id);
        }}
        aria-label="Dismiss notification popup"
      >
        <X size={14} />
      </button>
      <div className="notification-toast-progress" />
    </motion.div>
  );
}

export function AppShell({ activeView, children, isDarkMode, navItems, onNavigate, onToggleTheme,
  renderAvatar, user, userRating, directConversations = [], incomingFriendRequests = [],
  onAcceptNotification, onDeclineNotification }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [commandOpen, setCommandOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [readNotificationIds, setReadNotificationIds] = useState([]);
  const notificationStorageKey = `medicomm-read-notifications-${user?.id ?? "guest"}`;
  const clearedStorageKey = `medicomm-cleared-notifications-${user?.id ?? "guest"}`;
  const [clearedNotificationIds, setClearedNotificationIds] = useState([]);
  const [activeToasts, setActiveToasts] = useState([]);
  const [notificationMenuOpen, setNotificationMenuOpen] = useState(false);
  const [viewedInMenuIds, setViewedInMenuIds] = useState([]);
  const seenToastIdsRef = useRef(new Set());
  const initialLoadRef = useRef(true);

  const groupedItems = useMemo(() => ({
    learn: navItems.filter((item) => ["Home", "Dashboard", "Practice", "Bookmarks", "Analytics"].includes(item)),
    connect: navItems.filter((item) => ["Leaderboard", "Communities", "Reviews", "Compete"].includes(item)),
    account: navItems.filter((item) => ["Pricing", "Profile", "Settings"].includes(item)),
  }), [navItems]);
  const commandResults = navItems.filter((item) => item.toLowerCase().includes(query.trim().toLowerCase()));

  useEffect(() => {
    try {
      const savedCleared = JSON.parse(window.localStorage.getItem(clearedStorageKey) ?? "[]");
      setClearedNotificationIds(Array.isArray(savedCleared) ? savedCleared : []);
    } catch {
      setClearedNotificationIds([]);
    }
  }, [clearedStorageKey]);

  const saveClearedNotificationIds = (ids) => {
    const uniqueIds = [...new Set(ids)];
    setClearedNotificationIds(uniqueIds);
    try {
      window.localStorage.setItem(clearedStorageKey, JSON.stringify(uniqueIds));
    } catch {}
  };

  const notifications = useMemo(() => {
    const messageNotifications = directConversations.flatMap((conversation) => {
      const latestMessage = conversation.messages?.at(-1);
      if (!latestMessage || latestMessage.isOwnMessage || latestMessage.type === "system") return [];
      const isChallenge = latestMessage.type === "challenge";
      return [{
        id: `message-${latestMessage.id}`,
        type: isChallenge ? "challenge" : "message",
        title: isChallenge
          ? `${conversation.otherParticipant?.name ?? latestMessage.userName ?? "A learner"} challenged you to a 1v1 match!`
          : (conversation.otherParticipant?.name ?? latestMessage.userName ?? "New message"),
        text: latestMessage.text,
        createdAt: latestMessage.createdAt,
        destination: isChallenge ? "Compete" : "Communities",
        challengeId: latestMessage.challengeId ?? null,
        conversationId: conversation.id,
        otherParticipant: conversation.otherParticipant,
      }];
    });

    const friendRequestNotifications = (incomingFriendRequests || []).map((req) => ({
      id: `friend-request-${req.id}`,
      type: "friend_request",
      title: `${req.user?.name || "A learner"} sent you a friend request`,
      text: `${req.user?.name || "Learner"}${req.user?.medicalCollege ? ` from ${req.user.medicalCollege}` : ""} wants to connect with you.`,
      createdAt: req.createdAt,
      destination: "Communities",
      requestId: req.id,
      requestUser: req.user,
    }));

    const systemNotifications = [
      {
        id: "system-welcome-notifications",
        type: "system",
        title: "Notifications are now live",
        text: "Messages, friend requests, and 1v1 challenges will appear here.",
        createdAt: "2026-07-29T17:00:00.000Z",
        destination: "Dashboard",
      },
    ];

    return [...messageNotifications, ...friendRequestNotifications, ...systemNotifications]
      .filter((n) => !clearedNotificationIds.includes(n.id))
      .sort((left, right) => new Date(right.createdAt).getTime() - new Date(left.createdAt).getTime());
  }, [directConversations, incomingFriendRequests, clearedNotificationIds]);

  const unreadNotificationCount = notifications.filter((notification) => !readNotificationIds.includes(notification.id)).length;

  useEffect(() => {
    try {
      const savedIds = JSON.parse(window.localStorage.getItem(notificationStorageKey) ?? "[]");
      setReadNotificationIds(Array.isArray(savedIds) ? savedIds : []);
    } catch {
      setReadNotificationIds([]);
    }
  }, [notificationStorageKey]);

  const saveReadNotificationIds = (ids) => {
    const uniqueIds = [...new Set(ids)];
    setReadNotificationIds(uniqueIds);
    try {
      window.localStorage.setItem(notificationStorageKey, JSON.stringify(uniqueIds));
    } catch {}
  };

  // Toast triggers for newly arrived notifications
  useEffect(() => {
    if (initialLoadRef.current) {
      if (notifications.length > 0) {
        notifications.forEach((n) => seenToastIdsRef.current.add(n.id));
        initialLoadRef.current = false;
      }
      return;
    }

    const newNotifications = notifications.filter(
      (n) => !seenToastIdsRef.current.has(n.id) && !clearedNotificationIds.includes(n.id)
    );

    if (newNotifications.length > 0) {
      newNotifications.forEach((n) => seenToastIdsRef.current.add(n.id));
      setActiveToasts((current) => [...current, ...newNotifications]);
    }
  }, [notifications, clearedNotificationIds]);

  // 4-second auto-dismiss for popup toasts
  useEffect(() => {
    if (!activeToasts.length) return;
    const oldest = activeToasts[0];
    const timer = setTimeout(() => {
      setActiveToasts((current) => current.filter((t) => t.id !== oldest.id));
    }, 4000);
    return () => clearTimeout(timer);
  }, [activeToasts]);

  // When user opens the menu, record viewed IDs; when closed, clear them from the list
  const handleNotificationMenuOpenChange = (open) => {
    setNotificationMenuOpen(open);
    if (open) {
      const currentIds = notifications.map((n) => n.id);
      setViewedInMenuIds(currentIds);
      saveReadNotificationIds([...readNotificationIds, ...currentIds]);
    } else {
      if (viewedInMenuIds.length > 0) {
        saveClearedNotificationIds([...clearedNotificationIds, ...viewedInMenuIds]);
        setViewedInMenuIds([]);
      }
    }
  };

  const handleAccept = (notification) => {
    saveClearedNotificationIds([...clearedNotificationIds, notification.id]);
    setActiveToasts((current) => current.filter((t) => t.id !== notification.id));
    setNotificationMenuOpen(false);
    if (onAcceptNotification) onAcceptNotification(notification);
  };

  const handleDecline = (notification) => {
    saveClearedNotificationIds([...clearedNotificationIds, notification.id]);
    setActiveToasts((current) => current.filter((t) => t.id !== notification.id));
    setNotificationMenuOpen(false);
    if (onDeclineNotification) onDeclineNotification(notification);
  };

  const openNotification = (notification) => {
    saveClearedNotificationIds([...clearedNotificationIds, notification.id]);
    setActiveToasts((current) => current.filter((t) => t.id !== notification.id));
    setNotificationMenuOpen(false);
    navigate(notification.destination);
  };

  const clearAllNotifications = () => {
    saveClearedNotificationIds([...clearedNotificationIds, ...notifications.map((n) => n.id)]);
    setActiveToasts([]);
  };
  const formatNotificationTime = (value) => {
    const timestamp = new Date(value).getTime();
    if (!Number.isFinite(timestamp)) return "";
    const elapsedMinutes = Math.max(0, Math.floor((Date.now() - timestamp) / 60000));
    if (elapsedMinutes < 1) return "Now";
    if (elapsedMinutes < 60) return `${elapsedMinutes}m`;
    if (elapsedMinutes < 1440) return `${Math.floor(elapsedMinutes / 60)}h`;
    return `${Math.floor(elapsedMinutes / 1440)}d`;
  };
  const navigate = (item) => { onNavigate(item); setMobileMenuOpen(false); setCommandOpen(false); setQuery(""); };
  const toggleSidebar = () => {
    if (window.matchMedia("(max-width: 820px)").matches) {
      setMobileMenuOpen(true);
      return;
    }
    setSidebarCollapsed((current) => !current);
  };
  const SidebarToggleIcon = sidebarCollapsed ? PanelLeftOpen : PanelLeftClose;

  return (
    <div className={`page-shell app-shell-v2${sidebarCollapsed ? " app-shell-sidebar-collapsed" : ""}`}>
      <a className="skip-link" href="#main-content">Skip to content</a>
      <aside className={`app-sidebar${mobileMenuOpen ? " app-sidebar-open" : ""}${sidebarCollapsed ? " app-sidebar-collapsed" : ""}`} aria-label="Application navigation">
        <div className="sidebar-brand-row">
          <button className="brand brand-button" type="button" onClick={() => navigate("Home")}>
            <span className="brand-mark" aria-hidden="true"><BrandMark title="" /></span>
            <span className="brand-copy"><strong><span className="brand-medi">Med</span><span className="brand-comm">ulla</span></strong><small>Medical learning</small></span>
          </button>
          <button className="icon-button sidebar-close" type="button" onClick={() => setMobileMenuOpen(false)} aria-label="Close navigation"><X size={19} /></button>
        </div>
        <nav className="shell-nav">
          <div className="shell-nav-group"><p>Workspace</p>{groupedItems.learn.map((item) => <NavButton key={item} item={item} active={activeView === item} onNavigate={navigate} />)}</div>
          <div className="shell-nav-group"><p>Community</p>{groupedItems.connect.map((item) => <NavButton key={item} item={item} active={activeView === item} onNavigate={navigate} />)}</div>
          <div className="shell-nav-group shell-nav-group-bottom"><p>Account</p>{groupedItems.account.map((item) => <NavButton key={item} item={item} active={activeView === item} onNavigate={navigate} />)}</div>
        </nav>
        <button className="sidebar-upgrade" type="button" onClick={() => navigate("Pricing")}>
          <span className="upgrade-icon"><Sparkles size={17} /></span><span><strong>Unlock Pro</strong><small>More analytics & practice</small></span><Zap size={16} />
        </button>
      </aside>
      {mobileMenuOpen ? <button className="sidebar-scrim" aria-label="Close navigation" onClick={() => setMobileMenuOpen(false)} /> : null}

      <div className="shell-workspace">
        <header className="topbar">
          <div className="topbar-leading">
            <button
              className="icon-button sidebar-toggle-button"
              type="button"
              onClick={toggleSidebar}
              aria-label={sidebarCollapsed ? "Show navigation" : "Hide navigation"}
              aria-expanded={!sidebarCollapsed}
              title={sidebarCollapsed ? "Show navigation" : "Hide navigation"}
            >
              <SidebarToggleIcon size={20} />
            </button>
            <div className="page-context"><span>{activeView === "Home" ? "Overview" : "Workspace"}</span><strong>{activeView}</strong></div>
          </div>
          <div className="topbar-actions">
            <Tooltip.Root><Tooltip.Trigger asChild><button className="icon-button" type="button" onClick={onToggleTheme} aria-label={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}>{isDarkMode ? <Sun size={19} /> : <Moon size={19} />}</button></Tooltip.Trigger><Tooltip.Portal><Tooltip.Content className="tooltip-content" sideOffset={8}>{isDarkMode ? "Light mode" : "Dark mode"}</Tooltip.Content></Tooltip.Portal></Tooltip.Root>
            <DropdownMenu.Root modal={false} open={notificationMenuOpen} onOpenChange={handleNotificationMenuOpenChange}>
              <DropdownMenu.Trigger asChild>
                <button className="icon-button notification-button" type="button" aria-label={`Notifications${unreadNotificationCount ? `, ${unreadNotificationCount} unread` : ""}`}>
                  <Bell size={19} />
                  {unreadNotificationCount ? <span aria-hidden="true" /> : null}
                </button>
              </DropdownMenu.Trigger>
              <DropdownMenu.Portal>
                <DropdownMenu.Content className="notification-menu" align="end" sideOffset={8}>
                  <div className="notification-menu-header">
                    <div><strong>Notifications</strong><span>{unreadNotificationCount ? `${unreadNotificationCount} unread` : "You are all caught up"}</span></div>
                    {notifications.length ? <button type="button" onClick={clearAllNotifications}><Check size={14} /> Clear all</button> : null}
                  </div>
                  <div className="notification-list">
                    {notifications.length ? notifications.map((notification) => {
                      const isUnread = !readNotificationIds.includes(notification.id);
                      const NotificationIcon =
                        notification.type === "challenge"
                          ? Swords
                          : notification.type === "friend_request"
                          ? UserPlus
                          : notification.type === "message"
                          ? MessageCircle
                          : Megaphone;
                      return (
                        <DropdownMenu.Item
                          className={`notification-item${isUnread ? " notification-item-unread" : ""}`}
                          key={notification.id}
                          onSelect={() => openNotification(notification)}
                        >
                          <span className={`notification-type notification-type-${notification.type}`}><NotificationIcon size={17} /></span>
                          <span className="notification-copy">
                            <span><strong>{notification.title}</strong><time>{formatNotificationTime(notification.createdAt)}</time></span>
                            <small>{notification.text}</small>
                            {((notification.type === "challenge" || notification.type === "friend_request") && (onAcceptNotification || onDeclineNotification)) ? (
                              <div className="notification-item-actions" onClick={(e) => e.stopPropagation()}>
                                {onAcceptNotification && (
                                  <button
                                    type="button"
                                    className="notification-action-btn notification-action-accept"
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      handleAccept(notification);
                                    }}
                                  >
                                    <Check size={12} />
                                    Accept
                                  </button>
                                )}
                                {onDeclineNotification && (
                                  <button
                                    type="button"
                                    className="notification-action-btn notification-action-decline"
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      handleDecline(notification);
                                    }}
                                  >
                                    <X size={12} />
                                    Decline
                                  </button>
                                )}
                              </div>
                            ) : null}
                          </span>
                          {isUnread ? <i aria-label="Unread" /> : null}
                        </DropdownMenu.Item>
                      );
                    }) : <div className="notification-empty"><Bell size={22} /><strong>No notifications</strong><span>New friend requests, 1v1 challenges, and messages will appear here.</span></div>}
                  </div>
                </DropdownMenu.Content>
              </DropdownMenu.Portal>
            </DropdownMenu.Root>
            <TokenBalance user={user} />
            {/* Keep the header menu from locking body scroll and shifting the page. */}
            <DropdownMenu.Root modal={false}>
              <DropdownMenu.Trigger asChild><button className="user-chip" type="button" aria-label="Open account menu"><span className={`avatar${user?.hasPracticeAccess ? " paid-avatar" : ""}`}>{renderAvatar()}</span><span className="user-chip-copy"><strong>{user?.name || "Guest learner"}</strong><span>{user?.email === "guest@medicomm.local" ? "Guest session" : `${userRating} XP`}</span></span><ChevronDown size={15} /></button></DropdownMenu.Trigger>
              <DropdownMenu.Portal><DropdownMenu.Content className="account-menu" align="end" sideOffset={8}>
                <DropdownMenu.Label><strong>{user?.name}</strong><span>{user?.medicalCollege}</span></DropdownMenu.Label><DropdownMenu.Separator />
                <DropdownMenu.Item onSelect={() => navigate("Profile")}><UserRound size={16} /> Profile</DropdownMenu.Item>
                <DropdownMenu.Item onSelect={() => navigate("Settings")}><Settings size={16} /> Settings</DropdownMenu.Item>
                <DropdownMenu.Item onSelect={() => navigate("Pricing")}><CreditCard size={16} /> Plans & billing</DropdownMenu.Item>
                <DropdownMenu.Separator /><DropdownMenu.Item onSelect={() => navigate("Home")}><CircleHelp size={16} /> Help center</DropdownMenu.Item>
              </DropdownMenu.Content></DropdownMenu.Portal>
            </DropdownMenu.Root>
          </div>
        </header>
        <main id="main-content" tabIndex="-1"><AnimatePresence mode="wait" initial={false}><motion.div key={activeView} initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -3 }} transition={{ duration: 0.16, ease: "easeOut" }}>{children}</motion.div></AnimatePresence></main>
      </div>

      <nav className="mobile-nav" aria-label="Mobile primary">
        {primaryMobileItems.map((item) => <NavButton key={item} item={item} active={activeView === item} onNavigate={navigate} />)}
        <button className={`shell-nav-link${mobileMenuOpen ? " shell-nav-link-active" : ""}`} type="button" onClick={() => setMobileMenuOpen(true)}><Menu size={18} /><span>More</span></button>
      </nav>

      <Dialog.Root open={commandOpen} onOpenChange={setCommandOpen}><Dialog.Portal><Dialog.Overlay className="dialog-overlay" /><Dialog.Content className="command-dialog" aria-describedby={undefined}>
        <Dialog.Title className="sr-only">Search Medulla</Dialog.Title>
        <div className="command-input-wrap"><Search size={20} /><input autoFocus value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search pages, subjects, or actions…" aria-label="Search" /><kbd>Esc</kbd></div>
        <div className="command-results"><p>Quick navigation</p>{commandResults.length ? commandResults.map((item) => { const Icon = iconMap[item] ?? Command; return <button key={item} type="button" onClick={() => navigate(item)}><span><Icon size={18} />{item}</span><small>Open</small></button>; }) : <div className="command-empty">No matching destination. Try “Practice” or “Analytics”.</div>}</div>
      </Dialog.Content></Dialog.Portal></Dialog.Root>
      {/* 4-Second Popup Toasts */}
      <aside aria-label="Notification alerts" className="notification-toast-container">
        <AnimatePresence>
          {activeToasts.map((toast) => (
            <NotificationToast
              key={toast.id}
              notification={toast}
              onDismiss={(id) => setActiveToasts((cur) => cur.filter((t) => t.id !== id))}
              onNavigate={openNotification}
              onAccept={onAcceptNotification ? handleAccept : undefined}
              onDecline={onDeclineNotification ? handleDecline : undefined}
            />
          ))}
        </AnimatePresence>
      </aside>
    </div>
  );
}
