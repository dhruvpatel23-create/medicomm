import { useEffect, useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import * as Dialog from "@radix-ui/react-dialog";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import * as Tooltip from "@radix-ui/react-tooltip";
import {
  Activity, BarChart3, Bell, Bookmark, BookOpen, ChevronDown, CircleHelp, Command, CreditCard,
  Check, Home, LayoutDashboard, Menu, MessageCircle, Moon, Search, Settings, Sparkles,
  Megaphone, PanelLeftClose, PanelLeftOpen, Stethoscope, Sun, Swords, Trophy, UserRound, X, Zap,
} from "lucide-react";

const iconMap = {
  Home, Dashboard: LayoutDashboard, Practice: BookOpen, Bookmarks: Bookmark, Analytics: BarChart3,
  Leaderboard: Trophy, Communities: MessageCircle, Compete: Swords,
  Pricing: CreditCard, Profile: UserRound, Settings,
};

const primaryMobileItems = ["Dashboard", "Practice", "Bookmarks", "Communities"];

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

export function AppShell({ activeView, children, isDarkMode, navItems, onNavigate, onToggleTheme,
  renderAvatar, user, userRating, directConversations = [] }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [commandOpen, setCommandOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [readNotificationIds, setReadNotificationIds] = useState([]);
  const notificationStorageKey = `medicomm-read-notifications-${user?.id ?? "guest"}`;
  const groupedItems = useMemo(() => ({
    learn: navItems.filter((item) => ["Home", "Dashboard", "Practice", "Bookmarks", "Analytics"].includes(item)),
    connect: navItems.filter((item) => ["Leaderboard", "Communities", "Compete"].includes(item)),
    account: navItems.filter((item) => ["Pricing", "Profile", "Settings"].includes(item)),
  }), [navItems]);
  const commandResults = navItems.filter((item) => item.toLowerCase().includes(query.trim().toLowerCase()));
  const notifications = useMemo(() => {
    const messageNotifications = directConversations.flatMap((conversation) => {
      const latestMessage = conversation.messages?.at(-1);
      if (!latestMessage || latestMessage.isOwnMessage) return [];
      return [{
        id: `message-${latestMessage.id}`,
        type: "message",
        title: conversation.otherParticipant?.name ?? latestMessage.userName ?? "New message",
        text: latestMessage.text,
        createdAt: latestMessage.createdAt,
        destination: "Communities",
      }];
    });
    const systemNotifications = [
      {
        id: "system-welcome-notifications",
        type: "system",
        title: "Notifications are now live",
        text: "Messages and important MediComm updates will appear here.",
        createdAt: "2026-07-29T17:00:00.000Z",
        destination: "Dashboard",
      },
    ];
    return [...messageNotifications, ...systemNotifications]
      .sort((left, right) => new Date(right.createdAt).getTime() - new Date(left.createdAt).getTime());
  }, [directConversations]);
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
    } catch {
      // The panel still works when storage is unavailable; read state lasts for this session.
    }
  };
  const openNotification = (notification) => {
    saveReadNotificationIds([...readNotificationIds, notification.id]);
    navigate(notification.destination);
  };
  const markAllNotificationsRead = () => saveReadNotificationIds(notifications.map((notification) => notification.id));
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
            <span className="brand-mark" aria-hidden="true"><Stethoscope size={20} /></span>
            <span className="brand-copy"><strong><span className="brand-medi">Medi</span><span className="brand-comm">Comm</span></strong><small>Medical learning</small></span>
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
            <DropdownMenu.Root modal={false}>
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
                    {unreadNotificationCount ? <button type="button" onClick={markAllNotificationsRead}><Check size={14} /> Mark all read</button> : null}
                  </div>
                  <div className="notification-list">
                    {notifications.length ? notifications.map((notification) => {
                      const isUnread = !readNotificationIds.includes(notification.id);
                      const NotificationIcon = notification.type === "message" ? MessageCircle : Megaphone;
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
                          </span>
                          {isUnread ? <i aria-label="Unread" /> : null}
                        </DropdownMenu.Item>
                      );
                    }) : <div className="notification-empty"><Bell size={22} /><strong>No notifications</strong><span>New messages and MediComm updates will appear here.</span></div>}
                  </div>
                </DropdownMenu.Content>
              </DropdownMenu.Portal>
            </DropdownMenu.Root>
            <div className="topbar-stat" title="Current learning streak"><Zap size={16} /><strong>{user?.streak ?? 1}</strong><span>day streak</span></div>
            <DropdownMenu.Root>
              <DropdownMenu.Trigger asChild><button className="user-chip" type="button" aria-label="Open account menu"><span className="avatar">{renderAvatar()}</span><span className="user-chip-copy"><strong>{user?.name || "Guest learner"}</strong><span>{user?.email === "guest@medicomm.local" ? "Guest session" : `${userRating} XP`}</span></span><ChevronDown size={15} /></button></DropdownMenu.Trigger>
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
        <Dialog.Title className="sr-only">Search MediComm</Dialog.Title>
        <div className="command-input-wrap"><Search size={20} /><input autoFocus value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search pages, subjects, or actions…" aria-label="Search" /><kbd>Esc</kbd></div>
        <div className="command-results"><p>Quick navigation</p>{commandResults.length ? commandResults.map((item) => { const Icon = iconMap[item] ?? Command; return <button key={item} type="button" onClick={() => navigate(item)}><span><Icon size={18} />{item}</span><small>Open</small></button>; }) : <div className="command-empty">No matching destination. Try “Practice” or “Analytics”.</div>}</div>
      </Dialog.Content></Dialog.Portal></Dialog.Root>
    </div>
  );
}
