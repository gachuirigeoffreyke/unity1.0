"""1.5: Plan page. Runs after v5_patch.py."""
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "template.html")
s = open(p, encoding="utf-8").read()
css = open(os.path.join(here, "v6_style.css"), encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)

def rep_between(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i); s = s[:i] + new + s[j:]

rep("</style>", css + "</style>")
rep('const VERSION = "1.4";', 'const VERSION = "1.5";')
rep("  week: '<path d=\"M10.5 14h45v10.5h-45z\"", "  plan: '<circle cx=\"47\" cy=\"21\" r=\"5.5\" fill=\"#e2574c\" stroke=\"none\"/><path d=\"M8 17l16-6 16 6 16-6v37l-16 6-16-6-16 6z\"/><path d=\"M24 11v37M40 17v37\"/><path d=\"M14 41c5-8 9 1 15-6s8-3 13-9\" stroke-dasharray=\"3 4.5\"/>',\n  week: '<path d=\"M10.5 14h45v10.5h-45z\"")
rep("  attn() {", '''  "plan-view"(el) { UI.planView = el.dataset.v; render(); },
  "col-toggle"(el) {
    const k = el.dataset.k, shut = el.getAttribute("aria-expanded") === "false";
    UI.colShut = UI.colShut || new Set(); UI.colOpen = UI.colOpen || new Set();
    if (shut) { UI.colOpen.add(k); UI.colShut.delete(k); } else { UI.colShut.add(k); UI.colOpen.delete(k); }
    render();
  },
  "copy-outline"() { const t = outlineMd(S.planTrack || "sw"); (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(() => toast("Outline copied")).catch(() => toast("Copy was blocked by the browser.")); },
  attn() {''')

