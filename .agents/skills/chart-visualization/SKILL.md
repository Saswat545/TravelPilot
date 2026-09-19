---
name: chart-visualization
description: 'Comprehensive chart generation skill powered by AntV that provides 26+ chart types for intelligent data visualization. Use when creating charts, graphs, or data visualizations.'
---
# Chart Visualization Skills (AntV)

Turning data into a visual language for better thinking with AntV.

## Available Skills

| Skill | Description |
|-------|-------------|
| `chart-visualization` | 26+ chart types: time series, comparisons, part-to-whole, relationships, geographic, hierarchical, statistical |
| `antv-g2-chart` | G2 v5 chart code generator - bar, line, pie, scatter, area, heatmap, and more |
| `antv-g6-graph` | G6 v5 graph visualization - network graphs, tree graphs, flow charts, mind maps |
| `antv-x6-editor` | X6 v3 graph editor - flowcharts, DAGs, ER diagrams, org charts, UML |
| `gpt-vis` | AI-native visualization with natural syntax for LLMs |

## Chart Type Selection

| Data Pattern | Chart Type | Example |
|-------------|-----------|---------|
| Time series | Line, Area | Revenue over months |
| Comparison | Bar, Column | Sales by region |
| Part-to-whole | Pie, Donut, Treemap | Market share |
| Relationship | Scatter, Bubble | Price vs demand |
| Distribution | Histogram, Box plot | User ages |
| Hierarchical | Treemap, Sunburst, Sankey | Category breakdown |
| Geographic | Choropleth, Symbol map | Regional data |
| Statistical | Box plot, Violin, Error bar | Experiment results |

## Usage

```bash
# Generate a G2 chart
npx @antv/g2-spec <data.json>

# Generate a G6 graph
npx @antv/g6-spec <graph-data.json>

# Generate GPT-Vis chart
npx gpt-vis <chart-type> <data>
```

## Key Libraries

- **G2** (v5): Grammar of Graphics - statistical charts
- **G6** (v5): Graph visualization - network/node diagrams
- **X6** (v3): Diagram editor - interactive flowcharts
- **L7**: Geographic visualization - maps
- **S2**: Multidimensional data table - pivot tables
