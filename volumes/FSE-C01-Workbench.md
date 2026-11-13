# FSE-C01 · Workbench & Re-entry

**Full-Stack Development & Engineering Playbook · TSW Track 1**

| Field | Value |
|---|---|
| Strand | Craft (C) |
| Phase | 1 for M01–M03: M01–M02 done as Chama S00 build work in the week of 26 Oct, checked off in W1 (2–8 Nov); M03 in W1. M05 in W10 and W15; M04 and M06 in Phase 3 (§0.1) |
| Version / date | 1.1 · 2026-10-26 (re-dated to V00 v1.3; first issue 1.0 · 2026-10-03) |
| Versions targeted | §0.2 (checked live 2026-10-03) |
| Prerequisites | FSE-V00 v1.3 read; Ubuntu 26.04 laptop with sudo; about 120 GB free on Ubuntu (V00 §7.6) |
| Hour budget | 17–24 h (about 20 h: M01–M02 ≈ 8 h as Chama S00 build work, 2 h in W1, 10.5 h in W10–W19) |
| Applied in | P01.S00 onward. Every later sprint uses this workbench |
| AI modes | Mostly 0–1. This volume builds the habits that make Modes 2–3 safe later |

> **Re-dated 2026-10-26 (v1.1) to FSE-V00 v1.3, re-baseline B2.** Week 1 is now **Mon 2 – Sun 8 Nov 2026** (W*n* starts Mon 2 Nov + 7(*n*−1) days). Content is unchanged; only the calendar, week numbers and build cross-references moved.

Evidence labels follow V00 §0.1: **[V R-xxxx]** verified this run · **[J]** judgement · **[A]** assumption · **[VERIFY]** not verified. All code here is for learning; review and test it before relying on it.

## Contents

- §0 Volume opener: schedule, versions, Kenyan context, before-Monday checklist
- C01.M01 Ubuntu dev environment & toolchains
- C01.M02 Git & GitHub workflow
- C01.M03 The learning system: AI modes, logs, Anki, explain-backs
- C01.M04 Linux & CLI depth (Phase 3)
- C01.M05 Debugging & reading docs/errors (Phase 3; quick-start inside M01)
- C01.M06 Networking tools for developers (Phase 3)
- Trends Watch · Answer key · Resource index · YAML manifest · Handoff

---

## 0. Volume opener

### 0.1 Where the modules sit on the calendar

| Module | Planned h (range) | When | Applied in |
|---|---|---|---|
| C01.M03 Learning system | 1.5 (1–2) | **W1** (Mon 2 Nov), finished in the Saturday retro | Every week from W1 |
| C01.M01 Dev environment | 5 (4–6) | **Week of 26 Oct**, as Chama S00 build work (repo skeleton); 0.5 h check-off in W1 when `verify.sh` passes | P01.S00–S01, P02.S00 |
| C01.M02 Git & GitHub | 3 (3–4) | **Week of 26 Oct**, as S00 build work; 0.5 h check-off in W1 after the first signed PR merges | P01.S00–S05, all of P02 |
| C01.M05 Debugging | 3.5 (3–4) | **W10** (4–10 Jan) 2 h + **W15** (8–14 Feb) 1.5 h; a 30-minute quick-start sits inside M01 | P02 core review, P01 v1.1, P03 |
| C01.M04 Linux & CLI depth | 4.5 (4–5) | **W16–W17** (15–28 Feb 2027) | P03 operations; P01 backups retrofit |
| C01.M06 Networking tools | 2.5 (2–3) | **W19** (8–14 Mar 2027) | L02.X01 hosting card; P03/P05 integrations |
| **Total** | **20 (17–24)** | | |

**Scheduling note.** V00 v1.3 places C01.M05 in W10 (2 h, in time for the Forecourt core review) and W15 (1.5 h). The debugging quick-start stays inside M01 (step 6).

**Before W1 (week of 26 Oct, Build clock).** Run M01 steps 1–6 and M02 part 1 as Chama S00 work. They're the repo skeleton and environment, so the tracker doesn't count them as study hours.

**W1 running order (2–8 Nov; 14 h, V00 §12).** Anki's 10 minutes a day start Monday:

| Day | Block | Content |
|---|---|---|
| Mon | 06:00–08:00 | M03 part 1: tracker, Anki, mode rules (1 h) · run `verify.sh` and tick M01 · confirm signed commits and tick M02 |
| Tue | 06:00–08:00 | C02.M01 Python core refresh (from C02a) |
| Wed | 06:00–08:00 | C02.M01 finish (0.5 h) · C02.M02 errors, pytest, uv layout (1.5 h) |
| Thu | 06:00–08:00 | C03.M01 modelling & SQL essentials (from C03a). Chama CP-P01 MVP demo is today |
| Fri | 06:00–08:00 | C03.M01 finish (0.5 h) · C03.M02 money & double-entry ledgers, part 1 (1.5 h) |
| Sat | 07:00–08:00 | C03.M02 part 1 continued (0.5 h) · CP-P01 self-assessment (0.5 h). The rest of the morning is free in this ramp week |
| Sat | 11:30–13:30 | C11 Mode 0 block · weekly retro and logs |

### 0.2 Versions targeted (checked 2026-10-03)

| Tool | Version / state | Source |
|---|---|---|
| Ubuntu | 26.04 LTS "Resolute Raccoon", released 23 Apr 2026, standard support to Apr 2031; kernel 7.0 | [V R-0128] |
| System Python | 3.14 is Ubuntu 26.04's default `python3`, marked externally managed (PEP 668): pip refuses system-wide installs | [V R-0100] |
| uv | 0.12.23 (released 2026-10-03) | [V R-0001] |
| Python for projects | 3.14 via uv (FSE); 3.12 via uv for STRUCTURES' `strlib` | V00 §0.4, §14.1 |
| Node.js | 24 LTS via fnm; 26 LTS from 28 Oct 2026 (switch in W6, the 7–13 Dec light week, after Chama v1.0.1) | V00 §0.4 |
| Docker Engine | 29.x from Docker's apt repository, which publishes `resolute` packages; Compose plugin v5 (v5.6.0 released 2026-10-02); containerd 2.x is the default on 26.04 | [V R-0103, R-0127, R-0128] |
| PostgreSQL | `postgres:18` image. From 18 the image's data directory is `/var/lib/postgresql/18/docker` and the volume is declared at `/var/lib/postgresql` | [V R-0104] |
| Git | ≥ 2.34 is needed for SSH commit signing | [V R-0111] |
| debugpy · Django Debug Toolbar | 1.8.22 · 8.0.0 (supports Django 5.2, 6.0, 6.1) | [V R-0001] |
| pre-commit · prek | 4.6.2 · 0.5.4 (a Rust re-implementation, pre-1.0: Assess only) | [V R-0001] |
| VS Code | Current release; `chat.disableAIFeatures` hides built-in AI features and disables Copilot extensions, per user or per workspace | [V R-0106] |
| Anki | 26.09.2 (15 Sep 2026); the FSRS scheduler has been built in since 23.10 | [V R-0114] |
| React Native DevTools | Replaced Chrome DevTools from React Native 0.76; Expo SDK 57 uses it (press `j` in the Expo terminal) | [V R-0120] |

### 0.3 Kenyan context for the workbench

- **Power.** Outages interrupt installs and editing. Keep the laptop on a UPS or a full battery during `apt full-upgrade`. Commit small and often (commits are local, so they work offline), and push when the connection returns. If an upgrade is cut mid-way, `sudo dpkg --configure -a` resumes it [J].
- **Data.** W1 downloads roughly 1–3 GB: Docker images, toolchains, editor, updates [J]. Do them on home fibre rather than a mobile bundle. C07 (P01 v2, 2027) adds the Android SDK, which is larger. Pin image tags (`postgres:18`) so you don't re-pull by accident.
- **Mirrors.** KENET registers an Ubuntu mirror at `ubuntu.mirror.ac.ke`. Launchpad lists it as unofficial, and its 26.04 coverage isn't confirmed; TENET's `ubuntu.mirror.ac.za` is the nearest large official one [V R-0126]. M06's lab measures which is faster from your connection; don't switch mirrors before then.
- **Time.** Kenya is UTC+3 (EAT). Log and timestamp server-side events in UTC from day one; it saves pain when hosts and clients sit in different zones [J].
- **Client data.** Chama statements are members' personal financial data. They never go into Git repositories, test fixtures or AI chats unless anonymised first (V00 §5(f), L02.K01).

### 0.4 Before Monday

1. Back up anything you can't lose. External drive or cloud.
2. Free disk to about 120 GB on Ubuntu (V00 §7.6).
3. Have a GitHub account, with two-factor authentication on.
4. Claude Pro active, for Mode 1 tutoring.

---

## [C01.M01] Ubuntu dev environment & toolchains

**Tags:** Craft | Phase 1 | Applied in P01.S00, P01.S01, P02.S00 | AI modes 0, 1
**Prerequisites:** §0.4 done; sudo access.
**Time:** 4–6 h (planned 5 h; done as Chama S00 build work in the week of 26 Oct; checked off in W1).
**Versions targeted:** §0.2, verified 2026-10-03.

**Learning outcomes**

1. **Build** a reproducible environment on Ubuntu 26.04 from a written bootstrap, and prove it with a verify script that fails loudly when anything is missing.
2. **Explain** why the system Python is left to Ubuntu (PEP 668), and use uv to install, pin and run per-project Python (3.14 for FSE, 3.12 for `strlib`).
3. **Install** Node 24 LTS through fnm, with automatic per-project switching from `.node-version`.
4. **Run** PostgreSQL 18 in Docker on a named volume bound to localhost, and **explain** why its mount path differs from older guides.
5. **Configure** VS Code with an AI-free Mode 0 setup, and **debug** a Python script with a breakpoint.

**Core path**

| # | Item | Exact part | Time | Mode |
|---|---|---|---|---|
| 1 | Read: uv "Working on projects" guide [R-0101]; uv README [R-0102] | Guide in full; README sections "Projects", "Tools", "Python versions" | 25 min | 1 |
| 2 | Read: Docker, "Install Docker Engine on Ubuntu" [R-0103] | "Install using the apt repository", then the Linux post-install page | 20 min | 1 |
| 3 | Read: Docker Hub `postgres` image [R-0104] | "PGDATA" section only | 5 min | 1 |
| 4 | Read: fnm README [R-0105] | "Installation" and "Shell setup" | 10 min | 1 |
| 5 | Read: VS Code, "Set up GitHub Copilot" [R-0106] | "Remove AI features" section only | 5 min | 1 |
| 6 | Watch: Missing Semester 2026, "Development Environment and Tools" [R-0107] | Notes page, or the first half of the video | 30 min | 1 |
| 7 | Do: steps 1–6 below | — | 2.5 h | 1 (tutor for errors) |
| 8 | Test: drill C01.D01.1 and quiz C01.Q01 | — | 35 min | 0 |

**Supplementary:** Talk Python To Me #476, "Unified Python packaging with uv" (Sept 2024; concepts still current) [R-0108] · Missing Semester 2026, "Packaging and Shipping Code" [R-0107].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0101 | uv docs: Working on projects | doc | Free | A | Official; covers `.python-version` and `uv.lock` |
| R-0102 | uv README (GitHub) | doc | Free | A | Shortest accurate tour of the commands |
| R-0103 | Docker Docs: Engine on Ubuntu | doc | Free | A | Official; lists 26.04 support |
| R-0104 | Docker Hub: postgres image | doc | Free | A | The PG18 path change lives here |
| R-0105 | fnm README | doc | Free | B | Maintained, fast, reads `.node-version` and `.nvmrc` |
| R-0106 | VS Code docs: Remove AI features | doc | Free | A | The official switch for Mode 0 |
| R-0107 | MIT Missing Semester (2026) | course + video | Free | A | Updated 2026 edition, including agentic coding |

