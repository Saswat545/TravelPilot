import { Icon } from './icons'
import './PlanningForm.css'

const INTERESTS = ['culture', 'food', 'nature', 'shopping', 'entertainment', 'adventure', 'relaxation']

export default function PlanningForm({
  destination, setDestination,
  startDate, setStartDate,
  endDate, setEndDate,
  budget, setBudget,
  interests, setInterests,
  numTravelers, setNumTravelers,
  onPlan, onChaos,
  loading, chaosLoading, hasItinerary,
}) {
  const toggleInterest = (interest) => {
    setInterests(prev =>
      prev.includes(interest) ? prev.filter(i => i !== interest) : [...prev, interest]
    )
  }

  return (
    <div className="planning-form">
      <div className="form-title">
        <Icon name="mapPin" />
        Trip Parameters
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Destination</label>
          <input type="text" value={destination} onChange={e => setDestination(e.target.value)}
            placeholder="e.g., Tokyo, Paris" />
        </div>
        <div className="form-group">
          <label>Start Date</label>
          <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
        </div>
        <div className="form-group">
          <label>End Date</label>
          <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Budget (USD)</label>
          <input type="number" value={budget} onChange={e => setBudget(Number(e.target.value))} min="0" />
        </div>
        <div className="form-group">
          <label>Travelers</label>
          <input type="number" value={numTravelers} onChange={e => setNumTravelers(Number(e.target.value))} min="1" max="10" />
        </div>
      </div>

      <div className="form-group">
        <label>Interests</label>
        <div className="interests-row">
          {INTERESTS.map(interest => (
            <span key={interest}
              className={`interest-chip ${interests.includes(interest) ? 'selected' : ''}`}
              onClick={() => toggleInterest(interest)}>
              {interest}
            </span>
          ))}
        </div>
      </div>

      <div className="form-actions">
        <button className="btn btn-primary" onClick={onPlan} disabled={loading}>
          {loading ? (
            <><span className="spinner" style={{ width: 14, height: 14 }} /> Planning...</>
          ) : (
            <><Icon name="arrowRight" /> Plan My Trip</>
          )}
        </button>
        {hasItinerary && (
          <button className="btn btn-chaos" onClick={onChaos} disabled={chaosLoading}>
            {chaosLoading ? (
              <><span className="spinner" style={{ width: 14, height: 14, borderTopColor: '#fff' }} /> Processing...</>
            ) : (
              <><Icon name="zap" /> Chaos Mode</>
            )}
          </button>
        )}
      </div>
    </div>
  )
}
