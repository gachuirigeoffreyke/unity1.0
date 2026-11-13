"""Apply the 1.1 redesign to template.html: new shell, styles, Home dashboard and track pages."""
import os
import re
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "template_v1.html")
dst = os.path.join(here, "template.html")
if not os.path.exists(src):
    shutil.copy(dst, src)
s = open(src, encoding="utf-8").read()
css = open(os.path.join(here, "v2_style.css"), encoding="utf-8").read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


def rep_between(start, end, new):
    global s
    i = s.index(start)
    j = s.index(end, i)
    s = s[:i] + new + s[j:]


# ---- head, styles, shell
rep('<meta name="theme-color" content="#17354d">', '<meta name="theme-color" content="#161719">')
rep_between("<style>", "</style>", "<style>\n" + css)
rep_between('<div class="app">', '<dialog id="dlg">', '''<div class="app">
  <aside class="rail" id="rail" aria-label="Home and tracks"></aside>
  <header class="top"><button class="brand" data-act="view" data-v="home" aria-label="UNITY home"><i></i>UNITY</button><nav class="tabs" id="nav" aria-label="Views"></nav><div class="topmeta" id="topmeta"></div></header>
  <main id="main"></main>
  <nav class="bnav" id="bnav" aria-label="Sections"></nav>
</div>
''')
rep('const VERSION = "1.0";', 'const VERSION = "1.1";')
rep('timer: null, reviews: {}, view: "today", planTrack: "sw"', 'timer: null, reviews: {}, view: "home", planTrack: "sw"')

NAV = r'''const ICON = {
  home: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
  sw: '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M13.5 5l-3 14"/>',
  str: '<path d="M3 20h18M5 20V8M19 20V8M3 8h18M5 8l7-4 7 4M5 14h14"/>',
  ai: '<path d="M11 3l1.9 5.6L18.5 10.5l-5.6 1.9L11 18l-1.9-5.6L3.5 10.5l5.6-1.9z"/><path d="M19 15l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7z"/>',
  ent: '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2M3 13h18"/>',
  build: '<circle cx="9" cy="9" r="3"/><circle cx="17" cy="10" r="2.3"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5M15.5 14.7c3 .1 5.5 1.9 5.5 5.3"/>',
  today: '<circle cx="12" cy="12" r="9"/><path d="M10 8.5l5.5 3.5-5.5 3.5z"/>',
  week: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  plan: '<path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>',
  ideas: '<path d="M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9c.6.5 1 1.3 1 2.1h5c0-.8.4-1.6 1-2.1A6 6 0 0012 3z"/>',
  proof: '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.8 2.8L16 9.5"/>',
  more: '<path d="M4 6h9M19 6h1M4 12h3M13 12h7M4 18h11"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  theme: '<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 010 18z" fill="currentColor" stroke="none"/>'
};
const ico = (k, n = 20) => `<svg viewBox="0 0 24 24" width="${n}" height="${n}" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICON[k] || ""}</svg>`;
function applyTheme() { const t = S.settings.theme, r = document.documentElement; if (t === "light" || t === "dark") r.dataset.theme = t; else delete r.dataset.theme; }
function renderNav() {
  const parked = S.ideas.filter(i => i.st === "parked").length, cur = ' aria-current="page"';
  const wk = monday(todayIso()), st = weekStatus(wk);
  const goal = st.plan.goal, pct = goal ? Math.min(100, st.mins / (goal * 60) * 100) : 0;
  $("#rail").innerHTML = `<button class="ritem" data-act="view" data-v="home" aria-label="Home"${S.view === "home" ? cur : ""}><span class="rico">${ico("home")}</span><span class="rlbl">Home</span></button><div class="rsep"></div>` +
    SEED.tracks.filter(t => !t.recurring).map(t => {
      const r = st.rows.find(x => x.tr.id === t.id);
      return `<button class="ritem" data-act="track" data-tr="${t.id}" style="--tc:var(--c-${t.id})" aria-label="${esc(t.name)}"${S.view === "track" && S.planTrack === t.id ? cur : ""}><span class="rico tc">${ico(t.id)}</span><span class="rlbl">${esc(t.name)}<small class="num">${hrs(r.mins)}${r.target > 0 ? " / " + hnum(r.target) : ""} h this week</small></span></button>`;
    }).join("");
  const badge = parked ? `<span class="badge">${parked}</span>` : "";
  $("#nav").innerHTML = [["today", "Today"], ["week", "Week"], ["plan", "Plan"], ["ideas", "Ideas"], ["proof", "Proof"]]
    .map(([id, n]) => `<button data-act="view" data-v="${id}"${S.view === id ? cur : ""}>${ico(id, 17)}${n}${id === "ideas" ? badge : ""}</button>`).join("");
  $("#topmeta").innerHTML = (S.timer ? `<button class="pill" data-act="view" data-v="today" aria-label="Session running, open Today"><i class="live"></i><span id="clock2">00:00</span></button>` : "") +
    `<span class="wkmeta num">${hrs(st.mins)}${goal ? " / " + hnum(goal) : ""} h this week${goal ? `<span class="meter" aria-hidden="true"><i style="width:${pct}%"></i></span>` : ""}</span>
    <button class="ibtn" data-act="quick-idea" aria-label="Park an idea" title="Park an idea">${ico("plus")}</button>
    <button class="ibtn" data-act="theme" aria-label="Switch theme" title="Theme: ${esc(S.settings.theme || "auto")}">${ico("theme")}</button>
    <button class="ibtn" data-act="view" data-v="more" aria-label="Settings and backup" title="Settings and backup"${S.view === "more" ? cur : ""}>${ico("more")}</button>`;
  $("#bnav").innerHTML = [["home", "Home"], ["today", "Today"], ["week", "Week"], ["plan", "Plan"], ["ideas", "Ideas"], ["more", "More"]]
    .map(([id, n]) => `<button data-act="view" data-v="${id}"${S.view === id || (id === "home" && S.view === "track") ? cur : ""}>${ico(id)}${n}${id === "ideas" ? badge : ""}</button>`).join("");
}

'''
rep_between("function renderNav() {", "function lessonTag(i) {", NAV)

