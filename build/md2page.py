#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""仓库根目录的 .md 索引 → 站点 HTML 页。
用法: python3 build/md2page.py            # 生成 site/index/{research,tools,standards}.html
只处理这四件：标题 / 引用块 / 表格 / 列表 / 段落。⛔ 不引第三方库。
"""
import html, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "index"
CSS = """
  :root{--ink:#16233a;--red:#8c1d18;--paper:#fbfaf7;--faint:#8a8f98;--rule:#e5e2dc;}
  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{margin:0;background:var(--paper);color:var(--ink);
    font-family:"Songti SC","Source Han Serif SC","Noto Serif CJK SC",Georgia,serif;line-height:1.8;font-size:16.5px}
  main{max-width:760px;margin:0 auto;padding:10vh 28px 12vh}
  .back{display:inline-block;color:var(--faint);font-size:14px;text-decoration:none;margin-bottom:34px}
  .back:hover{color:var(--red)}
  h1{font-size:28px;font-weight:600;margin:0 0 10px;line-height:1.45}
  h2{font-size:16px;font-weight:600;letter-spacing:.1em;color:var(--faint);margin:46px 0 14px;
     padding-bottom:8px;border-bottom:1px solid var(--rule);text-transform:uppercase}
  h3{font-size:17.5px;font-weight:600;margin:30px 0 12px}
  p{margin:0 0 16px}
  blockquote{margin:0 0 22px;padding:12px 18px;background:#f5f3ee;border-left:2px solid var(--red);
    color:#3d4a5c;font-size:15.5px}
  blockquote p{margin:0 0 8px}blockquote p:last-child{margin:0}
  table{width:100%;border-collapse:collapse;margin:0 0 24px;font-size:14.5px}
  th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
  th{color:var(--faint);font-weight:600;font-size:13px;letter-spacing:.04em}
  ul,ol{padding-left:22px;margin:0 0 18px}li{margin:0 0 7px}
  code{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:.88em;background:#f2f0eb;padding:1px 5px;border-radius:3px}
  a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--rule)}
  a:hover{color:var(--red);border-bottom-color:var(--red)}
  strong{font-weight:600}
  hr{border:0;border-top:1px solid var(--rule);margin:34px 0}
  footer{margin-top:60px;padding-top:22px;border-top:1px solid var(--rule);color:var(--faint);font-size:13.5px}
  footer p{margin:0 0 6px}
  @media (max-width:600px){main{padding:8vh 18px}table{font-size:13.5px}th,td{padding:7px 6px}}
"""

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"(?<![=\"'])(https?://[^\s<）)]+)", r'<a href="\1">\1</a>', s)
    return s

def convert(md):
    out, i, lines = [], 0, md.split("\n")
    while i < len(lines):
        ln = lines[i]
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip(">").strip()); i += 1
            out.append("<blockquote>" + "".join(f"<p>{inline(x)}</p>" for x in buf if x) + "</blockquote>")
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            if len(rows) >= 2 and set("".join(rows[1])) <= set("-: "):
                head, body = rows[0], rows[2:]
            else:
                head, body = None, rows
            t = ["<table>"]
            if head:
                t.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr>")
            for r in body:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</table>")
            out.append("".join(t)); continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            lvl = len(m.group(1)); txt = m.group(2)
            tag = "h1" if lvl == 1 else ("h2" if lvl == 2 else ("h3" if lvl == 3 else "h4"))
            if tag in ("h1", "h2", "h3", "h4"):
                pass
            out.append(f"<{tag}>{inline(txt)}</{tag}>"); i += 1; continue
        if re.match(r"^-{3,}$", ln.strip()):
            out.append("<hr>"); i += 1; continue
        if re.match(r"^[-*]\s+", ln):
            buf = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                buf.append(re.sub(r"^[-*]\s+", "", lines[i])); i += 1
            out.append("<ul>" + "".join(f"<li>{inline(b)}</li>" for b in buf) + "</ul>"); continue
        if re.match(r"^\d+\.\s+", ln):
            buf = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                buf.append(re.sub(r"^\d+\.\s+", "", lines[i])); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(b)}</li>" for b in buf) + "</ol>"); continue
        if not ln.strip():
            i += 1; continue
        out.append(f"<p>{inline(ln.strip())}</p>"); i += 1
    return "\n".join(out)

PAGES = [
    ("research", "research-index.md", "研究索引",
     "GEO / AEO / AI Search 领域的 54 篇公开研究（2023–2026）：按八个问题分组的精选，加按十个主题的完整清单。"),
    ("tools", "tool-ecosystem.md", "工具生态",
     "30+ 个开源项目与平台：端到端 GEO、Agent Skill / MCP、内容就绪度与结构化、研究配套、出版基础设施。"),
    ("standards", "standards.md", "技术标准与 AI 可读性",
     "llms.txt、结构化标记，以及让内容被机器读懂的那一层。"),
]

def shell(slug, title, desc, body):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · 联翩实验室</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="联翩实验室">
<link rel="canonical" href="https://xuyuanlab.com/index/{slug}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)} · 联翩实验室">
<meta property="og:url" content="https://xuyuanlab.com/index/{slug}">
<style>{CSS}</style>
</head>
<body>
<main>
  <a class="back" href="/index/">← 索引</a>
{body}
  <footer>
    <p>编目只做指向：题名、出处、链接。⛔ 不转载原文。</p>
    <p><a href="/">首页</a> · <a href="/watch/">观察</a> · <a href="https://github.com/daorucuo/ai-citation-notes">GitHub</a> · 本站文字内容 CC BY 4.0</p>
    <p style="margin-top:10px">联翩实验室 · 由 <code>build/md2page.py</code> 从仓库根目录的 <code>{{md}}</code> 生成</p>
  </footer>
</main>
</body>
</html>
"""

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, src, title, desc in PAGES:
        md = (ROOT / src).read_text(encoding="utf-8")
        body = convert(md)
        page = shell(slug, title, desc, body).replace("{md}", src)
        (OUT / f"{slug}.html").write_text(page, encoding="utf-8")
        print(f"✅ site/index/{slug}.html  ← {src}  ({len(md.splitlines())} 行 md)")
