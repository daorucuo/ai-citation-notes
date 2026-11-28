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
    r = {"scan": None, "new": None, "rate": None, "sources": None, "atoms": None, "stored": None}
    if cands:
        try:
            d = json.loads(cands[0].read_text(encoding="utf-8"))
            # 收割机报告有两种键名（英文 2026-11-08 版 / 中文 2026-11-09 起），两种都要认
            fetch = d.get("fetch") or d.get("源") or {}
            store = d.get("store") or d.get("存段") or {}
            nn = fetch.get("newsnow") or {}
            r["scan"] = nn.get("total", nn.get("抓回"))
            r["new"]  = nn.get("new",   nn.get("新增"))
            rate = nn.get("rate", nn.get("新增率"))
            if isinstance(rate, float): rate = f"{rate*100:.1f}%"
            r["rate"] = rate
            r["sources"] = nn.get("sources", nn.get("子源"))
            r["atoms"] = store.get("atoms", store.get("原子"))
            # ★ 2026-11-15 补：报告 schema 又换了一版 —— NewsNow 那组数搬进了 `逐源.NewsNow`
            #   （抓回／新增／新增率／成功／失败／暂停），原来只认 `fetch.newsnow` ⇒ 11-15 起
            #   读数恒为「未取」，而数据其实在报告里。**只映射真实字段，⛔ 一个数都不编。**
            #   ⚠️ 不把 `料仓.今日条目`(60) 塞进 atoms —— 那是**条目**不是**原子**（今天原子 6 条），
            #      塞进去会印成「立住 60 条原子」，是假数。
            # ★★ 2026-11-25 修：`逐源.NewsNow.抓回` 不是「今日扫」——
            #   它只是 NewsNow 一路的抓回，而且 11-24 与 11-25 **两天都是 534**（同一个数），
            #   拿它当全天扫描量会在页面上印出一个假的「今日扫」。
            #   唯一能对得上料仓实物的是 `料仓.今日条目`（11-24=445、11-25=801，与 `料仓/原始.jsonl` 实点一致）。
            # ★★ 2026-11-28 修：收割机把字段名从 `今日条目` 改成了 `今日条数`
            #   （11-27 报告是「今日条目」=532；11-28 报告是「今日条数」=180）⇒ 只认前者就取空，
            #   页面掉进兜底分支，印出「今日扫 524」——那其实是**线索批**，不是入仓量。
            #   同一类坑第二次（11-25 那次是 `逐源.NewsNow.抓回`）：**字段名一变，读数就静默变假。**
            _lk = d.get("料仓") or {}
            r["stored"] = _lk.get("今日条目") or _lk.get("今日条数")
            if r["scan"] is None:
                nn2 = ((d.get("逐源") or {}).get("NewsNow") or {})
                r["scan"] = nn2.get("抓回")
                r["new"] = nn2.get("新增")
                r["rate"] = nn2.get("新增率")
                ok, bad, pause = nn2.get("成功"), nn2.get("失败"), nn2.get("暂停")
                if ok is not None:
                    r["sources"] = f"{ok} 通 / {bad} 失败 / {pause} 暂停"
        except Exception as e:
            print(f"  ⚠️ 读数解析失败：{e}")
    return r

def readings_html(r):
    bits = []
    # ⛔ 2026-11-25：`scan` 那组数不可信（见 readings() 里的说明），**能对账的只有落仓**
    if r.get("stored") is not None:
        bits.append(f'今日落仓 <b>{r["stored"]}</b> 条')
    elif r["scan"] is not None:
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
    if b["tag"] is None and "可引用" in b["verdict"]:
        out = ['<div class="citable">', f'<h2>{inline(b["verdict"])}</h2>',
               '<p class="cn">下面每一句都能脱离上下文单独成立，带日期与出处，供直接引用。</p>', "<ul>"]
        for ln in b["body"].splitlines():
            ln = ln.strip()
            if ln.startswith("- "):
                out.append(f"<li>{inline(ln[2:].strip())}</li>")
        out.append("</ul></div>")
        return "\n".join(out)
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
           f'<h2 class="verdict"><span class="tag">{inline(b["tag"])}</span>{inline(b["verdict"])}</h2>']
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

