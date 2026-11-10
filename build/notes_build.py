#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""首页「实践」栏 ← site/notes/index.html 最新 N 篇。

起因：2026-11-10 发了四篇稿，首页一个字没动 —— 因为那三个 <li> 是写死的。
      观察栏有 OBS:HOME 标记位会自动重排，实践栏没有，于是新稿只出现在 /notes/ 里。

用法: python3 build/notes_build.py      # 重排 site/index.html 里 NOTES:PRACTICE 之间那一段
⛔ 不引第三方库。⛔ 不动「思考」栏（那一栏是人工挑的一句话，不是列表）。
"""
import html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
LIMIT = 6          # 右栏容量，不是数量目标
START = "<!-- NOTES:PRACTICE:START -->"
END = "<!-- NOTES:PRACTICE:END -->"


def entries():
    """从 notes/index.html 抓条目（新→旧，页面顺序就是时间顺序）"""
    s = (SITE / "notes" / "index.html").read_text(encoding="utf-8")
    out = []
    for m in re.finditer(
        r'<a class="entry" href="/notes/([^"]+)">\s*'
        r'<p class="date">(.*?)</p>\s*'
        r'<p class="title">(.*?)</p>',
        s, re.S,
    ):
        slug, date, title = m.group(1), m.group(2).strip(), m.group(3).strip()
        # date 形如「2026-11-10 · 媒体 · Le Point」→ 取项目/标签部分
        parts = [x.strip() for x in date.split("·", 1)]
        tag = parts[1] if len(parts) > 1 else ""
        proj = tag.split("·")[0].strip() or "笔记"
        out.append((slug, proj, title))
    return out


def build():
    items = entries()[:LIMIT]
    if not items:
        print("⚠️ notes/index.html 里没抓到条目，不动首页")
        return
    rows = "".join(
        f'''          <li><a href="/notes/{slug}">
            <span class="proj">{html.escape(proj)}</span>
            <span class="rt">{html.escape(title)}</span>
          </a></li>\n'''
        for slug, proj, title in items
    )
    block = f'{START}\n        <ul class="rlist">\n{rows}        </ul>\n        {END}'
    p = SITE / "index.html"
    s = p.read_text(encoding="utf-8")
    if START not in s or END not in s:
        raise SystemExit("🔴 首页缺 NOTES:PRACTICE 标记位，拒绝静默跳过")
    s = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, s, flags=re.S)
    p.write_text(s, encoding="utf-8")
    print(f"  ↻ index.html（NOTES:PRACTICE）{len(items)} 条：")
    for slug, proj, title in items:
        print(f"      {proj:8s} {title[:38]}")


if __name__ == "__main__":
    build()
