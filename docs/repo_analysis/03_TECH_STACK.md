# ontoKB Technology Stack & Architecture Reference

This document provides a comprehensive technical breakdown of every language, library, framework, protocol, and database system utilized within the **ontoKB** codebase.

---

## 1. Technology Stack Summary Matrix

| Layer | Primary Technology | Version / Requirement | Purpose & Justification |
|---|---|---|---|
| **Language & Runtime** | Python | `>=3.10` (Tested on `3.13.1`) | High-level orchestration, rich ML/NLP ecosystem, and native SQLite support. |
| **Data Modeling** | Pydantic | `>=2.5.0` | Strict data validation, schema enforcement, and JSON-Schema generation for LLM structured outputs. |
| **Ontology & Rules** | PyYAML | `>=6.0.0` | Human-readable schema definition (`ontology/core.yaml`) and forward-chaining rule definitions (`rules/default.yaml`). |
| **Database & Persistence** | SQLite3 | Native (bundled in Python) | Single-file, zero-maintenance relational triple store, alias normalization, and revision-tracked memory store. |
| **Agent Harness** | Codex App-Server | OpenAI Codex Protocol | Subprocess JSON-RPC communication enabling dynamic host-side tool execution while keeping model sandbox read-only. |
| **LLM Provider API** | OpenAI / Anthropic | `openai>=2.40`, `anthropic>=0.116` | Fallback direct API integrations using OpenAI structured outputs (`response_format=ExtractionResult`). |
| **Audio & Video Processing** | `yt-dlp`, `faster-whisper` | `yt-dlp>=2024.1.1`, `faster-whisper>=1.1.0` | YouTube audio/subtitle extraction; local offline speech-to-text fallback transcription. |
| **Web Scraping & Parsing** | `beautifulsoup4`, `requests` | `bs4>=4.12`, `requests>=2.31` | Web article parsing (e.g., Netease tech.163 articles) and general HTML extraction. |
| **HTTP Server** | `http.server.ThreadingHTTPServer` | Native (Standard Library) | Zero-dependency, multi-threaded JSON API and static web server running on port `8765`. |
| **Interactive Graph UI** | D3.js | `v7` (via CDN) | Force-directed SVG knowledge graph visualization, camera transitions, and clustering. |
| **Frontend Framework** | Vanilla Modern JavaScript / CSS | ES6+ / Native CSS Variables | Zero-build frontend (no npm/vite/webpack runtime dependency); bundled dynamically by the Python server. |
| **Personal Knowledge Base**| Obsidian Vault Format | Native Markdown + Frontmatter | Emits human-readable Markdown notes, backlinks, and tags into `vault/`. |
| **Test Suite** | pytest | `>=7.4.0` | 144 unit and integration tests covering graph mutations, LLM schema parsing, and mock Codex interactions. |

---

## 2. Core Backend & Data Modeling

### 2.1 Pydantic Schemas (`src/ontokb/models.py`)
ontoKB relies heavily on Pydantic v2 to ensure strict data validation between unstructured text, LLM outputs, and relational database rows:
* **`ContentItem`**: Captures ingested sources (type, url, title, duration, timestamp, raw text).
* **`ExtractedEntity`**: Defines canonical entity names, Schema.org type, aliases, and property maps.
* **`ExtractedTriple`**: Defines subject, predicate, object, confidence ($[0.0, 1.0]$), and raw textual evidence spans.
* **`ProcessedContent` & `ExtractionResult`**: LLM-facing output formats that enforce valid JSON structure directly from language models using schema-constrained sampling.

### 2.2 Ontology Definition (`ontology/core.yaml`)
* Conforms to a **Schema.org** research profile with domain/range validation rules.
* **Class Hierarchy**:
  * Root: `Thing`
  * Core Subclasses: `Person`, `Organization`, `Product`, `DefinedTerm`, `Event`, `CreativeWork`
  * Media & Knowledge Subclasses: `MediaObject`, `VideoObject`, `Article`, `Book`, `SoftwareApplication`, `Claim`
* **Relation Taxonomy**:
  * Structural: `mentions`, `about`, `citation`
  * Attributions: `author`, `publisher`, `worksFor`
  * Domain Relations: `develops`, `adopts`, `makes`, `uses`, `competesWith`, `makesClaim`, `supports`, `contradicts`

---

## 3. Storage & Relational Database Layer (`src/ontokb/graph.py`)

