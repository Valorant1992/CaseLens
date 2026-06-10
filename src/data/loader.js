/**
 * loader.js
 * Loads all 12 JSON files from the /data folder once and returns a frozen store.
 * The /data folder sits at the repo root (one level above the vite project root).
 * Vite's `server.fs.allow: ['..']` makes this work in dev.
 */

const BASE = '/data';

const FILES = [
  'customers',
  'accounts',
  'counterparties',
  'transactions',
  'alerts',
  'alert_transactions',
  'cases',
  'case_alerts',
  'case_events',
  'case_notes',
  'screening_hits',
  'customer_risk_profiles',
];

let _store = null;

export async function loadStore() {
  if (_store) return _store;

  const results = await Promise.all(
    FILES.map(async (name) => {
      const res = await fetch(`${BASE}/${name}.json`);
      if (!res.ok) throw new Error(`Failed to load ${name}.json (${res.status})`);
      return [name, await res.json()];
    })
  );

  _store = Object.fromEntries(results);
  return _store;
}

export function getStore() {
  if (!_store) throw new Error('Store not loaded yet — await loadStore() first');
  return _store;
}