### Steps

**Step 1 · Disk audit (30 min, Monday)**

```bash
df -h / /home
sudo apt install -y ncdu
ncdu ~          # arrow keys to browse, q to quit
```

Target about 120 GB free on Ubuntu (V00 §7.6). Move media and VM images to external storage before continuing.

**Step 2 · System preparation (15 min)**

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y build-essential curl git ca-certificates gnupg unzip \
  ripgrep fd-find jq tree htop shellcheck direnv postgresql-client
python3 --version     # Ubuntu's own Python 3.14: leave it alone
git --version         # must be 2.34 or later for SSH signing (M02)
```

Ubuntu's Python belongs to the operating system. Never `sudo pip install` into it, and don't use `--break-system-packages` on your own machine; both can break `apt` [V R-0100]. uv gives every project its own interpreter and environment instead.

**Step 3 · Python through uv (35 min)**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# open a new terminal so ~/.local/bin is on PATH
uv --version
uv python install 3.14 3.12
uv python list --only-installed
mkdir -p ~/code && cd ~/code
uv init hello-fse && cd hello-fse
uv python pin 3.14                       # writes .python-version
uv add "django>=6.1,<6.2"
uv add --dev pytest ruff
uv run python -c "import django; print(django.get_version())"
uv tool install pre-commit              # CLI tools live outside projects
```

`uv init` creates `pyproject.toml` and `.python-version`. The first `uv run`, `uv sync` or `uv lock` creates `.venv` and `uv.lock`. Commit `uv.lock` and `.python-version`; never commit `.venv` [V R-0101]. `uv self update` upgrades uv itself when installed this way [V R-0102].

**Step 4 · Node 24 LTS through fnm (20 min)**

```bash
curl -fsSL https://fnm.vercel.app/install | bash
# check ~/.bashrc: the fnm line should read
#   eval "$(fnm env --use-on-cd --shell bash)"
exec bash
fnm install 24
fnm default 24
node --version && npm --version
```

`--use-on-cd` switches Node automatically when you enter a folder containing `.node-version` or `.nvmrc` [V R-0105]. In W6, run `fnm install 26 && fnm default 26` and update each project's `.node-version`.

**Step 5 · Docker Engine and PostgreSQL 18 (40 min)**

Follow Docker's "Install using the apt repository" steps exactly as written on [R-0103]. The page detects your codename (`resolute`) and installs `docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-buildx-plugin` and `docker-compose-plugin`. Ubuntu's own `docker.io` package lags behind upstream, so don't mix the two [V R-0103].

```bash
sudo docker run hello-world
sudo usermod -aG docker "$USER"     # then log out and back in
docker compose version              # Compose v2+ syntax: "docker compose", no hyphen
```

Membership of the `docker` group is effectively root on this machine. That's an acceptable trade on a single-user development laptop, and never acceptable on a server you share [J]. Rootless options come in C09.

```bash
docker volume create pgdata18
docker run -d --name pg18 --restart unless-stopped \
  -e POSTGRES_PASSWORD=devonly \
  -p 127.0.0.1:5432:5432 \
  -v pgdata18:/var/lib/postgresql \
  postgres:18
docker exec pg18 pg_isready -U postgres
psql "postgresql://postgres:devonly@127.0.0.1:5432/postgres" -c "select version();"
```

- **Why `/var/lib/postgresql`.** From PostgreSQL 18 the image keeps data in `/var/lib/postgresql/18/docker` and declares the volume at `/var/lib/postgresql`. Guides written for 17 and earlier mount `/var/lib/postgresql/data`, which is wrong for 18 [V R-0104].
- **Why `127.0.0.1:`.** Without it, Docker publishes port 5432 on every network interface. On café or co-working Wi-Fi, that exposes your database to everyone on the network [J].
- `devonly` is a throwaway local password. Real passwords live in `.env` files that are git-ignored (M02).

**Step 6 · Editor, Mode 0 setup and debugger quick-start (30 min)**

- Install VS Code from code.visualstudio.com [VERIFY current Ubuntu method on that page]. Add the Python, Python Debugger, Ruff, Docker and GitHub Pull Requests extensions.
- **Mode 0 switch.** In any folder used for Mode 0 drills, create `.vscode/settings.json` with the content below. It hides chat and inline suggestions and disables Copilot extensions for that workspace [V R-0106]. A dedicated VS Code profile with the same setting works too.

  ```json
  { "chat.disableAIFeatures": true }
  ```

- **Debugger quick-start.** This bridges the gap until M05.
  1. Put `breakpoint()` in a short script and run `uv run python script.py`. That drops you into `pdb`: `n` next line, `s` step in, `p var` print, `c` continue, `q` quit.
  2. In VS Code, set a breakpoint in the gutter and press F5. Inspect variables in the side panel.
  3. Read Python tracebacks from the bottom up. The last line is the error; the deepest frame in *your* code is usually where to look.
  4. For the React Native app (P01 v2, 2027), press `j` in the Expo terminal to open React Native DevTools [V R-0120].

### Unplugged drill C01.D01.1 (Mode 0, 20 min)

No AI and no internet; your own notes are allowed. For each scenario, write the cause and the fix.

1. In a fresh terminal on Ubuntu 26.04 you run `pip install requests` and get an error.
2. A colleague's compose file mounts `postgres:18` data at `/var/lib/postgresql/data`.
3. Inside a project whose `.node-version` says `24`, `node -v` prints `v22.x`.
4. `docker ps` fails with "permission denied … /var/run/docker.sock" straight after `usermod`.
5. `uv run python --version` prints 3.12 in a project you believe is on 3.14.
6. A port scan from the office Wi-Fi shows your laptop answering on 5432.

Solutions are in the answer key. **C01.D01.2** (W6 light week, 30 min): delete `hello-fse` and the `pg18` container and volume, then rebuild both using only your `workbench` README, timed.

### Build task C01.BT01.1: the `workbench` repository (applied in P01.S00)

**Spec.** A private GitHub repository holding your environment as code:

- `bootstrap.sh`: idempotent; installs or updates uv, both Pythons, fnm and Node 24, and pulls `postgres:18`. It prints instructions rather than silently running anything that needs sudo.
- `verify.sh`: checks every tool and exits non-zero on any failure.
- `README.md`: a "Rebuild in 30 minutes" section.

**Acceptance criteria:**

- **Given** a configured laptop, **when** you run `./verify.sh`, **then** every line prints PASS and the exit code is 0. It checks: uv present; Python 3.14 and 3.12 available to uv; Node major 24 (26 after W6); `docker compose version` works; `pg18` answers `pg_isready`; Git ≥ 2.34; `gh auth status` succeeds; `commit.gpgsign` is true.
- **Given** a broken tool (for example, temporarily rename `uv`), **when** you run `verify.sh`, **then** that line prints FAIL and the exit code is non-zero.
- `shellcheck *.sh` reports nothing.
- Running `bootstrap.sh` twice changes nothing the second time.
- No secrets in the repository.

A reference `verify.sh` is in the answer key. Write yours first.

### AI exercise (Mode 1)

Paste your `bootstrap.sh` into Claude and ask it to **review only**: idempotency, quoting, failure handling, anything unsafe. Ask it not to rewrite the script. Apply the fixes yourself and log the session as AIL-0001.

### Review checklist and common mistakes

- `sudo pip …` or `--break-system-packages` on your own machine.
- `sudo` in front of uv, fnm or npm (they install per-user).
- Old tutorials: `docker-compose` (the hyphenated v1 binary) or `apt install docker.io`.
- PG18 data mounted at `/var/lib/postgresql/data`.
- Database ports published on `0.0.0.0`.
- `.python-version`, `.node-version` or `uv.lock` left uncommitted; `.venv` committed.
- Secrets in scripts or shell history. Use `.env` files that are git-ignored.

### Kenya context notes

Run step 5's image pulls on fibre. If power drops mid-`apt`, run `sudo dpkg --configure -a`, then `sudo apt -f install`. Keep `workbench` pushed: it's your recovery plan if the SSD fails.

### Self-check quiz C01.Q01

1. What does PEP 668 change for you on Ubuntu 26.04, and what do you use instead?
2. Which two files must you commit for a uv project to be reproducible, and which folder must you never commit?
3. What does `--use-on-cd` add to fnm?
4. Code-reading: `docker run -p 5432:5432 …`. What is risky here, and what is the fix?
5. Where does the `postgres:18` image keep its data, and where should the volume be mounted?
6. Why install Docker from Docker's own repository rather than Ubuntu's `docker.io`?
7. What security trade-off do you accept by joining the `docker` group?
8. Debugging: `uv run` fails with "No interpreter found for Python 3.14". Name two likely causes.
9. Which VS Code setting implements Mode 0, and at which levels can it be set?
10. In `pdb`, what do `n`, `s`, `p` and `c` do?

**Portfolio output:** the `workbench` repository.
**Done when:** `verify.sh` passes; D01.1 is done and checked against the key; Q01 ≥ 80%; AIL-0001 is logged; the Mode 0 setting is in place.

---

## [C01.M02] Git & GitHub workflow

**Tags:** Craft | Phase 1 | Applied in P01.S00–S05, P02 (all sprints) | AI modes 0, 1
**Prerequisites:** C01.M01 step 2 (Git installed).
**Time:** 3–4 h (planned 3 h; done as S00 build work in the week of 26 Oct; checked off in W1).
**Versions targeted:** Git ≥ 2.34 for SSH signing [V R-0111]; GitHub as of 2026-10-03.

**Learning outcomes**

1. **Predict** the commit graph after a sequence of commits, branches, merges and rebases, including where `HEAD` and each branch point.
2. **Configure** identity, SSH authentication and SSH commit signing so GitHub marks your commits "Verified".
3. **Run** a solo pull-request cycle: short-lived branch → small commits → `gh pr create` → self-review against the template → squash-merge → delete the branch.
4. **Recover** from common mistakes (amend, soft reset, revert, reflog, stash) without losing work or rewriting shared history.
5. **Protect** `main` with the tools your GitHub plan actually allows.

**Core path**

| # | Item | Exact part | Time | Mode |
|---|---|---|---|---|
| 1 | Do: Learn Git Branching [R-0109] | Main tab: "Introduction Sequence" and "Ramping Up". Remote tab: "Push & Pull" | 60 min | **0** |
| 2 | Read: *Pro Git*, 2nd ed. [R-0110] | 2.1–2.5 (basics), 3.1–3.2 (branching, merging), 3.5–3.6 (remote branches, rebasing), 7.7 (Reset demystified) | 40 min | 1 |
| 3 | Read: GitHub Docs, "About commit signature verification" [R-0111] | "SSH commit signature verification" section | 10 min | 1 |
| 4 | Do: setup commands below and build task C01.BT02.1 | — | 50 min | 1 |
| 5 | Test: drills D02.1–D02.2 and quiz Q02 | — | 20 min | 0 |

**Supplementary:** Missing Semester 2026, "Version Control and Git" [R-0107] · *Pro Git* 7.10, "Debugging with Git" (`bisect`), used again in M05 [R-0110] · GitHub CLI manual, `gh pr` [R-0112].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0109 | Learn Git Branching | platform | Free | B | Visual graph practice; nothing beats it for the mental model |
| R-0110 | *Pro Git*, 2nd ed. (Chacon & Straub), continuously corrected online, CC BY-NC-SA 3.0 | book | Free online | A | The canonical reference; written for Git 2.x |
| R-0111 | GitHub Docs: commit signature verification | doc | Free | A | Official SSH-signing steps |
| R-0112 | GitHub CLI manual | doc | Free | A | Official `gh` reference |

