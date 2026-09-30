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
    (5, "Foundation", "Phase B: Business Architecture", "TOGAF_Day5_Business_Architecture.html",
     "How the enterprise needs to operate: capabilities, value streams, the common steps of Phases B–D, and gap analysis"),
    (6, "Foundation", "Phase C: Data Architecture", "TOGAF_Day6_Data_Architecture.html",
     "Logical and physical data assets, data management, migration and governance, and the key Data Architecture artifacts"),
    (7, "Foundation", "Phase C: Application Architecture", "TOGAF_Day7_Application_Architecture.html",
     "The applications the enterprise needs, how they interact, the III-RM, and the key Application Architecture artifacts"),
    (8, "Foundation", "Phase D: Technology Architecture", "TOGAF_Day8_Technology_Architecture.html",
     "Platforms and infrastructure, the Technical Reference Model, key technology considerations and artifacts"),
    (9, "Foundation", "Phase E: Opportunities & Solutions", "TOGAF_Day9_Opportunities_Solutions.html",
     "The first implementation phase: consolidating gaps, work packages, Transition Architectures and the initial roadmap"),
    (10, "Foundation", "Phase F: Migration Planning", "TOGAF_Day10_Migration_Planning.html",
     "Finalizing the roadmap and migration plan: business value, prioritization and the four management frameworks"),
    (11, "Foundation", "Phase G: Implementation Governance", "TOGAF_Day11_Implementation_Governance.html",
     "Architectural oversight of implementation: Architecture Contracts, compliance levels and dispensations"),
    (12, "Foundation", "Phase H and Requirements Management", "TOGAF_Day12_Change_and_Requirements_Management.html",
     "Managing change after implementation, the three classes of change, and Requirements Management at the centre of the ADM"),
    (13, "Foundation", "Checkpoint: Full ADM Review Test", "TOGAF_Day13_ADM_Checkpoint.html",
     "The whole ADM on one page, where every deliverable is created and finalized, the top exam traps, and a 20-question checkpoint test"),
    (14, "Foundation", "Applying the ADM", None, None),
    (15, "Foundation", "ADM Techniques I", None, None),
    (16, "Foundation", "ADM Techniques II", None, None),
    (17, "Foundation", "Architecture Content Framework and Metamodel", None, None),
    (18, "Foundation", "Deliverables, Artifacts, ABBs and SBBs in Depth", None, None),
    (19, "Foundation", "Enterprise Continuum and Architecture Repository", None, None),
    (20, "Foundation", "Architecture Governance and Compliance", None, None),
    (21, "Foundation", "Architecture Capability Framework", None, None),
    (22, "Foundation", "Series Guides and Reference Models", None, None),
    (23, "Practitioner & Mock Exams", "Practitioner Scenarios I (Phases A–D)", None, None),
    (24, "Practitioner & Mock Exams", "Practitioner Scenarios II (Phases E–H)", None, None),
    (25, "Practitioner & Mock Exams", "Final Mock Exam", None, None),
]

PRACTICE = "Practitioner & Mock Exams"   # index section the mock exams appear in

