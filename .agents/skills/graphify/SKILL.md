---
name: graphify
description: >
  Turn any folder of files into a navigable knowledge graph with community
  detection, an honest audit trail, and three outputs: interactive HTML,
  GraphRAG-ready JSON, and a plain-language GRAPH_REPORT.md. Works on code
  (tree-sitter AST), docs, PDFs, images, videos, and research papers.
trigger: /graphify
---

# /graphify

Turn any folder of files into a navigable knowledge graph with community
detection, an honest audit trail, and three outputs: interactive HTML,
GraphRAG-ready JSON, and a plain-language GRAPH_REPORT.md.

## Usage

```
/graphify                    # full pipeline on current directory → Obsidian vault
/graphify <path>             # full pipeline on specific path
/graphify <path> --mode deep # thorough extraction, richer INFERRED edges
/graphify <path> --update    # incremental - re-extract only new/changed files
/graphify <path> --cluster-only  # rerun clustering on existing graph
/graphify <path> --no-viz    # skip visualization, just report + JSON
/graphify <path> --svg       # also export graph.svg (embeds in Notion, GitHub)
/graphify <path> --graphml   # export graph.graphml (Gephi, yEd)
/graphify <path> --neo4j     # generate graphify-out/cypher.txt for Neo4j
/graphify <path> --neo4j-push bolt://localhost:7687  # push directly to Neo4j
/graphify <path> --mcp       # start MCP stdio server for agent access
/graphify <path> --watch     # watch folder, auto-rebuild on code changes
/graphify add <url>          # fetch URL, save to ./raw, update graph
/graphify query "<question>" # BFS traversal - broad context
/graphify query "<question>" --dfs  # DFS - trace a specific path
/graphify path "A" "B"      # shortest path between two concepts
/graphify explain "Node"    # plain-language explanation of a node
```

## What graphify is for

graphify is built around Andrej Karpathy's /raw folder workflow: drop
anything into a folder - papers, tweets, screenshots, code, notes - and
get a structured knowledge graph that shows you what you didn't know was
connected.

Three things it does that Claude alone cannot:
1. **Persistent graph** - relationships stored in `graphify-out/graph.json` survive across sessions
2. **Honest audit trail** - every edge tagged EXTRACTED, INFERRED, or AMBIGUOUS
3. **Cross-document surprise** - community detection finds connections between concepts in different files

## What You Must Do When Invoked

If no path was given, use `.` (current directory). Do not ask the user for a path.

### Step 1 - Ensure graphify is installed
```bash
python3 -c "import graphify" 2>/dev/null || pip install graphifyy -q --break-system-packages 2>&1 | tail -3
```

### Step 2 - Detect files
```bash
python3 -c "
import json
from graphify.detect import detect
from pathlib import Path
result = detect(Path('INPUT_PATH'))
print(json.dumps(result))
" > .graphify_detect.json
```

Present a clean summary:
```
Corpus: X files · ~Y words
code: N files (.py .ts .go ...)
docs: N files (.md .txt ...)
papers: N files (.pdf ...)
images: N files
```

### Step 3 - Extract entities and relationships

**Part A - Structural extraction for code files** (AST, deterministic, free):
```bash
python3 -c "
import sys, json
from graphify.extract import collect_files, extract
from pathlib import Path
code_files = []
detect = json.loads(Path('.graphify_detect.json').read_text())
for f in detect.get('files', {}).get('code', []):
    code_files.extend(collect_files(Path(f)) if Path(f).is_dir() else [Path(f)])
if code_files:
    result = extract(code_files)
    Path('.graphify_ast.json').write_text(json.dumps(result, indent=2))
    print(f'AST: {len(result[\"nodes\"])} nodes, {len(result[\"edges\"])} edges')
else:
    Path('.graphify_ast.json').write_text(json.dumps({'nodes':[],'edges':[],'input_tokens':0,'output_tokens':0}))
    print('No code files - skipping AST extraction')
"
```

**Part B - Semantic extraction** (parallel subagents for docs/papers/images):
- Use the Agent tool for parallel extraction (MANDATORY - reading files yourself is 5-10x slower)
- Split files into chunks of 20-25
- Dispatch ALL subagents in a single message for parallel execution
- Each subagent extracts nodes, edges, hyperedges with confidence tags

**Part C - Merge AST + semantic into final extraction**

### Step 4 - Build graph, cluster, analyze, generate outputs
```bash
mkdir -p graphify-out
python3 -c "
import sys, json
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json
from pathlib import Path
extraction = json.loads(Path('.graphify_extract.json').read_text())
detection = json.loads(Path('.graphify_detect.json').read_text())
G = build_from_json(extraction)
communities = cluster(G)
cohesion = score_all(G, communities)
# ... generate report, export JSON
"
```

### Step 5 - Label communities
Read `.graphify_analysis.json`. For each community, write a 2-5 word
plain-language name (e.g. "Attention Mechanism", "Training Pipeline").

### Step 6 - Generate Obsidian vault + HTML visualization

## Output files

| File | Purpose |
| --- | --- |
| `graphify-out/GRAPH_REPORT.md` | Highlights, key concepts, surprising connections, suggested questions |
| `graphify-out/graph.json` | Full graph for querying without re-reading files |
| `graphify-out/graph.html` | Interactive HTML visualization (open in browser) |
| `graphify-out/obsidian/` | Obsidian vault with community-colored graph view |
| `graphify-out/obsidian/graph.canvas` | Structured community layout for Obsidian |

## CLI commands

| Command | Description |
| --- | --- |
| `graphify query "<question>"` | BFS traversal for broad context |
| `graphify query "<question>" --dfs` | DFS for tracing specific paths |
| `graphify path "A" "B"` | Shortest path between two concepts |
| `graphify explain "Node"` | Plain-language explanation of a node |
| `graphify add <url>` | Fetch URL and add to corpus |
| `graphify install` | Register skill with AI assistant |
