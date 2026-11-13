"""1.4: hand-drawn illustrations and the Week page. Runs after v4_patch.py."""
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "template.html")
s = open(p, encoding="utf-8").read()
css = open(os.path.join(here, "v5_style.css"), encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)

def rep_between(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i); s = s[:i] + new + s[j:]

rep("</style>", css + "</style>")
rep('<dialog id="dlg">', '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="rough" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="2.4"/></filter></svg>
<dialog id="dlg">''')
rep('const VERSION = "1.3";', 'const VERSION = "1.4";')
rep("function applyTheme() {", r'''const SK = {
  cal: '<path d="M10.5 14h45v10.5h-45z" fill="#e2574c" stroke="none" opacity=".9"/><rect x="8" y="12" width="48" height="44" rx="7"/><path d="M8 25h48M21 7v10M43 7v10"/>',
  bulb: '<circle cx="35" cy="26" r="13" fill="#f2c94c" stroke="none" opacity=".6"/><path d="M24 47h16M27 53h10M32 11c-9 0-16 7-16 15 0 5 3 9 6 12 2 2 3 4 3 7h14c0-3 1-5 3-7 3-3 6-7 6-12 0-8-7-15-16-15z"/><path d="M27 30l5 5 5-5M32 35v9M32 2v4M11 9l3 3M53 9l-3 3M4 26h4M56 26h4"/>',
  week: '<path d="M10.5 14h45v10.5h-45z" fill="#6f9be8" stroke="none" opacity=".75"/><rect x="8" y="12" width="48" height="44" rx="7"/><path d="M8 25h48M21 7v10M43 7v10M17 35h6M29 35h6M41 35h6M17 45h6M29 45h6"/><path d="M40 45l3 3 6-7" stroke="#22a06b" stroke-width="2.6"/>'
};
function sketch(k, d) {
  return `<div class="sk" aria-hidden="true"><svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" filter="url(#rough)">${SK[k]}</svg>${k === "cal" ? `<span class="sk-m">${d.toLocaleDateString("en-GB", { month: "short" })}</span><span class="sk-d num">${d.getDate()}</span>` : ""}</div>`;
}
const viewWk = () => addDays(monday(todayIso()), -7 * (UI.wkOff || 0));
function applyTheme() {''')
rep('''<div class="cal" aria-hidden="true"><span class="cal-m">${d.toLocaleDateString("en-GB", { month: "short" })}</span><span class="cal-d num">${d.getDate()}</span><span class="cal-w">${d.toLocaleDateString("en-GB", { weekday: "short" })}</span></div>''', '''${sketch("cal", d)}''')
rep('''<div class="bulb">${ico("ideas", 34)}</div>''', '''${sketch("bulb")}''')
rep('S.reviews[monday(todayIso())] = { ts: Date.now()', 'S.reviews[viewWk()] = { ts: Date.now()')
rep('delete S.reviews[monday(todayIso())];', 'delete S.reviews[viewWk()];')
rep("  attn() {", '''  "wk-nav"(el) { const d = +el.dataset.dir; UI.wkOff = d === 0 ? 0 : Math.max(0, (UI.wkOff || 0) + d); render(); },
  attn() {''')

WEEK = r'''function viewWeek() {
  const t = todayIso(), wk = viewWk(), off = UI.wkOff || 0, st = weekStatus(wk), ws = weekSessions(wk), goal = st.plan.goal, mode = st.plan.mode, h = [];
  const modeTxt = mode === "pause" ? "engagement minimum" : mode === "ramp" ? "ramp week" : mode === "warmup" ? "warm-up, no target yet" : "full week";
  const head = `<div class="today-head">${sketch("week")}<div class="th-text"><h2>Week of ${fmtDate(wk, { day: "numeric", month: "long" })}</h2><p class="lede num">${hrs(st.mins)} h logged${goal ? ` of ${hnum(goal)} h` : ""} · ${modeTxt}${off ? "" : " · this week"}</p></div>
    <div class="row" style="margin-left:auto"><button class="btn sm" data-act="wk-nav" data-dir="1">‹ Earlier</button>${off ? `<button class="btn sm" data-act="wk-nav" data-dir="-1">Later ›</button><button class="btn sm pri" data-act="wk-nav" data-dir="0">This week</button>` : ""}</div></div>`;
  const rows = st.rows.filter(r => r.base > 0 || r.mins > 0);
  h.push(`<article class="card wk-a"><div class="card-h">${eb("layers", "By track")}<span class="meta">${goal ? `${Math.round(Math.min(100, st.mins / (goal * 60) * 100))}% of target` : ""}</span></div>
    <div class="big num">${hrs(st.mins)}<small>${goal ? `of ${hnum(goal)} h` : "h logged"}</small></div>` +
    rows.map(r => `<div class="wkrow" style="--tc:var(--c-${r.tr.id})"><span>${esc(r.tr.name)}</span><div class="bar"><i style="width:${Math.min(100, r.mins / ((r.target || r.base || 1) * 60) * 100)}%"></i></div><span class="r num">${hrs(r.mins)}${r.target > 0 ? " / " + hnum(r.target) : ""} h</span></div>`).join("") + `</article>`);
  const days = []; let mx = 120;
  for (let i = 0; i < 7; i++) { const d = addDays(wk, i), by = {}; let m = 0; for (const x of ws) if (x.d === d) { by[x.tr] = (by[x.tr] || 0) + x.m; m += x.m; } days.push({ d, m, by }); mx = Math.max(mx, m); }
  const active = days.filter(x => x.m > 0).length;
  h.push(`<article class="card wk-b"><div class="card-h">${eb("pulse", "By day")}<span class="meta num">${active} of 7 days</span></div><div class="dstack">` +
    days.map(x => `<div class="dcol${x.d === t ? " now" : ""}"><span class="num">${x.m ? hrs(x.m) : ""}</span><div class="dwrap"><div class="dbar" style="height:${x.m / mx * 100}%">${SEED.tracks.filter(tr => x.by[tr.id]).map(tr => `<i style="--tc:var(--c-${tr.id});--m:${x.by[tr.id]}" title="${esc(tr.name)}: ${hrs(x.by[tr.id])} h"></i>`).join("")}</div></div><b>${fmtDate(x.d, { weekday: "short" })} ${parse(x.d).getDate()}</b></div>`).join("") +
    `</div><div class="legend">${rows.map(r => `<span style="--tc:var(--c-${r.tr.id})"><i></i>${esc(r.tr.name)}</span>`).join("")}</div></article>`);
  const rv = S.reviews[wk], parked = S.ideas.filter(i => i.st === "parked").length;
  h.push(`<article class="card wk-c"><div class="card-h">${eb("review", "Close the week")}${rv ? `<span class="tag good">Closed ${fmtDate(iso(new Date(rv.ts)))}</span>` : `<span class="tag">Open</span>`}</div>` + (rv ?
    `${rv.note ? `<div class="note">${esc(rv.note)}</div>` : `<p class="lede">Closed without a note.</p>`}<div class="row" style="margin-top:auto"><button class="btn sm" data-act="reopen-week">Edit</button></div>` :
    `<p class="lede">Ten minutes: decide every parked idea, then write one line on what to change.</p>
     <form data-form="close-week" style="display:flex;flex-direction:column;gap:10px;flex:1"><label style="flex:1">What worked, and one thing to change<textarea name="note" id="wk-note" style="flex:1"></textarea></label>
     <div class="row"><button class="btn pri" type="submit">Close this week</button>${parked ? `<button class="btn" type="button" data-act="view" data-v="ideas">Decide ${parked} idea${parked > 1 ? "s" : ""}</button>` : ""}</div></form>`) + `</article>`);
  h.push(`<article class="card wk-d"><div class="card-h" style="align-items:center">${eb("today", `Sessions (${ws.length})`)}<button class="btn sm" data-act="past">Log a past session</button></div><div class="scroll">` +
    (ws.length ? ws.slice().sort((a, b) => b.ts - a.ts).map(x => `<div class="srow"><div><span class="chip" style="--tc:var(--c-${x.tr})">${esc(track(x.tr).short)}</span> ${esc(sessionLabel(x))}${x.off ? ` <span class="tag warn">off plan</span>` : ""}
      <div class="meta">${fmtDate(x.d)}${x.mode !== null && x.mode !== undefined ? ` · AI mode ${x.mode}` : ""}${x.note ? ` · ${esc(x.note)}` : ""}</div></div>
      <div class="row"><span class="num">${hrs(x.m)} h</span><button class="btn sm quiet danger" data-act="del-session" data-id="${x.id}">${UI.armed === x.id ? "Confirm" : "Delete"}</button></div></div>`).join("") : `<div class="empty">No sessions in this week.</div>`) + `</div></article>`);
  const cur = monday(t), first = monday(iso(new Date(S.created))), hist = [];
  for (let i = 0; i < 8; i++) { const w = addDays(cur, -7 * i); if (i > 0 && w < first) break; const s2 = weekStatus(w); hist.push({ w, i, m: s2.mins, g: s2.plan.goal, mode: s2.plan.mode }); }
  h.push(`<article class="card wk-e"><div class="card-h">${eb("week", "Recent weeks")}<span class="meta">hours against target</span></div>` +
    hist.map(x => `<div class="wkrow${x.i === off ? " cur" : ""}" style="grid-template-columns:96px 1fr 86px"><span>${fmtDate(x.w, { day: "numeric", month: "short" })}</span><div class="bar"><i style="width:${x.g ? Math.min(100, x.m / (x.g * 60) * 100) : (x.m ? 100 : 0)}%"></i></div><span class="r num">${hrs(x.m)}${x.g ? " / " + hnum(x.g) : ""} h</span></div>`).join("") +
    (hist.length < 2 ? `<div class="meta" style="margin-top:auto">Earlier weeks appear here as you go.</div>` : "") + `</article>`);
  return head + `<div class="dash wkpage">${h.join("")}</div>`;
}
'''
rep_between("function viewWeek() {", "function trackStats(trId) {", WEEK)
open(p, "w", encoding="utf-8").write(s)
print("v5 patched", len(s))
