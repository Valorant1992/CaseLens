/** Chip.jsx — severity / status / disposition / hit-type chips */
export default function Chip({ type, value, label }) {
  const cls = `chip ${type}-${value}`;
  return <span className={cls}>{label ?? value}</span>;
}

export function SeverityChip({ value }) {
  const icons = { CRITICAL: '🔴', HIGH: '🟠', MEDIUM: '🟡', LOW: '🟢' };
  return <Chip type="severity" value={value} label={<>{icons[value]} {value}</>} />;
}

export function StatusChip({ value }) {
  const labels = {
    AUTO_CLEARED:    'Auto-Cleared',
    ESCALATED:       'Escalated',
    ESCALATED_TO_L2: 'Escalated L2',
    OPEN:            'Open',
  };
  return <Chip type="status" value={value} label={labels[value] ?? value} />;
}

export function DispositionChip({ value }) {
  const labels = {
    SAR_CANDIDATE:         'SAR Candidate',
    AUTO_CLEARED:          'Auto-Cleared',
    ESCALATED_TO_L2:       'Escalated L2',
    CLOSED_FALSE_POSITIVE: 'False Positive',
  };
  return <Chip type="disposition" value={value} label={labels[value] ?? value} />;
}

export function HitTypeChip({ value }) {
  const icons = { PEP: '🏛', SANCTION: '⛔', ADVERSE_MEDIA: '📰' };
  return <Chip type="hit" value={value} label={<>{icons[value]} {value.replace('_', ' ')}</>} />;
}

export function HitStatusChip({ value }) {
  return <Chip type="hit" value={value} label={value.replace('_', ' ')} />;
}