PLAN = r'''function stageOf(i) {
  const g = i.g || "Other", k = g.indexOf(" · ");
  if (i.tr === "str" && /^STR\.(SETUP|V0[123])/.test(i.id)) return ["Phase 1 · Foundations rebuild", g];
  if (k > 0 && i.tr !== "str" && !/^\d+$/.test(g.slice(0, k))) return [g.slice(0, k), g.slice(k + 3)];
  return [g, ""];
}
function planData(trId, L) {
  const all = S.items.filter(i => i.tr === trId && i.st !== "removed").sort((a, b) => a.o - b.o), open = all.filter(i => i.st === "open");
  const stages = [], si = {};
  for (const i of all) {
    const [pn, sub] = stageOf(i);
    if (!(pn in si)) { si[pn] = stages.length; stages.push({ name: pn, subs: [], gi: {}, count: 0, done: 0, hours: 0, remain: 0 }); }
    const sg = stages[si[pn]];
    if (!(i.g in sg.gi)) { sg.gi[i.g] = sg.subs.length; sg.subs.push({ g: i.g, label: sub, items: [] }); }
    sg.subs[sg.gi[i.g]].items.push(i); sg.count++; sg.hours += i.h;
    if (i.st === "done") sg.done++; else if (i.st === "open") sg.remain += Math.max(0, i.h - (L[i.id] || 0) / 60);
  }
  const nx = open[0], wkT = S.settings.targets[trId] || 0; let cum = 0;
  for (const sg of stages) {
    sg.pct = sg.hours > 0 ? Math.max(0, Math.min(100, (1 - sg.remain / sg.hours) * 100)) : (sg.count ? sg.done / sg.count * 100 : 0);
    sg.allDone = sg.count > 0 && sg.done === sg.count; sg.cur = !!nx && stageOf(nx)[0] === sg.name; cum += sg.remain;
    sg.eta = sg.allDone ? "Done" : (wkT > 0 ? "about " + parse(addDays(todayIso(), Math.ceil(cum / wkT) * 7)).toLocaleDateString("en-GB", { month: "short", year: "numeric" }) : "");
  }
  return { all, open, stages, nextId: nx && nx.id, nextG: nx && nx.g };
}
function outlineMd(trId) {
  const pd = planData(trId, logged()), out = [`# ${track(trId).name}`];
  for (const sg of pd.stages) {
    out.push("", `## ${sg.name}  (${sg.done}/${sg.count}, ${hnum(sg.hours)} h)`);
    for (const sub of sg.subs) {
      if (sub.label) out.push("", `### ${sub.label}`);
      for (const i of sub.items) out.push(`- [${i.st === "done" ? "x" : " "}] ${i.id}  ${i.t}${i.h > 0 ? ` (${hnum(i.h)} h)` : ""}${i.st === "later" ? "  [set aside]" : ""}`);
    }
  }
  return out.join("\n");
}
function boardHtml(trId, L, pd) {
  if (pd.nextG && !UI.touchedG) UI.openG.add(trId + "|" + pd.nextG);
  UI.colShut = UI.colShut || new Set(); UI.colOpen = UI.colOpen || new Set();
  const narrow = window.matchMedia("(max-width:700px)").matches;   // on a phone only the current stage starts open
  return `<div class="board">` + pd.stages.map(sg => {
    const ck = trId + "#" + sg.name, shut = UI.colShut.has(ck) || ((sg.allDone || (narrow && !sg.cur)) && !UI.colOpen.has(ck));
    const subs = shut ? "" : sg.subs.map(sub => {
      const key = trId + "|" + sub.g, d = sub.items.filter(i => i.st === "done").length, hh = sub.items.reduce((a, i) => a + i.h, 0);
      const vis = sub.items.filter(i => UI.showDone || i.st !== "done"), isOpen = UI.openG.has(key);
      return `<details class="grp" data-g="${esc(key)}"${isOpen ? " open" : ""}><summary>${esc(sub.label || "Items")}<span class="num">${d}/${sub.items.length} · ${hnum(hh)} h</span></summary>` +
        (isOpen ? (vis.length ? vis.map(i => itemRow(i, L, i.id === pd.nextId)).join("") : `<div class="empty" style="padding:8px 13px">All finished here.</div>`) : "") + `</details>`;
    }).join("");
    return `<section class="col${shut ? " shut" : ""}${sg.cur ? " cur" : ""}"><header class="col-h"><button class="col-t" data-act="col-toggle" data-k="${esc(ck)}" aria-expanded="${!shut}" title="${shut ? "Open" : "Collapse"} ${esc(sg.name)}"><span class="col-n">${esc(sg.name)}</span><span class="meta num">${sg.done}/${sg.count} · ${hnum(sg.hours)} h</span></button><div class="bar"><i style="width:${sg.pct}%"></i></div></header>${subs}</section>`;
  }).join("") + `</div>`;
}
function viewPlan() {
  const trId = S.planTrack || "sw", tr = track(trId), s = trackStats(trId), L = logged(), pd = planData(trId, L), view = UI.planView || "dash", nx = s.open[0];
  const head = `<div class="today-head">${sketch("plan")}<div class="th-text"><h2>Plan</h2><p class="lede">Each track is a queue of stages. Work the top item; move things when the order is wrong.</p></div></div>`;
  const tabs = `<div class="ftabs" role="tablist" aria-label="Tracks">` + SEED.tracks.filter(t => !t.recurring).map(t => `<button class="ftab" role="tab" data-act="plan-track" data-tr="${t.id}" style="--tc:var(--c-${t.id})" aria-selected="${t.id === trId}">${ico(t.id, 16)}${esc(t.name)}<span class="meta num">${Math.round(trackStats(t.id).pct)}%</span></button>`).join("") + `</div>`;
  let body;
  if (view === "road") {
    const curS = pd.stages.find(x => x.cur);
    body = `<div class="road">` + pd.stages.map((sg, n) => `<div class="step${sg.allDone ? " done" : sg.cur ? " cur" : ""}"><div class="node">${sg.allDone ? "✓" : n + 1}</div><b>${esc(sg.name)}</b><span class="meta num">${sg.done}/${sg.count} items · ${hnum(sg.hours)} h</span><div class="bar"><i style="width:${sg.pct}%"></i></div><span class="meta num">${sg.cur ? "You are here · " : ""}${esc(sg.eta)}</span></div>`).join("") + `</div>` +
      (curS && curS.subs.some(x => x.label) ? `<div class="row"><span class="meta">Inside ${esc(curS.name)}:</span>${curS.subs.map(x => { const d = x.items.filter(i => i.st === "done").length; return `<span class="tag${d === x.items.length ? " good" : ""}">${esc(x.label || "Items")} ${d}/${x.items.length}</span>`; }).join("")}</div>` : "");
  } else if (view === "outline") {
    body = `<div class="row" style="justify-content:space-between"><span class="meta">The whole path as a checklist. Paste it anywhere that reads Markdown.</span><button class="btn sm" data-act="copy-outline">Copy as Markdown</button></div><pre class="md" tabindex="0">${esc(outlineMd(trId))}</pre>`;
  } else {
    const wr = weekStatus(monday(todayIso())).rows.find(r => r.tr.id === trId), lm = nx ? (L[nx.id] || 0) : 0;
    body = `<div class="stats"><div class="stat"><b class="num">${Math.round(s.pct)}%</b><span>of planned hours done</span></div>
      <div class="stat"><b class="num">${hrs(wr.mins)}${wr.target > 0 ? ` / ${hnum(wr.target)}` : ""}</b><span>hours this week</span></div>
      <div class="stat"><b class="num">${hrs(s.mins)}</b><span>hours logged in total</span></div>
      <div class="stat"><b class="num">${hnum(s.remain)}</b><span>planned hours left</span></div>
      <div class="stat"><b class="num">${s.weeks ? esc(s.finish) : "—"}</b><span>${s.weeks ? `finish at ${hnum(s.wkT)} h a week` : (s.remain > 0 ? "no weekly hours set" : "queue finished")}</span></div></div>
      <div class="pd2">${nx ? `<div class="nextbox"><div class="card-h">${eb("today", "Next up")}<span class="meta num">${nx.h > 0 ? `${hrs(lm)} of ${hnum(nx.h)} h` : ""}</span></div><h3>${esc(nx.t)}</h3><div class="meta"><code>${esc(nx.id)}</code>${lessonTag(nx)}</div>${nx.next ? `<div class="note">Pick up at: ${esc(nx.next)}</div>` : ""}
        <div class="row" style="margin-top:auto"><button class="btn pri" data-act="start" data-tr="${trId}" data-it="${esc(nx.id)}">Start session</button><button class="btn" data-act="item-done" data-it="${esc(nx.id)}">Mark done</button></div></div>` : `<div class="nextbox"><h3>Queue finished</h3></div>`}
      <div class="sbars">${pd.stages.map(sg => `<div class="wkrow${sg.cur ? " cur" : ""}"><span class="clamp1">${esc(sg.name)}</span><div class="bar"><i style="width:${sg.pct}%"></i></div><span class="r num">${sg.done}/${sg.count}</span></div>`).join("")}</div></div>`;
  }
  const seg = `<div class="seg" role="group" aria-label="Summary view">` + [["dash", "Dashboard"], ["road", "Roadmap"], ["outline", "Outline"]].map(([v, n]) => `<button data-act="plan-view" data-v="${v}" aria-pressed="${v === view}">${n}</button>`).join("") + `</div>`;
  return head + tabs + `<div class="folder" style="--tc:var(--c-${trId})"><section class="psum"><div class="card-h" style="align-items:center"><div class="row" style="gap:12px;flex-wrap:nowrap"><span class="rico tc" style="background:var(--sunk)">${ico(trId, 22)}</span><div><h3>${esc(tr.name)}</h3><p class="meta num">${s.done.length} of ${s.all.length} items · ${hnum(s.remain)} h left${s.weeks ? ` · finish about ${s.finish}` : ""}</p></div></div>${seg}</div>${body}</section>
    <hr><div class="card-h" style="align-items:center">${eb("layers", `Stages (${pd.stages.length})`)}${queueTools()}</div>${boardHtml(trId, L, pd)}</div>`;
}
'''
rep_between("function viewPlan() {", "function itemRow(i, L, isNext) {", PLAN)
open(p, "w", encoding="utf-8").write(s)
print("v6 patched", len(s))
