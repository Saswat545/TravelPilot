---
name: omni-compression
description: Configure RTK (command output), Caveman (prose), and stacked compression modes. Manage language packs, custom rules, and test prompt compression reducing tokens by 60–90%.
---
## Overview
Configure RTK (command output), Caveman (prose), and stacked compression modes. Manage language packs, custom rules, and test prompt compression reducing tokens by 60–90%.

## Authentication
All requests require a valid Bearer token or session cookie.

## Endpoints
### POST /api/compression/preview
Preview compression for a message payload
```bash
curl -X POST https://localhost:20128/api/compression/preview \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### GET /api/compression/language-packs
List Caveman compression language packs
```bash
curl https://localhost:20128/api/compression/language-packs \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### GET /api/compression/rules
List Caveman compression rule metadata
```bash
curl https://localhost:20128/api/compression/rules \
-H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

## Compression Engines
| Engine | Best for | Typical savings |
| --- | --- | --- |
| RTK | Terminal / build / test / git output | 60–90% |
| Caveman | Human prose, chat history | 46% input |
| Stacked (`rtk → caveman`) | Mixed coding sessions | 78–95% |
| MCP accessibility filter | Browser/accessibility tool results | 60–80% |

## Enable RTK (best for coding agents)
```bash
curl -X PUT https://localhost:20128/api/settings/compression \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{ "mode": "rtk", "enabled": true }'
```

## Enable stacked mode (maximum savings)
```bash
curl -X PUT https://localhost:20128/api/settings/compression \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "mode": "stacked",
  "enabled": true,
  "stackedPipeline": ["rtk", "caveman"]
}'
```

## Preview compression
```bash
curl -X POST https://localhost:20128/api/compression/preview \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "mode": "rtk",
  "text": "your text here"
}'
```

## Payloads
See the full OpenAPI specification at `GET /api/openapi/spec` or `docs/openapi.yaml` for detailed request/response schemas.