HOME = r'''function trackStats(trId) {
  const L = logged(), all = S.items.filter(i => i.tr === trId && i.st !== "removed").sort((a, b) => a.o - b.o);
  const done = all.filter(i => i.st === "done"), open = all.filter(i => i.st === "open");
  const total = all.reduce((a, i) => a + i.h, 0), aside = all.filter(i => i.st === "later").reduce((a, i) => a + i.h, 0);
  const remain = open.reduce((a, i) => a + Math.max(0, i.h - (L[i.id] || 0) / 60), 0);
  const mins = live().filter(x => x.tr === trId).reduce((a, x) => a + x.m, 0), wkT = S.settings.targets[trId] || 0;
  const weeks = wkT > 0 && remain > 0 ? Math.ceil(remain / wkT) : 0;
  const finish = weeks ? parse(addDays(todayIso(), weeks * 7)).toLocaleDateString("en-GB", { month: "short", year: "numeric" }) : "";
  const pct = total > 0 ? Math.max(0, Math.min(100, (total - remain - aside) / total * 100)) : 0;
  return { all, done, open, total, remain, mins, wkT, weeks, finish, pct };
}
function suggestion() {
  const st = weekStatus(monday(todayIso()));
  const rows = st.rows.filter(r => r.base > 0).sort((a, b) => a.mins / ((a.target || a.base) * 60) - b.mins / ((b.target || b.base) * 60) || a.i - b.i);
  for (const r of rows) { const it = r.tr.recurring ? null : nextItem(r.tr.id); if (r.tr.recurring || it) return { r, it }; }
  return null;
}
function consistency() {
  const by = {}, t = todayIso(); for (const x of live()) by[x.d] = (by[x.d] || 0) + x.m;
  let run = 0, d = by[t] ? t : addDays(t, -1); while (by[d]) { run++; d = addDays(d, -1); }
  let d28 = 0; for (let i = 0; i < 28; i++) if (by[addDays(t, -i)]) d28++;
  const w0 = addDays(monday(t), -77), cells = [];
  for (let k = 0; k < 84; k++) { const dd = addDays(w0, k), m = by[dd] || 0; cells.push({ d: dd, m, lv: m === 0 ? 0 : m < 60 ? 1 : m < 180 ? 2 : m < 300 ? 3 : 4, fut: dd > t }); }
  return { run, d28, cells };
}
function attention() {
  const a = [], t = todayIso(), parked = S.ideas.filter(i => i.st === "parked").length;
  if (S.pause && S.pause.until < t) a.push({ t: "Your engagement has ended. Resume the full plan.", v: "today", b: "Open" });
  if (parked) a.push({ t: `${parked} parked idea${parked > 1 ? "s" : ""} waiting for a decision`, v: "ideas", b: "Decide" });
  for (const tr of SEED.tracks) { if (tr.recurring) continue; const it = nextItem(tr.id); if (it && !it.c) a.push({ t: `${tr.name}: the lesson for “${it.t}” is not written yet. Ask Claude for it.`, tr: tr.id, b: "Open" }); }
  if ((parse(t).getDay() + 6) % 7 >= 5 && !S.reviews[monday(t)]) a.push({ t: "This week is not closed yet", v: "week", b: "Close it" });
  return a;
}
function viewHome() {
  const t = todayIso(), st = weekStatus(monday(t)), L = logged(), h = [], tm = S.timer, sg = suggestion();
  if (tm) {
    const it = tm.it && item(tm.it);
    h.push(`<article class="card hero" style="--tc:var(--c-${tm.tr})"><span class="eyebrow">In session · ${esc(track(tm.tr).name)}</span><h1>${esc(it ? it.t : tm.label || track(tm.tr).label || "")}</h1><div class="clock" id="clock">00:00</div>
      <div class="steps">Recall the last session (5 min) · Learn · Do · Test yourself · Log</div><div class="row"><button class="btn pri lg" data-act="stop">Stop and log</button></div></article>`);
  } else if (sg) {
    const tr = sg.r.tr, it = sg.it, lm = it ? (L[it.id] || 0) : 0;
    h.push(`<article class="card hero" style="--tc:var(--c-${tr.id})"><span class="eyebrow">${fmtDate(t, { weekday: "long", day: "numeric", month: "long" })} · next up in ${esc(tr.name)}</span>
      <h1>${esc(it ? it.t : tr.label)}</h1>
      ${it ? `<div class="meta"><code>${esc(it.id)}</code>${it.h > 0 ? `<span class="num">${hrs(lm)} of ${hnum(it.h)} h</span>` : ""}${lessonTag(it)}</div>${it.next ? `<div class="note">Pick up at: ${esc(it.next)}</div>` : ""}` : ""}
      <div class="row"><button class="btn pri lg" data-act="start" data-tr="${tr.id}"${it ? ` data-it="${esc(it.id)}"` : ""}>Start session</button><button class="btn lg" data-act="view" data-v="today">All of today</button></div></article>`);
  } else h.push(`<article class="card hero"><span class="eyebrow">${fmtDate(t)}</span><h1>Every queue is finished.</h1></article>`);
  const goal = st.plan.goal, mode = st.plan.mode;
  h.push(`<article class="card wk"><div class="card-h"><span class="eyebrow">This week</span><span class="meta">${mode === "pause" ? "Engagement minimum" : mode === "warmup" ? `Warm-up until ${fmtDate(S.settings.start)}` : mode === "ramp" ? "Ramp week" : "Full week"}</span></div>
    <div class="big num">${hrs(st.mins)}<small>${goal ? `of ${hnum(goal)} h` : "h logged"}</small></div>` +
    st.rows.filter(r => r.base > 0 || r.mins > 0).map(r => `<div class="wkrow" style="--tc:var(--c-${r.tr.id})"><span>${esc(r.tr.name)}</span><div class="bar"><i style="width:${Math.min(100, r.mins / ((r.target || r.base || 1) * 60) * 100)}%"></i></div><span class="r num">${hrs(r.mins)}${r.target > 0 ? " / " + hnum(r.target) : ""} h</span></div>`).join("") + `</article>`);
  for (const tr of SEED.tracks.filter(x => !x.recurring && x.target > 0)) {
    const s = trackStats(tr.id), nx = s.open[0];
    h.push(`<button class="card trk tcard" data-act="track" data-tr="${tr.id}" style="--tc:var(--c-${tr.id})"><span class="tname">${ico(tr.id, 18)}${esc(tr.name)}</span>
      <div class="big num">${Math.round(s.pct)}<small>% done</small></div><div class="bar"><i style="width:${s.pct}%"></i></div>
      <div class="meta num">${s.done.length} of ${s.all.length} items · ${hnum(s.remain)} h left</div>
      <div class="meta num">${s.weeks ? `Finish about ${s.finish} at ${hnum(s.wkT)} h a week` : (s.remain > 0 ? "No weekly hours set" : "Queue finished")}</div>
      ${nx ? `<div class="note clamp">Next: ${esc(nx.t)}</div>` : ""}</button>`);
  }
  const c = consistency(), totalM = live().reduce((a, x) => a + x.m, 0);
  h.push(`<article class="card cons"><div class="card-h"><span class="eyebrow">Consistency</span><span class="meta num">${c.d28} of the last 28 days</span></div>
    <div class="row" style="gap:28px;align-items:flex-end"><div><div class="big num">${c.run}<small>day${c.run === 1 ? "" : "s"} in a row</small></div><div class="meta num" style="margin-top:6px">${hrs(totalM)} h in ${live().length} session${live().length === 1 ? "" : "s"} so far</div></div>
    <div class="heat" style="flex:1;min-width:220px" role="img" aria-label="Hours studied per day over the last twelve weeks">${c.cells.map(x => `<i class="l${x.lv}${x.fut ? " fut" : ""}${x.d === t ? " now" : ""}" title="${fmtDate(x.d)}: ${hrs(x.m)} h"></i>`).join("")}</div></div>
    <div class="meta">One square per day, Monday at the top, this week on the right. Darker means more hours.</div></article>`);
  const at = attention(), ng = nudges();
  h.push(`<article class="card attn"><span class="eyebrow">Needs attention</span>` + (at.length || ng.length ?
    at.map(a => `<div class="arow"><span>${esc(a.t)}</span><button class="btn sm" data-act="${a.tr ? "track" : "view"}" ${a.tr ? `data-tr="${a.tr}"` : `data-v="${a.v}"`}>${a.b}</button></div>`).join("") + ng.map(n => `<div class="arow"><span>${n}</span><span></span></div>`).join("") :
    `<div class="empty">Nothing needs you right now.</div>`) + `</article>`);
  return `<div class="dash">${h.join("")}</div>`;
}
function queueHtml(trId, L) {
  const all = S.items.filter(i => i.tr === trId && i.st !== "removed").sort((a, b) => a.o - b.o), open = all.filter(i => i.st === "open"), h = [];
  const groups = [], gi = {};
  for (const i of all) { if (!(i.g in gi)) { gi[i.g] = groups.length; groups.push({ g: i.g, items: [] }); } groups[gi[i.g]].items.push(i); }
  const nextId = open[0] && open[0].id, nextG = open[0] && open[0].g;
  if (nextG && !UI.touchedG) UI.openG.add(trId + "|" + nextG);
  for (const g of groups) {
    const key = trId + "|" + g.g, d = g.items.filter(i => i.st === "done").length, hh = g.items.reduce((a, i) => a + i.h, 0);
    const vis = g.items.filter(i => UI.showDone || i.st !== "done");
    h.push(`<details class="grp" data-g="${esc(key)}"${UI.openG.has(key) ? " open" : ""} style="--tc:var(--c-${trId})"><summary>${esc(g.g)}<span class="num">${d}/${g.items.length} · ${hnum(hh)} h</span></summary>` +
      (UI.openG.has(key) ? (vis.length ? vis.map(i => itemRow(i, L, i.id === nextId)).join("") : `<div class="empty" style="padding:8px 16px">All finished here.</div>`) : "") + `</details>`);
  }
  return h.join("");
}
const queueTools = () => `<div class="row"><button class="btn sm" data-act="add-item">Add an item</button><label class="check" style="font-size:13px"><input type="checkbox" data-chg="show-done"${UI.showDone ? " checked" : ""}> Show finished items</label></div>`;
function viewTrack() {
  const trId = S.planTrack || "sw", tr = track(trId), s = trackStats(trId), L = logged(), h = [], nx = s.open[0];
  const wr = weekStatus(monday(todayIso())).rows.find(r => r.tr.id === trId), ps = S.proofs.filter(p => p.tr === trId && !p.del);
  h.push(`<div class="row" style="justify-content:space-between;--tc:var(--c-${trId})"><div class="row" style="gap:14px"><span class="rico tc" style="background:var(--sunk)">${ico(trId, 22)}</span><div><h2>${esc(tr.name)}</h2><p class="lede num">${s.done.length} of ${s.all.length} items done · ${Math.round(s.pct)}% of planned hours</p></div></div>${queueTools()}</div>`);
  h.push(`<div class="stats"><div class="stat"><b class="num">${hrs(wr.mins)}${wr.target > 0 ? ` / ${hnum(wr.target)}` : ""}</b><span>hours this week</span></div>
    <div class="stat"><b class="num">${hrs(s.mins)}</b><span>hours logged in total</span></div>
    <div class="stat"><b class="num">${hnum(s.remain)}</b><span>planned hours left</span></div>
    <div class="stat"><b class="num">${s.weeks ? esc(s.finish) : "—"}</b><span>${s.weeks ? `finish at ${hnum(s.wkT)} h a week` : (s.remain > 0 ? "no weekly hours set" : "queue finished")}</span></div></div>`);
  if (nx) {
    const lm = L[nx.id] || 0;
    h.push(`<article class="card trk" style="--tc:var(--c-${trId})"><div class="card-h"><span class="chip">Next up</span><span class="meta num">${nx.h > 0 ? `${hrs(lm)} of ${hnum(nx.h)} h` : ""}</span></div><h3>${esc(nx.t)}</h3>
      <div class="meta"><code>${esc(nx.id)}</code>${lessonTag(nx)}</div>${nx.h > 0 ? `<div class="bar"><i style="width:${Math.min(100, lm / (nx.h * 60) * 100)}%"></i></div>` : ""}
      ${nx.next ? `<div class="note">Pick up at: ${esc(nx.next)}</div>` : (nx.n ? `<div class="note">${esc(nx.n)}</div>` : "")}
      <div class="row"><button class="btn pri" data-act="start" data-tr="${trId}" data-it="${esc(nx.id)}">Start session</button><button class="btn" data-act="item-done" data-it="${esc(nx.id)}">Mark done</button></div></article>`);
  }
  h.push(`<div class="sect"><h2>Queue</h2></div>` + queueHtml(trId, L));
  if (ps.length) h.push(`<div class="sect"><h2>Proof for this track</h2><button class="btn sm" data-act="view" data-v="proof">Open Proof</button></div><div class="card">` + ps.map(p => `<div class="arow"><span class="${p.done ? "done-t" : ""}">${esc(p.t)}</span><span class="tag${p.done ? " good" : ""}">${p.done ? "Done" : "Open"}</span></div>`).join("") + `</div>`);
  return h.join("");
}
function viewPlan() {
  const trId = S.planTrack || "sw", tr = track(trId), s = trackStats(trId), L = logged(), h = [];
  h.push(`<div><h2>Plan</h2><p class="lede">Each track is a queue. Work the top item; move things when the order is wrong.</p></div>`);
  h.push(`<div class="chips">` + SEED.tracks.filter(t => !t.recurring).map(t => `<button data-act="plan-track" data-tr="${t.id}" aria-pressed="${t.id === trId}">${esc(t.name)}</button>`).join("") + `</div>`);
  h.push(`<div class="card trk" style="--tc:var(--c-${trId})"><div class="card-h"><span class="chip">${esc(tr.name)}</span><span class="meta num">${s.done.length} of ${s.all.length} items done</span></div>
    <div class="meta num">${s.remain > 0 ? `${hnum(s.remain)} h of planned work left${s.weeks ? `, about ${s.weeks} weeks at ${hnum(s.wkT)} h a week` : ""}` : "No planned hours left in this queue"}</div>
    ${s.open.length ? `<div class="note">Top of the queue: ${s.open.slice(0, 3).map(i => esc(i.t)).join(" → ")}</div>` : ""}${queueTools()}</div>`);
  return h.join("") + queueHtml(trId, L);
}
'''
rep_between("function viewPlan() {", "function itemRow(i, L, isNext) {", HOME)

