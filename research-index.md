# 研究索引

> GEO / AEO / AI Search 领域的公开研究（2023–2026）。
> 分两部分：**我们按问题分组的精选**（带着判断读），和**完整清单**（按主题编，可检索）。

---

## 一、按八个问题分组（精选）

### 1 · 这件事值不值得做

| 研究 | 它说明了什么 | 出处 |
|---|---|---|
| **How Generative AI Disrupts Search: Consumer Behavior, Website Traffic, and the Impact of Google AI Overviews** | 用真实日志数据，量化 AI 摘要对用户行为和网站流量的影响 | ACM SIGIR 2026 |
| **Zero-Click Search and Answer Engines: A Literature Review** | 系统性梳理"零点击"趋势下搜索可见性的转型 | JIEM, 2025 |
| **Characterizing Web Search in the Age of Generative AI** | 对比传统搜索与生成式搜索的检索足迹与稳定性差异 | arXiv:2510.11560 |
| **GEO: Generative Engine Optimization** | 这个领域的奠基论文，提出 GEO 的问题、方法与评测基准 | KDD 2024 / arXiv:2311.09735 |

### 2 · "对题"为什么比"权威"更重要

| 研究 | 它说明了什么 | 出处 |
|---|---|---|
| **From Citation Selection to Citation Absorption** | 提出"引用选择 → 引用吸收"两阶段框架；与引用影响力相关性最高的是**内容与问题的匹配度**，高于内容质量本身 | arXiv:2604.25707 |
| **C-SEO Bench: Does Conversational SEO Work?** | 建立基准，系统检验"对话式优化"到底有没有效果 | NeurIPS Datasets & Benchmarks 2025 / arXiv:2506.11097 |
| **AI Answer Engine Citation Behavior: A Longitudinal Study of GEO in 16 Generative Engines** | 16 个生成式引擎的引用行为纵向研究 | arXiv:2509.10762 |
| **GEO at Scale: Measuring Brand Visibility Across AI Search Engines** | 跨引擎的品牌可见度规模化测量 | arXiv:2606.20065 |

### 3 · "引用广度"和"吸收深度"是两件事

| 研究 | 它说明了什么 | 出处 |
|---|---|---|
| **From Citation Selection to Citation Absorption** | 引得多不等于影响大：有的引擎引用条数多但影响力弱，有的引用条数少但影响强——两个指标必须分开测量 | arXiv:2604.25707 |
| **AI Answer Engine Citation Behavior** | 同一内容在不同引擎里的引用行为不一样，单平台结论不能外推 | arXiv:2509.10762 |
| **When Content is Goliath and Algorithm is David: The Style and Semantic Effects of Generative Search Engine** | 内容风格与语义结构，各自如何影响生成式搜索的取舍 | ResearchGate, 2025 |

### 4 · 内容写成什么样，才会被引用

| 研究 | 它说明了什么 | 出处 |
|---|---|---|
| **What Generative Search Engines Like: Explaining and Optimizing Website Visibility** | 解释生成式搜索偏好什么样的页面，并给出可操作的优化方向 | arXiv:2510.11438 |
| **Structural Feature Engineering for Generative Engine Optimization** | 页面结构特征与引用效果之间的关系——结构本身有独立贡献 | arXiv:2603.29979 |
| **Think Before Writing: Feature-Level Optimization for Generative Engine Optimization** | 在写作之前做特征级优化，比写完再改有效 | arXiv:2604.19113 |
| **What Evidence Do Language Models Find Convincing?** | 模型认为什么样的证据可信——直接影响内容该怎么写 | arXiv:2402.11782 |

### 5 · 怎么测才可信（方法问题）

| 研究 | 它说明了什么 | 出处 |
|---|---|---|
| **Don't Measure Once: Reliable AI Search Visibility Requires Repeated Trials and Structure-Aware Metrics** | 单次测量不可靠——可见性评估需要重复试验与结构感知指标 | arXiv:2604.07585 |
| **Disentangling Answer Engine Optimization from Platform Growth: A Log-Based Natural Experiment on ChatGPT Referral Traffic** | 用日志自然实验，把"优化带来的变化"与"平台自身的增长"分开 | arXiv:2606.04362 |
| **SAGEO: A Search Arena for Generative Engine Optimization in a Realistic Environment** | 更接近真实环境的评测场，用于对比不同做法 | arXiv:2602.12187 |
| **SAGE: Scalable AI Governance & Evaluation** | 生产级搜索的评估与治理框架 | arXiv:2602.07840 |

### 6 · "引到错的版本"是已被研究过的风险

