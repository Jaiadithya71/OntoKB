# ontoKBv2 来源评估与复用决策

检查日期：2026-09-28。方法为对选定源码和文档的只读静态检查，未启动应用、运行测试或执行迁移。判断限定于已检查路径，文件存在不代表部署行为已验证。

## 输入与文档参考

| 输入 | 快照身份 |
|---|---|
| ontoKB | `C:/Users/10042/Documents/ontoKB`；选定文件指纹见 source_manifest.json；这是可变工作目录，不冒充固定发布版 |
| LOGOS | `C:/Users/10042/Downloads/chennai-training/logos-code.zip`；SHA-256 `06F50AA1ABE266215A81A0DA6386E7C76639CAC8DCFF47C18C10966983CC1C52` |
| TEBIS | `C:/Users/10042/Downloads/chennai-training/tebis-teams-meeting.zip`；SHA-256 `7F86B832697BD9BDA605BA109C5D9846CC3E011451BC35CBDE2AC4435690D856` |
| Miniproject 格式参考 | `C:/Users/Admin/WhisperLive/docs/PROJECT_REQUIREMENTS_EN.md`；采用项目介绍、基线、需求、部署、优化、指标、评测和交付结构 |

同时参考了当前 Internal Policy QA 交付文档中“拟定指标与实测结果分开”的做法。WhisperLive 仅提供结构，不继承其 ASR、Netaccess、HA 或硬件要求。LOGOS 使用用户指定旧快照，不宣称最新版本一致，也没有以另一个更新目录替换。

## ontoKB 证据及含义

| 相对路径 | 观察 | v2 决策 |
|---|---|---|
| ontology/core.yaml；src/ontokb/ontology.py | Schema.org 受控剖面、继承、domain/range 校验；实体验证入口仅接收类型，不接收完整强类型属性记录 | 保留词汇与关系边界，补属性/值/引用校验和可执行领域契约 |
| src/ontokb/graph.py | SQLite entities/triples/contents、全局唯一规范名称/别名、JSON 属性、source/evidence 及人工修改表 | 保留便携/追溯，身份权威改为带范围稳定 ID 及审核消歧 |
| src/ontokb/memory.py；README.md | 独立 reviewed/included/stance/note、快照身份和判断历史；README 说明记忆纳入不改变普通 Chat 范围 | 保留语义，新增强制的检索范围和可迁移记忆导出 |
| src/ontokb/rules.py | 前向规则产生 action facts，限制迭代 | 可复用确定性自动化组件，但不等于完整有权限 Action Type runtime |
| src/ontokb/codex_backend.py | 每次 generate 启动 app-server、创建 thread、处理动态工具、上限 8 次后终止进程；工具耗时延长 deadline | harness 已存在；升级会话/持久任务、真实总时限、取消、恢复和审批，不能把 harness 引入描述成从零开始 |
| src/ontokb/knowledge_agent.py | 限定读取/重新分析/同步工具，要求验证写入；模型只读沙箱下宿主工具仍能写库 | 保留限定工具模式，加强服务端可信授权和审计；模型沙箱不能代替宿主写权限 |
| README.md；docs/PRD.md | 文章/视频与 vault 流程；README 指明队列自动消费/报告缺口及记忆对比上限 | 补持久自动化，显示超限/不完整；原文进度不是此次测量结果 |

## LOGOS 作为主要蓝本

ZIP 根目录为 `logos-code/`。

