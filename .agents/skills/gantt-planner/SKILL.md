---
name: gantt-planner
description: 'Generate interactive HTML Gantt charts with Critical Path Method (CPM) analysis from task lists and dependencies, highlighting the critical path and calculating float times.'
---
# Gantt Planner

Generate interactive HTML Gantt charts with CPM analysis.

## Features

- **Interactive Gantt charts** - task bars, dependencies
- **Critical Path Method (CPM)** - identifies longest path
- **Float time calculation** - slack for each task
- **Critical path highlighting** - visual emphasis
- **Dependency arrows** - task relationships
- **Milestone markers** - key dates
- **Progress tracking** - completion status

## When to Use

- User asks to create a Gantt chart
- Schedule project tasks
- Analyze the critical path
- Visualize dependencies
- Project timelines, milestones, task scheduling

## Data Format

```json
{
  "tasks": [
    { "id": "T1", "name": "Design", "start": "2024-01-01", "duration": 5, "deps": [] },
    { "id": "T2", "name": "Build", "start": "2024-01-06", "duration": 10, "deps": ["T1"] }
  ]
}
```