EXAMS = [
    # (number, level label, title, file, dek)
    (1, "Level 1 · Warm-up", "Part 1 Mock Exam 1: Warm-up", "TOGAF_Part1_Mock_Exam_1_Warmup.html",
     "40 direct questions on the core definitions and facts. Build confidence and find the gaps before the harder papers."),
    (2, "Level 2 · Exam standard", "Part 1 Mock Exam 2: Exam Standard", "TOGAF_Part1_Mock_Exam_2_Standard.html",
     "40 questions pitched at the real Foundation exam, with the same close distractors and topic mix."),
    (3, "Level 3 · Challenging", "Part 1 Mock Exam 3: Challenging", "TOGAF_Part1_Mock_Exam_3_Challenging.html",
     "40 harder questions: \"which is NOT\", near-identical options and applied scenarios. Pass this and you are ready."),
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


def build_exam(i):
    n, level, title, file, dek = EXAMS[i]
    intro = (ROOT / f"content/exam{n}.html").read_text()
    questions = (ROOT / f"content/exam{n}.questions.js").read_text().strip().rstrip(";")
    nq = len(re.findall(r"\bq:\s*\"", questions))
    intro, toc = number_sections(intro)
    toc.append(("quiz", "Start the exam"))
    toc_items = "".join(f'<li><a href="#{h}">{html.escape(t)}</a></li>' for h, t in toc)
    prev_link = next_link = ""
    if i > 0:
        p = EXAMS[i - 1]
        prev_link = f'<a class="prev" href="{p[3]}"><small>← Mock Exam {p[0]}</small><span>{html.escape(p[1])}</span></a>'
    if i < len(EXAMS) - 1:
        x = EXAMS[i + 1]
        next_link = f'<a class="next" href="{x[3]}"><small>Mock Exam {x[0]} →</small><span>{html.escape(x[1])}</span></a>'
    page = f"""
<header class="hero">
  <div class="kicker">Mock Exam {n} of {len(EXAMS)} · TOGAF EA Foundation (Part 1)</div>
  <h1>{html.escape(title)}</h1>
  <p class="dek">{dek}</p>
  <span class="level">{html.escape(level)}</span>
  <div class="byline"><span><b>{SITE}</b></span><span>{nq} questions</span><span>60 minutes</span><span>Pass mark 60%</span><span>TOGAF Standard, 10th Edition</span></div>
</header>
<div class="layout">
  <aside class="toc">
    <details open><summary style="list-style:none"><h4>In this exam</h4></summary>
    <ol>{toc_items}</ol></details>
  </aside>
  <article>
    <div class="facts">
      <div><b>{nq}</b><span>questions</span></div>
      <div><b>60</b><span>minutes</span></div>
      <div><b>24</b><span>correct to pass (60%)</span></div>
      <div><b>1</b><span>correct answer each</span></div>
    </div>
{intro}
    <section class="quiz-head" id="quiz">
      <div class="kicker">Exam conditions</div>
      <h2>Start Mock Exam {n}</h2>
      <p>Closed book, {nq} questions, 60 minutes. Start the timer, answer every question, then submit to see your score, a breakdown by topic, and the reasoning for every option.</p>
    </section>
    <div class="controls sticky">
      <button id="startBtn">Start 60-min timer</button>
      <span id="answered"></span>
      <span id="timer">60:00</span>
    </div>
    <div id="questions"></div>
    <div class="controls">
      <button id="submitBtn">Submit exam</button>
      <button class="secondary" id="resetBtn">Reset</button>
      <span id="score"></span>
    </div>
    <div id="breakdown" hidden></div>
    <nav class="pager">{prev_link}{next_link}</nav>
  </article>
</div>
<script>if (window.innerWidth < 980) document.querySelector(".toc details").removeAttribute("open");</script>
<script>
window.QUIZ_MINUTES = 60;
const QUESTIONS = {questions};
{QUIZ_JS}
</script>"""
    (ROOT / file).write_text(shell(f"{title} · {SITE}", page))
    return file


def build_index(published_count):
    sections = {}
    for d in DAYS:
        sections.setdefault(d[1], []).append(d)
    parts = []
    for name, items in sections.items():
        tiles = []
        if name == PRACTICE:
            for en, level, etitle, efile, edek in EXAMS:
                if (ROOT / f"content/exam{en}.questions.js").exists():
                    tiles.append(f'<a class="tile" href="{efile}"><div class="n">Mock Exam {en} · Part 1</div>'
                                 f'<div class="t">{html.escape(etitle.split(": ", 1)[1])}</div><div class="d">{edek}</div>'
                                 f'<div class="lvl">{html.escape(level)} · 40 questions · 60 min</div></a>')
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
    exam_rows = "\n".join(f"- [{title}]({file}) ({level})" for _, level, title, file, _ in EXAMS
                          if (ROOT / file).exists())
    (ROOT / "README.md").write_text(f"""# TOGAF Explained: 25-Day Study Guide

A 25-day study programme for the **TOGAF Standard, 10th Edition** (Foundation and Practitioner). Each day has an explainer-style lesson and a 20-minute interactive mock test with scoring and detailed reasoning for every option.

**Live site:** https://born2vin.github.io/togaf-study-guide/

| Day | Topic | Page |
|---|---|---|
{rows}

## Part 1 (Foundation) mock exams

Three full-length mock exams in the real exam format: 40 questions, 60 minutes, 60% to pass.

{exam_rows}

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
    for i, e in enumerate(EXAMS):
        if (ROOT / f"content/exam{e[0]}.questions.js").exists():
            print("built", build_exam(i))
    build_index(len(published))
    build_readme()
    print("built index.html, README.md")
