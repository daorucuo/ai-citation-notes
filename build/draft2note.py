#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""草稿箱 md → 站点 notes 页。

用法: python3 build/draft2note.py
只处理这几件：h2/h3 / 引用块 / 表格 / 列表 / 段落 / **粗** / *斜* / ---
⛔ 不引第三方库。⛔ 不改已有页面，只新增 + 在 notes/index.html 顶部插入条目。
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DRAFT = Path("/Users/xuyuan/WorkBuddy/素材库/materials/草稿箱")

# slug, 源文件, 标题, 描述(命题), 分类标签
PAGES = [
    ("no-one-can-verify-the-ai-proofreader",
     "草稿_裁掉15个校对之后没人能证明AI校得对_20261110.md",
     "裁掉 15 个校对之后，没人能证明 AI 校得对",
     "Le Point 把校对从 18 人砍到 3 人，理由是 AI 能顶。可替 AI 验收的人，也一起被裁掉了。误报会吵，漏报不吵。",
     "媒体 · Le Point"),
    ("side-effects-feel-like-efficacy",
     "草稿_让你觉得有效的最快办法是让它难受_20261110.md",
     "让人觉得一个药有效，最快的办法是让它有副作用",
     "古罗马医生拿粪便当药，理由恰恰是它恶心。两千年后一个双盲试验测出了这个机制：真药加一个让人口干的副作用，镇痛效果翻了三倍。",
     "人文 · 古罗马 / 安慰剂"),
    ("language-is-not-the-engine-of-thought",
     "草稿_语言不是思考的引擎_20261110.md",
     "语言不是思考的引擎，是一件可以拆的工具",
     "有的人几乎没有内心独白，照样能思考；而一旦允许他们把词念出声，成绩就和别人一样了。那「一句话说不出来」到底算什么问题？",
     "人文 · 认知"),
    ("leaderboard-noise-not-signal",
     "草稿_分差比误差还小的排行榜_20261112.md",
     "一个分差比误差还小的排行榜，排的是噪声的顺序",
     "SWE-bench Verified 前十名的差距小于测试自身的误差；ALE-Bench 换「中位人类」评分后前十全并列。多数「基准饱和」出在测量里，不在任务里。",
     "技术 · 评测效度"),
    ("local-facts-have-no-backup",
     "草稿_地方事实没有备份_20261111.md",
     "地方事实没有备份",
     "英国地方新闻社从近 200 家剩到 17 家。丢掉的不只是新闻 —— 新闻走了还能去别处看，「为什么」走了没有别处可看：官方记录记结果，记者记录记理由，而理由没有备份，AI 也补不上。",
     "媒体 · 编辑部内部"),
    ("the-0997-grader-never-read-the-reasoning",
     "草稿_那个拿了0997的评测从不读推理链_20261111.md",
     "那个拿了 0.997 的评测，从不读推理链",
     "一个从不读内容的打分器在多跳推理基准上拿到 AUC 0.997，单字符串匹配就赢过 11 个真实系统。它量的不是推理对不对，是文字像不像被编辑过。",
     "技术 · 评测效度"),
    ("masculinity-crisis-sells-rent-crisis-does-not",
     "草稿_男性气质危机好卖租金危机不好卖_20261110.md",
     "「男性气质危机」好卖，「租金危机」不好卖",
     "布克奖短名单小说《Black Bag》里，一个男人最狂野的幻想是有个像样的老板。把这些说成气质问题，正好帮了寡头。附一个能用的判据。",
     "人文 · 文学"),
]

DATE = "2026-11-12"

