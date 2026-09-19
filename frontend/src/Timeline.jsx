import { Icon, getCategoryIcon } from './icons'
import './Timeline.css'

export default function Timeline({ itinerary, chaosResult }) {
  if (!itinerary) return null

  return (
    <div className="timeline">
      <div className="timeline-header">
        <h2>{itinerary.destination}</h2>
        <span className="timeline-header-meta">
          {itinerary.days.length} day{itinerary.days.length > 1 ? 's' : ''} / {itinerary.total_travel_minutes}min travel
        </span>
      </div>

      {itinerary.days.map((day, dayIdx) => (
        <div key={dayIdx} className="day-section">
          <div className="day-label">
            Day {day.day_index + 1} — {new Date(day.date).toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' })}
          </div>

          {day.activities.map((act) => {
            const diffEntry = chaosResult?.repair?.diff_entries?.find(d => d.activity_id === act.id)
            const isRemoved = diffEntry?.type === 'removed'
            const isModified = diffEntry?.type === 'modified'
            const isShifted = diffEntry?.type === 'shifted'

            return (
              <div key={act.id}
                className={`timeline-item ${isRemoved ? 'removed' : ''} ${isModified ? 'modified' : ''} ${isShifted ? 'shifted' : ''}`}>
                <div className="timeline-time">
                  {new Date(act.scheduled_start).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
                  <br />
                  {new Date(act.scheduled_end).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
                </div>
                <div className="timeline-content">
                  <div className="timeline-name">
                    {getCategoryIcon(act.category)}
                    {act.name}
                  </div>
                  <div className="timeline-meta">
                    <span>{act.category}</span>
                    <span className="timeline-meta-dot" />
                    <span>${act.cost}</span>
                    <span className="timeline-meta-dot" />
                    <span>{act.duration_minutes}min</span>
                  </div>
                  {act.travel_time_from_prev > 0 && (
                    <div className="timeline-travel">
                      <Icon name="arrowRight" />
                      {act.travel_time_from_prev.toFixed(0)}min from previous
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      ))}
    </div>
  )
}
