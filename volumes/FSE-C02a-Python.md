# FSE-C02a · Python in Depth, Part A (C02.M01–M05)

**Full-Stack Development & Engineering Playbook · TSW Track 1**

| Field | Value |
|---|---|
| Strand | Craft (C). C02 is the canonical Python spine that STRUCTURES' T3 builds on (V00 §14.1) |
| Phase | 1 (M01–M03) and 2 (M04–M05). Each module also has a depth pass in Phase 3 |
| Version / date | 1.1 · 2026-10-26 (re-dated to V00 v1.3; first issue 1.0 · 2026-10-07) |
| Versions targeted | §0.2. Every code answer here was run on Python 3.14.4 with pytest 9.1.1 and mypy 2.4.0 |
| Prerequisites | C01.M01 step 3 (uv and Python 3.14); C01.M02 (Git); C01.M03 (tracker) |
| Hour budget | 19–27 h for M01–M05: a 12.5 h first pass in W1–W14, plus a depth pass of about 9 h in Phase 3 (W21–W22) |
| Applied in | P01.S01, P01.S02, P01.S04, P02.S04, P02.S06, P03 |
| Part B | `FSE-C02b-Python.md` (M06–M10), due by Fri 29 Jan 2027 (V00 §16.2) |

Evidence labels follow V00 §0.1: **[V R-xxxx]** verified this run · **[J]** judgement · **[A]** assumption · **[VERIFY]** not verified. All code is for learning; review and test it before relying on it.

> **Re-dated 2026-10-26 (v1.1) to FSE-V00 v1.3, re-baseline B2.** Week 1 is now **Mon 2 – Sun 8 Nov 2026** (W*n* starts Mon 2 Nov + 7(*n*−1) days). Content is unchanged; only the calendar, week numbers and build cross-references moved.

## Contents

- §0 Volume opener: calendar, versions, how C02a feeds the builds, Kenyan context
- C02.M01 Core refresh: types, functions, collections, comprehensions
- C02.M02 Errors, pytest basics and uv project layout
- C02.M03 Text and data processing: CSV, PDF, regex, Decimal, time zones
- C02.M04 Iterators, generators, decorators, context managers
- C02.M05 Typing in depth: generics, protocols, dataclasses, Pydantic
- Trends Watch · Answer key · Resource index · YAML manifest · Handoff

---

## 0. Volume opener

### 0.1 Calendar

The **first pass** hours come from V00 §12's week plan. The **depth pass** brings each module up to its mid-range budget; the tracker places it in Phase 3. Each module states which of its parts belong to the depth pass.

| Module | Hours (range) | First pass | Depth pass | Applied in |
|---|---|---|---|---|
| C02.M01 Core refresh | 4–6 | **W1** (2–8 Nov) Tue + Wed, 2.5 h | 2 h, W21 | P01.S01 |
| C02.M02 Errors, pytest, layout | 2–3 | **W1** Wed, 1.5 h | 0.5 h, Phase 3 | P01.S01–S02 |
| C02.M03 Text and data processing | 3–4 | **W4** (23–29 Nov), 1.5 h | 1.5 h, W21–W22 | P01.S04, P01 v1.0.1 |
| C02.M04 Iterators, generators, decorators, context managers | 5–7 | **W9** (28 Dec–3 Jan) 2 h + **W11** (11–17 Jan) 1.5 h | 1 h, W22 | P02.S04 |
| C02.M05 Typing in depth | 5–7 | **W10** (4–10 Jan) 2 h + **W14** (1–7 Feb) 1.5 h | 4.5 h, W22 | P02.S06, P03 |

### 0.2 Versions targeted (checked 2026-10-07)

| Item | Version | Note |
|---|---|---|
| Python | **3.14** (tested on 3.14.4) | 3.15.0 is due Fri 9 Oct 2026 [V R-0004]. Stay on 3.14 until Django lists 3.15 support |
| 3.14 language features you'll meet | PEP 649 deferred evaluation of annotations (with the new `annotationlib` module); PEP 750 template strings; PEP 758 `except` without brackets; PEP 779 free-threaded build officially supported | [V R-0130] |
| pytest · pytest-cov · Hypothesis | 9.1.1 · 7.1.0 · 6.168.5 | [V R-0001] |
| ruff · mypy · pyrefly | 0.16.10 · 2.4.0 · 1.3.2 | mypy is the reference checker here; pyrefly is a faster alternative [V R-0001] |
| Pydantic | 2.13.5 | [V R-0001] |
| pdfplumber · pypdf · cryptography | 0.11.10 · 6.19.0 · 50.0.2 | pypdf needs `cryptography` to open AES-encrypted PDFs [V R-0143] |
| tzdata | 2026.5 | Only needed where the OS lacks IANA time-zone data (Windows); Ubuntu ships it [J] |

### 0.3 How C02a feeds the builds

| Build need | When | Module |
|---|---|---|
| Ledger core and group rules, hand-built in Mode 1 | P01.S01, from Wed 28 Oct (the week before W1) | M01, M02 |
| Auth, roles and permission tests | P01.S02, W1 | M02 |
| M-Pesa statement import and reconciliation | P01.S04, W2 | M03 |
| Import from client spreadsheets (Forecourt PMO) | P02.S04, W11–W12 | M04 |
| Typed module boundaries and validated inputs | P02.S06, P03 | M05 |
| STRUCTURES `strlib.units` with pytest | STR W2 | M01–M02 (V00 §14.1) |

NumPy and linear algebra are taught in STRUCTURES V01.M10 (W8–W9), not here (V00 R4).

### 0.4 Kenyan context for Python work

