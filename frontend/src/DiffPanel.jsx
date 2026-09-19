import { Icon } from './icons'
import './DiffPanel.css'

export default function DiffPanel({ chaosResult, show }) {
  if (!show || !chaosResult) return null

  return (
    <div className="diff-panel">
      <div className="diff-header">
        <Icon name="zap" />
        <h3>Disruption Repair</h3>
      </div>

      <div className="diff-disruption">
        <Icon name="alertTriangle" />
        <span>
          <strong>{chaosResult.disruption.activity_name}</strong> — {chaosResult.disruption.reason}
        </span>
      </div>

      <div className="diff-section-title">Changes Applied</div>
      {chaosResult.repair.diff_entries.map((entry, idx) => (
        <div key={idx} className={`diff-entry ${entry.type}`}>
          <span className="diff-entry-badge">{entry.type}</span>
          <div className="diff-entry-content">
            <div className="diff-entry-name">{entry.activity_name}</div>
            <div className="diff-entry-reason">{entry.reason}</div>
            {entry.old_value && entry.new_value && (
              <div className="diff-entry-values">
                <span className="diff-old">{entry.old_value}</span>
                <span className="diff-arrow">→</span>
                <span className="diff-new">{entry.new_value}</span>
              </div>
            )}
          </div>
        </div>
      ))}

      <div className="diff-explanation">{chaosResult.repair.explanation}</div>

      {chaosResult.repair.degraded && (
        <div className="diff-degraded">
          <Icon name="alertTriangle" />
          <span>Degraded mode: {chaosResult.repair.degradation_reason}</span>
        </div>
      )}
    </div>
  )
}
