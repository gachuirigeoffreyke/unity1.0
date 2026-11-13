# FSE-C11a · Computer Science Foundations, Part A (C11.M01–M04, M10)

**Full-Stack Development & Engineering Playbook · TSW Track 1**

| Field | Value |
|---|---|
| Strand | Craft (C). The fixed weekly **Mode 0** block (V00 §1.3, R7) |
| Phase | Continuous. Part A covers W1–W29 (2 Nov 2026 – 23 May 2027): M01 W1–W7, M02 W8–W15, M03 W16–W22, M04 W23–W29. M10 runs every week |
| Version / date | 1.1 · 2026-10-26 (re-dated to V00 v1.3; first issue 1.0 · 2026-10-08) |
| Versions targeted | Python 3.14 (tested on 3.14.4); pytest 9.1.1 |
| Prerequisites | C01.M03 (learning system); C02.M01, from W1 Tuesday |
| Hour budget | 43.5 h in W1–W29 (29 blocks × 1.5 h): new material in M01–M04 (25 h) and spaced reps in M10 (18.5 h) |
| Applied in | P01.S04, P02.S03, P02 review gates, P03, P04 |
| Depth | Working-engineer depth, not interview grinding (V00 §5(g)) |
| Part B | `FSE-C11b-CSFoundations.md` (M05–M09), due by the end of W28 (V00 §16.2) |

> **Re-dated 2026-10-26 (v1.1) to FSE-V00 v1.3, re-baseline B2.** Week 1 is now **Mon 2 – Sun 8 Nov 2026** (W*n* starts Mon 2 Nov + 7(*n*−1) days). Content is unchanged; only the calendar, week numbers and build cross-references moved.

Evidence labels follow V00 §0.1. All code is for learning.

## Contents

- §0 How the Mode 0 block works: format, calendar, rules, Kenyan context
- C11.M01 Complexity, arrays, strings, hash maps
- C11.M02 Stacks, queues, linked lists, recursion
- C11.M03 Sorting and searching
- C11.M04 Trees, binary search trees, heaps
- C11.M10 Rolling Mode 0 practice reps
- Trends Watch · Answer key · Resource index · YAML manifest · Handoff

---

## 0. How the Mode 0 block works

### 0.1 The block

**Saturday, 11:30–13:00** (V00 §1.4; the weekly retro follows at 13:00).

| Minutes | What | Mode |
|---|---|---|
| 0–5 | **Retrieve:** write down, from memory, last week's idea and one problem you solved | 0 |
| 5–60 | **New:** read the assigned part, then solve the drill or problem on paper *before* typing | 0 |
| 60–90 | **Reps (M10):** re-solve one earlier problem from your spaced queue, timed, without looking | 0 |

In light weeks (W6 7–13 Dec, W12 18–24 Jan, W18, W24) the whole block is reps. Light weeks carry no new content (V00 §1.4).

**Mode 0 rules for this block:**

- No AI: chat, completions and agents are all off. Use the C01.M01 Mode 0 workspace with `chat.disableAIFeatures`.
- Books, official docs, paper, Python and pytest are allowed.
- Write on paper first. Type only to check your answer.
- When you're stuck, use this ladder before reaching for a solution:
  1. Re-read the problem.
  2. Work a tiny example by hand.
  3. Write the brute-force version.
  4. Only then, look at a hint in the resource.
- Log the block in the tracker under its C11 item, with the drill IDs in the evidence field.

**Where the build tasks fit.** Each module's build task has an algorithmic core, which you write in this block (Mode 0). Wiring that core into the product happens on the build clock during the named sprint (Mode 1–2).

### 0.2 Calendar (matches the tracker's C11 item for each week)

| Weeks | Module | New material (h) | Reps (h) | Build task feeds |
|---|---|---|---|---|
| W1–W7 (W6 light) | C11.M01 Complexity, arrays, strings, hash maps | 6 | 4.5 | P01.S04 reconciliation (W2) and v1.0.1 |
| W8–W15 (W12 light) | C11.M02 Stacks, queues, linked lists, recursion | 7 | 5 | P02.S03 progress roll-up (W11–W12) |
| W16–W22 (W18 light) | C11.M03 Sorting and searching | 6 | 4.5 | P03 POS (W14–W23) |
| W23–W29 (W24 light) | C11.M04 Trees, BSTs, heaps | 6 | 4.5 | P04 Field/CRM (W24–W33) |
| Every week | C11.M10 Practice reps | — | 18.5 total | P02 review gates (complexity checklist) |

The order inside M02 puts **recursion first** (W8–W9), so it lands before P02.S03 uses it (W11–W12).

### 0.3 Versions

Python 3.14. Two standard-library details you'll use:

- `bisect` functions accept `key=` (since 3.10).
- `heapq` gained public max-heap functions in 3.14: `heapify_max`, `heappush_max`, `heappop_max`, `heapreplace_max` and `heappushpop_max` [V R-0130, R-0166].

### 0.4 Kenyan context

- **Data cost.** The MIT 6.006 lecture videos are about an hour each. Use the PDF notes by default, and download any video you need on home fibre.
- **Offline use.** The Erickson PDF and the MIT notes work offline. The Runestone book needs a connection for its interactive parts, so open its pages before you lose the connection.
- **Why it pays off for you.** Reconciliation, roll-ups and scheduling are your products' core logic. A slow matcher won't show at one chama's scale, but it will once the startup serves many groups (M01's measurement).

---

## [C11.M01] Complexity, arrays, strings, hash maps

**Tags:** Craft | Continuous (W1–W7) | Applied in P01.S04 | AI mode 0
**Prerequisites:** C02.M01 (from W1).
**Time:** 6–8 h. Planned: 6 h new material across 6 blocks, plus reps.
**Versions targeted:** Python 3.14.

**Learning outcomes**

1. **State** the Big-O cost of everyday Python operations (list, dict, set, string, deque) and **predict** which of two implementations scales.
2. **Use** hash maps to turn nested-loop matching into a single pass.
3. **Measure** rather than guess: time both versions at realistic sizes.
4. **Solve** the classic array and hash-map patterns (two-sum, frequency counting, anagram detection) unplugged.

**Core path** (one row per block)

