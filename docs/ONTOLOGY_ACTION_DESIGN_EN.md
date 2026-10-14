# ontoKBv2 Ontology and Action Design

Version 1.0 · 2026-09-28 · Normative design appendix

## Design boundary

The Codex harness is the primary interaction and task-execution environment. It chooses among scoped ontology tools; it does not become the system of record or gain unrestricted write access to SQLite. LOGOS supplies the domain/contracts, release, policy and receipt patterns. ontoKB supplies personal capture and memory semantics. The following is a proposed v2 contract, not a description of already implemented endpoints.

```text
User request or explicitly configured scheduled task
  -> Codex harness and ontoKBv2 skills
  -> authenticated tools with workspace and run context
  -> read Function OR preview / authorize / execute Action
  -> typed ontology runtime, policies and state transitions
  -> atomic canonical storage + receipt + durable outbox
  -> rebuildable search / Obsidian / optional evidence views
  -> tool readback and user-visible evidence/result
```

The ingestion worker uses the same runtime with a narrower service identity. Imported documents and retrieved text are untrusted data, never instructions that can change tool permissions. Keep canonical storage outside the harness's general file-write capability; do not rely on prompt text to prevent direct writes.

## Shared types and identity

Every persisted object has `workspace_id: UUID`, `object_id: UUID`, immutable `type_id`, `schema_version`, `revision: integer >=1`, `created_at` and `recorded_at` UTC timestamps, and an owner/access classification. The composite identity is workspace plus object ID. A name change never changes identity. `valid_from` and `valid_to` describe world applicability when known; `recorded_at` describes when the system learned or changed the record. Unknown dates stay null and are not silently set to ingestion time. All intervals use a documented half-open convention and preserve timezone provenance.

Object and Action schemas reject unknown fields by default. Define string length limits, enums, nullability, numeric ranges/units, date/time formats, unique constraints and typed foreign references. Unknown type, failed coercion or missing mandatory evidence returns a structured error; do not silently truncate or cast. Shared interface contracts such as `EvidenceBacked`, `Versioned` and `Reviewable` can reduce duplication, but handlers still validate each concrete type. Schema.org URIs remain interoperability mappings, not the complete execution contract.

Source-owned fields, derived fields and owner-authored fields have different writers. Re-extraction may propose new source claims; it cannot overwrite an owner's stance or a reviewed correction. Use immutable revisions and tombstones where needed to preserve references. A local owner may delete data under the documented retention policy; minimize audit payloads rather than copying all sensitive content into an undeletable log.

## Initial object catalog

All rows are required for the P0/P1 slice unless indicated. Fields shown supplement the common fields; the implementation must supply full machine-readable schemas.

