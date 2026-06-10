/**
 * AlertsView.jsx — full alert queue list page
 */
import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { useDataStore } from '../../hooks/useDataStore';
import { SeverityChip, StatusChip } from '../shared/Chip';

function fmt(iso) {
  return new Date(iso).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
}

export default function AlertsView({ onSelectCase, onSelectAlert, searchQuery }) {
  const { store } = useDataStore();

  const rows = useMemo(() => {
    const q = searchQuery?.toLowerCase() ?? '';
    return store.alerts
      .filter(a => {
        if (!q) return true;
        const cust = store.customers.find(c => c.customer_id === a.customer_id);
        return a.alert_id.toLowerCase().includes(q) ||
          a.scenario_name.toLowerCase().includes(q) ||
          cust?.full_name?.toLowerCase().includes(q);
      })
      .sort((a, b) => new Date(b.alert_created_at) - new Date(a.alert_created_at));
  }, [store, searchQuery]);

  return (
    <motion.div className="main-content" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <div className="page-header">
        <div>
          <div className="page-header__title">Alert Queue</div>
          <div className="page-header__subtitle">{rows.length} alerts · sorted by date descending</div>
        </div>
      </div>
      <div className="alert-group">
        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr><th>Alert ID</th><th>Scenario</th><th>Type</th><th>Customer</th><th>Severity</th><th>Status</th><th>Created</th></tr>
            </thead>
            <tbody>
              {rows.map(a => {
                const cust = store.customers.find(c => c.customer_id === a.customer_id);
                const cas = store.cases.find(c => c.primary_alert_id === a.alert_id);
                return (
                  <tr key={a.alert_id} onClick={() => cas ? onSelectCase(cas.case_id) : onSelectAlert(a.alert_id)}>
                    <td><span className="mono">{a.alert_id}</span></td>
                    <td>{a.scenario_name}</td>
                    <td>{a.alert_type}</td>
                    <td>{cust?.full_name ?? a.customer_id}</td>
                    <td><SeverityChip value={a.severity} /></td>
                    <td><StatusChip value={a.status} /></td>
                    <td>{fmt(a.alert_created_at)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </motion.div>
  );
}
