---
name: data-viz-renderer
description: 'Generate self-contained HTML/SVG infographics from JSON data, including stat cards, bar charts, flow diagrams, and mixed dashboards. 8 color palettes, built-in icons, no external dependencies.'
---
# Data Viz Renderer

Generate self-contained HTML/SVG infographics from JSON data.

## Capabilities

- **Stat cards** - KPI metrics with labels
- **Bar charts** - horizontal/vertical
- **Flow diagrams** - process flows
- **Mixed dashboards** - combined visualizations
- **8 color palettes** - built-in themes
- **Built-in icons** - no external dependencies

## Usage

```json
{
  "type": "dashboard",
  "title": "Q4 Results",
  "items": [
    { "type": "stat", "label": "Revenue", "value": "$1.2M", "delta": "+15%" },
    { "type": "bar", "data": [{"label": "Product A", "value": 45}, ...] }
  ]
}
```

## When to Use

- User requests data visualization, infographics, or charts
- Need a self-contained HTML/SVG output
- Creating dashboards or reports