CSS = """
  :root{
    --ink:#16233a;      /* 墨蓝 · 正文 */
    --red:#8c1d18;      /* 暗红 · 唯一强调色，占比 <3% */
    --paper:#fbfaf7;    /* 纸白 */
    --faint:#8a8f98;    /* 次级文字 */
    --rule:#e5e2dc;     /* 分隔线 */
  }
  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{
    margin:0;
    background:var(--paper);
    color:var(--ink);
    font-family:"Songti SC","Source Han Serif SC","Noto Serif CJK SC",Georgia,serif;
    line-height:1.85;
    font-size:17px;
  }
  main{max-width:640px;margin:0 auto;padding:12vh 28px 12vh}
  .back{display:inline-block;color:var(--faint);font-size:14px;text-decoration:none;margin-bottom:40px}
  .back:hover{color:var(--red)}
  h1{font-size:27px;font-weight:600;letter-spacing:.02em;margin:0 0 10px;line-height:1.5}
  .date{color:var(--faint);font-size:14px;margin:0 0 10px}
  .src{color:var(--faint);font-size:13.5px;line-height:1.65;margin:0 0 44px}
  h2{
    font-size:15px;font-weight:600;letter-spacing:.12em;color:var(--faint);
    margin:52px 0 18px;
  }
  h3{font-size:18px;font-weight:600;margin:34px 0 14px}
  p{margin:0 0 18px}
  .lead{border-left:2px solid var(--red);padding:2px 0 2px 18px;margin:0 0 20px}
  .lead p{margin:0;font-size:18px}
  ul,ol{padding-left:22px;margin:0 0 18px}
  li{margin:0 0 8px}
  table{width:100%;border-collapse:collapse;margin:0 0 20px;font-size:15.5px}
  th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--rule);vertical-align:top}
  th{color:var(--faint);font-weight:600;font-size:14px;letter-spacing:.04em}
  tr:last-child td{border-bottom:1px solid var(--rule)}
  blockquote{margin:0 0 22px;padding:14px 18px;background:#f5f3ee;border-left:2px solid var(--red);font-size:16px}
  blockquote p{margin:0 0 10px}blockquote p:last-child{margin:0}
  code{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:.9em;background:#f2f0eb;padding:1px 5px;border-radius:3px}
  .note{background:#f5f3ee;border-left:2px solid var(--rule);padding:14px 18px;margin:0 0 20px;font-size:15.5px}
  .note p{margin:0 0 10px}
  .note p:last-child{margin:0}
  a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--rule)}
  a:hover{border-bottom-color:var(--red);color:var(--red)}
  strong{font-weight:600}
  hr{border:0;border-top:1px solid var(--rule);margin:40px 0}
  footer{margin-top:64px;padding-top:24px;border-top:1px solid var(--rule);color:var(--faint);font-size:14px}
  footer p{margin:0 0 6px}
  @media (max-width:600px){
    main{padding:8vh 20px 8vh}
    body{font-size:16px}
    table{font-size:14.5px}
    th,td{padding:8px 8px}
  }
"""


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+?)`", r"<code>\1</code>", s)
    return s


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def render(md):
    """md 正文（已剥掉 h1 与命题块）→ HTML"""
    out, i, lines = [], 0, md.split("\n")
    while i < len(lines):
        ln = lines[i].rstrip()
        s = ln.strip()
        if not s:
            i += 1
            continue
        # 表格
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            head = cells(s)
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i].strip()))
                i += 1
            out.append("<table>")
            out.append("<thead><tr>" + "".join(f"<th>{inline(h)}</th>" for h in head) + "</tr></thead>")
            out.append("<tbody>")
            for r in rows:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</tbody></table>")
            continue
        # 引用块
        if s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            inner = "".join(f"<p>{inline(b)}</p>" for b in buf if b)
            out.append(f"<blockquote>{inner}</blockquote>")
            continue
        # 分隔线
        if re.match(r"^-{3,}$", s):
            out.append("<hr>")
            i += 1
            continue
        # 标题
        m = re.match(r"^(#{2,4})\s+(.*)$", s)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue
        # 列表
        if re.match(r"^[-*]\s+", s) or re.match(r"^\d+\.\s+", s):
            ordered = bool(re.match(r"^\d+\.\s+", s))
            items = []
            while i < len(lines):
                t = lines[i].strip()
                if re.match(r"^[-*]\s+", t):
                    items.append(re.sub(r"^[-*]\s+", "", t)); i += 1
                elif re.match(r"^\d+\.\s+", t):
                    items.append(re.sub(r"^\d+\.\s+", "", t)); i += 1
                elif t and not re.match(r"^[#>|]|^-{3,}$", t) and items:
                    items[-1] += " " + t; i += 1
                else:
                    break
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        # 段落
        para = [s]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^[#>|\-*]|^\d+\.\s", lines[i].strip()):
            para.append(lines[i].strip()); i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


def build(slug, src, title, desc, tag):
    raw = (DRAFT / src).read_text(encoding="utf-8")
    lines = raw.split("\n")
    # 剥掉 h1
    body_start = 0
    for idx, l in enumerate(lines):
        if l.startswith("# "):
            body_start = idx + 1
            break
    rest = lines[body_start:]
    # 取命题块（**命题**：...）与 meta 行（*人文｜...*）
    lead, meta_used = None, ""
    keep = []
    for l in rest:
        s = l.strip()
        if lead is None and s.startswith("**命题**"):
            lead = s; continue
        if not meta_used and re.match(r"^\*[^*].*[|｜].*\*$", s):
            meta_used = re.sub(r"^\*|\*$", "", s); continue
        keep.append(l)
    body = render("\n".join(keep))

    src_line = re.sub(r"^[^｜|]*[｜|]\s*\d{4}-\d{2}-\d{2}\s*[｜|]\s*", "", meta_used).strip()
    src_html = f'<p class="src">{inline(src_line)}</p>' if src_line else ""

    lead_html = ""
    if lead:
        txt = re.sub(r"^\*\*命题\*\*[：:]\s*", "", lead)
        lead_html = f'<div class="lead"><p>{inline(txt)}</p></div>'

    # 结尾自疑块：把最后的 <p><em>1. ...</em></p> 收进 .note —— render 已处理，这里简单跳过

    url = f"https://xuyuanlab.com/notes/{slug}"
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": f"{url}#article",
                "headline": title,
                "description": desc,
                "datePublished": DATE,
                "dateModified": DATE,
                "inLanguage": "zh-CN",
                "author": {"@id": "https://xuyuanlab.com/#org"},
                "publisher": {"@id": "https://xuyuanlab.com/#org"},
                "mainEntityOfPage": url,
                "license": "https://creativecommons.org/licenses/by/4.0/",
            },
            {
                "@type": "FAQPage",
                "@id": f"{url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "这篇的一句话结论是什么？",
                        "acceptedAnswer": {"@type": "Answer", "text": desc},
                    }
                ],
            },
        ],
    }

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="联翩实验室">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:url" content="{url}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:site_name" content="联翩实验室">
<meta property="og:locale" content="zh_CN">
<meta property="og:image" content="https://xuyuanlab.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="https://xuyuanlab.com/og.png">
<style>{CSS}</style>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
</head>
<body>
<main>

  <a class="back" href="/">← 联翩实验室</a>

  <h1>{html.escape(title)}</h1>
  <p class="date">{DATE} · {html.escape(tag)}</p>

{lead_html}
{src_html}

{body}

  <footer>
    <a href="/llms.txt">llms.txt</a> · <a href="https://github.com/daorucuo">GitHub</a> · 本站文字内容 CC BY 4.0
  </footer>

</main>
<img src="/px.gif" alt="" width="1" height="1" style="position:absolute;opacity:0" loading="lazy">
</body>
</html>
"""
    out = SITE / "notes" / f"{slug}.html"
    out.write_text(doc, encoding="utf-8")
    return out, title, desc, tag, url


def insert_index(entries):
    """把新条目插到 notes/index.html 顶部。★ 幂等：已在页面里的 slug 跳过。"""
    p = SITE / "notes" / "index.html"
    s = p.read_text(encoding="utf-8")
    block = ""
    for slug, title, desc, tag in entries:
        if f'href="/notes/{slug}"' in s:
            continue
        block += f"""  <a class="entry" href="/notes/{slug}">
    <p class="date">{DATE} · {html.escape(tag)}</p>
    <p class="title">{html.escape(title)}</p>
    <p class="desc">{html.escape(desc)}</p>
  </a>

"""
    if block:
        anchor = s.index('<a class="entry"')
        s = s[:anchor] + block + s[anchor:]
        p.write_text(s, encoding="utf-8")
    return p


def update_sitemap(entries):
    p = SITE / "sitemap.xml"
    s = p.read_text(encoding="utf-8")
    add = ""
    for slug, *_ in entries:
        u = f"https://xuyuanlab.com/notes/{slug}"
        if u in s:
            continue
        add += f"  <url><loc>{u}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n"
    if add:
        s = s.replace("</urlset>", add + "</urlset>")
        p.write_text(s, encoding="utf-8")
    return p


def main():
    built = []
    for slug, src, title, desc, tag in PAGES:
        path, t, d, g, u = build(slug, src, title, desc, tag)
        built.append((slug, t, d, g, u))
        print(f"  ✅ {path.relative_to(ROOT)}")
    insert_index([(b[0], b[1], b[2], b[3]) for b in built])
    import subprocess
    subprocess.run([sys.executable, str(ROOT / "build" / "notes_build.py")], check=True)
    print("  ✅ site/notes/index.html 顶部插入 4 条")
    update_sitemap(built)
    print("  ✅ site/sitemap.xml")


if __name__ == "__main__":
    main()
