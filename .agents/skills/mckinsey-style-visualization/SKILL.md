---
name: mckinsey-style-visualization
description: 'Turn notes, metrics, and prose into executive-ready visualizations - board slides, reports, proposals, training materials, technical diagrams, and infographics with SVG rendering.'
---
# McKinsey-Style Visualization

Messy notes in. Board-ready slides out.

## Capabilities

- **22 rendering patterns**: waterfall, executive summary, 2x2, scatter, heatmap, Gantt, small multiples, cover, section dividers, agendas, closings
- **SVG slide generation**: Real rendered output, not hand-drawn
- **Animated HTML decks**: Self-contained, keyboard navigation, progress bar
- **PDF export**: Press P in browser to print
- **Japanese support**: CJK text wrapping, dedicated business document profiles

## Slide Patterns

| Pattern | Use Case |
|---------|----------|
| Executive Summary | Key findings, top-line metrics |
| Waterfall | Growth/decline bridge analysis |
| 2x2 Matrix | Priority/impact quadrants |
| Process Flow | Step-by-step workflows |
| Roadmap | Timeline with milestones |
| Gantt | Project schedule with dependencies |
| Small Multiples | Comparative panel views |
| Heatmap | Cross-tabulated data |
| Scatter | Correlation with annotations |

## Usage

```bash
# Scaffold a deck
python3 scripts/scaffold_deck.py board-update -o demo

# Build HTML deck
python3 scripts/build_html_deck.py --manifest demo/deck.json -o demo.html
```
