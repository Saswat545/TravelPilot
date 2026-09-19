---
name: omni-combos-routing
description: Create and manage routing combos with 19 strategies (priority, weighted, round-robin, Auto-combo, and more). Configure fallback chains, test routing outcomes, and retrieve combo metrics.
---
## Overview
Create and manage routing combos with 19 strategies. Configure fallback chains, test routing outcomes, and retrieve combo metrics.

## Authentication
All requests require a valid Bearer token or session cookie.

## Endpoints
### GET /api/combos
List routing combos
```bash
curl https://localhost:20128/api/combos \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### POST /api/combos
Create routing combo
```bash
curl -X POST https://localhost:20128/api/combos \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### GET /api/combos/{id}
Get combo by ID
```bash
curl https://localhost:20128/api/combos/{id} \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### PUT /api/combos/{id}
Update combo (partial update)
```bash
curl -X PUT https://localhost:20128/api/combos/{id} \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### DELETE /api/combos/{id}
Delete combo
```bash
curl -X DELETE https://localhost:20128/api/combos/{id} \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### GET /api/combos/metrics
Get combo metrics
```bash
curl https://localhost:20128/api/combos/metrics \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### POST /api/combos/test
Test a combo configuration
```bash
curl -X POST https://localhost:20128/api/combos/test \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

## 19 Routing Strategies
| Strategy | Description |
| --- | --- |
| `priority` | Always use target[0]; fall back on error |
| `weighted` | Distribute by weight percentage |
| `round-robin` | Rotate targets in order |
| `auto` | Auto-Combo scoring across 13 factors |
| `lkgp` | Last-known-good-provider sticky routing |
| `fusion` | Run a panel in parallel and synthesize one judged response |
| `pipeline` | Run a configured sequence of targets as a pipeline |
| `p2c` | Power-of-two choices load balancing |
| `least-used` | Route to the target with the lowest observed usage |
| `cost-optimized` | Pick the cheapest eligible target |
| `headroom` | Prefer targets with more remaining quota |
| `cache-optimized` | Prefer targets with stronger cache affinity |
| `context-relay` | Chain models for very long contexts |
| `context-optimized` | Pick the best model for the request's context size |

## Payloads
See the full OpenAPI specification at `GET /api/openapi/spec` or `docs/openapi.yaml` for detailed request/response schemas.
