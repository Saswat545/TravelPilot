import { useState } from 'react'
import { Doughnut, Bar } from 'react-chartjs-2'
import { Icon } from './icons'
import { tooltipConfig, legendConfig, xAxisConfig, yAxisConfig, noLegendPlugin } from './charts'
import './Sidebar.css'

function getResilienceColor(score) {
  if (score < 25) return 'strong'
  if (score < 50) return 'good'
  if (score < 75) return 'fragile'
  return 'critical'
}

function getFactorColor(score) {
  if (score > 70) return 'var(--color-destructive)'
  if (score > 40) return 'var(--color-accent)'
  return 'var(--color-success)'
}

/* ---- Resilience Card ---- */
function ResilienceCard({ resilience }) {
  if (!resilience) return null
  return (
    <div className="resilience-card">
      <div className="resilience-label">Resilience Score</div>
      <div className="resilience-score-display">
        <div className={`resilience-number ${getResilienceColor(resilience.overall)}`}>
          {resilience.overall.toFixed(0)}
        </div>
        <div className={`resilience-rating ${getResilienceColor(resilience.overall)}`}>
          {resilience.rating}
        </div>
      </div>
      <div className="resilience-summary">{resilience.summary}</div>
      <div className="resilience-factors">
        {resilience.factors.map((factor, idx) => (
          <div key={idx} className="factor-row">
            <span className="factor-name">{factor.name}</span>
            <div className="factor-bar">
              <div className="factor-bar-fill" style={{ width: `${factor.score}%`, background: getFactorColor(factor.score) }} />
            </div>
            <span className="factor-value">{factor.score.toFixed(0)}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

/* ---- Charts ---- */
function ResilienceGauge({ resilience }) {
  if (!resilience) return null
  const data = {
    labels: ['Fragility', 'Resilience'],
    datasets: [{ data: [resilience.overall, 100 - resilience.overall], backgroundColor: [getFactorColor(resilience.overall), '#E8ECF0'], borderWidth: 0, cutout: '75%' }],
  }
  return (
    <div className="charts-card">
      <div className="charts-card-header"><Icon name="trendingUp" /><h3>Resilience Gauge</h3></div>
      <div className="chart-container"><Doughnut data={data} options={{ responsive: true, maintainAspectRatio: false, plugins: noLegendPlugin }} /></div>
    </div>
  )
}

function ActivityDistribution({ itinerary }) {
  if (!itinerary) return null
  const counts = {}
  itinerary.days.forEach(day => day.activities.forEach(act => { counts[act.category] = (counts[act.category] || 0) + 1 }))
  const labels = Object.keys(counts)
  const colors = ['#171717', '#A16207', '#404040', '#6B7280', '#D4A843', '#9CA3AF', '#374151']
  const data = {
    labels,
    datasets: [{ data: Object.values(counts), backgroundColor: colors.slice(0, labels.length), borderWidth: 2, borderColor: '#FFFFFF' }],
  }
  return (
    <div className="charts-card">
      <div className="charts-card-header"><Icon name="barChart3" /><h3>Activity Mix</h3></div>
      <div className="chart-container"><Doughnut data={data} options={{ responsive: true, maintainAspectRatio: false, cutout: '60%', plugins: { ...noLegendPlugin, legend: legendConfig('circle') } }} /></div>
    </div>
  )
}

function TimeAllocation({ itinerary }) {
  if (!itinerary) return null
  const data = {
    labels: itinerary.days.map((_, i) => `Day ${i + 1}`),
    datasets: [
      { label: 'Activity Time', data: itinerary.days.map(d => d.total_activity_minutes / 60), backgroundColor: '#171717', borderRadius: 4 },
      { label: 'Travel Time', data: itinerary.days.map(d => d.total_travel_minutes / 60), backgroundColor: '#A16207', borderRadius: 4 },
    ],
  }
  const options = {
    responsive: true, maintainAspectRatio: false,
    plugins: { legend: legendConfig('rectRounded'), tooltip: tooltipConfig },
    scales: { x: xAxisConfig(true), y: yAxisConfig(true, v => `${v}h`) },
  }
  return (
    <div className="charts-card">
      <div className="charts-card-header"><Icon name="clock" /><h3>Time Allocation</h3></div>
      <div className="chart-container"><Bar data={data} options={options} /></div>
    </div>
  )
}

function DailyCost({ itinerary }) {
  if (!itinerary) return null
  const data = {
    labels: itinerary.days.map((_, i) => `Day ${i + 1}`),
    datasets: [{ label: 'Cost ($)', data: itinerary.days.map(d => d.activities.reduce((s, a) => s + a.cost, 0)), backgroundColor: '#171717', borderRadius: 4, barThickness: 24 }],
  }
  const options = {
    responsive: true, maintainAspectRatio: false,
    plugins: { ...noLegendPlugin, tooltip: { ...tooltipConfig, callbacks: { label: ctx => `$${ctx.raw}` } } },
    scales: { x: xAxisConfig(), y: yAxisConfig(false, v => `$${v}`) },
  }
  return (
    <div className="charts-card">
      <div className="charts-card-header"><Icon name="barChart3" /><h3>Daily Cost</h3></div>
      <div className="chart-container"><Bar data={data} options={options} /></div>
    </div>
  )
}

/* ---- Budget Card ---- */
function BudgetCard({ itinerary }) {
  if (!itinerary) return null
  return (
    <div className="budget-card">
      <div className="budget-card-header"><Icon name="dollarSign" /><h3>Budget Breakdown</h3></div>
      {itinerary.days.map((day, idx) => (
        <div key={idx} className="budget-row">
          <span className="budget-row-label">Day {idx + 1}</span>
          <span className="budget-row-value">${day.activities.reduce((s, a) => s + a.cost, 0).toFixed(0)}</span>
        </div>
      ))}
      <div className="budget-row budget-total">
        <span className="budget-row-label">Total</span>
        <span className="budget-row-value">${itinerary.total_cost.toFixed(0)}</span>
      </div>
    </div>
  )
}

/* ---- Chat Card ---- */
function ChatCard({ itinerary }) {
  const [chatMessage, setChatMessage] = useState('')
  const [chatHistory, setChatHistory] = useState([])
  const [chatLoading, setChatLoading] = useState(false)

  const handleChat = async () => {
    if (!chatMessage.trim()) return
    const userMsg = chatMessage
    setChatMessage('')
    setChatHistory(prev => [...prev, { role: 'user', content: userMsg }])
    setChatLoading(true)
    try {
      const res = await fetch(`/api/chat?message=${encodeURIComponent(userMsg)}`, { method: 'POST' })
      const data = await res.json()
      setChatHistory(prev => [...prev, { role: 'assistant', content: data.response }])
    } catch {
      setChatHistory(prev => [...prev, { role: 'assistant', content: 'Could not process your question. Please try again.' }])
    } finally {
      setChatLoading(false)
    }
  }

  return (
    <div className="chat-card">
      <div className="chat-card-header"><Icon name="messageCircle" /><h3>Trip Q&A</h3></div>
      <div className="chat-messages">
        {chatHistory.map((msg, idx) => (
          <div key={idx} className={`chat-bubble ${msg.role}`}>{msg.content}</div>
        ))}
        {chatLoading && (
          <div className="chat-bubble assistant"><div className="spinner" style={{ width: 14, height: 14 }} /></div>
        )}
      </div>
      <div className="chat-input-row">
        <input type="text" value={chatMessage} onChange={e => setChatMessage(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleChat()} placeholder="What should I do tomorrow?" />
        <button onClick={handleChat}><Icon name="send" /></button>
      </div>
    </div>
  )
}

/* ---- Sidebar (composed) ---- */
export default function Sidebar({ itinerary, resilience }) {
  return (
    <div className="sidebar">
      <ResilienceCard resilience={resilience} />
      <ResilienceGauge resilience={resilience} />
      <ActivityDistribution itinerary={itinerary} />
      <TimeAllocation itinerary={itinerary} />
      <BudgetCard itinerary={itinerary} />
      <DailyCost itinerary={itinerary} />
      <ChatCard itinerary={itinerary} />
    </div>
  )
}