- **Money.** Kenyan shilling (KES) amounts arrive as text with thousands separators (`"1,500.00"`). Parse them to `Decimal` from strings, never from floats, and state the rounding rule explicitly (M01, M03).
- **Time.** `Africa/Nairobi` is UTC+3 all year. Store UTC, but evaluate business deadlines ("contribution due by the 5th") in Nairobi time. A payment at 01:30 on the 8th in Nairobi is still the 7th in UTC (M03).
- **Text.** Names in statements can carry non-ASCII letters (for example, Kikuyu's Ũ). Read and write UTF-8 everywhere.
- **Data protection.** Statements and member lists are personal financial data. Fixtures are synthetic or anonymised. Never paste real statements into regex testers or AI chats (V00 §5(f), L02.K01).
- **Formats.** Real M-Pesa statement layouts are verified in L02.I02 against the client's samples. Everything in this volume uses **synthetic** data with made-up column names.

---

## [C02.M01] Core refresh: types, functions, collections, comprehensions

**Tags:** Craft | Phase 1 (W1); depth pass in Phase 3 | Applied in P01.S01 | AI modes 0, 1
**Prerequisites:** C01.M01 step 3.
**Time:** 4–6 h. First pass 2.5 h: W1 Tuesday 2 h + Wednesday 0.5 h. Depth pass 2 h (W21).
**Versions targeted:** Python 3.14.

**Learning outcomes**

1. **Predict** the output of code involving mutability, aliasing, truthiness, integer and float arithmetic, and comprehension scope (drill D01.1).
2. **Choose** between list, tuple, dict and set for a job, and use comprehensions, `dict.get`, `collections.Counter` and `defaultdict` idiomatically.
3. **Write** functions with keyword-only and default parameters while avoiding the mutable-default trap.
4. **Use** `match` statements for dispatch on dict-shaped data.
5. **Explain** why floats are wrong for money, and parse KES amounts into `Decimal`.

**Core path**

| # | Item | Exact part | Time | Mode |
|---|---|---|---|---|
| 1 | Read: *The Python Tutorial* (3.14) [R-0131] | Ch. 3 (skim); ch. 4 "More Control Flow Tools": `if`, `for`, `range`, `break`/`continue`, `else` on loops, `match`, "Defining Functions", "More on Defining Functions" (default values, keyword arguments, special parameters); ch. 5 "Data Structures": list comprehensions, tuples, sets, dictionaries, looping techniques | 60 min | 1 |
| 2 | Do: Exercism Python track [R-0133] | Concept exercises for Lists, Dicts, Dict Methods, Sets, and Unpacking and Multiple Assignment | 45 min | **0** |
| 3 | Do: drill D01.1, then build task BT01.1 | — | 60 min | 0 → 1 |
| 4 | Test: quiz Q01 | — | 15 min | 0 |
| — | **Depth pass (Phase 3):** six Exercism practice exercises of your choice, and the `collections` module (`Counter`, `defaultdict`, `deque`) | — | 2 h | 0–1 |

**Supplementary:**

- CS50P lectures 0–4 (Functions/Variables to Libraries) [R-0132]. The recordings date from 2022, but core Python hasn't changed. Watch only the parts you're unsure of.
- *Automate the Boring Stuff with Python*, 3rd ed., ch. 6–8 (lists, dictionaries, strings), free online [R-0134].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0131 | *The Python Tutorial* (Python 3.14 docs) | doc | Free | A | Canonical, current, and concise for a returning engineer |
| R-0133 | Exercism Python track: 140 exercises across 17 concepts, free mentoring [V R-0133] | platform | Free | B | Small Mode 0 reps, with human mentor feedback available |
| R-0132 | CS50P (Harvard) | course + video | Free; verified certificate US$219 [V R-0132] | A | Best structured video course if you prefer lectures |

Note: Exercism's tooling targets Python 3.10–3.13 [V R-0133]. Its exercises run fine on 3.14 locally.

### Unplugged drill C02.D01.1 · Predict the output (Mode 0, 20 min)

Write each answer on paper before running anything. The answers were checked on Python 3.14.4.

```python
def add_item(item, bucket=[]):
    bucket.append(item)
    return bucket
print("1", add_item("a"), add_item("b"))

a = [1, 2]; b = a; b += [3]; print("2", a)
t = (1, [2]); t[1].append(3); print("3", t)
print("4", 0.1 + 0.2 == 0.3, round(2.5), round(3.5))

from decimal import Decimal
print("5", Decimal("0.1") + Decimal("0.2") == Decimal("0.3"), Decimal(0.1) == Decimal("0.1"))
print("6", 7 // 2, -7 // 2, 7 % 3, -7 % 3)

d = {"b": 1, "a": 2}; d["c"] = 3; print("7", list(d))
x = 10; nums = [x for x in range(3)]; print("8", x)
print("9", bool([]), bool([0]), bool(""), bool("0"), None or "default")

match {"kind": "loan", "amount": "500"}:
    case {"kind": "contribution"}: print("10 C")
    case {"kind": "loan", "amount": amt}: print("10 L", amt)
    case _: print("10 ?")

print("11", [n * n for n in range(6) if n % 2])
s = "M-PESA"; print("12", s[2:], s[::-1], s.lower().replace("-", ""))
```

### Build task C02.BT01.1 · `chama_core.rules` (applied in P01.S01)

**Spec.** A pure-Python module, with no Django yet, that applies a group's contribution rules. These rules are **illustrative**; the client's real rules replace them in P01.S01.

- `parse_amount(text: str) -> Decimal`:
  - accepts `"1,000.00"`, `"1000"` and `" 1,200.5 "`;
  - returns 2 decimal places, rounding half-up;
  - raises `ValueError` for empty text, non-numbers, negatives, NaN and infinity.
- `monthly_status(rules, payments, member, year, month) -> dict` with keys `member, due, paid, late, fine, shortfall, credit`. The rules work like this:
  - the deadline is `due_day` + `grace_days`;
  - only payments dated in the month count;
  - a member is **late** if the amount paid by the deadline is below the amount due;
  - a late member gets the fine;
  - `shortfall` is `max(0, due − paid)`; `credit` is `max(0, paid − due)`.
- `group_summary(...)` returns one row per member, sorted by member ID.

Sample data, also used by BT02.1's tests:

```python
RULES = {"monthly_amount": "1,000.00", "due_day": 5, "grace_days": 2, "late_fine": "100.00"}
MEMBERS = ["M004", "M002", "M001", "M003"]
PAYMENTS = [
    {"member": "M001", "amount": "1,000.00", "paid_on": "2026-09-28"},
    {"member": "M001", "amount": "1,000.00", "paid_on": "2026-10-03"},
    {"member": "M002", "amount": "600", "paid_on": "2026-10-06"},
    {"member": "M002", "amount": "400.00", "paid_on": "2026-10-09"},
    {"member": "M003", "amount": " 1,200.50 ", "paid_on": "2026-10-07"},
]
```

**Acceptance:** `group_summary(RULES, PAYMENTS, MEMBERS, 2026, 10)` must produce exactly this (values verified with the reference solution):

| Member | Paid | Late | Fine | Shortfall | Credit |
|---|---:|---|---:|---:|---:|
| M001 | 1000.00 | No | 0.00 | 0.00 | 0.00 |
| M002 | 1000.00 | Yes | 100.00 | 0.00 | 0.00 |
| M003 | 1200.50 | No | 0.00 | 0.00 | 200.50 |
| M004 | 0.00 | Yes | 100.00 | 1000.00 | 0.00 |

Also required: no floats anywhere; every function under 25 lines [J].

### AI exercise (Mode 1)

After your version passes the acceptance table, ask Claude to **review** it for idiom only: comprehensions, naming, edge cases. Ask it not to rewrite. Apply what you agree with and log it as AIL. The ledger itself stays hand-written (V00 never-delegate list).

### Review checklist and common mistakes

- Mutable default arguments.
- Mutating a list while looping over it.
- `Decimal(0.1)`, built from a float, instead of `Decimal("0.1")`.
- `sum()` of Decimals without a `Decimal("0")` start value: it works at runtime, but type checkers flag it (M05).
- `==` vs `is`: use `is` only for `None`.
- Comparing date *strings* instead of `date` objects.

### Kenya context notes

Chama rules vary a lot: flat versus percentage fines, grace days, rotating payouts. Keep the rules as **data** (the `RULES` dict) rather than code branches, so each group's rules can be configured. That design choice carries into P01.

### Self-check quiz C02.Q01

1. Why is `def f(x, acc=[])` a bug, and what is the idiomatic fix?
2. What is the difference between `b = a` and `b = a.copy()` for a list of lists?
3. When do you choose a tuple over a list?
4. When do you reach for `collections.Counter` or `defaultdict(int)` instead of a plain dict?
5. Code-reading: `{m: sum(x for mm, x in pays if mm == m) for m in members}`. What does it compute, and what is its cost as both lists grow?
6. Why is `0.1 + 0.2 == 0.3` false, and what do you use for KES amounts?
7. What does `round(2.5)` return, and why?
8. What is a keyword-only parameter, and why use one in money functions?
9. Debugging: a loop calls `members.remove(m)` while iterating over `members`, and some members are skipped. Why, and what's the fix?
10. What does `match` give you over `if`/`elif` for dict-shaped records?

**Portfolio output:** `chama_core/rules.py`.
**Done when:** D01.1 is checked against the key; BT01.1 matches the acceptance table; Q01 ≥ 80%.

---

## [C02.M02] Errors, pytest basics and uv project layout

**Tags:** Craft | Phase 1 (W1); depth pass in Phase 3 | Applied in P01.S01, P01.S02 | AI modes 0, 1
**Prerequisites:** C02.M01; C01.M01 (uv).
**Time:** 2–3 h. First pass 1.5 h in W1 (Wednesday). Depth pass 0.5 h.
**Versions targeted:** pytest 9.1.1, pytest-cov 7.1.0, ruff 0.16.10.

**Learning outcomes**

1. **Raise** specific exceptions with useful messages; **catch** narrowly; **use** `else`, `finally` and `raise … from`.
2. **Lay out** a uv library project with a `src/` package and a `tests/` folder, and **configure** pytest in `pyproject.toml`.
3. **Write** tests with plain `assert`, `pytest.raises`, `@pytest.mark.parametrize` and the `tmp_path` fixture.
4. **Read** a pytest failure report and **locate** the cause.
5. **Keep** `main` green with a pre-commit hook that runs ruff and the fast tests.

**Core path**

| # | Item | Exact part | Time | Mode |
|---|---|---|---|---|
| 1 | Read: *The Python Tutorial*, ch. 8 "Errors and Exceptions" [R-0131] | "Handling Exceptions", "Raising Exceptions", "Exception Chaining", "User-defined Exceptions", "Defining Clean-up Actions" | 25 min | 1 |
| 2 | Read: pytest docs [R-0135] | "Get Started" (all); "How to parametrize fixtures and test functions" (the `pytest.mark.parametrize` section); "How to use fixtures" (skim) | 30 min | 1 |
| 3 | Do: the project layout below, then build task BT02.1 | — | 45 min | 1 |
| 4 | Test: drill D02.1 and quiz Q02 | — | 20 min | 0 |
| — | **Depth pass:** Hypothesis property tests for `parse_amount` (also in C08.M02) | — | 0.5 h | 1 |

**Supplementary:**

- CS50P lecture 5, "Unit Tests" [R-0132].
- *Test-Driven Development with Python*, 3rd ed. (O'Reilly, October 2025; Python 3.14 and Django 5), ch. 1–2 [R-0136]. This is the Django-flavoured TDD book you'll lean on in C05/C08. Whether a free online edition exists is [VERIFY].
- *The Real Python Podcast*, episode "Testing Your Python Code Base: Unit vs. Integration" [R-0137].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0135 | pytest documentation (9.x) | doc | Free | A | Canonical; its "Get Started" page is short and exact |
| R-0136 | Percival, *Test-Driven Development with Python*, 3rd ed. | book | Paid; online edition [VERIFY] | A | Current for Python 3.14 and Django 5 |
| R-0137 | *The Real Python Podcast*: unit vs integration testing | podcast | Free | B | Commute-length framing of test types |

### Project layout (Wednesday of W1, 15 min)

```bash
cd ~/code
uv init --lib chama-core          # src/ layout, py.typed, a build backend
cd chama-core
uv add --dev pytest pytest-cov
mkdir tests
```

Resulting tree (checked with uv):

```
chama-core/
├── .python-version
├── pyproject.toml
├── src/chama_core/__init__.py
├── src/chama_core/py.typed
├── src/chama_core/rules.py        ← move BT01.1 here
└── tests/test_rules.py
```

Add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["tests"]          # lets tests import shared sample data
addopts = "-ra --strict-markers"
```

Why a `src/` layout: tests run against the *installed* package (uv installs the project into `.venv`), so a missing file or a broken import shows up in the tests rather than in production [J].

### Unplugged drill C02.D02.1 · Read the failure (Mode 0, 10 min)

Someone "simplified" `parse_amount`. This is the real pytest 9.1.1 output:

```text
...F.                                                                    [100%]
=================================== FAILURES ===================================
_________________ test_parse_amount_valid[1000.005-expected3] __________________

text = '1000.005', expected = Decimal('1000.01')

    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("1,000.00", Decimal("1000.00")),
            ("1000", Decimal("1000.00")),
            (" 1,200.5 ", Decimal("1200.50")),
            ("1000.005", Decimal("1000.01")),  # half-up, not banker's rounding
            ("0", Decimal("0.00")),
        ],
    )
    def test_parse_amount_valid(text, expected):
>       assert parse_amount(text) == expected
E       AssertionError: assert Decimal('1000.00') == Decimal('1000.01')
E        +  where Decimal('1000.00') = parse_amount('1000.005')

