"""Populate OntoKB SQLite database with a rich, realistic knowledge graph.
Covers multiple articles, entities of diverse Schema.org types, evidence-preserving triples,
and personal memory stances.
"""
from __future__ import annotations

import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from ontokb.graph import GraphStore
from ontokb.models import ExtractedEntity, ExtractedTriple
from ontokb.ontology import Ontology
from ontokb.reading import reading_library
from ontokb.visualize import graph_data
from ontokb.memory import MemoryService


def seed_database(db_path: str | Path, ontology_path: str | Path) -> None:
    onto = Ontology.load(ontology_path)
    graph = GraphStore(db_path, ontology=onto)

    # 1. Clear any old data
    tables = [
        "entities", "aliases", "triples", "contents",
        "manual_entities", "manual_triples", "manual_triple_keys",
        "edit_history", "personal_memory", "memory_history"
    ]
    with graph.conn:
        for t in tables:
            graph.conn.execute(f"DELETE FROM {t}")
        try:
            graph.conn.execute("DELETE FROM sqlite_sequence")
        except sqlite3.OperationalError:
            pass

    print("[1/5] Database reset completed.")

    # 2. Define Entities
    entities = [
        # Organizations
        ExtractedEntity(name="OpenAI", type="Organization", aliases=["Open AI", "OpenAI Inc"]),
        ExtractedEntity(name="Anthropic", type="Organization", aliases=["Anthropic PBC"]),
        ExtractedEntity(name="NVIDIA", type="Organization", aliases=["英伟达", "NVDA"]),
        ExtractedEntity(name="Microsoft", type="Organization", aliases=["微软", "MSFT"]),
        # People
        ExtractedEntity(name="Sam Altman", type="Person", aliases=["山姆·奥特曼", "Altman"]),
        ExtractedEntity(name="Noam Brown", type="Person", aliases=["诺姆·布朗"]),
        ExtractedEntity(name="Dario Amodei", type="Person", aliases=["达里奥·阿莫代", "Amodei"]),
        ExtractedEntity(name="Jensen Huang", type="Person", aliases=["黄仁勋", "Jensen"]),
        # Software Applications
        ExtractedEntity(name="o1", type="SoftwareApplication", aliases=["OpenAI o1", "Strawberry"]),
        ExtractedEntity(name="Codex", type="SoftwareApplication", aliases=["OpenAI Codex"]),
        ExtractedEntity(name="Claude 3.5 Sonnet", type="SoftwareApplication", aliases=["Claude 3.5", "Sonnet"]),
        ExtractedEntity(name="ontoKB", type="SoftwareApplication", aliases=["OntoKB v2", "OntoKB System"]),
        ExtractedEntity(name="PyTorch", type="SoftwareApplication", aliases=["pytorch"]),
        ExtractedEntity(name="Triton", type="SoftwareApplication", aliases=["OpenAI Triton"]),
        # Products
        ExtractedEntity(name="Blackwell", type="Product", aliases=["GB200", "B200"]),
        # Defined Terms (Technologies & Concepts)
        ExtractedEntity(name="强化学习", type="DefinedTerm", aliases=["Reinforcement Learning", "RL"]),
        ExtractedEntity(name="思维链推理", type="DefinedTerm", aliases=["Chain of Thought", "CoT"]),
        ExtractedEntity(name="测试时计算扩展", type="DefinedTerm", aliases=["Test-Time Compute", "Inference Scaling"]),
        ExtractedEntity(name="知识图谱", type="DefinedTerm", aliases=["KG", "Knowledge Graph"]),
        ExtractedEntity(name="检索增强生成", type="DefinedTerm", aliases=["RAG", "Retrieval-Augmented Generation"]),
        ExtractedEntity(name="端到端芯片互联", type="DefinedTerm", aliases=["NVLink", "InfiniBand"]),
        ExtractedEntity(name="知识工程", type="DefinedTerm", aliases=["Knowledge Engineering"]),
        # Claims
        ExtractedEntity(
            name="论断：测试时算力可线性提升推理准确率",
            type="Claim",
            properties={
                "text": "测试时计算扩展可在复杂推理任务中持续提升模型准确率",
                "verificationStatus": "verified"
            }
        ),
        ExtractedEntity(
            name="论断：强本体约束能消除智能体幻觉",
            type="Claim",
            properties={
                "text": "引入闭世界本体模式与确定性校验能够彻底遏制知识生成幻觉",
                "verificationStatus": "disputed"
            }
        ),
        ExtractedEntity(
            name="论断：后训练算力需求将超越预训练",
            type="Claim",
            properties={
                "text": "随着强化学习与测试时计算普及，后训练和推理算力开销将全面超越预训练阶段",
                "verificationStatus": "unverified"
            }
        ),
        ExtractedEntity(
            name="论断：未经人类审查的自动化知识入库必将崩溃",
            type="Claim",
            properties={
                "text": "缺乏人工介入与收据回溯机制的自动化知识抽取最终会导致知识库语义漂移和灾难性遗忘",
                "verificationStatus": "verified"
            }
        ),
    ]

    for ent in entities:
        graph.upsert_entity(ent, source="system:seed")

    print(f"[2/5] Seeded {len(entities)} typed entities.")

    # 3. Define Articles / Content Items
    articles = [
        {
            "id": "doc:openai-o1",
            "kind": "article",
            "source": "OpenAI Blog",
            "url": "https://openai.com/research/o1",
            "title": "OpenAI o1 架构与强化学习推理拓展",
            "status": "processed",
            "meta": {
                "categories": ["科技"],
                "summary": "OpenAI 正式发布具备长思维链推理能力的新模型 o1。该模型由 Noam Brown 等研究员参与设计，核心机制在于将强化学习引入测试时计算扩展。测试表明，论断：测试时算力可线性提升推理准确率在数学与编程基准上得到有力验证。Sam Altman 强调该突破将为未来的自主编程工具如 Codex 带来全新技术底座。",
                "key_points": [
                    "o1 通过强化学习训练隐式思维链，开辟测试时算力扩展新范式",
                    "Noam Brown 等人在博弈与决策领域的经验被成功迁移至大语言模型",
                    "测试时计算提升为复杂逻辑推理与代码生成奠定基石"
                ],
                "topics": ["大模型", "强化学习", "测试时计算", "OpenAI"]
            },
            "triples": [
                ("Sam Altman", "worksFor", "OpenAI", "Sam Altman serves as CEO of OpenAI, driving frontier AI strategy.", 0.95),
                ("Noam Brown", "worksFor", "OpenAI", "Noam Brown joined OpenAI to lead research on reasoning algorithms and multi-step RL.", 0.95),
                ("OpenAI", "develops", "o1", "OpenAI announced o1, a new series of reasoning models that spend more time thinking.", 0.98),
                ("OpenAI", "develops", "Codex", "OpenAI continues to maintain and evolve Codex for code completion and synthesis.", 0.92),
                ("o1", "uses", "强化学习", "The reasoning engine of o1 is trained with large-scale reinforcement learning.", 0.95),
                ("o1", "uses", "思维链推理", "o1 uses a chain of thought when thinking through user queries before answering.", 0.95),
                ("o1", "uses", "测试时计算扩展", "Inference compute scaling allows o1 to think longer on harder problems.", 0.92),
                ("OpenAI", "makesClaim", "论断：测试时算力可线性提升推理准确率", "OpenAI empirical results confirm that performance continues to scale with more test-time compute.", 0.90),
            ]
        },
        {
            "id": "doc:claude-35-agent",
            "kind": "article",
            "source": "Anthropic Research",
            "url": "https://anthropic.com/claude",
            "title": "Claude 3.5 Sonnet 与具身代码智能体实践",
            "status": "processed",
            "meta": {
                "categories": ["科技"],
                "summary": "Anthropic 由 Dario Amodei 领导，推出了业界领先的推理模型 Claude 3.5 Sonnet。该模型在开源框架 ontoKB 的日常知识工程实践中被深入应用，结合检索增强生成与知识图谱技术。开发者提出论断：强本体约束能消除智能体幻觉，但业界对其普适性仍有不同观点。同时，Anthropic 在前沿基础大模型领域与 OpenAI 展开激烈竞争。",
                "key_points": [
                    "Claude 3.5 Sonnet 在复杂工具调用与上下文理解中表现突出",
                    "ontoKB 融合 Schema.org 规范本体与个人记忆审查机制",
                    "结构化知识图谱与非结构化 RAG 的混合架构成为行业趋势"
                ],
                "topics": ["知识图谱", "智能体", "Anthropic", "RAG"]
            },
            "triples": [
                ("Dario Amodei", "worksFor", "Anthropic", "Dario Amodei is CEO and co-founder of Anthropic.", 0.98),
                ("Anthropic", "develops", "Claude 3.5 Sonnet", "Anthropic released Claude 3.5 Sonnet as its flagship intelligent model.", 0.98),
                ("Anthropic", "competesWith", "OpenAI", "Anthropic directly competes with OpenAI across frontier foundation models.", 0.92),
                ("ontoKB", "uses", "Claude 3.5 Sonnet", "ontoKB integrates Claude 3.5 Sonnet as the reasoning and extraction engine.", 0.90),
                ("ontoKB", "uses", "知识图谱", "ontoKB stores facts in a schema-aligned SQLite knowledge graph.", 0.95),
                ("ontoKB", "uses", "检索增强生成", "Hybrid retrieval combines dense search with graph-guided RAG contexts.", 0.88),
                ("ontoKB", "makesClaim", "论断：强本体约束能消除智能体幻觉", "Experimental reports from ontoKB claim strict ontological boundaries curb ungrounded model output.", 0.85),
            ]
        },
        {
            "id": "doc:nvidia-ai-infrastructure",
            "kind": "article",
            "source": "GTC Keynote",
            "url": "https://nvidia.com/ai-infrastructure",
            "title": "NVIDIA 算力集群与下一代模型基础设施",
            "status": "processed",
            "meta": {
                "categories": ["科技"],
                "summary": "NVIDIA 首席执行官 Jensen Huang 展示了新一代 Blackwell 架构计算芯片。该平台深度整合端到端芯片互联技术，专门优化 PyTorch 与 Triton 等前沿深度学习系统。OpenAI 等顶级机构已部署 Blackwell 集群用于大模型后训练。黄仁勋在演讲中提出论断：后训练算力需求将超越预训练，引发了全行业对算力配比策略的广泛讨论。",
                "key_points": [
                    "Blackwell 架构大幅降低大规模分布式推理的能耗与延迟",
                    "NVLink 互联带宽满足长思维链测试时计算的高通量需求",
                    "PyTorch 与 Triton 成为各大算力集群上的通用编程标准"
                ],
                "topics": ["芯片算力", "基础设施", "NVIDIA", "推理计算"]
            },
            "triples": [
                ("Jensen Huang", "worksFor", "NVIDIA", "Jensen Huang is the founder and CEO of NVIDIA.", 0.98),
                ("NVIDIA", "makes", "Blackwell", "NVIDIA manufactures the Blackwell GPU architecture for massive AI workloads.", 0.98),
                ("NVIDIA", "develops", "端到端芯片互联", "NVIDIA developed fifth-generation NVLink high-speed interconnect technology.", 0.94),
                ("Blackwell", "uses", "端到端芯片互联", "Blackwell accelerators leverage NVLink for high-bandwidth multi-GPU pooling.", 0.95),
                ("OpenAI", "adopts", "Blackwell", "OpenAI deployed clusters of NVIDIA Blackwell hardware for inference and post-training.", 0.90),
                ("OpenAI", "develops", "Triton", "OpenAI designed Triton to enable high-efficiency GPU kernel writing in Python.", 0.95),
                ("Triton", "uses", "PyTorch", "Triton integrates seamlessly with PyTorch 2.0 compiler backends.", 0.92),
                ("Jensen Huang", "makesClaim", "论断：后训练算力需求将超越预训练", "Jensen Huang remarked that post-training and test-time reasoning will dominate global AI FLOPS.", 0.88),
            ]
        },
        {
            "id": "doc:kg-and-personal-memory",
            "kind": "article",
            "source": "Knowledge Systems Review",
            "url": "https://example.org/personal-kg",
            "title": "个人数字第二大脑与本体论知识库演进",
            "status": "processed",
            "meta": {
                "categories": ["历史", "科技"],
                "summary": "从早期的专家系统到现代知识工程，个人知识管理正在经历深刻转变。ontoKB 通过将客观文章证据与个人主观记忆严格隔离，探索抗漂移的知识维护范式。文中指出论断：未经人类审查的自动化知识入库必将崩溃，提醒开发者不可过度依赖纯黑盒抽取。Microsoft 等大型企业在知识工程中的长期教训也证实了审计收据的重要性。",
                "key_points": [
                    "知识工程的长期价值在于本体的确定性与关系的严谨性",
                    "个人记忆库允许针对同一客观论断表达认同、存疑或反对态度",
                    "不可篡改的变更日志与收据机制保障知识演化的透明度"
                ],
                "topics": ["知识管理", "本体", "第二大脑"]
            },
            "triples": [
                ("Microsoft", "competesWith", "OpenAI", "Microsoft and OpenAI maintain a strategic yet increasingly competitive AI relationship.", 0.85),
                ("Microsoft", "adopts", "知识工程", "Microsoft utilizes enterprise knowledge graphs across Office and Bing ecosystems.", 0.90),
                ("ontoKB", "uses", "知识工程", "ontoKB adheres to formal Schema.org ontological principles.", 0.95),
                ("ontoKB", "makesClaim", "论断：未经人类审查的自动化知识入库必将崩溃", "The ontoKB design document argues unverified automatic ingestion leads to catastrophic semantic drift.", 0.90),
                ("论断：测试时算力可线性提升推理准确率", "supports", "论断：后训练算力需求将超越预训练", "Empirical test-time scaling results directly support Huang's claim that post-training compute will dominate.", 0.85),
            ]
        }
    ]

    for art in articles:
        # Upsert content
        graph.upsert_content(
            content_id=art["id"],
            kind=art["kind"],
            source=art["source"],
            url=art["url"],
            title=art["title"],
            status=art["status"],
            meta=art["meta"],
        )
        # Add associated triples
        for s, p, o, ev, conf in art["triples"]:
            graph.add_triple(
                ExtractedTriple(subject=s, predicate=p, object=o, evidence=ev, confidence=conf),
                ontology=onto,
                source=art["id"]
            )

    print(f"[3/5] Seeded {len(articles)} articles and associated triples.")

    # 4. Seed Personal Memory with sample reviews & stances
    mem = MemoryService(graph)
    targets = mem.targets()
    now_str = datetime.now(timezone.utc).isoformat()
    
    # Review a few items to give life to Personal Memory drawer
    # Find claim target keys
    sample_reviews = [
        ("论断：测试时算力可线性提升推理准确率", "agree", "数学和代码基准已有重复验证，符合扩展定律预期。"),
        ("论断：强本体约束能消除智能体幻觉", "uncertain", "本体能约束类型边界，但难以完全避免开放域事实性错觉，尚需更多实证。"),
        ("论断：未经人类审查的自动化知识入库必将崩溃", "agree", "极其认同，黑盒自动化抽取若无人工把关必然产生级联污染。"),
    ]

    with graph.conn:
        for target_key, snapshot in targets.items():
            for claim_title, stance, note in sample_reviews:
                if snapshot.get("title") == claim_title:
                    graph.conn.execute(
                        """INSERT OR REPLACE INTO personal_memory 
                           (key, snapshot, reviewed, included, stance, note, revision, updated_at)
                           VALUES (?, ?, 1, 1, ?, ?, 1, ?)""",
                        (target_key, json.dumps(snapshot, ensure_ascii=False), stance, note, now_str)
                    )

    print("[4/5] Seeded Personal Memory curated stances.")

    # 5. Verification
    data = graph_data(graph)
    lib = reading_library(graph)
    print(f"[5/5] Done! Total nodes: {len(data['nodes'])}, Total edges: {len(data['edges'])}, Library docs: {len(lib)}")
    for doc in lib:
        print(f"  - [{doc['id']}] '{doc['title']}' ({len(doc['steps'])} summary steps, {doc['entity_count']} entities, {doc['relation_count']} relations)")

    graph.close()


if __name__ == "__main__":
    import sys
    db = Path("data/kb.db")
    onto = Path("ontology/core.yaml")
    seed_database(db, onto)
