/**
 * useDataStore.js
 * React context + hook for the loaded dataset.
 * Wraps loader.js so components can access the store anywhere.
 */
import { createContext, useContext, useEffect, useState } from 'react';
import { loadStore } from '../data/loader';

const DataContext = createContext(null);

export function DataProvider({ children }) {
  const [store,  setStore]  = useState(null);
  const [error,  setError]  = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStore()
      .then(s => { setStore(s); setLoading(false); })
      .catch(e => { setError(e.message); setLoading(false); });
  }, []);

  return (
    <DataContext.Provider value={{ store, error, loading }}>
      {children}
    </DataContext.Provider>
  );
}

export function useDataStore() {
  const ctx = useContext(DataContext);
  if (!ctx) throw new Error('useDataStore must be used inside <DataProvider>');
  return ctx;
}
