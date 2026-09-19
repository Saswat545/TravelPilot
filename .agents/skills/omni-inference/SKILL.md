---
name: omni-inference
description: "The core OpenAI-compatible inference endpoints: chat completions, embeddings, images, audio (TTS/STT), moderations, rerank, and the Responses API."
---
## Overview
The core OpenAI-compatible inference endpoints: chat completions, embeddings, images, audio (TTS/STT), moderations, rerank, and the Responses API. The primary integration surface for AI agents.

## Authentication
All requests require a valid Bearer token or session cookie.

## Endpoints
### POST /api/v1/chat/completions
OpenAI-compatible chat completions endpoint
```bash
curl -X POST https://localhost:20128/api/v1/chat/completions \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### POST /api/v1/messages
Anthropic Messages API endpoint
```bash
curl -X POST https://localhost:20128/api/v1/messages \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### POST /api/v1/responses
OpenAI Responses API endpoint
```bash
curl -X POST https://localhost:20128/api/v1/responses \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### POST /api/v1/embeddings
Create embeddings
```bash
curl -X POST https://localhost:20128/api/v1/embeddings \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### POST /api/v1/images/generations
Generate images
```bash
curl -X POST https://localhost:20128/api/v1/images/generations \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### POST /api/v1/audio/speech
Text-to-speech endpoint
```bash
curl -X POST https://localhost:20128/api/v1/audio/speech \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### POST /api/v1/audio/transcriptions
Audio-to-text transcription endpoint
```bash
curl -X POST https://localhost:20128/api/v1/audio/transcriptions \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### POST /api/v1/moderations
Content moderation endpoint
```bash
curl -X POST https://localhost:20128/api/v1/moderations \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### POST /api/v1/rerank
Document reranking endpoint
```bash
curl -X POST https://localhost:20128/api/v1/rerank \
-H "Authorization: Bearer $OMNIROUTE_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

## Payloads
See the full OpenAPI specification at `GET /api/openapi/spec` or `docs/openapi.yaml` for detailed request/response schemas.
