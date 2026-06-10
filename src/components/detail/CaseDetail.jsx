/**
 * CaseDetail.jsx
 * Full case drill-down panel, slides in from the right.
 */
import { useMemo, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDataStore } from '../../hooks/useDataStore';
import { getCaseById } from '../../data/service';
import { SeverityChip, StatusChip, DispositionChip, HitTypeChip, HitStatusChip } from '../shared/Chip';
import SarModal from '../shared/SarModal';

// ---- helpers ----
function fmt(iso, opts = {}) {
  if (!iso) return '—';
  return new Date(iso).toLocaleString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', ...opts,
  });
}

function fmtMoney(amount, currency) {
  if (amount == null) return '—';
  return `${currency ?? ''} ${Number(amount).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function SectionCard({ title, icon, children, noPad = false }) {
  return (
    <div className="section-card">
      <div className="section-card__header">
        {icon && <span>{icon}</span>}
        <span className="section-card__title">{title}</span>
      </div>
      <div className={`section-card__body${noPad ? ' no-pad' : ''}`}>
        {children}
      </div>
    </div>
  );
}

function KvGrid({ items }) {
  return (
    <div className="kv-grid">
      {items.map(([label, value]) => (
        <div className="kv-item" key={label}>
          <div className="kv-item__label">{label}</div>
          <div className="kv-item__value">{value ?? '—'}</div>
        </div>
      ))}
    </div>
  );
}

// ---- Timeline ----
function EventTimeline({ events }) {
  const TYPE_ICONS = {
    CASE_CREATION:      '🗂',
    INVESTIGATION_START:'🔍',
    CASE_ESCALATION:    '⬆️',
    CASE_CLOSURE:       '✅',
    AUTO_RESOLUTION:    '🤖',
    ALERT_ASSOCIATION:  '🔗',
    REGULATORY_REFERRAL:'🏛',
    ACCOUNT_RESTRICTION:'🔒',
    EVIDENCE_GATHERED:  '📋',
    DOCUMENT_REQUEST:   '📄',
    PENDING_RESPONSE:   '⏳',
  };

  return (
    <div className="timeline">
      {events.map(ev => (
        <div className="timeline-item" key={ev.event_id}>
          <div className={`timeline-dot ${ev.event_type}`}>
            {TYPE_ICONS[ev.event_type] ?? '•'}
          </div>
          <div className="timeline-content">
            <div className="flex items-center gap-2">
              <span className="timeline-content__type">{ev.event_type.replace(/_/g, ' ')}</span>
              <span className="timeline-content__actor">· {ev.actor}</span>
            </div>
            <div className="timeline-content__ts">{fmt(ev.timestamp)}</div>
            <div className="timeline-content__details">{ev.details}</div>
          </div>
        </div>
      ))}
      {events.length === 0 && <div className="empty-state">No events recorded</div>}
    </div>
  );
}

// ---- Case Notes ----
function CaseNotes({ notes }) {
  return (
    <div className="note-list">
      {notes.map(n => (
        <div className="note-item" key={n.note_id}>
          <div className="note-item__meta">
            <span className={`note-item__author${n.author.startsWith('SYSTEM') ? ' system' : ''}`}>
              {n.author.startsWith('SYSTEM') ? '🤖' : '👤'} {n.author}
            </span>
            <span className="note-item__ts">{fmt(n.timestamp)}</span>
          </div>
          <div className="note-item__text">{n.note_text}</div>
        </div>
      ))}
      {notes.length === 0 && <div className="empty-state">No notes on this case</div>}
    </div>
  );
}

// ---- Screening Hits ----
function ScreeningHits({ hits }) {
  const ICONS = { PEP: '🏛', SANCTION: '⛔', ADVERSE_MEDIA: '📰' };
  if (!hits.length) return <div className="empty-state">No screening hits</div>;
  return (
    <div>
      {hits.map(h => (
        <div className="hit-row" key={h.hit_id}>
          <div className="hit-row__icon">{ICONS[h.hit_type] ?? '⚠️'}</div>
          <div className="hit-row__content">
            <div className="hit-row__name">{h.matched_name}</div>
            <div className="hit-row__meta">
              {h.source} · Score: {(h.match_score * 100).toFixed(0)}%
              &nbsp;·&nbsp;<HitTypeChip value={h.hit_type} />&nbsp;
              <HitStatusChip value={h.status} />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

// ---- Transaction table ----
function TransactionTable({ allTxns, primaryTxnId, store }) {
  return (
    <div className="table-scroll">
      <table className="data-table">
        <thead>
          <tr>
            <th>Txn ID</th>
            <th>Role</th>
            <th>Type</th>
            <th>Direction</th>
            <th>Amount</th>
            <th>Counterparty</th>
            <th>Channel</th>
            <th>Country</th>
            <th>Timestamp</th>
            <th>Narrative</th>
          </tr>
        </thead>
        <tbody>
          {allTxns.map(({ transaction_id, relationship_type, transaction: txn }) => {
            if (!txn) return null;
            const cp = txn.counterparty_id
              ? store.counterparties.find(c => c.counterparty_id === txn.counterparty_id)
              : null;
            const isPrimary = txn.transaction_id === primaryTxnId;
            return (
              <tr key={transaction_id} style={isPrimary ? { fontWeight: 600, background: 'var(--clr-esc-bg)' } : {}}>
                <td><span className="mono">{txn.transaction_id}</span></td>
                <td>
                  <span className={`chip ${isPrimary ? 'severity-HIGH' : 'status-AUTO_CLEARED'}`} style={{ fontSize: '10px' }}>
                    {isPrimary ? 'TRIGGER' : relationship_type}
                  </span>
                </td>
                <td>{txn.txn_type}</td>
                <td>{txn.direction}</td>
                <td><span className="mono">{fmtMoney(txn.amount, txn.currency)}</span></td>
                <td>{cp ? <>{cp.name}<br/><span className="text-muted" style={{fontSize:'11px'}}>{cp.country} {cp.risk_flag ? '⚠️' : ''}</span></> : '—'}</td>
                <td>{txn.channel}</td>
                <td>{txn.country}</td>
                <td>{fmt(txn.timestamp, { hour: '2-digit', minute: '2-digit', second: undefined })}</td>
                <td style={{ maxWidth: 200, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{txn.narrative}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// ---- Disposition card ----
function DispositionCard({ cas, onGenerateSar }) {
  const ICONS = {
    SAR_CANDIDATE:         '⚠️',
    AUTO_CLEARED:          '✅',
    ESCALATED_TO_L2:       '🔶',
    CLOSED_FALSE_POSITIVE: '❌',
  };
  const DESCS = {
    SAR_CANDIDATE:         'This case meets the threshold for a Suspicious Activity Report. Review investigation notes and confirm with MLRO before filing.',
    AUTO_CLEARED:          'Alert automatically resolved by the rule engine. Supporting evidence confirmed no illicit activity.',
    ESCALATED_TO_L2:       'Case has been escalated to Level 2 for enhanced due diligence. Awaiting investigation outcome.',
    CLOSED_FALSE_POSITIVE: 'Case closed. Alert reviewed and confirmed as a false positive. No further action required.',
  };

  return (
    <div className={`disposition-card ${cas.disposition}`}>
      <div className="disposition-card__icon">{ICONS[cas.disposition] ?? '📋'}</div>
      <div style={{ flex: 1 }}>
        <div className="disposition-card__title">
          <DispositionChip value={cas.disposition} /> &nbsp; {cas.case_status}
        </div>
        <div className="disposition-card__text">{DESCS[cas.disposition]}</div>
        {cas.disposition === 'SAR_CANDIDATE' && (
          <div className="disposition-card__actions">
            <button className="btn btn-danger" onClick={onGenerateSar}>
              ⚡ Generate SAR
            </button>
            <button className="btn btn-ghost">📎 Attach Evidence</button>
          </div>
        )}
        {cas.disposition === 'ESCALATED_TO_L2' && (
          <div className="disposition-card__actions">
            <button className="btn btn-ghost">📎 Add Note</button>
            <button className="btn btn-ghost">📋 Request Documents</button>
          </div>
        )}
      </div>
    </div>
  );
}

// ---- Risk score bar ----
function RiskBar({ score, band }) {
  return (
    <div>
      <div className="flex items-center gap-2 mt-1">
        <div className="risk-bar" style={{ flex: 1 }}>
          <div className="risk-bar__track">
            <div
              className={`risk-bar__fill ${band ?? 'LOW'}`}
              style={{ width: `${Math.min(score ?? 0, 100)}%` }}
            />
          </div>
          <div className="risk-bar__val">{score ?? '—'}</div>
        </div>
      </div>
    </div>
  );
}

// ---- Main CaseDetail ----
export default function CaseDetail({ caseId, onClose }) {
  const { store } = useDataStore();
  const [showSarModal, setShowSarModal] = useState(false);
  const [sarFiled, setSarFiled] = useState(false);

  const data = useMemo(() => getCaseById(store, caseId), [store, caseId]);

  if (!data) {
    return (
      <div className="detail-panel-overlay" onClick={onClose}>
        <div className="detail-panel" onClick={e => e.stopPropagation()}>
          <div className="detail-panel__header"><h2>Not found</h2><button className="detail-panel__close" onClick={onClose}>✕ Close</button></div>
        </div>
      </div>
    );
  }

  const { cas, customerData, primaryAlertData, timeline, notes } = data;
  const { customer, accounts, profile, hits } = customerData ?? {};
  const { alert, allTxns, counterparty } = primaryAlertData ?? {};

  function handleSarConfirm(cid) {
    setSarFiled(true);
    setShowSarModal(false);
    console.log('[SAR] Filing initiated for case:', cid);
    // Extension point: call SAR generation agent here
  }

  return (
    <>
      <AnimatePresence>
        <motion.div
          className="detail-panel-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.18 }}
          onClick={onClose}
        >
          <motion.div
            className="detail-panel"
            initial={{ x: 60, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 60, opacity: 0 }}
            transition={{ duration: 0.22 }}
            onClick={e => e.stopPropagation()}
          >
            {/* Header */}
            <div className="detail-panel__header">
              <span style={{ fontSize: '1.1rem' }}>📁</span>
              <h2>{cas.case_id}</h2>
              {alert && <SeverityChip value={alert.severity} />}
              <DispositionChip value={cas.disposition} />
              <button className="detail-panel__close" onClick={onClose}>✕ Close</button>
            </div>

            <div className="detail-panel__body">

              {/* Disposition */}
              <DispositionCard
                cas={cas}
                onGenerateSar={() => setShowSarModal(true)}
              />
              {sarFiled && (
                <div style={{ background: 'var(--clr-sar-bg)', border: '1px solid var(--clr-sar-border)', borderRadius: 'var(--radius)', padding: '10px 16px', color: 'var(--clr-sar)', fontWeight: 600, fontSize: 'var(--text-sm)' }}>
                  ✅ SAR filing initiated — reference logged with MLRO.
                </div>
              )}

              {/* Alert Summary */}
              {alert && (
                <SectionCard title="Alert Summary" icon="🔔">
                  <KvGrid items={[
                    ['Alert ID',    alert.alert_id],
                    ['Scenario',    alert.scenario_name],
                    ['Type',        alert.alert_type],
                    ['Status',      <StatusChip value={alert.status} />],
                    ['Created',     fmt(alert.alert_created_at)],
                    ['Account',     alert.account_id],
                    ['Primary Txn', alert.primary_txn_id],
                  ]} />
                  <div style={{ marginTop: 'var(--sp-4)', padding: '10px 14px', background: 'var(--bg-subtle)', borderRadius: 'var(--radius)', fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                    <strong>Rule Summary: </strong>{alert.reason_summary}
                  </div>
                </SectionCard>
              )}

              {/* Customer / KYC */}
              {customer && (
                <SectionCard title="Customer & KYC Profile" icon="👤">
                  <KvGrid items={[
                    ['Name',          customer.full_name],
                    ['ID',            customer.customer_id],
                    ['Type',          customer.customer_type],
                    ['Segment',       customer.segment],
                    ['Occupation',    customer.occupation_or_business_type],
                    ['Residence',     customer.residence_country],
                    ['Nationality',   customer.nationality],
                    ['Onboarded',     customer.onboarded_date],
                    ['KYC Rating',    customer.kyc_risk_rating],
                    ['PEP',           customer.pep_flag ? '⚠️ Yes' : 'No'],
                    ['Sanctions',     customer.sanctions_flag ? '⛔ Yes' : 'No'],
                    ['Adverse Media', customer.adverse_media_flag ? '📰 Yes' : 'No'],
                  ]} />
                  {profile && (
                    <div style={{ marginTop: 'var(--sp-4)' }}>
                      <div className="kv-item__label">Risk Score ({profile.risk_band})</div>
                      <RiskBar score={profile.customer_risk_score} band={profile.risk_band} />
                      <div style={{ marginTop: 'var(--sp-2)', fontSize: 'var(--text-xs)', color: 'var(--text-muted)' }}>
                        {profile.risk_rationale}
                      </div>
                      <div style={{ marginTop: 'var(--sp-3)', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--sp-3)' }}>
                        <div><div className="kv-item__label">Expected Monthly Turnover</div><div className="kv-item__value">{fmtMoney(profile.expected_monthly_turnover, '')}</div></div>
                        <div><div className="kv-item__label">Expected Cash Activity</div><div className="kv-item__value">{fmtMoney(profile.expected_cash_activity, '')}</div></div>
                      </div>
                      <div style={{ marginTop: 'var(--sp-2)' }}>
                        <div className="kv-item__label">Expected Geographies</div>
                        <div className="kv-item__value">{profile.expected_geographies?.join(', ')}</div>
                      </div>
                    </div>
                  )}
                </SectionCard>
              )}

              {/* Accounts */}
              {accounts?.length > 0 && (
                <SectionCard title="Linked Accounts" icon="🏦" noPad>
                  <div className="table-scroll">
                    <table className="data-table">
                      <thead>
                        <tr><th>Account ID</th><th>Number</th><th>Type</th><th>Currency</th><th>Country</th><th>Status</th><th>Opened</th></tr>
                      </thead>
                      <tbody>
                        {accounts.map(acc => (
                          <tr key={acc.account_id} style={acc.account_id === alert?.account_id ? { fontWeight: 600, background: 'var(--clr-esc-bg)' } : {}}>
                            <td><span className="mono">{acc.account_id}</span></td>
                            <td><span className="mono">{acc.account_number_masked}</span></td>
                            <td>{acc.account_type}</td>
                            <td>{acc.currency}</td>
                            <td>{acc.branch_country}</td>
                            <td>{acc.status}</td>
                            <td>{acc.opened_date}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </SectionCard>
              )}

              {/* Transactions */}
              {allTxns?.length > 0 && (
                <SectionCard title={`Trigger + Supporting Transactions (${allTxns.length})`} icon="💸" noPad>
                  <TransactionTable allTxns={allTxns} primaryTxnId={alert?.primary_txn_id} store={store} />
                </SectionCard>
              )}

              {/* Screening Hits */}
              <SectionCard title="Screening Hits" icon="🛡" noPad>
                <ScreeningHits hits={hits ?? []} />
              </SectionCard>

              {/* Case Timeline */}
              <SectionCard title="Case Event Timeline" icon="📅" noPad>
                <EventTimeline events={timeline} />
              </SectionCard>

              {/* Case Notes */}
              <SectionCard title="Investigation Notes" icon="📝" noPad>
                <CaseNotes notes={notes} />
              </SectionCard>

            </div>
          </motion.div>
        </motion.div>
      </AnimatePresence>

      {showSarModal && (
        <SarModal
          caseData={{ cas }}
          onConfirm={handleSarConfirm}
          onCancel={() => setShowSarModal(false)}
        />
      )}
    </>
  );
}
