---
name: omni-auth
description: Manage API key authentication and session tokens. Start here to authenticate requests via Bearer token, obtain session cookies, and configure login requirements for the OmniRoute API.
---
## Overview
Manage API key authentication and session tokens. Start here to authenticate requests via Bearer token, obtain session cookies, and configure login requirements for the OmniRoute API.

## Authentication
Remote API requests use a Bearer credential. Dashboard login is different: `POST /api/auth/login` accepts a management password and returns an `auth_token` session cookie.

## Endpoints
### POST /api/auth/login
Authenticate user
```bash
curl -X POST https://localhost:20128/api/auth/login \
-H "Content-Type: application/json" \
-c cookie.jar \
-d '{"password":"<management-password>"}'
```

### POST /api/auth/logout
Log out
```bash
CSRF_TOKEN=$(curl -s https://localhost:20128/api/auth/csrf -b cookie.jar | jq -r .token)
curl -X POST https://localhost:20128/api/auth/logout \
-b cookie.jar \
-H "x-omniroute-csrf: $CSRF_TOKEN" \
-H "Content-Type: application/json" \
-d '{}'
```

### GET /api/auth/oidc/login
Start OIDC login for the dashboard admin gate

### GET /api/auth/oidc/callback
Complete OIDC login for the dashboard admin gate

## Payloads
See the full OpenAPI specification at `GET /api/openapi/spec` or `docs/openapi.yaml` for detailed request/response schemas.
