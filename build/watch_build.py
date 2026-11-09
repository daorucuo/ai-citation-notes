#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""观察 · 构建器
内容:  content/watch/<YYYY-MM-DD>.md      人写（front-matter ＋ 条目）
读数:  自动从 收割机/3_报告/收割机日常报告_<YYYYMMDD>_*.json 取，⛔ 不手抄、⛔ 不编数
产出:  site/watch/<YYYY-MM-DD>.html
       并重写 site/watch/index.html 与 site/index.html 里 <!-- OBS:... --> 标记之间那一段
用法:
    python3 build/watch_build.py 2026-11-08
    python3 build/watch_build.py --all
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "watch"
SITE = ROOT / "site"
HARVEST = Path("/Users/xuyuan/WorkBuddy/素材库/materials/收割机/3_报告")
LIMIT_INDEX = 20   # 观察栏上限（版面容量，不是数量目标）

# ---------- 读数：只从收割机报告取，取不到就写"未取" ----------
def readings(date):
    ymd = date.replace("-", "")
    cands = sorted(HARVEST.glob(f"收割机日常报告_{ymd}_*.json"))
    r = {"scan": None, "new": None, "rate": None, "sources": None, "atoms": None}
    if cands:
        try:
            d = json.loads(cands[0].read_text(encoding="utf-8"))
            nn = (d.get("fetch") or {}).get("newsnow") or {}
            r["scan"] = nn.get("total"); r["new"] = nn.get("new")
            r["rate"] = nn.get("rate");  r["sources"] = nn.get("sources")
            r["atoms"] = (d.get("store") or {}).get("atoms")
        except Exception as e:
            print(f"  ⚠️ 读数解析失败：{e}")
    return r

def readings_html(r):
    bits = []
    if r["scan"] is not None:
        bits.append(f'今日扫 <b>{r["scan"]}</b> 条')
        if r["new"] is not None:
            bits.append(f'新增 {r["new"]}（{r["rate"]}）')
    if r["sources"]:
        bits.append(html.escape(r["sources"]))
    if r["atoms"] is not None:
        bits.append(f'立住 <b>{r["atoms"]}</b> 条原子')
    return " ／ ".join(bits) if bits else "读数未取"

# ---------- 内容解析 ----------
def parse(path):
    raw = path.read_text(encoding="utf-8")
    head, _, body = raw.partition("\n## ")
    meta = {}
    for ln in head.splitlines():
        m = re.match(r"^(\S+):\s*(.*)$", ln.strip())
        if m: meta[m.group(1)] = m.group(2).strip()
    blocks = []
    for chunk in ("## " + body).split("\n## "):
        chunk = chunk.strip()
        if not chunk: continue
        title_line, _, rest = chunk.partition("\n")
        title_line = re.sub(r"^#{1,6}\s*", "", title_line.strip())
        m = re.match(r"^【(.+?)】(.+)$", title_line)
        tag, verdict = (m.group(1), m.group(2).strip()) if m else (None, title_line.strip())
        blocks.append({"tag": tag, "verdict": verdict, "body": rest.strip()})
    return meta, blocks

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"(https?://[^\s<）)]+)", r'<a href="\1">\1</a>', s)
    return s

BEATS = [("· 发生了什么", "· 发生了什么"), ("· 这意味着什么", "· 这意味着什么"), ("· 所以要关注什么", "· 所以要关注什么")]

def render_block(b):
    if b["tag"] is None:            # 「今天没搞懂的」
        out = [f'<div class="unknown">', f'<h2>{inline(b["verdict"])}</h2>']
        for para in re.split(r"\n\s*\n", b["body"]):
            para = para.strip()
            if not para: continue
            if para.startswith("来源："):
                out.append(f'<p class="src">{inline(para)}</p>'); continue
            if para.startswith("- "):
                out.append("<ul>" + "".join(f"<li>{inline(x[2:].strip())}</li>"
                           for x in para.splitlines() if x.strip().startswith("- ")) + "</ul>")
            else:
                out.append(f"<p>{inline(para)}</p>")
        out.append("</div>")
        return "\n".join(out)
    out = ['<div class="item">',
           f'<p class="verdict"><span class="tag">{inline(b["tag"])}</span>{inline(b["verdict"])}</p>']
    for para in re.split(r"\n\s*\n", b["body"]):
        para = para.strip()
        if not para: continue
        if para.startswith("来源："):
            out.append(f'<p class="src">{inline(para)}</p>'); continue
        m = re.match(r"^(· [^：]+：)(.*)$", para, re.S)
        if m:
            out.append(f'<p class="beat"><span class="lbl">{m.group(1)}</span>{inline(m.group(2).strip())}</p>')
        else:
            out.append(f"<p>{inline(para)}</p>")
    out.append("</div>")
    return "\n".join(out)

CSS = open(ROOT / "build" / "watch.css", encoding="utf-8").read()

def build(date):
    src = CONTENT / f"{date}.md"
    if not src.exists():
        print(f"❌ 缺内容件：{src}"); return None
    meta, blocks = parse(src)
    no = meta.get("期号", "?")
    tags = meta.get("标签", "")
    summary = meta.get("摘要", "")
    r = readings(date)
    items = [b for b in blocks if b["tag"]]
    unknowns = [b for b in blocks if b["tag"] is None]
    body = "\n".join(render_block(b) for b in items + unknowns)
    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>观察 No.{no} · {date} · 联翩实验室</title>
