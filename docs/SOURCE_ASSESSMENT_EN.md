# ontoKBv2 Source Assessment and Reuse Decisions

Inspection date: 2026-09-28. Method: read-only static inspection of selected source and documentation. No applications, test suites or migrations were run. Findings are limited to inspected paths; file presence does not establish deployed behavior.

## Inputs and document reference

| Input | Snapshot identity |
|---|---|
| ontoKB | `C:/Users/10042/Documents/ontoKB`; selected file hashes in source_manifest.json; a mutable working directory, not represented as a pinned release |
| LOGOS | `C:/Users/10042/Downloads/chennai-training/logos-code.zip`; SHA-256 `06F50AA1ABE266215A81A0DA6386E7C76639CAC8DCFF47C18C10966983CC1C52` |
| TEBIS | `C:/Users/10042/Downloads/chennai-training/tebis-teams-meeting.zip`; SHA-256 `7F86B832697BD9BDA605BA109C5D9846CC3E011451BC35CBDE2AC4435690D856` |
| Miniproject style reference | `C:/Users/Admin/WhisperLive/docs/PROJECT_REQUIREMENTS_EN.md`; project overview, baseline, requirements, deployment, optimization, metrics, evaluation and delivery structure |

The local Internal Policy QA delivery documents also informed the distinction between proposed gates and measured results. WhisperLive supplies structure, not ASR, Netaccess, HA or hardware requirements for this project. LOGOS is the user's supplied older snapshot; no latest-version parity is asserted and no unrelated newer checkout is substituted.

## ontoKB evidence and implications

| Evidence path relative to ontoKB | Observed content | Design implication |
|---|---|---|
| `ontology/core.yaml`; `src/ontokb/ontology.py` | Controlled Schema.org profile, class hierarchy and domain/range validation; validator entry point accepts an entity type, not a complete strongly typed property record | Retain vocabularies and relation boundaries; add full property/value/reference validation and executable domain contracts |
| `src/ontokb/graph.py` | SQLite entities/triples/contents; globally unique normalized name and alias; JSON properties; source/evidence columns; manual edit tables | Preserve portability and provenance; replace name-based identity authority with scoped stable IDs and reviewed identity resolution |
| `src/ontokb/memory.py`; `README.md` | Independent reviewed/included/stance/note metadata, snapshot identity and judgment history; README says ordinary Chat scope is not changed by personal-memory inclusion | Preserve semantics; add explicit runtime recall scopes and portable memory export |
| `src/ontokb/rules.py` | Forward-chaining local rules produce action facts and bound iterations | Useful deterministic automation component, not a complete permissioned Action Type runtime |
| `src/ontokb/codex_backend.py` | Starts an app-server subprocess per generate call, creates a thread, processes dynamic tools, caps calls at 8 and terminates the process; tool execution time extends its deadline | Harness use already exists; upgrade persistent sessions/jobs, true end-to-end deadlines, cancellation, recovery and approvals instead of describing harness adoption as entirely new |
| `src/ontokb/knowledge_agent.py` | Bounded read/reanalyze/sync tools and instructions to verify writes; host tools can mutate despite read-only model sandbox | Retain scoped tool pattern; strengthen trusted service-side authority and audit. Model sandbox does not enforce host mutation permissions |
| `README.md`; `docs/PRD.md` | Article/video capture and vault workflows; README identifies queue auto-consumption/reporting gaps and bounded memory comparison | Complete durable automation and expose overflow/incomplete work; README progress statements are not new measurements |

## LOGOS reuse as the principal blueprint

Archive root: `logos-code/`.

