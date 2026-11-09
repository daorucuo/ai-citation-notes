#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""盖日期：把「最后更新」统一改成今天（或指定日期）。
为什么有它：这三处以前全靠手改，已在 2026-11-08 之前漏过三次。
用法: python3 build/stamp.py [YYYY-MM-DD]     默认今天
"""
import datetime, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()

TARGETS = [
    ("site/index.html",  r"最后更新 \d{4}-\d{2}-\d{2}",                  f"最后更新 {DATE}"),
    ("site/llms.txt",    r"\*最后更新：\d{4}-\d{2}-\d{2}\*",             f"*最后更新：{DATE}*"),
    ("sources.md",       r"\*最后更新：\d{4}-\d{2}(-\d{2})?\*",          f"*最后更新：{DATE}*"),
    ("site/watch/index.html", r"最后更新 \d{4}-\d{2}-\d{2}",             f"最后更新 {DATE}"),
    ("site/about.html",  r"最后更新 \d{4}-\d{2}-\d{2}",                  f"最后更新 {DATE}"),
]

if __name__ == "__main__":
    for rel, pat, rep in TARGETS:
        p = ROOT / rel
        if not p.exists():
            print(f"  ⏭ {rel} 不存在"); continue
        t = p.read_text(encoding="utf-8")
        new, n = re.subn(pat, rep, t)
        if n:
            p.write_text(new, encoding="utf-8")
            print(f"  ✅ {rel} → {DATE}（{n} 处）")
        else:
            print(f"  ⚠️ {rel} 未匹配到日期")
