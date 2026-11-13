"""Build the UNITY seed (tracks, queues, proofs, criteria) from the FSE and STR tracker seeds."""
import json
import sys

fse_path, str_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
fse = json.load(open(fse_path, encoding="utf-8"))["plan"]
strp = json.load(open(str_path, encoding="utf-8"))["plan"]

TRACKS = [
    {"id": "sw", "name": "Software", "short": "SW", "target": 20},
    {"id": "str", "name": "Structural", "short": "STR", "target": 10},
    {"id": "ai", "name": "AI", "short": "AI", "target": 4},
    {"id": "ent", "name": "Entrepreneurship", "short": "ENT", "target": 3},
    {"id": "rev", "name": "Review", "short": "REV", "target": 3, "recurring": True,
     "label": "Review block: flashcards, weekly review, spaced re-quiz"},
    {"id": "build", "name": "Chama build", "short": "BLD", "target": 0},
]

FSE_VOL = {
    "C01": "C01 Workbench", "C02": "C02 Python", "C03": "C03 Data, SQL and ledgers",
    "C04": "C04 Web platform and TypeScript", "C05": "C05 Backend: Django, DRF, FastAPI",
    "C06": "C06 Frontend: React", "C07": "C07 Mobile: React Native and Expo",
    "C08": "C08 Testing and code quality", "C09": "C09 DevOps and operations",
    "C10": "C10 Security and privacy", "C11": "C11 Computer science foundations",
    "C12": "C12 Architecture and system design", "C13": "C13 AI engineering",
    "C14": "C14 Business of software",
}
FSE_SRC = {"C01": "FSE-C01-Workbench.md", "C02": "FSE-C02a-Python.md", "C11": "FSE-C11a-CSFoundations.md"}
WRITTEN = {"C01.M01", "C01.M02", "C01.M03", "C01.M04", "C01.M05", "C01.M06",
           "C02.M01", "C02.M02", "C02.M03", "C02.M04", "C02.M05",
           "C11.M01", "C11.M02", "C11.M03", "C11.M04", "C11.M10"}
# Foundations and architecture first inside each phase.
VOL_PRIORITY = ["C01", "C02", "C11", "C03", "C04", "C05", "C08", "C12", "C06", "C07", "C09", "C10"]
PHASE_NAME = {"P1": "Stage 1", "P2": "Stage 2", "P3": "Stage 3", "P4": "Stage 4", "P5": "Stage 5", "P6": "Stage 6"}

cat = {c["id"]: c for c in fse["catalogue"]}
items = []


def mid(c):
    return round((c["lo"] + c["hi"]) / 2, 2)


def add(track, iid, title, hours, group, written=False, src="", note=""):
    items.append({"id": iid, "tr": track, "t": title, "h": hours, "g": group,
                  "c": 1 if written else 0, "src": src, "n": note, "st": "open"})


# ---- Software: FSE craft C01-C12, by stage then by foundations-first volume order
sw = [c for c in fse["catalogue"] if c["id"][:3] not in ("C13", "C14")]
sw.sort(key=lambda c: (c["first"], VOL_PRIORITY.index(c["id"][:3]), c["id"]))
for c in sw:
    vol = c["id"][:3]
    add("sw", "FSE." + c["id"], c["t"], mid(c), f'{PHASE_NAME[c["first"]]} · {FSE_VOL[vol]}',
        c["id"] in WRITTEN, FSE_SRC.get(vol, "") if c["id"] in WRITTEN else "")

# ---- Structural: EBK actions first, then the STR plan in its own order
STR_VOL = {
    "V00": "Setup", "V01": "V01 Mechanics and maths", "V02": "V02 Structural analysis",
    "V03": "V03 Actions, loads, design philosophy", "V15a": "Phase 2 · Low and mid-rise buildings",
    "V04": "Phase 2 · Low and mid-rise buildings", "V05": "Phase 2 · Low and mid-rise buildings",
    "V06": "Phase 2 · Low and mid-rise buildings", "V07": "Phase 2 · Low and mid-rise buildings",
}
PHASE_STR = {p["id"]: f'Phase {p["id"][1]} · {p["name"]}' for p in strp["phases"]}
add("str", "STR.EBK.01", "Email EBK: next Engineering Conversion Programme intake, and my eligibility as a BTech holder",
    1, "Registration route", True,
    note="Replaces the plan's Graduate Engineer application. Ask for: next intake date, entry requirements, fees, and whether earlier supervised work can count.")
add("str", "STR.EBK.02", "Decide on KETRB registration as a Candidate Engineering Technologist",
    1.5, "Registration route", True,
    note="A registration you can hold now, separate from the EBK route. Check the current requirements on the KETRB site before applying.")
for it in strp["items"]:
    vol = it["vol"]
    if it["phase"] == "P1":
        group = STR_VOL.get(vol, PHASE_STR["P1"])
    else:
        group = PHASE_STR[it["phase"]]
    written = vol in ("V00", "V01")
    src = "STR-V01-Mechanics-Maths.md" if vol == "V01" else ("STR-V00-Navigator.md" if vol == "V00" else "")
    add("str", "STR." + it["id"], it["title"], it["hours"], group, written, src)

# ---- AI: literacy and APIs first, directing agents after building a few apps personally
def c13(mid_id):
    c = cat["C13." + mid_id]
    return c["t"].replace("Part A · ", "").replace("Part B · ", ""), mid(c)


