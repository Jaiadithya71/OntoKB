# OntoKB v2: Detailed Feature Analysis Document

**Document Identifier**: ONTOKB-DOC-05  
**Version**: 2.0.0  
**Date**: September 2026  
**Status**: Complete Architectural Breakdown  

---

## 1. Executive Summary & System Overview

**OntoKB** is a schema-governed, evidence-grounded personal and research knowledge graph system. Built at the intersection of Large Language Models (LLMs) and Formal Knowledge Representation, it addresses the fundamental flaws of naive Retrieval-Augmented Generation (RAG) and unconstrained LLM information extraction:
1. **Hallucination & Semantic Drift**: Traditional extraction models freely invent node types and relation labels. OntoKB enforces a closed-world Schema.org ontology profile (`ontology/core.yaml`).
2. **Ungrounded Assertions**: Traditional systems extract facts as floating text strings. OntoKB enforces **two-tier graph grounding**, mandating verbatim quote evidence for every knowledge relation.
3. **Loss of Epistemic Boundaries**: Traditional vector databases confuse objective document statements with the reader's personal beliefs. OntoKB provides a dedicated **Personal Memory & Stance System** that strictly isolates source claims from user judgments.
4. **Non-Auditable Modifications**: OntoKB treats knowledge curation as transactional database operations, providing provenance receipts, mutation journals, and an undo stack.

---

## 2. Comprehensive Feature Capability Matrix

| Feature Area | Sub-Feature | Implementation Module | Primary Capabilities |
| :--- | :--- | :--- | :--- |
| **Data Acquisition** | YouTube Transcription | `sources/youtube.py` | Extracts timed subtitles via `youtube-transcript-api`; falls back to local `whisper` audio transcription. |
| | Article Intake | `reading.py`, `api.py` | Validated text ingestion (20–100,000 characters) with source URL provenance. |
| | Anti-Collision ID | `pipeline.py` | Deterministic SHA-256 hashing across `(title, url, text)` preventing duplicate ingestions. |
| **Ontology & Schema** | Schema.org Profile | `ontology/core.yaml` | Hierarchical class definitions (`Thing`, `Person`, `Organization`, `Product`, `DefinedTerm`, `Claim`, etc.). |
| | Domain & Range Validation | `ontology.py` | Type checking on triple endpoints (`subject_type`, `predicate`, `object_type`) with canonical aliases. |
| | Symmetric & Extended Relations | `ontology.py` | Built-in symmetric relations (`competesWith`, `relatedTo`, `contradicts`) and custom local semantics (`develops`, `adopts`, `makesClaim`). |
| **Extraction Engine** | Two-Tier Grounding | `pipeline.py`, `llm.py` | Knowledge Tier (entity-to-entity facts) + Document Tier (`CreativeWork` -> `mentions`/`about` -> `Thing`). |
| | Evidence Anchoring | `models.py`, `graph.py` | Verbatim text quote preservation and confidence scoring per extracted assertion. |
| | Extraction Rejections | `pipeline.py` | Logs ontology violations and out-of-domain extractions for debugging and quality auditing. |
| **Interactive Graph UI** | Guided Summary Walk | `reading.js`, D3.js | Paragraph-by-paragraph graph tour; dynamically lights up step entities and 1-hop neighbors while dimming background nodes. |
| | Global Explore Canvas | `reading.js`, D3.js | Full-canvas force-directed graph with Schema.org type color coding, node search, and zoom/pan controls. |
| | Dynamic Filter Bar | `reading.js` | Hierarchical filtering by layer (`Core`, `Claims`, `Documents`, `All`) and by Schema.org entity type. |
| **Knowledge Editor** | Human Curation UI | `editor.js`, `editing.py` | Visual modal for renaming entities, managing aliases, changing types, and editing relations. |
| | Provenance Protection | `graph.py` | Manual entity edits are flagged in `manual_entities` and protected from automated LLM overwrites. |
| | Transactional Journal | `editing.py`, SQLite | Audit receipts (`edit_history`) recording before/after states with single-step undo support. |
| **Personal Memory** | Stance & Opinion Tracking | `memory.js`, `memory.py` | Assign subjective stances (`agree`, `uncertain`, `disagree`) to claims and relations without altering source facts. |
| | Memory History Journal | `memory.py` | Immutable log of how personal viewpoints evolve over time as new documents are read. |
| | Cross-Document Comparison | `memory.py`, `assistant.py`| Automated LLM reasoning comparing newly ingested content against historical personal stances. |
| **Graph-Guided Chat** | Hybrid Retrieval | `assistant.py`, `api.py` | Entity substring extraction, graph expansion (1-hop/2-hop neighbors), and semantic prompt assembly. |
| | Conversational Memory | `chat_history.py` | Multi-turn contextual chat maintaining entity continuity across turns. |
| **Vault Projection** | Obsidian Markdown Sync | `vault.py` | Automatic generation of Obsidian-compatible Markdown files with YAML frontmatter and `[[wikilinks]]`. |
| **Inference Rules** | Logical Rule Engine | `rules.py`, `rules/default.yaml` | Rule-based inference over the graph store to deduce derived edges and flag contradictions. |

