---
name: omni-models
description: Query available AI models across all configured providers. List models, resolve model aliases, and browse the full model catalog including provider-specific variants.
---
## Overview
Query available AI models across all configured providers. List models, resolve model aliases, and browse the full model catalog including provider-specific variants.

## Authentication
All requests require a valid Bearer token or session cookie.

## Endpoints
### GET /api/v1/models
List available models
```bash
curl https://localhost:20128/api/v1/models \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### GET /api/models
List models (management)
```bash
curl https://localhost:20128/api/models \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### POST /api/models/alias
Create or update a model alias
```bash
curl -X POST https://localhost:20128/api/models/alias \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### GET /api/models/catalog
Get full model catalog
```bash
curl https://localhost:20128/api/models/catalog \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

## Payloads
See the full OpenAPI specification at `GET /api/openapi/spec` or `docs/openapi.yaml` for detailed request/response schemas.
