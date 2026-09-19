/* Shared Chart.js configuration — single source of truth for all chart styling */

const FONT_SANS = 'Fira Sans, sans-serif'
const FONT_MONO = 'Fira Code, monospace'

export const tooltipConfig = {
  backgroundColor: '#171717',
  titleFont: { family: FONT_SANS, size: 12 },
  bodyFont: { family: FONT_SANS, size: 11 },
  padding: 10,
  cornerRadius: 6,
}

export const legendConfig = (pointStyle = 'rectRounded') => ({
  display: true,
  position: 'bottom',
  labels: {
    font: { family: FONT_SANS, size: 11 },
    color: '#6B7280',
    usePointStyle: true,
    pointStyle,
    padding: 12,
  },
})

export const xAxisConfig = (stacked = false) => ({
  stacked,
  grid: { display: false },
  ticks: { font: { family: FONT_MONO, size: 11 }, color: '#6B7280' },
})

export const yAxisConfig = (stacked = false, callback) => ({
  stacked,
  grid: { color: '#E8ECF0' },
  ticks: {
    font: { family: FONT_MONO, size: 11 },
    color: '#6B7280',
    ...(callback ? { callback } : {}),
  },
})

export const noLegendPlugin = { legend: { display: false }, tooltip: tooltipConfig }
