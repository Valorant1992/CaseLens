/** TopBar.jsx */
export default function TopBar({ searchQuery, onSearch }) {
  return (
    <header className="topbar">
      <div className="topbar__brand">
        <span className="topbar__brand-dot" />
        Bretton AML
      </div>
      <div className="topbar__search">
        <input
          type="search"
          placeholder="Search alert ID, case ID or customer name…"
          value={searchQuery}
          onChange={e => onSearch(e.target.value)}
        />
      </div>
    </header>
  );
}