# ---- today in columns, More gets a Proof link for phones
rep('h.push(`<div class="sect"><h2>Next up</h2></div>`);', 'h.push(`<div class="sect"><h2>Next up</h2></div><div class="cols">`);')
rep('h.push(`<div class="sect"><h2>Caught an idea?</h2></div>', 'h.push(`</div><div class="sect"><h2>Caught an idea?</h2></div>')
rep('h.push(`<div><h2>More</h2></div>`);', 'h.push(`<div class="row" style="justify-content:space-between"><h2>Settings and backup</h2><button class="btn sm" data-act="view" data-v="proof">Open Proof</button></div>`);')

# ---- render, tick, actions
rep('const VIEWS = { today: viewToday,', 'const VIEWS = { home: viewHome, track: viewTrack, today: viewToday,')
rep('''  if (!VIEWS[S.view]) S.view = "today";
  renderNav();
  $("#main").innerHTML = VIEWS[S.view]();''', '''  if (!VIEWS[S.view]) S.view = "home";
  applyTheme();
  renderNav();
  $("#main").dataset.view = S.view;
  $("#main").innerHTML = VIEWS[S.view]();''')
rep('''  const c = $("#clock");
  if (S && S.timer) {''', '''  const c = $("#clock"), c2 = $("#clock2");
  if (S && S.timer) {''')