tests/test_rules.py:20: AssertionError
=========================== short test summary info ============================
FAILED tests/test_rules.py::test_parse_amount_valid[1000.005-expected3] - Ass...
1 failed, 4 passed, 11 deselected in 0.15s
```

Answer without running anything:

1. Which case failed?
2. What did the code return, and what was expected?
3. What exactly was "simplified" in the code?
4. Why did the other four cases pass?

### Build task C02.BT02.1 · Tests and a green gate for `chama_core` (applied in P01.S01–S02)

**Spec.**

- Write tests for BT01.1 in `tests/test_rules.py`, with the sample data in `tests/sample_rules.py`. At minimum:
  - parametrized valid amounts, including the half-up case;
  - parametrized invalid inputs (`""`, `"abc"`, `"-5"`, `"1.2.3"`, `"NaN"`, `"Infinity"`);
  - each sample member's outcome;
  - a payment exactly on the deadline day;
  - a member with no payments;
  - the summary's ordering and total fines.
- Add `.pre-commit-config.yaml` running `ruff check`, `ruff format` and `uv run pytest -q`.

**Acceptance criteria:**

- `uv run pytest -q --cov=chama_core --cov-report=term-missing` passes, with 100% line coverage on `rules.py`. The reference suite has 16 tests and reaches 100%.
- A commit with a failing test is blocked by the hook.

A pre-commit configuration that works with this layout:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.16.10
    hooks:
      - id: ruff-check
      - id: ruff-format
  - repo: local
    hooks:
      - id: pytest
        name: pytest (fast)
        entry: uv run pytest -q
        language: system
        pass_filenames: false
        types: [python]
```

### AI exercise (Mode 1)

After writing the tests yourself, ask Claude, "Which edge cases does this test suite miss?" Add only the cases you agree with, writing them yourself. Log it as AIL.

### Review checklist and common mistakes

- `except Exception:` around parsing, which hides real bugs.
- Tests that assert nothing, or test the implementation instead of behaviour.
- One giant test covering many cases; parametrize instead.
- Slow tests inside the pre-commit hook. Integration and end-to-end tests belong in CI (C09.M02).

### Kenya context notes

Tests are where you pin down a group's rules: grace days, fine policy, rounding. When a treasurer disputes a fine, the passing test *is* the agreed rule. Name tests in plain language the treasurer would recognise.

### Self-check quiz C02.Q02

1. Why catch `ValueError` rather than `Exception` around parsing?
2. What is the difference between `raise X from e` and `raise X from None`?
3. When does an `else` block run in `try`/`except`/`else`/`finally`, and when does `finally` run?
4. What does a `src/` layout protect you from?
5. What does `uv run pytest` guarantee that a bare `pytest` might not?
6. What does `@pytest.mark.parametrize` give you over a loop inside one test?
7. How do you assert that a function raises, and how do you check the message?
8. In D02.1, what does the ID `[1000.005-expected3]` encode?
9. What does the `tmp_path` fixture provide?
10. What belongs in a pre-commit hook, and what belongs in CI?

**Portfolio output:** the `chama-core` repository with a green test suite.
**Done when:** D02.1 is checked; BT02.1 is accepted; Q02 ≥ 80%.

---

## [C02.M03] Text and data processing: CSV, PDF, regex, Decimal, time zones

**Tags:** Craft | Phase 1 (W4); depth pass early in Phase 3 | Applied in P01.S04 | AI modes 0, 1
**Prerequisites:** C02.M01–M02.
**Time:** 3–4 h. First pass 1.5 h in W4. Depth pass 1.5 h (W21–W22).
**Versions targeted:** Python 3.14 standard library; pdfplumber 0.11.10; pypdf 6.19.0.

**Learning outcomes**

1. **Read and write** CSV with `csv.DictReader`/`DictWriter`, handling byte-order marks, quoting and thousands separators.
2. **Write** regular expressions with named groups and anchors, and **say** when a parser beats a regex.
3. **Convert** money text to `Decimal` with an explicit rounding mode.
4. **Parse** local timestamps as `Africa/Nairobi`, **store** them in UTC, and **evaluate** deadlines in local time.
5. **Extract** text and tables from a password-protected PDF with pdfplumber, and **state** the limits of doing so.

**Core path**

| # | Item | Exact part | Time | Mode |
|---|---|---|---|---|
| 1 | Read: Python docs [R-0138, R-0139, R-0140] | `csv`: `DictReader`, `DictWriter`, and the `newline=''` note. `decimal`: "Quick-start tutorial". `zoneinfo`: "Using ZoneInfo" | 35 min | 1 |
| 2 | Read: "Regular Expression HOWTO" [R-0141] | "Simple patterns", "Using regular expressions", "More pattern power" (grouping and named groups) | 25 min | 1 |
| 3 | Read: pdfplumber README [R-0142] | Python usage: `pdfplumber.open(..., password=...)`, `extract_text`, `extract_table` | 10 min | 1 |
| 4 | Do: drill D03.1, then build task BT03.1 | — | 45 min | 0 → 1 |
| 5 | Test: quiz Q03 | — | 10 min | 0 |
| — | **Depth pass:** the PDF path of BT03.1 on a synthetic password-protected statement; pypdf's "Encryption and decryption of PDFs" page [R-0143] | — | 1.5 h | 1 |

**Supplementary:**

- *Automate the Boring Stuff with Python*, 3rd ed., free online [R-0134]: ch. 9 (regex), ch. 17 (PDF and Word documents), ch. 18 (CSV, JSON and XML).
- CS50P lectures 6–7 (File I/O, Regular Expressions) [R-0132].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0138–R-0141 | Python 3.14 docs: `csv`, `decimal`, `zoneinfo`; Regular Expression HOWTO | doc | Free | A | Exactly the standard-library tools the importer uses |
| R-0142 | pdfplumber (jsvine) | tool + doc | Free | B | Table extraction from text-based PDFs; supports passwords |
| R-0134 | Sweigart, *Automate the Boring Stuff with Python*, 3rd ed. (2025), free online under Creative Commons | book | Free online | B | Practical, current, with a dedicated PDF chapter |

### Unplugged drill C02.D03.1 · Predict, then write one pattern (Mode 0, 15 min)

Predict each line (checked on Python 3.14.4):

```python
from decimal import Decimal, ROUND_HALF_UP
print("1", Decimal("1000.005").quantize(Decimal("0.01")))
print("2", Decimal("1000.005").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
print("3", Decimal("2.675").quantize(Decimal("0.01")), round(2.675, 2))
try:
    Decimal("1,000.00")
except Exception as e:
    print("4", type(e).__name__)

from datetime import datetime
from zoneinfo import ZoneInfo
t = datetime(2026, 10, 3, 8, 14, 22, tzinfo=ZoneInfo("Africa/Nairobi"))
print("5", t.astimezone(ZoneInfo("UTC")).isoformat())
print("6", datetime.fromisoformat("2026-10-03 08:14:22").tzinfo)

import re
print("8", re.findall(r"\d+", "Paid 1,000.00 on 03/10"))
```

Line 7: write a pattern with named groups `phone` and `name` that extracts `2547******123` and `MEMBER ONE` from `"Funds received from 2547******123 - MEMBER ONE"`.

### Build task C02.BT03.1 · Statement importer prototype (applied in P01.S04)

**Spec.** Write `chama_core/statements.py` with `parse_statement_csv(path) -> tuple[list[Txn], list[RowError]]`. `Txn` and `RowError` are frozen dataclasses (a preview of M05).

Each `Txn` has:

- `receipt`;
- `at_utc`: an aware UTC datetime;
- `amount`: a positive `Decimal`;
- `direction`: `"in"` or `"out"`;
- `counterparty`: the masked phone number, if any;
- `details`.

Rules:

- Rows whose status isn't `Completed` are reported as skipped.
- A repeated receipt is reported as a duplicate. The receipt is the **idempotency key**: importing the same statement twice must never double-count.
- A row must have exactly one of `paid_in` and `withdrawn`.
- Timestamps are Nairobi local time and are converted to UTC.
- Errors are **collected, not raised**, so a treasurer sees every problem at once.

Synthetic sample (`tests/statement_sample.csv`). The column names are made up; L02.I02 maps the real ones. Save it as UTF-8. Spreadsheet exports often add a byte-order mark, so open the file with `encoding="utf-8-sig"`, which handles both cases.

```csv
receipt,completed_at,details,status,paid_in,withdrawn,balance
SYN0000001,2026-10-03 08:14:22,Funds received from 2547******123 - MEMBER ONE,Completed,"1,000.00",,"1,000.00"
SYN0000002,2026-10-06 19:02:10,Funds received from 2547******456 - MEMBER TWO,Completed,600.00,,"1,600.00"
SYN0000003,2026-10-06 21:40:00,Funds received from 2547******789 - WANJIKŨ THREE,Failed,500.00,,"1,600.00"
SYN0000004,2026-10-07 23:55:59,Funds received from 2547******789 - WANJIKŨ THREE,Completed,"1,200.50",,"2,800.50"
SYN0000004,2026-10-07 23:55:59,Funds received from 2547******789 - WANJIKŨ THREE,Completed,"1,200.50",,"2,800.50"
SYN0000005,2026-10-08 10:00:00,Payment to SUPPLIER LTD,Completed,,"350.00","2,450.50"
SYN0000006,2026-10-09 07:30:00,Funds received from 2547******456 - MEMBER TWO,Completed,400.00,,"2,850.50"
SYN0000007,2026-10-09 07:31:00,Malformed row,Completed,,,"2,850.50"
```

**Acceptance** (verified against the reference solution):