---

## 3. Deep Dive: Content Ingestion & Acquisition Engine

### 3.1 YouTube Video Acquisition Pipeline
Located in [`src/ontokb/sources/youtube.py`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/sources/youtube.py):
1. **URL Normalization**: Accepts multiple YouTube URL formats (`youtube.com/watch?v=...`, `youtu.be/...`, shorts, live, and embed links), extracting the 11-character video ID.
2. **Subtitle Extraction**: Uses `youtube-transcript-api` to query available subtitle tracks, prioritizing user language preferences (Simplified Chinese, Traditional Chinese, English).
3. **Local Audio Fallback (Whisper)**: If no official or auto-generated subtitles exist, OntoKB invokes `yt-dlp` to download the audio stream and triggers local Whisper transcription (`base` or `small` model) to extract transcripts.
4. **Text Caching**: Transcripts are persisted locally under `data/transcripts/youtube/<vid>.txt` to avoid redundant network calls and API limits.

### 3.2 Article Ingestion Pipeline
Located in [`src/ontokb/reading.py`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/reading.py):
1. **Input Validation**: Enforces rigorous bounds: title must be 1–200 characters; raw text must be 20–100,000 characters; URL must adhere to standard `http`/`https` schemes.
2. **Deterministic Content Identity**: Generates a composite SHA-256 fingerprint:
   $$\text{Content ID} = \text{"article:"} + \text{SHA256}(\text{title} \parallel \text{url} \parallel \text{raw\_text})[:24]$$
   If the document already exists in `contents` with status `processed`, the ingestion pipeline short-circuits to avoid duplicate processing.
3. **Concurrency Control**: Implements `_ingest_lock = threading.Lock()` with non-blocking acquisition (`acquire(blocking=False)`), preventing race conditions during concurrent ingestion requests.

---

## 4. Deep Dive: Ontology-Constrained LLM Extraction Pipeline

### 4.1 Closed-World Schema.org Profile
Located in [`ontology/core.yaml`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/ontology/core.yaml) and [`src/ontokb/ontology.py`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/ontology.py):
- **Single-Inheritance Hierarchy**: Every entity type inherits from `Thing`:
  - `Person` (Individual human beings; excludes AI agents and job roles)
  - `Organization` (Corporations, academic labs, standards bodies)
  - `Product` (Physical goods, devices, hardware platforms)
  - `SoftwareApplication` (Named software systems, libraries, compilers, models)
  - `DefinedTerm` (Theoretical concepts, technical mechanisms, categories)
  - `CreativeWork` (Articles, Books, Videos, MediaObjects)
  - `Claim` (Verifiable assertions, predictions, hypotheses, and arguments)