| 研究 | 它说明了什么 | 出处 |
|---|---|---|
| **CONFLICTBANK: A Benchmark for Evaluating the Influence of Knowledge Conflicts in LLMs** | 当模型同时检索到新旧两版信息时，回答会不稳定——知识冲突可以被测量 | OpenReview, 2024 |
| **Persistent Pre-Training Poisoning of LLMs** | 预训练阶段的污染会长期留存，且难以事后清除 | arXiv:2410.13722 |
| **Adversarial Search Engine Optimization for Large Language Models** | 对抗式优化（把内容"塞给"模型）的手法与机理 | arXiv:2406.18382 |
| **Manipulating Large Language Models to Increase Product Visibility** | 操纵内容以提升可见度的具体路径 | arXiv:2404.07981 |

### 7 · 合规做法是可行的

| 研究 | 它说明了什么 | 出处 |
|---|---|---|
| **White Hat Search Engine Optimization using Large Language Models** | 用合规手段做内容优化，效果有实证依据 | arXiv:2502.07315 |
| **Unveiling the Resilience of LLM-Enhanced Search Engines Against Adversarial Attacks** | 模型侧对操纵手段的抗性正在增强——捷径的窗口在收窄 | arXiv:2603.25500 |
| **风险与操纵主题（共 10 篇）** | 刷量、投毒、排名操纵的手法与检测研究 | 见下方完整清单 06 类 |

### 8 · 要做底座，技术上怎么搭

| 研究 | 它说明了什么 | 出处 |
|---|---|---|
| **MCompassRAG: Topic Metadata as a Semantic Compass for Paragraph-Level Retrieval** | 主题元数据能显著改善段落级检索——"分类"这件事在技术上是有效的 | arXiv:2606.18508 |
| **Decoupling Search from Reasoning: A Vendor-Agnostic Grounding Architecture for LLM Agents** | 把"检索"与"推理"解耦，做与厂商无关的可信来源层 | arXiv:2606.18947 |
| **SproutRAG: Attention-Guided Tree Search for Long-Document RAG** | 长文档场景下的检索优化 | arXiv:2606.18381 |

---

## 二、完整清单（54 篇 · 按 10 个主题）

### 01 · GEO 基础框架（4）

| 标题 | 年 | 来源 |
|---|---|---|
| GEO: Generative Engine Optimization | 2023/24 | arXiv:2311.09735 · KDD 2024 |
| Generative Engine Optimization in Digital Repositories | 2025 | Infonomy |
| Generative Engine Optimization: How to Dominate AI Search | 2025 | arXiv:2509.08919 |
| Navigating the Shift: Web Search vs Generative AI Response Generation | 2026 | arXiv:2601.16858 |

### 02 · GEO 方法优化（7）

| 标题 | 年 | 来源 |
|---|---|---|
| Beyond Keywords: GSEO with Content-Centric Agents | 2025 | arXiv:2509.05607 |
| Beyond SEO: A Transformer-Based Approach for Web Content Optimisation | 2025 | arXiv:2507.03169 |
| IF-GEO: Conflict-Aware Instruction Fusion for Multi-Query GEO | 2026 | arXiv:2601.13938 |
| Role-Augmented Intent-Driven GSEO | 2025 | arXiv:2508.11158 |
| Think Before Writing: Feature-Level Optimization for GEO | 2026 | arXiv:2604.19113 |
| What Generative Search Engines Like | 2025 | arXiv:2510.11438 |
| White Hat Search Engine Optimization using LLMs | 2025 | arXiv:2502.07315 |

### 03 · GEO 测量评估（8）

| 标题 | 年 | 来源 |
|---|---|---|
| AI Answer Engine Citation Behavior: A Longitudinal Study in 16 Generative Engines | 2025 | arXiv:2509.10762 |
| C-SEO Bench: Does Conversational SEO Work? | 2025 | arXiv:2506.11097 · NeurIPS D&B |
| Don't Measure Once: Reliable AI Search Visibility Requires Repeated Trials | 2026 | arXiv:2604.07585 |
| Disentangling AEO from Platform Growth: Log-Based Natural Experiment on ChatGPT Referral | 2026 | arXiv:2606.04362 |
| From Citation Selection to Citation Absorption | 2026 | arXiv:2604.25707 |
| GEO at Scale: Measuring Brand Visibility Across AI Search Engines | 2026 | arXiv:2606.20065 |
| SAGEO: A Search Arena for GEO in a Realistic Environment | 2026 | arXiv:2602.12187 |
| Structural Feature Engineering for GEO | 2026 | arXiv:2603.29979 |

### 04 · AI 搜索实证（6）