| Type | Required domain fields and constraints | Meaning |
|---|---|---|
| SourceDocument | `kind: article/note/video/meeting_record/pdf/book/reference`, title, canonical locator or local upload ID | Stable identity of a captured source; a named video is not a person or a claim |
| SourceVersion | document reference, content hash, capture timestamp, parser version, immutable content reference, language | One immutable snapshot; unique document plus content hash; changed source creates a new version |
| EvidenceSpan | source-version reference, locator kind, start/end or page/time coordinates, exact quote, quote hash | Resolvable source evidence; bounds and quote must match canonical extracted text |
| Person | display name; optional external IDs with namespace and aliases | Real human; a shared name is not evidence of identity |
| Organization | display name, optional external IDs, optional organization kind | Organization instance; separate from products and concepts |
| Concept | preferred label and vocabulary namespace; optional description | Reusable topic/term, not a full proposition |
| SoftwareProduct | name, product kind, optional publisher/version | Specific software or product; preserve ontoKB Product/SoftwareApplication distinction through kind and mapping |
| Event | title, event kind; optional time interval and participants | Actual recorded event; uncertain future assertions remain claims |
| Claim | text, evidence references >=1, optional speaker, `verification_status`, extraction provenance, publication state | Source-attributed assertion; subject/predicate/object or literal may be added as validated structured content |
| PersonalMemory | owner, target object or claim, `reviewed: bool`, `included: bool`, `stance: undecided/agree/question/disagree`, note, current judgment reference if any | Owner's relationship to knowledge; stance allowed only on Claim or a claim-backed relation |
| JudgmentRevision | memory reference, prior revision, before/after stance, rationale, effective/recorded time, optional influence-source references | Append-only owner judgment history; historical snapshot is retained when its target changes |
| Project | title and `status: active/paused/completed/archived` | Scope for personal work; not an organizational tenancy boundary |
| Task | title, owner, optional project/due time, `status: proposed/open/in_progress/completed/cancelled`, evidence refs for extracted tasks | Internal actionable object; an extracted promise starts proposed, not as a confirmed commitment |
| ReviewProposal | kind, typed target references, evidence, proposed diff, state and expiry | Pending identity/claim/stance/schema decision with no implied approval |
| ActionRun | action type/version, actor, run/command IDs, target revisions, input hash, outcome and receipt reference | Executed or rejected operation, distinct from a Task describing work to do |
| OntologyRelease | bundle ID/hash, schema/Action/policy/function versions, handler manifest, compatibility report, activation state | P1 immutable runtime contract and migration boundary |

System records also include `IngestionJob`, `AuditReceipt`, `OutboxEvent` and `AutomationRule`; these use explicit schemas and access policies even if not displayed as everyday ontology objects. `AutomationRule` stores permitted sources, schedule/timezone, approved Action set, limits, owner authorization and enabled/paused status. Recurring rule runs cannot silently widen these settings.

## Link types and fact representation

| Link | Endpoints | Cardinality and rule |
|---|---|---|
| hasVersion | SourceDocument -> SourceVersion | 1 to many; each version belongs to exactly one document |
| hasSpan | SourceVersion -> EvidenceSpan | 1 to many; each span belongs to exactly one version |
| supportedBy | Claim -> EvidenceSpan | Each publishable claim has >=1 resolvable span; many claims may use one span |
| about | Claim/SourceDocument -> Person/Organization/Concept/SoftwareProduct/Event/Project | Many to many; about does not imply support or truth |
| attributedTo | Claim -> Person/Organization | 0 or 1 resolved speaker for the initial model; unknown stays unknown; source attribution remains available |
| contradicts | Claim <-> Claim | Symmetric, scoped by meaning/time; candidate conflict until validated, not inferred from mere disagreement in keywords |
| supersedes | Claim -> Claim | Directed, acyclic; older claim remains queryable; correction of a source claim is separate from a judgment revision |
| remembers | PersonalMemory -> typed target | Exactly one target per memory record; owner/target uniqueness applies to the current memory |
| hasJudgmentRevision | PersonalMemory -> JudgmentRevision | Ordered history; exactly one memory per revision |
| belongsTo | Task -> Project | 0 or 1 project per task in the first release |
| assignedTo | Task -> Person | 0 or 1 resolved person; external mention is not an authorization to assign work |

Migrated domain relationships such as `worksFor(Person, Organization)` remain typed. Each source-derived relation assertion references a Claim or equivalent first-class assertion record carrying source, evidence, confidence and applicability; the relationship display is a projection. Multiple contradictory assertions may coexist without overwriting the underlying person/organization. Label every projection with its assertion ID, and do not infer a new fact from graph adjacency.

## Functions and tool surface

Read functions include `search_objects`, `read_evidence`, `get_object_history`, `query_as_of`, `compare_claims` and `get_action_receipt`. A comparison may return a suggestion; persisting a proposal is a separate Action. Validate query filters, typed IDs and pagination; compiled queries are generated by trusted code rather than accepting model-produced SQL.

