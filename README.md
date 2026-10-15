# TOGAF Explained: 25-Day Study Guide

A 25-day study programme for the **TOGAF Standard, 10th Edition** (Foundation and Practitioner). Each day has an explainer-style lesson and an interactive timed test with scoring and detailed reasoning for every option. Days 23–25 use Part 2 (Practitioner) scenario questions with 5/3/1/0 gradient scoring.

**Live site:** https://born2vin.github.io/togaf-study-guide/

| Day | Topic | Page |
|---|---|---|
| 1 | Introduction to TOGAF | [Open](TOGAF_Day1_Introduction.html) |
| 2 | Core Terminology | [Open](TOGAF_Day2_Core_Terminology.html) |
| 3 | Preliminary Phase and Architecture Principles | [Open](TOGAF_Day3_Preliminary_Phase.html) |
| 4 | Phase A: Architecture Vision | [Open](TOGAF_Day4_Architecture_Vision.html) |
| 5 | Phase B: Business Architecture | [Open](TOGAF_Day5_Business_Architecture.html) |
| 6 | Phase C: Data Architecture | [Open](TOGAF_Day6_Data_Architecture.html) |
| 7 | Phase C: Application Architecture | [Open](TOGAF_Day7_Application_Architecture.html) |
| 8 | Phase D: Technology Architecture | [Open](TOGAF_Day8_Technology_Architecture.html) |
| 9 | Phase E: Opportunities & Solutions | [Open](TOGAF_Day9_Opportunities_Solutions.html) |
| 10 | Phase F: Migration Planning | [Open](TOGAF_Day10_Migration_Planning.html) |
| 11 | Phase G: Implementation Governance | [Open](TOGAF_Day11_Implementation_Governance.html) |
| 12 | Phase H and Requirements Management | [Open](TOGAF_Day12_Change_and_Requirements_Management.html) |
| 13 | Checkpoint: Full ADM Review Test | [Open](TOGAF_Day13_ADM_Checkpoint.html) |
| 14 | Applying the ADM | [Open](TOGAF_Day14_Applying_the_ADM.html) |
| 15 | ADM Techniques I | [Open](TOGAF_Day15_ADM_Techniques_I.html) |
| 16 | ADM Techniques II | [Open](TOGAF_Day16_ADM_Techniques_II.html) |
| 17 | Architecture Content Framework and Metamodel | [Open](TOGAF_Day17_Content_Framework_Metamodel.html) |
| 18 | Deliverables, Artifacts, ABBs and SBBs in Depth | [Open](TOGAF_Day18_Deliverables_and_Building_Blocks.html) |
| 19 | Enterprise Continuum and Architecture Repository | [Open](TOGAF_Day19_Enterprise_Continuum_Repository.html) |
| 20 | Architecture Governance and Compliance | [Open](TOGAF_Day20_Governance_and_Compliance.html) |
| 21 | Architecture Capability Framework | [Open](TOGAF_Day21_Architecture_Capability.html) |
| 22 | Series Guides and Reference Models | [Open](TOGAF_Day22_Series_Guides_Reference_Models.html) |
| 23 | Practitioner Scenarios I (Phases A–D) | [Open](TOGAF_Day23_Practitioner_Scenarios_A_to_D.html) |
| 24 | Practitioner Scenarios II (Phases E–H) | [Open](TOGAF_Day24_Practitioner_Scenarios_E_to_H.html) |
| 25 | Final Mock Exam | [Open](TOGAF_Day25_Final_Mock_Exam.html) |

## Part 1 (Foundation) mock exams

Three full-length mock exams in the real exam format: 40 questions, 60 minutes, 60% to pass.

- [Part 1 Mock Exam 1: Warm-up](TOGAF_Part1_Mock_Exam_1_Warmup.html) (Level 1 · Warm-up)
- [Part 1 Mock Exam 2: Exam Standard](TOGAF_Part1_Mock_Exam_2_Standard.html) (Level 2 · Exam standard)
- [Part 1 Mock Exam 3: Challenging](TOGAF_Part1_Mock_Exam_3_Challenging.html) (Level 3 · Challenging)

## How the site is built

Every page shares one template, so the design stays identical across all days.

- `template/style.css` and `template/quiz.js`: the shared design and quiz engine
- `content/dayN.html` and `content/dayN.questions.js`: each day's lesson and questions
- `build.py`: generates the self-contained day pages, `index.html` and this README

To add a day, write its two content files, register it in `DAYS` in `build.py`, then run `python3 build.py`.

*Unofficial study material. TOGAF is a registered trademark of The Open Group.*
