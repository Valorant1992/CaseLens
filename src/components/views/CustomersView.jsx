/** CustomersView.jsx */
import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { useDataStore } from '../../hooks/useDataStore';

export default function CustomersView({ searchQuery }) {
  const { store } = useDataStore();

  const rows = useMemo(() => {
    const q = searchQuery?.toLowerCase() ?? '';
    return store.customers.filter(c =>
      !q ||
      c.customer_id.toLowerCase().includes(q) ||
      c.full_name.toLowerCase().includes(q) ||
      c.occupation_or_business_type?.toLowerCase().includes(q)
    );
  }, [store, searchQuery]);

  return (
    <motion.div className="main-content" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <div className="page-header">
        <div>
          <div className="page-header__title">Customers</div>
          <div className="page-header__subtitle">{rows.length} customers in dataset</div>
        </div>
      </div>
      <div className="alert-group">
        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th><th>Name</th><th>Type</th><th>Segment</th>
                <th>KYC Rating</th><th>Risk Score</th><th>PEP</th><th>Sanctions</th><th>Onboarded</th>
              </tr>
            </thead>
            <tbody>
              {rows.map(c => {
                const profile = store.customer_risk_profiles.find(p => p.customer_id === c.customer_id);
                return (
                  <tr key={c.customer_id}>
                    <td><span className="mono">{c.customer_id}</span></td>
                    <td style={{ fontWeight: 500 }}>{c.full_name}</td>
                    <td>{c.customer_type}</td>
                    <td>{c.segment}</td>
                    <td>
                      <span className={`chip severity-${c.kyc_risk_rating === 'HIGH' ? 'HIGH' : c.kyc_risk_rating === 'MEDIUM' ? 'MEDIUM' : 'LOW'}`}>
                        {c.kyc_risk_rating}
                      </span>
                    </td>
                    <td>
                      {profile ? (
                        <span style={{ fontWeight: 600, color: profile.risk_band === 'HIGH' ? 'var(--clr-sar)' : profile.risk_band === 'MEDIUM' ? 'var(--clr-esc)' : 'var(--clr-auto)' }}>
                          {profile.customer_risk_score} <span style={{ fontWeight: 400, color: 'var(--text-muted)', fontSize: 'var(--text-xs)' }}>({profile.risk_band})</span>
                        </span>
                      ) : '—'}
                    </td>
                    <td>{c.pep_flag ? <span style={{ color: 'var(--clr-sar)' }}>⚠️ Yes</span> : 'No'}</td>
                    <td>{c.sanctions_flag ? <span style={{ color: 'var(--clr-sar)' }}>⛔ Yes</span> : 'No'}</td>
                    <td>{c.onboarded_date}</td>
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