### Setup (Thursday, about 1.5 h with reading)

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"      # the address on your GitHub account
git config --global init.defaultBranch main
git config --global pull.ff only            # never create surprise merge commits on pull
git config --global rebase.autoStash true

ssh-keygen -t ed25519 -C "you@example.com"  # use a passphrase
# Ubuntu's desktop keyring usually acts as ssh-agent and unlocks the key at login

# Sign commits with the same SSH key
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
git config --global tag.gpgsign true

# Let Git verify signatures locally too
echo "you@example.com $(cat ~/.ssh/id_ed25519.pub)" > ~/.ssh/allowed_signers
git config --global gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers
```

- On GitHub, add the public key **twice**: once as an *Authentication* key and once as a *Signing* key (Settings → SSH and GPG keys). GitHub accepts the same key for both roles [V R-0111].
- Install the GitHub CLI from its official instructions [VERIFY current Ubuntu steps on cli.github.com], then run `gh auth login` and choose SSH.
- Check: make a commit, run `git log --show-signature -1` (it should say "Good signature"), push, and look for "Verified" on GitHub.

### Branch protection on your plan

Rulesets (require a PR, require status checks, block force-pushes) are available on **public** repositories with GitHub Free, and on **private** repositories only with GitHub Pro, Team or Enterprise [V R-0124].

- **Client repositories are private.** On GitHub Free, use discipline, CI (C09.M02) and a local `pre-push` hook that refuses direct pushes to `main`. Save the hook as `.git/hooks/pre-push` and make it executable:

  ```bash
  #!/usr/bin/env bash
  # Refuse direct pushes to main; open a pull request instead.
  while read -r _local_ref _local_sha remote_ref _remote_sha; do
    if [[ "$remote_ref" == "refs/heads/main" ]]; then
      echo "Direct push to main blocked. Push a branch and open a PR." >&2
      exit 1
    fi
  done
  exit 0
  ```

- **Practice repository.** Make a public practice repository with a real ruleset (require a PR, block force-pushes), so you learn the feature properly.
- **Upgrade trigger.** Consider GitHub Pro once you hold two or more client repositories with CI [J; price VERIFY].

### The PR workflow you'll use for every sprint

1. Branch from an up-to-date `main`: `git switch main && git pull && git switch -c feat/ledger-postings`. Prefixes: `feat/`, `fix/`, `chore/`, `docs/`.
2. Make small commits with a Conventional Commits subject (`feat: add posting batch model`) and a body that says *why* [J].
3. Stage deliberately with `git add -p`, not `git add .`.
4. `git push -u origin HEAD`, then `gh pr create --fill`. Edit the description using the template below.
5. Self-review the diff on GitHub as if a stranger wrote it. Tick the template.
6. Squash-merge, then `git switch main && git pull && git branch -d <branch>`.

**PR template** (`.github/pull_request_template.md`):

```markdown
## What and why
## How to test
## Checklist
- [ ] Tests added/updated and passing locally
- [ ] No secrets, .env files or client data in the diff
- [ ] AI mode used: 0 / 1 / 2 / 3 (AIL id: ____)
- [ ] Explain-back needed? (EBL id: ____)
- [ ] Migrations reviewed (if any)
```

### Unplugged drills (Mode 0)

**C01.D02.1 · Graph prediction (15 min).** Start: `main` points at C2 (history C0 → C1 → C2), and HEAD is on `main`. Draw the graph after each command, marking HEAD and every branch:

1. `git switch -c feat`
2. `git commit` (makes C3)
3. `git commit` (makes C4)
4. `git switch main`
5. `git commit` (makes C5)
6. `git switch feat`
7. `git rebase main`
8. `git switch main` then `git merge feat`

Bonus: what would step 8 produce if you had skipped step 7? Check your drawing in the Learn Git Branching sandbox afterwards.

**C01.D02.2 · Recovery kata (10 min).** Give the command(s) for each:

- (a) A typo in the last commit message, not pushed.
- (b) Two commits made on `main` that belong on a feature branch, not pushed.
- (c) A bad commit already pushed to shared `main`.
- (d) Commits "lost" after a mistaken `git reset --hard`.
- (e) Half-finished edits, and you must switch branches for an urgent fix.

### Build task C01.BT02.1: Chama repository foundation (applied in P01.S00)

**Spec.** Create the private Chama repository (or repositories, if P01 splits API and app) with:

- a README;
- a `.gitignore` covering Python, Node, `.env*` (but not `.env.example`), `.venv/`, `node_modules/` and `*.sqlite3`;
- `.env.example` with placeholder values only;
- the PR template above;
- the `pre-push` hook (plus a `scripts/install-hooks.sh` that installs it, because hooks aren't versioned by default);
- signed commits.

Complete one full PR cycle using `gh`.

**Acceptance criteria:**

- GitHub shows "Verified" on every commit.
- `git check-ignore -v .env` names your `.gitignore` rule.
- A direct `git push origin main` is refused by the hook.
- One PR is squash-merged with the template filled in, and the branch is deleted.
- No client data anywhere in the repository.

### AI exercise (Mode 1)

Write five graph-prediction puzzles of your own, like D02.1. Ask Claude to check your *answers*, not to solve the puzzles for you. Every disagreement gets resolved in the Learn Git Branching sandbox, which is the source of truth. Log it as AIL-0002.

### Review checklist and common mistakes

- **Force-pushing shared branches.** If you ever must, use `--force-with-lease`, and only on your own branch.
- **A committed secret.** Rotate it immediately. Rewriting history is not enough, because clones and forks keep the old commits [J].
- **Giant commits** mixing refactors and features.
- **Merging without reading the diff** you or an agent produced.

### Kenya context notes

Git is fully offline-capable. During outages keep committing locally, then push when you're back online. Keep binaries such as statement PDFs and phone recordings out of Git; they bloat every clone over metered connections and may contain personal data.

### Self-check quiz C01.Q02

1. What is `HEAD`, and what is a "detached HEAD"?
2. After `git rebase main` on `feat`, why do the rebased commits have new IDs?
3. When do you use `git revert` instead of `git reset`?
4. Code-reading: what does `pull.ff only` prevent, and what do you do when a pull is refused?
5. Why add the same SSH key to GitHub as both an authentication key and a signing key?
6. What does `git add -p` give you that `git add .` doesn't?
7. Can a GitHub Free account enforce a ruleset on a private repository? What is your fallback?
8. Debugging: `git log --show-signature` reports "No signature" on a new commit. Name two settings to check.
9. What does `--force-with-lease` protect against?
10. Why are hooks not shared automatically when someone clones the repository, and how do you share them?

**Portfolio output:** the Chama repository history: signed commits and a clean PR trail.
**Done when:** commits show Verified; the Learn Git Branching sequences are complete; D02.1 and D02.2 are checked against the key; BT02.1 is accepted; Q02 ≥ 80%.

---

## [C01.M03] The learning system: AI modes, logs, Anki, explain-backs

**Tags:** Craft | Phase 1 | Applied in every week and every sprint | AI modes 0, 1
**Prerequisites:** V00 §1.3–§1.4 and §11.
**Time:** 1–2 h (planned 1.5 h: Monday 1.0 h, Saturday 0.5 h).

**Learning outcomes**

1. **Classify** any task into AI Mode 0–3 and **state** what you must own in each (V00 §1.3).
2. **Run** the five-step session protocol and close a week in `FSE-Tracker.csv` (V00 §11.2).
3. **Configure** Anki with FSRS, and **write** prompts that are focused, precise, consistent, tractable and effortful [V R-0113].
4. **Perform** an explain-back and score it with the EBL rubric.
5. **Explain**, in your own words, why retrieval practice and spacing beat re-reading.

**Core path**

| # | Item | Exact part | Time | Mode |
|---|---|---|---|---|
| 1 | Read: FSE-V00 §1.3, §1.4, §11 | Whole sections | 15 min | 0 |
| 2 | Read: Matuschak, "How to write good prompts" [R-0113] | From the start through the five properties of good retrieval prompts | 20 min | 1 |
| 3 | Read: Anki manual [R-0114] | "Getting Started", then "Deck Options" → FSRS | 15 min | 1 |
| 4 | Do: set up the tracker files, install Anki (desktop) and AnkiDroid (phone), enable FSRS, write the first 10 cards | — | 30 min | 1 |
| 5 | Test: drill D03.1, a recorded explain-back rehearsal, quiz Q03 | — | 10 min | 0 |

**Supplementary:**

- "Learning How to Learn" (Oakley & Sejnowski, Coursera). Free to audit; about 15 h in total. The course page shows the current certificate price. Take week 1 in a light week if you want the science in more depth [R-0115].
- *The Knowledge Project* podcast, episode with Barbara Oakley [R-0116].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0113 | Andy Matuschak, "How to write good prompts" | article | Free | B | The best practical guide to writing cards that build understanding |
| R-0114 | Anki (26.09.2) and its manual | tool + doc | Free on desktop and Android | A | FSRS scheduler built in; works offline |
| R-0115 | "Learning How to Learn" (Coursera) | course | Free to audit; certificate price on the course page | A | The most-taken learning-science MOOC |
| R-0116 | *The Knowledge Project*: Barbara Oakley | podcast | Free | B | 1-hour primer for commutes |

### Setup

1. **Tracker.** Create `FSE-Tracker.csv` with the header from V00 §11.2, plus `FSE-TRACKER.md` holding the AI-mode log and explain-back log tables. Keep both in a private `fse-tracker` repository, committed each Saturday.
2. **Anki.** Install the desktop app from the official site [R-0114] and AnkiDroid on your phone. Turn on FSRS in Deck Options → FSRS. Create the deck `FSE::C01`.
3. **Card rules** [J, building on R-0113]:
   - one idea per card;
   - ask for a reason or a prediction, not a recital;
   - no lists longer than three items;
   - write the card in your own words the same day you learn the idea.
4. **Explain-back routine.** Pick a component. With no screen, record a voice memo of 3–5 minutes covering:
   - its purpose;
   - how data flows through it;
   - how it fails;
   - how it is tested;
   - one change you'd make.

   Score each element ✓/✗ in the EBL log. Any ✗ becomes debt for the next light week.

**Example cards for this volume** (write your own; these show the shape):

| Front | Back |
|---|---|
| Where does `postgres:18` keep data, and where do you mount the volume? | `/var/lib/postgresql/18/docker`; mount at `/var/lib/postgresql` |
| Why publish Postgres as `127.0.0.1:5432:5432`? | So it isn't reachable from other machines on the network |
| `git revert` vs `git reset`: which is safe on shared `main`, and why? | revert, because it adds a new commit instead of rewriting history |
| What makes an explain-back pass? | Purpose, data flow, failure modes, tests, plus one change made, all without AI |

### Unplugged drill C01.D03.1 · Mode classification (Mode 0, 10 min)

Give the AI mode and what you must own for each task:

1. Solving a C11 graph problem.
2. Asking Claude why `docker compose up` fails, then typing the fix yourself.
3. Claude writes the DRF serializers while you write the tests.
4. An agent builds Forecourt's project-register screens from your spec.
5. Writing the ledger posting function for Chama.
6. Generating a regex for statement parsing with AI, then using it.
7. Reviewing an agent's PR on tenant permissions.
8. Explaining `bootstrap.sh` from memory.

### Build task C01.BT03.1 · Learning system live (applied in every week; first in P01.S00)

**Acceptance criteria:**

- `FSE-Tracker.csv` has W1 closed on Saturday: planned and actual hours, modes, status.
- The AI-mode log has entries AIL-0001 and AIL-0002.
- The explain-back log has EBL-0001: a rehearsal on `bootstrap.sh`.
- Anki holds at least 10 cards of your own in `FSE::C01` with FSRS on.
- The weekly calendar blocks from V00 §14.3 are created.

### AI exercise (Mode 1)

Ask Claude to generate five retrieval questions from your M01 notes. Answer them from memory, let Claude mark them, then write cards **yourself** for the questions you missed. AI-written cards skip the encoding step that makes cards work [J].

### Review checklist and common mistakes

- Logs written as a diary instead of as evidence (IDs, hours, outcomes).
- Cards copied verbatim from sources.
- An Anki backlog of more than two days (an early-warning sign, V00 §5(i)).
- Treating a failed explain-back as failure rather than data.

### Kenya context notes

AnkiDroid reviews work offline, so matatu time or a queue covers the daily 10 minutes. Sync over Wi-Fi.

### Self-check quiz C01.Q03

1. In Mode 2, what must you do before code ships?
2. Name three items on the never-delegate list (V00 §5(e)).
3. What is the Mode 0 floor across the study clock?
4. Why do retrieval practice and spacing beat re-reading?
5. Rewrite this weak card: "List the Docker install steps."
6. What does FSRS change compared with fixed review intervals?
7. Which tracker status follows two consecutive weeks under 80% of planned hours?
8. When is explain-back debt paid?

**Portfolio output:** none public. The tracker becomes TSW Track 1 data (V00 §15).
**Done when:** BT03.1 is accepted; Q03 ≥ 80%; EBL-0001 is recorded.

---

## [C01.M04] Linux & CLI depth

**Tags:** Craft | Phase 3 (W16–W17) | Applied in P03 operations; retrofitted to P01 backups | AI modes 0, 1
**Prerequisites:** C01.M01; C09.M01 (first deploy, W3).
**Time:** 4–5 h (planned 4.5 h).

**Learning outcomes**

1. **Compose** pipelines (`rg`/`grep`, `sort`, `uniq`, `cut`, `awk`, `xargs`, `jq`) that answer questions about logs and CSV exports.
2. **Write** a defensive Bash script (`set -euo pipefail`, quoting, `trap`) that passes ShellCheck.
3. **Manage** processes and services: `ps`, `htop`, signals, `systemctl`, `journalctl`, and a user-level systemd service with a timer.
4. **Explain** permissions and ownership, **fix** a permission error, and **set up** key-only SSH to a server with `~/.ssh/config`.
5. **Clear** OverTheWire Bandit levels 0–15.

**Core path**

| # | Item | Exact part | Time | Mode |
|---|---|---|---|---|
| 1 | Read or watch: Missing Semester 2026 [R-0107] | "Course Overview + Introduction to the Shell" and "Command-line Environment" (notes pages are faster than the videos) | 75 min | 1 |
| 2 | Do: OverTheWire Bandit [R-0117] | Levels 0–15. Man pages are allowed; walkthroughs are not | 90 min | **0** |
| 3 | Read: Shotts, *The Linux Command Line* [R-0118] | The chapters on permissions, processes, and the shell-scripting chapters through flow control | 45 min | 1 |
| 4 | Do: drill D04.1 and build task BT04.1 | — | 60 min | 0 → 1 |

**Supplementary:** ShellCheck's wiki pages for each warning code [R-0129] · `tldr` pages (`sudo apt install tldr`) · the systemd unit documentation (`man systemd.service`, `man systemd.timer`).

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0107 | MIT Missing Semester (2026) | course | Free | A | Current, dense, with exercises |
| R-0117 | OverTheWire Bandit (34 levels) | platform | Free | B | Real shell practice on a real server over SSH |
| R-0118 | Shotts, *The Linux Command Line*. 3rd ed., No Starch, Feb 2026 (paid); free editions on linuxcommand.org [VERIFY which edition is free] | book | Paid / free older edition | A | The standard beginner-to-intermediate text |
| R-0129 | ShellCheck | tool | Free | B | Catches the Bash bugs that bite in production |

### Unplugged drill C01.D04.1 · Log pipeline (Mode 0, 25 min)

Save the twelve lines below as `access.log`. They use documentation-only IP ranges. Answer each question with **one pipeline** and write down both the pipeline and the result.

```text
192.0.2.10 - - [12/Mar/2027:08:01:12 +0000] "GET /api/statements HTTP/1.1" 200 1532
192.0.2.10 - - [12/Mar/2027:08:01:15 +0000] "POST /api/contributions HTTP/1.1" 201 312
198.51.100.7 - - [12/Mar/2027:08:05:40 +0000] "GET /api/statements HTTP/1.1" 500 87
203.0.113.25 - - [12/Mar/2027:08:06:02 +0000] "POST /payments/c2b/confirm HTTP/1.1" 200 44
192.0.2.10 - - [12/Mar/2027:08:15:30 +0000] "GET /api/members HTTP/1.1" 200 2290
198.51.100.7 - - [12/Mar/2027:08:47:09 +0000] "GET /api/statements HTTP/1.1" 500 87
192.0.2.44 - - [12/Mar/2027:09:02:11 +0000] "GET /api/loans HTTP/1.1" 403 61
192.0.2.10 - - [12/Mar/2027:09:10:56 +0000] "GET /api/statements HTTP/1.1" 200 1532
203.0.113.25 - - [12/Mar/2027:09:12:00 +0000] "POST /payments/c2b/confirm HTTP/1.1" 502 0
198.51.100.7 - - [12/Mar/2027:09:31:45 +0000] "GET /api/statements HTTP/1.1" 200 1498
192.0.2.44 - - [12/Mar/2027:10:00:03 +0000] "POST /api/loans HTTP/1.1" 201 220
192.0.2.10 - - [12/Mar/2027:10:20:17 +0000] "GET /api/members HTTP/1.1" 304 0
```

1. Which IP made the most requests, and how many?
2. How many responses were 5xx?
3. How many requests fell in each hour?
4. Which paths returned 5xx, and how often each?
5. What is the total number of response bytes?
6. How many distinct IPs requested `/api/statements`?

Then write one sentence on what an operator should investigate first.

### Build task C01.BT04.1 · `backup-db.sh` with a systemd timer (applied in P03 operations; retrofit to P01)

**Spec.** A ShellCheck-clean script that:

- runs `pg_dump -Fc` inside the database container;
- writes `backups/<db>-<UTC timestamp>.dump`;
- keeps the newest 14 dumps and deletes older ones;
- logs to journald (`systemd-cat` or stdout under systemd);
- exits non-zero on any failure.

Run it daily from a **user** systemd service and timer pair (`~/.config/systemd/user/`).

**Acceptance criteria:**

- `systemctl --user list-timers` shows the timer.
- `journalctl --user -u backup-db` shows successful runs.
- Each dump passes `pg_restore --list`.
- A deliberately wrong DB name makes the unit fail visibly.
- `shellcheck backup-db.sh` is clean.
- The script has `set -euo pipefail` and quotes every variable.

C09.M03 adds off-site copies and restore drills. This task is the local half.

### AI exercise (Mode 1)

After finishing BT04.1 yourself, ask Claude to list failure modes the script doesn't handle: disk full, container stopped, partial dumps. Add tests or guards for two of them, and log the session.

### Review checklist and common mistakes

- Unquoted variables (`rm -rf $DIR/` with an empty `DIR`).
- Missing `pipefail`, which hides failures inside pipelines.
- Parsing `ls` output.
- Cron jobs that can't find the PATH.
- `chmod 777` as a "fix".
- Password logins left on servers.

### Kenya context notes

On a Nairobi VPS, unattended timers must survive reboots after power events at the data centre. Check `systemctl --user` lingering (`loginctl enable-linger`) so user timers run without an active login [J].

### Self-check quiz C01.Q04

1. What does each of `set -e`, `set -u` and `set -o pipefail` change?
2. Code-reading: `for f in $(ls *.dump); do rm $f; done`. Name two bugs.
3. What is the difference between `SIGTERM` and `SIGKILL`, and why send TERM first?
4. Translate `chmod 640 secrets.env` into who can do what.
5. Which command shows a unit's logs since the last boot?
6. Why does a user-level timer need lingering enabled on a server?
7. What does `xargs -0` pair with, and why?
8. Debugging: a script works in your terminal but fails under systemd with "command not found". What is the likely cause?

**Portfolio output:** `backup-db.sh` plus its unit files in the ops folder of the P03 repository.
**Done when:** Bandit level 15 is cleared; D04.1 is checked against the key; BT04.1 is accepted; Q04 ≥ 80%.

---

## [C01.M05] Debugging & reading docs and errors

**Tags:** Craft | Phase 2–3 (W10, W15); quick-start in C01.M01 step 6 | Applied in the P02 core review, P01 v1.1, P03 | AI modes 0, 1
**Prerequisites:** C01.M01; C05.M01–M02; C07.M01.
**Time:** 3–4 h (planned 3.5 h).

**Learning outcomes**

1. **Apply** a written debugging loop (reproduce → isolate → hypothesise → test → fix → add a regression test) and record it.
2. **Use** `pdb`/`breakpoint()` and the VS Code debugger on a Django view, and **use** Django Debug Toolbar to find an N+1 query.
3. **Use** React Native DevTools (`j` in the Expo terminal) to inspect the console, network requests and components.
4. **Read** a Python traceback and a JavaScript stack trace, and **find** the first frame in your own code.
5. **Find** a regression commit with `git bisect`.
6. **Navigate** official documentation fast: version selector, guides vs reference, release notes, issue trackers.

**Core path**

| # | Item | Exact part | Time | Mode |
|---|---|---|---|---|
| 1 | Read or watch: Missing Semester 2026, "Debugging and Profiling" [R-0107] | Notes, plus the video's debugging half | 45 min | 1 |
| 2 | Read: Python `pdb` docs [R-0119] | Debugger commands table | 15 min | 1 |
| 3 | Read: Expo, "Debugging and profiling tools" [R-0120] | "Debugging with React Native DevTools" | 15 min | 1 |
| 4 | Read: Django Debug Toolbar install page [R-0121] | Installation and the SQL panel | 10 min | 1 |
| 5 | Read: *Pro Git* 7.10, "Debugging with Git" [R-0110] | `git bisect` section | 10 min | 1 |
| 6 | Do: drills D05.1–D05.2 and build task BT05.1 | — | 90 min | 0 → 1 |
| 7 | Test: quiz Q05 | — | 15 min | 0 |

**Supplementary:** Missing Semester 2026, "Code Quality" [R-0107].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0119 | Python docs: `pdb` | doc | Free | A | Canonical |
| R-0120 | Expo Docs: Debugging and profiling tools | doc | Free | A | Official path to React Native DevTools; RN ≥ 0.76 |
| R-0121 | django-debug-toolbar 8.0.0 (PyPI) | tool | Free | B | Supports Django 6.1; shows SQL per request |

Note: React Native DevTools opens in Chrome or Edge, so install a Chromium-based browser on Ubuntu [V R-0120].

### Unplugged drills (Mode 0)

**C01.D05.1 · Find the bug with `pdb` only (20 min).** No AI and no print statements: use `breakpoint()`. Save these two files and run `uv run pytest -q`.

```python
# ledger.py
from decimal import Decimal

