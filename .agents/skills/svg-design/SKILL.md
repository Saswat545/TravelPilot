---
name: svg-design
description: 'Create SVG logos, icons, and graphics. Covers path commands, shape primitives, styling, gradients, masks, sprites, optimization, and animation.'
---
# SVG Design

SVGs are code. Write them by hand like markup: clean, minimal, semantically meaningful.

## Canvas Size Conventions

| Size | Use Case |
|------|----------|
| `0 0 16 16` | Micro icons, favicons |
| `0 0 20 20` | Small UI icons, form elements |
| `0 0 24 24` | Standard icons (most common) |
| `0 0 32 32` | Medium icons, navigation |
| `0 0 48 48` | Large display icons |

**Default to 24x24** unless there's a reason not to.

## SVG Skeleton

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
  fill="none" stroke="currentColor" stroke-width="2"
  stroke-linecap="round" stroke-linejoin="round">
  <!-- content -->
</svg>
```

## Styling Defaults

| Attribute | Icon Default | Logo Default |
|-----------|-------------|--------------|
| `fill` | `none` | varies |
| `stroke` | `currentColor` | `none` or `currentColor` |
| `stroke-width` | `2` | varies |
| `stroke-linecap` | `round` | `round` or `butt` |
| `stroke-linejoin` | `round` | `round` or `miter` |

## Shape vs Path Decision

| Use Shape When | Use Path When |
|----------------|---------------|
| Basic geometric form | Curves, complex outlines |
| Readability matters | Minimize element count |
| Need to animate properties | Combining multiple shapes |
| Will be programmatically modified | Exporting from design tools |