| Proposed tool | Runtime mapping | Authority |
|---|---|---|
| `memory_search` / `memory_read_evidence` | Read functions with source/memory scope and optional as-of time | Read only; scope filters enforced before any evidence reaches the model |
| `memory_capture` | EnqueueCapture Action | Writes a job/source registration, not trusted claims |
| `memory_list_reviews` | Read proposals | No implicit acceptance |
| `memory_preview_action` | Validate and calculate typed proposed diff | No canonical mutation; produces payload/revision-bound preview |
| `memory_execute_action` | Allowlisted Action dispatch | Policy and approval checks at execution time; no arbitrary handler name |
| `memory_run_status` / `memory_action_receipt` | Read durable job/Action state | Reconcile after cancellation, restart or lost responses |

The service obtains actor/workspace from its authenticated session; model-supplied `actor_id`, role or workspace overrides are rejected. Approval comes from a trusted user interaction or an existing bounded authorization, not a boolean generated by the agent. Bind it to a normalized payload hash, target revision set, action/bundle version and expiry. Long-running jobs return a job ID immediately; they do not keep a tool call blocked indefinitely.

## Action catalog

All semantic mutations pass through this registry, including service-driven imports and re-extraction. The default agent may propose owner-only Actions; it can execute them only within verified user authorization.

| Action | Actor and guard | Effect and evidence |
|---|---|---|
| EnqueueCapture | Owner or preauthorized rule; permitted source/size and budget | Idempotent IngestionJob and capture receipt |
| RegisterSourceVersion | Worker; completed parser output and content checksum | Immutable version/spans; deterministic duplicate reuse |
| ProposeKnowledge | Worker; valid extraction schema and evidence coordinates | Candidate objects/claims/relations; no automatic user stance |
| PublishValidatedClaim | Validator service; calibrated low-risk gate or owner-reviewed approval | Publication state and gate decision; never upgrades verification to truth merely because confidence is high |
| RejectProposal / CorrectClaim | Owner; reason and expected revision; preserve originals | Reject or supersede candidate/claim with traceable correction |
| AcceptMemory / ExcludeMemory | Owner; accessible typed target; explicit inclusion decision | Change personal scope; do not mark all related claims included |
| ReviseJudgment | Owner; current memory revision and rationale | New JudgmentRevision; no background auto-agreement |
| MergeEntities / SplitEntity | Owner-approved diff; compatible types, reference impact check | Canonical redirects/reassigned references and full reversible mapping; never name-only merge |
| CreateTask / StartTask / CompleteTask / CancelTask / ReopenTask | Owner or specifically delegated internal-task rule; legal state transition | Internal Task state change with revision and receipt; no external system side effect |
| GenerateReviewDraft | Scheduled service or owner; time range, scope and budget | Cited draft and incomplete-source list; no belief changes |
| PublishOntologyRelease | Owner/admin capability; schemas/handlers/tests/migration pass | Activate immutable bundle; source authority and policies fixed by release |
| ConfigureAutomation | Owner; explicit schedule/source scope/Action allowlist/limits | Persist or pause bounded AutomationRule |
| ExportWorkspace / DeleteSource / DeleteMemory | Owner; scoped export or deletion preview, retention/impact checks | Portable package or deletion/tombstone and projection invalidation; no unrequested bulk deletion |
| RestoreSnapshot / CompensateAction | Owner; compatible backup or reversible action and current revision check | Restore/reversal report; preserve record of original action and compensation |

## Executable example

The example below specifies a minimum contract for `CompleteTask`; it is an illustrative design, not a deployed schema or Palantir API.

```yaml
action_type: ontokbv2.CompleteTask
version: 1
target_type: ontokbv2.Task
input:
  task_id: {type: uuid, required: true}
  expected_revision: {type: integer, minimum: 1, required: true}
  completion_note: {type: string, max_length: 2000, required: false}
  idempotency_key: {type: string, required: true}
actor: trusted_session_only
permission: task.complete.own
preconditions:
  - target_in_actor_workspace
  - revision_matches
  - state_in_open_or_in_progress
approval: explicit_user_intent_or_scoped_existing_authorization
handler: task.complete.v1
transaction:
  - set_status_completed
  - set_completed_at
  - increment_revision
  - persist_receipt_and_outbox
output: {task_ref: typed_ref, new_revision: integer, receipt_id: uuid}
compensation: reopen_task_with_revision_check
```

