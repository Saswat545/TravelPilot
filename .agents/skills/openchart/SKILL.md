---
name: openchart
description: 'Generate charts, tables, graphs, and Sankey diagrams with OpenChart. Part of the OpenData platform agent skills for data visualizations and design.'
---
# OpenChart Data Visualization

Generate charts, tables, graphs, Sankey diagrams, tilemaps, and geo maps from declarative VizSpec JSON.

## Core Concept

Write a VizSpec JSON object, render with `<Chart>` / `<DataTable>` / `<Graph>` / `<Sankey>` / `<TileMap>` / `<GeoMap>` (React/Vue/Svelte) or `createChart()` / `createTable()` (vanilla JS). The engine validates, compiles, and renders.

## Chart Selection Decision Tree

```
Single KPI / KPI row -> spec.metrics: Metric[]
Temporal x-axis? -> 1 series: line | 2-5 series: line + color | 6+: filter top 5
Categorical + numeric? -> Ranked list: bar (horizontal) | Periodic: bar (vertical) | 2-6 composition: arc
Two numeric columns? -> point (optional size/color for 3rd/4th dims)
Categorical + series + num? -> stacked bar (use color for series)
Distribution/spread? -> box or violin
```

## Mark Types (16)

| Mark | Use Case |
|------|----------|
| `interval` | Bar, column charts |
| `line` | Line charts, time series |
| `area` | Area charts, streamgraphs |
| `point` | Scatter plots, bubble charts |
| `arc` | Pie, donut, rose charts |
| `rect` | Heatmaps, treemaps |
| `cell` | Calendar heatmaps, matrices |
| `tick` | Dot plots, lollipop charts |
| `circle` | Bubble plots |
| `lollipop` | Lollipop charts |
| `range` | Range bars, Gantt charts |
| `waffle` | Waffle charts |
| `text` | Text-based viz |
| `rule` | Reference lines |
| `vector` | Vector fields |
| `box` | Box plots |

## Installation

```bash
npm install @opendata-ai/openchart-core @opendata-ai/openchart-engine
```

## Quick Example

```json
{
  "mark": "interval",
  "encoding": {
    "x": { "field": "category", "type": "nominal" },
    "y": { "field": "value", "type": "quantitative" },
    "color": { "field": "series", "type": "nominal" }
  },
  "data": [
    { "category": "A", "value": 30, "series": "X" },
    { "category": "B", "value": 80, "series": "Y" }
  ]
}
```
