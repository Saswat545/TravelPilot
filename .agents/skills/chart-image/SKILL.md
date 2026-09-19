---
name: chart-image
description: 'Generate publication-quality PNG chart images from data, supporting line, bar, area, candlestick, pie, and heatmap charts. Runs as a lightweight headless Node.js process.'
---
# Chart Image

Generate publication-quality PNG chart images from data without a browser.

## Supported Chart Types

- Line charts
- Bar charts (vertical/horizontal)
- Area charts
- Candlestick charts
- Pie/donut charts
- Heatmaps

## Usage

```bash
# Generate from JSON data
chart-image --type bar --data data.json --output chart.png

# Generate with options
chart-image --type line --data data.json --width 1200 --height 600 --title "Sales Trend"
```

## When to Use

- User asks to visualize data as an image
- Need a static chart for reports/presentations
- Creating a graph for documentation
- Generating a time series plot
