"""1.2: two-layer shell, attention panel, rebalanced Home. Runs after v2_patch.py."""
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "template.html")
s = open(p, encoding="utf-8").read()
css = open(os.path.join(here, "v3_style.css"), encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)

def rep_between(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i); s = s[:i] + new + s[j:]

rep("</style>", css + "</style>")
rep_between('<div class="app">', '<dialog id="dlg">', '''<div class="app">
  <aside class="rail" id="rail" aria-label="Home and tracks"></aside>
  <div class="inner" id="inner">
    <header class="top"><button class="brand" data-act="view" data-v="home" aria-label="UNITY home"><i></i>UNITY</button><nav class="tabs" id="nav" aria-label="Views"></nav><div class="topmeta" id="topmeta"></div></header>
    <main id="main"></main>
  </div>
  <aside class="attn-panel" id="attn" aria-label="Needs attention" hidden></aside>
  <nav class="bnav" id="bnav" aria-label="Sections"></nav>
</div>
''')
rep('const VERSION = "1.1";', 'const VERSION = "1.2";')
rep('''<button class="ritem" data-act="view" data-v="home" aria-label="Home"${S.view === "home" ? cur : ""}><span class="rico">${ico("home")}</span><span class="rlbl">Home</span></button><div class="rsep"></div>`''',
    '''<button class="rbrand" data-act="view" data-v="home" aria-label="UNITY home"><i></i><b>UNITY</b></button>`''')
rep("  plus: '", '''  bell: '<path d="M6 9a6 6 0 1112 0c0 5 2 6 2 7H4c0-1 2-2 2-7zM10 20a2 2 0 004 0"/>',
  close: '<path d="M6 6l12 12M18 6L6 18"/>',
  plus: \'''')
rep('''    <button class="ibtn" data-act="quick-idea"''', '''    ${(n => `<button class="ibtn" data-act="attn" aria-label="Needs attention${n ? ": " + n : ""}" title="Needs attention"${UI.attn ? cur : ""}>${ico("bell")}${n ? `<span class="badge">${n}</span>` : ""}</button>`)(attention().length + nudges().length)}
    <button class="ibtn" data-act="quick-idea"''')
rep("function renderNav() {", '''function toTop() { window.scrollTo(0, 0); const i = $("#inner"); if (i) i.scrollTop = 0; }
function renderAttn() {
  const p = $("#attn"); p.hidden = !UI.attn; if (!UI.attn) { p.innerHTML = ""; return; }
  const at = attention(), ng = nudges();
  p.innerHTML = `<div class="card-h" style="align-items:center"><h3>Needs attention</h3><button class="ibtn" data-act="attn" aria-label="Close">${ico("close")}</button></div>` + (at.length || ng.length ?
    at.map(a => `<div class="arow"><span>${esc(a.t)}</span><button class="btn sm" data-act="attn-go" ${a.tr ? `data-tr="${a.tr}"` : `data-v="${a.v}"`}>${a.b}</button></div>`).join("") + ng.map(n => `<div class="arow"><span>${n}</span><span></span></div>`).join("") :
    `<div class="empty">Nothing needs you right now.</div>`);
}
function renderNav() {''')
rep('''  renderNav();
  $("#main").dataset.view''', '''  renderNav();
  renderAttn();
  $("#main").dataset.view''')
n = s.count("window.scrollTo(0, 0)")
s = s.replace("window.scrollTo(0, 0)", "toTop()").replace("function toTop() { toTop();", "function toTop() { window.scrollTo(0, 0);")
rep("  theme() {", '''  attn() { UI.attn = !UI.attn; render(); },
  "attn-go"(el) { UI.attn = false; if (el.dataset.tr) ACT.track(el); else ACT.view(el); },
  theme() {''')

