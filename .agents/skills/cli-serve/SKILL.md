---
name: cli-serve
description: Start, stop, and restart the OmniRoute server from the CLI. Manage daemon mode, port configuration, auto-recovery, system tray integration, and the dashboard open shortcut.
---
## Overview
Start, stop, and restart the OmniRoute server from the CLI. Manage daemon mode, port configuration, auto-recovery, system tray integration, and the dashboard open shortcut.

## Quick install
```bash
npm install -g omniroute # or: npx omniroute
omniroute --version
```

## Subcommands
### `dashboard`
```bash
omniroute dashboard
```

### `restart`
```bash
omniroute restart
```

### `serve`
```bash
omniroute serve
```
Flags: `--port <port>`, `--no-open`, `--daemon`, `--log`, `--no-recovery`, `--max-restarts <n>`, `--tray`, `--no-tray`, `--tls-cert <path>`, `--tls-key <path>`

### `stop`
```bash
omniroute stop
```

## Server lifecycle
```bash
omniroute           # Start server (default port 20128)
omniroute serve     # Explicit alias
omniroute --port 3000   # Override port
omniroute --no-open     # Don't auto-open browser
omniroute --mcp         # Start as MCP server (stdio transport)
omniroute stop          # Stop the running server
omniroute restart       # Restart the server
omniroute dashboard     # Open dashboard in browser
omniroute status        # Runtime status (uptime, requests, providers)
```

## Setup & provisioning
```bash
omniroute setup     # Step-by-step interactive setup
omniroute doctor    # Full health check
omniroute backup    # Snapshot config + SQLite DB
omniroute restore   # Restore from a previous snapshot
```

## Connection
Every CLI command reads:
| Source | Variable / Flag |
| --- | --- |
| Base URL | `OMNIROUTE_BASE_URL` or `--base-url` |
| API key | `OMNIROUTE_API_KEY` or `--api-key` |

Default base URL: `http://localhost:20128`

## Errors
- `Connection refused` → server not running; run `omniroute` or `omniroute serve`
- `401 Unauthorized` → wrong or missing API key
- `command not found: omniroute` → not in PATH; check `npm root -g` or re-install