| Week | Item | Exact part | Mode |
|---|---|---|---|
| W1 | Read: Miller & Ranum, *Problem Solving with Algorithms and Data Structures using Python* (3rd ed., Runestone) [R-0160] | Ch. 2 "Algorithm Analysis": 2.2 What Is Algorithm Analysis?, 2.3 Big O Notation | 0 |
| W2 | Same book [R-0160] | 2.4 "An Anagram Detection Example" (all four solutions; predict each one's Big-O before reading) | 0 |
| W3 | Read: Python docs, "Time complexity of operations on built-in types" [R-0161]; Runestone 2.5–2.7 (performance of lists and dictionaries) [R-0160] | The list, dict and set tables | 0 |
| W4 | Drill C11.D01.1 (complexity classification) and C11.D01.2 (two-sum on paper) | — | 0 |
| W5 | Build task BT01.1: write the core matcher, both versions, and measure them | — | 0 |
| W7 | MIT 6.006 Spring 2020, Lecture 4 "Hashing" notes [R-0162]; NeetCode "Arrays & Hashing", two easy problems [R-0163] | Notes PDF | 0 |

**Supplementary:** MIT 6.006 Lecture 1 "Introduction" and Lecture 2 "Data Structures" notes [R-0162] · Exercism practice exercises on dictionaries and strings [R-0133].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0160 | Miller & Ranum, *Problem Solving with Algorithms and Data Structures using Python*, 3rd ed. (Runestone, interactive, CC BY-NC-SA 4.0) | book | Free | A | Python throughout; runnable examples; gentle but rigorous |
| R-0161 | Python docs: time complexity of built-in types | doc | Free | A | The authoritative cost table for CPython |
| R-0162 | MIT 6.006 *Introduction to Algorithms*, Spring 2020 (OCW): lecture notes, recitations, problem sets with solutions, videos | course | Free | A | The canonical university course; the notes are compact |

### Unplugged drills (Mode 0)

**C11.D01.1 · What does it cost? (20 min).** Give the Big-O of each line, where `n = len(xs)` and `m = len(payments)`:

1. `x in xs`, where `xs` is a list.
2. `x in s`, where `s` is a set.
3. `for p in payments: for e in expected: …`
4. `sorted(xs)`
5. `while xs: xs.pop(0)` (all iterations together)
6. `while d: d.popleft()`, where `d` is a `deque` (all iterations together)
7. `s = ""; for part in parts: s += part` versus `"".join(parts)`
8. `len(xs)`

**C11.D01.2 · Two-sum on paper (15 min).** Given the amounts `[500, 1200, 300, 700]` and the target `1000`, find the index pair in **one pass**. Write the function, state its Big-O, and explain what you'd store in the dict.

### Build task C11.BT01.1 · Reconciliation matcher, measured (applied in P01.S04)

**Spec.**

- `expected` and `received` are lists of `(phone, amount, ref)`.
- Write `match_naive` (nested loops) and `match_indexed`. The indexed version builds a dict from `(phone, amount)` to a FIFO `deque` of receipts, so duplicate payments are matched in order.
- Prove that both return identical pairs on random data.
- Time both at 360 rows (one chama's year), 2,000, 5,000 and 20,000 rows.

**Reference measurements** (test machine, Python 3.14.4; your laptop will differ, but the ratios won't):

| Rows | Naive | Indexed | Ratio |
|---:|---:|---:|---:|
| 360 | 0.003 s | 0.0005 s | 6× |
| 2,000 | 0.109 s | 0.003 s | 36× |
| 5,000 | 0.882 s | 0.008 s | 106× |
| 20,000 | about 14 s (projected) | 0.040 s | — |

**Acceptance criteria:**

- Identical output on random data, with a test.
- At 20,000 rows, the indexed version takes under 0.2 s on your laptop.
- A one-paragraph note in the P01 repository: which version Chama uses, and at what scale the choice matters. At one chama's scale, either is fine; the startup's multi-group product is where it isn't.

### Review checklist and common mistakes

- `if x in some_list` inside a loop (accidentally quadratic).
- Using a list as a queue (`pop(0)`).
- Building strings with `+=` in loops.
- Trusting intuition instead of `timeit` or `perf_counter`.
- Forgetting that dict and set keys must be hashable and immutable.

### Kenya context notes

M-Pesa reconciliation keys (phone + amount + time window) are rarely unique. Members pay the same amount, and treasurers sometimes pay on members' behalf. The FIFO-queue design handles honest duplicates. Ambiguous cases go to the treasurer's exceptions queue (P01.S04), not to a guess.

### Self-check quiz C11.Q01

1. What does O(n) mean, and why do we drop constants?
2. Why is `x in set` O(1) on average, and when does it degrade?
3. What is the total cost of draining a list with `pop(0)`? With `deque.popleft()`?
4. Code-reading: `for e in expected: if e.phone in [r.phone for r in received]: …`. What's the cost, and what's the fix?
5. When is an O(n²) algorithm acceptable?
6. Why measure at several sizes rather than one?
7. What does "amortised O(1)" mean for `list.append`?
8. Two-sum: why store `value → index` rather than `index → value`?

**Portfolio output:** the matcher, with its benchmark note.
**Done when:** D01.1 and D01.2 are checked; BT01.1 meets the acceptance criteria; Q01 ≥ 80%.

---

## [C11.M02] Stacks, queues, linked lists, recursion

**Tags:** Craft | Continuous (W8–W15) | Applied in P02.S03 | AI mode 0
**Prerequisites:** C11.M01.
**Time:** 6–8 h. Planned: 7 h new material across 7 blocks, plus reps.

**Learning outcomes**

1. **Trace** a recursive function's call stack by hand, and **identify** its base case, its progress towards the base case, and its cost.
2. **Convert** recursion into iteration with an explicit stack, and **explain** Python's recursion limit.
3. **Use** stacks (balanced symbols, undo) and queues (BFS order, job processing) with `list` and `collections.deque`.
4. **Implement** a singly linked list and **state** when Python lists are better.

**Core path** (recursion first, ahead of P02.S03 in W11–W12)

| Week | Item | Exact part | Mode |
|---|---|---|---|
| W8 | Runestone ch. 4 "Recursion" [R-0160] | 4.2–4.4 (What Is Recursion?, sum of a list, the three laws), 4.6 "Stack Frames: Implementing Recursion" | 0 |
| W9 | Build task BT02.1: recursive roll-up, then the iterative version | — | 0 |
| W10 | Runestone ch. 3 "Basic Data Structures" [R-0160] | 3.3–3.7 (stacks, balanced symbols) | 0 |
| W11 | Same chapter | 3.10–3.12 and 3.15–3.17 (queues, deques); drill D02.1 | 0 |
| W13 | Same chapter | 3.19–3.23 (linked lists, ordered lists, analysis) | 0 |
| W14 | Erickson, *Algorithms*, ch. 1 "Recursion" [R-0164] | The opening sections, through the Tower of Hanoi [VERIFY section numbers]; stop where you lose the thread. It's written for a second course | 0 |
| W15 | NeetCode "Stack" and "Linked List", two easy problems each [R-0163] | — | 0 |

**Supplementary:** MIT 6.006 Recitation 2 (data structures) [R-0162] · Python docs `collections.deque` [R-0165].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0160 | Runestone *pythonds3*, ch. 3–4 | book | Free | A | Stack frames drawn out step by step |
| R-0164 | Jeff Erickson, *Algorithms* (1st ed., 2019; CC BY 4.0) | book | Free PDF; paperback US$27.50 | A | The best writing on *thinking* recursively |
| R-0165 | Python docs: `collections` (`deque`), `sys.setrecursionlimit`, `functools.cache` | doc | Free | A | The real tools |

### Unplugged drill C11.D02.1 (Mode 0, 25 min)

1. Trace `total([500, 1000, 200])` for `def total(xs): return 0 if not xs else xs[0] + total(xs[1:])`:
   - draw every stack frame;
   - give the result;
   - give the Big-O, counting the slices;
   - say what happens with 5,000 items.
2. Write `is_balanced(text)` with a list used as a stack, so that `"{[()]}"` is true and `"([)]"`, `"(("` and `"a(b)c]"` are false.
3. Why is `collections.deque` the right queue, and `list.pop(0)` the wrong one?

### Build task C11.BT02.1 · Portfolio roll-up, two ways (applied in P02.S03)

**Spec.** A Forecourt PMO portfolio is a tree: portfolio → projects → sites, with milestones in P02. Leaves carry `budget`, `spent` and `progress` (0–1, as a `Decimal`). Write:

- `rollup_recursive(node)` and `rollup_iterative(node)`, the latter a post-order traversal with an explicit stack. Both return totals for `budget`, `spent` and `earned` (`budget × progress`).
- `progress(result)`: earned ÷ budget, so progress is **weighted by budget**, not a simple average.

Sample tree:

```
PORTFOLIO
├── PRJ-1
│   ├── SITE-A  budget 400,000  spent 250,000  progress 0.50
│   └── SITE-B  budget 600,000  spent 100,000  progress 0.10
└── PRJ-2       budget 1,000,000 spent 900,000 progress 0.80
```

**Acceptance criteria** (all verified with the reference):

- Both versions give budget **2,000,000**, spent **1,250,000** and progress **0.5300**.
- A 10,000-deep chain of nodes works iteratively, and the recursive version raises `RecursionError` (Python's default limit is 1000).
- At least 4 tests.
- A note on why Forecourt uses budget-weighted progress, and which version ships. Real portfolio depth is small, so recursion is fine in production; the iterative version is the one to understand.

### Review checklist and common mistakes

- A missing or unreachable base case.
- Slicing in recursion (hidden O(n²)).
- Raising the recursion limit instead of fixing the algorithm.
- `list.pop(0)` queues.
- Mutating the tree while traversing it.

### Kenya context notes

Client PMO data arrives as spreadsheets with an implicit hierarchy (indentation, or WBS codes like `1.2.3`). Building the tree from codes is a stack problem. Note it for P02.S04's import.

### Self-check quiz C11.Q02

1. What are the three laws of recursion?
2. What does Python store in each stack frame, and why is there a recursion limit?
3. Turn a recursive post-order traversal into an iterative one: what do you push, and why the `done` flag?
4. Stack or queue: undoing edits? Processing upload jobs in arrival order? Visiting tree levels one at a time?
5. What does a linked list do better than a Python list, and what worse?
6. Why does `functools.cache` turn naive recursive Fibonacci from exponential to linear time?
7. Code-reading: a recursive function receives `xs[1:]` on each call. What is its real cost?
8. Debugging: `RecursionError: maximum recursion depth exceeded` on a 3-level tree. What's the likely bug?

**Portfolio output:** the roll-up module and its tests.
**Done when:** D02.1 is checked; BT02.1 meets the acceptance criteria; Q02 ≥ 80%.

---

## [C11.M03] Sorting and searching

**Tags:** Craft | Continuous (W16–W22) | Applied in P03 | AI mode 0
**Prerequisites:** C11.M01–M02.
**Time:** 6–8 h. Planned: 6 h new material across 6 blocks, plus reps.

**Learning outcomes**

1. **Implement** binary search (lower bound) without an off-by-one error, and **trace** it by hand.
2. **Explain** O(n log n) comparison sorting through merge sort, and when Python's built-in sort (stable, adaptive) is all you need.
3. **Use** stability to sort by several keys, and **use** `bisect` with `key=` for lookups on sorted data.
4. **Choose** between sorting once and searching many times, versus hashing.

**Core path**

| Week | Item | Exact part | Mode |
|---|---|---|---|
| W16 | Runestone ch. 5 "Searching and Sorting" [R-0160] | 5.2–5.4 (sequential and binary search, with analysis) | 0 |
| W17 | Drill D03.1 (binary-search trace and lower-bound implementation) | — | 0 |
| W19 | Runestone [R-0160] | 5.6–5.9 (sorting; bubble, selection and insertion sort: understand them, then never ship them) | 0 |
| W20 | Runestone [R-0160]; MIT 6.006 Lecture 3 "Sorting" notes [R-0162] | 5.11 "The Merge Sort", 5.12 "The Quicksort" | 0 |
| W21 | Build task BT03.1 (POS lookups and report ordering) | — | 0 |
| W22 | Python docs `bisect` [R-0166]; NeetCode "Binary Search", two easy problems [R-0163] | `bisect_left`, `bisect_right`, `key=` | 0 |

**Supplementary:** MIT 6.006 Lecture 5 "Linear Sorting" (counting and radix sort) [R-0162] · Python "Sorting Techniques" HOWTO (stability, key functions) [VERIFY link].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0160 | Runestone *pythonds3*, ch. 5 | book | Free | A | Every algorithm, with analysis and runnable code |
| R-0162 | MIT 6.006 Lecture 3 notes | course | Free | A | A rigorous treatment of merge sort |
| R-0166 | Python docs: `bisect`, `heapq` | doc | Free | A | The tools you'll actually use |

### Unplugged drill C11.D03.1 (Mode 0, 25 min)

1. For `xs = [3, 8, 15, 15, 22, 40, 41, 57]`, trace lower-bound binary search for the target 15, then for 16. Write `(lo, hi, mid, xs[mid])` at every step, and the returned index.
2. Write `lower_bound(xs, target)` (half-open interval, `while lo < hi`). Make it return the same as `bisect.bisect_left` for every target from −2 to 60.
3. What do `bisect_left` and `bisect_right` each return for 15? Why does `price_on(date)` need `bisect_right`?

### Build task C11.BT03.1 · POS lookups and end-of-day ordering (applied in P03)

**Spec.**

- `price_on(effective, day)`: `effective` is a sorted list of `(date_iso, price)`. Return the price in force on `day`, meaning the last change on or before it, using `bisect_right`. Raise `LookupError` for days before the first price.
- `eod_report(sales)`: order sales by till ascending, then amount descending, then time ascending, using **stable sorts applied least-significant key first**.
- `sales_between(sorted_times, start, end)`: count sales in a time window, using two `bisect` calls.

**Acceptance criteria** (verified with the reference):

- With prices `[("2026-01-01", 120.00), ("2026-07-01", 135.00), ("2026-10-15", 140.00)]`:
  - 1 Jul → 135.00;
  - 14 Oct → 135.00;
  - 31 Dec → 140.00;
  - 31 Dec 2025 → `LookupError`.
- `eod_report` on the four-sale sample in the answer key gives `(1, 900, 10:00)`, `(1, 500, 07:00)`, `(1, 500, 09:00)`, `(2, 500, 08:00)`.
- Lookups are O(log n), stated in docstrings.

### Review checklist and common mistakes

- Off-by-one errors from mixing closed and half-open intervals.
- `while lo <= hi` with half-open updates.
- Sorting inside a loop.
- Sorting strings of numbers (`"100" < "20"`).
- Assuming `sorted()` is unstable; it's stable, which is what makes multi-key sorts work.

### Kenya context notes

Fuel and shop prices change by notice. EPRA's monthly pump-price reviews are the obvious forecourt case. "Price on date" lookups must use the effective date, not the date you entered the change [J].

### Self-check quiz C11.Q03

1. Why must the input be sorted for binary search, and what does it cost to sort first?
2. What do `bisect_left` and `bisect_right` each return when the target appears more than once?
3. Why is merge sort O(n log n)? Sketch the recursion tree.
4. What is a stable sort, and how does stability let you sort by several keys?
5. When does hashing beat sort-then-search?
6. Code-reading: `while lo <= hi: mid = (lo + hi) // 2; … hi = mid`. Where's the bug?
7. What algorithm does Python's `sorted` use, and on what kind of input is it fastest? (Answer from the docs, not from memory.)
8. Debugging: `price_on` returns the *next* price, not the current one. Which `bisect` function was used?

**Portfolio output:** the POS lookup module and its tests.
**Done when:** D03.1 is checked; BT03.1 meets the acceptance criteria; Q03 ≥ 80%.

---

## [C11.M04] Trees, binary search trees, heaps

**Tags:** Craft | Continuous (W23–W29) | Applied in P04 | AI mode 0
**Prerequisites:** C11.M02–M03.
**Time:** 6–8 h. Planned: 6 h new material across 6 blocks, plus reps.

**Learning outcomes**

1. **Traverse** trees in pre-order, in-order and post-order by hand, and **say** which traversal suits which job.
2. **Insert into and search** a binary search tree, and **explain** why balance decides whether operations cost O(log n) or O(n).
3. **Implement** a binary min-heap (push and pop with sift up and sift down) on a list.
4. **Use** `heapq` for priority queues, including lazy deletion for rescheduling, and the max-heap functions new in 3.14.

**Core path**

| Week | Item | Exact part | Mode |
|---|---|---|---|
| W23 | Runestone ch. 6 "Trees and Tree Algorithms" [R-0160] | 6.2–6.4 and 6.8 (vocabulary, implementation, traversals) | 0 |
| W25 | Runestone [R-0160] | 6.12–6.15 (binary search trees: operations, implementation, analysis) | 0 |
| W26 | Runestone [R-0160]; MIT 6.006 Lecture 8 "Binary Heaps" notes [R-0162] | 6.9–6.11 (priority queues with binary heaps) | 0 |
| W27 | Drill D04.1 (BST and heap by hand; your own min-heap) | — | 0 |
| W28 | Build task BT04.1 (SLA scheduler) | — | 0 |
| W29 | Python docs `heapq`: "Priority Queue Implementation Notes" [R-0166]; Runestone 6.16–6.17 (balanced BSTs: concepts only) | — | 0 |

**Supplementary:** MIT 6.006 Lectures 6–7 "Binary Trees" (including AVL) [R-0162] · NeetCode "Trees" and "Heap / Priority Queue", easy problems [R-0163].

### Unplugged drill C11.D04.1 (Mode 0, 30 min)

1. Insert `50, 30, 70, 20, 40, 60, 80, 35` into an empty BST. Draw it, then give the in-order and pre-order sequences and the height (counted in edges).
2. Push `5, 3, 8, 1, 9, 2` into an empty min-heap stored as a list. Write the list after each push, then after two pops.
3. Write `MinHeap.push` and `MinHeap.pop` without `heapq`. Test that pushing 200 random numbers and popping them all returns them sorted.

### Build task C11.BT04.1 · SLA work-order scheduler (applied in P04)

**Spec.** Write `SlaQueue` with:

- `add(job_id, due_at, priority)`;
- `reschedule(job_id, new_due, priority)`;
- `next_job()`.

Ordering is by `(due_at, priority, insertion sequence)`, so ties go to the earliest-added job. Rescheduling uses the `heapq` docs' **lazy-deletion** recipe: mark the old entry as removed and push a new one. Popping skips removed entries.

**Acceptance criteria** (verified with the reference):

- Add `WO-1` (due 10:00, priority 2), `WO-2` (09:00, priority 1) and `WO-3` (09:00, priority 0).
- Reschedule `WO-1` to 08:00.
- `next_job()` then returns `WO-1`, `WO-3`, `WO-2`, then `None`.
- Every operation is O(log n).
- At least 4 tests, including ties and rescheduling an already-rescheduled job.

### Review checklist and common mistakes

- Heap entries that can't be compared, such as dicts. Add a sequence counter as a tie-breaker.
- Assuming `heap[1]` is the second-smallest item.
- Deleting from the middle of a heap (use lazy deletion).
- An unbalanced BST built from sorted input, which is just a linked list.
- Forgetting that `heapq` is a *min*-heap. Use the 3.14 `*_max` functions, or negate keys.

### Kenya context notes

Field technicians in Nairobi traffic miss slots. The scheduler must reschedule cheaply many times a day, and that's what lazy deletion is for. SLA times are stored in UTC and shown in Nairobi time (C02.M03).

### Self-check quiz C11.Q04

1. Which traversal outputs a BST's keys in sorted order?
2. Why does inserting sorted keys into a plain BST give O(n) operations?
3. What are the heap's two properties (structure and order)?
4. In an array-backed heap, where are the children and the parent of index *i*?
5. What does each push or pop cost, and why?
6. How does lazy deletion avoid an O(n) removal?
7. What did Python 3.14 add to `heapq`?
8. Debugging: `TypeError: '<' not supported between instances of 'dict' and 'dict'` from `heappush`. What's the fix?

**Portfolio output:** the scheduler module and its tests.
**Done when:** D04.1 is checked; BT04.1 meets the acceptance criteria; Q04 ≥ 80%.

---

## [C11.M10] Rolling Mode 0 practice reps

**Tags:** Craft | Continuous (every week) | Applied in P02 review gates (RG-P02-1 to RG-P02-4) and every later code review | AI mode 0
**Prerequisites:** none. It starts in W1.
**Time:** 30 minutes per normal week and the whole 1.5 h block in light weeks: 18.5 h across W1–W29.

**Learning outcomes**

1. **Re-solve** earlier problems from memory on a spaced schedule, and **track** time and error types.
2. **Recognise** patterns (hash map, two pointers, stack, binary search, heap, recursion) from a problem's wording.
3. **Spot** complexity problems in code you review, including code agents write.

**Method.**

1. Every problem you solve in a C11 block gets an Anki card in the deck `FSE::C11`. The front is the problem statement in one or two lines; the back is the pattern name and the key insight, not the code.
2. When a card comes due, re-solve the problem from a blank file, timed, without looking.
3. Log the result in the weekly tracker as `C11.M10: <problem> <minutes> <ok | slip | fail>`.
4. Anki's scheduler (FSRS, C01.M03) does the spacing.
5. A `fail` means you re-read the pattern and re-solve the problem the next week.

**Core path:** your own deck. New problems come from the module currently in its window, plus NeetCode easy problems in the matching category [R-0163] and Exercism practice exercises [R-0133].

### Unplugged drill C11.D10.1 · Name the pattern (Mode 0, 10 min, first done in W6)

For each problem, name the pattern and its expected Big-O, without solving it:

1. Do two receipts in a statement have the same reference?
2. Find the first member whose cumulative contributions exceed KES 50,000, given sorted running totals.
3. Do the brackets in a formula string match?
4. Which 5 work orders are most overdue, from 10,000?
5. Sum the budgets in a project tree.
6. Which two loan requests together exactly use the available pool?

### Build task C11.BT10.1 · Complexity review checklist (applied in P02 review gates)

**Spec.** Write `REVIEW-COMPLEXITY.md` in the P02 repository: a checklist used at every agent PR review (C08.M03). It must flag:

- membership tests on lists inside loops;
- queries inside loops (the Django N+1 pattern, C05.M08);
- `pop(0)`;
- string concatenation in loops;
- recursion on user-controlled depth;
- sorting inside loops;
- unbounded `.all()` loads.

**Acceptance criteria:**

- The checklist is used at RG-P02-1 to RG-P02-4.
- Each gate records at least one finding or an explicit "none found".
- One real finding is logged with its before-and-after timing.

### Review checklist and common mistakes

- Re-reading a solution instead of re-solving it.
- Skipping reps in busy weeks; reps are the first thing to protect, not the first to cut.
- Collecting problems without recording their patterns.

### Kenya context notes

Do reps offline: problem cards on AnkiDroid, solutions on paper. 30 minutes needs no connection.

### Self-check quiz C11.Q10

1. Why re-solve from a blank file instead of re-reading your old solution?
2. What goes on the back of a problem card, and why not the code?
3. What does a `slip` mean, as opposed to a `fail`?
4. Name three code smells from your checklist that indicate accidental O(n²).
5. Why review agent PRs specifically for complexity?
6. How many reps per week are protected even in a minimum viable week (V00 §5(i))?
7. What do you log for each rep, and why record the outcome type?
8. A problem that took 10 minutes the first time takes 25 on a rep. What does that tell you, and what do you do next?

**Portfolio output:** the `FSE::C11` deck and the review checklist.
**Done when:** D10.1 is checked; at least 20 reps are logged by W29; BT10.1 has been used at the P02 gates.

---

## Trends Watch (C11a)

| Blip | Why it matters here | L01 ID | As of |
|---|---|---|---|
| **AI writes the first draft; you own its complexity** | Agents produce code that works on small test data and fails at scale: nested loops, N+1 queries. The M10 checklist exists for P02's Mode 3 build | L01.B01 | 2026-10-08 |
| **`heapq` gains max-heap functions in Python 3.14** [V R-0130, R-0166] | No more negated keys for max-heaps. Worth knowing when reading older code | — (minor) | 2026-10-08 |
| **Fundamentals still gate hiring** | V00 keeps DSA at working depth unless the employment goal (G4) rises. If it does, add the timed-practice track from V00 §5(g) | L01.B11 (proposed) | 2026-10-08 |

---

## Answer key

<details><summary><b>C11.D01.1</b>: costs</summary>

1. O(n): a list scan.
2. O(1) on average. It degrades to O(n) only with pathological hash collisions [V R-0161].
3. O(n·m).
4. O(n log n).
5. O(n²) in total, because each `pop(0)` shifts every remaining element.
6. O(n) in total.
7. `+=` in a loop can be O(n²), copying the growing string each time (CPython sometimes optimises this, but don't rely on it). `"".join` is O(total length).
8. O(1).
</details>

<details><summary><b>C11.D01.2 · C11.BT01.1</b>: two-sum and both matchers (tested)</summary>

Two-sum on the sample returns `(2, 3)` (300 + 700). It is O(n), storing value → index for every number seen so far.

```python
from collections import defaultdict, deque

# ---------- M01: two-sum and reconciliation matching ----------
def two_sum(amounts: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}
    for i, a in enumerate(amounts):
        if target - a in seen:
            return seen[target - a], i
        seen[a] = i
    return None

def match_naive(expected, received):
    """expected/received: lists of (key, amount, ref). O(len(expected) * len(received))."""
    used, pairs = set(), []
    for e in expected:
        for j, r in enumerate(received):
            if j not in used and r[0] == e[0] and r[1] == e[1]:
                used.add(j); pairs.append((e[2], r[2])); break
    return pairs

def match_indexed(expected, received):
    """Same result, O(len(expected) + len(received)) using a dict of FIFO queues."""
    index: dict[tuple, deque] = defaultdict(deque)
    for r in received:
        index[(r[0], r[1])].append(r[2])
    pairs = []
    for e in expected:
        q = index.get((e[0], e[1]))
        if q:
            pairs.append((e[2], q.popleft()))
    return pairs
```
</details>

<details><summary><b>C11.Q01</b></summary>

1. Growth rate as n grows. Constants depend on the machine; the growth rate decides what happens at scale.
2. Hashing goes straight to the slot. It degrades when many keys collide.
3. O(n²); O(n).
4. O(e × r): a new list is built on every iteration. Build `received_phones = {r.phone for r in received}` once, then test membership in the set.
5. When n is small and bounded (one chama's year), or when the simpler code is much easier to verify. Measure first.
6. Growth only shows between sizes. One size hides the curve.
7. Occasional resizes are spread across many appends, so the average cost per append stays constant.
8. You look up the *complement* (target − value) and need its index, so the value has to be the key.
</details>

<details><summary><b>C11.D02.1</b></summary>

1. The frames are `total([500,1000,200])` → `total([1000,200])` → `total([200])` → `total([])`, which returns 0. Then 200, 1200, and finally **1700**. Each call copies a slice, so the cost is O(n²). With 5,000 items it raises `RecursionError` (the default limit is 1000). Fix it with a loop or an index parameter.
2. See `is_balanced` in the BT02.1 reference below.
3. `deque.popleft()` is O(1); `list.pop(0)` is O(n), because every remaining element shifts.
</details>

<details><summary><b>C11.BT02.1</b>: reference (all acceptance values verified)</summary>

```python
from decimal import Decimal

# ---------- M02: stack and recursion ----------
PAIRS = {")": "(", "]": "[", "}": "{"}
def is_balanced(text: str) -> bool:
    stack: list[str] = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in PAIRS:
            if not stack or stack.pop() != PAIRS[ch]:
                return False
    return not stack

def rollup_recursive(node: dict) -> dict:
    kids = node.get("children") or []
    if not kids:
        return {"budget": node["budget"], "spent": node["spent"], "earned": node["budget"] * node["progress"]}
    parts = [rollup_recursive(k) for k in kids]
    return {k: sum((p[k] for p in parts), Decimal("0")) for k in ("budget", "spent", "earned")}

def rollup_iterative(root: dict) -> dict:
    """Post-order with an explicit stack: no recursion limit."""
    results: dict[int, dict] = {}
    stack = [(root, False)]
    while stack:
        node, done = stack.pop()
        kids = node.get("children") or []
        if not kids:
            results[id(node)] = {"budget": node["budget"], "spent": node["spent"], "earned": node["budget"] * node["progress"]}
        elif done:
            parts = [results.pop(id(k)) for k in kids]
            results[id(node)] = {k: sum((p[k] for p in parts), Decimal("0")) for k in ("budget", "spent", "earned")}
        else:
            stack.append((node, True))
            stack.extend((k, False) for k in kids)
    return results[id(root)]

def progress(r: dict) -> Decimal:
    return (r["earned"] / r["budget"]).quantize(Decimal("0.0001")) if r["budget"] else Decimal("0")
```
</details>

<details><summary><b>C11.Q02</b></summary>

1. A base case; progress towards the base case on every call; a call to itself.
2. Local variables and the return point. Every frame uses memory, so CPython caps the depth (default 1000) to fail cleanly instead of crashing.
3. Push `(node, False)`. When you pop it, push `(node, True)` and then its children. When `(node, True)` comes off the stack, all of its children have been processed. The flag tells you which visit you're on.
4. Undoing edits: a stack. Processing uploads in arrival order: a queue. Visiting tree levels one at a time: a queue (breadth-first).
5. O(1) insertion and removal once you hold a reference to the node, with no shifting. It's worse at indexing, has poor cache locality, and costs more memory per element.
6. It memoises: each subproblem is computed once.
7. O(n²), because every call copies a slice.
8. A missing or unreachable base case, often a leaf check like `if not node["children"]` that fails on a missing key, or a child that refers back to its parent.
</details>

<details><summary><b>C11.D03.1</b></summary>

| Target | Steps (lo, hi, mid, xs[mid]) | Returns |
|---|---|---|
| 15 | (0, 8, 4, 22) → (0, 4, 2, 15) → (0, 2, 1, 8) | **2** |
| 16 | (0, 8, 4, 22) → (0, 4, 2, 15) → (3, 4, 3, 15) | **4** |

- For 15, `bisect_left` returns 2 and `bisect_right` returns 4.
- `price_on` needs the last change *on or before* the day, which is index `bisect_right(...) − 1`. With `bisect_left`, a change effective on that exact day would be missed.
</details>

<details><summary><b>C11.BT03.1</b>: reference (tested)</summary>

```python
import bisect
from decimal import Decimal

# ---------- M03: binary search ----------
def lower_bound(xs: list, target) -> int:
    lo, hi = 0, len(xs)
    while lo < hi:
        mid = (lo + hi) // 2
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

def price_on(effective: list[tuple[str, Decimal]], day: str) -> Decimal:
    """effective: sorted (date_iso, price). Price in force on `day` (last change on or before it)."""
    i = bisect.bisect_right([d for d, _ in effective], day)
    if i == 0:
        raise LookupError(f"no price before {day}")
    return effective[i - 1][1]

def eod_report(sales: list[dict]) -> list[dict]:
    """till ascending, amount descending, time ascending. Stable sorts: least significant key first."""
    rows = sorted(sales, key=lambda s: s["at"])
    rows = sorted(rows, key=lambda s: s["amount"], reverse=True)
    return sorted(rows, key=lambda s: s["till"])
```

Sample for `eod_report`:

```python
[{"till": 2, "amount": 500, "at": "08:00"}, {"till": 1, "amount": 500, "at": "09:00"},
 {"till": 1, "amount": 900, "at": "10:00"}, {"till": 1, "amount": 500, "at": "07:00"}]
```
</details>

<details><summary><b>C11.Q03</b></summary>

1. Each comparison discards half of the range, which only works if the order is known. Sorting first costs O(n log n). That pays off when you search many times.
2. `bisect_left` returns the first position of the target; `bisect_right` returns the position just after its last occurrence.
3. Merge sort halves the list log n times, and each level of the recursion tree does O(n) merging work.
4. A stable sort keeps equal items in their original order. Sort by the least significant key first, and each later sort preserves the earlier ordering among ties.
5. Hashing wins when you only need exact matches. Sorting wins for ranges, nearest-match and ordered output.
6. `hi = mid` with a closed interval (`<=`) can loop forever. Use half-open `lo < hi`, or set `hi = mid − 1`.
7. A stable, adaptive merge-based sort (Timsort), fastest on input that already contains sorted runs. Confirm the details in the docs.
8. `bisect_left` was used where `bisect_right` (minus one) was needed, or the "− 1" was forgotten.
</details>

<details><summary><b>C11.D04.1</b></summary>

1. **In-order:** 20, 30, 35, 40, 50, 60, 70, 80. **Pre-order:** 50, 30, 20, 40, 35, 70, 60, 80. **Height:** 3 edges (50 → 30 → 40 → 35).
2. The list after each step:

   | Step | Heap list |
   |---|---|
   | push 5 | `[5]` |
   | push 3 | `[3, 5]` |
   | push 8 | `[3, 5, 8]` |
   | push 1 | `[1, 3, 8, 5]` |
   | push 9 | `[1, 3, 8, 5, 9]` |
   | push 2 | `[1, 3, 2, 5, 9, 8]` |
   | pop → 1 | `[2, 3, 8, 5, 9]` |
   | pop → 2 | `[3, 5, 8, 9]` |

3. See `MinHeap` in the reference below.
</details>

<details><summary><b>C11.BT04.1</b>: reference (tested)</summary>

```python
import heapq
import itertools

# ---------- M04: heaps ----------
class MinHeap:
    def __init__(self) -> None:
        self.a: list = []
    def push(self, x) -> None:
        a = self.a; a.append(x); i = len(a) - 1
        while i > 0 and a[(i - 1) // 2] > a[i]:
            p = (i - 1) // 2; a[i], a[p] = a[p], a[i]; i = p
    def pop(self):
        a = self.a; top = a[0]; last = a.pop()
        if a:
            a[0] = last; i = 0
            while True:
                l, r, s = 2 * i + 1, 2 * i + 2, i
                if l < len(a) and a[l] < a[s]: s = l
                if r < len(a) and a[r] < a[s]: s = r
                if s == i: break
                a[i], a[s] = a[s], a[i]; i = s
        return top

class SlaQueue:
    """Work orders by (due_at, priority, seq). Reschedule via lazy invalidation (heapq docs recipe)."""
    REMOVED = object()
    def __init__(self) -> None:
        self.heap: list = []; self.entries: dict[str, list] = {}; self.seq = itertools.count()
    def add(self, job_id: str, due_at: str, priority: int) -> None:
        if job_id in self.entries:
            self.entries.pop(job_id)[-1] = self.REMOVED
        entry = [due_at, priority, next(self.seq), job_id]
        self.entries[job_id] = entry; heapq.heappush(self.heap, entry)
    reschedule = add
    def next_job(self) -> str | None:
        while self.heap:
            *_, job = heapq.heappop(self.heap)
            if job is not self.REMOVED:
                del self.entries[job]; return job
        return None
```
</details>

<details><summary><b>C11.Q04</b></summary>

1. In-order.
2. Each new key becomes the right child of the previous one, so the tree degenerates into a chain.
3. **Structure:** a complete binary tree, stored as a list. **Order:** every parent is ≤ its children (for a min-heap).
4. The children are at 2i + 1 and 2i + 2; the parent is at (i − 1) // 2.
5. O(log n): one swap path along the tree's height.
6. It marks the old entry and pushes a new one, and pops skip marked entries. Each operation stays O(log n), at the cost of some stale entries.
7. `heapify_max`, `heappush_max`, `heappop_max`, `heapreplace_max` and `heappushpop_max`.
8. Push tuples, `(due, priority, seq, item)`, so a unique counter breaks ties before Python ever compares the dicts.
</details>

<details><summary><b>C11.D10.1</b></summary>

1. Hash set: O(n).
2. Binary search on the sorted totals: O(log n).
3. Stack: O(n).
4. Heap: `heapq.nsmallest(5, …)` is O(n log k).
5. Recursion or a stack (post-order): O(n).
6. Two-sum with a hash map: O(n).
</details>

<details><summary><b>C11.Q10</b></summary>

1. Recognising an answer isn't the same as producing it. Retrieval builds the skill (C01.M03).
2. The pattern and the key insight. Code on the card gets read instead of recalled.
3. A `slip` means you solved it, slowly or after one wrong turn. A `fail` means you couldn't solve it without help.
4. Any three of: `in list` inside a loop, queries inside a loop, `pop(0)`, string `+=`, sorting inside a loop.
5. Agents optimise for passing the tests at hand, and small test data hides quadratic costs.
6. The whole C11 block (1.5 h, including reps) stays in the minimum viable week. At least one rep, every week.
7. The problem, the minutes taken, and `ok`, `slip` or `fail`. The outcome type tells you what to fix: the pattern (`fail`) or your fluency with it (`slip`).
8. Your recall of the pattern is weak, even though you once solved it. Log a `slip`, re-read the pattern note on the card, and re-solve it next week. Grade the card "Hard" so FSRS brings it back sooner.
</details>


---

## Resource index (C11a)

R-0130 and R-0133 are defined in C02a. New IDs run from R-0160.

| ID | Resource | Provider | Type | Cost | Checked | Verified | Used in |
|---|---|---|---|---|---|---|---|
| R-0130 | [What's New In Python 3.14 (defined in C02a)](https://docs.python.org/3/whatsnew/3.14.html) | Python docs | doc | free | 2026-10-08 | yes | §0 / Trends Watch |
| R-0133 | [Exercism Python track (defined in C02a)](https://exercism.org/tracks/python) | Exercism | platform | free | 2026-10-08 | yes | C11.M01, C11.M10 |
| R-0160 | [Problem Solving with Algorithms and Data Structures using Python, 3rd ed. (Miller & Ranum; Runestone interactive, CC BY-NC-SA 4.0)](https://runestone.academy/ns/books/published/pythonds3/index.html) | Runestone Academy / Luther College | book | free | 2026-10-08 | yes | C11.M01, C11.M02, C11.M03, C11.M04 |
| R-0161 | [Time complexity of operations on built-in types (CPython)](https://docs.python.org/3/builtins/time-complexity.html) | Python docs | doc | free | 2026-10-08 | yes | C11.M01 |
| R-0162 | [6.006 Introduction to Algorithms, Spring 2020 (lecture notes, recitations, problem sets with solutions, videos)](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) | MIT OpenCourseWare | course | free | 2026-10-08 | yes | C11.M01, C11.M02, C11.M03, C11.M04 |
| R-0163 | [NeetCode practice lists (NeetCode 150 / Blind 75, by pattern; free tier, verified via secondary sources)](https://neetcode.io/practice) | NeetCode | platform | freemium | 2026-10-08 | yes | C11.M01, C11.M02, C11.M03, C11.M04, C11.M10 |
| R-0164 | [Algorithms, 1st ed. (2019), free PDF under CC BY 4.0](https://jeffe.cs.illinois.edu/teaching/algorithms/) | Jeff Erickson (UIUC) | book | free | 2026-10-08 | yes | C11.M02 |
| R-0165 | [collections (deque), sys.setrecursionlimit, functools.cache](https://docs.python.org/3/library/collections.html) | Python docs | doc | free | 2026-10-08 | yes | C11.M02 |
| R-0166 | [bisect and heapq (including 3.14 max-heap functions and the priority-queue notes)](https://docs.python.org/3/library/heapq.html) | Python docs | doc | free | 2026-10-08 | yes | C11.M03, C11.M04 |

---

## YAML manifest

```yaml
manifest_version: 1
playbook: FSE
tsw_track: 1
volume: C11a
title: Computer Science Foundations, Part A
version: '1.1'
date: '2026-10-26'
modules:
- id: FSE.C11.M01
  title: Complexity, arrays, strings, hash maps
  prerequisites: []
  hours: [6, 8]
  outcomes: [State Big-O of everyday Python operations, Replace nested matching with hash maps, Measure at several sizes,
    Solve array/hash patterns unplugged]
  ai_modes: [0]
  applied_in: [FSE.P01.S04]
  resources: [R-0133, R-0160, R-0161, R-0162, R-0163]
  assessments: [FSE.C11.Q01, FSE.C11.D01.1, FSE.C11.D01.2, FSE.C11.BT01.1]
- id: FSE.C11.M02
  title: Stacks, queues, linked lists, recursion
  prerequisites: [FSE.C11.M01]
  hours: [6, 8]
  outcomes: [Trace recursion and its cost, Convert recursion to an explicit stack, Use stacks and deques correctly, Implement
      a linked list]
  ai_modes: [0]
  applied_in: [FSE.P02.S03]
  resources: [R-0160, R-0162, R-0163, R-0164, R-0165]
  assessments: [FSE.C11.Q02, FSE.C11.D02.1, FSE.C11.BT02.1]
- id: FSE.C11.M03
  title: Sorting and searching
  prerequisites: [FSE.C11.M02]
  hours: [6, 8]
  outcomes: [Implement lower-bound binary search, Explain O(n log n) sorting, Use stable multi-key sorts and bisect, Choose
      sort-and-search vs hashing]
  ai_modes: [0]
  applied_in: [FSE.P03]
  resources: [R-0160, R-0162, R-0163, R-0166]
  assessments: [FSE.C11.Q03, FSE.C11.D03.1, FSE.C11.BT03.1]
- id: FSE.C11.M04
  title: Trees, binary search trees, heaps
  prerequisites: [FSE.C11.M03]
  hours: [6, 8]
  outcomes: [Traverse trees by hand, Explain BST balance and cost, Implement a binary min-heap, Use heapq with lazy deletion]
  ai_modes: [0]
  applied_in: [FSE.P04]
  resources: [R-0160, R-0162, R-0163, R-0166]
  assessments: [FSE.C11.Q04, FSE.C11.D04.1, FSE.C11.BT04.1]
- id: FSE.C11.M10
  title: Rolling Mode 0 practice reps (spaced problem sets)
  prerequisites: []
  hours: [20, 25]
  outcomes: [Re-solve on a spaced schedule, Recognise patterns from problem wording, Spot complexity problems in reviewed
      code]
  ai_modes: [0]
  applied_in: [FSE.RG-P02-1, FSE.RG-P02-2, FSE.RG-P02-3, FSE.RG-P02-4]
  resources: [R-0133, R-0163]
  assessments: [FSE.C11.Q10, FSE.C11.D10.1, FSE.C11.BT10.1]
resources:
- id: R-0130
  title: What's New In Python 3.14 (defined in C02a)
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/whatsnew/3.14.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-08'}
  version_targeted: Python 3.14
  level: null
  role: evidence
  status: active
  verified: true
- id: R-0133
  title: Exercism Python track (defined in C02a)
  provider: Exercism
  type: platform
  url: https://exercism.org/tracks/python
  cost: {tier: free, price: null, currency: null, checked: '2026-10-08'}
  version_targeted: null
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0160
  title: Problem Solving with Algorithms and Data Structures using Python, 3rd ed. (Miller & Ranum; Runestone interactive,
    CC BY-NC-SA 4.0)
  provider: Runestone Academy / Luther College
  type: book
  url: https://runestone.academy/ns/books/published/pythonds3/index.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-08'}
  version_targeted: Python 3
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0161
  title: Time complexity of operations on built-in types (CPython)
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/builtins/time-complexity.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-08'}
  version_targeted: CPython 3.14
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0162
  title: 6.006 Introduction to Algorithms, Spring 2020 (lecture notes, recitations, problem sets with solutions, videos)
  provider: MIT OpenCourseWare
  type: course
  url: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-08'}
  version_targeted: null
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0163
  title: NeetCode practice lists (NeetCode 150 / Blind 75, by pattern; free tier, verified via secondary sources)
  provider: NeetCode
  type: platform
  url: https://neetcode.io/practice
  cost: {tier: freemium, price: null, currency: null, checked: '2026-10-08'}
  version_targeted: null
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0164
  title: Algorithms, 1st ed. (2019), free PDF under CC BY 4.0
  provider: Jeff Erickson (UIUC)
  type: book
  url: https://jeffe.cs.illinois.edu/teaching/algorithms/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-08'}
  version_targeted: null
  level: advanced
  role: learning
  status: active
  verified: true
- id: R-0165
  title: collections (deque), sys.setrecursionlimit, functools.cache
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/library/collections.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-08'}
  version_targeted: Python 3.14
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0166
  title: bisect and heapq (including 3.14 max-heap functions and the priority-queue notes)
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/library/heapq.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-08'}
  version_targeted: Python 3.14
  level: intermediate
  role: learning
  status: active
  verified: true
x_block:
  day: Saturday
  time: 11:30-13:00
  hours_per_week: 1.5
  split_minutes: {retrieve: 5, new: 55, reps: 30}
  light_weeks_all_reps: [6, 12, 18, 24]
x_windows:
  FSE.C11.M01: [1, 7]
  FSE.C11.M02: [8, 15]
  FSE.C11.M03: [16, 22]
  FSE.C11.M04: [23, 29]
  FSE.C11.M10: [1, 66]
x_tested_on: {python: 3.14.4, pytest: 9.1.1, reference_tests_passing: 14}
```

---

## Handoff

```
HANDOFF: C11a
Covered: The Saturday Mode 0 block (format, rules, calendar matching the tracker's C11 item
  for each week); C11.M01–M04 and M10 to the §8.1 template; drills D01.1–D10.1 and quizzes
  Q01–Q10 with machine-checked answers; build-task cores BT01.1 (matcher, measured: 106x
  at 5,000 rows), BT02.1 (budget-weighted roll-up; the iterative version survives a
  10,000-deep tree), BT03.1 (price-on-date, stable end-of-day sort), BT04.1 (SLA heap with
  lazy rescheduling) and BT10.1 (agent-PR complexity checklist). 14 reference tests pass
  on Python 3.14.4.
Deferred / open items:
  - M02 runs recursion first (W8–W9), ahead of P02.S03 (W11–W12); queues and linked lists follow.
  - Hour note: the fixed block gives 97.5 h over W1–W65, at the top of V00's C11 range
    (74–97 h). The extra is practice reps; no change needed.
  - C11b (M05–M09: graphs, dynamic programming, how computers work, networks, operating
    systems) is due by W18.
Links marked [VERIFY]: Erickson ch. 1 section numbers; the Python "Sorting Techniques"
  HOWTO link.
Build-clock status: v1.1 re-dated to V00 v1.3 (B2). P01 runs in the CHAMA APP Project; BT01.1's matcher is the reference for its S04 (W2).
AI-mode log summary: none. C11 is Mode 0 by definition.
Decisions made: no ADRs. Conventions: FIFO deque matching for duplicate payments
  (ambiguous cases go to the exceptions queue); budget-weighted progress for PMO
  roll-ups; effective-date pricing via bisect_right; lazy-deletion heaps for SLA
  scheduling.
Re-scored skills: n/a until GATE-1 (DSA baseline 0.3/5).
Prerequisites confirmed for next volume: C03 (W1) uses M01's hash-map matching in
  C03.M03 (reconciliation).
Next: C03, starting at C03.M01 (then C05a, C04, the L02 batch 1 cards; P01 when the
  client inputs arrive)
```
