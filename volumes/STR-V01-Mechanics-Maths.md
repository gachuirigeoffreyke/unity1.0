# STR-V01 · Engineering Mechanics & Maths Rebuild
### STRUCTURES — Structural Design Mastery Playbook · Phase 1: Foundations Rebuild

| Field | Value |
|---|---|
| Volume | **V01 — Engineering Mechanics & Maths Rebuild** |
| Phase | 1 · Foundations Rebuild |
| Version / date | v1.1 · 2026-10-29 (schedule re-dated: W01 now starts Mon 2 Nov 2026). v1.0 · 2026-10-03 (research and link checks: 2026-10-03, unchanged) |
| Prerequisites | STR-V00 v1.3 approved; Week 1 setup done (toolkit, V00 diagnostic D01–D12) |
| Hour budget | **70 h**, weeks W02–W09 (9 Nov 2026 – 3 Jan 2027), plus REV-01 in the light week W06 |
| Tracker items | `V01.M01` … `V01.M10` (one tracker item per module, same IDs and hours) |
| Code basis | Mostly code-neutral mechanics. Where material constants or buckling rules appear, EN (KS EN, 1st generation) is primary and BS is given in full alongside it (V00 §5(b)) |

> **Conventions.** `[R-xxxx]` resolves in Appendix B. **(judgement)** = professional judgement. `[VERIFY]` = not confirmed from a live source on 2026-10-03. Worked examples are for learning only; real designs need independent checking by a registered engineer. No code text or tables are reproduced: clause numbers only.