CSS = open(ROOT / "build" / "watch.css", encoding="utf-8").read() + """
  .citable{border-top:2px solid var(--ink);margin-top:44px;padding-top:22px}
  .citable h2{font-size:16px;letter-spacing:.1em;color:var(--red);margin:0 0 8px}
  .citable .cn{color:var(--faint);font-size:13.5px;margin:0 0 14px}
  .citable ul{padding-left:20px;margin:0}
  .citable li{margin:0 0 10px;font-size:15.5px;line-height:1.75}
"""

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
    # 页面主标题：优先用 front-matter 的摘要（一句话说清这期讲什么），缺了退回首条判词
    headline = summary or (items[0]["verdict"] if items else f"观察 No.{no}")
    body = "\n".join(render_block(b) for b in items + unknowns)
    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>观察 No.{no} · {date} · 联翩实验室</title>
<meta name="description" content="{html.escape(summary)}">
<meta name="author" content="联翩实验室">
<link rel="canonical" href="https://xuyuanlab.com/watch/{date}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(headline)}">
<meta property="og:url" content="https://xuyuanlab.com/watch/{date}">
<meta property="og:description" content="{html.escape(summary)}">
<meta property="og:site_name" content="联翩实验室">
<meta property="og:locale" content="zh_CN">
<meta property="og:image" content="https://xuyuanlab.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(headline)}">
<meta name="twitter:description" content="{html.escape(summary)}">
<meta name="twitter:image" content="https://xuyuanlab.com/og.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>{CSS}</style>
<script type="application/ld+json">
{{
  "@context":"https://schema.org","@graph":[
  {{"@type":"Article",
  "@id":"https://xuyuanlab.com/watch/{date}#article",
  "headline":"{html.escape(headline)}",
  "description":"{html.escape(summary)}",
  "datePublished":"{date}","dateModified":"{date}","inLanguage":"zh-CN",
  "isPartOf":{{"@id":"https://xuyuanlab.com/watch/#collection"}},
  "author":{{"@id":"https://xuyuanlab.com/#org"}},
  "publisher":{{"@id":"https://xuyuanlab.com/#org"}},
  "mainEntityOfPage":"https://xuyuanlab.com/watch/{date}",
  "license":"https://creativecommons.org/licenses/by/4.0/"
}},
  {{"@type":"Organization",
  "@id":"https://xuyuanlab.com/#org","name":"联翩实验室","url":"https://xuyuanlab.com/",
  "logo":{{"@type":"ImageObject","url":"https://xuyuanlab.com/apple-touch-icon.png"}}
}},
  {{"@type":"BreadcrumbList",
  "itemListElement":[
    {{"@type":"ListItem","position":1,"name":"联翩实验室","item":"https://xuyuanlab.com/"}},
    {{"@type":"ListItem","position":2,"name":"观察","item":"https://xuyuanlab.com/watch/"}},
    {{"@type":"ListItem","position":3,"name":"No.{no} · {date}","item":"https://xuyuanlab.com/watch/{date}"}}
  ]}}
  ]
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
  <p class="kicker">本期 {len(items)} 条</p>
  <h1>{html.escape(headline)}</h1>
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
    # ★ 2026-11-15 修：页脚「本期用到的数与出处」没有主标签，会被当成一条「没搞懂的」，
    #   于是构建日志印出"2 没搞懂的"而正文只有 1 条 —— **报了个假数**。
    #   渲染保持原样（与 11-13 一致，`.unknown` 只是条分隔线），这里只把**计数**算对。
    FOOTER = "本期用到的数与出处"
    真未知 = [b for b in unknowns if b["verdict"] != FOOTER]
    n_cit = sum(1 for b in 真未知 if "可引用" in b["verdict"]); n_unk = len(真未知) - n_cit
    print(f"✅ {out.relative_to(ROOT)}  （{len(items)} 条 ＋ {n_unk} 没搞懂的 ＋ {n_cit} 可引用）｜读数：{readings_html(r)[:60]}")
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
        if f.name.startswith("_") or f.name.lower() == "readme.md":
            continue
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
            if f.name.startswith("_") or f.name.lower() == "readme.md":
                continue
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
    n_real = len([f for f in CONTENT.glob("*.md") if not f.name.startswith("_") and f.name.lower() != "readme.md"])
    print(f"\n共 {n_real} 期；列表上限 {LIMIT_INDEX}")