| 标题 | 年 | 来源 |
|---|---|---|
| A Survey of Generative Search and Recommendation in the Era of LLMs | 2024/25 | generative-rec.github.io |
| Characterizing Web Search in the Age of Generative AI | 2026 | arXiv:2510.11560 |
| What Do Chinese-Language Generative Search Engines Cite and Surface? | 2026 | arXiv:2607.15771 |
| How Generative AI Disrupts Search: Consumer Behavior, Website Traffic, Google AI Overviews | 2026 | ACM SIGIR 2026 |
| NExT-Search: Rebuilding User Feedback Ecosystem for Generative AI Search | 2025 | arXiv:2505.14680 |
| What Evidence Do Language Models Find Convincing? | 2024 | arXiv:2402.11782 |

### 05 · AEO 理论整合（5）

| 标题 | 年 | 来源 |
|---|---|---|
| From SEO to AEO: Generative AI and the Transformation of Search Visibility | 2025 | ResearchGate |
| Optimizing for the AI-Driven Search Era: Integrated Framework for SEO/GEO/AEO | 2025 | IJSREM |
| Smart Search Optimization: Integrating SEO, AEO and GEO | 2025 | Loro Journal |
| How the Transition from SEO to GEO, AEO, and AIO Impacts Digital Marketing | 2025 | IJCRT |
| Zero-Click Search and Answer Engines: A Literature Review | 2025/26 | JIEM |

### 06 · 风险、操纵与对抗（10）

| 标题 | 年 | 来源 |
|---|---|---|
| Adversarial Search Engine Optimization for LLMs | 2024 | arXiv:2406.18382 |
| CONFLICTBANK: Knowledge Conflicts in LLMs | 2024 | OpenReview |
| Dynamics of Adversarial Attacks on LLM-Based Search Engines | 2025 | arXiv:2501.00745 |
| GASLITEing the Retrieval: Vulnerabilities in Dense Embedding-Based Search | 2024/25 | OpenReview |
| Manipulating LLMs to Increase Product Visibility | 2024 | arXiv:2404.07981 |
| Persistent Pre-Training Poisoning of LLMs | 2024 | arXiv:2410.13722 |
| PoisonArena: Competing Poisoning Attacks in RAG | 2025 | arXiv:2505.12574 |
| Ranking Manipulation for Conversational Search Engines | 2024 | arXiv:2406.03589 |
| StealthRank: LLM Ranking Manipulation via Stealthy Prompt Optimization | 2025 | arXiv:2504.05804 |
| Unveiling the Resilience of LLM-Enhanced Search Engines Against Adversarial Attacks | 2026 | arXiv:2603.25500 |

### 07 · 垂直场景与多模态（5）

| 标题 | 年 | 来源 |
|---|---|---|
| Caption Injection for Optimization in Generative Search Engines | 2025 | arXiv:2511.04080 |
| E-GEO: A Testbed for GEO in E-Commerce | 2025 | arXiv:2511.20867 |
| Multimodal GEO: Rank Manipulation for VLM Rankers | 2026 | ResearchGate |
| GEO: A VLM and Agent Framework for Pinterest Acquisition Growth | 2026 | arXiv:2602.02961 |
| When Content is Goliath and Algorithm is David: Style and Semantic Effects | 2025 | ResearchGate |

### 08 · AI 搜索架构与 Agentic Search（4）

| 标题 | 年 | 来源 |
|---|---|---|
| Decoupling Search from Reasoning: A Vendor-Agnostic Grounding Architecture | 2026 | arXiv:2606.18947 |
| Beyond Parallel Sampling: Diverse Query Initialization for Agentic Search | 2026 | arXiv:2606.17209 |
| ScholarQuest: Taxonomy-Guided Benchmark for Agentic Academic Paper Search | 2026 | arXiv:2606.20235 |
| When Does Streaming Tool Use Help? Tool-Intent Stabilization in Streaming RAG | 2026 | arXiv:2606.20113 |

### 09 · RAG 检索优化（3）

| 标题 | 年 | 来源 |
|---|---|---|
| MCompassRAG: Topic Metadata as a Semantic Compass for Paragraph-Level Retrieval | 2026 | arXiv:2606.18508 |
| SCAR: Semantic Continuity-Aware Retrieval for RAG | 2026 | arXiv:2606.16661 |
| SproutRAG: Attention-Guided Tree Search for Long-Document RAG | 2026 | arXiv:2606.18381 |

### 10 · 搜索评估与治理（2）

| 标题 | 年 | 来源 |
|---|---|---|
| Scaling Search Relevance: Augmenting App Store Ranking with LLM-Generated Judgments | 2026 | arXiv:2602.23234 |
| SAGE: Scalable AI Governance & Evaluation | 2026 | arXiv:2602.07840 |

---

## 三、怎么用这份索引

1. **按问题读**——先看第一部分，八个问题对应八组文献；
2. **按主题查**——第二部分按 10 个主题编，可直接用 arXiv 编号取原文；
3. **顺手核**——所有出处都是公开可复查的；引用时注明来源即可。

> 各篇著作权归原作者或出版方，本索引只做编目与指向，不转载原文。
