# ontoKBv2 Ontology 与 Action 设计

版本 1.0 · 2026-09-28 · 规范性设计附录

## 设计边界

Codex harness 是主要交互与任务执行环境，通过限定 ontology 工具完成任务；它不是权威数据库，也不直接获得任意 SQLite 写权限。LOGOS 提供领域契约、发布、策略与回执模式，ontoKB 提供个人收集和记忆语义。以下是拟定 v2 契约，不是已经实现的接口说明。

```text
用户请求或明确配置的定时任务
  -> Codex harness 与 ontoKBv2 skills
  -> 带工作区和 run 上下文的认证工具
  -> 只读 Function 或 Action 预览 / 授权 / 执行
  -> 强类型 ontology runtime、策略和状态迁移
  -> 权威存储、回执、持久 outbox 原子提交
  -> 可重建的搜索 / Obsidian / 可选证据视图
  -> 工具回读与用户可见证据及结果
```

接入 worker 使用权限更小的服务身份经过同一运行时。导入文档和检索文本是非可信数据，不能修改工具权限。权威存储应放在 harness 通用文件写能力之外，不能只靠提示词禁止直接修改。

## 公共类型与身份

所有对象包含 `workspace_id: UUID`、`object_id: UUID`、不变 `type_id`、`schema_version`、`revision: integer >=1`、UTC `created_at`/`recorded_at`、拥有者/访问分级。身份由工作区加对象 ID 确定，改名不能改变身份。已知时以 `valid_from`/`valid_to` 表达现实适用时间，`recorded_at` 表达系统获知或修改时间；未知时间保持 null，不自动填入入库时间。时间区间统一采用明确的左闭右开规则，保留时区来源。

对象与 Action schema 默认拒绝未知字段，声明长度、枚举、空值、数值范围/单位、时间格式、唯一性和强类型外键。未知类型、转换失败、必需证据缺失返回结构化错误，不静默截断或强制转换。可共享 EvidenceBacked、Versioned、Reviewable 接口，但仍需校验具体类型。Schema.org URI 保留为互操作映射，不是完整执行契约。

来源字段、派生字段和用户字段由不同写入者管理。重新抽取可以提出新的来源论断，不能覆盖用户立场和已审核修正。采用不可变修订及必要 tombstone 保持引用。用户按保留策略删除数据时，审计应只留最少元数据，不把敏感全文复制到永远不可删除的日志。

## 首版对象目录

除明确说明外均属于 P0/P1。下列字段是公共字段之外的领域字段，实施时须补齐机器可读 schema。

| 类型 | 必需领域字段与约束 | 含义 |
|---|---|---|
| SourceDocument | kind 为 article/note/video/meeting_record/pdf/book/reference，标题，规范 locator 或本地上传 ID | 来源稳定身份，视频本身不是人物或论断 |
| SourceVersion | 文档引用、内容哈希、采集时间、解析器版本、不可变内容引用、语言 | 不可变快照；文档加内容哈希唯一，变化创建新版本 |
| EvidenceSpan | 来源版本引用、定位类型、起止范围或页码/时间、准确原文、quote hash | 可解析的证据，范围及文本须与规范提取正文一致 |
| Person | 显示名称，可选命名空间化外部 ID 与别名 | 自然人，共享名字不是同一身份的证据 |
| Organization | 名称，可选外部 ID 及机构类别 | 机构实例，与产品、概念分离 |
| Concept | 标准名称及词汇命名空间，可选描述 | 可复用主题/术语，不是完整命题 |
| SoftwareProduct | 名称、产品类别，可选发布者/版本 | 具体软件或产品，以 kind 和映射保留原 Product/SoftwareApplication 区别 |
| Event | 标题、事件类型，可选时间区间和参与者 | 已记录事件，未确定未来事件仍以论断表达 |
| Claim | 文本、至少一条证据、可选说话者、verification_status、抽取来源、发布状态 | 有来源归属的断言，可补受校验的主谓宾或字面值 |
| PersonalMemory | 拥有者、对象/论断目标、reviewed、included、stance 为 undecided/agree/question/disagree、说明、当前判断引用 | 用户与知识的关系；立场仅适用于 Claim 或有 Claim 支撑的关系 |
| JudgmentRevision | 记忆引用、上次版本、前后立场、理由、适用/记录时间、可选影响来源 | 追加式判断历史，目标变化时仍保留历史快照 |
| Project | 标题及 active/paused/completed/archived 状态 | 个人工作范围，不是企业租户边界 |
| Task | 标题、拥有者、可选项目/截止时间、proposed/open/in_progress/completed/cancelled、抽取任务所需证据 | 内部可操作对象；抽出的承诺先是 proposed，不自动成为已确认承诺 |
| ReviewProposal | 类别、强类型目标引用、证据、拟修改 diff、状态和有效期 | 身份/论断/立场/schema 待审核项，不隐含批准 |
| ActionRun | Action 类型/版本、执行者、run/command ID、目标版本、输入哈希、结果及回执 | 操作执行或拒绝记录，与描述待办的 Task 不同 |
| OntologyRelease | bundle ID/hash、schema/Action/策略/函数版本、handler 清单、兼容报告、激活状态 | P1 不可变执行契约与迁移边界 |

