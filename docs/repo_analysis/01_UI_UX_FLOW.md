# ontoKB UI/UX Flow & Screen Navigation Guide

This document provides a comprehensive mapping of every screen, view, modal, button, and user interaction within the **ontoKB** application.

---

## 1. Application Architecture & Entry Point

The ontoKB user interface is a high-performance single-page web application served locally by the Python backend:
* **Default URL**: `http://127.0.0.1:8765/`
* **Entry Command**: `python -m ontokb.cli api` or `.\start.ps1`
* **Source Template**: [`src/ontokb/web/reading.html`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/ontoKB/src/ontokb/web/reading.html)
* **Frontend Modules**:
  * Core Reading & Graph: [`reading.html`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/ontoKB/src/ontokb/web/reading.html), [`reading.js`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/ontoKB/src/ontokb/web/reading.js), [`reading.css`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/ontoKB/src/ontokb/web/reading.css)
  * Knowledge Assistant / Chat: [`assistant.js`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/ontoKB/src/ontokb/web/assistant.js)
  * Knowledge Editor: [`editor.js`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/ontoKB/src/ontokb/web/editor.js), [`editor.css`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/ontoKB/src/ontokb/web/editor.css)
  * Personal Memory Review: [`memory.js`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/ontoKB/src/ontokb/web/memory.js), [`memory.css`](file:///c:/Users/jaiad/Personal_Work_Related/Third%20Wave%20Tech%20Training/Mini%20Project%20-%20ontoKB/ontoKBv2/ontoKBv2/ontoKB/src/ontokb/web/memory.css)

---

## 2. Global Navigation & Top Bar (Masthead)

The top navigation header (`<header class="masthead">`) stays persistent across the top of the interface:

```
+-------------------------------------------------------------------------------------------------------------+
| ✳ onto.让知识彼此连接  [阅读工作台] [探索图谱]  |  [个人记忆] [整理知识] [知识助手 ↗] [＋ 新建摘要] [打开 Chat ↗] |
+-------------------------------------------------------------------------------------------------------------+
```

### Masthead Elements & Click Actions

| UI Element | Selector / ID | Action on Click |
|---|---|---|
| **Brand Logo** | `.brand` | Returns to default view / refreshes perspective. |
| **阅读工作台 (Reading Workbench)** | `#reading-nav` | Activates the split-view: Left Reader sidebar + Center Interactive Graph stage. |
| **探索图谱 (Explore Graph)** | `#explore-nav` | Hides the reader sidebar to give full canvas width to the force-directed knowledge graph. |
| **个人记忆 (Personal Memory)** | `#memory-open` | Opens the **Personal Research Memory Dialog** (`#memory-dialog`) modal. |
| **整理知识 (Curate Knowledge)** | `#editor-open` | Opens the **Knowledge Editor Modal** (`#knowledge-editor`) for entities, claims, and relations. |
| **知识助手 ↗ (Knowledge Assistant)** | `#assistant-open` | Slides open the right-hand **Assistant Drawer** (`#query-panel`), focusing on the active tab. |
| **＋ 新建摘要 (New Summary)** | `#article-open` | Opens the **New Article Ingestion Modal** (`#article-dialog`). |
| **打开 Chat ↗ (Open Chat)** | `#chat-open` | Opens the Assistant Drawer directly to the **Chat** tab (`#chat-view`). |

---

## 3. Screen 1: Reader Workspace (Left Sidebar)

Located in `<aside class="reader">`, this panel enables structured reading of ingested articles/videos alongside their knowledge graph connections.

```
+------------------------------------------------------+
| YOUR READING SPACE                     [ 12 篇资料 ] |
| [全部分类] [AI] [商业] [技术]                        |
| [ 选择阅读资料 v ]                                   |
+------------------------------------------------------+
| [ 资料摘要 ]   [AI / 大模型]                         |
| OpenAI o1 深度解析与推理架构                         |
| <a>阅读原文 ↗</a>                                    |
| [ 14 实体 ]   [ 22 关系 ]   [ 5 阅读片段 ]           |
|                                                      |
| 文章摘要  (点击段落，漫步知识)                       |
|  +------------------------------------------------+  |
|  | 01 OpenAI 发布 o1 推理模型，引入强化学习机制...  |  |
|  +------------------------------------------------+  |
|  | 02 模型在数学与代码基准测试中大幅超越 GPT-4o...   |  |
|  +------------------------------------------------+  |
|                                                      |
| 值得记住  KEY TAKEAWAYS                              |
|  • 采用思维链（CoT）推理强化训练                     |
|  • 延迟换取精度的系统级范式转变                      |
+------------------------------------------------------+
```

### Components & Interactions

1. **Category Filter Pills (`#category-filters`)**:
   * Displays pill buttons for categories (e.g., `全部`, `AI`, `芯片`, `历史`).
   * Clicking a category filters the document list in `#document-select`.
2. **Document Selector Dropdown (`#document-select`)**:
   * Dropdown listing all processed documents (`contents` table in SQLite).
   * Selecting a document loads its title, metrics, summary steps, takeaways, and filters the graph.
3. **Document Header & External Link (`#source-link`)**:
   * Shows source title and classification tag (`资料摘要` / `视频分析`).
   * Clicking `阅读原文 ↗` opens original URL in a new browser tab.
4. **Document Metrics Pill**:
   * Displays count of extracted nodes (`#doc-nodes`), relations (`#doc-links`), and reading steps (`#doc-steps`).
5. **Interactive Summary Steps (`#summary-steps`)**:
   * Displays numbered summary paragraphs (e.g., `01`, `02`, `03`).
   * **Click Action**: Clicking any summary step:
     1. Highlights that step with an active accent border.
     2. Highlights all entities and relations mentioned in that step on the center graph.
     3. Centers the graph viewport on the relevant cluster.
     4. Updates the bottom Tour Dock.
6. **Key Takeaways (`#key-points`)**:
   * Bulleted list of distilled conclusions generated during LLM extraction.

---

## 4. Screen 2: Center Interactive Knowledge Graph Stage

Located in `<section class="graph-stage">`, providing an interactive force-directed graph powered by **D3.js (v7)**.

```
+-------------------------------------------------------------------------------------------------+
| A WALK THROUGH IDEAS                                        [ 搜索实体... ]  [ ☷ ]  [ ⤢ ]      |
| 跟随摘要，发现连接。                                                                            |
| [ 层级: 全部层级 v ]  [ 类型: 全部类型 v ]                                                      |
+-------------------------------------------------------------------------------------------------+
|                                                                                                 |
|               (OpenAI) ----[develops]----> (o1-preview)                                         |
|                  |                               |                                              |
|              [worksFor]                      [mentions]                                         |
|                  v                               v                                              |
|             (Sam Altman)                   (Noam Brown)                                         |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   | 关系与原始证据                                                                      [×] |   |
|   | OpenAI --[develops]--> o1-preview                                                       |   |
|   | "OpenAI announced o1, a new series of reasoning models trained with reinforcement..."   |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
| [ 02 / 05 ]  摘要漫游    [ ← ] [ ▶ 开始漫游 ] [ → ]  [ 速度: 10秒 v ]    [ 查看证据 ↗ ]         |
| =====================--------------------------------------------------------------------------- |
+-------------------------------------------------------------------------------------------------+
```

### Controls & Visual Interactions

1. **Entity Search (`#search`)**:
   * Autocomplete search input. Typing filters entities and flies the camera to the matching node.
2. **Filter Toggle (`#filter-toggle`)**:
   * Toggles visibility of the secondary filter bar (`#filters`).
3. **Fit View Button (`#fit-view`)**:
   * Resets zoom, centering all nodes in the canvas viewport.
4. **Layer Filter (`#layer-filter`)**:
   * Options:
     * `实体与概念 (core)`: Shows only Person, Organization, DefinedTerm, SoftwareApplication.
     * `论断 (claims)`: Shows Claim nodes and their `makesClaim` / `supports` links.
     * `资料 (documents)`: Shows SourceDocument nodes and `about` / `mentions` links.
     * `全部层级 (all)`: Unfiltered graph view.
5. **Type Filter (`#type-filter`)**:
   * Filters nodes dynamically by Schema.org classification (e.g., `Person`, `Organization`, `DefinedTerm`).
6. **Graph Interaction**:
   * **Node Hover**: Highlights 1-hop connected edges and neighboring nodes; dims distant nodes.
   * **Node Drag**: Pins node location in the physics simulation.
   * **Node Click**: Displays node properties, aliases, and connected triples in status message (`#info`).
   * **Edge Click**: Opens the **Evidence Panel** (`#evidence-panel`) showing the exact verbatim quote and source reference supporting this triple.
7. **Tour Dock (Bottom Walkthrough Bar)**:
   * **Tour Step Indicator (`#tour-step`)**: E.g., `01 / 05`.
   * **Playback Controls**:
     * Previous (`#tour-prev`): Jumps to preceding summary step.
     * Play/Pause (`#tour-play`): Automatically steps through the article summary every $N$ seconds, animating the graph camera.
     * Next (`#tour-next`): Advances to subsequent summary step.
     * Speed Dropdown (`#tour-speed`): Select between `6s`, `10s`, or `15s` per step.
   * **View Evidence (`#evidence-open`)**: Pops open the evidence modal for the currently highlighted graph relationships.

---

## 5. Screen 3: Right Assistant Drawer (Query & Chat)

Located in `<aside id="query-panel" class="drawer">`. It slides out from the right edge and features an adjustable split-screen resizer.

```
+-----------------------------------------------------------------------------+
| <==> [ 展开 ]  和你的知识对话                                           [×] |
| [ 实体查询 ]  [ Chat ]                                                      |
+-----------------------------------------------------------------------------+
| 当前资料：OpenAI o1 深度解析                                                |
| [ 检查资料 ]  [ 重新分析并回写 ]  [ 同步笔记 ]                              |
|                                                                             |
| +-------------------------------------------------------------------------+ |
| | [Assistant] Codex 知识助手就绪。可检查资料、回写图谱或同步 Obsidian。   | |
| |                                                                         | |
| | [User] 这篇资料提到了哪些核心算法？                                     | |
| |                                                                         | |
| | [Assistant] 基于资料正文与图谱：                                        | |
| | 1. 强化学习（RL）用于推理时间计算拓展                                  | |
| | 2. 搜索与自我反思机制                                                   | |
| | [执行记录: kb_query_graph 成功 · 命中 8 条关系]                         | |
| +-------------------------------------------------------------------------+ |
|                                                                             |
| [v] 检索设置 (按词匹配 | Top 20 | 扩展相关词)     [v] 执行助手   [ 新对话 ] |
| +-------------------------------------------------------------------------+ |
| | 向知识库提问，或粘贴 YouTube 链接进行分析...                            | |
| +-------------------------------------------------------------------------+ |
| [ 发送 ]                         Enter 发送 · Shift + Enter 换行            |
+-----------------------------------------------------------------------------+
```

### Drawer Controls

1. **Width Resizer (`#workspace-resizer`)**:
   * Drag handle on the left edge allowing the user to resize the drawer from 320px up to 80% screen width.
2. **Expand / Collapse Button (`maximize`)**:
   * Toggles the drawer between compact drawer width and 50% split-pane mode.
3. **Close Button (`#assistant-close`)**:
   * Closes the drawer.

### Tab 1: 实体查询 (Entity Query View)
* **Search Input (`#query-input`)**: Queries entities and 1-hop subgraphs directly from SQLite.
* **Query Settings**:
  * Mode: `按词匹配 (terms)` vs. `全文匹配 (phrase)`.
  * Top-K: Range from 1 to 200 (default 20).
  * Expand checkbox (`#query-expand`): Resolves aliases and synonyms.
* **Results Display (`#query-results`)**: Renders structured entity cards with property tables and Obsidian vault links.

### Tab 2: Chat (Conversational Agent & Ingestion View)
* **Target Document Badge (`.chat-target`)**: Indicates currently focused document context.
* **Quick Action Buttons**:
  * **[ 检查资料 ]**: Sends pre-crafted prompt: *"请检查当前资料的正文、摘要和笔记是否一致，先不要修改。"*
  * **[ 重新分析并回写 ]**: Sends: *"请用完整正文重新分析当前资料，替换旧摘要和该来源的旧关系，并同步笔记。"*
  * **[ 同步笔记 ]**: Sends: *"请将当前资料最新的分析结果同步到 Obsidian 笔记，并验证结果。"*
* **执行助手 Toggle (`agentToggle`)**:
  * When checked (`true`): Agent is permitted to execute registered host tools (`kb_list_documents`, `kb_read_document`, `kb_reanalyze_document`, `kb_sync_note`, `kb_query_graph`).
  * When unchecked (`false`): Pure text Q&A without mutating host state.
* **Direct YouTube URL Processing**:
  * If the user pastes a YouTube URL into the chat box, the backend detects the video URL, runs ingestion and transcription, updates the graph, writes Obsidian notes, and streams the completion response into the chat.
* **Multi-turn History Pill**:
  * Retains up to 10 conversation turns (capped at 32,000 characters).
  * `[ 新对话 ]` button wipes the session buffer.

---

## 6. Modal 1: New Summary Ingestion Dialog (`#article-dialog`)

Triggered by clicking **`＋ 新建摘要`** in the top masthead.

```
+--------------------------------------------------------------------------+
| COLLECT · UNDERSTAND · CONNECT                                       [×] |
| 从文章，开始一篇摘要。                                                   |
+--------------------------------------------------------------------------+
| 粘贴文章正文                                                             |
|                                                                          |
| 文章标题 *                                                               |
| [ 给这篇文章一个名字...                                                ] |
|                                                                          |
| 来源链接（可选）                                                         |
| [ https://...                                                          ] |
|                                                                          |
| 文章正文 *                                                               |
| +----------------------------------------------------------------------+ |
| | 粘贴正文（20 - 100,000 字符）。将生成摘要、关键要点，并提取实体和关系。 | |
| +----------------------------------------------------------------------+ |
|                                                                          |
| 摘要与图谱会保存到你的知识库                                             |
| 使用已配置的模型，可能需要几分钟。              [ 生成摘要并入库 ↗ ]   |
+--------------------------------------------------------------------------+
```

* **Inputs**:
  * `#article-title` (Text, required, max 200 chars).
  * `#article-url` (URL, optional).
  * `#article-text` (Textarea, required, 20 to 100,000 chars).
* **Submit Action (`#article-submit`)**:
  * Sends `POST /api/articles` with JSON payload.
  * Disables form, displays spinner in `#article-status`.
  * On completion, closes modal, refreshes `#document-select`, and renders the newly generated graph.

---

## 7. Modal 2: Knowledge Editor (`#knowledge-editor`)

Triggered by clicking **`整理知识`** in the top masthead. Governs entity normalization, claim verification, and relation curation.

```
+-------------------------------------------------------------------------------------------------------------+
| CURATE YOUR KNOWLEDGE                                                        [ 修改记录 ]  [× 关闭 ]         |
| 整理知识  -  修正实体、核实论断，让每一条连接更准确。                                                         |
+---------------------------------------------------------+---------------------------------------------------+
| [ 搜索名称、别名或关系... ]                             | KNOWLEDGE RECORD                                  |
| 文章分类: [ 全部分类 v ]   来源文章: [ 全部文章 v ]     | 编辑实体                                          |
| [ 实体 ]  [ 论断 ]  [ 关系 ]                            | 修改后会同步关联关系；原始出处与证据继续保留。    |
| 记忆范围: [ 全部知识 v ]   审核状态: [ 全部审核状态 v ] |                                                   |
| ------------------------------------------------------- | 实体名称:                                         |
| 42 条记录 · 名称、类型与别名                            | [ OpenAI                                        ] |
| +-----------------------------------------------------+ | 实体类型:                                         |
| | OpenAI                                              | [ Organization v                                ] |
| | 组织 · 个人记忆 · 已审核                            | 别名 (每行一个):                                  |
| +-----------------------------------------------------+ | +-----------------------------------------------+ |
| | Sam Altman                                          | | OpenAI Inc                                    | |
| | 自然人 · 个人记忆 · 已审核                          | | OpenAI LP                                     | |
| +-----------------------------------------------------+ | +-----------------------------------------------+ |
| | o1-preview                                          |                                                   |
| | 软件或应用 · 资料库 · 未审核                        | ------------------------------------------------- |
| +-----------------------------------------------------+ | [x] 纳入个人记忆     [x] 已审核                   |
|                                                         | 立场: [ 认同 v ]                                  |
|                                                         | 个人判断说明:                                     |
|                                                         | [ 前沿模型研发领军机构...                       ] |
+---------------------------------------------------------+---------------------------------------------------+
| ● 有尚未保存的知识修改                     [ 删除关系 ]                    [ 重置修改 ]  [ 保存修改 (Primary) ] |
+-------------------------------------------------------------------------------------------------------------+
```

### Editor Tabs & Specific Forms

1. **Category & Article Filters (`#ke-category`, `#ke-article`)**:
   * Scopes displayed records to specific source documents.
2. **Category Tabs**:
   * **实体 (Entities)**: Modifies entity canonical `name`, `type` (Schema.org class), and `aliases` (line-separated list).
   * **论断 (Claims)**: Modifies claim text and `verificationStatus` (`待核实 / unverified`, `已核实 / verified`, `有争议 / disputed`, `已否定 / refuted`).
   * **关系 (Triples)**:
     * Subject searchable dropdown (`#ke-subject`).
     * Predicate selector (`#ke-predicate`).
     * Object searchable dropdown (`#ke-object`).
     * Confidence input (`#ke-confidence`, 0.0 - 1.0).
     * Read-only Evidence quote box (`blockquote.ke-evidence`).
3. **Personal Memory Section (Inside Editor Form)**:
   * Checkbox: `纳入个人记忆` (`#ke-memory-included`).
   * Checkbox: `已审核` (`#ke-memory-reviewed`).
   * Stance Selector: `认同 (agree)` / `存疑 (uncertain)` / `不认同 (disagree)` / `未表态 (unset)`.
   * Personal Note textarea.
4. **Action Buttons**:
   * `[ 保存修改 ]` (`#ke-save`): Submits mutation to `POST /api/editor/entity` or `POST /api/editor/triple`.
   * `[ 删除关系 ]` (`#ke-delete`): Available only for Triples; soft-deletes the link.
   * `[ 重置修改 ]` (`#ke-reset`): Reverts form to database baseline.
   * `[ 修改记录 ]` (`#ke-history`): Opens modal displaying audit log (`edit_history` table) with **[ 撤销 / Undo ]** buttons!

---

## 8. Modal 3: Personal Memory & Stance Dialog (`#memory-dialog`)

Triggered by clicking **`个人记忆`** in the top masthead. Governs subjective curation and protects against automatic stance alteration.

```
+-------------------------------------------------------------------------------------------------------------+
| PERSONAL RESEARCH MEMORY                                                                          [× 关闭 ] |
| 个人记忆与判断变化  -  收录是记住；审核是检查；个人立场由你决定。                                             |
+-------------------------------------------------------------------------------------------------------------+
| [ 搜索实体、论断或关系... ]  记忆范围: [ 全部知识 v ]   知识类别: [ 论断 v ]                                |
| 对照新资料: [ 选择用于对照的新资料 v ]  [ 新资料对旧判断的影响 (Compare) ]                                  |
+---------------------------------------------------------+---------------------------------------------------+
| 18 条知识记录                                           | o1-preview 具备强推理与自我纠错能力               |
| +-----------------------------------------------------+ | 设置仅属于这条记录，不会连带认可邻接实体。        |
| | o1-preview 具备强推理与自我纠错能力                 |                                                   |
| | 已审核 · 个人记忆 · 认同                            | 审核状态: [ 已审核 v ]                            |
| +-----------------------------------------------------+ | 记忆范围: [ 纳入个人记忆 v ]                      |
| | 纯强化学习将在 2026 年替代所有监督微调              | 我的立场: [ 存疑 (uncertain) v ]                  |
| | 已审核 · 个人记忆 · 存疑                            |                                                   |
| +-----------------------------------------------------+ | 我的判断或适用条件:                               |
|                                                         | [ 监督微调在领域对齐中仍有不可替代性...         ] |
|                                                         |                                                   |
|                                                         | 受哪篇资料影响: [ OpenAI o1 技术报告 v ]          |
|                                                         |                                                   |
|                                                         | [ 保存个人判断 (Primary) ]                        |
|                                                         | ------------------------------------------------- |
|                                                         | 当时记录的来源与证据                              |
|                                                         | 来源: OpenAI o1 Release <a>打开来源 ↗</a>         |
|                                                         | > "We found that RL enables complex CoT..."       |
+---------------------------------------------------------+---------------------------------------------------+
```

### Key Operations

1. **Dual Scopes**:
   * `个人记忆 (included: true)`: Included in the user's personal thought vault.
   * `资料库 (included: false)`: Retained as source material without personal adoption.
2. **Four Controlled Stances**:
   * `认同 (agree)`: User endorses the claim.
   * `存疑 (uncertain)`: User finds evidence inconclusive or actively questions it.
   * `不认同 (disagree)`: User refutes the claim.
   * `未表态 (unset)`: Default neutral stance.
3. **Compare Against New Source (`#memory-compare`)**:
   * Selects an ingested document from `#memory-source`.
   * Sends `POST /api/memory/compare`.
   * The LLM analyzes how the new document's claims impact the user's existing memory judgments.
   * Renders a structured comparison report **without automatically changing any saved user stance**.
4. **History Audit (`scope === 'history'`)**:
   * Selecting `判断变化记录` displays every past stance change, previous vs. new values, timestamp, and influencing source.
