---
name: preview-d3
description: 'Interactive 2D data visualizations using D3.js with zoom, pan, and custom rendering. Renders visual previews directly in the browser with no servers or external dependencies.'
---
# Preview D3 Skill

Interactive D3.js visualization viewer with built-in zoom, pan, and export capabilities.

## Usage

```bash
# Pipe D3 code
cat visualization.js | ./run.sh

# From a file
./run.sh chart.d3
```

## Features

- **Universal D3 compatibility** - Works with any D3 code
- **Zoom and pan** - Mouse wheel (0.5x to 10x), drag to pan
- **Reset zoom** button
- **Code viewer** toggle
- **Export to SVG** functionality
- **Preserves interactions** - Tooltips, draggable nodes, animations
- **Responsive design** adapts to screen size

## D3 Code Template

```javascript
const container = document.querySelector('#visualization');
const rect = container.getBoundingClientRect();
const width = rect.width;
const height = rect.height;
const margin = { top: 60, right: 40, bottom: 60, left: 60 };

const svg = d3.select('#visualization')
  .append('svg')
  .attr('width', width)
  .attr('height', height);
```
