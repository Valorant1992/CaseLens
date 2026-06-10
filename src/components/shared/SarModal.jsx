/** SarModal.jsx — confirmation modal before generating SAR */
import { motion, AnimatePresence } from 'framer-motion';

export default function SarModal({ caseData, onConfirm, onCancel }) {
  const { cas } = caseData;

  return (
    <AnimatePresence>
      <motion.div
        className="modal-overlay"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onCancel}
      >
        <motion.div
          className="modal"
          initial={{ scale: 0.94, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.94, opacity: 0 }}
          transition={{ duration: 0.18 }}
          onClick={e => e.stopPropagation()}
        >
          <div className="modal__header">
            <span style={{ fontSize: '1.4rem' }}>⚠️</span>
            <h3>Generate Suspicious Activity Report</h3>
          </div>
          <div className="modal__body">
            <p>
              You are about to generate a SAR for case <strong>{cas.case_id}</strong>.
              This action will be logged in the audit trail and submitted to the
              MLRO for review.
            </p>
            <p style={{ marginTop: '12px' }}>
              <strong>Customer:</strong> {cas.customer_id}<br />
              <strong>Disposition:</strong> {cas.disposition}<br />
              <strong>Opened:</strong> {new Date(cas.opened_at).toLocaleDateString()}
            </p>
            <p style={{ marginTop: '12px', color: 'var(--clr-sar)', fontWeight: 600 }}>
              This action cannot be undone. Confirm only if review is complete.
            </p>
          </div>
          <div className="modal__footer">
            <button className="btn btn-ghost" onClick={onCancel}>Cancel</button>
            <button className="btn btn-danger" onClick={() => onConfirm(cas.case_id)}>
              ⚡ Confirm & Generate SAR
            </button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