AI = [
    ("AI.F01", "How language models work: tokens, context windows, training vs inference", 8, "1 · Literacy and power use"),
    ("AI.F02", "The AI landscape and the vocabulary practitioners use", 4, "1 · Literacy and power use"),
    ("AI.P01", "Prompting: system prompts, few-shot examples, structured output", 10, "1 · Literacy and power use"),
    ("AI.P02", "Managing context, judging outputs and spotting hallucinations", 6, "1 · Literacy and power use"),
    ("FSE.C13.M07", None, None, "2 · Building AI features"),
    ("FSE.C13.M08", None, None, "2 · Building AI features"),
    ("FSE.C13.M09", None, None, "2 · Building AI features"),
    ("FSE.C13.M10", None, None, "2 · Building AI features"),
    ("AI.A01", "Agents: the agentic loop, tool use, memory and planning patterns", 16, "3 · Agents and systems"),
    ("FSE.C13.M05", None, None, "3 · Agents and systems"),
    ("AI.A02", "Multi-agent patterns, observability and debugging", 8, "3 · Agents and systems"),
    ("AI.S01", "AI systems engineering: evaluation design, tracing, prompt-injection defence, cost control", 14, "3 · Agents and systems"),
    ("AI.GATE", "Gate: I have built and shipped at least two apps personally", 0.5, "4 · Directing agents to build"),
    ("FSE.C13.M01", None, None, "4 · Directing agents to build"),
    ("FSE.C13.M02", None, None, "4 · Directing agents to build"),
    ("FSE.C13.M06", None, None, "4 · Directing agents to build"),
    ("FSE.C13.M03", None, None, "4 · Directing agents to build"),
    ("FSE.C13.M04", None, None, "4 · Directing agents to build"),
    ("FSE.C13.M11", None, None, "4 · Directing agents to build"),
]
for iid, title, hours, group in AI:
    note = ""
    if iid.startswith("FSE."):
        title, hours = c13(iid.split(".")[-1])
    elif iid != "AI.GATE":
        note = "From your AI roadmaps. Hours are an estimate; adjust after the first session."
    add("ai", iid, title, hours, group, iid.startswith("AI."), "AI roadmap documents" if iid.startswith("AI.") and iid != "AI.GATE" else "", note)

# ---- Entrepreneurship: ends in a registered company and a paying customer
def c14(mid_id):
    c = cat["C14." + mid_id]
    return c["t"], mid(c)


ENT = [
    ("ENT.01", "Write the venture thesis: who pays, for what, and why you", 2, "1 · Find the customer"),
    ("FSE.C14.M06", None, None, "1 · Find the customer"),
    ("ENT.02", "Ten customer conversations, each written up the same day", 10, "1 · Find the customer"),
    ("FSE.C14.M05", None, None, "2 · Set up the company"),
    ("ENT.03", "Choose the business structure and register it; tax PIN and bank account", 6, "2 · Set up the company"),
    ("ENT.04", "Data protection: decide on ODPC registration and write the privacy basics", 3, "2 · Set up the company"),
    ("FSE.C14.M03", None, None, "3 · Sell and deliver"),
    ("FSE.C14.M02", None, None, "3 · Sell and deliver"),
    ("FSE.C14.M01", None, None, "3 · Sell and deliver"),
    ("FSE.C14.M04", None, None, "3 · Sell and deliver"),
    ("ENT.05", "First paid engagement: signed scope, price and acceptance terms", 6, "3 · Sell and deliver"),
    ("ENT.06", "Startup resume review: check the criteria on the Proof page and set the date", 1, "4 · Resume the startup"),
]
for iid, title, hours, group in ENT:
    note = ""
    if iid.startswith("FSE."):
        title, hours = c14(iid.split(".")[-1])
    else:
        note = "Draft item. Edit it to fit."
    add("ent", iid, title, hours, group, iid.startswith("ENT."), "", note)

# ---- Chama build lane
for iid, title in [
    ("BLD.P01.1", "Chama: second MVP increment (statement import and reconciliation)"),
    ("BLD.P01.2", "Chama v1.0: release to the client (set the new date)"),
    ("BLD.P01.3", "Chama v1.0.1: share-out recording"),
]:
    add("build", iid, title, 0, "P01 Chama app", True, "CHAMA APP project")

for i, it in enumerate(items):
    it["o"] = (i + 1) * 10

PROOFS = [
    ("str", "EBK has answered in writing on the conversion programme and my eligibility"),
    ("str", "Phase 1 gate passed: mechanics, analysis and a working stiffness solver"),
    ("str", "Two self-set design projects documented from brief to drawings"),
    ("str", "Attached to one live project under a registered engineer"),
    ("sw", "Three apps built personally and deployed"),
    ("sw", "A written architecture decision record for each app"),
    ("sw", "Can explain every shipped component without notes"),
    ("ai", "One AI feature shipped with an evaluation suite"),
    ("ai", "One project built by directing agents from my own spec"),
    ("ent", "Company registered"),
    ("ent", "First paying customer"),
]
CRITERIA = [
    "Software Stage 1 and Stage 2 queues finished",
    "Three apps built personally and deployed",
    "Chama v1.0 in the client's hands",
    "Company registered",
    "Ten customer conversations written up",
]

seed = {
    "tracks": TRACKS,
    "items": items,
    "proofs": [{"id": f"PR.{i+1:02d}", "tr": tr, "t": t, "done": 0, "ev": ""} for i, (tr, t) in enumerate(PROOFS)],
    "criteria": [{"id": f"CR.{i+1:02d}", "t": t, "done": 0} for i, t in enumerate(CRITERIA)],
}
json.dump(seed, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

from collections import Counter
print(Counter(i["tr"] for i in items))
for tr in ("sw", "str", "ai", "ent"):
    print(tr, round(sum(i["h"] for i in items if i["tr"] == tr), 1), "h")
print([i["id"] for i in items if i["tr"] == "sw"][:14])