- **Relation Constraints**: Every predicate defines strict `domain` and `range` unions:
  - `worksFor`: `Person` $\to$ `Organization`
  - `develops`: `Organization` $\to$ `[DefinedTerm, SoftwareApplication, Product]`
  - `makes`: `Organization` $\to$ `[Product, SoftwareApplication]`
  - `adopts`: `Organization` $\to$ `[DefinedTerm, SoftwareApplication, Product]`
  - `uses`: `[Product, SoftwareApplication]` $\to$ `[DefinedTerm, SoftwareApplication, Product]`
  - `competesWith`: `Organization` $\to$ `Organization` (Symmetric)
  - `makesClaim`: `[Person, Organization, CreativeWork]` $\to$ `Claim`
  - `supports` / `contradicts`: `Claim` $\to$ `Claim`

### 4.2 Two-Tier Grounded Graph Architecture
Located in [`src/ontokb/pipeline.py`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/pipeline.py):
- **Tier 1 (Knowledge Tier)**: Extracted subject-predicate-object triples representing factual claims between real-world entities.
- **Tier 2 (Document Tier)**: Automatically generated provenance edges connecting the ingested `CreativeWork` node to every extracted entity via `mentions` or `about`.
- **Verbatim Evidence Anchoring**: Triples cannot exist without an accompanying verbatim excerpt from the source text and an extraction confidence score ($[0.0, 1.0]$).

---

## 5. Deep Dive: Dual-Mode Interactive Visualization UI

Located in [`src/ontokb/web/reading.html`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/web/reading.html) and [`src/ontokb/web/reading.js`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/web/reading.js):

### 5.1 Mode 1: Guided Summary Walking (`阅读工作台`)
- **Deterministic Text-to-Graph Alignment**: The article summary is partitioned into distinct sentences. In each sentence, regex token matching identifies mentioned entity names and aliases.
- **Dynamic 1-Hop Focus**:
  $$\text{Active Nodes} = \text{Directly Mentioned Entities} \cup \text{1-Hop Neighborhood}$$
  Non-active nodes are dimmed to opacity `0.09`, while active nodes and connecting edges are highlighted with animated halos and glowing SVG paths.
- **Evidence Drawer**: Clicking "查看证据 ↗" slides open the primary source drawer displaying verbatim citations and source attribution for each active relationship.
- **Autonomous Tour**: The "▶ 开始漫游" feature automatically steps through the summary sentences at configurable intervals (6s, 10s, 15s), panning and zooming the camera smoothly across the knowledge graph.

### 5.2 Mode 2: Global Graph Exploration (`探索图谱`)
- **D3 Force Simulation**: Force-directed layout utilizing `d3.forceSimulation`, `forceLink` (distance 110), `forceManyBody` (charge -240), and `forceCollide` (radius 34).
- **Schema-Based Color Palette**:
  - `Organization`: `#899a69` (Muted Sage)
  - `Person`: `#c4936e` (Warm Ochre)
  - `DefinedTerm`: `#839c9b` (Slate Teal)
  - `SoftwareApplication`: `#a79abb` (Soft Purple)
  - `Claim`: `#b5a475` (Golden Bronze)
  - `Product`: `#D85A30` (Coral Amber)
- **Hierarchical Layer Filtering**: Allows filtering the graph by semantic layer (`All`, `Core Concepts`, `Claims Only`, `Documents Only`) or by specific Schema.org entity classes.

---

## 6. Deep Dive: Transactional Knowledge Editor

Located in [`src/ontokb/editing.py`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/editing.py) and [`src/ontokb/web/editor.js`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/web/editor.js):
- **Human Provenance Immunity**: When a user modifies an entity or relationship, the record is flagged in `manual_entities` or `manual_triples`. Subsequent automated LLM extraction runs are strictly barred from overwriting human decisions.
- **Contextual Entity Operations**:
  - Rename entity (propagates to all connected triples and aliases).
  - Add / remove normalized aliases.
  - Reclassify entity type (validates that all existing incident edges still satisfy domain/range constraints).
  - Soft-delete or hard-delete entities.