def member_balance(entries, member_id):
    """Net position of a member: contributions minus loans plus repayments."""
    balance = Decimal("0")
    for e in entries:
        if e["member"] == member_id:
            if e["kind"] == "contribution":
                balance += Decimal(e["amount"])
            elif e["kind"] == "loan":
                balance -= Decimal(e["amount"])
            elif e["kind"] == "repayment":
                balance -= Decimal(e["amount"])
    return balance
```

```python
# test_ledger.py
from decimal import Decimal
from ledger import member_balance

ENTRIES = [
    {"member": "M001", "kind": "contribution", "amount": "1000.00"},
    {"member": "M001", "kind": "loan", "amount": "500.00"},
    {"member": "M002", "kind": "contribution", "amount": "750.00"},
    {"member": "M001", "kind": "repayment", "amount": "200.00"},
]

def test_balance_after_partial_repayment():
    assert member_balance(ENTRIES, "M001") == Decimal("700.00")
```

Record the loop: symptom, hypothesis, the evidence from `pdb`, the fix, and a second test you'd add. Then answer: why is a simple running balance the wrong design for Chama's ledger (C03.M02)?

**C01.D05.2 · Read the traceback (10 min).** Name the first frame in *your* code, the root cause, and the fix.

```text
Traceback (most recent call last):
  File ".../django/core/handlers/exception.py", line 55, in inner
    response = get_response(request)
  File ".../django/core/handlers/base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/home/gashu/code/chama-api/contributions/views.py", line 41, in record_contribution
    Contribution.objects.create(member=member, amount=data["amount"], period=period)
  File ".../django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File ".../django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