| Evidence path under root | Observed content | Reuse or hardening decision |
|---|---|---|
| `README.md` | Workbench plus Foundry/Knowledge/Runtime/Audit/worker; PostgreSQL/OpenSearch local dependencies; Connect/Build/Review/Release | Reuse logical governance workflow; package a small local service rather than require the entire development topology |
| `packages/domain/src/customer-support/ontology/object-types.ts` | Object definitions with primary keys and property descriptors | Adapt as personal-memory domain, preserving executable property contracts |
| `.../action-types.ts`; `.../state-models.ts`; `.../policy-bindings.ts`; `.../source-authority.ts` | Action risk/approval/effect metadata, lifecycle transitions, policy decisions and source authority | Keep separation of definitions, policies, state and authority; replace customer-support vocabulary and prove enforcement |
| `packages/domain/src/domain-contract.ts` | Reads contract YAML using line/regular-expression helpers; checks required named entries against domain definitions | Replace partial parsing with complete schema validation and generated contracts; name parity alone does not verify semantic equivalence |
| `packages/domain/src/ontology-runtime.test.ts` | Contract/ontology consistency and reply-plan ontology context tests | Reuse test pattern, extend to invalid inputs, handler/policy coverage and end-to-end runtime effects |
| `packages/platform/src/index.ts` | Identity helpers, role guards, expected-version checks, receipts, in-memory idempotency/outbox classes, audit sink; development security modes | Useful primitives; require persistent idempotency/outbox and tested auth/configuration. Existence of in-memory helpers does not prove every deployment uses only memory |
| `services/runtime/src/domains/customer-support/routes.ts` | Draft generation/approval routes perform checks and emit receipts; approval is a customer-support-specific path | Reuse command/receipt pattern but build generic registry-driven dispatch; prove atomic mutation/receipt behavior rather than assuming it from separate calls |

The snapshot has more than a graph schema and is the strongest supplied platform starting point. Its current business purpose is customer support, not a ready personal-memory product. Strong source artifacts still require fresh security, durability, dependency and behavioral validation.

## TEBIS as a precise counterexample

Archive root: `tebis-teams-meeting-merged-ontlogies-work-optimizationv0/`.

| Evidence | Observed limitation or useful concept | v2 response |
|---|---|---|
| `contracts/ontology/action_types.yaml` | States explicitly that it is a declarative registry, not a rule-engine implementation | Require registry-to-handler-to-test coverage for every published Action |
| Same file, `AnonymizePersonData` | Notes that real RBAC is absent and required permission is recorded, not mechanically enforced; audit issue remains identified in that note | Enforce identity and permission in service code, demonstrate denied executions and audit failure behavior |
| `contracts/ontology/entity_registry.yaml`, Evidence entry | Explains formal Evidence-node pattern was not implemented; actual binding uses direct SUPPORTED_BY to SourceSpan | Keep design and active contract consistent; an EvidenceSpan design is valid when explicitly implemented and tested |
| Same file, Transcript entry | Canonical schema is null/pending | Fail required release contract completeness; do not count a graph label as a complete typed object |
| `contracts/ontology/knowledge_lifecycle.yaml` | Candidate/confirmation lifecycle and evidence concepts | Reuse conceptual separation, but integrate with executable state transitions |
| `buildtime-agent/agents/autoschemakg-meeting-agent/pipeline.py` | Inspected path is a placeholder that returns placeholder status | Trace active routes; never count placeholder files as feature completion. This does not imply every TEBIS pipeline is a placeholder |
| `tebis-bcl/app/router/action_items.py` | GET route lists action items via pipeline | A task-search endpoint is not proof of an executable Action API; demonstrate state-changing commands separately |

The lesson is implementation consistency and enforceable behavior, not that knowledge graphs are inherently unsuitable. Do not remove source spans, temporal modeling or candidate review merely because this project is used as a counterexample.

## Reference concepts and release limits

Palantir describes an ontology combining object/link semantics with actions and functions. Its Action and permission concepts motivate typed changes and explicit access boundaries; the proposed local design is an independent adaptation. References checked 2026-09-28: [Ontology](https://www.palantir.com/docs/foundry/ontology/overview), [Actions](https://www.palantir.com/docs/foundry/action-types/overview), [permissions](https://www.palantir.com/docs/foundry/object-permissioning/overview).

Official OpenAI guidance supports choosing an integration surface for the Codex harness; the design selects native Codex plus scoped tools and retains app-server as an optional embedded adapter. See [Codex as a platform](https://developers.openai.com/blog/codex-as-a-platform) and [App Server](https://learn.chatgpt.com/docs/app-server), checked 2026-09-28. Actual supported versions, authentication, quotas and unattended behavior remain implementation validation items.

**Private first:** intended open source does not authorize immediate publication of supplied archives or personal knowledge. Create a private development repository, verify provenance/licenses, keep private data out of commits and make a separate public-release decision. No remote repository was created during this assessment.