- **Contextual Relation Operations**:
  - Edit predicate type (with ontology validation).
  - Retarget subject or object endpoint.
  - Update verbatim evidence quotes.
- **Immutable Edit Journal & Undo**: Every mutation appends an entry to the `edit_history` table containing JSON snapshots of `before_state` and `after_state`. Users can execute single-click rollbacks.

---

## 7. Deep Dive: Epistemic Personal Memory System

Located in [`src/ontokb/memory.py`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/memory.py) and [`src/ontokb/web/memory.js`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/web/memory.js):
- **Core Philosophy**: A personal knowledge base must distinguish between *what a document claims* (objective evidence) and *what the user believes* (subjective stance).
- **Target Key Generation**:
  - Entity target: $\text{SHA256}([\text{kind}, \text{id}, \text{name}, \text{type}])$
  - Triple target: $\text{SHA256}([\text{"triple"}, \text{s.id}, \text{s.name}, \text{predicate}, \text{o.id}, \text{o.name}, \text{source}, \text{evidence}])$
- **Curation Dimensions**:
  - `reviewed`: Boolean indicating whether the user has inspected the assertion.
  - `included`: Boolean indicating whether the item is admitted into the personal memory tier.
  - `stance`: Three-state evaluation: `agree` (accepted truth), `uncertain` (open question), or `disagree` (rejected thesis).
  - `note`: Free-text justification explaining the reader's reasoning.
- **Cross-Document Comparison (`/api/memory/compare`)**: When a new document is ingested, the user can trigger an automated comparative analysis. The LLM compares the claims in the new document against historical personal memory stances, outputting a synthesis report highlighting confirmations, contradictions, and shifts in perspective.

---

## 8. Deep Dive: Graph-Guided Chat & Hybrid RAG Assistant

Located in [`src/ontokb/assistant.py`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/assistant.py) and [`src/ontokb/api.py`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/api.py):
- **Entity Discovery in Unsegmented Text**: Identifies known entity names and aliases within user queries using length-descending greedy substring matching (`_entities_mentioned_in_question`).
- **Graph Expansion**: Performs 1-hop and 2-hop BFS expansions from matched entities, assembling a structured subgraph of facts, evidence quotes, and document titles.
- **Evidence-Preserving Prompting**: Injects exact tabular triples and citations into the LLM system prompt. The model is instructed to formulate its response strictly based on the provided graph context, preventing ungrounded speculation.
- **Conversational State Tracking**: Maintains multi-turn dialog history (`chat_history.py`) to resolve coreferences (e.g. "What did he develop?" correctly binding "he" to the previously discussed Person entity).

---

## 9. Deep Dive: Obsidian Vault Projection & Rules

### 9.1 Obsidian Vault Bi-directional Projection
Located in [`src/ontokb/vault.py`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/vault.py):
- **Markdown Entity Notes**: Automatically projects SQLite graph entities into local Markdown files in the Obsidian vault.
- **Structured YAML Frontmatter**: Embeds type metadata, aliases, ontology URI, review status, and sources.
- **Wikilinks**: Renders relationships as clickable `[[Wikilinks]]` with predicate tags, allowing users to browse their knowledge graph inside Obsidian's native interface.

### 9.2 Rule Engine & Deductive Inference
Located in [`src/ontokb/rules.py`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/src/ontokb/rules.py) and [`rules/default.yaml`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/rules/default.yaml):
- **Rule Declarations**: Specifies logical antecedent-consequent patterns (e.g., if entity $A$ works for $B$, and $B$ develops software $C$, deduce that $A$ participates in developing $C$).
- **Integrity Constraints**: Identifies contradictory assertions and flags ontology inconsistencies for human review.
