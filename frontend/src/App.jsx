import { useState, useRef } from 'react'
import { Chart as ChartJS, ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'
import Pipeline from './Pipeline'
import PlanningForm from './PlanningForm'
import Timeline from './Timeline'
import Sidebar from './Sidebar'
import DiffPanel from './DiffPanel'
import './App.css'

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend)

export default function App() {
  const dashboardRef = useRef(null)

  /* Form state */
  const [destination, setDestination] = useState('Tokyo')
  const [startDate, setStartDate] = useState('2024-01-01')
  const [endDate, setEndDate] = useState('2024-01-01')
  const [budget, setBudget] = useState(200)
  const [interests, setInterests] = useState(['culture', 'food'])
  const [numTravelers, setNumTravelers] = useState(1)

  /* Itinerary state — single owner */
  const [itinerary, setItinerary] = useState(null)
  const [resilience, setResilience] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /* Chaos state */
  const [chaosResult, setChaosResult] = useState(null)
  const [chaosLoading, setChaosLoading] = useState(false)
  const [showDiff, setShowDiff] = useState(false)

  /* Pipeline progress */
  const [pipelineStep, setPipelineStep] = useState(0)

  const handlePlan = async () => {
    setLoading(true)
    setError(null)
    setChaosResult(null)
    setShowDiff(false)
    setPipelineStep(1)

    try {
      await new Promise(r => setTimeout(r, 400))
      setPipelineStep(2)

      const res = await fetch('/api/plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ destination, start_date: startDate, end_date: endDate, budget, interests, num_travelers: numTravelers }),
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Failed to plan trip')
      }

      const data = await res.json()
      setItinerary(data)
      setResilience(data.resilience_score)
      setPipelineStep(4)

      setTimeout(() => dashboardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100)
    } catch (err) {
      setError(err.message)
      setPipelineStep(0)
    } finally {
      setLoading(false)
    }
  }

  const handleChaos = async () => {
    setChaosLoading(true)
    setError(null)
    try {
      const res = await fetch('/api/chaos', { method: 'POST' })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Chaos failed')
      }
      setChaosResult(await res.json())
      setShowDiff(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setChaosLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="1em" height="1em">
            <path d="M12 20v2m0-20v2m5 16v2m0-20v2M2 12h2m-2 5h2M2 7h2m16 5h2m-2 5h2M20 7h2M7 20v2M7 2v2" />
            <rect width="16" height="16" x="4" y="4" rx="2" /><rect width="8" height="8" x="8" y="8" rx="1" />
          </svg>
          AI-Powered Trip Intelligence
        </div>
        <h1>TravelPilot</h1>
        <p className="header-sub">
          Intelligent trip planning with algorithmic scheduling, resilience scoring, and autonomous disruption repair.
        </p>
      </header>

      <Pipeline activeStep={pipelineStep} />

      <PlanningForm
        destination={destination} setDestination={setDestination}
        startDate={startDate} setStartDate={setStartDate}
        endDate={endDate} setEndDate={setEndDate}
        budget={budget} setBudget={setBudget}
        interests={interests} setInterests={setInterests}
        numTravelers={numTravelers} setNumTravelers={setNumTravelers}
        onPlan={handlePlan} onChaos={handleChaos}
        loading={loading} chaosLoading={chaosLoading} hasItinerary={!!itinerary}
      />

      {error && (
        <div className="error-banner">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="18" height="18">
            <path d="m21.73 18l-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3M12 9v4m0 4h.01" />
          </svg>
          {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          <div className="spinner" />
          <span>Generating your itinerary...</span>
        </div>
      )}

      {itinerary && !loading && (
        <div className="dashboard" ref={dashboardRef}>
          <Timeline itinerary={itinerary} chaosResult={chaosResult} />
          <Sidebar itinerary={itinerary} resilience={resilience} />
        </div>
      )}

      <DiffPanel chaosResult={chaosResult} show={showDiff} />
    </div>
  )
}
