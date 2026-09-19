import { Icon } from './icons'
import './Pipeline.css'

const STEPS = [
  { label: 'Planner Agent', icon: 'settings' },
  { label: 'Scheduler Engine', icon: 'cpu' },
  { label: 'Resilience Score', icon: 'shieldCheck' },
  { label: 'Repair Agent', icon: 'wrench' },
]

export default function Pipeline({ activeStep }) {
  return (
    <div className="pipeline">
      {STEPS.map((step, i) => (
        <div key={i} style={{ display: 'flex', alignItems: 'center' }}>
          <div className={`pipeline-step ${activeStep > i || (activeStep === 4 && i < 4) ? 'active' : ''}`}>
            <span className="pipeline-step-icon">
              <Icon name={step.icon} />
            </span>
            {step.label}
          </div>
          {i < 3 && <div className="pipeline-arrow" />}
        </div>
      ))}
    </div>
  )
}
