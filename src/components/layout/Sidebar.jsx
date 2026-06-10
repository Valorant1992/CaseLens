/** Sidebar.jsx */
const NAV_ITEMS = [
  { id: 'dashboard',     icon: '⊞',  label: 'Case Manager' },
  { id: 'alerts',        icon: '🔔', label: 'Alert Queue' },
  { id: 'cases',         icon: '📁', label: 'Cases' },
  { id: 'customers',     icon: '👥', label: 'Customers' },
  { id: 'transactions',  icon: '💸', label: 'Transactions' },
];

export default function Sidebar({ activeView, onNavigate, summary }) {
  const badges = {
    dashboard:    null,
    alerts:       summary?.totalAlerts,
    cases:        summary?.totalCases,
    customers:    null,
    transactions: null,
  };

  return (
    <nav className="sidebar">
      <span className="sidebar__section-label">Navigation</span>
      {NAV_ITEMS.map(item => (
        <button
          key={item.id}
          className={`sidebar__nav-item${activeView === item.id ? ' active' : ''}`}
          onClick={() => onNavigate(item.id)}
        >
          <span className="nav-icon">{item.icon}</span>
          {item.label}
          {badges[item.id] != null && (
            <span className="sidebar__badge">{badges[item.id]}</span>
          )}
        </button>
      ))}
    </nav>
  );
}