系统记录还包含 IngestionJob、AuditReceipt、OutboxEvent、AutomationRule，即使不显示为日常对象，也必须有 schema 和权限。AutomationRule 保存允许来源、日程/时区、允许 Action、预算、拥有者授权和启停状态；周期运行不能悄悄扩大配置。

## 关系类型与事实表达

| 关系 | 端点 | 基数与规则 |
|---|---|---|
| hasVersion | SourceDocument -> SourceVersion | 一对多，每版本只属于一个文档 |
| hasSpan | SourceVersion -> EvidenceSpan | 一对多，每片段只属于一个版本 |
| supportedBy | Claim -> EvidenceSpan | 可发布论断至少一个可解析证据，片段可支持多个论断 |
| about | Claim/SourceDocument -> Person/Organization/Concept/SoftwareProduct/Event/Project | 多对多，提及不等于支持或真实 |
| attributedTo | Claim -> Person/Organization | 首版零或一个已解析说话者，未知保持未知，仍有来源归属 |
| contradicts | Claim <-> Claim | 对称且有语义/时间范围，验证前只是候选冲突，不能仅按关键词推断 |
| supersedes | Claim -> Claim | 有向无环，旧论断可查询；来源修正不等于个人判断修改 |
| remembers | PersonalMemory -> 强类型目标 | 每条记忆一个目标，当前记忆按拥有者/目标唯一 |
| hasJudgmentRevision | PersonalMemory -> JudgmentRevision | 有序历史，每修订只属于一条记忆 |
| belongsTo | Task -> Project | 首版每任务零或一个项目 |
| assignedTo | Task -> Person | 零或一个已解析人物，提及某人不代表授权派任务 |

迁移保留 worksFor(Person, Organization) 等强类型领域关系。每条来源关系断言应引用 Claim 或同等的一等断言记录，保存来源、证据、置信度及适用时间，关系展示只是投影。互相矛盾的断言可并存，不能覆盖人物/机构本身。投影带 assertion ID，不能从图相邻直接推导新事实。

## Function 与工具接口

只读函数包括 search_objects、read_evidence、get_object_history、query_as_of、compare_claims、get_action_receipt。对比可返回建议，持久保存提案是另一个 Action。校验查询条件、类型 ID 和分页；可信代码编译查询，不执行模型生成的任意 SQL。

| 拟定工具 | 运行时映射 | 权限 |
|---|---|---|
| memory_search / memory_read_evidence | 带资料/记忆范围、可选历史时间的读取函数 | 只读，证据进入模型前强制范围过滤 |
| memory_capture | EnqueueCapture | 写任务/来源登记，不写可信事实 |
| memory_list_reviews | 读取提案 | 不隐式接受 |
| memory_preview_action | 校验并计算强类型 diff | 不修改权威数据，预览绑定参数及版本 |
| memory_execute_action | 白名单 Action 分发 | 执行时检查策略/审批，不能指定任意 handler |
| memory_run_status / memory_action_receipt | 读取持久任务/Action 状态 | 取消、重启或响应丢失后的对账依据 |

服务从认证会话取得 actor/workspace，拒绝模型参数中的身份/角色/工作区覆盖。批准来自可信用户交互或已有有界授权，不接受 agent 生成的布尔值。绑定规范参数哈希、目标版本集、Action/bundle 版本和到期时间。长任务立即返回 job ID，不无限阻塞工具调用。

## Action 目录

所有语义修改经过该注册表，包括服务导入和重新抽取。默认 Agent 可提议用户专属 Action，执行时必须具有已验证的用户授权。

