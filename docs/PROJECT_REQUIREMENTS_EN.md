# ontoKBv2 Codex Harness Personal Memory with an Executable Enterprise Ontology

Version 1.0 · 2026-09-28 · Miniproject specification

## Project overview

Upgrade ontoKB into a personal memory agent centered on the Codex harness. The primary workflow is asking the agent to capture, recall, compare, review and act through governed tools, with progress, approval when required, interruption and recovery. Ordinary users should not need to design a schema or operate an enterprise platform. Use the supplied `logos-code.zip` as the ontology and governance blueprint: retain source ingestion, publication, typed execution and audit, while adapting its capabilities into harness tools. Preserve ontoKB's capture, evidence, reading, personal stance, history and Obsidian workflows. A conventional web application is not the delivery center; optional evidence and review views support the agent experience.

The user should be able to save an article, video transcript, note or meeting record; obtain structured objects and traceable claims automatically; ask questions about sources or personal memory; understand how new evidence affects earlier judgments; and perform controlled actions such as accepting a memory, updating a judgment or completing a task. The system must distinguish what a source says, what the system has validated, and what the user believes.

“Enterprise ontology” means executable contracts for object types, typed properties, link types, functions, actions, lifecycle rules, policies, provenance and versioned releases. A graph visualization, triples with labels, prompt instructions or YAML definitions alone do not satisfy the project. The design is inspired by Palantir's ontology concepts, not a claim of product equivalence, compatibility or certification. See the official [Ontology overview](https://www.palantir.com/docs/foundry/ontology/overview), [Action types](https://www.palantir.com/docs/foundry/action-types/overview) and [object permissioning](https://www.palantir.com/docs/foundry/object-permissioning/overview).

## Baseline and historical assessment

The baseline is the supplied snapshot, not an assumed latest LOGOS release. Static source inspection establishes the following; live behavior and accuracy remain to be measured.

| Source | Reusable foundation | Upgrade required |
|---|---|---|
| ontoKB | Schema.org application profile, class and relation validation, SQLite storage, source evidence, manual corrections, revision checks, personal-memory judgments and history, article/video ingestion and Obsidian projection | Property-level runtime contracts; stable scoped identity; generic Action execution; durable automation; governed releases; complete evaluation and usable distribution |
| LOGOS ZIP | Typed object, function and Action definitions; domain package; source authority; state and policy models; Connect/Build/Review/Release workflow; runtime routes and receipts | Replace customer-support assumptions with personal-memory semantics; harden contract loading and durable execution; validate security configuration and recovery; simplify deployment |
| TEBIS meeting ZIP | Source spans, candidate review, temporal modeling and explicit registries provide useful examples | Avoid declaration–implementation drift, placeholder paths, and permissions recorded without enforcement. An extracted ActionItem is an object, not an executable Action Type |

ontoKB already has an ontology profile and local “actions” in its rule engine. The gap is the breadth and enforcement of the operational model. TEBIS also contains typed schemas and Action declarations; its shortcomings must be demonstrated by specific runtime gaps rather than described as having no ontology at all. Detailed evidence and ZIP fingerprints are in [Source assessment](SOURCE_ASSESSMENT_EN.md).

## Product scope and intended users

Target researchers, students, engineers and knowledge workers who want a reliable personal memory without becoming ontology administrators. The initial product has one owner per local workspace and supports English and Chinese content and UI. This language choice is a proposed baseline to confirm at project kickoff; Japanese and additional languages are later extensions. “Everyone can use it” means accessible onboarding, understandable workflows, portable data and transparent inference requirements, not unlimited formats, languages or universal automated truth verification.

Release scope is deliberately staged:

| Priority | Required outcome |
|---|---|
| P0 functional pilot | Windows Codex integration with skills and scoped tools; typed ontology runtime; capture and queue; cited recall; personal memory; internal Actions; migration; privacy and reproducible evaluation |
| P1 v2 acceptance | Full documented quality gates; durable scheduled ingestion and review; beginner usability; backup and restore; export/deletion; stable packaging and operations |
| P2 extensions | macOS/Linux product packaging, authenticated shared server, team approvals, extra connectors, OCR, raw-media ASR, enterprise SSO/HA and external writeback |