django.db.utils.IntegrityError: null value in column "group_id" of relation "contributions_contribution" violates not-null constraint
```

### Build task C01.BT05.1 · `DEBUGGING.md` notebook (applied in P01 v1.1 and P03)

**Spec.** In the active product repository, record three real bugs using the loop. Each entry has:

- the symptom and repro steps;
- the hypotheses, ranked;
- the evidence: debugger, logs, Toolbar SQL panel or DevTools;
- the fix commit;
- a regression test;
- the time spent.

**Acceptance criteria:**

- Three entries.
- Each regression test fails on the parent of the fix commit and passes after it (show `git stash` / `git switch --detach <parent>` evidence).
- At least one entry uses React Native DevTools.
- At least one uses Django Debug Toolbar or `git bisect`.

### AI exercise (Mode 1) · hypothesis calibration

For one real bug, ask Claude only for **ranked hypotheses**, not fixes. Test them yourself. Record in the AIL log whether Claude's top hypothesis was right. After five bugs you'll know how far to trust AI triage on your stack [J].

### Review checklist and common mistakes

- Changing code before you can reproduce the bug.
- Fixing the symptom instead of the cause.
- No regression test.
- Reading the top of a Python traceback instead of the bottom.
- Searching error text without the version of the tool you're on.
- `print` debugging left in commits.

### Kenya context notes

Bugs that only appear on cheap Android phones or slow networks need reproducing on those conditions: the physical test phone, or network throttling in DevTools. That's where the Chama users are.

### Self-check quiz C01.Q05

1. What are the six steps of the debugging loop, in order?
2. In a Python traceback, where is the exception, and which frame do you usually inspect first?
3. What does `breakpoint()` do, and how do you disable it without editing code? (Hint: an environment variable.)
4. How does Django Debug Toolbar reveal an N+1 query?
5. How do you open React Native DevTools from an Expo session?
6. What does `git bisect` need from you at each step?
7. Code-reading: `except Exception: pass`. What debugging harm does it do?
8. Why should every bug fix arrive with a test that fails before the fix?

**Portfolio output:** `DEBUGGING.md`.
**Done when:** D05.1 and D05.2 are checked; BT05.1 is accepted; Q05 ≥ 80%.

---

## [C01.M06] Networking tools for developers

**Tags:** Craft | Phase 3 (W19) | Applied in the L02.X01 hosting-card refresh, P03 integrations (Daraja, eTIMS) and P05 | AI modes 0, 1
**Prerequisites:** C01.M04; a deployed VPS from C09.M01.
**Time:** 2–3 h (planned 2.5 h).

**Learning outcomes**

1. **Trace** what happens between a URL and a response (DNS → TCP → TLS → HTTP), and **estimate** the round trips involved.
2. **Use** `dig`, `curl -w` timings, `openssl s_client` and `mtr` to measure and diagnose.
3. **Measure** latency from your own connection to Nairobi, Johannesburg/Cape Town and Frankfurt endpoints, and record it in L02.X01.
4. **Diagnose** typical failures (DNS, expired certificate, closed port, 4xx/5xx), including why a Daraja callback never arrives.

**Core path**

| # | Item | Exact part | Time | Mode |
|---|---|---|---|---|
| 1 | Read: *High Performance Browser Networking* [R-0122] | Ch. 1 "Primer on Latency and Bandwidth"; ch. 4 "Transport Layer Security" | 45 min | 1 |
| 2 | Read: *Everything curl* [R-0123] | "Using curl": verbose and trace options; the `-w` write-out variables | 20 min | 1 |
| 3 | Do: lab below, drill D06.1, build task BT06.1 | — | 70 min | 0 → 1 |
| 4 | Test: quiz Q06 | — | 15 min | 0 |

*Version flag:* *High Performance Browser Networking* dates from 2013, with light updates since. Its TLS chapter describes the TLS 1.2 handshake: treat it as **older version, concepts only**. TLS 1.3 completes a full handshake in one round trip [J].

**Resource table**

| ID | Resource | Type | Cost | Tier | Why this one |
|---|---|---|---|---|---|
| R-0122 | Grigorik, *High Performance Browser Networking* (hpbn.co, free online) | book | Free | A | The clearest explanation of latency for developers |
| R-0123 | Stenberg, *Everything curl* (everything.curl.dev, CC BY 4.0) | book | Free | A | By curl's author; continuously maintained |

### Lab (40 min)

```bash
sudo apt install -y mtr-tiny bind9-dnsutils
dig +short api.github.com
curl -sS -o /dev/null \
  -w 'dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total} code=%{http_code}\n' \
  https://example.com
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
mtr -rwzc 50 example.com
```

Measure three targets at morning, midday and evening peak:

- your Nairobi VPS (C09.M01);
- `ec2.af-south-1.amazonaws.com` (Cape Town);
- `ec2.eu-central-1.amazonaws.com` (Frankfurt).

Regional API endpoints are used because CDN-fronted sites answer from a nearby edge and would mislead you [J]. Add the medians to L02.X01.

**Mirror check.** Time `sudo apt update` against `archive.ubuntu.com`, `ubuntu.mirror.ac.ke` and `ubuntu.mirror.ac.za`. Switch only if a mirror is both faster and lists `resolute`.

### Unplugged drill C01.D06.1 · Read the timings (Mode 0, 15 min)

`curl -w` reports cumulative seconds. Two hosts served the same API.

```text
Host A (Nairobi VPS):  dns=0.012 connect=0.020 tls=0.030 ttfb=0.150 total=0.152
Host B (Frankfurt VPS): dns=0.015 connect=0.160 tls=0.310 ttfb=0.570 total=0.575
```

1. Estimate the round-trip time to each host.
2. Roughly how many round trips did each TLS handshake take, and what does that suggest about the TLS version?
3. Estimate the server processing time on each host. Is it the network or the server that differs?
4. A screen makes six sequential API calls. Estimate the network overhead on Host B if every call opens a new connection, versus reusing one connection. What does that imply for the Chama app?

### Build task C01.BT06.1 · `netcheck.sh` (applied in the L02.X01 refresh, P03 and P05)

**Spec.** A ShellCheck-clean script that reads `endpoints.txt` and appends one CSV row per endpoint per run, with these columns:

`utc_timestamp, host, dns_s, connect_s, tls_s, ttfb_s, total_s, http_code, cert_days_left`

A user timer runs it hourly for seven days.

**Acceptance criteria:**

- At least 150 rows collected.
- A one-paragraph summary of median and 95th-percentile total time per region, added to the L02.X01 notes.
- Certificate days-left is computed correctly for your own domain.
- The script exits non-zero when any endpoint is unreachable, but still writes the other rows.

### AI exercise (Mode 1)

Give Claude your seven-day CSV summary, **not the raw data**, and ask what hosting conclusion it supports and what it can't tell you. Compare its answer with V00 §6.6, and log any disagreement.

### Review checklist and common mistakes

- Measuring once, at midnight, and generalising.
- Testing CDN-fronted hosts.
- Confusing bandwidth with latency.
- Ignoring certificate expiry until clients see errors.
- Callback URLs containing words Daraja rejects, or served without HTTPS (L02.I01) [V R-0025].

### Kenya context notes

Results vary by ISP (fibre vs 4G) and time of day. Record the network you used with each run. Your users are mostly on mobile data, so the Chama app's real latency is your 4G figure, not your fibre figure.

### Self-check quiz C01.Q06

1. Name the four steps from URL to response, in order.
2. Why does latency, not bandwidth, usually dominate API-heavy mobile apps?
3. What does `time_appconnect` measure in `curl -w`?
4. Which command shows a certificate's expiry dates?
5. What does `mtr` show that `ping` doesn't?
6. Why can CDN-fronted hosts mislead a hosting-latency test?
7. Debugging: `dig` returns NXDOMAIN for your new subdomain. Name two likely causes.
8. Why does connection reuse (keep-alive) matter more on a 145 ms link than on an 8 ms link?

**Portfolio output:** the `netcheck.sh` dataset and the latency summary in L02.X01.
**Done when:** the lab is recorded; D06.1 is checked; BT06.1 is accepted; Q06 ≥ 80%.

---

## Trends Watch (C01)

| Blip | Why it matters for your workbench | L01 ID | As of |
|---|---|---|---|
| **Astral (uv, Ruff, ty) joined OpenAI** (Talk Python To Me, 17 Jun 2026) [V R-0125] | uv stays open source, and your projects use standard `pyproject.toml`, so lock-in is low: plain `pip` + `venv` remains a working fallback. Watch the licence and governance at each L01 refresh | Proposed for L01 (Python tooling consolidation) | 2026-10-03 |
| **Missing Semester's 2026 edition adds "Agentic Coding" and "Code Quality"** [V R-0107] | Tooling literacy now includes agents. C13.M02 draws on the agentic-coding lecture | L01.B01 | 2026-10-03 |
| **Docker Compose v5 and containerd 2.x as default on Ubuntu 26.04** [V R-0127, R-0128] | Tutorials using `docker-compose` (v1) or Ubuntu's `docker.io` mislead. Combined with the PostgreSQL 18 volume change, copy-pasted compose files can silently break | Proposed for L01 (container runtime churn) | 2026-10-03 |

---

## Answer key

<details><summary><b>C01.D01.1</b>: environment scenarios</summary>

1. Ubuntu marks its Python as externally managed (PEP 668), so pip refuses to install system-wide [V R-0100]. Use a uv project (`uv add requests`) or `uv tool install` for command-line tools.
2. For `postgres:18`, the volume belongs at `/var/lib/postgresql`. The old `/var/lib/postgresql/data` mount is wrong for 18 [V R-0104]. Fix the compose file and recreate the container.
3. The shell isn't running `fnm env --use-on-cd` (the `~/.bashrc` line is missing, or the shell wasn't reloaded), or Node 24 isn't installed (`fnm install`). Fix `~/.bashrc`, run `exec bash`, then `cd` into the folder again.
4. Group membership only applies to new login sessions. Log out and back in (or use `newgrp docker` for one shell).
5. Something pins 3.12: the project's `.python-version`, a `.python-version` in a parent folder, or a `UV_PYTHON` environment variable. Check with `cat .python-version` and `uv python find`, and make sure `requires-python` in `pyproject.toml` allows 3.14.
6. The port was published on all interfaces. Recreate the container with `-p 127.0.0.1:5432:5432`. Optionally enable `ufw` and deny inbound traffic by default.
</details>

<details><summary><b>C01.Q01</b></summary>

1. `pip` won't install into the system Python. Use uv-managed interpreters and per-project environments (`uv add`, `uv run`), and `uv tool install` for command-line tools.
2. Commit `uv.lock` and `.python-version` (alongside `pyproject.toml`). Never commit `.venv`.
3. Automatic `fnm use` whenever you enter a folder with `.node-version` or `.nvmrc`.
4. It publishes 5432 on every interface, so the database is reachable from the network. Use `-p 127.0.0.1:5432:5432`.
5. Data lives in `/var/lib/postgresql/18/docker`; mount the volume at `/var/lib/postgresql`.
6. Ubuntu's `docker.io` lags upstream. Docker's repository ships current Engine, Compose and Buildx with fixes. Don't mix the two sources.
7. Membership is effectively root: any process running as you can control the host through Docker.
8. Any two of:
   - 3.14 isn't installed through uv (`uv python install 3.14`);
   - you're offline, so uv can't download it;
   - `requires-python` excludes 3.14, or a stale `.python-version` pins something else;
   - an outdated uv (`uv self update`).
9. `chat.disableAIFeatures`, set per user or per workspace (and therefore per profile).
10. `n` runs the next line (stepping over calls); `s` steps into a call; `p` prints an expression; `c` continues to the next breakpoint.
</details>

<details><summary><b>C01.BT01.1</b>: reference <code>verify.sh</code> (look only after your own attempt; passes ShellCheck)</summary>

```bash
#!/usr/bin/env bash
# shellcheck disable=SC2317  # helper functions are called indirectly through check()
# verify.sh: check the FSE workbench; exit non-zero if any check fails.
# No `set -e`: we want every check to run and report, not stop at the first failure.
set -uo pipefail

