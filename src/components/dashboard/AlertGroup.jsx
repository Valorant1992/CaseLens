/**
 * AlertGroup.jsx
 * Collapsible section for one bucket (cleared / escalated / sar).
 */
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { SeverityChip, StatusChip, DispositionChip } from '../shared/Chip';

function fmtDate(iso) {
  return new Date(iso).toLocaleDateString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
  });
}

function fmtAmt(txn) {
  if (!txn) return '—';
  return `${txn.currency} ${Number(txn.amount).toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
}

export default function AlertGroup({
  title, bucket, items, store, onSelectAlert, onSelectCase,
  defaultOpen = true,
}) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div className="alert-group">
      <div className="alert-group__header" onClick={() => setOpen(o => !o)}>
        <span className="alert-group__chevron" style={{ transform: open ? 'rotate(90deg)' : 'none', transition: 'transform .18s' }}>▶</span>
        <span className="alert-group__title">{title}</span>
        <span className={`alert-group__count ${bucket}`}>{items.length}</span>
      </div>

      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            key="content"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.22 }}
            style={{ overflow: 'hidden' }}
          >
            <div className="table-scroll">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Alert</th>
                    <th>Scenario</th>
                    <th>Customer</th>
                    <th>Severity</th>
                    <th>Status</th>
                    <th>Disposition</th>
                    <th>Primary Txn</th>
                    <th>Created</th>
                    <th>Case</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map(({ alert, cas }) => {
                    const cust = store.customers.find(c => c.customer_id === alert.customer_id);
                    const txn  = store.transactions.find(t => t.transaction_id === alert.primary_txn_id);
                    return (
                      <tr key={alert.alert_id} onClick={() => cas ? onSelectCase(cas.case_id) : onSelectAlert(alert.alert_id)}>
                        <td><span className="mono">{alert.alert_id}</span></td>
                        <td>{alert.scenario_name}</td>
                        <td>{cust?.full_name ?? alert.customer_id}</td>
                        <td><SeverityChip value={alert.severity} /></td>
                        <td><StatusChip value={alert.status} /></td>
                        <td>{cas ? <DispositionChip value={cas.disposition} /> : <span className="text-muted">—</span>}</td>
                        <td><span className="mono">{fmtAmt(txn)}</span></td>
                        <td>{fmtDate(alert.alert_created_at)}</td>
                        <td>{cas ? <span className="mono">{cas.case_id}</span> : '—'}</td>
                      </tr>
                    );
                  })}
                  {items.length === 0 && (
                    <tr><td colSpan={9}><div className="empty-state"><div className="empty-state__icon">✅</div>No records in this group</div></td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
