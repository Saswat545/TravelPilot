---
name: story-map-builder
description: 'Generate an interactive HTML user story map visualizing product requirements in Epic > Feature > Story structure, with MoSCoW priority tagging and Release swimlane grouping.'
---
# Story Map Builder

Generate interactive HTML user story maps from product requirements.

## Features

- **Epic > Feature > Story hierarchy** - structured backlog
- **MoSCoW priority tagging** - Must/Should/Could/Won't
- **Release swimlane grouping** - version planning
- **Interactive HTML** - clickable, collapsible
- **Export capabilities** - shareable output

## When to Use

- User mentions story mapping
- Backlog visualization
- MoSCoW priority analysis
- Release planning
- Organizing requirements into a story map

## Data Format

```json
{
  "epics": [
    {
      "name": "User Authentication",
      "features": [
        {
          "name": "Login",
          "priority": "Must",
          "stories": ["Email login", "Password reset"]
        }
      ]
    }
  ]
}
```
