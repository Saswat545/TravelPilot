---
name: omni-providers
description: "Manage provider connections, API keys, OAuth flows, and connection tests. List, add, update, remove, and test AI provider integrations across OmniRoute's 327-provider catalog."
---
## Overview
Manage provider connections, API keys, OAuth flows, and connection tests. List, add, update, remove, and test AI provider integrations across OmniRoute's 327-provider catalog.

## Authentication
All requests require a valid Bearer token or session cookie.

## Endpoints
### GET /api/providers
List provider connections
```bash
curl https://localhost:20128/api/providers \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### POST /api/providers
Create provider connection
```bash
curl -X POST https://localhost:20128/api/providers \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### GET /api/providers/{id}
Get provider connection
```bash
curl https://localhost:20128/api/providers/{id} \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### PATCH /api/providers/{id}
Update provider connection
```bash
curl -X PATCH https://localhost:20128/api/providers/{id} \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### DELETE /api/providers/{id}
Delete provider connection
```bash
curl -X DELETE https://localhost:20128/api/providers/{id} \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### POST /api/providers/{id}/test
Test provider connection
```bash
curl -X POST https://localhost:20128/api/providers/{id}/test \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### POST /api/providers/{id}/refresh
Rotate / refresh OAuth tokens or re-validate credentials
```bash
curl -X POST https://localhost:20128/api/providers/{id}/refresh \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### GET /api/provider-metrics
Retrieve aggregated usage and performance metrics
```bash
curl https://localhost:20128/api/provider-metrics \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### GET /api/providers/health-matrix
Returns a health-matrix view of all providers
```bash
curl https://localhost:20128/api/providers/health-matrix \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

## Payloads
See the full OpenAPI specification at `GET /api/openapi/spec` or `docs/openapi.yaml` for detailed request/response schemas.