| 根目录下证据 | 观察 | 复用/加固 |
|---|---|---|
| README.md | Workbench、Foundry/Knowledge/Runtime/Audit/worker、PostgreSQL/OpenSearch 开发依赖、Connect/Build/Review/Release | 复用治理流程，个人版收敛为小型本地服务，不照搬开发拓扑 |
| packages/domain/src/customer-support/ontology/object-types.ts | 主键和属性描述的对象定义 | 改造为个人记忆领域并落实属性契约 |
| 同目录 action-types.ts、state-models.ts、policy-bindings.ts、source-authority.ts | Action 风险/审批/效果、生命周期、策略及来源权威 | 保留概念分离，替换客服词汇并证明强制执行 |
| packages/domain/src/domain-contract.ts | 用逐行/正则帮助函数读 YAML，校验领域定义中存在必需名称 | 改为完整 schema 校验和生成契约，名称一致不代表语义等价 |
| packages/domain/src/ontology-runtime.test.ts | 契约一致性与 reply-plan 本体上下文测试 | 扩展无效输入、handler/策略覆盖和端到端效果 |
| packages/platform/src/index.ts | 身份、角色检查、预期版本、回执、内存幂等/outbox、审计 sink、开发安全模式 | 有用基础，但要求持久幂等/outbox 和实际认证配置测试；不能据内存类存在就推断所有部署只用内存 |
| services/runtime/src/domains/customer-support/routes.ts | 草稿生成/批准检查与回执，路径针对客服 | 复用 command/receipt，构建注册表驱动分发，不能从独立调用推断修改与回执已原子化 |

该快照明显超过图谱 schema，是三个项目中最适合的平台基础，但当前领域是客服，并非可直接交付的个人记忆产品。源码基础仍需新的安全、持久性、依赖和行为测试。

## TEBIS 的具体反例

ZIP 根目录为 `tebis-teams-meeting-merged-ontlogies-work-optimizationv0/`。

| 证据 | 限制或有用概念 | v2 对策 |
|---|---|---|
| contracts/ontology/action_types.yaml | 明确注明为声明注册表，不实现规则引擎 | 每个已发布 Action 必须有 handler 和测试 |
| 同文件 AnonymizePersonData | 注明没有真实 RBAC，权限仅记录不强制；该说明保留审计问题 | 服务端执行身份权限，演示拒绝和审计失败行为 |
| contracts/ontology/entity_registry.yaml 的 Evidence | 说明正式 Evidence 节点未实现，实际采用直接 SUPPORTED_BY 到 SourceSpan | 设计与实际契约一致；EvidenceSpan 方案明确实现并测试即可 |
| 同文件 Transcript | canonical schema 为 null/pending | 发布前检查契约完整，图标签不能算完整强类型对象 |
| contracts/ontology/knowledge_lifecycle.yaml | 候选/确认和证据生命周期 | 借鉴概念，但要落为可执行状态迁移 |
| buildtime-agent/agents/autoschemakg-meeting-agent/pipeline.py | 该路径是返回 placeholder 状态的占位实现 | 追踪真实活动路径，不以占位文件算完成；不意味着所有 TEBIS 管线均为占位 |
| tebis-bcl/app/router/action_items.py | GET 路由经 pipeline 列出 action items | 待办查询不证明 Action 可执行，须另演示修改命令 |

反例教训是实现一致性及可强制执行的行为，不是知识图谱本身不适用；来源片段、时间模型、候选审核等有用部分应保留。

## 外部概念与公开边界

Palantir 本体将对象/关系语义与 Action、Function 结合。其操作和权限概念为本地强类型修改与权限边界提供参考，但这里是独立适配。2026-09-28 查阅官方 [Ontology](https://www.palantir.com/docs/foundry/ontology/overview)、[Actions](https://www.palantir.com/docs/foundry/action-types/overview)、[权限](https://www.palantir.com/docs/foundry/object-permissioning/overview)。

OpenAI 官方资料支持按用途选择 Codex harness 集成界面。本设计选择原生 Codex 加限定工具，app-server 保留为可选嵌入适配；参考 [Codex as a platform](https://developers.openai.com/blog/codex-as-a-platform) 和 [App Server](https://learn.chatgpt.com/docs/app-server)，查阅日期 2026-09-28。实际版本、账号、配额、无人值守行为仍需实施验证。

**先 private：** 计划开源不等于现在可公开所提供压缩包或个人知识。先建 private 开发仓库，检查来源和许可证，私人数据不入提交，公开另行决定。本次评估未创建远程仓库。