For task revision 7 in `open`, the owner's “Complete T-17” resolves the exact task and produces revision 8 plus one receipt. A lost response followed by the same key returns the previous result. The same key with different normalized input is an error. A second command expecting revision 7 is a version conflict; a task in `cancelled` fails its lifecycle guard. An agent statement that the task is complete is not evidence of execution.

## Lifecycle and consistency

Knowledge publication state is `candidate -> published -> superseded/retracted`, with `candidate -> rejected` and a controlled re-review path creating a new revision. Verification (`unverified/corroborated/disputed/verified_by_named_method`) is a separate field with method/evidence metadata. Published means usable under its attribution, not necessarily true. Source-library recall may cite published unverified assertions with explicit attribution; personal-memory recall requires owner inclusion and respects stance. Candidate material is available only in an explicit review/diagnostic scope.

Tasks transition `proposed -> open -> in_progress -> completed`, with allowed cancellation from proposed/open/in_progress. Direct open-to-completed is allowed. Reopening a completed task is a compensating Action with expected revision; changing an old record in place is forbidden. Source jobs use queued/running/retry_wait/needs_review/succeeded/failed/cancelled states with leases and checkpoints. Approval wait is visible, not counted as completed work.

Execute schema validation, trusted identity/policy checks, evidence/precondition checks and optimistic concurrency within the relevant transaction boundary; recheck mutable conditions at commit. Atomically persist mutations, durable idempotency result, receipt and outbox. Audit permission-denied/invalid attempts with minimal metadata without making partial semantic writes. If receipt persistence fails, the mutation must not commit. A process crash after commit is recovered by reading the idempotency record; projection failure is retried from outbox.

Internal DB atomicity does not provide distributed exactly-once guarantees. Future external actions require an adapter with its own idempotency, delivery acknowledgment, reconciliation and compensation rules, and are excluded from P0/P1. A tool timeout cannot be treated as proof that the operation did not happen.

## Migration and release rules

Inventory current tables, vault, configurations and personal-memory history without changing them. Take checksummed SQLite/vault backups. Map old integer IDs to scoped UUIDs and save the mapping. Preserve class URIs/aliases, claim text, relation source/evidence, manually deleted relations and all review/inclusion/stance/history dimensions. Do not infer that an edited or verified record was personally accepted. Retain old source IDs as external identifiers.

Map articles/videos/books to SourceDocument kinds plus provenance, concrete entities to compatible types, and full propositions to Claim. A cited book without captured text remains a referenced object, not a fabricated SourceVersion. Unsupported Thing instances and ambiguous legacy relationships enter quarantine. Evidence strings that cannot be reliably located in the exact source remain unresolved; do not invent offsets or silently mark them valid. Reconstruct source versions only from available snapshots and record capture uncertainty.

Dry-run reports must reconcile every source/entity/relation/memory/history row to migrated, quarantined or intentionally excluded with reason. Verify references and counts, sample owner judgments, rebuild projections and test rollback into a separate workspace. Freeze v1 writes during final cutover, or capture/replay deltas; avoid unsynchronized dual writing. Never test destructive migration on the sole original copy.

Use one machine-readable ontology bundle as definition authority, a proper parser and generated validators/tool schemas. Fail publication when an Action lacks a handler/test, policies refer to nonexistent types, state transitions have no Action, or YAML/code schemas differ. Publish a bundle hash and compatibility report; activation and rollback must state data-migration compatibility. Merely swapping an older schema over newer incompatible data is not a valid rollback.