ontoKB deliberately avoids heavy database servers (like Neo4j or PostgreSQL), storing the entire knowledge graph in an optimized, portable **SQLite3** database file:

### SQLite Schema Architecture
```sql
-- Core Entity Table
CREATE TABLE IF NOT EXISTS entities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    norm_name TEXT NOT NULL UNIQUE,     -- Lowercased, NFKC-normalized for deduplication
    type TEXT NOT NULL,                  -- Schema.org class
    aliases TEXT NOT NULL DEFAULT '[]',  -- JSON array of alternate names
    properties TEXT NOT NULL DEFAULT '{}',-- Key-value JSON map
    sources TEXT NOT NULL DEFAULT '[]',  -- Content IDs that mention this entity
    added_time TEXT NOT NULL DEFAULT ''
);

-- Alias Resolution Index
CREATE TABLE IF NOT EXISTS aliases (
    norm_alias TEXT PRIMARY KEY,
    entity_id INTEGER NOT NULL REFERENCES entities(id)
);

-- Triples (Graph Edges with Provenance)
CREATE TABLE IF NOT EXISTS triples (
    id INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES entities(id),
    predicate TEXT NOT NULL,
    object_id INTEGER NOT NULL REFERENCES entities(id),
    confidence REAL NOT NULL DEFAULT 0.8,
    source TEXT NOT NULL DEFAULT '',     -- Originating content ID
    evidence TEXT NOT NULL DEFAULT '',   -- Verbatim quotation from source
    created_at TEXT NOT NULL DEFAULT '',
    UNIQUE(subject_id, predicate, object_id, source)
);

-- Ingested Source Documents
CREATE TABLE IF NOT EXISTS contents (
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,                  -- video / article
    source TEXT NOT NULL,                -- youtube / netease / other
    url TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'queued',
    meta TEXT NOT NULL DEFAULT '{}'      -- Transcripts, summaries, timestamps
);

-- Manual Curation & Audit Ledger
CREATE TABLE IF NOT EXISTS edit_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    target_id INTEGER NOT NULL,
    before_state TEXT NOT NULL,          -- JSON snapshot before edit
    after_state TEXT NOT NULL,           -- JSON snapshot after edit
    created_at TEXT NOT NULL,
    undone INTEGER NOT NULL DEFAULT 0
);

-- Personal Memory & Subjective Beliefs
CREATE TABLE IF NOT EXISTS personal_memory (
    key TEXT PRIMARY KEY,                -- SHA-256 of target identity
    snapshot TEXT NOT NULL,              -- Frozen snapshot of entity or assertion
    reviewed INTEGER NOT NULL DEFAULT 0, -- Boolean review flag
    included INTEGER NOT NULL DEFAULT 0, -- Boolean personal vault inclusion
    stance TEXT NOT NULL DEFAULT 'unset',-- 'unset' | 'agree' | 'uncertain' | 'disagree'
    note TEXT NOT NULL DEFAULT '',       -- User's reasoning or constraints
    revision INTEGER NOT NULL DEFAULT 0, -- Concurrency version lock
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS memory_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_key TEXT NOT NULL,
    before_state TEXT NOT NULL,
    after_state TEXT NOT NULL,
    source_id TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);
```

### Key Technical Capabilities
* **Unicode Normalization**: Chinese simplified/traditional character unification via normalization mappings (`_CHINESE_VARIANTS`).
* **Atomic Transactions**: Multi-statement edits and backups execute within atomic context managers (`with self.conn:`).
* **Safe Backups**: Before any batch extraction or rewrite, SQLite database files are copied into timestamped snapshots under `backups/analysis-*`.

---

## 4. Agent Harness & Codex Integration (`src/ontokb/codex_backend.py`)

Rather than relying on generic client-side LLM wrappers, ontoKB implements an enterprise-grade agent harness pattern through the **OpenAI Codex CLI app-server**:

