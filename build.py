#!/usr/bin/env python3
"""Build the TOGAF study site from content/ + template/.

Every day's page uses the same template, so the look stays identical across
all 25 days. To add a day:
  1. write content/dayN.html            (lesson HTML: h2 sections with ids,
                                           cards, tables; end with an
                                           <h2 id="summary">The takeaway</h2> card)
  2. write content/dayN.questions.js    (a JS array of {q, o, a, r} objects)
  3. give that day a "file" and "dek" in DAYS below
  4. run:  python3 build.py
It regenerates every day page, index.html and README.md.
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).parent
SITE = "TOGAF Explained"
TOTAL = 25

DAYS = [
    # (day, section, title, file-or-None, dek-or-None)
    (1, "Foundation", "Introduction to TOGAF", "TOGAF_Day1_Introduction.html",
     "Foundation concepts, the four architecture domains, the ADM, and the structure of the Standard"),
    (2, "Foundation", "Core Terminology", "TOGAF_Day2_Core_Terminology.html",
     "Stakeholders and concerns, views and viewpoints, deliverables, artifacts, building blocks, and architecture states"),
    (3, "Foundation", "Preliminary Phase and Architecture Principles", "TOGAF_Day3_Preliminary_Phase.html",
     "Preparing the organization for EA, tailoring TOGAF, and defining good Architecture Principles"),
    (4, "Foundation", "Phase A: Architecture Vision", "TOGAF_Day4_Architecture_Vision.html",
     "Starting an ADM cycle: scope, stakeholders, the Architecture Vision and the Statement of Architecture Work"),
    (5, "Foundation", "Phase B: Business Architecture", None, None),
    (6, "Foundation", "Phase C: Data Architecture", None, None),
    (7, "Foundation", "Phase C: Application Architecture", None, None),
    (8, "Foundation", "Phase D: Technology Architecture", None, None),
    (9, "Foundation", "Phase E: Opportunities & Solutions", None, None),
    (10, "Foundation", "Phase F: Migration Planning", None, None),
    (11, "Foundation", "Phase G: Implementation Governance", None, None),
    (12, "Foundation", "Phase H and Requirements Management", None, None),
    (13, "Foundation", "Checkpoint: Full ADM Review Test", None, None),
    (14, "Foundation", "Applying the ADM", None, None),
    (15, "Foundation", "ADM Techniques I", None, None),
    (16, "Foundation", "ADM Techniques II", None, None),
    (17, "Foundation", "Architecture Content Framework and Metamodel", None, None),
    (18, "Foundation", "Deliverables, Artifacts, ABBs and SBBs in Depth", None, None),
    (19, "Foundation", "Enterprise Continuum and Architecture Repository", None, None),
    (20, "Foundation", "Architecture Governance and Compliance", None, None),
    (21, "Foundation", "Architecture Capability Framework", None, None),
    (22, "Foundation", "Series Guides and Reference Models", None, None),
    (23, "Practitioner & Final Exam", "Practitioner Scenarios I (Phases A–D)", None, None),
    (24, "Practitioner & Final Exam", "Practitioner Scenarios II (Phases E–H)", None, None),
    (25, "Practitioner & Final Exam", "Final Mock Exam", None, None),
]

CSS = (ROOT / "template/style.css").read_text()
QUIZ_JS = (ROOT / "template/quiz.js").read_text()
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900'
         '&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,700;1,8..60,400&display=swap" rel="stylesheet">')


def shell(title, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{FONTS}
<style>
{CSS}
</style>
</head>
<body>
<div class="masthead"><div class="in">
  <a class="brand" href="index.html">TOGAF<span>.</span>Explained</a>
  <a class="sect" href="index.html">All 25 days</a>
</div></div>
{body}
<footer class="site"><div class="in">Unofficial study material for the TOGAF Standard, 10th Edition. TOGAF is a registered trademark of The Open Group.</div></footer>
</body>
</html>
"""


def number_sections(body):
    """'<h2 id="x">3. Title</h2>' -> numbered kicker + title; collect TOC."""
    toc = []
    def repl(m):
        hid, text = m.group(1), m.group(2)
        n = re.match(r"(\d+)\.\s*(.*)", text)
        if n:
            num, label = n.group(1), n.group(2)
            toc.append((hid, re.sub("<.*?>", "", label)))
            return f'<h2 id="{hid}"><span class="num">{int(num):02d}</span>{label}</h2>'
        toc.append((hid, re.sub("<.*?>", "", text)))
        return m.group(0)
    return re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', repl, body), toc


