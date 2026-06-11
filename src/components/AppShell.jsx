import { Button } from "./ui";

export function AppShell({
  activeView,
  children,
  isDarkMode,
  navItems,
  onNavigate,
  onToggleTheme,
  renderAvatar,
  user,
  userRating,
}) {
  return (
    <div className="page-shell">
      <header className="topbar">
        <Button className="brand brand-button" variant="ghost" onClick={() => onNavigate("Home")}>
          <div className="brand-mark">MQ</div>
          <span>MediComm</span>
        </Button>

        <nav className="nav" aria-label="Primary">
          {navItems.map((item) => (
            <button
              className={`nav-link${activeView === item ? " nav-link-active" : ""}`}
              key={item}
              onClick={() => onNavigate(item)}
            >
              {item}
            </button>
          ))}
        </nav>

        <div className="topbar-actions">
          <button
            className="theme-toggle"
            type="button"
            onClick={onToggleTheme}
            aria-label={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
            title={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
          >
            <span className="theme-toggle-icon" aria-hidden="true">
              {isDarkMode ? "Light" : "Dark"}
            </span>
          </button>
          <div className="score score-fire">15</div>
          <div className="score score-bolt">{userRating}</div>
          <button className="user-chip" onClick={() => onNavigate("Profile")}>
            <div className="avatar">{renderAvatar()}</div>
            <div className="user-chip-copy">
              <strong>{user?.name}</strong>
              <span>{user?.medicalCollege}</span>
            </div>
          </button>
        </div>
      </header>

      <main>{children}</main>

      <nav className="mobile-nav" aria-label="Mobile primary">
        {navItems.map((item) => (
          <button
            className={`mobile-nav-link${activeView === item ? " mobile-nav-link-active" : ""}`}
            key={item}
            onClick={() => onNavigate(item)}
          >
            <span>{item}</span>
          </button>
        ))}
      </nav>

      <div className="preview-pill">
        <span>Practice, duels, communities, and profile data now use the MediComm backend session.</span>
        <button onClick={() => onNavigate("Profile")}>Open profile</button>
      </div>
    </div>
  );
}