fail=0

check() {
  local name="$1"; shift
  if "$@" >/dev/null 2>&1; then
    printf 'PASS  %s\n' "$name"
  else
    printf 'FAIL  %s\n' "$name"
    fail=1
  fi
}

node_major_ok() {
  local want="${NODE_MAJOR:-24}" got
  got="$(node --version 2>/dev/null)" || return 1
  got="${got#v}"
  [[ "${got%%.*}" == "$want" ]]
}

git_version_ok() {
  local v major minor
  v="$(git --version | awk '{print $3}')" || return 1
  major="${v%%.*}"
  minor="$(cut -d. -f2 <<<"$v")"
  (( major > 2 || (major == 2 && minor >= 34) ))
}

signing_on() {
  [[ "$(git config --global --get commit.gpgsign)" == "true" ]]
}

check "uv installed"                       command -v uv
check "Python 3.14 available to uv"        uv python find 3.14
check "Python 3.12 available to uv"        uv python find 3.12
check "Node major ${NODE_MAJOR:-24}"       node_major_ok
check "docker compose plugin"              docker compose version
check "pg18 accepting connections"         docker exec pg18 pg_isready -U postgres
check "git >= 2.34"                        git_version_ok
check "gh authenticated"                   gh auth status
check "commit signing enabled"             signing_on