rep('if (c) c.textContent = txt; document.title', 'if (c) c.textContent = txt; if (c2) c2.textContent = txt; document.title')
rep('''  "open-plan"(el) { S.planTrack = el.dataset.tr; S.view = "plan"; UI.touchedG = false; save(); render(); window.scrollTo(0, 0); },''',
    '''  "open-plan"(el) { ACT.track(el); },
  track(el) { if (el.closest("#rail")) $("#rail").classList.add("shut"); S.planTrack = el.dataset.tr; S.view = "track"; UI.touchedG = false; UI.openI = null; save(); render(); window.scrollTo(0, 0); },
  theme() { const o = ["auto", "light", "dark"]; S.settings.theme = o[(o.indexOf(S.settings.theme || "auto") + 1) % 3]; save(); render(); toast("Theme: " + S.settings.theme); },
  "quick-idea"() {
    openDlg(`<h2>Park an idea</h2><label>In one line<input type="text" name="text" id="qi-t" required maxlength="300" autofocus></label>
      <div class="row"><button class="btn pri" type="submit">Park</button><button class="btn" type="button" data-act="dlg-close">Cancel</button></div>`, d => { FORMS.capture(d); });
  },''')

rep("const pct = r.target > 0 ? Math.min(100, r.mins / (r.target * 60) * 100) : (r.mins ? 100 : 0);", "const pct = Math.min(100, r.mins / ((r.target || r.base || 1) * 60) * 100);")
rep('  view(el) { S.view = el.dataset.v;', '  view(el) { if (el.closest("#rail")) $("#rail").classList.add("shut"); S.view = el.dataset.v;')
rep('$("#dlg").addEventListener("cancel", () => { dlgSubmit = null; });', '$("#dlg").addEventListener("cancel", () => { dlgSubmit = null; });\n$("#rail").addEventListener("mouseleave", () => $("#rail").classList.remove("shut"));')
open(dst, "w", encoding="utf-8").write(s)
print("patched", len(s))