Full ontoKBv2 acceptance requires P0 and P1. A P0 demonstration is a pilot. The core must avoid unnecessary OS coupling, but cross-platform support is claimed only after testing each supported package. No shared hosting or Netaccess requirement is inherited merely because the WhisperLive reference has one.

## Scope and functional requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-01 | P0 | Provide an inbox for pasted text, Markdown/TXT, text-based PDF and allowlisted article/video URLs. For videos, use available transcripts. Record source, capture time, published time if known, checksum, extraction method and language. Preserve source snapshots; show unsupported or inaccessible content explicitly. |
| FR-02 | P0 | Process asynchronously with persisted stages, progress, retry, cancellation and deduplication. Identical content does not create duplicate claims or consume another model call unnecessarily; changed content creates a new source version. |
| FR-03 | P0 | Validate object properties, enum values, required fields, typed references, link endpoints/cardinality and identity before committing. Unknown types and invalid facts enter a visible quarantine; extraction must not invent published schema. |
| FR-04 | P0 | Resolve identities using stable identifiers, type, context and evidence. Names/aliases are lookup aids, not universal primary keys. Ambiguous same-name people remain separate. Support reviewed merge, split and reversal with reference history. |
| FR-05 | P0 | Store claims with exact source-version/span references, speaker when known, negation, temporal qualification and verification status. Preserve conflicting claims; display disagreements and freshness rather than choosing the latest sentence as truth. |
| FR-06 | P0 | Separate source knowledge, curated personal memory and personal stance. Existing review, inclusion, stance, note and history survive migration. Automation may propose a changed judgment but must not silently record user agreement. |
| FR-07 | P0 | Support cited question answering with explicit modes: source library, my memory and comparison. Query typed objects and time constraints, retrieve source passages, and return answer/clarify/insufficient_evidence/conflict/error. Enforce the selected scope in retrieval and generation. |
| FR-08 | P0 | Execute all semantic mutations through registered, versioned Actions with validated inputs, actor permissions, preconditions, expected revisions, idempotency and receipts. UI, import, worker and agent tools use the same enforcement boundary. |
| FR-09 | P0 | Expose object details, evidence, review queue, memory timeline, internal tasks and Action receipts through conversation and structured tool results. Optional panels support evidence or batch review; no core task requires dashboard navigation or graph manipulation. |
| FR-10 | P1 | Schedule permitted source refreshes and a weekly review draft. Detect changes, contradiction candidates and overdue internal tasks. Deduplicate notifications; report failed sources and incomplete reports. Generate report statements with evidence. |
| FR-11 | P1 | Publish immutable ontology bundles containing schemas, functions, Actions, policies and state models. Compare versions, validate compatibility, run contract tests and migrate before activation. Model-suggested extensions stay proposals until owner approval. |
| FR-12 | P0 | Migrate ontoKB through read-only inventory, backup, dry run, stable ID mapping, validation and staged cutover. Preserve manual corrections, rejected relations and memory snapshots; do not promote unreviewed old knowledge automatically. |
| FR-13 | P1 | Export/import a versioned portable package of sources, objects, links, claims, memories, configuration and permitted history. Keep Obsidian as a readable projection. Provide scoped deletion, projection cleanup and documented backup expiry. |
| FR-14 | P1 | Provide guided Codex/tool setup, account/model checks, a sample workspace, natural-language task examples, clear recovery and source/memory explanations. Support Chinese/English interaction and accessible optional panels. Daily use requires no shell commands, YAML editing or database console. |

P0 ingestion excludes image-only PDFs, DRM-protected material, arbitrary web crawling, live meeting capture and raw audio/video transcription. Existing ontoKB ASR can remain an optional adapter, with separate tests; missing transcripts must not produce an invented summary. External email/calendar/Teams actions are P2 and disabled by default. Internal tasks are sufficient to prove operational Actions in the miniproject.

## Ontology and Action requirements

| ID | Required contract |
|---|---|
| ON-01 | An immutable type identifier and schema version; object primary key; typed required/optional properties; validation and display metadata; owner/workspace scope |
| ON-02 | Named link types with source/target types, inverse semantics where relevant, cardinality, provenance and temporal rules; no universal untyped relation as the default |
| ON-03 | Separate `SourceDocument`, `SourceVersion`, `EvidenceSpan`, `Claim`, `PersonalMemory` and `JudgmentRevision`; claims are attributed assertions, not automatically verified facts |
| ON-04 | Distinguish pure/read functions from state-changing Actions. Every Action declares target/input/output, permission, pre/postconditions, risk, approval rule, handler, retry/idempotency behavior and receipt schema |
| ON-05 | Enforce lifecycle transitions and field-level write ownership. Derived indexes cannot author facts, imported text cannot authorize tools, and a background worker cannot impersonate the owner |
| ON-06 | Publish a bundle only when every required declaration resolves to executable validation/handler code and contract tests. Pin bundle/model/prompt/parser versions per run |