```
+-------------------------------------------------------------------------------+
| ontoKB Host Process (Python)                                                  |
|                                                                               |
|  [codex_backend.py]                                                           |
|       |                                                                       |
|   JSON-RPC over stdin/stdout                                                  |
|       |                                                                       |
|       v                                                                       |
|  +-------------------------------------------------------------------------+  |
|  | Codex CLI Subprocess (`codex app-server`)                              |  |
|  |   - Sandbox: "read-only"                                                |  |
|  |   - CWD: Temporary Directory                                            |  |
|  |   - Approvals: Dynamic Tool Protocol                                    |  |
|  +-------------------------------------------------------------------------+  |
|       |                                                                       |
|       | Tool Invocation: {"method": "item/tool/call", "params": {...}}        |
|       v                                                                       |
|  [knowledge_agent.py] (Host Tool Handler)                                     |
|       |                                                                       |
|       +--> kb_list_documents()                                                |
|       +--> kb_read_document()                                                 |
|       +--> kb_query_graph()                                                   |
|       +--> kb_reanalyze_document()                                            |
|       +--> kb_sync_note()                                                     |
|       |                                                                       |
|       v                                                                       |
|  Writes to SQLite DB and Obsidian Vault with verified receipts                |
+-------------------------------------------------------------------------------+
```

### Protocol Specifications
1. **Transport**: Subprocess pipeline (`Popen`) using UTF-8 text streaming over stdin/stdout.
2. **Security Sandbox**: Codex runs in a `read-only` sandbox with no access to arbitrary files or system shells.
3. **Execution Guardrails**:
   * **Turn Limit**: Maximum of 8 tool calls per conversational turn (`tool_calls <= 8`).
   * **Timeout Enforcement**: Monotonic clock watchdog enforcing a 180-second end-to-end task deadline.
   * **Untrusted Data Boundary**: User instructions explicitly inform the model that source content and transcript notes are untrusted data, preventing indirect prompt injection from executing unauthorized tool writes.

---

## 5. Media Processing & Ingestion Engines

### 5.1 YouTube Subtitle & Audio Extraction (`src/ontokb/sources/youtube.py`)
* Uses `yt-dlp` to query video metadata, channel details, and available subtitle tracks (`en`, `zh-Hans`, `zh-Hant`).
* Sanitizes and parses VTT / TTML subtitle formats into normalized sentence chunks.
* **Whisper Audio Fallback**:
  * If no subtitles exist, `yt-dlp` extracts 16kHz mono audio (`.wav`).
  * `faster-whisper` (`whisper-base` or `whisper-small` model) runs local transcription with VAD (Voice Activity Detection) filter.
  * Caches results into `data/transcripts/youtube/<video_id>.json`.

### 5.2 Article Scraping (`src/ontokb/sources/netease.py`)
* Custom extraction logic for news platforms (specifically Netease `tech.163.com`).
* Uses `requests` with custom headers and `BeautifulSoup4` to isolate `<div class="post_body">`, stripping tracking pixels, advertisements, and navigation links.

---

## 6. Forward-Chaining Rule Engine & Obsidian Export

### 6.1 Rule Engine (`src/ontokb/rules.py` & `rules/default.yaml`)
* Implements a deterministic forward-chaining rule engine over graph facts.
* Pattern matches on entities, types, and relations:
  * E.g., If `Person --worksFor--> Organization` and `Organization --develops--> DefinedTerm`, infer `Person --contributesTo--> DefinedTerm`.
* Emits synthesized wiki topics, MOC (Map of Content) pages, and research report alerts.

### 6.2 Obsidian Vault Integration (`src/ontokb/vault.py`)
* Automatically formats and writes Markdown notes structured for **Obsidian**:
  * `vault/Sources/<title>.md`: Ingested document summaries, key points, and metadata frontmatter.
  * `vault/Entities/<name>.md`: Auto-generated entity dossiers with incoming/outgoing links.
  * `vault/Wiki/<topic>.md`: Thematic synthesis.
  * `vault/Knowledge Graph.html`: Self-contained interactive visualization embedded directly inside the Obsidian vault.

---

## 7. Web & Frontend Architecture

### 7.1 Server Architecture (`src/ontokb/api.py`)
* Uses Python's native `ThreadingHTTPServer` to avoid framework bloat (no FastAPI, Flask, or Uvicorn dependencies required).
* Handles RESTful JSON API requests, CORS pre-flights, origin validation (`localhost` / `127.0.0.1` origin locking), and static file injection.

### 7.2 UI Rendering & Libraries
* **D3.js (v7)**: Force-directed simulation (`d3.forceSimulation`), link distance springs, collision detection, and zoom/pan SVG behaviors (`d3.zoom`).
* **Zero Runtime Build**: The HTML template (`reading.html`) dynamically receives injected CSS styles and JavaScript bundles at startup, allowing instant developer iteration without compiling JavaScript bundles.
