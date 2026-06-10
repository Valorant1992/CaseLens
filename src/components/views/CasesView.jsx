/** CasesView.jsx — full cases list */
import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { useDataStore } from '../../hooks/useDataStore';
import { DispositionChip } from '../shared/Chip';

function fmt(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
}

export default function CasesView({ onSelectCase, searchQuery }) {
  const { store } = useDataStore();

  const rows = useMemo(() => {
    const q = searchQuery?.toLowerCase() ?? '';
    return store.cases
      .filter(c => {
        if (!q) return true;
        const cust = store.customers.find(cu => cu.customer_id === c.customer_id);
        return c.case_id.toLowerCase().includes(q) ||
          c.primary_alert_id.toLowerCase().includes(q) ||
          cust?.full_name?.toLowerCase().includes(q);
      })
      .sort((a, b) => new Date(b.opened_at) - new Date(a.opened_at));
  }, [store, searchQuery]);

  return (
    <motion.div className="main-content" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <div className="page-header">
        <div>
          <div className="page-header__title">Cases</div>
          <div className="page-header__subtitle">{rows.length} cases</div>
        </div>
      </div>
      <div className="alert-group">
        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr><th>Case ID</th><th>Primary Alert</th><th>Customer</th><th>Status</th><th>Disposition</th><th>Opened</th><th>Closed</th></tr>
            </thead>
            <tbody>
              {rows.map(c => {
                const cust = store.customers.find(cu => cu.customer_id === c.customer_id);
                return (
                  <tr key={c.case_id} onClick={() => onSelectCase(c.case_id)}>
                    <td><span className="mono">{c.case_id}</span></td>
                    <td><span className="mono">{c.primary_alert_id}</span></td>
                    <td>{cust?.full_name ?? c.customer_id}</td>
                    <td>
                      <span className={`chip ${c.case_status === 'OPEN' ? 'status-OPEN' : 'status-AUTO_CLEARED'}`}>
                        {c.case_status}
                      </span>
                    </td>
                    <td><DispositionChip value={c.disposition} /></td>
                    <td>{fmt(c.opened_at)}</td>
                    <td>{fmt(c.closed_at)}</td>
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
