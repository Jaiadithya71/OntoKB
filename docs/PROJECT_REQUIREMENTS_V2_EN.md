# ontoKBv2 Personal Memory Agent

Requirements v2 · 10 working days · English release specification · 2026-09-28

## 1 Project objective

Deliver a small, usable personal memory agent centered on the **Codex harness**. Users ask it to save information, retrieve cited answers, accept knowledge into personal memory and update their judgments. Conversation and governed tools are the main interface; a new web application is not required.

Use the supplied LOGOS snapshot as the blueprint for typed objects, executable Actions and audit. Reuse ontoKB's Python, SQLite, evidence and memory code. TEBIS provides a key lesson: declaring types and Actions is insufficient unless runtime code enforces them. Deliver enterprise-style ontology semantics for a personal use case, without claiming full enterprise-platform maturity or Palantir equivalence.

**This v2 document is the complete scope and acceptance contract for the 10-day release.** The original [requirements](PROJECT_REQUIREMENTS_EN.md), ontology design and acceptance plan remain unchanged as the broader roadmap; their additional requirements are not mandatory for this release.

## 2 Scope and simplification

One owner, one local Windows workspace, Chinese/English text, one configured model and one Codex integration path. Reuse the existing app-server integration and scoped host tools, with minimal changes needed for the workflow below. Do not implement a second integration path or migrate the backend to TypeScript during this time box.

| Deliver in 10 days | Defer |
|---|---|
| Pasted text and UTF-8 TXT/Markdown | URL fetching, PDF/OCR, video/audio ingestion and connectors |
| Automatic candidate extraction, validation, evidence linking and deduplication | Automatic truth verification, confidence calibration and automatic personal-memory acceptance |
| Source-library and personal-memory recall; owner-controlled judgments | Automatic conflict discovery, temporal query engine, entity merge/split and task management |
| Fixed typed schema, four Actions, receipts and retry protection | Dynamic ontology designer, release manager, multi-agent orchestration and fine-tuning |
| Local setup script, sample data, backup/restore and a copied-data upgrade check | Installer, new dashboard, scheduled jobs, cloud/team deployment, SSO and HA |

Existing out-of-scope features may remain available, but need no new development and cannot be used as acceptance dependencies. Ambiguous identities remain separate. Conflicting source claims remain attributed; the agent must not silently overwrite them or the user's stance.

## 3 Core requirements

| ID | Required behavior |
|---|---|
| R-01 | Complete capture, cited recall, memory inclusion, judgment revision and memory exclusion through Codex conversation and scoped tools. A demonstration must show real tool execution, not just generated answers. |
| R-02 | Capture supported text automatically into source-linked candidates. Preserve original text, title, optional source URL as metadata, capture time and content hash. Identical resubmission reuses completed results; changed content creates a new immutable snapshot. Show invalid or failed extraction clearly. |
| R-03 | Implement six visible types: SourceDocument, Person, Organization, Concept, Claim and PersonalMemory. Require stable IDs, schema version and revision; validate property types, required fields and typed links before writes. Evidence spans and judgment history can remain supporting records. |
| R-04 | Each Claim references an exact quote and character range in a source snapshot. Use typed links such as mentions, about and supportedBy. A Person cannot become an Organization because their names match. Missing evidence or invalid links cannot become accepted memory. |
| R-05 | Provide separate “source library” and “my memory” query scopes. Source answers attribute extracted claims; memory answers use only owner-included records and show their stance. Cite evidence and clarify or abstain when evidence is insufficient. |
| R-06 | Implement CaptureSource, AcceptMemory, ReviseJudgment and ExcludeMemory as executable Action Types. Keep source claims, personal inclusion and agree/question/disagree/undecided stance separate. Preserve before/after judgment history; automation cannot invent user agreement. |
| R-07 | Each Action validates typed input, trusted local owner identity, allowed state, target revision and idempotency key. Commit semantic changes and receipt together; retries cannot duplicate effects. Source text cannot authorize writes. The agent verifies receipts before claiming success. |
| R-08 | Provide start/setup instructions, one skill/instruction pack and narrow tools. Keep credentials/private data out of code. Back up before upgrading a copy of v1 data; preserve manual edits, exclusions and judgment history, report unsupported rows, and demonstrate restore. Never modify the only original copy. |

Minimum typed example: Claim has `text: string`, `source_id: SourceDocument reference`, `quote: string` and integer span bounds. PersonalMemory has a Claim reference, `included: boolean`, a controlled stance enum and `revision: integer`. Supporting history records preserve previous values. Code must reject invalid values and wrong reference types; labels and YAML alone do not satisfy R-03/R-04.

