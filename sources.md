# 来源、许可与致谢

> 本仓库只做**编目、指向与判断**，不转载原文。

---

## 一、研究索引的来源

`research-index.md` 中 54 篇论文的编目，主要来自一个公开整理的中文 GEO 研究合集：

**GEO Citation Lab** —— 一个持续维护的 GEO / AEO / AI Search 研究库，按 10 个主题收录 54 篇论文（2023–2026），并提供在线检索与来源链接。

- 仓库：`github.com/yaojingang/geo-citation-lab`
- 论文目录：`02-geo-aeo-ai-search-papers/`（含论文清单 CSV 与在线导航页）
- 数据集：同仓库 `03-cn-geo-citation-dataset/`（中文生成式 AI 引用数据集）
- 实验报告：同仓库 `01-geo-experiment-data-report/`

**整理者**：姚金刚（yaojingang）—— 主页 `laoyao.cn`。国内较早从事 GEO 实务与开源的人之一，公开产出包括：

| 项目 | 类型 |
|---|---|
| `geo-citation-lab` | 数据集 + 实验报告 + 论文库 |
| [`GEORank`](https://github.com/yaojingang/GEORank) | GEO 排名与优化平台 |
| [`GEOHub`](https://github.com/yaojingang/GEOHub) | GEO / SEO agent skills |
| `GEOFlow` | GEO 内容工程与多站分发系统 |
| `yao-open-prompts` | 中文提示词库 |
| `yao-geo-skills` | GEO 相关 Skill 合集 |

**许可**：上述仓库的**代码采用 MIT**，**报告与文档采用 CC BY 4.0**（可转载，须署名）。本仓库在编目时保留了题名、年份与出处链接，即为其要求的署名方式。

> ⚠️ **论文本身的著作权归原作者与出版方**。本仓库**不存放、不转载任何论文 PDF**，只提供题名与出处（arXiv 编号 / 会议名），供读者自行检索原文。

---

## 二、工具生态的来源

`tool-ecosystem.md` 中的项目信息来自 GitHub 公开检索（2026-09-24），题名、简介与 star 数均为检索时的公开数据。

**各项目的许可请以其仓库自身声明为准**——本仓库只做指向，不代为声明。

---

## 三、技术标准的来源

`standards.md` 中涉及的 llms.txt 提案与相关项目，来源为其各自公开仓库。

---

## 三之二、文章里引用的外部研究

站内文章引用外部研究时，**逐个列出题名与链接**，并把「逐字可确认」和「处理原则」分开标。

| 文章 | 引用的研究 | 出处 |
|---|---|---|
| 《你那张验收单，是原题还是改过的》（2026-11-08） | EBU × BBC 联合研究：AI 助手在 45% 的案例里歪曲新闻内容（与语种、地域无关） | BBC Media Centre：<https://www.bbc.co.uk/mediacentre/2025/new-ebu-research-ai-assistants-news-content> |
| 同上 | MaxxBench：89 个 DeepSWE 任务只改指令／起始代码；15 个配置分差 20.9→48.3 个百分点；六个配置由 1.5 点内散到 23.0 点；DeepSeek V4.1 Flash 74.2%→55.6%；修 bug 后重评平均分 65.8%→64.5%（1.3 个百分点） | MaxxBench 研究页：<https://maxxbench.unlap.ai/research/why-maxxbench/>（2026-11-07） |

| 《那 56% 不是 AI 挣来的》（2026-11-08） | Business Insider 2025-05 裁 21%、转向 AI | Nieman Lab：<https://www.niemanlab.org/2025/05/business-insider-will-lay-off-21-of-staff-amid-ai-disruption-and-extreme-traffic-drops-outside-of-our-control/> |
| 同上 | 工会声明原句 “No slop in our shop!”、要求向读者披露 AI 产出 | Talking Biz News：<https://talkingbiznews.com/media-news/business-insider-union-slams-ai-effort/> |
| 同上 | 芒果超媒《后西游记》上星、5 个交易日 +56.19%（来自综艺《后会友期》）、Q3 归母净利 1,155 万（−95.42%）、公允价值变动损失 7,311 万 | 虎嗅转妙投 APP（2026-11-08）：<https://www.huxiu.com/article/4903839.html> ⚠️ 二手（券商转述，数据源 Wind），财务数须回财报核 |

> ⚠️ **BBC 那条「AI 稿没有编辑签字不发」，引的是该项研究之后的处理原则，不是一份逐字可查的编辑部章程。** 原文以 BBC 与 EBU 的公告为准。
> ⚠️ 文中把「新闻歪曲率 45%」与「代码基准漂移 23 个点」并置，**属类比，不是论证** —— 两个对象不同量，文章正文已明写。

---

**关于《AI 观察线》的读数**：栏目里的「扫了多少条／立住几条／成稿几篇」**是我们自己管线的运行数据（自测口径）**，不是外部统计。我们公开方法与类别，不公开抓取参数。线索中引用的外部事实，一律给出原始出处。

## 四、本仓库的许可

- **文字内容**：CC BY 4.0 —— 可转载、可改编，注明来源即可；
- **引用他人研究**：均注明题名与出处；如涉版权问题，请联系更正。

---

## 五、我们不做什么

- 不转载论文原文（只指向）；
- 不放任何未公开的一手数据；
- 不把整理成果说成原创研究——**编目是编目，判断是判断，两者在本仓库里分开标注**。

---

*最后更新：2026-11-11*
