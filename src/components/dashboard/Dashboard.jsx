/**
 * Dashboard.jsx
 * Main case manager view: KPI cards + filter bar + 3 alert group sections.
 */
import { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { useDataStore } from '../../hooks/useDataStore';
import { getDashboardSummary, getGroupedAlerts } from '../../data/service';
import KpiCards from './KpiCards';
import AlertGroup from './AlertGroup';

const SEVERITY_ORDER = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };

function sortBySeverity(items) {
  return [...items].sort(
    (a, b) => (SEVERITY_ORDER[a.alert.severity] ?? 9) - (SEVERITY_ORDER[b.alert.severity] ?? 9)
  );
}

export default function Dashboard({ onSelectCase, onSelectAlert, searchQuery }) {
  const { store } = useDataStore();
  const [severityFilter, setSeverityFilter] = useState(null);
  const [typologyFilter, setTypologyFilter] = useState(null);

  const summary = useMemo(() => getDashboardSummary(store), [store]);
  const grouped = useMemo(() => getGroupedAlerts(store), [store]);

  // Unique typologies for filter
  const typologies = useMemo(() => {
    const types = [...new Set(store.alerts.map(a => a.alert_type))];
    return types.sort();
  }, [store]);

  // Apply search + filters to each group
  const applyFilters = (items) => {
    return items.filter(({ alert, cas }) => {
      if (severityFilter && alert.severity !== severityFilter) return false;
      if (typologyFilter && alert.alert_type !== typologyFilter) return false;
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        const cust = store.customers.find(c => c.customer_id === alert.customer_id);
        const name = cust?.full_name?.toLowerCase() ?? '';
        return (
          alert.alert_id.toLowerCase().includes(q) ||
          (cas?.case_id?.toLowerCase().includes(q)) ||
          name.includes(q) ||
          alert.scenario_name.toLowerCase().includes(q)
        );
      }
      return true;
    });
  };

  const filteredSar       = applyFilters(sortBySeverity(grouped.sar));
  const filteredEscalated = applyFilters(sortBySeverity(grouped.escalated));
  const filteredCleared   = applyFilters(sortBySeverity(grouped.cleared));

  return (
    <motion.div
      className="main-content"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.2 }}
    >
      {/* Page header */}
      <div className="page-header">
        <div>
          <div className="page-header__title">Case Manager</div>
          <div className="page-header__subtitle">
            Alert queue · {new Date().toLocaleDateString('en-GB', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
          </div>
        </div>
      </div>

      {/* KPI cards */}
      <KpiCards summary={summary} />

      {/* Filter bar */}
      <div className="filter-bar">
        <span className="filter-bar__label">Severity</span>
        {['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map(s => (
          <button
            key={s}
            className={`filter-chip${severityFilter === s ? ' active' : ''}`}
            onClick={() => setSeverityFilter(v => v === s ? null : s)}
          >
            {s}
          </button>
        ))}
        <span className="filter-bar__label" style={{ marginLeft: 8 }}>Type</span>
        {typologies.map(t => (
          <button
            key={t}
            className={`filter-chip${typologyFilter === t ? ' active' : ''}`}
            onClick={() => setTypologyFilter(v => v === t ? null : t)}
            style={{ maxWidth: 160, overflow: 'hidden', textOverflow: 'ellipsis' }}
            title={t}
          >
            {t.length > 22 ? t.slice(0, 22) + '…' : t}
          </button>
        ))}
        {(severityFilter || typologyFilter) && (
          <button className="filter-chip" onClick={() => { setSeverityFilter(null); setTypologyFilter(null); }}>
            ✕ Clear
          </button>
        )}
      </div>

      {/* SAR candidates */}
      <AlertGroup
        title="⚠️ SAR Candidates — Requires Filing"
        bucket="sar"
        items={filteredSar}
        store={store}
        onSelectAlert={onSelectAlert}
        onSelectCase={onSelectCase}
        defaultOpen={true}
      />

      {/* Escalated */}
      <AlertGroup
        title="🔶 Escalated — Investigation Required"
        bucket="escalated"
        items={filteredEscalated}
        store={store}
        onSelectAlert={onSelectAlert}
        onSelectCase={onSelectCase}
        defaultOpen={true}
      />

      {/* Auto-cleared */}
      <AlertGroup
        title="✅ Auto-Cleared — Rule-Engine Resolved"
        bucket="cleared"
        items={filteredCleared}
        store={store}
        onSelectAlert={onSelectAlert}
        onSelectCase={onSelectCase}
        defaultOpen={false}
      />
    </motion.div>
  );
}
