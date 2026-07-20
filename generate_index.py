#!/usr/bin/env python3
"""
Generates index.html for a GitHub Pages repo full of dated HTML dashboards.

Usage:
    python3 generate_index.py [repo_dir]

Expects HTML files named YYYY-MM-DD.html (or YYYY-MM-DD-<label>.html) in repo_dir.
Writes/overwrites repo_dir/index.html with links to every file, newest first.
Anything not matching the date pattern is ignored (so index.html, README, .git etc.
are automatically skipped).
"""

import re
import sys
from pathlib import Path
from datetime import datetime

DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-(.+))?\.html$")

def main():
    repo_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    if not repo_dir.is_dir():
        print(f"Not a directory: {repo_dir}", file=sys.stderr)
        sys.exit(1)

    entries = []
    for f in repo_dir.glob("*.html"):
        if f.name == "index.html":
            continue
        m = DATE_RE.match(f.name)
        if not m:
            continue
        date_str, label = m.group(1), m.group(2)
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue
        entries.append((d, date_str, label, f.name))

    entries.sort(key=lambda e: e[0], reverse=True)

    rows = []
    for d, date_str, label, fname in entries:
        display = d.strftime("%A, %B %-d %Y") if hasattr(d, "strftime") else date_str
        title = f"{display}" + (f" — {label}" if label else "")
        rows.append(
            f'      <li><a href="{fname}">{title}</a></li>'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Daily Dashboards</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          max-width: 640px; margin: 40px auto; padding: 0 20px; color: #1a1a1a; }}
  h1 {{ font-size: 1.4rem; margin-bottom: 4px; }}
  p.meta {{ color: #666; font-size: 0.85rem; margin-top: 0; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
  a {{ text-decoration: none; color: #0645ad; font-size: 1rem; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
  <h1>Daily Dashboards</h1>
  <p class="meta">{len(entries)} entries · updated {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
  <ul>
{chr(10).join(rows) if rows else "    <li>No dashboards yet.</li>"}
  </ul>
</body>
</html>
"""
    out = repo_dir / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out} with {len(entries)} entries")

if __name__ == "__main__":
    main()