The concrete initial object catalog, Action examples and lifecycle semantics are in [Ontology and Action design](ONTOLOGY_ACTION_DESIGN_EN.md). That appendix is normative for P0/P1 implementation.

## Codex harness usage and integration requirements

The primary acceptance path is an ontoKBv2 skill/tool package used from Codex with an authenticated local ontology service, preferably through MCP. The harness owns conversation, planning and the model/tool loop; the ontology service owns durable knowledge and execution invariants. Merely developing code with Codex, using a Codex model for summaries, or adding chat to a CRUD dashboard does not meet this requirement.

Existing ontoKB `codex_backend.py` invokes `codex app-server` and `knowledge_agent.py` exposes bounded tools. Reuse that experience. If an embedded shell is selected, app-server can provide an alternative thin harness client; an independently implemented agent loop behind a chat widget is not the target. Native Codex integration is required; an embedded shell is optional and separately tested. Official guidance distinguishes exec, SDK and app-server use cases: [Codex as a platform](https://developers.openai.com/blog/codex-as-a-platform). See [App Server](https://learn.chatgpt.com/docs/app-server) for its lifecycle/events. Pin and test the actual interface/version; verify account availability and unattended execution instead of assuming them.

| ID | Mandatory harness behavior |
|---|---|
| HR-01 | Complete capture, cited recall, memory review/inclusion, judgment change, internal task action and weekly review through Codex plus tools without a required web dashboard. |
| HR-02 | Version skills/instructions, tool schemas, adapter, Codex release and model settings. Skills teach workflows; the tool service enforces authorization. |
| HR-03 | Bind trusted owner/workspace/session identity in the host. Tool inputs cannot elevate roles. Offer read tools and narrow Action tools, not arbitrary SQL or unrestricted shell/file access to private storage. |
| HR-04 | Persist run IDs, job checkpoints and receipts outside conversation context. After interruption/restart/compaction, reload canonical state and reconcile before resuming. A chat summary is not personal memory; replay cannot duplicate effects. |
| HR-05 | Support steering, cancellation and limits. Cancel pending work; keep committed Actions visible and undo only through compensation. Scheduled runs use explicit scope/budget and cannot escalate to owner privileges. |
| HR-06 | Bind required approval to the exact Action payload, target revisions, actor and expiry. Source text cannot approve an Action. Avoid repeated confirmation for already-authorized low-risk work. |
| HR-07 | Show progress, evidence, proposed changes and observable outcomes; private chain-of-thought is not required. Claim success only after receipt/readback verification; distinguish committed effects from a later failed response. |
| HR-08 | Test expired login, model outage, protocol mismatch, failed tools, cancellation, interrupted approvals, session mixing and injection. Record authentication/billing mode; do not redistribute a developer's account or assume all users have access. |

Example tasks: “Save these two articles and show uncertain extractions”; “What did I believe last month, and which new evidence challenges it?”; “Accept this claim into memory, with my stance undecided”; “Mark task T-17 complete”; “Prepare this week's review without changing my judgments.” The agent resolves IDs, reads evidence, previews material changes and invokes typed Actions. Acceptance verifies actual operations, not just its response wording.

## Architecture and deployment requirements

Use LOGOS's logical separation while delivering a local ontology tool service and durable worker around the Codex harness. A TypeScript ontology core can adapt LOGOS domain/contracts patterns; reuse useful ontoKB Python parsers through a bounded adapter or port them incrementally. There must be one authoritative mutation boundary. Any optional React evidence/review panel consumes the same contracts and is not required for primary task completion. Bundle service dependencies and provide guided Codex prerequisites and connection diagnostics. Record the final stack and harness transport before implementation.

| Module | Responsibility and boundary |
|---|---|
| Capture and build | Acquire permitted sources, preserve snapshots, parse/chunk/extract candidates and record processing versions |
| Ontology registry and runtime | Load a validated bundle; validate objects/links; authorize and execute Actions; control state transitions |
| Knowledge and recall | Read authorized current or historical object views; combine lexical/vector retrieval where useful with typed/time-aware queries and citation verification |
| Personal memory | Manage owner review, inclusion, stance and revision history without conflating them with source correctness |
| Audit and worker | Persist job state, deduplication keys, Action receipts and outbox records; replay projections after crashes |
| Codex skills and tool adapter | Deliver conversational workflows, map scoped tools to functions/Actions, and return evidence/run IDs/receipts |
| Optional views and exports | Display evidence/review details; project canonical state into Obsidian and search views |

SQLite with foreign keys, transactions, migration tooling and typed application validation is the proposed local system of record. Use a local content store for snapshots and a rebuildable search index. Port LOGOS persistence contracts to local storage; PostgreSQL/OpenSearch/MinIO and multiple API services are not mandatory laptop dependencies. A future shared deployment can implement the same contracts using server storage after isolation/concurrency testing. Choosing Neo4j or adding a graph does not itself establish enterprise ontology semantics.

| ID | Operational requirement |
|---|---|
| NFR-01 | Ship a versioned Windows skill/tool-service package with guided connection, start/stop, health checks, update/rollback and diagnostics. Declare supported Codex versions and per-user login prerequisites. Storage/tool runtime needs no GPU; local model hardware is separately budgeted. |
| NFR-02 | Bind the local API to loopback by default; authenticate local clients, validate origin and prevent browser-origin mutation abuse. Shared access requires real server identity, authorization and transport protection before enablement. |
| NFR-03 | Store credentials outside source/export files using an OS-protected mechanism. Disclose and obtain configuration consent for any remote model data transfer; local storage does not imply local inference. No telemetry or cloud synchronization by default. |
| NFR-04 | Isolate workspaces across storage, retrieval, caches, logs and agent tools. Protect private memory fields and raw source access. Show deletion scope and backup retention; do not claim erasure from an existing offline backup. |
| NFR-05 | Commit object changes, revision increments, receipts and outbox events atomically. Project asynchronously with visible pending status, retry and reconciliation. A failed projection must not be reported as a successful vault update. |
| NFR-06 | Provide encrypted backup support, restoration on a clean workspace, integrity verification and an owner-controlled retention policy. A local append-only audit log is not tamper-proof against the machine administrator. |
| NFR-07 | Record latency, model usage, failed jobs, queue age, review burden, source freshness and cost estimates with redacted diagnostics. Set bounded input sizes, concurrency, retry and model budgets. |

Initial benchmark profile: Windows 11, 4 physical CPU cores, 16 GB RAM and SSD; 10,000 documents, 100,000 objects/claims and 500,000 links in a declared synthetic scale fixture. Record hardware and model location. Scale fixtures measure performance, not factual accuracy. Storage/tools and optional evidence views work without inference; agent tasks show unavailable status when the selected harness/model cannot run. A local-model adapter is a later compatibility option, not a claim that Codex supports every local provider or works offline. It needs separate quality and tool-contract evaluation.

## Automation and precision strategy

Automate capture, parsing, candidate extraction, deterministic validation, low-risk source attribution, deduplication, indexing and review-draft preparation. Escalate identity ambiguity, weak evidence, conflicting information, schema changes, destructive actions and changes of personal stance. Let users batch-review supported proposals rather than edit triples manually.

Use a risk/quality gate with measurable coverage. A model's self-reported confidence is not calibrated correctness. Tune routing thresholds on validation data using source quality, exact evidence alignment, type constraints, identity ambiguity, conflict checks and empirical error rates. Auto-publish only eligible low-risk source assertions with valid evidence and passing calibrated gates. “System validated” means accepted by these checks; it does not mean independently verified truth. Personal memory inclusion remains owner-controlled by default, with any opt-in inclusion rule explicit and separately audited; no rule can synthesize the owner's stance.

Start with the Codex harness and narrow tools using constrained extraction, deterministic validators and lexical/typed retrieval. Add vector retrieval, reranking, verification or extra retrieval rounds only when ablations demonstrate useful accuracy/coverage gains within latency/cost limits. Prefer better parsing, identity resolution, evidence spans and contracts over larger prompts. Initially allow at most 3 retrieval rounds and 8 scoped tool calls per question, with a 30-second total deadline including retries and tool execution. Background ingestion permits 3 attempts per stage and 2 concurrent inference jobs. All limits are configurable and recorded; no failed validation may be bypassed. Multi-agent delegation is optional, shares the same permission/budget envelope and requires measured benefit; it is not a substitute for the core single-agent harness.

Fine-tuning is optional and not on the delivery critical path. Consider it only after labeled errors show a repeatable extraction weakness, data rights are clear and export/runtime compatibility is tested. An initial experiment is capped at two engineering days and one adapter training run within an explicitly allocated compute budget. Keep train/development/acceptance sources separate and retain the untuned baseline.

## Measurement and proposed acceptance targets

All targets below are proposed engineering gates. Freeze scope, hardware, selected model, prompt/bundle versions and numeric budgets after baseline characterization and before candidate tuning. A later change requires a visible scope decision and renewed evaluation; do not lower a gate after seeing the locked test results.

| ID | Metric and denominator | Initial gate |
|---|---|---|
| Q-01 | Correct type assignments / matched gold entities; missing entities separately counted in recall | Type accuracy >=97%; entity recall >=90% |
| Q-02 | Correct extracted relations / all emitted relations; correct / gold relations for recall | Precision >=97%; recall >=85% |
| Q-03 | Correct pairs merged / all automatically merged pairs; recall over gold same-identity pairs | Auto-merge precision >=99%; recall >=80%; no known critical wrong-person merge |
| Q-04 | Claim citations that actually support the claim / all citations; supported factual clauses with citations / all factual clauses | Citation precision >=98%; coverage >=95% |
| Q-05 | Fully correct grounded responses / all answerable questions; failed and timed-out cases remain included | >=90% overall and >=85% in every declared slice |
| Q-06 | Correct clarification/abstention / all insufficient-evidence or ambiguous cases; needless refusal / answerable questions | >=95%; needless refusal <=5% |
| Q-07 | Correct auto-published low-risk assertions / all auto-published assertions; automatically completed eligible sources / all eligible sources | Precision >=99%; automation coverage >=70% at that precision; at least 200 auto-published assertions in locked evaluation |
| Q-08 | Rejection of invalid/unauthorized/stale/duplicate mutation attempts in declared contract and fault cases | 100% correct test outcomes; zero unauthorized writes, duplicate effects or silent loss |
| Q-09 | Correct valid-time and recorded-time answers / all temporal questions | >=95%; all conflict and stance-history critical cases pass |
| Q-10 | Completion by novice users without developer assistance | >=4 of 5 users complete first capture, cited recall and memory review within 15 minutes after installation |
| Q-11 | Warm local search and object detail; full cited answer at concurrency 1 on declared profile | p95 <=1 s search; <=0.5 s detail; <=30 s answer, including provider/network time |
| Q-12 | Eligible 2,000-word English text ingestion, or a frozen equivalent-token Chinese size band, excluding initial download/ASR | p95 <=120 s at worker concurrency 2; track download separately |
| Q-13 | Stable execution, recovery and migration | 24-hour soak without lost committed data/unbounded queue; RPO 0 for committed local DB transactions in process-crash tests; restore from backup <=30 min on scale fixture |

Record API/model token usage and estimated currency cost per source, answer and day. Proposed default guardrails are USD 0.10 per standard 2,000-word ingestion, USD 0.05 per answer and USD 2/day, adjustable by the owner before use and frozen for evaluation. These are spending limits, not vendor price estimates or evidence of affordability with any model. Hard-stop new model work when a limit is reached, counting retries and verification passes; disclose unmetered subscription/local usage separately. Report storage and process-tree RAM, with application RSS <=4 GB excluding an explicitly budgeted local model/ASR process.

## Evaluation plan

Prepare at least 120 authorized or synthetic sources, balanced across English/Chinese and the supported ingestion types, plus at least 1,000 labeled entities, 1,000 relations, 200 identity pairs and 300 questions. Split sources and derivative claims by source family/project into 60 development, 30 validation and 30 locked acceptance sources; do not split neighboring chunks across partitions. Allocate questions 150/75/75 and identity pairs 100/50/50. Expand locked labels as needed to meet the automatic-publication sample gate; small subgroup denominators must remain visible. Include copied/revised sources, namesakes, negation, numbers, stale facts, contradictory claims, personal stances, missing evidence and prompt injection. Add 100 deterministic Action/security/fault cases outside the semantic quality set.

Two reviewers label the locked set and adjudicate material disagreement. The owner validates expected personal-memory behavior. Freeze eligible automation cases before routing so difficult cases cannot be hidden in a new “ineligible” category. Report rejection/review rates over both all inputs and eligible inputs. Keep gold answers out of indexes and prompts; evidence sources remain retrievable as intended. Report raw counts, confidence intervals, per-language/source/difficulty slices, model versions, costs and all failures. Repeat stochastic quality runs three times with fixed declared settings and never report only the best run.

Compare current ontoKB and ontoKBv2 on identical permitted content and equivalent models where possible; disclose differences. Target at least 20% relative reduction in material grounded-answer errors on a predeclared difficult cohort, while satisfying all absolute gates. If the baseline already has zero errors, freeze a replacement outcome such as reduced review time before experimentation. Ablate ontology validation, entity resolution and evidence verification; a visually richer graph is not an improvement metric. The [acceptance plan](ACCEPTANCE_PLAN_EN.md) defines critical failures and evidence requirements.

## Deliverables and indicative schedule

| Stage | Indicative effort | Exit evidence |
|---|---|---|
| M0 baseline and scope | 2–3 engineering days | Private repository setup, snapshot hashes, baseline run, harness/profile/stack selection, labeled-set plan and frozen acceptance contract |
| M1 ontology core | 4–5 days | Executable types/links/Actions/policies, Codex tool integration, runtime rejection cases, release manifest and handler coverage |
| M2 capture and memory | 4–5 days | Durable ingestion, evidence-grounded recall, memory review/history, safe identity resolution |
| M3 migration and automation | 3–4 days | Dry-run mapping, preserved manual state, crash recovery, schedules, weekly review and projections |
| M4 product and acceptance | 4–5 days | Skill/tool package, novice conversational tests, locked evaluation, harness interruption/recovery, soak, export/deletion and handover |

Plan approximately 17–22 engineering days for one experienced engineer, with scheduled product-owner and QA/reviewer availability. This is an estimate after source/model access, not a fixed delivery promise. Start with a narrow end-to-end slice; do not compress contract, migration and quality testing into a cosmetic prototype. Shared-server deployment, enterprise SSO, HA, additional operating systems and external writeback are separately estimated P2 work.

Deliver source and pinned dependencies; architecture decisions; versioned ontology bundle and generated contracts; Codex skills/instructions, tool-service package and setup diagnostics; migration/rollback tools; evaluation dataset manifest and runner; raw results; user/operator guides; source-license/dependency inventory; and a signed acceptance ledger. Public sample data must not contain private ontoKB content.

## Repository and open-source release note

**Create the development repository as private first.** The project is intended for eventual open-source release. Keep credentials, databases, vaults, transcripts and private evaluations out of commits; include source code only with verified reuse rights. Before a separate public-release decision, check reuse rights for LOGOS/TEBIS, select a compatible license, review dependencies and replace private data with redistributable examples. Private visibility does not grant permission to republish supplied code. Record repository URL and private visibility at M0. This documentation delivery does not create a remote repository.

## Confirmation and completion status

At kickoff, confirm the Windows/English/Chinese baseline, owner-controlled memory inclusion, selected model and data-egress policy, sample-data permission, effort allocation and numeric cost limits. Product owner owns scope/meaning, technical lead owns contracts/migration, QA owns locked evaluation, and the operator owns backup/recovery. One person may hold several roles in a personal project; do not imply independent approval when the same person performed both roles.

This document specifies future implementation. No live baseline benchmark, product upgrade, production deployment or acceptance sign-off has been performed as part of this documentation delivery.

## Sources

- Supplied WhisperLive Miniproject reference: `C:/Users/Admin/WhisperLive/docs/PROJECT_REQUIREMENTS_EN.md`.
- ontoKB source: `C:/Users/10042/Documents/ontoKB`.
- Primary architecture: `C:/Users/10042/Downloads/chennai-training/logos-code.zip`.
- Counterexample and reusable concepts: `C:/Users/10042/Downloads/chennai-training/tebis-teams-meeting.zip`.
- Palantir official conceptual documentation linked above, checked 2026-09-28. Detailed file evidence: [Source assessment](SOURCE_ASSESSMENT_EN.md).
