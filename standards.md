# 技术标准与 AI 可读性

> 内容要被 AI 引用，先得被 AI **读得懂**。
> 这是一层公开的技术约定——不神秘，但容易被忽略。

---

## 一、llms.txt

**是什么**：在网站根目录放一个 Markdown 文件（`/llms.txt`），用结构化的方式告诉语言模型：这个站点有什么、哪些内容重要、怎么读。

**为什么会有**：现有的 `robots.txt` 只解决"能不能抓"，`sitemap.xml` 只解决"有哪些页"。而模型需要的是**理解**——哪些是核心内容、哪些是导航噪音。

**格式**：Markdown，一般包含站点简介 + 分组链接列表。

| 项目 | ★ | 是什么 |
|---|---:|---|
| [AnswerDotAI/llms-txt](https://github.com/AnswerDotAI/llms-txt) | 2629 | llms.txt 的提案与说明 |
| [thedaviddias/llms-txt-hub](https://github.com/thedaviddias/llms-txt-hub) | 906 | 已采用 llms.txt 的站点目录 |
| [firecrawl/llmstxt-generator](https://github.com/firecrawl/llmstxt-generator) | 537 | 为任意站点生成 llms.txt / llms-full.txt |

---

## 二、和它配套的几层

| 层 | 文件 / 技术 | 解决什么 |
|---|---|---|
| **准入** | `robots.txt` | AI 爬虫能不能抓 |
| **地图** | `sitemap.xml` | 站点有哪些页面 |
| **理解** | `llms.txt` | 站点是什么、什么重要 |
| **语义** | JSON-LD / schema.org | 页面里的实体与关系是什么 |
| **形态** | Markdown 双标记 | 给 AI 一份干净版本，给人一份完整版 |

**形态那一层值得多说一句**：有项目（如 dualmark）的做法是——**同一页 URL，通过 HTTP 内容协商，给 AI 返回 Markdown、给浏览器返回 HTML。** 这是把"机器可读"做成基础设施，而不是靠事后优化。

---

## 三、我们怎么看这一层

1. **它是"被引用"的技术前提，不是加分项。** 内容形态再好，如果模型读不到、读不懂，就谈不上被引用。
2. **它是一种公开约定。** 采用 llms.txt 不需要跟任何厂商签约，写文件即可——**这降低了"成为可信来源"的门槛**。
3. **但它只解决"读得到"。** 读得到之后，拼的是**内容本身对不对题、切不切得开**（见 [`research-index.md`](research-index.md) 第 4 组）。
4. **它和"署名"是两回事。** 让模型读懂你的站点，不等于模型引用时会署你的名——**那是规范与治理层的事**。

> 一句话：**技术层让人读得到，治理层让引用算你的，内容层让人愿意引。三层缺一不可。**