def build_day(i, published):
    n, section, title, file, dek = published[i]
    body = (ROOT / f"content/day{n}.html").read_text()
    questions = (ROOT / f"content/day{n}.questions.js").read_text().strip().rstrip(";")
    body, toc = number_sections(body)
    toc.append(("quiz", "Mock test"))
    words = len(re.sub("<.*?>", " ", body).split())
    mins = max(3, round(words / 230))
    nq = questions.count("\n  { q:") or questions.count("{ q:")

    toc_items = "".join(f'<li><a href="#{h}">{html.escape(t)}</a></li>' for h, t in toc)
    prev_link = next_link = ""
    if i > 0:
        p = published[i - 1]
        prev_link = f'<a class="prev" href="{p[3]}"><small>← Day {p[0]}</small><span>{html.escape(p[2])}</span></a>'
    if i < len(published) - 1:
        x = published[i + 1]
        next_link = f'<a class="next" href="{x[3]}"><small>Day {x[0]} →</small><span>{html.escape(x[2])}</span></a>'

    page = f"""
<header class="hero">
  <div class="kicker">Day {n} of {TOTAL} · {html.escape(section)}</div>
  <h1>{html.escape(title)}</h1>
  <p class="dek">{dek}</p>
  <div class="byline"><span><b>{SITE}</b></span><span>About {mins} min read</span><span>{nq}-question mock test</span><span>TOGAF Standard, 10th Edition</span></div>
  <div class="progress" aria-label="Course progress"><i style="width:{n / TOTAL * 100:.0f}%"></i></div>
</header>
<div class="layout">
  <aside class="toc">
    <details open><summary style="list-style:none"><h4>In this explainer</h4></summary>
    <ol>{toc_items}</ol></details>
  </aside>
  <article>
{body}
    <section class="quiz-head" id="quiz">
      <div class="kicker">Test yourself</div>
      <h2>Day {n} mock test</h2>
      <p>{nq} questions in 20 minutes. Start the timer, pick your answers, then submit to see your score and the reasoning for every option.</p>
    </section>
    <div class="controls sticky">
      <button id="startBtn">Start 20-min timer</button>
      <span id="timer">20:00</span>
    </div>
    <div id="questions"></div>
    <div class="controls">
      <button id="submitBtn">Submit &amp; show reasoning</button>
      <button class="secondary" id="resetBtn">Reset</button>
      <span id="score"></span>
    </div>
    <nav class="pager">{prev_link}{next_link}</nav>
  </article>
</div>
<script>if (window.innerWidth < 980) document.querySelector(".toc details").removeAttribute("open");</script>
<script>
const QUESTIONS = {questions};
{QUIZ_JS}
</script>"""
    (ROOT / file).write_text(shell(f"Day {n}: {title} · {SITE}", page))
    return file


def build_index(published_count):
    sections = {}
    for d in DAYS:
        sections.setdefault(d[1], []).append(d)
    parts = []
    for name, items in sections.items():
        tiles = []
        for n, _, title, file, dek in items:
            if file:
                tiles.append(f'<a class="tile" href="{file}"><div class="n">Day {n}</div>'
                             f'<div class="t">{html.escape(title)}</div><div class="d">{dek}</div></a>')
            else:
                tiles.append(f'<div class="tile soon"><div class="n">Day {n}</div><div class="t">{html.escape(title)}</div></div>')
        parts.append(f'<h2>{html.escape(name)}</h2><div class="grid">{"".join(tiles)}</div>')
    body = f"""
<header class="hero">
  <div class="kicker">A 25-day explainer series</div>
  <h1>Everything you need to pass TOGAF, one day at a time</h1>
  <p class="dek">Each day explains one part of the TOGAF Standard, 10th Edition, then tests you with a 20-minute mock exam and the reasoning behind every answer.</p>
  <div class="byline"><span><b>{SITE}</b></span><span>{published_count} of {TOTAL} days published</span><span>Foundation and Practitioner</span></div>
  <div class="progress"><i style="width:{published_count / TOTAL * 100:.0f}%"></i></div>
</header>
<main class="series">{"".join(parts)}</main>"""
    (ROOT / "index.html").write_text(shell(f"{SITE}: 25-Day TOGAF Study Guide", body))


def build_readme():
    rows = "\n".join(
        f"| {n} | {title} | " + (f"[Open]({file})" if file else "Coming soon") + " |"
        for n, _, title, file, _ in DAYS)
    (ROOT / "README.md").write_text(f"""# TOGAF Explained: 25-Day Study Guide

A 25-day study programme for the **TOGAF Standard, 10th Edition** (Foundation and Practitioner). Each day has an explainer-style lesson and a 20-minute interactive mock test with scoring and detailed reasoning for every option.

**Live site:** https://born2vin.github.io/togaf-study-guide/

| Day | Topic | Page |
|---|---|---|
{rows}

## How the site is built

Every page shares one template, so the design stays identical across all days.

- `template/style.css` and `template/quiz.js`: the shared design and quiz engine
- `content/dayN.html` and `content/dayN.questions.js`: each day's lesson and questions
- `build.py`: generates the self-contained day pages, `index.html` and this README

To add a day, write its two content files, register it in `DAYS` in `build.py`, then run `python3 build.py`.

*Unofficial study material. TOGAF is a registered trademark of The Open Group.*
""")


if __name__ == "__main__":
    published = [d for d in DAYS if d[3]]
    for i in range(len(published)):
        print("built", build_day(i, published))
    build_index(len(published))
    build_readme()
    print("built index.html, README.md")