## Contents
0. [How to use this volume](#0-how-to-use-this-volume)
1. [Week-by-week plan (W02–W09)](#1-week-by-week-plan-w02w09)
2. [Shared resources for V01](#2-shared-resources-for-v01)
3. [Modules V01.M01–V01.M10](#3-modules)
4. [V01 end test](#4-v01-end-test)
5. [Trends Watch](#5-trends-watch)
6. [Answer key](#6-answer-key)
7. [Appendix A — Formula sheet you build yourself](#appendix-a--formula-sheet-you-build-yourself)
8. [Appendix B — Resource index (V01)](#appendix-b--resource-index-v01)
9. [Appendix C — Handoff block](#appendix-c--handoff-block)

---

## 0. How to use this volume

### 0.1 Pick your pathway from the W01 diagnostic

| Diagnostic score (V00.D01–D12) | Pathway | What changes |
|---|---|---|
| **10–12** | **Fast track** | For M01–M05: skip the reading, do the quiz first. If you score ≥80%, do only the worked problem and the software verification, then mark the module done. If you score below 80%, run the standard path for that module. Expected saving: up to ~20 h, which goes to the tracker as buffer (don't delete hours; mark the module done early). |
| **6–9** | **Standard** | Follow the core path in each module as written. |
| **0–5** | **Standard + drills** | Standard path, plus one extra problem set per module from the shared resources (+~1 h per module, taken from light-week buffer W06). |

Whatever the pathway, M06–M10 run in full: they carry the stress, deflection and buckling ideas that every later volume depends on.

### 0.2 How a module is built

Every module follows the V00 §8 template: outcomes → code coverage → core path (read, watch, do, with times) → worked problem with full solution → "Your turn" variant (solution in §6) → software verification → thread tasks → quiz → field notes → portfolio output → "Done when".

### 0.3 Sign conventions and units used throughout

- **SI units with structural multiples**: kN, m, kNm for forces and moments; N/mm² (= MPa) for stress; mm for section dimensions and deflections. State units on every line of a calculation.
- **Global axes**: x along the member or horizontal, y vertical (up positive), z out of the page (right-hand rule). Anticlockwise moments positive in equilibrium equations.
- **Beam internal forces**: sagging moment positive (tension at the bottom); shear positive when it tends to rotate a segment clockwise. Software often uses the opposite sign. Every verification exercise flags this.
- **Truss members**: tension positive, compression negative.

### 0.4 Logging in the tracker

Each module is one tracker item. Log hours honestly and rate **% complete by work remaining, not hours spent**. A module reaches 100% only when its "Done when" box is fully ticked (V00 §11.1). Log quiz scores as `V01.Q03` and so on, and verification records as `VER-V01.M03`.

---

## 1. Week-by-week plan (W02–W09)

R = read · W = watch · D = do (problems, code) · T = test · threads T1 AutoCAD, T3 Python, T4 EBK portfolio, T5 field. Hours match the tracker baseline (STR-V00 §12.2).

| Week | Dates | Module(s) and hours | Tasks (h) | Σh | Output |
|---|---|---|---|---:|---|
| **W02** | 9–15 Nov | M01 (6) · M02 (4 of 8) | M01: R 2.0 · W 0.75 · D 1.75 · T 0.5 · T3 1.0 — M02: R 1.5 · W 1.0 · T1 1.0 · D 0.5 | 10 | WP01.1 solved; `strlib.units` with tests; layer standard in DWT |
| **W03** | 16–22 Nov | M02 (4) · M03 (6 of 8) | M02: D 2.0 · verification 0.5 · T 0.5 · R 1.0 — M03: R 2.0 · W 1.0 · D 2.0 · T3 1.0 | 10 | WP02.1 + anaStruct check; truss hand calcs; joint-method solver started |
| **W04** | 23–29 Nov | M03 (2) · M04 (8) | M03: D 0.5 · verification 0.5 · T 0.5 · T1 0.5 — M04: R 2.5 · W 0.5 · D 2.5 · verification 0.5 · T 0.5 · T3 1.0 · T5 0.5 | 10 | Truss GA drawing; section-property function verified against `sectionproperties` |
| **W05** | 30 Nov–6 Dec | M05 (8) · M06 (2 of 6) | M05: R 2.0 · W 1.0 · D 2.5 · verification 0.5 · T 0.5 · T3 1.0 · T4 0.5 — M06: R 2.0 | 10 | SFD/BMD plotter; **GE application submitted** |
| **W06** | 7–13 Dec | **Light week — REV-01** | Retrieval set on M01–M05 (§6, REV-01) 3 · error-log fixes 2 · buffer 3 | 8 | REV-01 score logged |
| **W07** | 14–20 Dec | M06 (4) · M07 (6 of 8) | M06: R 0.5 · D 1.5 · verification 0.5 · T 0.5 · T1 1.0 — M07: W 2.0 · R 1.0 · D 2.0 · T3 1.0 | 10 | Rod/column calcs; Mohr's-circle function |
| **W08** | 21–27 Dec | M07 (2) · M08 (8) | M07: D 1.0 · verification 0.5 · T 0.5 — M08: W 2.0 · R 1.0 · D 2.5 · verification 1.0 · T 0.5 · T3 1.0 | 10 | Macaulay deflection verified against PyNite |
| **W09** | 28 Dec–3 Jan | M09 (5) · M10 (5) | M09: W 1.0 · R 0.5 · D 1.5 · verification 0.5 · T 0.5 · end test 1.0 — M10: W 0.75 · R 1.25 · D 1.5 · verification 0.5 · T 0.5 · end test 0.5 | 10 | **V01 end test ≥70%**; **IEK Graduate application in** |

Ask for V02 by W07, i.e. by 14 Dec 2026 (the tracker milestone is anchored to V02.M01's forecast start).

**Holiday note (judgement).** W08 (21–27 Dec) and W09 (28 Dec–3 Jan) cover Christmas and New Year. If you'll be away or busy, mark those weeks off (or light) in the tracker's Calendar tab: M07–M10 and the end test then move later in the forecast, and the baseline stays put. Don't squeeze the end test into a holiday week.

---

## 2. Shared resources for V01

These are the volume's backbone. Each module names the exact parts to use. All are free unless marked.

| ID | Resource | Type · cost | Code basis | Why it's in |
|---|---|---|---|---|
| R-0101 | Baker & Haynes, *Engineering Statics: Open and Interactive* (2020), engineeringstatics.org | Open textbook (CC BY-NC-SA), interactive web + PDF · **Free** | Code-neutral | Free, open-source statics text covering vectors, forces, moments, equilibrium and properties of shapes, written for the first engineering mechanics course. Its ten chapters run from forces and vectors through equilibrium of structures, centroids, internal loadings and moments of inertia, which maps one-to-one onto M01–M05. Interactive figures with checked answers suit self-study `[R-0101]` |
| R-0102 | NPTEL, *Strength of Materials*, Prof. S. K. Bhattacharyya, IIT Kharagpur (course 105105108) | Video course · **Free** to enrol and learn (paid exam certificate optional) | Code-neutral (some Indian Standard references → concepts only) | Taught in a civil engineering department by a structural engineer; course is free to enrol and learn from `[R-0102]`. Core video spine for M06–M09 |
| R-0103 | NPTEL, *Engineering Mechanics*, Prof. K. Ramesh, IIT Madras (nptel.ac.in/courses/112106286) | Video course · **Free** | Code-neutral | Listed as the prerequisite course for IIT Madras's Strength of Materials `[R-0103]`. Use selectively in M02–M03 |
| R-0104 | MIT OpenCourseWare, *2.001 Mechanics & Materials I* (Fall 2006) | Lecture notes + 11 problem sets · **Free** | Code-neutral (US units in places) | Lecture notes and eleven problem sets as PDFs, with a downloadable offline package `[R-0104]`. Tier A practice problems for M06–M09. Solutions are not listed on the assignments page, so self-check with software |
| R-0105 | 3Blue1Brown, *Essence of linear algebra* (YouTube / 3blue1brown.com) | Video series · **Free** | Maths | Short visual lessons (about 15 min each) on vectors, linear transformations, determinants, inverse matrices, dot and cross products and eigenvectors `[R-0105]`. Builds the geometric intuition the stiffness method rests on (M01, M10). Tier B, chosen because nothing in Tier A teaches the geometry as fast |
| R-0106 | Kong, Siauw & Bayen, *Python Programming and Numerical Methods* (Elsevier, 2020) | Book; free online edition `[VERIFY URL]`; print/eBook paid | Maths / code | Chapters cover linear systems, eigenvalues, root finding, numerical differentiation and integration, all with Jupyter code `[R-0106]`. One of the authors trained as a structural engineer. Used in M10 |
| R-0107 | `anaStruct` 1.7.0, `PyNiteFEA` 3.2.0, `sectionproperties` 3.10.2, `handcalcs` 1.11.0 (PyPI) | Python libraries · **Free** | Code-neutral | The "stated tools" for software verification in V01 (V00 §5(f)). Versions confirmed on PyPI 2026-10-02 `[R-0030 in V00]` |
| R-0108 | Calcpad (calcpad.eu) | Calculation software · **Free** | Code-neutral | Readable calc sheets; used for one presented calc per module from M04 on `[R-0025 in V00]` |
| R-0109 | *Optional, paid:* Hibbeler, *Mechanics of Materials* (any recent SI edition) **or** Gere & Goodno, *Mechanics of Materials* (SI) | Textbook · price `[VERIFY]` | Code-neutral | The reference text MIT used alongside 2.001 was Hibbeler `[R-0110]`. Buy (used is fine) only if you want a single bound reference with many solved problems; R-0102 + R-0104 cover the same ground for free |

**Not used, and why:** NPTEL *design* courses (Indian Standard basis, `[IS — concepts only]`) are left for later volumes; US-code content is avoided where an EN/BS-neutral equivalent exists.

---

## 3. Modules

## [V01.M01] Units, vectors and free-body diagrams
**Tags:** Phase 1 | Mechanics (code-neutral) | T1, T3
**Prerequisites:** V00 diagnostic taken
**Time:** 6 h (W02)

**Learning outcomes**
1. Convert between mass, weight, pressure and line load units without error (kg → kN, kPa → kN/m on a member).
2. Resolve forces into components and add them as vectors in 2D and 3D.
3. Compute the moment of a force about a point with $\mathbf{M} = \mathbf{r} \times \mathbf{F}$, and about an axis.
4. Draw a complete free-body diagram (FBD) of a structure or part, showing every external force and support reaction with assumed directions.

**Code coverage:** units and densities only. EN 1991-1-1 Annex A (nominal densities of construction materials) ↔ BS 648 (schedule of weights of building materials; status `[VERIFY]`). Clause numbers only; values are used, not reproduced.

**Core path**

| Step | Resource and exact part | Time |
|---|---|---:|
| Read | R-0101 ch. 1 (Introduction to Statics) and ch. 2 (Forces and Other Vectors), including the interactive checks | 2.0 h |
| Watch | R-0105 chapters 1–3 (vectors; linear combinations; linear transformations) | 0.75 h |
| Do | WP01.1 below, its "Your turn", and 8 problems from R-0101 ch. 2 | 1.75 h |
| Test | V01.Q01 | 0.5 h |
| Thread | T3: `strlib.units` (below) | 1.0 h |

**Supplementary:** R-0101 ch. 4.1–4.3 (moments) if the cross product is rusty.

### Worked problem V01.WP01.1 — Base actions on a PV-table post

**Situation.** A single steel post carries a small ground-mounted PV table. Take the post base as the origin, x horizontal downwind, y horizontal across, z vertically up.
- Wind: a net pressure of 0.65 kN/m² on 6.5 m² of panel area gives a horizontal force acting at 2.5 m above the base. (V03 shows how to derive wind loads properly; here it's given.)
- Self-weight of modules, rails and post: 3.0 kN, acting 1.2 m above the base and 150 mm downwind of the post axis.

**Find** the resultant force on the post and the moment at its base.

**Design basis and assumptions.** (A1) Forces are static and act at the stated points. (A2) The post is a rigid body for this calculation. (A3) Learning example only; no partial factors applied.

**Solution**

Wind force: $F_w = 0.65\ \text{kN/m}^2 \times 6.5\ \text{m}^2 = 4.225 \approx 4.2\ \text{kN}$, so $\mathbf{F}_1 = (4.2,\ 0,\ 0)$ kN at $\mathbf{r}_1 = (0,\ 0,\ 2.5)$ m.
Self-weight: $\mathbf{F}_2 = (0,\ 0,\ -3.0)$ kN at $\mathbf{r}_2 = (0.15,\ 0,\ 1.2)$ m.

Resultant force:
$$\mathbf{R} = \mathbf{F}_1 + \mathbf{F}_2 = (4.2,\ 0,\ -3.0)\ \text{kN}, \qquad |\mathbf{R}| = \sqrt{4.2^2 + 3.0^2} = 5.16\ \text{kN}$$
acting at $\tan^{-1}(3.0/4.2) = 35.5^\circ$ below the horizontal.

Moment about the base:
$$\mathbf{r}_1 \times \mathbf{F}_1 = (0,\ 0,\ 2.5) \times (4.2,\ 0,\ 0) = (0,\ 10.50,\ 0)\ \text{kNm}$$
$$\mathbf{r}_2 \times \mathbf{F}_2 = (0.15,\ 0,\ 1.2) \times (0,\ 0,\ -3.0) = (0,\ 0.45,\ 0)\ \text{kNm}$$
$$\mathbf{M}_{base} = (0,\ 10.95,\ 0)\ \text{kNm}$$

**Checks.** Units kN × m = kNm ✓. Direction: both moments act about +y, so the eccentric self-weight adds to the wind overturning moment, which it would not if the panel sat upwind ✓. Scalar check: 4.2 × 2.5 + 3.0 × 0.15 = 10.95 ✓.

**What this tells an engineer.** The foundation or ground screw must resist ≈11 kNm of overturning plus the 4.2 kN shear. Self-weight is small, so this post is wind-governed. That is typical for PV and canopies, and the reason V03 treats wind in depth.

**Your turn (V01.WP01.1-YT).** Same post, but wind 5.0 kN at 3.0 m and self-weight 3.6 kN at 1.4 m, 200 mm downwind. Find |R| and the base moment. *(Answer in §6.)*

**Software verification.** Stated tool: NumPy. Compute `np.cross(r, F)` for both forces and sum. Tolerance: exact to rounding. Record as VER-V01.M01.

**Thread tasks**
- **T3:** create `strlib/units.py` using `pint` or `forallpeople`, with conversions for kg→kN (g = 9.81 m/s²), kPa×m²→kN, kN/m²×width→kN/m. Write three `pytest` tests, including this WP's 4.225 kN.
- **T1:** finish the layer standard in your DWT (structure, centrelines, dimensions, text, hatch, hidden, notes) with colours and lineweights.

**Self-check quiz V01.Q01** *(answers in §6)*
1. A PV module weighs 28 kg. What is its weight in kN?
2. A slab carries 2.5 kPa. What line load does it put on a beam supporting a 3.0 m wide strip?
3. Two forces, 3 kN along +x and 4 kN along +y, act at the same point. Give the magnitude and direction of the resultant.
4. What is $\mathbf{i} \times \mathbf{j}$? What is $\mathbf{j} \times \mathbf{i}$?
5. A 10 kN force acts vertically downward 2 m to the right of point O. What is the moment about O, with magnitude and sense?
6. True or false: a free-body diagram should show internal forces between parts of the body you have isolated.
7. Why is the wind force on a PV table usually more important than its self-weight for the foundation?
8. Normal-weight reinforced concrete is often taken at about 25 kN/m³. Roughly what is a 200 mm slab's self-weight in kPa?

**Field notes (Kenya).** Supplier datasheets for PV modules, inverters, tanks and dispensers give mass in kg; loads must be in kN. Missing the ×9.81/1000 step is the most common unit error on small projects **(judgement)**. Older drawings sometimes mix units, so check the title block before taking any dimension.

**Portfolio output.** `strlib.units` committed with tests (T4 learning evidence, CPD log).
**Done when:** WP and "Your turn" match the key; Q01 ≥70%; VER-V01.M01 recorded; units module tests pass.

---

## [V01.M02] Equilibrium, supports and determinacy
**Tags:** Phase 1 | Mechanics | T1
**Prerequisites:** M01
**Time:** 8 h (W02–W03)

**Learning outcomes**
1. Idealise real supports (pins, rollers, fixed bases, bearings) and state the reactions each provides.
2. Write and solve the equilibrium equations for 2D rigid bodies, including beams with overhangs.
3. Classify plane structures as unstable, statically determinate or indeterminate (and to what degree).
4. Recognise geometric instability that a reaction count alone misses.

**Code coverage:** none directly. Support idealisation reappears in EN 1993-1-8 (joint classification) and BS 5950-1 §2.1.2 (simple and continuous design) `[VERIFY clause]` in V05.

**Core path**

| Step | Resource and exact part | Time |
|---|---|---:|
| Read | R-0101 ch. 3 (Equilibrium of Particles) and ch. 5 (Rigid Body Equilibrium) | 2.5 h |
| Watch | R-0103 lectures on free-body diagrams and equilibrium of rigid bodies (lecture numbers `[VERIFY]`) | 1.0 h |
| Do | WP02.1, its "Your turn", and 6 determinacy drills from R-0101 ch. 5 | 2.5 h |
| Verify | anaStruct (below) | 0.5 h |
| Test | V01.Q02 | 0.5 h |
| Thread | T1: drafting basics (below) | 1.0 h |

**Supplementary:** R-0104 problem sets for extra equilibrium practice; anaStruct's support types (hinged, roll, fixed) to see how idealisation changes reactions.

### Worked problem V01.WP02.1 — A canopy beam with an overhang

**Situation.** A beam is pinned at A (x = 0), on a roller at B (x = 6 m), and cantilevers 2 m beyond B to C (x = 8 m), like a forecourt canopy beam overhanging its last column. It carries a UDL of 8 kN/m over its full 8 m length and a 12 kN point load at the tip C (fascia and signage).

**Find** the reactions. Then classify the four structures below.

**Assumptions.** (A1) A provides vertical and horizontal reactions; B vertical only. (A2) No horizontal loads, so $H_A = 0$. (A3) Learning example; unfactored loads.

**Solution.** Total UDL = 8 × 8 = 64 kN, acting at x = 4 m.
$$\sum M_A = 0:\quad R_B(6) - 64(4) - 12(8) = 0 \;\Rightarrow\; R_B = \frac{256 + 96}{6} = 58.67\ \text{kN}\ \uparrow$$
$$\sum F_y = 0:\quad R_A = 64 + 12 - 58.67 = 17.33\ \text{kN}\ \uparrow$$
**Check** with $\sum M_B = 0$: $-R_A(6) + 8 \times 6 \times 3 - 8 \times 2 \times 1 - 12 \times 2 = -104 + 144 - 16 - 24 = 0$ ✓.

**Determinacy.** For plane frames, compare the reactions plus internal force unknowns with the available equations: $r - 3 - c$, where $c$ counts the extra equations given by internal hinges.

| Structure | r | Releases (c) | Degree | Classification |
|---|---:|---:|---:|---|
| (a) Propped cantilever (fixed + roller) | 4 | 0 | 1 | Indeterminate, 1st degree |
| (b) Two-pinned portal frame | 4 | 0 | 1 | Indeterminate, 1st degree |
| (c) Three-pinned portal frame (hinge at apex) | 4 | 1 | 0 | Determinate |
| (d) Beam on three rollers (no horizontal restraint) | 3 | 0 | 0 by count | **Unstable**: all reactions parallel, so nothing resists horizontal load |

**Lesson.** The count is necessary, not sufficient. Always check the arrangement: parallel or concurrent reactions make a mechanism.

**Your turn (V01.WP02.1-YT).** Span 5 m, overhang 1.5 m, UDL 10 kN/m over the full 6.5 m, tip load 8 kN. Find $R_A$ and $R_B$. *(Answer in §6.)*

**Software verification (VER-V01.M02).** Stated tool: anaStruct 1.7.0. Model two elements (0–6 m, 6–8 m), hinged support at node 1, roller at node 2, `q_load(-8)` on both elements, `point_load(3, Fy=-12)`. When I ran this on 2026-10-03 it returned reactions of 17.33 and 58.67 kN, matching the hand calc exactly. **Watch the sign convention:** anaStruct reports these upward reactions as negative numbers. Tolerance ≤1% (V00 §11.4).

**Thread tasks.** **T1:** draw the beam in AutoCAD on the structure layer, with centrelines, a dimension string and support symbols as blocks. This is the start of your symbol library.

**Self-check quiz V01.Q02**
1. How many reaction components does a pin provide in 2D? A roller? A fixed support?
2. A simply supported beam of span L carries a point load P at L/3 from A. What are the reactions?
3. State the degree of indeterminacy of a fixed-ended beam (both ends fixed, plane loading).
4. Why is a three-pinned portal frame determinate even though it has four reactions?
5. A beam has a pin at A and rollers at B and C. How indeterminate is it?
6. Give one physical example of a support usually idealised as a pin that is in reality partially fixed.
7. In WP02.1, what happens to $R_A$ if the tip load increases to 30 kN? What does a negative $R_A$ mean physically?
8. What extra check confirms a reaction calculation, beyond the two equations you used?

**Field notes (Kenya).** Canopy and cantilever beams can make the back-span support pull *up* (negative reaction) when the overhang is heavily loaded or wind uplift acts. Holding-down bolts and pad weights must be checked for uplift, not just bearing **(judgement)**. Base plates detailed as "pinned" with four bolts are partly fixed, and that changes moments in the frame.

**Portfolio output.** Support symbol block library in the DWT.
**Done when:** WP and "Your turn" match; Q02 ≥70%; VER-V01.M02 recorded.

---

## [V01.M03] Trusses and frames: method of joints and sections
**Tags:** Phase 1 | Mechanics | T1, T3
**Prerequisites:** M02
**Time:** 8 h (W03–W04)

**Learning outcomes**
1. Check a plane truss for determinacy and stability ($m + r$ vs $2j$).
2. Find member forces by the method of joints and the method of sections.
3. Spot zero-force members by inspection, and explain why they still matter.
4. Analyse pin-jointed frames and machines (multi-force members) by separating parts.

**Code coverage:** none directly. Truss idealisation (pinned joints, loads at nodes) is revisited in V05 under EN 1993-1-8 / BS 5950-1.

**Core path**

| Step | Resource and exact part | Time |
|---|---|---:|
| Read | R-0101 ch. 6 (Equilibrium of Structures: trusses, frames and machines) | 2.0 h |
| Watch | R-0103 lectures on trusses (method of joints and sections) `[VERIFY lecture numbers]` | 1.0 h |
| Do | WP03.1, its "Your turn", and 6 problems from R-0101 ch. 6 | 2.5 h |
| Verify | anaStruct truss model | 0.5 h |
| Test | V01.Q03 | 0.5 h |
| Threads | T3: joint-method solver (1.0 h); T1: truss general arrangement drawing (0.5 h) | 1.5 h |

**Supplementary:** R-0101 ch. 6 interactive truss figures. Experiment: in anaStruct, delete vertical U1–L1 from the WP truss and load joint L1. The model fails to solve, because L1 becomes a mechanism (two collinear members can't resist a transverse load). That's the zero-force member lesson made visible.

### Worked problem V01.WP03.1 — A shed roof truss

**Situation.** A parallel-chord Pratt truss spans 12 m in four 3 m panels and is 3 m deep. Bottom nodes L0–L4 sit at x = 0, 3, 6, 9, 12 m. Top nodes U1–U3 sit at x = 3, 6, 9 m. The end posts L0–U1 and U3–L4 are inclined. There are verticals U1–L1, U2–L2, U3–L3 and diagonals U1–L2, U3–L2. Purlins put 15 kN on each top node. L0 is pinned and L4 is on a roller.

**Find** the forces in the panel-2 members (U1–U2, L1–L2, U1–L2), the end post, and all the verticals.

**Determinacy.** m = 13 members, j = 8 joints, r = 3: m + r = 16 = 2j ✓ (and the arrangement is triangulated, so it's stable).

**Reactions.** By symmetry, $R_{L0} = R_{L4} = 45/2 = 22.5$ kN ↑.

**Method of sections (cut through panel 2, keep the left part).**
$$\sum M_{L2} = 0:\quad 22.5(6) - 15(3) - F_{U1U2}(3) = 0 \Rightarrow F_{U1U2} = 30.0\ \text{kN (compression)}$$
$$\sum M_{U1} = 0:\quad 22.5(3) - F_{L1L2}(3) = 0 \Rightarrow F_{L1L2} = 22.5\ \text{kN (tension)}$$
$$\sum F_y = 0:\quad 22.5 - 15 - F_{U1L2}\sin 45^\circ = 0 \Rightarrow F_{U1L2} = \frac{7.5}{0.7071} = 10.61\ \text{kN (tension)}$$
Check $\sum F_x$: $-30.0 + 10.61\cos 45^\circ + 22.5 = -30.0 + 7.5 + 22.5 = 0$ ✓.

**Method of joints.**
- Joint L0: $22.5 + F_{L0U1}\sin 45^\circ = 0 \Rightarrow F_{L0U1} = -31.82$ kN (**compression**), and $F_{L0L1} = +22.5$ kN (tension).
- Joint L1: no load, and both chords are horizontal, so **$F_{U1L1} = 0$**: a zero-force member.
- Joint U2: $-15 - F_{U2L2} = 0 \Rightarrow F_{U2L2} = -15.0$ kN (compression).
- Check at joint L2: the diagonals give 2 × 7.5 = 15 kN up, and U2–L2 pushes down 15 kN ✓.

**Why the zero-force vertical still matters.** It braces the top chord against buckling out of the plane, and it carries load the moment any load lands on L1, such as a hoist or a services hanger. Deleting it "because it carries nothing" is a classic fabrication-yard mistake **(judgement)**.

**Your turn (V01.WP03.1-YT).** Increase each top-node load to 20 kN and hang 10 kN from L2 (signage). Find U1–U2, L1–L2, U1–L2 and U2–L2. *(Answer in §6.)*

**Software verification (VER-V01.M03).** Stated tool: anaStruct 1.7.0 using `add_truss_element`. I ran it on 2026-10-03: L0–L1 = L1–L2 = 22.5, U1–U2 = −30.0, L0–U1 = −31.82, U1–L1 = 0.0, U2–L2 = −15.0, U1–L2 = +10.607 kN, all matching the hand calc (Δ = 0%). anaStruct reports compression as negative.

**Thread tasks.**
- **T3:** write `strlib/truss.py`, a method-of-joints solver that assembles the 2j equilibrium equations and solves them with `numpy.linalg.solve`. Test it against this WP. (This is your first linear system; M10 and V02.M08 build on it.)
- **T1:** draw the truss general arrangement (GA) with member marks and a force table.

**Self-check quiz V01.Q03**
1. A truss has 11 members, 7 joints and 3 reactions. Is it determinate?
2. At an unloaded joint where two non-collinear members meet, what are the member forces?
3. At an unloaded joint where three members meet and two are collinear, what can you say about the third?
4. When is the method of sections faster than the method of joints?
5. In a Pratt truss under gravity load, are the diagonals typically in tension or compression? And in a Howe truss?
6. Why are truss loads assumed to act at the nodes, and what happens to a chord if purlins sit between nodes?
7. In WP03.1, which member carries the largest force, and why does that make sense?
8. What is the difference between a truss member and a frame (multi-force) member?

**Field notes (Kenya).** Shed and canopy trusses are commonly built from welded hollow sections, angles or cold-formed profiles. Watch for purlins placed between nodes, which bends the top chord, and for "simplified" bracing that removes zero-force members, which ruins chord stability **(judgement)**.

**Portfolio output.** Truss GA drawing + `truss.py` with tests.
**Done when:** WP and "Your turn" match; Q03 ≥70%; VER-V01.M03 recorded; solver tests pass.

---

## [V01.M04] Distributed loads, centroids and section properties
**Tags:** Phase 1 | Mechanics | T3, T5
**Prerequisites:** M01
**Time:** 8 h (W04)

**Learning outcomes**
1. Replace distributed loads (uniform, triangular, trapezoidal) with statically equivalent resultants.
2. Locate the centroid of composite areas.
3. Compute second moment of area ($I$), elastic modulus ($Z$, EN $W_{el}$), plastic modulus ($S$, EN $W_{pl}$) and radius of gyration ($i$, BS $r$) for built-up sections, using the parallel-axis theorem.
4. Explain the shape factor and why an I-section is efficient in bending.

**Code coverage:** notation only. EN 1993-1-1 §1.6 symbols ($W_{el}$, $W_{pl}$, $i$) ↔ BS 5950-1 notation ($Z$, $S$, $r$). Section classification (EN 1993-1-1 §5.5 ↔ BS 5950-1 §3.5) waits for V05.

**Core path**

| Step | Resource and exact part | Time |
|---|---|---:|
| Read | R-0101 ch. 7 (Centroids and Centers of Gravity) and ch. 10 (Moments of Inertia) | 2.5 h |
| Watch | R-0101's interactive figures for ch. 10 (parallel-axis theorem) | 0.5 h |
| Do | WP04.1, its "Your turn", and 4 problems from R-0101 ch. 10 | 2.5 h |
| Verify | `sectionproperties` | 0.5 h |
| Test | V01.Q04 | 0.5 h |
| Threads | T3: section-property function (1.0 h); T5: spot sections on site (0.5 h) | 1.5 h |

**Supplementary:** the `sectionproperties` documentation examples (plastic properties, composite sections); R-0101 ch. 10 interactive figures.

### Worked problem V01.WP04.1 — A welded I-girder, a tee, and a trapezoidal load

**Part A: welded I-girder** (a canopy rafter built up from plate): flanges 200 × 12 mm, web 376 × 8 mm, overall depth 400 mm.
$$A = 2(200)(12) + 376(8) = 4800 + 3008 = 7808\ \text{mm}^2$$
$$I_x = \frac{200(400)^3}{12} - \frac{(200-8)(376)^3}{12} = 2.161 \times 10^8\ \text{mm}^4$$
$$W_{el} = Z = \frac{I_x}{200} = 1.081 \times 10^6\ \text{mm}^3$$
$$W_{pl} = S = 2(200)(12)(194) + 2\left[8 \times 188 \times 94\right] = 931\,200 + 282\,752 = 1.214 \times 10^6\ \text{mm}^3$$
Shape factor $W_{pl}/W_{el} = 1.12$. Most of the material is in the flanges, far from the neutral axis, which is why an I-section is efficient in bending.

**Part B: a tee** (a stiffener or a column cap): flange 300 × 20 mm on top of a 280 × 10 mm web, total depth 300 mm. Measure $\bar{y}$ from the bottom of the web.
$$A_f = 6000\ \text{mm}^2 \text{ at } y = 290,\qquad A_w = 2800\ \text{mm}^2 \text{ at } y = 140$$
$$\bar{y} = \frac{6000(290) + 2800(140)}{8800} = 242.3\ \text{mm from the bottom (57.7 mm below the top)}$$
$$I_x = \frac{300(20)^3}{12} + 6000(47.7)^2 + \frac{10(280)^3}{12} + 2800(102.3)^2 = 6.145 \times 10^7\ \text{mm}^4$$
$$Z_{top} = 6.145\times10^7/57.7 = 1.064\times10^6\ \text{mm}^3,\qquad Z_{bot} = 6.145\times10^7/242.3 = 2.54\times10^5\ \text{mm}^3$$
The tip of the web is four times more highly stressed than the flange for the same moment. That asymmetry matters in V05.

**Part C: trapezoidal load**, rising from 4 kN/m at x = 0 to 10 kN/m at x = 6 m (for example, a load from a tapering roof area).
$$W = \tfrac{1}{2}(4 + 10)(6) = 42\ \text{kN},\qquad \bar{x} = \frac{L(w_1 + 2w_2)}{3(w_1 + w_2)} = \frac{6(4 + 20)}{3(14)} = 3.43\ \text{m from the 4 kN/m end}$$

**Checks.** $\bar{y}$ lies within the flange-heavy upper part, as expected ✓. $\bar{x}$ is past mid-length, toward the heavier end ✓.

**Your turn (V01.WP04.1-YT).** A tee with a 250 × 16 mm flange on a 300 × 12 mm web: find $A$, $\bar{y}$, $I_x$, $Z_{top}$, $Z_{bot}$. *(Answer in §6.)*

**Software verification (VER-V01.M04).** Stated tool: `sectionproperties` 3.10.2. Build each section from `rectangular_section` pieces and run `calculate_geometric_properties()` and `calculate_plastic_properties()`. I ran it on 2026-10-03: I-girder A = 7808, $I_x$ = 216 148 651, $Z$ = 1 080 743, $S$ = 1 213 952; tee $\bar{y}$ = 242.27, $I_x$ = 61 447 879. That matches the hand calcs exactly (rectangles mesh without error). Tolerance ≤0.5%.

**Thread tasks.**
- **T3:** `strlib/sections.py` with a `composite_rect(parts)` function returning A, centroid, I, Z and S. Test it against this WP and against `sectionproperties`.
- **T5:** find two built-up or rolled sections on a site, in a fabrication yard or on drawings. Photograph them, measure them, and compute their I.
- **Calcpad:** present Part B as your first formatted calc sheet.

**Self-check quiz V01.Q04**
1. State the parallel-axis theorem.
2. What is I for a 300 × 600 mm rectangle about its major axis?
3. Why is $W_{pl}$ always greater than $W_{el}$?
4. Where does the resultant of a triangular load of peak w over length L act, and how large is it?
5. A section has I = 8 × 10⁷ mm⁴ and A = 6000 mm². What is its radius of gyration?
6. What do $W_{el}$ and $W_{pl}$ correspond to in BS 5950 notation?
7. For a symmetric I-section, why are $Z_{top}$ and $Z_{bot}$ equal, while for a tee they are not?
8. Doubling the depth of a rectangular beam multiplies its I by what?

**Field notes (Kenya).** Local fabricators often build sections from plate or back-to-back channels, depending on what hot-rolled sizes are in stock **(judgement)**. Always compute the properties of the section as actually built, including weld sizes and any plate thickness substitutions, rather than assuming a catalogue section.

**Portfolio output.** First Calcpad calc sheet; `sections.py` with tests.
**Done when:** WP and "Your turn" match; Q04 ≥70%; VER-V01.M04 recorded.

---

## [V01.M05] Axial, shear and moment diagrams
**Tags:** Phase 1 | Mechanics | T3, T4
**Prerequisites:** M02, M04
**Time:** 8 h (W05)

**Learning outcomes**
1. Find internal axial force, shear and moment at any section by free bodies.
2. Draw shear force and bending moment diagrams (SFD/BMD) using the load–shear–moment relationships $dV/dx = -w$ and $dM/dx = V$.
3. Locate maximum moments (where V = 0), hogging moments over supports, and points of contraflexure.
4. Sketch the deflected shape from the BMD.

**Code coverage:** none directly; the sign convention matches EN 1990/EN 1992 practice (sagging positive) and the bending moment diagrams in BS 8110 design aids.

**Core path**

| Step | Resource and exact part | Time |
|---|---|---:|
| Read | R-0101 ch. 8 (Internal Loadings: shear and moment diagrams) | 2.0 h |
| Watch | R-0102 lectures on shear force and bending moment diagrams `[VERIFY lecture numbers]` | 1.0 h |
| Do | WP05.1, its "Your turn", and 6 diagram drills from R-0101 ch. 8 | 2.5 h |
| Verify | anaStruct | 0.5 h |
| Test | V01.Q05 | 0.5 h |
| Threads | T3: SFD/BMD plotter (1.0 h); T4: submit your GE application (0.5 h) | 1.5 h |

**Supplementary:** R-0101 ch. 8 interactive shear and moment diagram figures; R-0102 lectures on relations between load, shear and moment.

### Worked problem V01.WP05.1 — Diagrams for the overhanging canopy beam

Use the WP02.1 beam: $R_A$ = 17.33 kN, $R_B$ = 58.67 kN, UDL 8 kN/m, 12 kN at the tip.

**Span AB (0 ≤ x ≤ 6 m):**
$$V(x) = 17.33 - 8x, \qquad M(x) = 17.33x - 4x^2$$
- V = 0 at $x = 17.33/8 = 2.17$ m, where $M_{max} = 17.33(2.17) - 4(2.17)^2 = 18.78$ kNm (**sagging**).
- Point of contraflexure: $M = 0$ at $x = 17.33/4 = 4.33$ m.
- Just left of B: $V = 17.33 - 48 = -30.67$ kN.

**At support B:** shear jumps by $R_B$: $-30.67 + 58.67 = +28.0$ kN, which equals the load on the overhang ($8 \times 2 + 12 = 28$) ✓.
$$M_B = -(12 \times 2 + 8 \times 2 \times 1) = -40.0\ \text{kNm}\ \text{(**hogging**)}$$
Check from the left: $17.33(6) - 4(36) = 104 - 144 = -40$ ✓.

**Overhang BC:** V falls linearly from 28.0 to 12.0 kN; M rises from −40 to 0 at the tip.

**Reading the diagrams.** The largest moment is the 40 kNm hogging over B, more than twice the 18.8 kNm sagging in the span. In concrete, the main steel over B goes in the top. In steel, the bottom flange near B is in compression, which matters for lateral–torsional buckling in V05. The beam curves upward (hogs) from x = 4.33 m to the tip.

**Your turn (V01.WP05.1-YT).** Draw the diagrams for the WP02.1-YT beam. Give the maximum sagging moment and its position, $M_B$, and the point of contraflexure. *(Answer in §6.)*

**Software verification (VER-V01.M05).** Stated tool: anaStruct (same model as M02). I ran it on 2026-10-03: hogging 40.00 kNm and sagging 18.77 kNm, against 18.78 by hand (Δ = 0.03%, due to element discretisation). anaStruct's moment sign is opposite to this volume's convention, so compare magnitudes and diagram shape. Tolerance ≤2%.

**Thread tasks.**
- **T3:** `strlib/diagrams.py`, which takes reactions and loads and returns V(x) and M(x) arrays, and plots them with matplotlib. Test it against this WP.
- **T4:** submit your Graduate Engineer application (tracker milestone EBK-GE) and log the date in the EBK clock.

**Self-check quiz V01.Q05**
1. What is the slope of the BMD at any point equal to?
2. Where does the maximum moment occur in a span carrying distributed load?
3. What happens to the SFD at a point load? And to the BMD?
4. What is the maximum moment in a simply supported beam with a central point load P?
5. What is a point of contraflexure, and why does it matter for reinforcement detailing?
6. A cantilever of length L carries a UDL w. What are the support moment and shear?
7. In WP05.1, why is the shear jump at B equal to $R_B$?
8. Sketch (in words) the deflected shape of WP05.1's beam.

**Field notes (Kenya).** Cantilevered balconies, canopies and slab overhangs depend on top reinforcement. Site crews sometimes place it low, or let it be trodden down before the pour, and the cantilever loses most of its capacity. Read the BMD to know which face is in tension, then inspect cover and bar position at that face **(judgement)**.

**Portfolio output.** Diagram plotter; GE application receipt (EBK portfolio).
**Done when:** WP and "Your turn" match; Q05 ≥70%; VER-V01.M05 recorded; GE application submitted.

---

## [V01.M06] Stress, strain and material behaviour
**Tags:** Phase 1 | Materials (concrete, steel, timber, aluminium) | T1
**Prerequisites:** M02
**Time:** 6 h (W05, W07)

**Learning outcomes**
1. Compute axial stress, strain and elongation; apply Hooke's law and Poisson's ratio.
2. Calculate thermal strain, and the stress when thermal movement is restrained.
3. Analyse a two-material member (an RC column) using strain compatibility and the modular ratio.
4. Describe the stress–strain behaviour of structural steel, concrete, timber and aluminium, and what "yield", "ductility" and "brittle" mean for design.

**Code coverage (EN primary, BS alongside):**

| Property | EN (KS EN) | BS | What differs |
|---|---|---|---|
| Steel E, G, ν, α | EN 1993-1-1 §3.2.6 | BS 5950-1 §3.1.3 | **E = 210 kN/mm² in EN; 205 kN/mm² in BS 5950.** Same steel, different code constant: use the one matching the code you design to |
| Reinforcement E | EN 1992-1-1 §3.2.7 | BS 8110-1 §2.4.2.3 `[VERIFY]` | 200 kN/mm² in both |
| Concrete E, ν, α | EN 1992-1-1 §3.1.3, Table 3.1 | BS 8110-2 §7.2 `[VERIFY]` | EN ties $E_{cm}$ to strength class; BS gives a range tied to cube strength |
| Aluminium | EN 1999-1-1 §3.2.5 `[VERIFY]` | BS 8118-1 `[VERIFY]` | E ≈ 70 kN/mm², a third of steel: deflection and buckling govern PV rails |
| Timber | EN 1995-1-1 with EN 338 strength classes | BS 5268-2 strength classes `[VERIFY]` | Different class tables; stiffness varies with grain direction and moisture |

**Core path**

| Step | Resource and exact part | Time |
|---|---|---:|
| Watch | R-0102 lectures on stress, strain, Hooke's law, thermal stress and composite bars `[VERIFY lecture numbers]` | 1.5 h |
| Read | R-0104 lecture notes on stress, strain and material behaviour; the code clauses in the table above | 1.0 h |
| Do | WP06.1, its "Your turn", and 2 problems from R-0104 problem sets 1–3 `[VERIFY topic mapping]` | 1.5 h |
| Verify | Python transformed-section function | 0.5 h |
| Test | V01.Q06 | 0.5 h |
| Thread | T1: dimensioning and annotation scales | 1.0 h |

**Supplementary:** R-0104 lecture notes on thermal stress and statically indeterminate axial members.

### Worked problem V01.WP06.1 — A canopy tie rod and an RC column

**Part A: tie rod.** A 20 mm diameter steel rod, 4.0 m long, carries 45 kN in tension. E = 210 kN/mm², α = 12 × 10⁻⁶ /°C.
$$A = \pi(10)^2 = 314.2\ \text{mm}^2,\qquad \sigma = \frac{45\,000}{314.2} = 143.2\ \text{N/mm}^2$$
$$\delta = \frac{\sigma L}{E} = \frac{143.2 \times 4000}{210\,000} = 2.73\ \text{mm}$$
If the rod were fully restrained and heated by 30 °C:
$$\sigma_T = E\alpha\Delta T = 210\,000 \times 12\times10^{-6} \times 30 = 75.6\ \text{N/mm}^2\ \text{(compression)}$$
That's more than half the stress from the load, which is why long restrained steel members exposed to the sun need movement joints.

**Part B: RC column.** A 300 × 300 mm column with 4 bars of 16 mm diameter carries a service axial load of 1200 kN. Assume short-term $E_c$ = 30 kN/mm² (an assumption for this example; EN 1992-1-1 Table 3.1 gives $E_{cm}$ by class) and $E_s$ = 200 kN/mm².
$$A_s = 4 \times \pi(8)^2 = 804\ \text{mm}^2,\qquad A_c = 90\,000 - 804 = 89\,196\ \text{mm}^2,\qquad n = E_s/E_c = 6.67$$
Compatibility: concrete and steel strain equally, so $\sigma_s = n\,\sigma_c$.
$$\sigma_c = \frac{N}{A_c + nA_s} = \frac{1\,200\,000}{89\,196 + 6.67 \times 804} = \frac{1\,200\,000}{94\,557} = 12.7\ \text{N/mm}^2$$
$$\sigma_s = 6.67 \times 12.7 = 84.6\ \text{N/mm}^2$$
The steel is less than 1% of the area but carries 5.7% of the load. Under long-term load, creep lowers the effective $E_c$, n rises, and load migrates to the steel. That's why V04 uses an effective (long-term) modulus.

**Checks.** Both stresses are well below material strengths ✓. $\sigma_s/\sigma_c = n$ ✓.

**Your turn (V01.WP06.1-YT).** A 24 mm rod, 5.0 m long, carries 60 kN. Find σ, δ, and the restrained thermal stress for a 25 °C rise. *(Answer in §6.)*

**Software verification (VER-V01.M06).** Stated tool: your own `strlib/axial.py` (transformed area and composite stresses), tested against this WP. Tolerance: exact to rounding. Then change E to 205 kN/mm² (BS 5950) and note that δ rises by 2.4%.

**Thread tasks.** **T1:** set up annotation scales (1:20, 1:50, 1:100), dimension styles and a text style. Annotate the WP06 column section with bar marks in the BS 8666 manner, as practice ahead of V04.

**Self-check quiz V01.Q06**
1. Define engineering strain. Why is it dimensionless?
2. A bar with E = 200 kN/mm² is stressed to 100 N/mm². What is the strain?
3. What is Poisson's ratio for steel, and roughly for uncracked concrete?
4. Why does restraint matter for thermal stress? What is the stress in an unrestrained bar heated by 50 °C?
5. In a composite column, why is $\sigma_s/\sigma_c = n$?
6. Which design code uses E = 205 kN/mm² for structural steel, and which uses 210 kN/mm²?
7. Sketch (in words) the stress–strain curves for mild steel and for concrete in compression. Which one shows a yield plateau?
8. Why does aluminium's E (about 70 kN/mm²) matter more for PV racking than its strength?

**Field notes (Kenya).** Reinforcement in Kenya is supplied by several local mills and importers, with grade markings and mill certificates. Ask for the certificate, and for bend and tensile test results on important jobs. Concrete cube results in local practice are often reported by "class"; know whether a figure is a cube or a cylinder strength before using it **(judgement; local grade conventions `[VERIFY]` in V04)**.

**Portfolio output.** Annotated column section DWG; `axial.py`.
**Done when:** WP and "Your turn" match; Q06 ≥70%; VER-V01.M06 recorded.

---

## [V01.M07] Bending and shear stress, combined stress, Mohr's circle
**Tags:** Phase 1 | Mechanics | T3
**Prerequisites:** M04, M05, M06
**Time:** 8 h (W07–W08)

**Learning outcomes**
1. Compute bending stress $\sigma = My/I$ and check it against $M/Z$.
2. Compute shear stress $\tau = VQ/(It)$ at any level of a section, and compare it with the "average web shear" shortcut.
3. Transform plane stress and find principal stresses and the maximum shear stress, by formula and with Mohr's circle.
4. Apply the von Mises criterion to a point with combined σ and τ.

**Code coverage:**

| Check | EN 1993-1-1 | BS 5950-1 | What differs |
|---|---|---|---|
| Elastic bending | §6.2.5 | §4.2.5 | Both allow plastic modulus for compact (Class 1–2 / plastic–compact) sections |
| Shear | §6.2.6, incl. (4) for elastic τ | §4.2.3 | **Shear strength: EN uses $f_y/\sqrt{3}$ (0.577 $f_y$); BS uses 0.6 $p_y$** |
| Combined stress | §6.2.1(5) von Mises criterion | — `[VERIFY BS equivalent]` | EN states the elastic interaction criterion explicitly |

**Core path**

| Step | Resource and exact part | Time |
|---|---|---:|
| Watch | R-0102 lectures on bending stress, shear stress in beams, and transformation of stress / Mohr's circle `[VERIFY lecture numbers]` | 2.0 h |
| Read | R-0104 lecture notes on beam stresses and stress transformation | 1.0 h |
| Do | WP07.1, its "Your turn", and 4 Mohr's-circle drills | 3.0 h |
| Verify | `sectionproperties` stress plot | 0.5 h |
| Test | V01.Q07 | 0.5 h |
| Thread | T3: Mohr's-circle function | 1.0 h |

**Supplementary:** R-0104 problem sets on stress transformation; R-0102 lectures on combined stresses.

### Worked problem V01.WP07.1 — Stresses in the welded I-girder

Use the WP04.1 girder ($I_x$ = 2.1615 × 10⁸ mm⁴, depth 400 mm, flanges 200 × 12 mm, web 376 × 8 mm) at a section where M = 120 kNm and V = 80 kN.

**Bending stress at the extreme fibre:**
$$\sigma_{max} = \frac{My}{I} = \frac{120\times10^6 \times 200}{2.1615\times10^8} = 111.0\ \text{N/mm}^2$$

**Shear stress at the neutral axis:**
$$Q_{NA} = 200(12)(194) + 8(188)(94) = 465\,600 + 141\,376 = 606\,976\ \text{mm}^3$$
$$\tau_{NA} = \frac{VQ}{It} = \frac{80\,000 \times 606\,976}{2.1615\times10^8 \times 8} = 28.1\ \text{N/mm}^2$$
The "average web shear" $V/(h_w t_w) = 80\,000/(376 \times 8) = 26.6$ N/mm² is within 6%. That is why codes use a shear area.

**Combined stress at the web–flange junction** (y = 188 mm):
$$\sigma = \frac{120\times10^6 \times 188}{2.1615\times10^8} = 104.4\ \text{N/mm}^2,\qquad \tau = \frac{80\,000 \times 465\,600}{2.1615\times10^8 \times 8} = 21.5\ \text{N/mm}^2$$
Mohr's circle: centre at σ/2 = 52.2, radius $R = \sqrt{52.2^2 + 21.5^2} = 56.5$ N/mm².
$$\sigma_1 = 52.2 + 56.5 = 108.6,\qquad \sigma_2 = 52.2 - 56.5 = -4.3,\qquad \tau_{max} = 56.5\ \text{N/mm}^2$$
Von Mises: $\sigma_{vm} = \sqrt{\sigma^2 + 3\tau^2} = \sqrt{104.4^2 + 3(21.5)^2} = 110.8$ N/mm².

**Reading the result.** At this section, the combined stress at the junction (110.8) is just below the extreme-fibre bending stress (111.0). Where shear is high and moment is high at the same point, such as over the support of a continuous beam, the junction can govern. EN 1993-1-1 §6.2.1(5) is the check for that point.

**Your turn (V01.WP07.1-YT).** Same girder with M = 150 kNm and V = 100 kN. Find $\sigma_{max}$, $\tau_{NA}$, and the junction's principal stresses and von Mises stress. *(Answer in §6.)*

**Software verification (VER-V01.M07).** Stated tool: `sectionproperties`. Run `calculate_warping_properties()`, then `calculate_stress(mxx=120e6, vy=80e3)`, and read the peak bending and shear stresses. Expect bending to match to <0.5%. Expect shear at the neutral axis within ~5%: the FE solution captures shear flow and the flange's share of shear, which VQ/It simplifies. Record any difference and its reason. Tolerance ≤5% (V00 §11.4, local stresses).

**Thread task.** **T3:** `strlib/stress.py` with `principal(sx, sy, txy)` returning σ₁, σ₂, τmax and the principal angle, plus `von_mises(...)`. Test it against this WP and V00.D09.

**Self-check quiz V01.Q07**
1. Where is bending stress zero in a beam section, and where is it largest?
2. Why is shear stress zero at the extreme fibres of a rectangular section?
3. What is the maximum shear stress in a rectangular section, as a multiple of V/A?
4. On Mohr's circle, what do the points where the circle crosses the σ-axis represent?
5. For pure shear τ, what are the principal stresses, and at what angle do they act?
6. State the von Mises equivalent stress for a point with σ and τ only.
7. Why do steel codes use a reduced shear strength ($f_y/\sqrt{3}$ or 0.6 $p_y$)?
8. In WP07.1, where would you look first for the most critical combined stress along a continuous beam?

**Field notes (Kenya).** Combined stresses matter most at welded junctions of built-up girders and at holes cut on site for services through webs. Unplanned web penetrations near supports, where shear is highest, are a common site change that should go back to the designer **(judgement)**.

**Portfolio output.** `stress.py` with tests; Mohr's-circle plot of WP07.1.
**Done when:** WP and "Your turn" match; Q07 ≥70%; VER-V01.M07 recorded with the reason for the shear difference.

---

## [V01.M08] Torsion and beam deflections
**Tags:** Phase 1 | Mechanics | T3
**Prerequisites:** M05, M06
**Time:** 8 h (W08)

**Learning outcomes**
1. Compute torsional shear stress and angle of twist in solid and hollow circular sections; explain why open sections are weak in torsion.
2. Find beam deflections by double integration and by Macaulay's (singularity function) method.
3. Use moment-area theorems for slope and deflection at specific points.
4. Compare a deflection with a serviceability limit and say which code sets it.

**Code coverage:**

| Topic | EN | BS | What differs |
|---|---|---|---|
| Torsion in steel members | EN 1993-1-1 §6.2.7 | BS 5950-1 (torsion detail via SCI guidance `[VERIFY]`) | EN gives an explicit torsion check |
| Deflection limits | EN 1990 Annex A1 §A1.4 (values set in the National Annex) | BS 5950-1 §2.5.2 and Table 8 | **BS tabulates limits (e.g. span/360 for beams carrying brittle finishes); EN leaves them to the NA**. Check the Kenya NA in V03 `[VERIFY]` |
| RC deflection | EN 1992-1-1 §7.4 | BS 8110-1 §3.4.6 (span/effective-depth) | Both use span/depth rules for routine cases |

**Core path**

| Step | Resource and exact part | Time |
|---|---|---:|
| Watch | R-0102 lectures on torsion of circular shafts and deflection of beams (double integration, Macaulay, moment-area) `[VERIFY lecture numbers]` | 2.0 h |
| Read | R-0104 lecture notes on torsion and beam deflection | 1.0 h |
| Do | WP08.1 (both parts), its "Your turn", and 3 deflection drills | 2.5 h |
| Verify | PyNite and `sectionproperties` | 1.0 h |
| Test | V01.Q08 | 0.5 h |
| Thread | T3: Macaulay deflection tool | 1.0 h |

**Supplementary:** R-0102 lectures on statically indeterminate beams, a preview of V02.M04–M06.

### Worked problem V01.WP08.1 — Deflection of a canopy purlin beam, and torsion in a sign post

**Part A: deflection.** A simply supported beam spans 6 m and carries a 30 kN point load 2 m from A plus a 5 kN/m UDL. E = 210 kN/mm², I = 8.0 × 10⁷ mm⁴, so EI = 16 800 kNm².

Reactions: $R_A = 30 \times 4/6 + 5 \times 6/2 = 20 + 15 = 35$ kN.

Macaulay:
$$EI\,y'' = M(x) = 35x - 30\langle x-2\rangle - \tfrac{5}{2}x^2$$
$$EI\,y = \frac{35x^3}{6} - \frac{30\langle x-2\rangle^3}{6} - \frac{5x^4}{24} + C_1x + C_2$$
Boundary conditions: y(0) = 0 gives $C_2 = 0$. y(6) = 0 gives
$$C_1 = -\frac{1}{6}\left[\frac{35(216)}{6} - \frac{30(64)}{6} - \frac{5(1296)}{24}\right] = -\frac{1260 - 320 - 270}{6} = -111.67$$
At midspan (x = 3):
$$EI\,y = \frac{35(27)}{6} - \frac{30(1)}{6} - \frac{5(81)}{24} - 111.67(3) = 157.5 - 5.0 - 16.88 - 335.0 = -199.4\ \text{kNm}^3$$
$$y = -\frac{199.4}{16\,800} = -0.01187\ \text{m} = -11.9\ \text{mm}$$
The maximum, 11.91 mm, occurs at x ≈ 2.84 m, close to midspan as usual. For comparison, span/360 = 16.7 mm: this beam passes a typical brittle-finish limit **(learning example; real limits depend on the code and NA)**.

**Part B: torsion.** A CHS 168.3 × 6.3 sign post, 3.0 m tall, carries a torque of 5 kNm from an eccentric sign under wind. G = 81 kN/mm².
$$J = \frac{\pi(D^4 - d^4)}{32} = \frac{\pi(168.3^4 - 155.7^4)}{32} = 2.107\times10^7\ \text{mm}^4$$
$$\tau = \frac{T\,r}{J} = \frac{5\times10^6 \times 84.15}{2.107\times10^7} = 20.0\ \text{N/mm}^2,\qquad \theta = \frac{TL}{GJ} = \frac{5\times10^6 \times 3000}{81\,000 \times 2.107\times10^7} = 0.0088\ \text{rad} = 0.50^\circ$$
A closed tube resists torsion very efficiently. An open section of similar weight, such as a channel, would twist many times more. That's why posts carrying eccentric signs or PV panels are usually tubes.

**Your turn (V01.WP08.1-YT).** Span 5 m, a 20 kN point load at 1.5 m from A, UDL 4 kN/m, EI = 16 800 kNm². Find $R_A$, $C_1$, the midspan deflection, and the maximum deflection with its position. *(Answer in §6.)*

**Software verification (VER-V01.M08).**
- **PyNite 3.2.0** (`from Pynite import FEModel3D`): one member with nodes at 0, 2, 3 and 6 m, a pin and a roller, a point load and a distributed load. I ran it on 2026-10-03: deflection at 3 m = 11.868 mm and maximum = 11.907 mm, matching Macaulay (Δ < 0.01%). Tolerance ≤5%.
- **`sectionproperties`** CHS torsion constant: J = 2.0997 × 10⁷ mm⁴ against 2.107 × 10⁷ by formula (−0.34%). The difference comes from approximating the circle as a 64-sided polygon; a finer `n` closes the gap. A good reminder that geometry discretisation shows up in "exact" answers.

**Thread task.** **T3:** `strlib/deflection.py`, a Macaulay engine taking point loads, UDLs and supports and returning y(x). Test it against this WP and PyNite.

**Self-check quiz V01.Q08**
1. What is the maximum deflection of a simply supported beam under a UDL w?
2. What is the tip deflection of a cantilever under an end load P?
3. Why are Macaulay brackets $\langle x-a\rangle$ set to zero when x < a?
4. How many boundary conditions does a simply supported beam give, and which ones?
5. Why is a closed tube far stiffer in torsion than an open channel of the same area?
6. If you double the span of a simply supported beam under UDL, what happens to the deflection?
7. Which document sets deflection limits for steel beams under BS 5950-1, and which under the Eurocodes?
8. In WP08.1 Part A, why is the maximum deflection slightly left of midspan?

**Field notes (Kenya).** Sagging canopy fascias and ponding on flat roofs are deflection failures, not strength failures. They're common complaints on forecourts and carports **(judgement)**. Eccentric signage on single posts twists them, so check torsion and base fixity, not just bending.

**Portfolio output.** `deflection.py` with tests; VER record showing the PyNite match.
**Done when:** WP and "Your turn" match; Q08 ≥70%; VER-V01.M08 recorded.

---

## [V01.M09] Buckling: Euler, effective length and imperfections
**Tags:** Phase 1 | Steel (preview) | T3
**Prerequisites:** M04, M06, M08
**Time:** 5 h (W09)

**Learning outcomes**
1. Derive and apply the Euler critical load $N_{cr} = \pi^2EI/L_{cr}^2$ and state its assumptions.
2. Choose effective lengths for common end conditions, and explain why codes use practical rather than theoretical values.
3. Explain why real columns fail below $N_{cr}$ (imperfections, residual stress, yielding) and how codes capture this.
4. Compute a column's buckling resistance using **EN 1993-1-1** (reduction factor χ) and **BS 5950-1** (Perry–Robertson $p_c$) and compare the two.

**Code coverage (EN primary, BS in full):**

| Step | EN 1993-1-1 | BS 5950-1 |
|---|---|---|
| Buckling resistance | §6.3.1.1, $N_{b,Rd} = \chi A f_y/\gamma_{M1}$ | §4.7.4, $P_c = A_g\,p_c$ |
| Curve selection | §6.3.1.2, Table 6.2 (curve by section type, fabrication and steel grade); imperfection factors in Table 6.1 | §4.7.5, Table 23 (strut curve by section type) |
| Strength formula | §6.3.1.2: Φ and χ from $\bar{\lambda}$ | Annex C: Perry–Robertson, $p_c$ from λ |
| Effective length | Not given in EN 1993-1-1 (use guidance / NCCI) | Table 22 (effective lengths of compression members) |
| Partial factor | $\gamma_{M1}$: recommended 1.0; **Kenya NA value `[VERIFY]`** | Factors built into $p_y$ and the load factors |

**Core path**

| Step | Resource and exact part | Time |
|---|---|---:|
| Watch | R-0102 lectures on columns and buckling (Euler, end conditions, eccentric loading) `[VERIFY lecture numbers]` | 1.0 h |
| Read | The clauses in the table above (EN 1993-1-1 §6.3.1; BS 5950-1 §4.7 and Annex C) | 0.5 h |
| Do | WP09.1, its "Your turn" | 1.5 h |
| Verify | Finite-difference buckling eigenvalue (NumPy) | 0.5 h |
| Test | V01.Q09 | 0.5 h |
| End test | V01 end test, part 1 (§4) | 1.0 h |

**Supplementary:** R-0104 problem sets on columns; R-0102 lectures on eccentrically loaded columns.

### Worked problem V01.WP09.1 — A canopy column: Euler vs. EN vs. BS

**Situation.** A pin-ended CHS 114.3 × 5.0 column, 4.0 m long, hot-finished, S355. (A pinned canopy column braced at the top, for example.)

**Section.** $A = \frac{\pi}{4}(114.3^2 - 104.3^2) = 1717\ \text{mm}^2$, $I = \frac{\pi}{64}(114.3^4 - 104.3^4) = 2.569\times10^6\ \text{mm}^4$, $i = \sqrt{I/A} = 38.7$ mm.

**Euler (elastic, perfect column), E = 210 kN/mm², $L_{cr}$ = 4000 mm:**
$$N_{cr} = \frac{\pi^2 \times 210\,000 \times 2.569\times10^6}{4000^2} = 332.8\ \text{kN}$$

**EN 1993-1-1 §6.3.1:**
$$\lambda = L_{cr}/i = 103.4,\qquad \lambda_1 = \pi\sqrt{E/f_y} = 76.4,\qquad \bar{\lambda} = \lambda/\lambda_1 = 1.353$$
Hot-finished CHS → curve a, α = 0.21 (Tables 6.1 and 6.2).
$$\Phi = 0.5\left[1 + 0.21(1.353 - 0.2) + 1.353^2\right] = 1.537$$
$$\chi = \frac{1}{\Phi + \sqrt{\Phi^2 - \bar{\lambda}^2}} = \frac{1}{1.537 + 0.728} = 0.442$$
$$N_{b,Rd} = \frac{0.442 \times 1717 \times 355}{1.0} = 269.1\ \text{kN}\quad(\gamma_{M1} = 1.0,\ \text{recommended value; check the Kenya NA})$$

**BS 5950-1 §4.7 / Annex C (E = 205 kN/mm², $p_y$ = 355 N/mm² for t ≤ 16 mm, strut curve a, Robertson constant a = 2.0):**
$$\lambda = 103.4,\qquad \lambda_0 = 0.2\sqrt{\pi^2 E/p_y} = 15.1,\qquad \eta = \frac{2.0(103.4 - 15.1)}{1000} = 0.177$$
$$p_E = \frac{\pi^2 E}{\lambda^2} = 189.2\ \text{N/mm}^2,\qquad \phi = \frac{p_y + (\eta + 1)p_E}{2} = 288.8\ \text{N/mm}^2$$
$$p_c = \frac{p_E\,p_y}{\phi + \sqrt{\phi^2 - p_E\,p_y}} = \frac{189.2 \times 355}{288.8 + 127.5} = 161.4\ \text{N/mm}^2,\qquad P_c = 161.4 \times 1717 = 277.1\ \text{kN}$$

**Compare.**

| Quantity | Value | Ratio to squash load $Af_y$ = 609.5 kN |
|---|---:|---:|
| Euler $N_{cr}$ | 332.8 kN | 0.55 |
| EN $N_{b,Rd}$ | 269.1 kN | 0.44 |
| BS $P_c$ | 277.1 kN | 0.45 |

This column is slender. Buckling, not material strength, controls, and imperfections cut capacity a further ~19% below Euler. EN and BS agree within 3%. The differences come from E (210 vs 205), the curve formulation, and the Perry factor. **Note:** BS capacities are compared against factored loads using BS 5950 load factors, and EN capacities against EN 1990 combinations. Compare resistances like this only to understand the codes, never to mix them in one design (V00 §5(b)).

**Your turn (V01.WP09.1-YT).** A CHS 139.7 × 5.0 column, pin-ended, 4.5 m, S355 hot-finished. Find $N_{cr}$, $\bar{\lambda}$, χ, $N_{b,Rd}$ and the BS $P_c$. *(Answer in §6.)*

**Software verification (VER-V01.M09).** Stated tool: a NumPy finite-difference eigenvalue solver (your code). Discretise $EI\,y'' + Py = 0$ with n segments and take the smallest eigenvalue of $-EI\,D_2$. My run on 2026-10-03: n = 10 gave 330.1 kN (−0.8%), n = 20 gave 332.1 kN (−0.2%), n = 50 gave 332.7 kN (−0.03%), against exact 332.8 kN. It converges as the mesh refines, which is the core idea of V12. Tolerance ≤1% at n ≥ 20.

**Thread task.** **T3:** `strlib/buckling.py` with `ncr()`, `chi_en(lambda_bar, curve)` and `pc_bs(lam, py, curve)`, tested against this WP and the "Your turn".

**Self-check quiz V01.Q09**
1. State the Euler critical load and list its four main assumptions.
2. What is the theoretical effective-length factor for a column fixed at both ends, and for a cantilever column?
3. Give three reasons real columns fail below $N_{cr}$.
4. Define the non-dimensional slenderness $\bar{\lambda}$ in terms of A, $f_y$ and $N_{cr}$.
5. Which EN buckling curve applies to a hot-finished CHS in S355?
6. What Robertson constant does BS 5950-1 Annex C use for strut curve a?
7. What is χ when $\bar{\lambda} \le 0.2$, and why?
8. If WP09.1's column were 8 m long instead of 4 m, what would happen to $N_{cr}$?

**Field notes (Kenya).** Slender tubular columns on canopies and carports, and temporary props under slab formwork, are classic buckling risks. Props that are too slender, unbraced or out of plumb have a long history in construction collapses worldwide; V17.T05 tracks enforcement responses in Kenya **(judgement; incident data in V17)**.

**Portfolio output.** `buckling.py` with tests; a one-page EN vs BS comparison sheet (good interview material).
**Done when:** WP and "Your turn" match; Q09 ≥70%; VER-V01.M09 recorded.

---

## [V01.M10] Maths toolkit: linear algebra, calculus and numerical methods
**Tags:** Phase 1 | Maths | T3
**Prerequisites:** M03 (truss solver), M08
**Time:** 5 h (W09)

**Learning outcomes**
1. Set up and solve small linear systems by Gaussian elimination and with `numpy.linalg.solve`, and explain why a stiffness matrix is symmetric and when it's singular.
2. Find roots of nonlinear equations by Newton–Raphson and judge convergence.
3. Integrate numerically (trapezoidal, Simpson's) and estimate the error.
4. Interpret eigenvalues and eigenvectors in structural terms (buckling loads and shapes, natural frequencies and modes).

**Code coverage:** none.

**Core path**

| Step | Resource and exact part | Time |
|---|---|---:|
| Watch | R-0105 chapters 6 (determinant), 7 (inverse matrices, column space, null space) and 14 (eigenvectors and eigenvalues) | 0.75 h |
| Read | R-0106 ch. 14 (linear algebra and systems of linear equations), ch. 19 (root finding: Newton–Raphson) and ch. 21 (numerical integration) | 1.25 h |
| Do | WP10.1 (three parts) and its "Your turn" | 1.5 h |
| Verify | NumPy / SciPy | 0.5 h |
| Test | V01.Q10 | 0.5 h |
| End test | V01 end test, part 2 (§4) | 0.5 h |

**Supplementary:** *The Structural Engineering Channel* podcast (Engineering Management Institute), Ep. 161, "How AI in Education Is Transforming Structural Engineering Learning and Careers" `[R-0111]`. US-based practice, so treat career specifics as context only; useful for thinking about how you use AI tools in this programme.

### Worked problem V01.WP10.1 — Three numerical tools you'll use for the next four years

**Part A: a spring-chain "stiffness matrix".** Three springs in series are fixed at the left end: k₁ = 100, k₂ = 200, k₃ = 150 kN/mm. Loads: 10 kN at node 2 and 20 kN at node 3.
$$\mathbf{K} = \begin{bmatrix} k_1+k_2 & -k_2 & 0 \\ -k_2 & k_2+k_3 & -k_3 \\ 0 & -k_3 & k_3 \end{bmatrix} = \begin{bmatrix} 300 & -200 & 0 \\ -200 & 350 & -150 \\ 0 & -150 & 150 \end{bmatrix},\qquad \mathbf{F} = \begin{Bmatrix} 0 \\ 10 \\ 20 \end{Bmatrix}$$
Elimination: row 1 gives $u_1 = \tfrac{2}{3}u_2$. Row 3 gives $u_3 = u_2 + 0.1333$. Substituting into row 2: $216.67u_2 - 150(u_2 + 0.1333) = 10$, so $u_2 = 0.450$ mm, $u_1 = 0.300$ mm, $u_3 = 0.583$ mm.
**Physical check:** spring 3 force = 150(0.583 − 0.450) = 20 kN ✓; spring 2 = 200(0.450 − 0.300) = 30 kN ✓; spring 1 = 100(0.300) = 30 kN = the support reaction ✓. **K** is symmetric (Maxwell–Betti reciprocity). Delete k₁ and **K** becomes singular: the chain is a mechanism, as in V00.D12.

**Part B: Newton–Raphson for a cracked RC section's neutral axis.** A 300 mm wide section with d = 450 mm, 3 bars of 16 mm ($A_s$ = 603 mm²) and modular ratio n = 15. Taking moments of area about the neutral axis gives
$$f(x) = \frac{b}{2}x^2 + nA_s x - nA_s d = 150x^2 + 9048x - 4\,071\,504 = 0,\qquad f'(x) = 300x + 9048$$
Starting from $x_0 = d/2 = 225$ mm: $x_1 = 152.4$, $x_2 = 137.95$, $x_3 = 137.332$, $x_4 = 137.331$ mm. Quadratic convergence: the number of correct digits roughly doubles each step. The exact quadratic root is 137.33 mm. You'll meet this equation again in V04 (cracked section properties).

**Part C: Simpson's rule for a load resultant.** A load varies as $w(x) = 2 + 0.5x^2$ kN/m over 0–4 m. Exact: $\int_0^4 w\,dx = 8 + 0.5(64/3) = 18.67$ kN. With h = 1 m:
- Simpson's rule: $\frac{1}{3}[2 + 4(2.5) + 2(4) + 4(6.5) + 10] = 18.67$ kN. Exact, because Simpson's rule integrates cubics exactly.
- Trapezoidal rule: $1.0[1 + 2.5 + 4 + 6.5 + 5] = 19.0$ kN (+1.8%).

**Your turn (V01.WP10.1-YT).** Springs k₁ = 150, k₂ = 100, k₃ = 200 kN/mm, loads 5 kN at node 1 and 15 kN at node 3. Find $u_1$, $u_2$, $u_3$ by hand, then check with NumPy. *(Answer in §6.)*

**Software verification (VER-V01.M10).** Stated tools: `numpy.linalg.solve` for Part A, `scipy.optimize.newton` for Part B, `scipy.integrate.simpson` for Part C. Expect exact agreement to rounding. Also print `numpy.linalg.cond(K)` and note what a large condition number would mean (Q10.7).

**Thread task.** **T3:** extend `truss.py` (M03) so it assembles **K** from member stiffnesses instead of joint equilibrium. That's the bridge into V02.M08 (direct stiffness method).

**Self-check quiz V01.Q10**
1. What does a singular stiffness matrix tell you about the structure?
2. Why do solvers factorise **K** rather than compute $\mathbf{K}^{-1}$?
3. Write the Newton–Raphson update formula.
4. Give two situations where Newton–Raphson fails or converges slowly.
5. Up to what polynomial degree is Simpson's rule exact?
6. In a buckling eigenproblem, what do the eigenvalues and eigenvectors represent?
7. What does a large condition number warn you about in a structural model?
8. Which NumPy/SciPy functions solve $\mathbf{K}\mathbf{u} = \mathbf{F}$, and which is preferable for a symmetric positive-definite **K**?

**Field notes.** Most small-practice calculations in Kenya live in spreadsheets **(judgement)**. Spreadsheets aren't wrong, but they're hard to test and easy to break silently. The habit you're building (code with tests checked against hand calcs and independent software) is what makes your calcs defensible at the professional interview and later as a product (goal 4).

**Portfolio output.** Stiffness-assembly version of `truss.py`; V01 end test result.
**Done when:** WP and "Your turn" match; Q10 ≥70%; VER-V01.M10 recorded; V01 end test ≥70%.

---

## 4. V01 end test

**When:** W09 (1.5 h across M09 and M10). Closed book, but you may use the formula sheet you built yourself (Appendix A). **Pass mark: ≥70% (each item scored 0, ½ or 1).** Log it in the tracker as quiz `V01.END`.

1. A simply supported beam spans 8 m, with point loads of 20 kN at 2 m and 30 kN at 5 m from A. Find the reactions and the maximum moment.
2. A rectangular hollow section, 200 mm wide × 300 mm deep outside, with 10 mm walls. Find $I_x$ and $Z_x$.
3. That section carries M = 60 kNm. What is the extreme-fibre bending stress?
4. At a point, σx = 60, σy = −20, τxy = 30 N/mm². Find the principal stresses and the maximum in-plane shear stress.
5. A 2.5 m cantilever carries a UDL of 6 kN/m, with EI = 5000 kNm². Find the tip deflection.
6. A pin-ended column 3.5 m long has I = 1.2 × 10⁷ mm⁴ and E = 210 kN/mm². Find $N_{cr}$. What would it be with both ends fixed (theoretical)?
7. Solve $\begin{bmatrix}5 & -2\\-2 & 4\end{bmatrix}\mathbf{u} = \begin{Bmatrix}3\\6\end{Bmatrix}$ and check your answer by substitution.

**If you score below 70%:** don't start V02. Spend the W12 light-week buffer on the modules behind the items you missed, then re-sit the missed items.

---

## 5. Trends Watch

> **Trends Watch — V01 (as of 2026-10-03)**
> - **Code-based calc sheets replacing spreadsheets** (V17.T09): tools like `handcalcs` and Calcpad render readable, checkable calcs from code. *Why it matters:* the T3 thread is building exactly this habit, and it's the core of goal 4.
> - **AI tutors and assistants for learning mechanics** (V17.T10): useful for explanations and generating practice problems, but they still produce confident arithmetic and sign errors. *Why it matters:* keep the hand-calc + independent-software verification rule; never take an AI-produced number into a calc unchecked.
> - **Open, interactive engineering textbooks** (proposed for V17): free texts like R-0101 with built-in checked exercises are maturing. *Why it matters:* they lower the cost of the free-first approach and work offline.

---

## 6. Answer key

Open each block only after you've attempted the questions.

### 6.1 Quizzes

<details><summary><b>V01.Q01</b> Units, vectors and FBDs</summary>

1. 28 × 9.81 / 1000 = **0.275 kN**.
2. 2.5 kN/m² × 3.0 m = **7.5 kN/m**.
3. √(3² + 4²) = **5 kN** at tan⁻¹(4/3) = **53.1°** from +x.
4. **i × j = k**; **j × i = −k** (the cross product is anticommutative).
5. 10 × 2 = **20 kNm, clockwise**.
6. **False.** An FBD shows only the external forces on the isolated body. Internal forces appear only when you cut the body, and then they become external to the part you keep.
7. Wind acts high up, so its lever arm about the base is long, while the self-weight of a light PV table is small and acts close to the post axis. Overturning is therefore wind-driven.
8. 0.2 m × 25 kN/m³ = **5.0 kPa**.
</details>

<details><summary><b>V01.Q02</b> Equilibrium, supports and determinacy</summary>

1. Pin **2**, roller **1**, fixed **3**.
2. $R_A$ = **2P/3**, $R_B$ = **P/3**.
3. **3** in general (6 reactions − 3 equations). Under purely transverse loading with axial effects ignored, it's often treated as 2.
4. The apex hinge adds one equation (M = 0 at the hinge), giving 4 equations for 4 unknowns.
5. r = 4 → **indeterminate to the 1st degree**.
6. Any of: a steel column base plate with four bolts; a beam bearing on masonry with a padstone; a fin-plate or end-plate beam connection.
7. $R_B$ = (256 + 240)/6 = 82.67 kN, so **$R_A$ = 11.33 kN**. $R_A$ turns negative once the tip load exceeds **64 kN**. A negative reaction means support A must hold the beam *down* (uplift), so it needs anchorage or holding-down bolts.
8. Take moments about a second point (e.g. $\sum M_B = 0$) or re-check $\sum F_y = 0$ with the values found.
</details>

<details><summary><b>V01.Q03</b> Trusses and frames</summary>

1. m + r = 14 = 2j → **determinate** (if the arrangement is stable).
2. **Both are zero.**
3. The third (non-collinear) member is **zero**; the collinear pair carry **equal** forces.
4. When you need only a few member forces in the middle of a truss. One cut and one moment equation gives each force directly.
5. Pratt: **diagonals in tension**, verticals in compression. Howe: **diagonals in compression**, verticals in tension.
6. Members are idealised as two-force (axial-only) members with pinned ends. Purlins between nodes **bend the chord**, which must then be checked for combined axial force and bending.
7. The **end post L0–U1, at 31.8 kN compression**. It carries the full support reaction up into the top chord, where the panel shear is largest.
8. A truss member is a two-force member (axial force only). A frame member carries three or more forces or loads along its length, so it develops **shear and bending**.
</details>

<details><summary><b>V01.Q04</b> Distributed loads, centroids and section properties</summary>

1. $I = I_c + Ad^2$, where $I_c$ is about the parallel centroidal axis and d is the distance between the axes.
2. 300 × 600³ / 12 = **5.4 × 10⁹ mm⁴**.
3. $W_{el}$ limits stress to yield at the extreme fibre only (linear distribution). $W_{pl}$ assumes the whole section has yielded (uniform stress blocks), so it uses the material near the neutral axis fully. Hence $W_{pl} \ge W_{el}$.
4. Magnitude **wL/2**, acting **L/3 from the peak end** (2L/3 from the zero end).
5. $i = \sqrt{8\times10^7/6000}$ = **115.5 mm**.
6. **Z** (elastic modulus) and **S** (plastic modulus).
7. In a symmetric section the neutral axis is at mid-depth, so both extreme fibres are the same distance away. In a tee the neutral axis sits near the flange, so the distances (and hence Z) differ.
8. **8 times** (I ∝ d³).
</details>

<details><summary><b>V01.Q05</b> Axial, shear and moment diagrams</summary>

1. **The shear force** (dM/dx = V).
2. **Where the shear force crosses zero.**
3. The SFD **jumps** by P; the BMD has a **kink** (a change of slope).
4. **PL/4.**
5. The point where M changes sign, so the tension face switches. Bars must extend beyond it with adequate anchorage, so curtailment and laps depend on where it is.
6. Support moment **wL²/2** (hogging); support shear **wL**.
7. The reaction is a concentrated upward force, so the shear jumps by exactly its magnitude.
8. Sagging (concave up) from A to x ≈ 4.33 m, then hogging (concave down) to the tip. The span dips between A and B, and the overhang tip deflects downward beyond B.
</details>

<details><summary><b>V01.Q06</b> Stress, strain and materials</summary>

1. ε = ΔL/L. It's a ratio of two lengths, so it has no units.
2. ε = 100/200 000 = **5 × 10⁻⁴** (0.05%).
3. Steel ≈ **0.3**; uncracked concrete ≈ **0.2**.
4. Free thermal expansion causes no stress; stress appears only when the movement is prevented. Unrestrained bar → **zero stress**.
5. Perfect bond means equal strains. Since σ = Eε for each material, $\sigma_s/\sigma_c = E_s/E_c = n$.
6. **BS 5950-1 uses 205 kN/mm²; EN 1993-1-1 uses 210 kN/mm².**
7. Mild steel: linear to yield, a yield plateau, then strain hardening and necking. Concrete in compression: a nonlinear rise to a peak near 0.2% strain, then softening to crushing around 0.35%, with no plateau. **Steel has the plateau.**
8. Low E means large deflections and low buckling resistance (N_cr ∝ E) in slender rails and purlins. Strength rarely governs before stiffness does.
</details>

<details><summary><b>V01.Q07</b> Bending, shear, combined stress</summary>

1. Zero at the **neutral axis**; largest at the **extreme fibres**.
2. Q = 0 at the extreme fibre (there's no area beyond it), so τ = 0.
3. **1.5 V/A.**
4. The **principal stresses** (on planes with zero shear).
5. σ₁ = **+τ**, σ₂ = **−τ**, on planes at **45°** to the planes of pure shear.
6. $\sigma_{vm} = \sqrt{\sigma^2 + 3\tau^2}$.
7. Under the von Mises criterion, a material in pure shear yields at $f_y/\sqrt{3}$ ≈ 0.577 $f_y$. BS 5950 rounds this to 0.6 $p_y$.
8. **Over interior supports of continuous beams**, at the web–flange junction, where high moment and high shear coincide.
</details>

<details><summary><b>V01.Q08</b> Torsion and deflection</summary>

1. **5wL⁴/(384EI).**
2. **PL³/(3EI).**
3. A load at x = a doesn't affect the bending moment to its left, so its term must vanish for x < a.
4. **Two:** y(0) = 0 and y(L) = 0.
5. A closed section carries torque by shear flow around its whole perimeter (J grows with the square of the enclosed area). A thin open section resists only through its thin walls (J ≈ Σbt³/3), which is far smaller.
6. **16 times** (∝ L⁴).
7. BS 5950-1 **§2.5.2, Table 8**. Under the Eurocodes, **EN 1990 Annex A1 §A1.4** leaves the limits to the National Annex or project specification.
8. The point load sits left of centre (at 2 m), so the deflected shape is skewed toward it. The maximum falls between the load and midspan.
</details>

<details><summary><b>V01.Q09</b> Buckling</summary>

1. $N_{cr} = \pi^2EI/L_{cr}^2$. Assumes a perfectly straight member, load exactly along the axis, linear-elastic material, and small deflections (plus ideal end conditions).
2. Fixed–fixed: **0.5** (theoretical). Cantilever: **2.0**.
3. Any three of: initial out-of-straightness; load eccentricity; residual stresses from rolling or welding; material yielding before elastic buckling; imperfect end restraint.
4. $\bar{\lambda} = \sqrt{Af_y/N_{cr}}$.
5. **Curve a** (EN 1993-1-1 Table 6.2).
6. **a = 2.0.**
7. **χ = 1.0**. The column is stocky enough that yielding, not buckling, governs.
8. It drops to **one quarter** (≈ 83 kN), because N_cr ∝ 1/L².
</details>

<details><summary><b>V01.Q10</b> Maths toolkit</summary>

1. The structure is a **mechanism**, or not adequately restrained (rigid-body motion is possible).
2. Factorisation is faster and more accurate, and it preserves the sparsity and symmetry of **K**. Forming the inverse wastes work and amplifies rounding error.
3. $x_{k+1} = x_k - f(x_k)/f'(x_k)$.
4. Any two of: $f'(x) \approx 0$ near the iterate; a poor starting point; multiple or repeated roots; discontinuous or noisy functions.
5. Polynomials up to **degree 3**.
6. Eigenvalues are the **critical (buckling) loads**; eigenvectors are the **buckled mode shapes**. (In dynamics: natural frequencies and mode shapes.)
7. The model is **ill-conditioned**: results are sensitive to rounding. Common causes are very stiff elements next to very flexible ones, or near-mechanisms.
8. `numpy.linalg.solve`, or `scipy.linalg.solve(..., assume_a="pos")` / `cho_factor`–`cho_solve` for a symmetric positive-definite **K** (Cholesky is preferable).
</details>

### 6.2 "Your turn" solutions

<details><summary><b>WP01.1-YT</b></summary>

**R** = (5.0, 0, −3.6) kN, |R| = **6.16 kN**, at **35.8°** below horizontal. **M** = 5.0 × 3.0 + 3.6 × 0.2 = 15.00 + 0.72 = **15.72 kNm** about +y.
</details>

<details><summary><b>WP02.1-YT</b></summary>

UDL total 65 kN at 3.25 m. $R_B$ = (65 × 3.25 + 8 × 6.5)/5 = (211.25 + 52)/5 = **52.65 kN**; $R_A$ = 73 − 52.65 = **20.35 kN**.
</details>

<details><summary><b>WP03.1-YT</b></summary>

Reactions 70/2 = 35 kN each. U1–U2: (35 × 6 − 20 × 3)/3 = **50.0 kN compression**. L1–L2: 35 × 3/3 = **35.0 kN tension**. U1–L2: (35 − 20)/0.7071 = **21.21 kN tension**. U2–L2: **20.0 kN compression** (joint U2). Check at L2: 2 × 15 (diagonals, up) − 20 (vertical, down) − 10 (hanging load) = 0 ✓.
</details>

<details><summary><b>WP04.1-YT</b></summary>

A = 4000 + 3600 = **7600 mm²**. ȳ = (4000 × 308 + 3600 × 150)/7600 = **233.2 mm** from the bottom (82.8 mm from the top). $I_x$ = 250(16)³/12 + 4000(74.8)² + 12(300)³/12 + 3600(83.2)² = **7.44 × 10⁷ mm⁴**. $Z_{top}$ = **8.98 × 10⁵ mm³**; $Z_{bot}$ = **3.19 × 10⁵ mm³**.
</details>

<details><summary><b>WP05.1-YT</b></summary>

V = 0 at x = 20.35/10 = **2.035 m**; $M_{max}$ = $R_A^2/(2w)$ = **20.71 kNm** (sagging). $M_B$ = −(8 × 1.5 + 10 × 1.5²/2) = **−23.25 kNm** (hogging). Contraflexure where 20.35x − 5x² = 0 → **x = 4.07 m**. Shear just left of B: 20.35 − 10 × 5 = −29.65 kN; just right of B: −29.65 + 52.65 = **+23.0 kN** = 8 + 10 × 1.5 ✓.
</details>

<details><summary><b>WP06.1-YT</b></summary>

A = π(12)² = 452.4 mm². σ = 60 000/452.4 = **132.6 N/mm²**. δ = 132.6 × 5000/210 000 = **3.16 mm**. Restrained thermal stress = 210 000 × 12×10⁻⁶ × 25 = **63.0 N/mm²** (compression).
</details>

<details><summary><b>WP07.1-YT</b></summary>

σ_max = 150×10⁶ × 200 / 2.1615×10⁸ = **138.8 N/mm²**. τ_NA = 100 000 × 606 976 / (2.1615×10⁸ × 8) = **35.1 N/mm²**. Junction: σ = **130.5**, τ = **26.9** N/mm². Mohr: centre 65.2, R = 70.6 → σ₁ = **135.8**, σ₂ = **−5.3**, τ_max = 70.6 N/mm². σ_vm = **138.6 N/mm²**.
</details>

<details><summary><b>WP08.1-YT</b></summary>

$R_A$ = 20 × 3.5/5 + 4 × 5/2 = **24.0 kN**. $EI\,y = 4x^3 - \tfrac{20}{6}\langle x-1.5\rangle^3 - \tfrac{4}{24}x^4 + C_1x$, with y(5) = 0 → **C₁ = −50.58**. Midspan: y(2.5) = **−4.39 mm**. Maximum **4.41 mm at x ≈ 2.36 m**.
</details>

<details><summary><b>WP09.1-YT</b></summary>

A = **2116 mm²**, I = **4.805 × 10⁶ mm⁴**, i = **47.7 mm**. $N_{cr}$ = π² × 210 000 × 4.805×10⁶ / 4500² = **491.8 kN**. λ = 94.4, $\bar{\lambda}$ = **1.236**, Φ = 1.373, **χ = 0.508**, $N_{b,Rd}$ = 0.508 × 2116 × 355 / 1.0 = **381.5 kN**. BS 5950: $p_c$ = **186.9 N/mm²**, $P_c$ = **395.4 kN** (+3.7% vs EN).
</details>

<details><summary><b>WP10.1-YT</b></summary>

**K** = [[250, −100, 0], [−100, 300, −200], [0, −200, 200]], **F** = (5, 0, 15). Solution: $u_1$ = **0.133 mm**, $u_2$ = **0.283 mm**, $u_3$ = **0.358 mm**. Check: spring 3 = 200 × 0.075 = 15 kN ✓; spring 2 = 100 × 0.150 = 15 kN ✓; spring 1 = 150 × 0.133 = 20 kN = 5 + 15 ✓.
</details>

### 6.3 REV-01 (light week W06): retrieval set for M01–M05

First re-attempt every quiz item you got wrong in Q01–Q05. Then answer these eight new mixed items without notes (target ≥75%):

1. A 1.5-tonne steel beam: weight in kN?
2. An 8 kN force acts at 45° to the horizontal at the end of a 2 m horizontal arm. What is its moment about the arm's root?
3. Degree of indeterminacy of a portal frame with both bases fixed?
4. An unloaded joint has two non-collinear members. Their forces?
5. Centroid of an equal angle 100 × 100 × 10 mm, measured from the outer corner?
6. Simply supported beam, span 7 m, UDL 6 kN/m: $M_{max}$ and $V_{max}$?
7. A triangular load with a 9 kN/m peak over 6 m: resultant and its position?
8. A 3 m cantilever carries a 10 kN end load plus 4 kN/m: support moment?

<details><summary><b>REV-01 answers</b></summary>

1. 1500 × 9.81/1000 = **14.7 kN**. 2. Perpendicular component 8 sin 45° = 5.66 kN × 2 m = **11.3 kNm**. 3. **3**. 4. **Both zero**. 5. Legs 100 × 10 and 90 × 10: x̄ = ȳ = (1000 × 50 + 900 × 5)/1900 = **28.7 mm**. 6. $M_{max}$ = 6 × 49/8 = **36.75 kNm**; $V_{max}$ = **21 kN**. 7. **27 kN**, acting **2 m from the 9 kN/m end**. 8. 10 × 3 + 4 × 9/2 = **48 kNm** (hogging).
</details>

### 6.4 V01 end test answers

<details><summary><b>V01.END</b></summary>

1. $R_A$ = (20 × 6 + 30 × 3)/8 = **26.25 kN**; $R_B$ = **23.75 kN**. M at 2 m = 52.5 kNm; at 5 m = 23.75 × 3 = **71.25 kNm (maximum)**.
2. $I_x$ = (200 × 300³ − 180 × 280³)/12 = **1.207 × 10⁸ mm⁴**; $Z_x$ = I/150 = **8.05 × 10⁵ mm³**.
3. σ = 60×10⁶/8.05×10⁵ = **74.6 N/mm²**.
4. Centre 20, R = √(40² + 30²) = 50 → σ₁ = **70**, σ₂ = **−30**, τ_max = **50 N/mm²**.
5. δ = wL⁴/(8EI) = 6 × 2.5⁴/(8 × 5000) = 0.00586 m = **5.86 mm**.
6. $N_{cr}$ = π² × 210 000 × 1.2×10⁷ / 3500² = **2030 kN**. Fixed–fixed (L_cr = 0.5L): **4 × = 8121 kN** (theoretical; practical design uses larger effective-length factors).
7. det = 16; **u = (1.5, 2.25)**. Check: 5(1.5) − 2(2.25) = 3 ✓; −2(1.5) + 4(2.25) = 6 ✓.
</details>

---

## Appendix A — Formula sheet you build yourself

Build this on one A4 sheet (two sides) as you go, in your own handwriting or in Calcpad. Writing it is part of the learning; it's also the only aid allowed in the end test and gate exams. Minimum contents:

- **M01–M02:** unit conversions; vector components; $\mathbf{M} = \mathbf{r}\times\mathbf{F}$; equilibrium equations; determinacy test for beams/frames and trusses.
- **M03:** method of joints and sections; zero-force member rules.
- **M04:** centroid of composites; parallel-axis theorem; I, Z, S for rectangle, I-section and tee; resultants of uniform, triangular and trapezoidal loads.
- **M05:** dV/dx = −w, dM/dx = V; standard $M_{max}$ results (PL/4, wL²/8, wL²/2).
- **M06:** σ = N/A, ε = δ/L, σ = Eε, ν; thermal strain; modular-ratio method; E values in EN vs BS.
- **M07:** σ = My/I, τ = VQ/(It), 1.5V/A; plane-stress transformation; principal stresses; von Mises.
- **M08:** τ = Tr/J, θ = TL/(GJ); Macaulay set-up; standard deflections (5wL⁴/384EI, PL³/48EI, PL³/3EI, wL⁴/8EI).
- **M09:** $N_{cr}$; effective-length factors; $\bar{\lambda}$, Φ, χ (EN); λ₀, η, $p_E$, φ, $p_c$ (BS).
- **M10:** Gaussian elimination steps; Newton–Raphson; trapezoidal and Simpson's rules.

---

## Appendix B — Resource index (V01)

Resource IDs for this volume use the R-01xx block (V00 used R-00xx), so no ID is ever reused. All links were checked live on **2026-10-03** unless marked.

| ID | Title | Provider | Type | Cost | Tier | URL |
|---|---|---|---|---|---|---|
| R-0101 | *Engineering Statics: Open and Interactive* (2020) | D. W. Baker & W. Haynes | Open textbook (web + PDF), CC BY-NC-SA | Free | A | https://engineeringstatics.org · PDF: https://engineeringstatics.org/pdf/statics.pdf |
| R-0102 | *Strength of Materials* (course 105105108) | NPTEL / IIT Kharagpur, Prof. S. K. Bhattacharyya | Video course | Free to enrol and learn; certificate exam optional (paid) | A | https://onlinecourses.nptel.ac.in/noc23_ce80/preview |
| R-0103 | *Engineering Mechanics* (course 112106286) | NPTEL / IIT Madras, Prof. K. Ramesh | Video course | Free | A | https://nptel.ac.in/courses/112106286 (seen listed as a prerequisite on IIT Madras's Strength of Materials page; course page not opened `[VERIFY]`) |
| R-0104 | *2.001 Mechanics & Materials I* (Fall 2006) | MIT OpenCourseWare | Lecture notes + 11 problem sets | Free | A | https://ocw.mit.edu/courses/2-001-mechanics-materials-i-fall-2006/ |
| R-0105 | *Essence of linear algebra* | 3Blue1Brown (G. Sanderson) | Video series | Free | B | https://www.3blue1brown.com/lessons/eola-preview |
| R-0106 | *Python Programming and Numerical Methods* (2020) | Q. Kong, T. Siauw, A. Bayen (Elsevier) | Book | Free online edition `[VERIFY URL]`; print/eBook paid `[VERIFY price]` | A | https://bayen.berkeley.edu/python-programming-and-numerical-methods |
| R-0107 | anaStruct 1.7.0, PyNiteFEA 3.2.0, sectionproperties 3.10.2, handcalcs 1.11.0 | PyPI | Python libraries | Free | B | https://pypi.org (versions as listed in V00 R-0030) |
| R-0108 | Calcpad | Proektsoft | Calc software | Free | B | https://calcpad.eu (V00 R-0025) |
| R-0109 | Hibbeler, *Mechanics of Materials* (SI) or Gere & Goodno, *Mechanics of Materials* (SI) | Pearson / Cengage | Textbook (optional) | Paid, price `[VERIFY]` | A | — |
| R-0110 | MIT 2.001 Spring 2006 course home page (textbook: Hibbeler, 6th ed.) | MIT (archived course site) | Course page | — | C | https://stuff.mit.edu/afs/sipb/project/course-search/backup-20080314-0222/web_scripts/search/urls/stellar.sp06.2.001.html |
| R-0111 | *The Structural Engineering Channel* podcast (Engineering Management Institute) | M. Picardal and co-hosts | Podcast | Free | B | https://engineeringmanagementinstitute.org/tag/the-structural-engineering-channel |

---

## Appendix C — Handoff block

```
HANDOFF: V01
Covered: V01.M01–M10 (70 h, W02–W09): units/vectors/FBDs; equilibrium, supports, determinacy;
  trusses (joints, sections, zero-force members); centroids and section properties (I, Z, S, i);
  SFD/BMD; stress/strain/materials incl. EN vs BS constants (E 210 vs 205); bending and shear
  stress, Mohr's circle, von Mises; torsion and deflection (Macaulay, moment-area); buckling
  (Euler; EN 1993-1-1 §6.3.1 χ vs BS 5950-1 Annex C Perry–Robertson); linear systems,
  Newton–Raphson, numerical integration, eigenproblems. 10 worked problems with "Your turn"
  variants; 10 quizzes (80 items); REV-01; V01 end test; software verification records
  VER-V01.M01–M10, nine of them run and matched on 2026-10-03 (anaStruct, sectionproperties,
  PyNite, NumPy).
Deferred / open items:
  1. NPTEL lecture-number mapping for R-0102 and R-0103, and the topic mapping of MIT 2.001
     problem sets (R-0104), to be confirmed when you enrol/download.
  2. Kenya NA value of γM1 (EN 1993-1-1) and Kenya NA deflection limits — V03.M02.
  3. Local reinforcement grade conventions and mill certificates — V04.
Links marked [VERIFY]: R-0103 course page; R-0106 free online URL and price; R-0109 prices;
  BS clause refs (BS 8110-1 §2.4.2.3, BS 8110-2 §7.2, BS 8118-1, BS 5268-2 strength
  classes, BS 648 status, BS 5950-1 §2.1.2, BS torsion guidance); EN 1999-1-1 §3.2.5.
Thread status (T1–T5):
  T1 AutoCAD — layer standard, support-symbol blocks, truss GA, annotation scales and
     dimension styles, annotated column section.
  T2 MIDAS — not started (vendor tutorials in V02 W19; first model V02.M10).
  T3 Python — strlib: units, truss (joint method + stiffness assembly), sections, diagrams,
     axial, stress (principal/von Mises), deflection (Macaulay), buckling (EN χ, BS pc),
     all with pytest tests against hand calcs.
  T4 EBK portfolio — GE application due W05; IEK Graduate application due W09; CPD log
     entries for V01 study.
  T5 Field — section spotting (W04).
Prerequisites confirmed for next volume: V01 end test ≥70%; strlib.truss assembles K;
  comfortable with Macaulay deflections (V02.M02 compares energy methods against them).
Next: V02, starting at module V02.M01
```
