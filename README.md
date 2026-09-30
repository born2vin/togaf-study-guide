# TOGAF Explained: 25-Day Study Guide

A 25-day study programme for the **TOGAF Standard, 10th Edition** (Foundation and Practitioner). Each day has an explainer-style lesson and a 20-minute interactive mock test with scoring and detailed reasoning for every option.

**Live site:** https://born2vin.github.io/togaf-study-guide/

| Day | Topic | Page |
|---|---|---|
| 1 | Introduction to TOGAF | [Open](TOGAF_Day1_Introduction.html) |
| 2 | Core Terminology | [Open](TOGAF_Day2_Core_Terminology.html) |
| 3 | Preliminary Phase and Architecture Principles | [Open](TOGAF_Day3_Preliminary_Phase.html) |
| 4 | Phase A: Architecture Vision | [Open](TOGAF_Day4_Architecture_Vision.html) |
| 5 | Phase B: Business Architecture | Coming soon |
| 6 | Phase C: Data Architecture | Coming soon |
| 7 | Phase C: Application Architecture | Coming soon |
| 8 | Phase D: Technology Architecture | Coming soon |
| 9 | Phase E: Opportunities & Solutions | Coming soon |
| 10 | Phase F: Migration Planning | Coming soon |
| 11 | Phase G: Implementation Governance | Coming soon |
| 12 | Phase H and Requirements Management | Coming soon |
| 13 | Checkpoint: Full ADM Review Test | Coming soon |
| 14 | Applying the ADM | Coming soon |
| 15 | ADM Techniques I | Coming soon |
| 16 | ADM Techniques II | Coming soon |
| 17 | Architecture Content Framework and Metamodel | Coming soon |
| 18 | Deliverables, Artifacts, ABBs and SBBs in Depth | Coming soon |
| 19 | Enterprise Continuum and Architecture Repository | Coming soon |
| 20 | Architecture Governance and Compliance | Coming soon |
| 21 | Architecture Capability Framework | Coming soon |
| 22 | Series Guides and Reference Models | Coming soon |
| 23 | Practitioner Scenarios I (Phases A–D) | Coming soon |
| 24 | Practitioner Scenarios II (Phases E–H) | Coming soon |
| 25 | Final Mock Exam | Coming soon |

## How the site is built

Every page shares one template, so the design stays identical across all days.

- `template/style.css` and `template/quiz.js`: the shared design and quiz engine
- `content/dayN.html` and `content/dayN.questions.js`: each day's lesson and questions
- `build.py`: generates the self-contained day pages, `index.html` and this README

To add a day, write its two content files, register it in `DAYS` in `build.py`, then run `python3 build.py`.

*Unofficial study material. TOGAF is a registered trademark of The Open Group.*
