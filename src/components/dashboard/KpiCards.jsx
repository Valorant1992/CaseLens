/** KpiCards.jsx */
import { motion } from 'framer-motion';

const cardVariants = {
  hidden: { opacity: 0, y: 14 },
  visible: i => ({ opacity: 1, y: 0, transition: { delay: i * 0.07, duration: 0.25 } }),
};

export default function KpiCards({ summary }) {
  const cards = [
    { type: 'total',    label: 'Total Alerts',   value: summary.totalAlerts,   meta: `${summary.totalCases} cases open` },
    { type: 'cleared',  label: 'Auto-Cleared',   value: summary.autoCleared,   meta: 'Rule-engine resolved' },
    { type: 'escalated',label: 'Escalated',      value: summary.escalated,     meta: `${summary.openCases} cases open` },
    { type: 'sar',      label: 'SAR Candidates', value: summary.sarCandidate,  meta: 'Requires SAR filing' },
  ];

  return (
    <div className="kpi-grid">
      {cards.map((card, i) => (
        <motion.div
          key={card.type}
          className={`kpi-card ${card.type}`}
          custom={i}
          initial="hidden"
          animate="visible"
          variants={cardVariants}
        >
          <div className="kpi-card__label">{card.label}</div>
          <div className="kpi-card__value">{card.value}</div>
          <div className="kpi-card__meta">{card.meta}</div>
        </motion.div>
      ))}
    </div>
  );
}