HOME = r'''function suggestions() {
  const st = weekStatus(monday(todayIso())), out = [];
  const rows = st.rows.filter(r => r.base > 0).sort((a, b) => a.mins / ((a.target || a.base) * 60) - b.mins / ((b.target || b.base) * 60) || a.i - b.i);
  for (const r of rows) { const it = r.tr.recurring ? null : nextItem(r.tr.id); if (r.tr.recurring || it) out.push({ r, it }); }
  return out;
}
function viewHome() {
  const t = todayIso(), st = weekStatus(monday(t)), L = logged(), h = [], tm = S.timer, sgs = suggestions(), sg = sgs[0];
  const after = list => list.length ? `<div class="after"><span class="eyebrow">After this</span>` + list.map(x => `<div class="nx" style="--tc:var(--c-${x.r.tr.id})"><i></i><span class="clamp1"><b>${esc(x.r.tr.name)}</b> · ${esc(x.it ? x.it.t : x.r.tr.label)}</span>${tm ? "" : `<button class="btn sm quiet" data-act="start" data-tr="${x.r.tr.id}"${x.it ? ` data-it="${esc(x.it.id)}"` : ""}>Start</button>`}</div>`).join("") + `</div>` : "";
  if (tm) {
    const it = tm.it && item(tm.it);
    h.push(`<article class="card hero" style="--tc:var(--c-${tm.tr})"><span class="eyebrow">In session · ${esc(track(tm.tr).name)}</span><h1>${esc(it ? it.t : tm.label || track(tm.tr).label || "")}</h1><div class="clock" id="clock">00:00</div>
      <div class="steps">Recall the last session (5 min) · Learn · Do · Test yourself · Log</div>${it && it.next ? `<div class="note">Pick up at: ${esc(it.next)}</div>` : ""}
      <div class="row"><button class="btn pri lg" data-act="stop">Stop and log</button></div>${after(sgs.filter(x => x.r.tr.id !== tm.tr).slice(0, 2))}</article>`);
  } else if (sg) {
    const tr = sg.r.tr, it = sg.it, lm = it ? (L[it.id] || 0) : 0;
    h.push(`<article class="card hero" style="--tc:var(--c-${tr.id})"><span class="eyebrow">${fmtDate(t, { weekday: "long", day: "numeric", month: "long" })} · next up in ${esc(tr.name)}</span>
      <h1>${esc(it ? it.t : tr.label)}</h1>
      ${it ? `<div class="meta"><code>${esc(it.id)}</code>${it.h > 0 ? `<span class="num">${hrs(lm)} of ${hnum(it.h)} h</span>` : ""}${lessonTag(it)}</div>${it.next ? `<div class="note">Pick up at: ${esc(it.next)}</div>` : (it.n ? `<div class="note">${esc(it.n)}</div>` : "")}` : ""}
      <div class="row"><button class="btn pri lg" data-act="start" data-tr="${tr.id}"${it ? ` data-it="${esc(it.id)}"` : ""}>Start session</button><button class="btn lg" data-act="view" data-v="today">All of today</button></div>${after(sgs.slice(1, 3))}</article>`);
  } else h.push(`<article class="card hero"><span class="eyebrow">${fmtDate(t)}</span><h1>Every queue is finished.</h1></article>`);

  const ts = SEED.tracks.filter(x => !x.recurring && x.target > 0).map(tr => ({ tr, s: trackStats(tr.id) }));
  h.push(`<article class="card tracks"><div class="card-h"><span class="eyebrow">Tracks</span><span class="meta num">${ts.reduce((a, x) => a + x.s.done.length, 0)} of ${ts.reduce((a, x) => a + x.s.all.length, 0)} items done</span></div><div class="tgrid">` +
    ts.map(({ tr, s }) => `<button class="tmini" data-act="track" data-tr="${tr.id}" style="--tc:var(--c-${tr.id})"><span class="tname">${ico(tr.id, 18)}${esc(tr.name)}</span>
      <span class="big num">${Math.round(s.pct)}<small>%</small></span><div class="bar"><i style="width:${s.pct}%"></i></div>
      <span class="meta num">${s.done.length} of ${s.all.length} · ${hnum(s.remain)} h left</span><span class="meta num">${s.weeks ? `Finish about ${s.finish}` : (s.remain > 0 ? "No weekly hours set" : "Finished")}</span></button>`).join("") + `</div></article>`);

  const c = consistency(), totalM = live().reduce((a, x) => a + x.m, 0);
  h.push(`<article class="card cons"><div class="card-h"><span class="eyebrow">Consistency</span><span class="meta num">${c.d28} of the last 28 days</span></div>
    <div class="row" style="gap:22px;align-items:flex-end;flex-wrap:nowrap"><div style="flex:none"><div class="big num">${c.run}<small>day${c.run === 1 ? "" : "s"} in a row</small></div><div class="meta num" style="margin-top:6px">${hrs(totalM)} h · ${live().length} session${live().length === 1 ? "" : "s"}</div></div>
    <div class="heat" style="flex:1;min-width:0" role="img" aria-label="Hours studied per day over the last twelve weeks">${c.cells.map(x => `<i class="l${x.lv}${x.fut ? " fut" : ""}${x.d === t ? " now" : ""}" title="${fmtDate(x.d)}: ${hrs(x.m)} h"></i>`).join("")}</div></div>
    <div class="meta">Twelve weeks, Monday at the top. Darker means more hours.</div></article>`);

  const goal = st.plan.goal, mode = st.plan.mode;
  h.push(`<article class="card wk"><div class="card-h"><span class="eyebrow">This week</span><span class="meta">${mode === "pause" ? "Engagement minimum" : mode === "warmup" ? `Warm-up until ${fmtDate(S.settings.start)}` : mode === "ramp" ? "Ramp week" : "Full week"}</span></div>
    <div class="big num">${hrs(st.mins)}<small>${goal ? `of ${hnum(goal)} h` : "h logged"}</small></div>` +
    st.rows.filter(r => !r.tr.recurring && (r.base > 0 || r.mins > 0)).map(r => `<div class="wkrow" style="--tc:var(--c-${r.tr.id});grid-template-columns:118px 1fr 78px"><span>${esc(r.tr.name)}</span><div class="bar"><i style="width:${Math.min(100, r.mins / ((r.target || r.base || 1) * 60) * 100)}%"></i></div><span class="r num">${hrs(r.mins)}${r.target > 0 ? " / " + hnum(r.target) : ""} h</span></div>`).join("") + `</article>`);

  const rv = st.rows.find(r => r.tr.id === "rev"), closed = S.reviews[monday(t)];
  const due = S.items.filter(i => i.st === "done" && i.doneAt).sort((a, b) => a.doneAt < b.doneAt ? 1 : -1).slice(0, 3);
  h.push(`<article class="card rev" style="--tc:var(--c-rev)"><div class="card-h"><span class="eyebrow">Review</span><span class="tag${closed ? " good" : ""}">${closed ? "Week closed" : "Week open"}</span></div>
    <div class="big num">${hrs(rv ? rv.mins : 0)}<small>${rv && rv.target > 0 ? `of ${hnum(rv.target)} h` : "h this week"}</small></div>` +
    (due.length ? `<div class="meta">Re-quiz what you finished last</div>` + due.map(i => `<div class="rq"><span class="clamp1">${esc(i.t)}</span><span class="meta num">${daysBetween(i.doneAt, t)} d ago</span></div>`).join("") : `<p class="lede">Items you finish appear here for a re-quiz.</p>`) +
    `<div class="row">${tm ? "" : `<button class="btn" data-act="start" data-tr="rev">Start review</button>`}${closed ? "" : `<button class="btn quiet" data-act="view" data-v="week">Close the week</button>`}</div></article>`);
  return `<div class="dash">${h.join("")}</div>`;
}
'''
rep_between("function viewHome() {", "function queueHtml(trId, L) {", HOME)
open(p, "w", encoding="utf-8").write(s)
print("v3 patched", len(s), "scrolls", n)
