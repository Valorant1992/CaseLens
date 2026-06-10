/**
 * App.jsx
 * Root component — wires together data loading, navigation, and the case detail panel.
 */
import { useState, useMemo } from 'react';
import { DataProvider, useDataStore } from './hooks/useDataStore';
import { getDashboardSummary } from './data/service';
import TopBar      from './components/layout/TopBar';
import Sidebar     from './components/layout/Sidebar';
import Dashboard   from './components/dashboard/Dashboard';
import CaseDetail  from './components/detail/CaseDetail';
import AlertsView  from './components/views/AlertsView';
import CasesView   from './components/views/CasesView';
import CustomersView     from './components/views/CustomersView';
import TransactionsView  from './components/views/TransactionsView';

function AppInner() {
  const { store, loading, error } = useDataStore();
  const [view, setView]           = useState('dashboard');
  const [searchQuery, setSearch]  = useState('');
  const [selectedCase, setSelectedCase] = useState(null);

  const summary = useMemo(
    () => store ? getDashboardSummary(store) : null,
    [store]
  );

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <div>Loading AML dataset…</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="loading-screen">
        <div style={{ color: 'var(--clr-sar)', fontWeight: 600 }}>⛔ Failed to load data</div>
        <div style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)' }}>{error}</div>
        <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', maxWidth: 500, textAlign: 'center' }}>
          Make sure you're running this via <code>npm run dev</code> from the <code>bretton-aml/</code> folder,
          and that the <code>data/</code> folder exists one level up.
        </div>
      </div>
    );
  }

  const sharedViewProps = {
    searchQuery,
    onSelectCase:  setSelectedCase,
    onSelectAlert: (alertId) => {
      // Find the case for this alert and open it
      const cas = store.cases.find(c => c.primary_alert_id === alertId);
      if (cas) setSelectedCase(cas.case_id);
    },
  };

  function renderView() {
    switch (view) {
      case 'dashboard':    return <Dashboard    {...sharedViewProps} />;
      case 'alerts':       return <AlertsView   {...sharedViewProps} />;
      case 'cases':        return <CasesView    {...sharedViewProps} />;
      case 'customers':    return <CustomersView {...sharedViewProps} />;
      case 'transactions': return <TransactionsView {...sharedViewProps} />;
      default:             return <Dashboard    {...sharedViewProps} />;
    }
  }

  return (
    <div className="app-shell">
      <TopBar searchQuery={searchQuery} onSearch={setSearch} />
      <Sidebar activeView={view} onNavigate={setView} summary={summary} />
      {renderView()}
      {selectedCase && (
        <CaseDetail caseId={selectedCase} onClose={() => setSelectedCase(null)} />
      )}
    </div>
  );
}

export default function App() {
  return (
    <DataProvider>
      <AppInner />
    </DataProvider>
  );
}