<meta name="description" content="{html.escape(summary or items[0]['verdict'] if items else '')}">
<meta name="author" content="联翩实验室">
<link rel="canonical" href="https://xuyuanlab.com/watch/{date}">
<meta property="og:type" content="article">
<meta property="og:title" content="观察 No.{no} · {date}">
<meta property="og:url" content="https://xuyuanlab.com/watch/{date}">
<style>{CSS}</style>
<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"Article",
  "@id":"https://xuyuanlab.com/watch/{date}#article",
  "headline":"观察 No.{no}：{items[0]['verdict'] if items else ''}",
  "description":"{html.escape(summary)}",
  "datePublished":"{date}","dateModified":"{date}","inLanguage":"zh-CN",
  "isPartOf":{{"@id":"https://xuyuanlab.com/watch/#collection"}},
  "author":{{"@id":"https://xuyuanlab.com/#person"}},
  "publisher":{{"@id":"https://xuyuanlab.com/#person"}},
  "mainEntityOfPage":"https://xuyuanlab.com/watch/{date}",
  "license":"https://creativecommons.org/licenses/by/4.0/"
}}
</script>
</head>
<body>
<main>
  <a class="back" href="/watch/">← 观察 · 各期</a>
  <div class="masthead"><span class="no">观 察　No.{no}</span></div>
  <p class="meta">
    <b>{date}</b>　｜　<b>{len(items)}</b> 条　｜　标签：<b>{html.escape(tags)}</b><br>
    {readings_html(r)}
  </p>
  <h1>本期{len(items)}条</h1>
{body}
  <div class="colophon">
    <p><strong>这个栏目怎么运作</strong><br>
    每天扫公开源，挑 3–5 条值得重点看的，一条一条单独写，不做配对。<br>
    每条三段：发生了什么 ／ 这意味着什么 ／ 所以要关注什么。<strong>缺一段就不发。</strong><br>
    收料标准：〔双源〕〔有数〕〔第一次〕〔冲突〕〔落位〕。<br>
    来源分层：〔一手·英文〕〔一手·中文〕〔二手〕—— <strong>只有中文二手源的料，本期不选。</strong><br>
    语言：<strong>不设分站</strong>，中文为主；哪条的一手是英文、英文更准，就直接用英文写。</p>
    <p style="margin-top:14px"><a href="/watch/">全部各期</a>　｜　<a href="/">首页</a>　｜　<a href="/llms.txt">llms.txt</a></p>
    <p style="margin-top:14px">{date} · 联翩实验室 · 本站文字内容 CC BY 4.0</p>
  </div>
</main>
</body>
</html>
"""
    out = SITE / "watch" / f"{date}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"✅ {out.relative_to(ROOT)}  （{len(items)} 条 ＋ {len(unknowns)} 条没搞懂的）｜读数：{readings_html(r)[:60]}")
    return {"date": date, "no": int(no) if str(no).isdigit() else 0,
            "lead": items[0]["verdict"] if items else "", "tags": tags,
            "summary": summary, "n": len(items)}

# ---------- 重写两处列表（标记之间） ----------
def replace_region(path, marker, new_html):
    p = SITE / path
    t = p.read_text(encoding="utf-8")
    pat = re.compile(rf"(<!-- OBS:{marker}:START -->).*?(<!-- OBS:{marker}:END -->)", re.S)
    if not pat.search(t):
        print(f"  ⚠️ {path} 缺标记 OBS:{marker}，跳过"); return
    t = pat.sub(lambda m: m.group(1) + "\n" + new_html + "\n" + m.group(2), t)
    p.write_text(t, encoding="utf-8")
    print(f"  ↻ {path} （OBS:{marker}）")

def collect():
    rows = []
    for f in sorted(CONTENT.glob("*.md")):
        meta, blocks = parse(f)
        items = [b for b in blocks if b["tag"]]
        rows.append({"date": f.stem, "no": int(meta.get("期号", 0)),
                     "lead": items[0]["verdict"] if items else "", "n": len(items),
                     "tags": meta.get("标签", ""), "summary": meta.get("摘要", "")})
    return sorted(rows, key=lambda r: r["date"], reverse=True)[:LIMIT_INDEX]

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--all":
        for f in sorted(CONTENT.glob("*.md")):
            build(f.stem)
    else:
        for d in args: build(d)
    rows = collect()
    if rows:
        w = rows[0]
        lead = f"""      <a class="lead-item" href="/watch/{w['date']}">
        <p class="lm">No.{w['no']} · {w['date']} · {w['n']} 条</p>
        <p class="lt">{html.escape(w['lead'])}</p>
        <p class="ld">{html.escape(w['summary'])}</p>
      </a>"""
        rest = "\n".join(
            f'        <li><a href="/watch/{r["date"]}"><span class="od">No.{r["no"]} · {r["date"]} · {r["n"]} 条</span>'
            f'<span class="ot">{html.escape(r["lead"])}</span></a></li>' for r in rows[1:])
        replace_region("index.html", "HOME", lead + "\n\n      <ul class=\"olist\">\n" + rest + "\n      </ul>")
        wl = "\n".join(
            f"""  <a class="entry" href="/watch/{r['date']}">
    <p class="date">No.{r['no']} · {r['date']} · {r['n']} 条</p>
    <p class="title">{html.escape(r['lead'])}</p>
    <p class="desc">{html.escape(r['summary'])}</p>
  </a>
""" for r in rows)
        replace_region("watch/index.html", "LIST", wl)
    print(f"\n共 {len(list(CONTENT.glob('*.md')))} 期；列表上限 {LIMIT_INDEX}")