| Action | 执行者与前提 | 效果与证据 |
|---|---|---|
| EnqueueCapture | 拥有者或预授权规则；允许来源/大小及预算 | 幂等任务和采集回执 |
| RegisterSourceVersion | worker；解析完成且校验和通过 | 不可变版本/片段，重复内容确定性复用 |
| ProposeKnowledge | worker；抽取 schema 和证据坐标合法 | 候选对象/论断/关系，不产生用户立场 |
| PublishValidatedClaim | 校验服务；已校准低风险门或用户审核 | 发布状态和门控决策，高置信度不能自动提升为真 |
| RejectProposal / CorrectClaim | 拥有者；理由、预期版本，保留原文 | 拒绝或替代候选/论断，修正可追踪 |
| AcceptMemory / ExcludeMemory | 拥有者；可访问目标，明确纳入决定 | 改变个人范围，不连带纳入所有相邻论断 |
| ReviseJudgment | 拥有者；当前版本与理由 | 新 JudgmentRevision，后台不能自动同意 |
| MergeEntities / SplitEntity | 用户批准 diff；类型兼容、引用影响检查 | 规范重定向/引用重分配及可逆映射，不按名字合并 |
| CreateTask / StartTask / CompleteTask / CancelTask / ReopenTask | 拥有者或明确委托的内部任务规则；合法迁移 | 内部 Task 状态、版本、回执，不影响外部系统 |
| GenerateReviewDraft | 定时服务或拥有者；时间、范围、预算 | 带引用草稿和未完成来源清单，不改立场 |
| PublishOntologyRelease | 拥有者/admin 能力；schema/handler/测试/迁移通过 | 激活不可变包，来源权威和策略由版本固定 |
| ConfigureAutomation | 拥有者；明确日程/来源/Action 白名单/限额 | 保存或暂停有界 AutomationRule |
| ExportWorkspace / DeleteSource / DeleteMemory | 拥有者；导出范围或删除预览、保留/影响校验 | 可迁移包或删除/tombstone、投影失效，不擅自批量删除 |
| RestoreSnapshot / CompensateAction | 拥有者；兼容备份或可逆操作及版本检查 | 恢复/撤销报告，保留原操作和补偿记录 |

## 可执行契约示例

以下为 CompleteTask 最低契约设计示意，不是已部署 schema 或 Palantir API。

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

任务 revision 7、状态 open 时，拥有者说“完成 T-17”，系统定位目标后产生 revision 8 和一条回执。响应丢失后用同一 key 重试，返回原结果；同 key 不同规范参数报错。另一命令仍期待 revision 7 时返回版本冲突，cancelled 状态失败。Agent 口头说完成不是执行证据。

## 生命周期与一致性

知识发布状态为 candidate -> published -> superseded/retracted，以及 candidate -> rejected；重新审核须生成新修订。核实状态 unverified/corroborated/disputed/verified_by_named_method 独立保存方法和证据。published 表示可在来源归属下使用，不代表必然为真。资料库可引用已发布的未核实断言并明确归属，个人记忆仅检索用户纳入且符合立场条件的内容。候选只能在显式审核/诊断范围使用。

Task 状态为 proposed -> open -> in_progress -> completed，proposed/open/in_progress 可取消，允许 open 直接完成。重新打开已完成任务须经补偿 Action 和版本检查，不直接修改旧记录。来源任务使用 queued/running/retry_wait/needs_review/succeeded/failed/cancelled，带租约和检查点；等待审批不是已完成。

在有关事务边界执行 schema、可信身份/权限、证据/前提及乐观并发检查，提交时重新检查可变条件；原子保存修改、持久幂等结果、回执与 outbox。拒绝/无效尝试记录最少审计元数据，不产生部分语义修改。回执持久化失败则修改不得提交；提交后崩溃依幂等记录恢复，投影失败按 outbox 重试。

本地事务不等于分布式 exactly-once。未来外部 Action 需适配器幂等、确认、对账、补偿，P0/P1 不包含。工具超时不能证明操作没有发生。

## 迁移与发布

只读盘点当前表、vault、配置和个人历史，并为 SQLite/vault 做校验和备份。旧整数 ID 映射为带工作区范围的 UUID 并保存映射。保留类型 URI/别名、论断、关系来源/证据、人工删除关系及全部审核/纳入/立场/历史维度；不能把已编辑或已核实推断为个人认可。旧 source ID 保留为外部标识。

文章/视频/书籍按来源类型及出处映射，具体实体映射兼容类型，完整命题映射 Claim。仅被引用而没有正文的书籍保持引用对象，不捏造 SourceVersion。不支持的 Thing 和歧义旧关系进入隔离区；无法在准确来源定位的证据文本保持 unresolved，不伪造坐标或通过标记。仅基于现有快照重建版本，并记录采集不确定性。

预演逐项对账所有来源/实体/关系/记忆/历史行，结果为 migrated、quarantined 或有理由的 intentionally_excluded。检查引用和数量，抽查判断，重建投影，在独立工作区测试回滚。最终切换冻结 v1 写入或记录并回放增量，不能无同步双写；不能在唯一原始数据上测试破坏性迁移。

以一个机器可读本体包为定义权威，使用正式解析器并生成 validator/工具 schema。Action 缺 handler/测试、策略引用不存在类型、状态迁移没有 Action、YAML/代码不一致时禁止发布。生成 bundle hash 和兼容报告；激活/回滚说明数据迁移兼容性，不能直接将旧 schema 覆盖到不兼容的新数据。