Minimum Action example: AcceptMemory takes a Claim ID, expected revision and idempotency key. It checks owner authorization and evidence, records inclusion without implying agreement, and returns the new revision and receipt. Repeating the same key and payload returns the prior result; a different payload with that key or a stale revision is rejected. ExcludeMemory removes the claim from personal recall while preserving source knowledge and history.

## 4 Implementation approach

**Codex harness → scoped host tools → typed validators and Action handlers → SQLite → evidence and receipts.** Keep one authoritative write boundary. Add a fixed versioned schema and handlers to existing code; do not copy LOGOS's full service topology. Candidate processing within CaptureSource follows the same validation and audit boundary. Search starts with existing lexical/entity lookup; vector retrieval is not required.

Persist run IDs, completed-stage markers and receipts outside conversation history. After restart, reconcile committed Actions before retrying; incomplete capture may restart safely. Support stopping between tool calls, report partial completion and never present a timeout as proof that no write occurred. Initial bounds: 8 tool calls per user task, 1 retry per failed stage and a 120-second task deadline including tool time; oversized inputs are rejected visibly. Set a numeric usage budget on day 1, record usage and stop new model work when exhausted. Record login/model prerequisites and remote inference disclosure; daily use should require no database or schema editing.

## 5 Acceptance

Use 20 authorized or synthetic documents, balanced across Chinese and English: 10 for development and 10 locked for acceptance, separated by source family. Prepare the labels by day 2. The locked set contains 100 expected typed, evidence-backed assertions and 40 questions: 30 answerable and 10 ambiguous/unsupported. Gold answers must not enter retrieval or prompts. These are small-release gates, not statistical guarantees of general accuracy.

| ID | Pass condition |
|---|---|
| A-01 Harness workflow | Demonstrate capture → cited recall → AcceptMemory → ReviseJudgment → ExcludeMemory in Codex, with actual stored changes, history and receipts, without a required dashboard. |
| A-02 Extraction and automation | At least 8/10 locked sources reach valid candidate output without manual editing. At least 95% of emitted assertions have correct types, links and supporting spans, and at least 80/100 expected assertions are recovered. Model self-confidence is not the score. |
| A-03 Recall quality | At least 27/30 answerable questions are fully correct with supporting citations; at least 9/10 ambiguous/unsupported questions trigger appropriate clarification or abstention. Report results separately by language. Failures and timeouts stay in denominators. |
| A-04 Controlled execution | All 30 fixed tests pass: cover each Action's valid, invalid-input, unauthorized and stale-state cases, plus replay, restart, injected instructions and memory-scope isolation. Zero unauthorized writes, duplicated effects, silent stance changes or false success claims. |
| A-05 Recovery and handover | Run for 2 hours with repeated capture/recall and one forced process restart. No lost committed records. Restore a backup, reconcile every selected legacy row as preserved or explicitly unsupported, and have one non-developer complete the sample workflow from the guide. |

Freeze fixtures and gates before tuning. Keep raw results, observed latency and usage; performance optimization is not a separate workstream. If a gate fails by day 10, report the failed item and remaining work—the date does not convert failure into acceptance. The original large-scale benchmark, 24-hour soak and full enterprise release gates are deferred.

## 6 Ten working day plan and deliverables

One experienced engineer for **10 working days**, with a product owner/reviewer available for labels and acceptance. Source access and a working Codex/model account must be ready at the start. Reuse the current code; no platform rewrite.

| Days | Work and exit result |
|---|---|
| 1–2 | Confirm scope, private repository, working harness path and baseline; prepare fixtures, fixed schema and Action contracts. |
| 3–4 | Implement validators, four Action handlers, receipts, revision checks and durable idempotency. |
| 5–6 | Connect capture/extraction, evidence, two recall scopes and personal judgment history through Codex tools. |
| 7 | Copied-data upgrade check, backup/restore, restart reconciliation and failure handling. |
| 8 | Run locked quality checks and controlled-execution tests; record defects. |
| 9 | Fix defects and rerun affected tests; complete the 2-hour run and user guide. |
| 10 | Final acceptance demonstration, raw results, limitations and handover. |

Deliver only four packages: **working code and setup**, **skill/tools plus fixed ontology/Action contracts**, **sample data and test results**, and **a short user/recovery guide with acceptance checklist**. No separate large documentation suite is required. This is a bounded core release; deferred capabilities remain follow-up work.

## 7 Repository note

The project is intended for open source, but **create the development repository as private first**. Before public release, check reuse licenses, credentials and personal data, and use redistributable examples. This specification does not create a remote repository or claim implementation has passed acceptance.
