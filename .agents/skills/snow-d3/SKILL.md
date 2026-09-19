---
name: snow-d3
description: 'Comprehensive D3.js v7 visualization skill covering all 30 modules, patterns, and 30 example chart types. Use when building custom data visualizations with D3.js.'
---
# Snow D3 - D3.js Visualization Skill

Expert-level D3.js v7 knowledge for building production-quality data visualizations.

## D3 Module Coverage

| Category | Modules |
|----------|---------|
| **Core** | selection, transition, fetch, dispatch, timer, interpolate |
| **Arrays** | ascending, bisect, group, shuffle, rollup, ticks |
| **Axes** | axisTop, axisRight, axisBottom, axisLeft |
| **Chords** | chord, ribbon, arc |
| **Collections** | map, set, nest, tuple |
| **Colors** | hsl, lab, rgb, cubehelix |
| **Dispatches** | on, copy, call |
| **Geographies** | geoPath, geoProjection, geoAlbers |
| **Geometries** | arc, area, line, pie, stack, symbol, voronoi |
| **Hierarchies** | cluster, hierarchy, pack, partition, stratify, tree, treemap |
| **Interpolators** | interpolateRgb, interpolateRound, quantize |
| **Paths** | path |
| **Polygons** | polygonHull, polygonCentroid |
- **Quads** | delaunay, quadtree
| **Scales** | scaleBand, scaleLinear, scaleLog, scaleOrdinal, scalePoint, scaleQuantize, scaleSqrt, scaleTime |
| **Shapes** | symbol, linkHorizontal, linkVertical |
| **Time** | timeDay, timeMonth, timeWeek, timeYear |
| **Time Formats** | timeFormat, timeParse |

## 30 Chart Examples

| # | Type | Key Concepts |
|---|------|-------------|
| 01 | Bar Chart | scaleBand, scaleLinear, tooltip, animated sort |
| 02 | Line Chart | scaleTime, line(), curveMonotoneX, Delaunay hover |
| 03 | Area Chart | stack(), area(), streamgraph |
| 04 | Scatter Plot | scaleSqrt, brush(), Delaunay |
| 05 | Pie/Donut | pie(), arc(), arcTween |
| 06 | Histogram | bin(), KDE, adjustable bins |
| 07 | Force Graph | forceSimulation, forceLink, drag() |
| 08 | Tree Layout | d3.tree(), hierarchy, click-collapse |
| 09 | Treemap | treemap(), squarify, breadcrumb |
| 10 | Choropleth | geoNaturalEarth1, scaleSequential |
| 11 | Bubble Chart | pack(), hierarchy, animated zoom |
| 12 | Transitions | enter/update/exit, easing |
| 13 | Brush+Zoom | brushX(), zoom(), linked panels |
| 14 | Chord Diagram | chord(), ribbon(), arc() |
| 15 | Heatmap | scaleSequential, d3-time |
| 16 | Radial Bar | scaleRadial, arc() |
| 17 | Sankey | sankeyLinkHorizontal, flow highlight |
| 18 | Box Plot | bin(), area() KDE, quartile stats |
| 19 | Waterfall | Running totals, positive/negative |
| 20 | Gantt | scaleTime, progress fill, today marker |
| 21 | Parallel Coords | scaleLinear per axis, brushY() |
| 22 | Radar | curveLinearClosed, radial projection |
| 23 | Bump Chart | scalePoint, curveBumpX, rank badges |
| 24 | Sunburst | partition(), hierarchy, click-to-zoom |
| 25 | Voronoi | Delaunay.from(), voronoi() |
| 26 | Contour | contourDensity(), geoPath() |
| 27 | Candlestick | scaleTime, OHLC rendering |
| 28 | Lollipop | bar + circle combination |
| 29 | Matrix | scaleBand for rows/columns |
| 30 | Ridgeline | area() with vertical offset |

## Patterns

- **Margin convention**: `const margin = { top: 20, right: 30, bottom: 40, left: 40 }`
- **Responsive charts**: Use ResizeObserver or container dimensions
- **Tooltips**: Append div to body, use `position: absolute`
- **Data joins**: `.data(data).join('enter', 'update', 'exit')`
- **Zoom**: `d3.zoom().scaleExtent([1, 8]).on('zoom', zoomed)`
- **Brush**: `d3.brushX().extent([[0, 0], [width, height]])`
