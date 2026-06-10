/** TransactionsView.jsx — paginated transaction list */
import { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { useDataStore } from '../../hooks/useDataStore';

const PAGE_SIZE = 50;

function fmtMoney(amount, currency) {
  return `${currency} ${Number(amount).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function fmt(iso) {
  return new Date(iso).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
}

export default function TransactionsView({ searchQuery }) {
  const { store } = useDataStore();
  const [page, setPage] = useState(0);
  const [typeFilter, setTypeFilter] = useState('');

  const txnTypes = useMemo(() => [...new Set(store.transactions.map(t => t.txn_type))].sort(), [store]);

  const filtered = useMemo(() => {
    const q = searchQuery?.toLowerCase() ?? '';
    return store.transactions
      .filter(t => {
        if (typeFilter && t.txn_type !== typeFilter) return false;
        if (!q) return true;
        return t.transaction_id.toLowerCase().includes(q) ||
          t.customer_id.toLowerCase().includes(q) ||
          t.narrative?.toLowerCase().includes(q);
      })
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  }, [store, searchQuery, typeFilter]);

  const pages = Math.ceil(filtered.length / PAGE_SIZE);
  const pageData = filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  return (
    <motion.div className="main-content" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <div className="page-header">
        <div>
          <div className="page-header__title">Transactions</div>
          <div className="page-header__subtitle">{filtered.length} of {store.transactions.length} transactions</div>
        </div>
      </div>

      <div className="filter-bar">
        <span className="filter-bar__label">Type</span>
        <button className={`filter-chip${!typeFilter ? ' active' : ''}`} onClick={() => { setTypeFilter(''); setPage(0); }}>All</button>
        {txnTypes.map(t => (
          <button key={t} className={`filter-chip${typeFilter === t ? ' active' : ''}`} onClick={() => { setTypeFilter(t); setPage(0); }}>{t}</button>
        ))}
      </div>

      <div className="alert-group">
        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr><th>Txn ID</th><th>Customer</th><th>Type</th><th>Dir</th><th>Amount</th><th>Channel</th><th>Country</th><th>Narrative</th><th>Timestamp</th></tr>
            </thead>
            <tbody>
              {pageData.map(t => (
                <tr key={t.transaction_id}>
                  <td><span className="mono">{t.transaction_id}</span></td>
                  <td><span className="mono">{t.customer_id}</span></td>
                  <td>{t.txn_type}</td>
                  <td>
                    <span style={{ color: t.direction === 'INCOMING' ? 'var(--clr-auto)' : 'var(--clr-sar)', fontWeight: 600 }}>
                      {t.direction === 'INCOMING' ? '↓' : '↑'}
                    </span>
                  </td>
                  <td><span className="mono" style={{ fontWeight: 500 }}>{fmtMoney(t.amount, t.currency)}</span></td>
                  <td>{t.channel}</td>
                  <td>{t.country}</td>
                  <td style={{ maxWidth: 200, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{t.narrative}</td>
                  <td>{fmt(t.timestamp)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {pages > 1 && (
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'center' }}>
          <button className="btn btn-ghost" disabled={page === 0} onClick={() => setPage(p => p - 1)}>← Prev</button>
          <span style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>
            Page {page + 1} of {pages}
          </span>
          <button className="btn btn-ghost" disabled={page >= pages - 1} onClick={() => setPage(p => p + 1)}>Next →</button>
        </div>
      )}
    </motion.div>
  );
}