- 5 transactions, 3 errors.
- Money in: **3200.50**. Money out: **350.00**.
- `SYN0000001` at `2026-10-03T05:14:22+00:00`; `SYN0000004` at `2026-10-07T20:55:59+00:00`.
- The errors, in order: `skipped: status Failed`, `duplicate receipt`, `need exactly one of paid_in / withdrawn`.
- At least 3 tests, including the totals, the UTC conversions and the error list.

**Stretch (depth pass):** export the sample to a password-protected PDF (for example, LibreOffice's export with a password). Open it with `pdfplumber.open(path, password=...)`, read the password from an environment variable rather than code, and compare the extracted rows with the CSV path.

### AI exercise (Mode 1)

Ask Claude to explain your regex back to you token by token, then compare its explanation with your intent. Don't ask it to write the pattern. Log it as AIL.

### Review checklist and common mistakes

- Parsing money with `float()`.
- Naive datetimes stored in the database.
- Deadlines evaluated on the UTC date.
- Regex used where `csv` should parse.
- Real client statements committed as fixtures.
- Statement passwords in code.
- Failing on the first bad row instead of collecting errors.

### Kenya context notes

- Statement PDFs are commonly password-protected when emailed [VERIFY in L02.I02], so the treasurer will need to enter the password at upload.
- Never store that password.
- Process files in memory, or delete them after import, according to the retention rule agreed in P01.S00 (DPA).

### Self-check quiz C02.Q03

1. Why open CSV files with `newline=""`?
2. What does `encoding="utf-8-sig"` do when there's no byte-order mark?
3. Why does `Decimal("1,000.00")` fail, and what is the safe parse?
4. What is the default rounding mode of the `decimal` context, and why state it explicitly for money?
5. Which do you store, naive or aware datetimes, and in which zone?
6. A payment completes at 01:30 on 8 Oct in Nairobi, and the deadline is the end of 7 Oct, Nairobi time. Is it late? What would a check on the UTC date wrongly conclude?
7. What does a named group give you over a numbered one?
8. When should you not use a regex?
9. How do you open a password-protected PDF with pdfplumber, and where should the password come from?
10. Why must statement fixtures be synthetic or anonymised?

**Portfolio output:** `chama_core/statements.py` and its tests.
**Done when:** D03.1 is checked; BT03.1 meets the acceptance list; Q03 ≥ 80%.

---

## [C02.M04] Iterators, generators, decorators, context managers

**Tags:** Craft | Phase 2 (W9, W11); depth pass in Phase 3 | Applied in P02.S04 | AI modes 0, 1, 2
**Prerequisites:** C02.M01–M03.
**Time:** 5–7 h. First pass 3.5 h: W9 2 h (iterators and generators), W11 1.5 h (decorators and context managers). Depth pass 1 h (W22).
**Versions targeted:** Python 3.14 (`itertools.batched` exists from 3.12).

**Learning outcomes**

1. **Explain** the iterator protocol and why a generator can be consumed only once.
2. **Build** lazy pipelines from generator functions, generator expressions and `itertools`, and **show** with `tracemalloc` that they run in near-constant memory.
3. **Write** decorators, including decorators that take arguments, that preserve metadata with `functools.wraps`.
4. **Write** context managers with `contextlib.contextmanager` and with classes, and **explain** when an exception is suppressed.
5. **Use** `contextlib.ExitStack` and `suppress` where they simplify cleanup.

**Core path**

| # | Item | Exact part | Time | Mode |
|---|---|---|---|---|
| 1 | Read: "Functional Programming HOWTO" [R-0144] | "Iterators", "Generator expressions and list comprehensions", "Generators", "Built-in functions", "The itertools module" | 50 min | 1 |
| 2 | Read: *The Python Tutorial*, ch. 9 [R-0131] | "Iterators", "Generators", "Generator Expressions" | 15 min | 1 |
| 3 | Read: Real Python, "How to Use Generators and yield in Python" [R-0147] | The data-pipeline sections | 20 min | 1 |
| 4 | Read: `contextlib` [R-0145] and `functools.wraps` [R-0146] | `contextmanager`, `suppress`, `ExitStack`, "Using a context manager as a function decorator"; `wraps` | 30 min | 1 |
| 5 | Do: drill D04.1 (W9 part a; W11 parts b–c) | — | 25 min | **0** |
| 6 | Do: build task BT04.1 (W11) | — | 60 min | 1–2 |
| 7 | Test: quiz Q04 | — | 10 min | 0 |
| — | **Depth pass:** class-based iterators, `send()`/`yield from`, `ExitStack` recipes | — | 2.5 h | 1 |

**Supplementary:** Ramalho, *Fluent Python*, 2nd ed., the chapters on decorators and closures, iterators and generators, and `with` blocks [R-0152; chapter numbers VERIFY] (paid; V00 §8 item 6) · Exercism "Generators" concept [R-0133].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0144 | Python docs: "Functional Programming HOWTO" | doc | Free | A | Clearest official treatment of iterators and generators |
| R-0145 · R-0146 | Python docs: `contextlib`; `functools` | doc | Free | A | The reference for both patterns |
| R-0147 | Real Python: "How to Use Generators and yield in Python" | article | Free | B | Pipeline examples close to import work |

### Unplugged drill C02.D04.1 · Three tools without AI (Mode 0, 25 min)

Write and test each of these:

- (a) `chunked(iterable, size)`: a generator that yields lists of up to `size` items. It must be lazy, keep the final short batch, and reject `size < 1`. Don't use `itertools.batched`.
- (b) `retry(times, exceptions)`: a decorator that retries only the listed exceptions, re-raises after the last attempt, and preserves `__name__` and `__doc__`.
- (c) `timer()`: a context manager that yields a dict and records elapsed seconds **even when the body raises**.

The reference solutions and their tests (all passing) are in the answer key.

### Build task C02.BT04.1 · Streaming spreadsheet import (applied in P02.S04)

**Spec.** Write `import_rows(path)` for Forecourt PMO's "import from client spreadsheets" story as a pipeline:

1. `rows(path)` reads a CSV lazily.
2. `normalise(rows)` parses money and dates.
3. `validate(rows)` yields `(row, errors)` pairs.
4. `chunked(..., 500)` groups rows into batches.
5. `atomic_batch()`, a context manager, collects each batch and "commits" it to an in-memory store, or rolls it back if any row in the batch is invalid.

`@timed`, a decorator, logs the duration. The real database replaces the in-memory store in C05.

**Acceptance criteria:**

- On a 100,000-row synthetic sheet, peak traced memory (`tracemalloc`) stays **under 5 MB**. A reference streaming pipeline peaked at 0.7 MB on this machine; materialising the same rows into a list peaked at 48.4 MB.
- A batch containing an invalid row leaves the store unchanged.
- `@timed` keeps `__name__`.
- At least 6 tests.

### AI exercise (Mode 2)

Pair with Claude on the synthetic data generator for the 100,000-row sheet (test scaffolding, not product logic). Read every line, then explain the generator back and log EBL. The pipeline itself stays in Mode 1.

### Review checklist and common mistakes

- Consuming a generator twice (the second pass is silently empty).
- Wrapping a large file in `list()` "just to check".
- Decorators without `wraps`.
- Cleanup code placed before `yield` instead of in `finally`.
- An `__exit__` that returns `True` by accident and swallows errors.
- `groupby` on unsorted input.

### Kenya context notes

Client spreadsheets arrive by WhatsApp or email in mixed formats. A streaming importer that **reports every bad row with its line number** saves days of back-and-forth with a site office over mobile data.

### Self-check quiz C02.Q04

1. What is the difference between an iterable and an iterator? Why does a generator work only once?
2. What is the difference between `[f(r) for r in rows]` and `(f(r) for r in rows)` for a 2 GB file?
3. What happens to a generator function's local variables at `yield`?
4. What does `functools.wraps` copy, and why does it matter for logs and debuggers?
5. How many nested functions does a decorator that takes arguments need?
6. In a `@contextmanager` function, where must cleanup go, and why?
7. When does a class-based context manager suppress an exception?
8. What must be true of the input to `itertools.groupby`?
9. Code-reading: `g = (a for a in amounts); print(sum(g), sum(g))` prints a total, then `0`. Why?
10. Debugging: logs show every decorated function as `wrapper`. What's the fix?

**Portfolio output:** the streaming importer and the `tools.py` utilities.
**Done when:** D04.1 passes its tests; BT04.1 meets the memory and rollback criteria; Q04 ≥ 80%.

---

## [C02.M05] Typing in depth: generics, protocols, dataclasses, Pydantic

**Tags:** Craft | Phase 2 (W10, W14); depth pass in Phase 3 | Applied in P02.S06, P03 | AI modes 0, 1
**Prerequisites:** C02.M01–M04.
**Time:** 5–7 h. First pass 3.5 h: W10 2 h + W14 1.5 h. Depth pass 4.5 h (W22).
**Versions targeted:** Python 3.14 (PEP 695 generics syntax; PEP 649 deferred annotations); mypy 2.4.0; Pydantic 2.13.5.

**Learning outcomes**

1. **Annotate** with built-in generics, `X | None`, `Literal`, `TypedDict`, and the `def first[T](xs: list[T]) -> T` syntax.
2. **Define** boundaries with `typing.Protocol` (structural typing) and **depend** on protocols rather than concrete classes.
3. **Model** data with `@dataclass(frozen=True, slots=True)`, and **choose** Pydantic `BaseModel` where untrusted input needs validation.
4. **Run** `mypy --strict` on a package and **fix** errors without scattering `Any` and `# type: ignore`.
5. **Explain** what PEP 649 changed in 3.14: annotations are evaluated lazily, and `annotationlib` is the runtime API for reading them.

**Core path**

| # | Item | Exact part | Time | Mode |
|---|---|---|---|---|
| 1 | Read: mypy "Type hints cheat sheet" [R-0148] | All | 20 min | 1 |
| 2 | Read: Python docs, `typing` [R-0149] | `Protocol`, `TypedDict`, `Literal`, `TypeIs` | 20 min | 1 |
| 3 | Read: Python docs, `dataclasses` [R-0150] | "Module contents" (the `frozen`, `slots` and `kw_only` parameters), "Post-init processing", "Frozen instances", "Default factory functions" | 20 min | 1 |
| 4 | Read: Pydantic docs, "Models" [R-0151] | Basic model usage; "Validating data" (`model_validate`) | 20 min | 1 |
| 5 | Read: "What's New in Python 3.14" [R-0130] | The PEP 649/749 section | 10 min | 1 |
| 6 | Do: drill D05.1, then build task BT05.1 (start) | — | 80 min | 0 → 1 |
| — | **Depth pass:** finish BT05.1; try pyrefly on the same package and compare its messages and speed with mypy's | — | 3 h | 1 |

**Supplementary:** the typing specification at typing.python.org (the authoritative rules behind every checker) [R-0149] · CS50P lecture 8, "Object-Oriented Programming" [R-0132].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0148 | mypy docs: Type hints cheat sheet | doc | Free | A | The fastest route to everyday annotations |
| R-0149 | Python docs: `typing`; the typing specification | doc | Free | A | Canonical |
| R-0150 | Python docs: `dataclasses` | doc | Free | A | Canonical |
| R-0151 | Pydantic docs: Models (v2) | doc | Free | A | Official; used again at Django and FastAPI boundaries (C05) |

### Unplugged drill C02.D05.1 · Be the type checker (Mode 0, 20 min)

Find every type error in this file **before** running `mypy --strict`. There are five. Then run mypy and compare.

```python
from dataclasses import dataclass
from decimal import Decimal
from typing import Literal, Protocol


@dataclass(frozen=True)
class Contribution:
    member: str
    amount: Decimal
    channel: Literal["mpesa", "cash", "bank"]


class Notifier(Protocol):
    def send(self, phone: str, text: str) -> bool: ...


class SmsNotifier:
    def send(self, phone: str, text: str) -> None:
        print(phone, text)


def total(items: list[Contribution]) -> Decimal:
    return sum(c.amount for c in items)


def remind(n: Notifier, phone: str) -> bool:
    return n.send(phone, "Contribution due Friday")


c = Contribution("M001", 1000, "mpesa")
c.amount = Decimal("500.00")
remind(SmsNotifier(), "254700000000")
Contribution("M002", Decimal("200"), "airtel")
```

### Build task C02.BT05.1 · Type `chama_core` (applied in P02.S06 and P03)

**Spec.**

- Make `mypy --strict src/` pass for `rules`, `statements` and `tools`. This means replacing the untyped `dict` arguments in `rules` with a `TypedDict` or a dataclass for the rules and payments.
- Add a `StatementSource` protocol with `parse(path: Path) -> tuple[list[Txn], list[RowError]]` and make the CSV importer satisfy it, ready for the PDF importer to do the same.
- At the trust boundary, add a Pydantic model `StatementUpload` with:
  - `group_id: str`;
  - `period_start: date`;
  - `period_end: date`;
  - `source: Literal["csv", "pdf"]`;
  - a validator that rejects `period_end < period_start`.

**Acceptance criteria:**

- `uv run mypy --strict src/` reports no errors.
- No `Any` appears without a one-line comment explaining why.
- `StatementUpload.model_validate(...)` rejects a reversed period and an unknown source.
- The existing tests still pass.

### AI exercise (Mode 1)

Paste one mypy error you can't explain and ask Claude what the checker is *inferring*, not how to silence it. Log it as AIL.

### Review checklist and common mistakes

- `Optional` and `List` from `typing` in new code; use `X | None` and `list`.
- `Any` used to silence errors.
- Pydantic models used deep inside domain logic. Keep them at boundaries; domain objects are dataclasses [J].
- Mutable defaults in dataclasses; use `field(default_factory=list)`.
- `# type: ignore` without an error code.

### Kenya context notes

`Literal["mpesa", "cash", "bank"]` turns a forgotten channel (Airtel Money, for example) into a type error rather than a silent miscount. When a group adds a channel, the type checker lists every place that needs updating.

### Self-check quiz C02.Q05

1. For a function argument, why is `Sequence[str]` often better than `list[str]`?
2. What does `Decimal | None` mean, and why prefer it over `Optional[Decimal]`?
3. How does a `Protocol` differ from an abstract base class?
4. What do `frozen=True` and `slots=True` each give a dataclass?
5. When do you use a dataclass, and when a Pydantic model?
6. In D05.1, what does mypy's complaint about `Decimal | Literal[0]` mean, and what's the fix?
7. Why does mypy reject `SmsNotifier` where a `Notifier` is expected?
8. How does `Literal` help Chama's payment channels?
9. What did PEP 649 change in Python 3.14?
10. When is `Any` acceptable?

**Portfolio output:** a typed `chama_core` package with `py.typed`.
**Done when:** D05.1 is checked against the mypy output; BT05.1 is accepted; Q05 ≥ 80%.

---

## Trends Watch (C02a)

| Blip | Why it matters here | L01 ID | As of |
|---|---|---|---|
| **Python 3.15.0 final due 9 Oct 2026** [V R-0004] | Keep projects on 3.14 until Django lists 3.15 support. Then upgrade with `uv python install 3.15` and a one-line `.python-version` change, behind a green test suite | L01.B06 | 2026-10-07 |
| **Rust-based type checkers maturing** (pyrefly 1.3 stable; ty still pre-1.0) [V R-0001] | Faster checks suit agent-heavy work, where many small PRs need typing feedback in seconds. mypy remains the reference for this playbook | Proposed for L01 (Python tooling consolidation) | 2026-10-07 |
| **PEP 750 template strings (3.14)** [V R-0130] | A standard way to build safe HTML or SQL fragments from user input. Assess it for C05/C10 before relying on library support | Proposed for L01 | 2026-10-07 |

---

## Answer key

<details><summary><b>C02.D01.1</b>: outputs (Python 3.14.4)</summary>

```text
1 ['a', 'b'] ['a', 'b']
2 [1, 2, 3]
3 (1, [2, 3])
4 False 2 4
5 True False
6 3 -4 1 2
7 ['b', 'a', 'c']
8 10
9 False True False True default
10 L 500
11 [1, 9, 25]
12 PESA ASEP-M mpesa
```

Explanations:

1. The default list is created **once**, when the function is defined. Both calls append to it, and `print` shows the same list twice.
2. `b = a` makes an alias, not a copy.
3. The tuple is immutable, but the list inside it isn't.
4. Binary floats can't represent 0.1 exactly. `round` uses round-half-to-even.
5. `Decimal` built from a string is exact. `Decimal(0.1)` captures the float's binary error.
6. `//` floors towards minus infinity; `%` takes the sign of the divisor.
7. Dicts keep insertion order.
8. Comprehension variables don't leak into the surrounding scope.
9. Empty containers and empty strings are falsy; `"0"` is truthy; `or` returns the first truthy operand.
10. Mapping patterns match on the keys present, and capture `amt`.
11. The filter keeps the odd numbers.
12. Slicing and string methods.
</details>

<details><summary><b>C02.Q01</b></summary>

1. The default is evaluated once and shared between calls. Use `acc=None`, then `if acc is None: acc = []`.
2. `b = a` is an alias. `.copy()` is a shallow copy: the outer list is new, but the inner lists are still shared. Use `copy.deepcopy`, or build new inner lists.
3. For fixed-size records, hashable keys, or data that shouldn't change.
4. When counting or grouping: they remove the "check whether the key exists" boilerplate.
5. The total per member. The cost is members × payments; a single pass with `defaultdict(Decimal)` is linear.
6. Binary floating-point error. Use `Decimal` built from strings, or integer cents (C03.M02 decides which).
7. `2`, because Python rounds half to even ("banker's rounding").
8. A parameter after `*` that must be passed by name. In money functions it prevents swapping amount and days by position.
9. Removing items shifts the indexes under the loop, so items get skipped. Iterate over a copy, or build a new list.
10. Patterns that check shape and capture values in one step, with an explicit `case _` default.
</details>

<details><summary><b>C02.BT01.1</b>: reference <code>rules.py</code> (look only after your own version passes)</summary>

```python
"""Illustrative chama contribution rules (C02.BT01.1 reference). Real rules come from P01.S00."""
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENTS = Decimal("0.01")


def parse_amount(text: str) -> Decimal:
    """Parse a KES amount such as '1,000.00' or ' 1000.5 ' into a 2-dp Decimal."""
    cleaned = text.strip().replace(",", "")
    try:
        value = Decimal(cleaned)
    except InvalidOperation:
        raise ValueError(f"not an amount: {text!r}") from None
    if not value.is_finite() or value < 0:
        raise ValueError(f"not an amount: {text!r}")
    return value.quantize(CENTS, rounding=ROUND_HALF_UP)


def monthly_status(rules: dict, payments: list[dict], member: str, year: int, month: int) -> dict:
    due = parse_amount(rules["monthly_amount"])
    deadline = date(year, month, rules["due_day"]) + timedelta(days=rules["grace_days"])
    mine = [
        (date.fromisoformat(p["paid_on"]), parse_amount(p["amount"]))
        for p in payments
        if p["member"] == member
    ]
    in_month = [(d, amt) for d, amt in mine if (d.year, d.month) == (year, month)]
    paid = sum((amt for _, amt in in_month), Decimal("0.00"))
    by_deadline = sum((amt for d, amt in in_month if d <= deadline), Decimal("0.00"))
    late = by_deadline < due
    return {
        "member": member,
        "due": due,
        "paid": paid,
        "late": late,
        "fine": parse_amount(rules["late_fine"]) if late else Decimal("0.00"),
        "shortfall": max(Decimal("0.00"), due - paid),
        "credit": max(Decimal("0.00"), paid - due),
    }


def group_summary(rules: dict, payments: list[dict], members: list[str], year: int, month: int) -> list[dict]:
    return [monthly_status(rules, payments, m, year, month) for m in sorted(members)]
```
</details>

<details><summary><b>C02.D02.1</b></summary>

1. The parametrize case with ID `1000.005-expected3`: the input `"1000.005"`, which is the fourth case (index 3).
2. It returned `Decimal('1000.00')`; the test expected `Decimal('1000.01')`.
3. The `rounding=ROUND_HALF_UP` argument was removed from `quantize`, so the context default, `ROUND_HALF_EVEN`, applied.
4. Their third decimal place isn't a 5, so both rounding modes agree on them.
</details>

<details><summary><b>C02.Q02</b></summary>

1. A narrow `except` handles the failure you expect and lets real bugs surface.
2. `from e` records the original cause. `from None` hides the context, which is useful when the internal error would only confuse callers.
3. `else` runs only if the `try` raised nothing. `finally` always runs.
4. Tests passing against loose files while the installed package is broken: a missing module or a bad import.
5. It runs inside the project's locked environment, on the project's pinned Python.
6. Each case is reported separately, and one failing case doesn't hide the others.
7. `with pytest.raises(ValueError, match="not an amount"):`
8. The parameter value used to build the ID, plus the position of the expected value: case index 3.
9. A unique, empty temporary directory as a `pathlib.Path`, for that test only.
10. A pre-commit hook gets fast checks: lint, format and quick unit tests. Slow integration and end-to-end tests belong in CI.
</details>

<details><summary><b>C02.BT02.1</b>: reference tests (16 tests, 100% coverage of <code>rules.py</code>)</summary>

```python
from decimal import Decimal

import pytest

from chama_core.rules import group_summary, monthly_status, parse_amount
from sample_rules import MEMBERS, PAYMENTS, RULES


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1,000.00", Decimal("1000.00")),
        ("1000", Decimal("1000.00")),
        (" 1,200.5 ", Decimal("1200.50")),
        ("1000.005", Decimal("1000.01")),  # half-up, not banker's rounding
        ("0", Decimal("0.00")),
    ],
)
def test_parse_amount_valid(text, expected):
    assert parse_amount(text) == expected


@pytest.mark.parametrize("text", ["", "abc", "-5", "1.2.3", "NaN", "Infinity"])
def test_parse_amount_rejects(text):
    with pytest.raises(ValueError):
        parse_amount(text)


def test_on_time_member_owes_nothing():
    s = monthly_status(RULES, PAYMENTS, "M001", 2026, 10)
    assert (s["paid"], s["late"], s["fine"], s["shortfall"]) == (Decimal("1000.00"), False, Decimal("0.00"), Decimal("0.00"))


def test_partial_by_deadline_is_late_even_if_completed_later():
    s = monthly_status(RULES, PAYMENTS, "M002", 2026, 10)
    assert s["late"] and s["fine"] == Decimal("100.00") and s["shortfall"] == Decimal("0.00")


def test_payment_on_deadline_day_counts():
    s = monthly_status(RULES, PAYMENTS, "M003", 2026, 10)  # paid on the 7th = 5th + 2 grace days
    assert not s["late"] and s["credit"] == Decimal("200.50")


def test_member_without_payments():
    s = monthly_status(RULES, PAYMENTS, "M004", 2026, 10)
    assert s["late"] and s["shortfall"] == Decimal("1000.00")


def test_summary_sorted_and_complete():
    rows = group_summary(RULES, PAYMENTS, MEMBERS, 2026, 10)
    assert [r["member"] for r in rows] == ["M001", "M002", "M003", "M004"]
    assert sum(r["fine"] for r in rows) == Decimal("200.00")
```
</details>

<details><summary><b>C02.D03.1</b></summary>

```text
1 1000.00
2 1000.01
3 2.68 2.67
4 InvalidOperation
5 2026-10-03T05:14:22+00:00
6 None
8 ['1', '000', '00', '03', '10']
```

- **Line 7:** `re.compile(r"from (?P<phone>2547\*+\d{3}) - (?P<name>.+)$")` gives `m["phone"] == "2547******123"` and `m["name"] == "MEMBER ONE"`.
- **Line 3:** the `Decimal` uses round-half-to-even, giving 2.68. The float `2.675` is stored as slightly *less* than 2.675, so `round` gives 2.67.
- **Line 8:** this is why money is never parsed with a naive `\d+`.
</details>

<details><summary><b>C02.Q03</b></summary>

1. The `csv` module handles line endings itself. Without `newline=""`, quoted fields that contain newlines break, and on Windows you get blank rows.
2. Nothing harmful: it decodes ordinary UTF-8 and strips a byte-order mark only when one is present.
3. A comma isn't valid in a `Decimal` literal. Strip the thousands separators, then build the `Decimal`, then validate it.
4. `ROUND_HALF_EVEN`. Money rules (fines, interest) need a stated, agreed policy.
5. Aware datetimes, stored in UTC. Convert to `Africa/Nairobi` for display and for business rules.
6. **Late.** It is 8 Oct in Nairobi. The UTC timestamp is 22:30 on 7 Oct, so a check on the UTC date would wrongly call it on time.
7. You read groups by name, the pattern documents itself, and reordering groups doesn't break the code that reads them.
8. When the input has a real structure (CSV, JSON, HTML) that a proper parser handles.
9. `pdfplumber.open(path, password=...)`. The password comes from the user at upload, or an environment variable in tests; never from code.
10. Statements are personal financial data under the Kenya DPA. Repositories and AI tools aren't places for it.
</details>

<details><summary><b>C02.BT03.1</b>: reference <code>statements.py</code> (all three acceptance tests pass)</summary>

```python
"""Synthetic statement importer (C02.BT03.1 reference). Real column mapping comes from L02.I02."""
import csv
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

from chama_core.rules import parse_amount

NAIROBI = ZoneInfo("Africa/Nairobi")
PHONE = re.compile(r"(?P<phone>2547\*+\d{3})")


@dataclass(frozen=True, slots=True)
class Txn:
    receipt: str
    at_utc: datetime
    amount: Decimal
    direction: str  # "in" or "out"
    counterparty: str
    details: str


@dataclass(frozen=True, slots=True)
class RowError:
    line: int
    receipt: str
    reason: str


def parse_statement_csv(path: Path) -> tuple[list[Txn], list[RowError]]:
    txns: list[Txn] = []
    errors: list[RowError] = []
    seen: set[str] = set()
    with path.open(newline="", encoding="utf-8-sig") as fh:
        for line, row in enumerate(csv.DictReader(fh), start=2):
            receipt = row["receipt"].strip()
            if row["status"].strip() != "Completed":
                errors.append(RowError(line, receipt, f"skipped: status {row['status'].strip()}"))
                continue
            if receipt in seen:
                errors.append(RowError(line, receipt, "duplicate receipt"))
                continue
            paid_in, withdrawn = row["paid_in"].strip(), row["withdrawn"].strip()
            if bool(paid_in) == bool(withdrawn):
                errors.append(RowError(line, receipt, "need exactly one of paid_in / withdrawn"))
                continue
            local = datetime.fromisoformat(row["completed_at"].strip()).replace(tzinfo=NAIROBI)
            m = PHONE.search(row["details"])
            seen.add(receipt)
            txns.append(Txn(
                receipt=receipt,
                at_utc=local.astimezone(UTC),
                amount=parse_amount(paid_in or withdrawn),
                direction="in" if paid_in else "out",
                counterparty=m["phone"] if m else "",
                details=row["details"].strip(),
            ))
    return txns, errors
```
</details>

<details><summary><b>C02.D04.1</b>: reference <code>tools.py</code> and tests (all pass on 3.14.4)</summary>

```python
"""C02.D04.1 reference solutions: chunked, retry, timer."""
import functools
import time
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager


def chunked[T](iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    if size < 1:
        raise ValueError("size must be >= 1")
    batch: list[T] = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def retry(times: int, exceptions: tuple[type[BaseException], ...] = (Exception,)):
    def decorate[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
            raise AssertionError("unreachable")
        return wrapper
    return decorate


@contextmanager
def timer() -> Iterator[dict[str, float]]:
    result: dict[str, float] = {}
    start = time.perf_counter()
    try:
        yield result
    finally:
        result["seconds"] = time.perf_counter() - start
```

```python
import pytest

from chama_core.tools import chunked, retry, timer


def test_chunked_is_lazy_and_keeps_remainder():
    gen = chunked(iter(range(7)), 3)
    assert next(gen) == [0, 1, 2]
    assert list(gen) == [[3, 4, 5], [6]]


def test_chunked_rejects_bad_size():
    with pytest.raises(ValueError):
        list(chunked([1], 0))


def test_retry_succeeds_on_third_try_and_keeps_metadata():
    calls = []

    @retry(times=3, exceptions=(ConnectionError,))
    def flaky():
        """Talks to Daraja."""
        calls.append(1)
        if len(calls) < 3:
            raise ConnectionError("timeout")
        return "ok"

    assert flaky() == "ok" and len(calls) == 3
    assert flaky.__name__ == "flaky" and flaky.__doc__ == "Talks to Daraja."


def test_retry_does_not_swallow_other_errors():
    @retry(times=3, exceptions=(ConnectionError,))
    def bad():
        raise ValueError("bad input")

    with pytest.raises(ValueError):
        bad()


def test_timer_records_even_on_error():
    with pytest.raises(RuntimeError):
        with timer() as t:
            raise RuntimeError("boom")
    assert t["seconds"] >= 0
```
</details>

<details><summary><b>C02.Q04</b></summary>

1. An iterable can produce iterators on demand; an iterator is single-pass state. A generator is its own iterator, so once exhausted it stays empty.
2. The list comprehension builds every result in memory. The generator expression yields one at a time, in near-constant memory.
3. They are kept. The frame is suspended and resumes at the next `next()`.
4. `__name__`, `__doc__`, `__qualname__`, `__module__`, and `__wrapped__`. Without them, logs, debuggers and documentation tools see `wrapper`.
5. Three: factory(args) → decorator(fn) → wrapper(*args).
6. In `finally` after the `yield`, so it runs even when the body raises.
7. When `__exit__` returns a truthy value.
8. It must be sorted, or at least grouped consecutively, by the same key.
9. The first `sum` exhausts the generator.
10. Apply `functools.wraps(fn)` to the wrapper.
</details>

<details><summary><b>C02.D05.1</b>: mypy 2.4.0 <code>--strict</code> output</summary>

```text
d05.py:23: error: Incompatible return value type (got "Decimal | Literal[0]", expected "Decimal")  [return-value]
d05.py:30: error: Argument 2 to "Contribution" has incompatible type "int"; expected "Decimal"  [arg-type]
d05.py:31: error: Property "amount" defined in "Contribution" is read-only  [misc]
d05.py:32: error: Argument 1 to "remind" has incompatible type "SmsNotifier"; expected "Notifier"  [arg-type]
d05.py:32: note: Following member(s) of "SmsNotifier" have conflicts:
d05.py:32: note:     Expected:
d05.py:32: note:         def send(self, phone: str, text: str) -> bool
d05.py:32: note:     Got:
d05.py:32: note:         def send(self, phone: str, text: str) -> None
d05.py:33: error: Argument 3 to "Contribution" has incompatible type "Literal['airtel']"; expected "Literal['mpesa', 'cash', 'bank']"  [arg-type]
Found 5 errors in 1 file (checked 1 source file)
```

Fixes:

- Line 23: `sum((c.amount for c in items), Decimal("0"))`.
- Line 30: `Decimal("1000")`.
- Line 31: frozen instances are read-only, so build a new one with `dataclasses.replace(c, amount=...)`.
- Line 32: `SmsNotifier.send` must return `bool` to satisfy the protocol.
- Line 33: use a valid channel. If the group really accepts Airtel Money, add `"airtel"` to the `Literal` and handle it everywhere the checker then flags.
</details>

<details><summary><b>C02.Q05</b></summary>

1. It accepts tuples and other sequences: accept the broadest type you need, return a specific one.
2. A `Decimal` or `None`. The `|` syntax is the modern form, needs no import, and reads naturally.
3. A protocol is satisfied by any class with matching methods, with no inheritance needed. An ABC requires explicit subclassing.
4. `frozen=True` makes assignment raise `FrozenInstanceError`. `slots=True` gives fixed attributes, lower memory use, and turns typos in attribute names into errors.
5. Dataclasses for internal domain objects. Pydantic at trust boundaries (uploads, API input, files), where validation and coercion matter.
6. `sum` starts from the integer `0`, so the result might be `0` rather than a `Decimal`. Pass `Decimal("0")` as the start value.
7. Its `send` returns `None`, where the protocol requires `bool`, so the structural match fails.
8. Unknown channels become type errors, and adding a channel shows every place that must handle it.
9. Annotations are evaluated lazily, only when needed. That removes most of the need for string forward references and `from __future__ import annotations`. The `annotationlib` module reads annotations at runtime.
10. Briefly, at an untyped third-party boundary, with a comment. Otherwise prefer `object` or a precise type.
</details>


---

## Resource index (C02a)

R-0001 and R-0004 are defined in V00. New IDs run from R-0130.

| ID | Resource | Provider | Type | Cost | Checked | Verified | Used in |
|---|---|---|---|---|---|---|---|
| R-0001 | [PyPI JSON API: package versions](https://pypi.org/) | Python Software Foundation | tool | free | 2026-10-07 | yes | §0 / Trends Watch |
| R-0004 | [PEP 790: Python 3.15 release schedule (defined in V00)](https://peps.python.org/pep-0790/) | Python Software Foundation | doc | free | 2026-10-07 | yes | §0 / Trends Watch |
| R-0130 | [What's New In Python 3.14](https://docs.python.org/3/whatsnew/3.14.html) | Python docs | doc | free | 2026-10-07 | yes | C02.M05 |
| R-0131 | [The Python Tutorial (3.14)](https://docs.python.org/3.14/tutorial/) | Python docs | doc | free | 2026-10-07 | yes | C02.M01, C02.M02, C02.M04 |
| R-0132 | [CS50's Introduction to Programming with Python (CS50P)](https://cs50.harvard.edu/python/) | Harvard (D. J. Malan) | course | freemium | 2026-10-07 | yes | C02.M01, C02.M02, C02.M03, C02.M05 |
| R-0133 | [Exercism Python track (140 exercises, 17 concepts, free mentoring)](https://exercism.org/tracks/python) | Exercism | platform | free | 2026-10-07 | yes | C02.M01, C02.M04 |
| R-0134 | [Automate the Boring Stuff with Python, 3rd ed. (free online, CC licence)](https://automatetheboringstuff.com/3e) | Al Sweigart / No Starch Press | book | free | 2026-10-07 | yes | C02.M01, C02.M03 |
| R-0135 | [pytest documentation: Get Started, parametrize, fixtures](https://docs.pytest.org/en/stable/getting-started.html) | pytest-dev | doc | free | 2026-10-07 | yes | C02.M02 |
| R-0136 | [Test-Driven Development with Python, 3rd ed. (Python 3.14, Django 5)](https://www.oreilly.com/library/view/test-driven-development-with/9781098148706) | Harry Percival / O'Reilly (Oct 2025) | book | paid | 2026-10-07 | yes | C02.M02 |
| R-0137 | [The Real Python Podcast: Testing Your Python Code Base: Unit vs. Integration](https://realpython.com/podcasts/rpp/) | Real Python | podcast | free | 2026-10-07 | VERIFY | C02.M02 |
| R-0138 | [csv: CSV file reading and writing](https://docs.python.org/3/library/csv.html) | Python docs | doc | free | 2026-10-07 | yes | C02.M03 |
| R-0139 | [decimal: quick-start tutorial](https://docs.python.org/3/library/decimal.html) | Python docs | doc | free | 2026-10-07 | yes | C02.M03 |
| R-0140 | [zoneinfo: IANA time zone support](https://docs.python.org/3/library/zoneinfo.html) | Python docs | doc | free | 2026-10-07 | yes | C02.M03 |
| R-0141 | [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html) | Python docs | doc | free | 2026-10-07 | yes | C02.M03 |
| R-0142 | [pdfplumber (README: password, extract_text, extract_table)](https://github.com/jsvine/pdfplumber) | jsvine (GitHub) | tool | free | 2026-10-07 | yes | C02.M03 |
| R-0143 | [pypdf: Encryption and decryption of PDFs](https://pypdf.readthedocs.io/en/stable/user/encryption-decryption.html) | py-pdf | doc | free | 2026-10-07 | yes | C02.M03 |
| R-0144 | [Functional Programming HOWTO (iterators, generators, itertools)](https://docs.python.org/3/howto/functional.html) | Python docs | doc | free | 2026-10-07 | yes | C02.M04 |
| R-0145 | [contextlib: utilities for with-statement contexts](https://docs.python.org/3/library/contextlib.html) | Python docs | doc | free | 2026-10-07 | yes | C02.M04 |
| R-0146 | [functools (wraps)](https://docs.python.org/3/library/functools.html) | Python docs | doc | free | 2026-10-07 | yes | C02.M04 |
| R-0147 | [How to Use Generators and yield in Python](https://realpython.com/python-generators/) | Real Python | article | free | 2026-10-07 | yes | C02.M04 |
| R-0148 | [Type hints cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) | mypy docs | doc | free | 2026-10-07 | yes | C02.M05 |
| R-0149 | [typing: support for type hints (+ the typing specification at typing.python.org)](https://docs.python.org/3/library/typing.html) | Python docs / Python typing council | doc | free | 2026-10-07 | yes | C02.M05 |
| R-0150 | [dataclasses: Data Classes](https://docs.python.org/3/library/dataclasses.html) | Python docs | doc | free | 2026-10-07 | yes | C02.M05 |
| R-0151 | [Pydantic: Models (v2)](https://docs.pydantic.dev/latest/concepts/models/) | Pydantic | doc | free | 2026-10-07 | yes | C02.M05 |
| R-0152 | [Fluent Python, 2nd ed. (L. Ramalho)](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/) | O'Reilly | book | paid | 2026-10-07 | VERIFY | C02.M04 |

---

## YAML manifest

```yaml
manifest_version: 1
playbook: FSE
tsw_track: 1
volume: C02a
title: Python in Depth, Part A
version: '1.1'
date: '2026-10-26'
modules:
- id: FSE.C02.M01
  title: 'Core refresh: types, functions, collections, comprehensions'
  prerequisites: [FSE.C01.M01]
  hours: [4, 6]
  outcomes: [Predict outputs involving mutability and arithmetic, Use collections and comprehensions idiomatically, Write
      safe function signatures, Use match for dict-shaped data, Parse KES amounts as Decimal]
  ai_modes: [0, 1]
  applied_in: [FSE.P01.S01]
  resources: [R-0131, R-0132, R-0133, R-0134]
  assessments: [FSE.C02.Q01, FSE.C02.D01.1, FSE.C02.BT01.1]
- id: FSE.C02.M02
  title: Errors, pytest basics and uv project layout
  prerequisites: [FSE.C02.M01]
  hours: [2, 3]
  outcomes: [Raise and catch exceptions precisely, Lay out a uv src/ project, Write parametrized pytest tests, Read failure
      reports, Gate commits with pre-commit]
  ai_modes: [0, 1]
  applied_in: [FSE.P01.S01, FSE.P01.S02]
  resources: [R-0131, R-0132, R-0135, R-0136, R-0137]
  assessments: [FSE.C02.Q02, FSE.C02.D02.1, FSE.C02.BT02.1]
- id: FSE.C02.M03
  title: 'Text & data processing: CSV/PDF extraction, regex, Decimal, dates and time zones'
  prerequisites: [FSE.C02.M02]
  hours: [3, 4]
  outcomes: [Read CSV with BOM and separators, Write named-group regexes, Quantize money with explicit rounding, 'Store UTC,
      evaluate deadlines in Nairobi time', Extract from password-protected PDFs]
  ai_modes: [0, 1]
  applied_in: [FSE.P01.S04]
  resources: [R-0132, R-0134, R-0138, R-0139, R-0140, R-0141, R-0142, R-0143]
  assessments: [FSE.C02.Q03, FSE.C02.D03.1, FSE.C02.BT03.1]
- id: FSE.C02.M04
  title: Iterators, generators, decorators, context managers
  prerequisites: [FSE.C02.M03]
  hours: [5, 7]
  outcomes: [Explain the iterator protocol, Build constant-memory pipelines, Write metadata-preserving decorators, Write context
      managers with correct cleanup]
  ai_modes: [0, 1, 2]
  applied_in: [FSE.P02.S04]
  resources: [R-0131, R-0133, R-0144, R-0145, R-0146, R-0147, R-0152]
  assessments: [FSE.C02.Q04, FSE.C02.D04.1, FSE.C02.BT04.1]
- id: FSE.C02.M05
  title: 'Typing in depth: generics, protocols, dataclasses, Pydantic'
  prerequisites: [FSE.C02.M04]
  hours: [5, 7]
  outcomes: [Annotate with modern generics and Literal, Define Protocol boundaries, Choose dataclass vs Pydantic, Pass mypy
      --strict, Explain PEP 649]
  ai_modes: [0, 1]
  applied_in: [FSE.P02.S06, FSE.P03]
  resources: [R-0130, R-0132, R-0148, R-0149, R-0150, R-0151]
  assessments: [FSE.C02.Q05, FSE.C02.D05.1, FSE.C02.BT05.1]
resources:
- id: R-0001
  title: 'PyPI JSON API: package versions'
  provider: Python Software Foundation
  type: tool
  url: https://pypi.org/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: null
  level: null
  role: evidence
  status: active
  verified: true
- id: R-0004
  title: 'PEP 790: Python 3.15 release schedule (defined in V00)'
  provider: Python Software Foundation
  type: doc
  url: https://peps.python.org/pep-0790/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: '3.15'
  level: null
  role: evidence
  status: active
  verified: true
- id: R-0130
  title: What's New In Python 3.14
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/whatsnew/3.14.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.14
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0131
  title: The Python Tutorial (3.14)
  provider: Python docs
  type: doc
  url: https://docs.python.org/3.14/tutorial/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.14
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0132
  title: CS50's Introduction to Programming with Python (CS50P)
  provider: Harvard (D. J. Malan)
  type: course
  url: https://cs50.harvard.edu/python/
  cost: {tier: freemium, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: 2022 lectures; core Python unchanged
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0133
  title: Exercism Python track (140 exercises, 17 concepts, free mentoring)
  provider: Exercism
  type: platform
  url: https://exercism.org/tracks/python
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: tooling on Python 3.13; runs on 3.14
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0134
  title: Automate the Boring Stuff with Python, 3rd ed. (free online, CC licence)
  provider: Al Sweigart / No Starch Press
  type: book
  url: https://automatetheboringstuff.com/3e
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: 3rd ed. (2025)
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0135
  title: 'pytest documentation: Get Started, parametrize, fixtures'
  provider: pytest-dev
  type: doc
  url: https://docs.pytest.org/en/stable/getting-started.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: pytest 9.x
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0136
  title: Test-Driven Development with Python, 3rd ed. (Python 3.14, Django 5)
  provider: Harry Percival / O'Reilly (Oct 2025)
  type: book
  url: https://www.oreilly.com/library/view/test-driven-development-with/9781098148706
  cost: {tier: paid, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.14; Django 5
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0137
  title: 'The Real Python Podcast: Testing Your Python Code Base: Unit vs. Integration'
  provider: Real Python
  type: podcast
  url: https://realpython.com/podcasts/rpp/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: null
  level: beginner
  role: learning
  status: active
  verified: VERIFY
- id: R-0138
  title: 'csv: CSV file reading and writing'
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/library/csv.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.14
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0139
  title: 'decimal: quick-start tutorial'
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/library/decimal.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.14
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0140
  title: 'zoneinfo: IANA time zone support'
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/library/zoneinfo.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.14
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0141
  title: Regular Expression HOWTO
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/howto/regex.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.14
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0142
  title: 'pdfplumber (README: password, extract_text, extract_table)'
  provider: jsvine (GitHub)
  type: tool
  url: https://github.com/jsvine/pdfplumber
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: 0.11.10
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0143
  title: 'pypdf: Encryption and decryption of PDFs'
  provider: py-pdf
  type: doc
  url: https://pypdf.readthedocs.io/en/stable/user/encryption-decryption.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: pypdf 6.x
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0144
  title: Functional Programming HOWTO (iterators, generators, itertools)
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/howto/functional.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.14
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0145
  title: 'contextlib: utilities for with-statement contexts'
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/library/contextlib.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.14
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0146
  title: functools (wraps)
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/library/functools.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.14
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0147
  title: How to Use Generators and yield in Python
  provider: Real Python
  type: article
  url: https://realpython.com/python-generators/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: null
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0148
  title: Type hints cheat sheet
  provider: mypy docs
  type: doc
  url: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: mypy 2.x
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0149
  title: 'typing: support for type hints (+ the typing specification at typing.python.org)'
  provider: Python docs / Python typing council
  type: doc
  url: https://docs.python.org/3/library/typing.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.14
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0150
  title: 'dataclasses: Data Classes'
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/library/dataclasses.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.14
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0151
  title: 'Pydantic: Models (v2)'
  provider: Pydantic
  type: doc
  url: https://docs.pydantic.dev/latest/concepts/models/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Pydantic 2.13
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0152
  title: Fluent Python, 2nd ed. (L. Ramalho)
  provider: O'Reilly
  type: book
  url: https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/
  cost: {tier: paid, price: null, currency: null, checked: '2026-10-07'}
  version_targeted: Python 3.10 era; concepts current
  level: advanced
  role: learning
  status: active
  verified: VERIFY
x_first_pass:
  FSE.C02.M01:
    weeks: [1]
    h: 3
  FSE.C02.M02:
    weeks: [2]
    h: 2
  FSE.C02.M03:
    weeks: [4]
    h: 2
  FSE.C02.M04:
    weeks: [9, 11]
    h: 3.5
  FSE.C02.M05:
    weeks: [14]
    h: 3
x_depth_pass_hours: {FSE.C02.M01: 2, FSE.C02.M02: 0.5, FSE.C02.M03: 1.5, FSE.C02.M04: 2.5, FSE.C02.M05: 3}
x_tested_on: {python: 3.14.4, pytest: 9.1.1, mypy: 2.4.0, pydantic: 2.13.5, reference_tests_passing: 24}
```

---

## Handoff

```
HANDOFF: C02a
Covered: C02.M01–M05 to the §8.1 template, each with a first pass (B2 weeks: W1, W1, W4, W9+W11, W10+W14)
  and a depth pass (Phase 3); drills D01.1–D05.1 and quizzes Q01–Q05 with keys; build tasks
  BT01.1–BT05.1 applied to P01.S01, P01.S02, P01.S04, P02.S04, P02.S06 and P03. All reference
  code ran on Python 3.14.4: 24 tests passing, 100% coverage on rules.py; mypy 2.4.0 output
  captured for D05.1; streaming import measured at 0.7 MB peak vs 48.4 MB materialised.
Deferred / open items:
  - Real M-Pesa statement columns, export routes and password conventions: L02.I02, with
    the client's anonymised samples (BT03.1 currently uses synthetic columns).
  - The illustrative chama rules in BT01.1 are replaced by the client's rules in P01.S01.
  - Depth-pass hours (about 9.5 h) sit in the tracker's provisional Phase 3 weeks.
Links marked [VERIFY]: free online edition of TDD with Python 3e; Real Python Podcast episode
  URL/number; Fluent Python 2e chapter numbers and price.
Build-clock status: v1.1 re-dated to V00 v1.3 (B2). P01 runs in the CHAMA APP Project; S01 starts Wed 28 Oct, before W1, so BT01.1 is a Mode 1 reference for it (Tutor covers the gap).
AI-mode log summary: planned AIL entries for BT01.1 review (M1), BT02.1 edge cases (M1),
  regex explain (M1), BT04.1 data generator (M2, with EBL), mypy inference (M1).
Decisions made: no ADRs. Conventions: Decimal from strings with explicit ROUND_HALF_UP for
  amounts; aware UTC storage with Africa/Nairobi business rules; receipt as the import
  idempotency key; errors collected rather than raised during import; src/ layout with
  pytest config in pyproject; dataclasses inside, Pydantic at trust boundaries.
Re-scored skills: n/a until GATE-1.
Prerequisites confirmed for next volume: C11a needs nothing beyond C01; C03 (W1) builds on
  BT01.1 (rules as data) and BT03.1 (idempotent imports).
Next: C11a, starting at C11.M01 (then C03, C05a, C04; P01 when the client inputs arrive)
```
