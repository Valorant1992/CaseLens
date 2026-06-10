/**
 * service.js
 * Pure query helpers that operate on the in-memory store.
 * All functions are stateless — pass the store as first argument.
 *
 * Extension points:
 *   - Replace store lookups with API calls without changing callers.
 *   - Add filters / pagination parameters as needed.
 */

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
const find   = (arr, key, val) => arr.find(x => x[key] === val) ?? null;
const filter = (arr, key, val) => arr.filter(x => x[key] === val);

// ---------------------------------------------------------------------------
// Customer
// ---------------------------------------------------------------------------
export function getCustomerById(store, customerId) {
  const customer = find(store.customers, 'customer_id', customerId);
  if (!customer) return null;

  const accounts = filter(store.accounts, 'customer_id', customerId);
  const profile  = find(store.customer_risk_profiles, 'customer_id', customerId);
  const hits     = getScreeningHitsForCustomer(store, customerId);

  return { customer, accounts, profile, hits };
}

export function getScreeningHitsForCustomer(store, customerId) {
  return filter(store.screening_hits, 'customer_id', customerId);
}

// ---------------------------------------------------------------------------
// Transactions
// ---------------------------------------------------------------------------
export function getTransactionById(store, txnId) {
  return find(store.transactions, 'transaction_id', txnId);
}

export function getTransactionsForAlert(store, alertId) {
  const links = filter(store.alert_transactions, 'alert_id', alertId);
  return links.map(link => ({
    ...link,
    transaction: find(store.transactions, 'transaction_id', link.transaction_id),
  }));
}

// ---------------------------------------------------------------------------
// Alert
// ---------------------------------------------------------------------------
export function getAlertById(store, alertId) {
  const alert = find(store.alerts, 'alert_id', alertId);
  if (!alert) return null;

  const customer    = find(store.customers,    'customer_id', alert.customer_id);
  const account     = find(store.accounts,     'account_id',  alert.account_id);
  const primaryTxn  = find(store.transactions, 'transaction_id', alert.primary_txn_id);
  const allTxns     = getTransactionsForAlert(store, alertId);
  const hits        = getScreeningHitsForCustomer(store, alert.customer_id);
  const counterparty = primaryTxn?.counterparty_id
    ? find(store.counterparties, 'counterparty_id', primaryTxn.counterparty_id)
    : null;

  return { alert, customer, account, primaryTxn, counterparty, allTxns, hits };
}

// ---------------------------------------------------------------------------
// Case
// ---------------------------------------------------------------------------
export function getCaseById(store, caseId) {
  const cas = find(store.cases, 'case_id', caseId);
  if (!cas) return null;

  // Linked alerts
  const caseAlertLinks = filter(store.case_alerts, 'case_id', caseId);
  const alerts = caseAlertLinks.map(link =>
    find(store.alerts, 'alert_id', link.alert_id)
  ).filter(Boolean);

  // Customer enrichment
  const customerData = getCustomerById(store, cas.customer_id);

  // Primary alert enrichment
  const primaryAlertData = getAlertById(store, cas.primary_alert_id);

  // Timeline
  const timeline = getCaseTimeline(store, caseId);

  // Notes
  const notes = getCaseNotes(store, caseId);

  return {
    cas,
    alerts,
    customerData,
    primaryAlertData,
    timeline,
    notes,
  };
}

export function getCaseTimeline(store, caseId) {
  return filter(store.case_events, 'case_id', caseId)
    .slice()
    .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
}

export function getCaseNotes(store, caseId) {
  return filter(store.case_notes, 'case_id', caseId)
    .slice()
    .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
}

// ---------------------------------------------------------------------------
// Dashboard
// ---------------------------------------------------------------------------

/**
 * Groups alerts into three buckets based on case disposition.
 * SAR_CANDIDATE → sar
 * ESCALATED / ESCALATED_TO_L2 / OPEN → escalated
 * AUTO_CLEARED / CLOSED_FALSE_POSITIVE → cleared
 */
export function getGroupedAlerts(store) {
  const sar       = [];
  const escalated = [];
  const cleared   = [];

  store.alerts.forEach(alert => {
    // Find the case for this alert (via case_alerts or cases.primary_alert_id)
    const cas = store.cases.find(
      c => c.primary_alert_id === alert.alert_id ||
           store.case_alerts.some(ca => ca.case_id === c.case_id && ca.alert_id === alert.alert_id)
    );

    const disposition = cas?.disposition ?? null;
    const status = alert.status;

    if (
      disposition === 'SAR_CANDIDATE' ||
      (disposition === null && status === 'ESCALATED')
    ) {
      sar.push({ alert, cas });
    } else if (
      disposition === 'ESCALATED_TO_L2' ||
      status === 'ESCALATED_TO_L2' ||
      cas?.case_status === 'OPEN'
    ) {
      escalated.push({ alert, cas });
    } else {
      cleared.push({ alert, cas });
    }
  });

  return { sar, escalated, cleared };
}

export function getDashboardSummary(store) {
  const grouped = getGroupedAlerts(store);
  return {
    totalAlerts:  store.alerts.length,
    totalCases:   store.cases.length,
    autoCleared:  grouped.cleared.length,
    escalated:    grouped.escalated.length,
    sarCandidate: grouped.sar.length,
    openCases:    store.cases.filter(c => c.case_status === 'OPEN').length,
  };
}

// ---------------------------------------------------------------------------
// Counterparty
// ---------------------------------------------------------------------------
export function getCounterpartyById(store, cpId) {
  return find(store.counterparties, 'counterparty_id', cpId);
}