exit "$fail"
```

`NODE_MAJOR=26 ./verify.sh` checks for Node 26 after the W6 switch.
</details>

<details><summary><b>C01.D02.1</b>: graph prediction</summary>

After step 7, the original C3 and C4 are rewritten as C3′ and C4′ on top of C5. The history reads C0 → C1 → C2 → C5 → C3′ → C4′:

- `main` points at C5;
- `feat` points at C4′;
- HEAD is on `feat`.

The old C3 and C4 are no longer on any branch, but stay reachable through `git reflog` for a while.

After step 8, `main` fast-forwards to C4′ and HEAD is on `main`. The history is linear, with no merge commit.

**Bonus:** without the rebase, `git merge feat` on `main` creates a merge commit C6 whose parents are C5 and C4.
</details>

<details><summary><b>C01.D02.2</b>: recovery kata</summary>

- (a) `git commit --amend`
- (b) On `main`: `git branch feat`, then `git reset --hard origin/main`, then `git switch feat`. This assumes `origin/main` is the correct base.
- (c) `git revert <sha>`, then push. Never rewrite shared history.
- (d) `git reflog` to find the commit, then `git branch rescue <sha>` (or `git reset --hard <sha>` if you're sure).
- (e) `git stash push -m "wip"` → switch branches and do the fix → switch back → `git stash pop`.
</details>

<details><summary><b>C01.Q02</b></summary>

1. HEAD is the pointer to what you have checked out, normally a branch. "Detached HEAD" means it points straight at a commit, so new commits belong to no branch.
2. A rebase replays each change onto a new parent. A commit's ID depends on its parent and content, so every replayed commit gets a new ID.
3. Use `revert` for anything already shared, because it adds an inverse commit. Use `reset` only on local, unpushed history.
4. It stops `git pull` creating a merge commit when the branches have diverged. When a pull is refused, rebase your work onto the remote (`git pull --rebase`), then push.
5. GitHub tracks the two roles separately: authentication lets you push; a signing key lets GitHub verify your commit signatures. The same key can be uploaded for both [V R-0111].
6. Hunk-by-hunk review before staging: focused commits, and stray debug code or secrets get caught.
7. No. Rulesets on private repositories need Pro, Team or Enterprise [V R-0124]. Fall back on a `pre-push` hook, CI checks and discipline, or upgrade.
8. Any two of `commit.gpgsign`, `gpg.format ssh`, and `user.signingkey` pointing at the right `.pub` file. For local verification, also `gpg.ssh.allowedSignersFile`.
9. It refuses to overwrite remote commits you haven't fetched, such as someone else's push.
10. `.git/hooks` isn't tracked. Share hooks through a tracked folder plus an install script, `core.hooksPath`, or a framework such as pre-commit.
</details>

<details><summary><b>C01.D03.1</b>: mode classification</summary>

1. **Mode 0.** You own everything.
2. **Mode 1.** The AI explains; you type and own the fix.
3. **Mode 2.** Read every line, own the tests, pass an explain-back before shipping.
4. **Mode 3.** You own the spec, ADRs, review, tests, security checks and deployment, plus explain-backs for what ships.
5. **Mode 1.** Ledger posting is on the never-delegate list, so you write it and AI may only tutor.
6. **Mode 2.** You must understand the regex, add tests using anonymised real statement lines, and explain it back.
7. **Mode 2-level ownership.** Tenant permissions are never-delegate: review line by line and own the tests. If an agent wrote the code, add an explain-back and rebuild a slice in the next light week (C10.D02.1).
8. **Mode 0.**
</details>

<details><summary><b>C01.Q03</b></summary>

1. Read every line, write or own the tests, and pass an explain-back.
2. Any three of: ledger posting and balance logic; reconciliation matching rules; authentication, authorisation and tenant isolation; secrets and payment credentials; data-protection decisions; production data migrations and restores; security-sensitive configuration; children's-data features.
3. At least 15% of study hours.
4. Effortful recall strengthens memory more than re-exposure does, and spacing schedules that recall as forgetting begins. Re-reading only creates a feeling of familiarity.
5. For example: "Why install Docker from Docker's own repository rather than Ubuntu's `docker.io`?" Write one focused card per fact you need.
6. FSRS models each card's memory state and schedules reviews to hit your target retention, instead of applying fixed interval multipliers.
7. It's an early-warning sign (V00 §5(i)). If it pulls cumulative hours below 80%, status is R (V00 §11.2). Act on the response ladder.
8. In the next light week.
</details>

<details><summary><b>C01.D04.1</b>: pipelines and results (computed on the sample)</summary>

1. `awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -1` → **192.0.2.10, 5 requests**
2. `awk '$9 ~ /^5/' access.log | wc -l` → **3**
3. `awk '{split($4,t,":"); print t[2]}' access.log | sort | uniq -c` → **08:00 – 6, 09:00 – 4, 10:00 – 2**
4. `awk '$9 ~ /^5/ {print $7}' access.log | sort | uniq -c | sort -rn` → **/api/statements 2, /payments/c2b/confirm 1**
5. `awk '{s+=$10} END {print s}' access.log` → **7663**
6. `awk '$7=="/api/statements" {print $1}' access.log | sort -u | wc -l` → **2**

**Investigate first:** the 502 on `/payments/c2b/confirm`. A failed payment-confirmation callback can mean an unrecorded payment, so reconcile it with a transaction-status query (L02.I01). Then look at the repeated identical 500s (87 bytes each) on `/api/statements` from one client, which suggest a deterministic bug in one member's statement.
</details>

<details><summary><b>C01.Q04</b></summary>

1. `-e` exits on an unhandled failure; `-u` makes unset variables an error; `pipefail` makes a pipeline fail if any stage fails.
2. Parsing `ls` breaks on spaces and newlines and errors when nothing matches; `$f` is unquoted; and `rm` has no `--` guard. Better: `shopt -s nullglob; for f in ./*.dump; do rm -- "$f"; done`.
3. TERM asks the process to exit and can be caught, so it can clean up. KILL can't be caught: no cleanup. Send TERM first.
4. The owner can read and write; the group can read; others have no access.
5. `journalctl -u <unit> -b` (for user units, `journalctl --user -u <unit> -b`).
6. Without lingering, a user's services stop when their last session ends, and don't start at boot.
7. NUL-delimited input such as `find -print0`, so filenames with spaces or newlines are handled safely.
8. systemd runs units with a minimal environment and PATH. Use absolute paths, or set `Environment=PATH=…` in the unit.
</details>

<details><summary><b>C01.D05.1</b>: the ledger bug</summary>

- **Symptom:** the test expects 700.00 but gets 300.00.
- **Hypothesis:** a sign error on one branch.
- **Evidence:** break inside the loop; `p e["kind"], balance` shows the balance falling from 500.00 to 300.00 on the repayment.
- **Fix:** repayments add (`balance += Decimal(e["amount"])`).
- **Extra tests:** a member with no entries returns 0; a fully repaid loan returns the contribution total.

**Design lesson:** a running total over mutable rows can't be audited or reconciled. Chama needs immutable double-entry postings, from which balances are derived and can be checked (C03.M02).
</details>

<details><summary><b>C01.D05.2</b>: the traceback</summary>

- **First frame in your code:** `contributions/views.py`, line 41, in `record_contribution`.
- **Root cause:** the `Contribution` was created without its `group`, and `group_id` is NOT NULL.
- **Fix:** pass the group, derived from the member *after* a permission check that the requester belongs to that group. Validate in the serializer, and add a test.
- Keep the NOT NULL constraint. It caught the bug.
</details>

<details><summary><b>C01.Q05</b></summary>

1. Reproduce → isolate → hypothesise → test → fix → add a regression test.
2. The exception is on the last line. Inspect the deepest frame that belongs to your own code first: frames run from oldest to newest.
3. It enters the debugger (`pdb` by default). `PYTHONBREAKPOINT=0` disables it.
4. The SQL panel shows the query count and repeated, similar queries for one request. Many near-identical SELECTs mean N+1.
5. Press `j` in the terminal running Expo, or choose Open DevTools from the developer menu [V R-0120].
6. A verdict on each commit it checks out (`git bisect good` or `git bisect bad`) after you test it.
7. It swallows the error: no traceback, and the failure surfaces somewhere far from its cause.
8. A test that fails before the fix proves it detects the bug, and it then guards against the bug returning.
</details>

<details><summary><b>C01.D06.1</b>: reading the timings</summary>

1. Round-trip time ≈ connect − dns. **A ≈ 8 ms; B ≈ 145 ms.**
2. TLS time ≈ tls − connect. **A ≈ 10 ms; B ≈ 150 ms**: about one round trip each. That fits TLS 1.3 (or a resumed session); a full TLS 1.2 handshake needs about two [J].
3. Server time ≈ ttfb − tls − one round trip. **A ≈ 0.150 − 0.030 − 0.008 = 112 ms; B ≈ 0.570 − 0.310 − 0.145 = 115 ms.** The servers are equally fast; the network is the difference.
4. Network overhead on Host B for six sequential calls:

   | Approach | Network overhead | Plus server time |
   |---|---|---|
   | New connection per call (TCP + TLS + request ≈ 3 round trips each) | 6 × 435 ms ≈ **2.6 s** | ≈ 0.7 s |
   | One reused connection (2 round trips once, then 1 per call) | 290 + 6 × 145 ≈ **1.16 s** | ≈ 0.7 s |

   **Implication for Chama:** reuse connections (keep-alive, one HTTP client), design screen-level endpoints that batch data, cache, and host close to users.
</details>

<details><summary><b>C01.Q06</b></summary>

1. DNS lookup → TCP connect → TLS handshake → HTTP request and response.
2. Each request costs at least one round trip, mobile apps make many small sequential calls, and small payloads never fill the bandwidth. Latency accumulates.
3. The time from the start of the request until the TLS handshake finished (cumulative).
4. `openssl s_client -connect host:443 -servername host </dev/null | openssl x509 -noout -dates`
5. Latency and packet loss at every hop along the route, over many probes.
6. CDN edges answer from a nearby point of presence, hiding how far away the origin server is.
7. Any two of: the record wasn't created or hasn't propagated; a typo; the wrong zone or delegation; a resolver still caching the negative answer.
8. A new connection costs two or more round trips: about 290 ms at 145 ms per round trip, versus about 16 ms at 8 ms. Reuse saves far more on the slower link.
</details>



---

## Resource index (C01)

R-0001 and R-0025 are defined in V00 and cited again here. New IDs run from R-0100.

| ID | Resource | Provider | Type | Cost | Checked | Verified | Used in |
|---|---|---|---|---|---|---|---|
| R-0001 | [PyPI JSON API: package versions](https://pypi.org/) | Python Software Foundation | tool | free | 2026-10-03 | yes | §0 / Trends Watch |
| R-0025 | [Daraja: Customer To Business Register URL (callback rules; defined in V00)](https://developer.safaricom.co.ke/apis/CustomerToBusinessRegisterURL) | Safaricom | doc | free | 2026-10-03 | yes | C01.M06 |
| R-0100 | [How to Install Python on Ubuntu 26.04 (default 3.14; PEP 668)](https://linuxize.com/post/how-to-install-python-on-ubuntu-26-04/) | Linuxize | article | free | 2026-10-03 | yes | C01.M01 |
| R-0101 | [uv docs: Working on projects](https://docs.astral.sh/uv/guides/projects/) | Astral | doc | free | 2026-10-03 | yes | C01.M01 |
| R-0102 | [uv README](https://github.com/astral-sh/uv) | Astral (GitHub) | doc | free | 2026-10-03 | yes | C01.M01 |
| R-0103 | [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) | Docker Docs | doc | free | 2026-10-03 | yes | C01.M01 |
| R-0104 | [postgres Docker Official Image (PGDATA section)](https://hub.docker.com/_/postgres) | Docker Hub | doc | free | 2026-10-03 | yes | C01.M01 |
| R-0105 | [fnm (Fast Node Manager) README](https://github.com/Schniz/fnm) | Schniz/fnm (GitHub) | doc | free | 2026-10-03 | yes | C01.M01 |
| R-0106 | [Set up GitHub Copilot in VS Code: Remove AI features](https://code.visualstudio.com/docs/setup/copilot) | Visual Studio Code Docs | doc | free | 2026-10-03 | yes | C01.M01 |
| R-0107 | [The Missing Semester of Your CS Education (2026)](https://missing.csail.mit.edu/2026/) | MIT (Athalye, Gjengset, Ortiz) | course | free | 2026-10-03 | yes | C01.M01, C01.M02, C01.M04, C01.M05 |
| R-0108 | [Talk Python To Me #476: Unified Python packaging with uv](https://talkpython.fm/episodes/transcript/476/unified-python-packaging-with-uv) | Talk Python (M. Kennedy) | podcast | free | 2026-10-03 | yes | C01.M01 |
| R-0109 | [Learn Git Branching](https://learngitbranching.js.org/) | P. Cottle | platform | free | 2026-10-03 | yes | C01.M02 |
| R-0110 | [Pro Git, 2nd edition (online, continuously corrected)](https://git-scm.com/book/en/v2) | S. Chacon & B. Straub / Apress | book | free | 2026-10-03 | yes | C01.M02, C01.M05 |
| R-0111 | [About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification) | GitHub Docs | doc | free | 2026-10-03 | yes | C01.M02 |
| R-0112 | [GitHub CLI manual: gh pr](https://cli.github.com/manual/gh_pr) | GitHub | doc | free | 2026-10-03 | VERIFY | C01.M02 |
| R-0113 | [How to write good prompts: using spaced repetition to create understanding](https://andymatuschak.org/prompts/) | Andy Matuschak | article | free | 2026-10-03 | yes | C01.M03 |
| R-0114 | [Anki (desktop 26.09.2; AnkiDroid) and the Anki manual](https://apps.ankiweb.net/) | Ankitects | tool | free | 2026-10-03 | yes | C01.M03 |
| R-0115 | [Learning How to Learn (Oakley & Sejnowski)](https://www.coursera.org/learn/learning-how-to-learn) | Coursera / McMaster / UC San Diego | course | freemium | 2026-10-03 | VERIFY | C01.M03 |
| R-0116 | [The Knowledge Project: Barbara Oakley, Learning How To Learn](https://fs.blog/knowledge-project/barbara-oakley) | Farnam Street | podcast | free | 2026-10-03 | yes | C01.M03 |
| R-0117 | [OverTheWire: Bandit wargame](https://overthewire.org/wargames/bandit/) | OverTheWire | platform | free | 2026-10-03 | yes | C01.M04 |
| R-0118 | [The Linux Command Line (W. Shotts); 3rd ed. No Starch, Feb 2026](https://linuxcommand.org/) | LinuxCommand.org / No Starch Press | book | paid | 2026-10-03 | VERIFY | C01.M04 |
| R-0119 | [pdb: the Python Debugger](https://docs.python.org/3/library/pdb.html) | Python docs | doc | free | 2026-10-03 | VERIFY | C01.M05 |
| R-0120 | [Debugging and profiling tools (React Native DevTools)](https://docs.expo.dev/debugging/tools/) | Expo Docs | doc | free | 2026-10-03 | yes | C01.M01, C01.M05 |
| R-0121 | [django-debug-toolbar 8.0.0](https://pypi.org/project/django-debug-toolbar/) | Django Commons (PyPI) | tool | free | 2026-10-03 | yes | C01.M05 |
| R-0122 | [High Performance Browser Networking (I. Grigorik)](https://hpbn.co/) | hpbn.co / O'Reilly | book | free | 2026-10-03 | yes | C01.M06 |
| R-0123 | [Everything curl (D. Stenberg)](https://everything.curl.dev/) | curl project | book | free | 2026-10-03 | yes | C01.M06 |
| R-0124 | [Troubleshooting rules (ruleset availability by plan)](https://docs.github.com/en/enterprise-server@3.19/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/troubleshooting-rules) | GitHub Docs | doc | free | 2026-10-03 | yes | C01.M02 |
| R-0125 | [Talk Python To Me: Astral joins OpenAI (17 Jun 2026)](https://www.iheart.com/podcast/31107561/episode/336976765/) | Talk Python (M. Kennedy) | podcast | free | 2026-10-03 | yes | §0 / Trends Watch |
| R-0126 | [Ubuntu mirror: Kenya Education Network (KENET)](https://blueprints.launchpad.net/ubuntu/+mirror/ubuntu.mirror.ac.ke-kenet) | Launchpad | doc | free | 2026-10-03 | yes | §0 / Trends Watch |
| R-0127 | [Docker Compose releases (v5.6.0, 2026-10-02)](https://github.com/docker/compose/releases) | Docker (GitHub) | doc | free | 2026-10-03 | yes | §0 / Trends Watch |
| R-0128 | [How to Install Docker on Ubuntu 26.04 LTS (release date, support window, containerd 2.x)](https://new.autogenius.io/blog/install-docker-ubuntu-26-04) | Autogenius / ComputingForGeeks | article | free | 2026-10-03 | yes | §0 / Trends Watch |
| R-0129 | [ShellCheck](https://www.shellcheck.net/) | koalaman (V. Holen) | tool | free | 2026-10-03 | VERIFY | C01.M04 |

---

## YAML manifest

```yaml
manifest_version: 1
playbook: FSE
tsw_track: 1
volume: C01
title: Workbench & Re-entry
version: '1.1'
date: '2026-10-26'
modules:
- id: FSE.C01.M01
  title: Ubuntu dev environment & toolchains (uv, Node LTS, Docker, PostgreSQL, editor)
  prerequisites: []
  hours: [4, 6]
  outcomes: [Build a reproducible environment proven by a verify script, Use uv for per-project Python; leave system Python
      alone, Run Node 24 via fnm with per-project switching, Run PostgreSQL 18 in Docker bound to localhost, Configure Mode
      0 and debug with breakpoints]
  ai_modes: [0, 1]
  applied_in: [FSE.P01.S00, FSE.P01.S01, FSE.P02.S00]
  resources: [R-0100, R-0101, R-0102, R-0103, R-0104, R-0105, R-0106, R-0107, R-0108, R-0120]
  assessments: [FSE.C01.Q01, FSE.C01.D01.1, FSE.C01.D01.2, FSE.C01.BT01.1]
- id: FSE.C01.M02
  title: Git & GitHub workflow (branches, PRs, reviews, commit signing, gh CLI)
  prerequisites: [FSE.C01.M01]
  hours: [3, 4]
  outcomes: [Predict commit graphs, Sign commits with SSH, Run a solo PR cycle with gh, Recover from mistakes safely, Protect
      main within plan limits]
  ai_modes: [0, 1]
  applied_in: [FSE.P01.S00, FSE.P01.S01, FSE.P01.S02, FSE.P01.S03, FSE.P01.S04, FSE.P01.S05, FSE.P02.S00]
  resources: [R-0107, R-0109, R-0110, R-0111, R-0112, R-0124]
  assessments: [FSE.C01.Q02, FSE.C01.D02.1, FSE.C01.D02.2, FSE.C01.BT02.1]
- id: FSE.C01.M03
  title: 'The learning system: AI modes, logs, Anki, explain-backs'
  prerequisites: []
  hours: [1, 2]
  outcomes: [Classify tasks by AI mode, Run the session protocol and weekly log, Write good spaced-repetition prompts with
      FSRS, Perform and score an explain-back]
  ai_modes: [0, 1]
  applied_in: [FSE.P01.S00]
  resources: [R-0113, R-0114, R-0115, R-0116]
  assessments: [FSE.C01.Q03, FSE.C01.D03.1, FSE.C01.BT03.1]
- id: FSE.C01.M04
  title: Linux & CLI depth (shell scripting, processes, permissions, systemd, ssh)
  prerequisites: [FSE.C01.M01, FSE.C09.M01]
  hours: [4, 5]
  outcomes: [Compose pipelines over logs and CSVs, Write ShellCheck-clean defensive Bash, Run user systemd services and timers,
    Set up key-only SSH, Clear Bandit 0-15]
  ai_modes: [0, 1]
  applied_in: [FSE.P03]
  resources: [R-0107, R-0117, R-0118, R-0129]
  assessments: [FSE.C01.Q04, FSE.C01.D04.1, FSE.C01.BT04.1]
- id: FSE.C01.M05
  title: Debugging & reading docs/errors across Python, Django and React Native
  prerequisites: [FSE.C01.M01, FSE.C05.M02, FSE.C07.M01]
  hours: [3, 4]
  outcomes: [Apply the debugging loop with regression tests, 'Use pdb, VS Code and Django Debug Toolbar', Use React Native
      DevTools, Read tracebacks, Bisect regressions]
  ai_modes: [0, 1]
  applied_in: [FSE.P01.S06, FSE.P03]
  resources: [R-0107, R-0110, R-0119, R-0120, R-0121]
  assessments: [FSE.C01.Q05, FSE.C01.D05.1, FSE.C01.D05.2, FSE.C01.BT05.1]
- id: FSE.C01.M06
  title: Networking tools for developers (DNS, TLS, curl, mtr, latency measurement)
  prerequisites: [FSE.C01.M04, FSE.C09.M01]
  hours: [2, 3]
  outcomes: [Trace URL to response and count round trips, 'Measure with dig, curl -w, openssl, mtr', Record regional latency
      in L02.X01, 'Diagnose DNS, TLS and callback failures']
  ai_modes: [0, 1]
  applied_in: [FSE.L02.X01, FSE.P03, FSE.P05]
  resources: [R-0025, R-0122, R-0123]
  assessments: [FSE.C01.Q06, FSE.C01.D06.1, FSE.C01.BT06.1]
resources:
- id: R-0001
  title: 'PyPI JSON API: package versions'
  provider: Python Software Foundation
  type: tool
  url: https://pypi.org/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: null
  level: null
  role: evidence
  status: active
  verified: true
- id: R-0025
  title: 'Daraja: Customer To Business Register URL (callback rules; defined in V00)'
  provider: Safaricom
  type: doc
  url: https://developer.safaricom.co.ke/apis/CustomerToBusinessRegisterURL
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: Daraja v3
  level: null
  role: evidence
  status: active
  verified: true
- id: R-0100
  title: How to Install Python on Ubuntu 26.04 (default 3.14; PEP 668)
  provider: Linuxize
  type: article
  url: https://linuxize.com/post/how-to-install-python-on-ubuntu-26-04/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: Ubuntu 26.04
  level: null
  role: evidence
  status: active
  verified: true
- id: R-0101
  title: 'uv docs: Working on projects'
  provider: Astral
  type: doc
  url: https://docs.astral.sh/uv/guides/projects/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: uv 0.12
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0102
  title: uv README
  provider: Astral (GitHub)
  type: doc
  url: https://github.com/astral-sh/uv
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: uv 0.12
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0103
  title: Install Docker Engine on Ubuntu
  provider: Docker Docs
  type: doc
  url: https://docs.docker.com/engine/install/ubuntu/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: Docker Engine 29; Ubuntu 26.04
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0104
  title: postgres Docker Official Image (PGDATA section)
  provider: Docker Hub
  type: doc
  url: https://hub.docker.com/_/postgres
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: PostgreSQL 18
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0105
  title: fnm (Fast Node Manager) README
  provider: Schniz/fnm (GitHub)
  type: doc
  url: https://github.com/Schniz/fnm
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: fnm current
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0106
  title: 'Set up GitHub Copilot in VS Code: Remove AI features'
  provider: Visual Studio Code Docs
  type: doc
  url: https://code.visualstudio.com/docs/setup/copilot
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: VS Code current
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0107
  title: The Missing Semester of Your CS Education (2026)
  provider: MIT (Athalye, Gjengset, Ortiz)
  type: course
  url: https://missing.csail.mit.edu/2026/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: 2026 edition
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0108
  title: 'Talk Python To Me #476: Unified Python packaging with uv'
  provider: Talk Python (M. Kennedy)
  type: podcast
  url: https://talkpython.fm/episodes/transcript/476/unified-python-packaging-with-uv
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: uv (2024; concepts current)
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0109
  title: Learn Git Branching
  provider: P. Cottle
  type: platform
  url: https://learngitbranching.js.org/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: null
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0110
  title: Pro Git, 2nd edition (online, continuously corrected)
  provider: S. Chacon & B. Straub / Apress
  type: book
  url: https://git-scm.com/book/en/v2
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: Git 2.x
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0111
  title: About commit signature verification
  provider: GitHub Docs
  type: doc
  url: https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: Git ≥ 2.34
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0112
  title: 'GitHub CLI manual: gh pr'
  provider: GitHub
  type: doc
  url: https://cli.github.com/manual/gh_pr
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: null
  level: beginner
  role: learning
  status: active
  verified: VERIFY
- id: R-0113
  title: 'How to write good prompts: using spaced repetition to create understanding'
  provider: Andy Matuschak
  type: article
  url: https://andymatuschak.org/prompts/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: null
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0114
  title: Anki (desktop 26.09.2; AnkiDroid) and the Anki manual
  provider: Ankitects
  type: tool
  url: https://apps.ankiweb.net/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: Anki 26.09 (FSRS)
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0115
  title: Learning How to Learn (Oakley & Sejnowski)
  provider: Coursera / McMaster / UC San Diego
  type: course
  url: https://www.coursera.org/learn/learning-how-to-learn
  cost: {tier: freemium, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: null
  level: beginner
  role: learning
  status: active
  verified: VERIFY
- id: R-0116
  title: 'The Knowledge Project: Barbara Oakley, Learning How To Learn'
  provider: Farnam Street
  type: podcast
  url: https://fs.blog/knowledge-project/barbara-oakley
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: null
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0117
  title: 'OverTheWire: Bandit wargame'
  provider: OverTheWire
  type: platform
  url: https://overthewire.org/wargames/bandit/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: null
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0118
  title: The Linux Command Line (W. Shotts); 3rd ed. No Starch, Feb 2026
  provider: LinuxCommand.org / No Starch Press
  type: book
  url: https://linuxcommand.org/
  cost: {tier: paid, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: 3rd ed. (2026); free online edition to confirm
  level: beginner
  role: learning
  status: active
  verified: VERIFY
- id: R-0119
  title: 'pdb: the Python Debugger'
  provider: Python docs
  type: doc
  url: https://docs.python.org/3/library/pdb.html
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: Python 3.14
  level: beginner
  role: learning
  status: active
  verified: VERIFY
- id: R-0120
  title: Debugging and profiling tools (React Native DevTools)
  provider: Expo Docs
  type: doc
  url: https://docs.expo.dev/debugging/tools/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: React Native ≥ 0.76; Expo SDK 57
  level: beginner
  role: learning
  status: active
  verified: true
- id: R-0121
  title: django-debug-toolbar 8.0.0
  provider: Django Commons (PyPI)
  type: tool
  url: https://pypi.org/project/django-debug-toolbar/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: Django 5.2–6.1
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0122
  title: High Performance Browser Networking (I. Grigorik)
  provider: hpbn.co / O'Reilly
  type: book
  url: https://hpbn.co/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: 2013; TLS chapter concepts only
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0123
  title: Everything curl (D. Stenberg)
  provider: curl project
  type: book
  url: https://everything.curl.dev/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: current
  level: intermediate
  role: learning
  status: active
  verified: true
- id: R-0124
  title: Troubleshooting rules (ruleset availability by plan)
  provider: GitHub Docs
  type: doc
  url: https://docs.github.com/en/enterprise-server@3.19/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/troubleshooting-rules
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: null
  level: null
  role: evidence
  status: active
  verified: true
- id: R-0125
  title: 'Talk Python To Me: Astral joins OpenAI (17 Jun 2026)'
  provider: Talk Python (M. Kennedy)
  type: podcast
  url: https://www.iheart.com/podcast/31107561/episode/336976765/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: null
  level: null
  role: evidence
  status: active
  verified: true
- id: R-0126
  title: 'Ubuntu mirror: Kenya Education Network (KENET)'
  provider: Launchpad
  type: doc
  url: https://blueprints.launchpad.net/ubuntu/+mirror/ubuntu.mirror.ac.ke-kenet
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: null
  level: null
  role: evidence
  status: active
  verified: true
- id: R-0127
  title: Docker Compose releases (v5.6.0, 2026-10-02)
  provider: Docker (GitHub)
  type: doc
  url: https://github.com/docker/compose/releases
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: Compose v5
  level: null
  role: evidence
  status: active
  verified: true
- id: R-0128
  title: How to Install Docker on Ubuntu 26.04 LTS (release date, support window, containerd 2.x)
  provider: Autogenius / ComputingForGeeks
  type: article
  url: https://new.autogenius.io/blog/install-docker-ubuntu-26-04
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: Ubuntu 26.04
  level: null
  role: evidence
  status: active
  verified: true
- id: R-0129
  title: ShellCheck
  provider: koalaman (V. Holen)
  type: tool
  url: https://www.shellcheck.net/
  cost: {tier: free, price: null, currency: null, checked: '2026-10-03'}
  version_targeted: null
  level: beginner
  role: learning
  status: active
  verified: VERIFY
x_schedule:
  FSE.C01.M03: [1]
  FSE.C01.M01: [1]
  FSE.C01.M02: [1]
  FSE.C01.M05: [15]
  FSE.C01.M04: [16, 17]
  FSE.C01.M06: [19]
x_planned_hours: 20
x_v00_feedback: [Record FSE.C01.M05 as first pulled in Phase 3]
```

---

## Handoff

```
HANDOFF: C01
Covered: C01.M01–M06 to the §8.1 template; W1 running order; versions verified
  2026-10-03 (Ubuntu 26.04, uv 0.12.23, Node 24 via fnm, Docker 29 + Compose v5,
  postgres:18 path change, Anki 26.09.2); drills D01.1–D06.1 with keys; build tasks
  BT01.1–BT06.1; quizzes Q01–Q06 with keys; reference verify.sh and pre-push hook
  (ShellCheck-clean, hook tested); Kenyan notes per module; Trends Watch.
Deferred / open items:
  - v1.1 (2026-10-26): re-dated to V00 v1.3 (B2, W1 = Mon 2 Nov). M01–M02 run as
    Chama S00 build work in the week of 26 Oct and are checked off in W1; M05 sits in
    W10 + W15, M04 in W16–W17 and M06 in W19 (tracker plan B2).
  - Apt mirror decision after the M06 lab.
  - GitHub Pro decision once two or more client repos have CI.
Links marked [VERIFY]: VS Code install method for Ubuntu; GitHub CLI install steps
  (cli.github.com) and gh manual URL; Shotts' free edition on linuxcommand.org;
  Python pdb docs URL; Coursera "Learning How to Learn" URL and certificate price;
  ShellCheck site; GitHub Pro price.
Build-clock status: P01 runs in the CHAMA APP Project (S00 closing 26–27 Oct). BT01.1
  (workbench) and BT02.1 (Chama repo foundation) are done there as S00 work; BT03.1
  (learning system) is due in W1 (2–8 Nov).
AI-mode log summary: AIL-0001 (bootstrap review, Mode 1) and AIL-0002 (graph
  puzzles, Mode 1) planned for W1; EBL-0001 explain-back rehearsal on bootstrap.sh.
Decisions made: no ADRs. Conventions adopted: uv for all Python (system Python
  untouched); fnm with .node-version; postgres:18 bound to 127.0.0.1; SSH commit
  signing; pull.ff only; pre-push hook on private repos; Mode 0 via
  chat.disableAIFeatures.
Re-scored skills: n/a until GATE-1.
Prerequisites confirmed for next volume: C02a needs uv + Python 3.14 (M01 step 3,
  Tuesday of W1) and the tracker (M03).
Next: C02a, starting at C02.M01 (then C11a; P01 as soon as the client inputs arrive)
```
