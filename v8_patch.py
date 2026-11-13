"""1.7: track pages, Settings, design-language audit, discard fix, clear logged hours. Runs after v7_patch.py."""
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "template.html")
s = open(p, encoding="utf-8").read()
css = open(os.path.join(here, "v8_style.css"), encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)

def rep_between(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i); s = s[:i] + new + s[j:]

rep("</style>", css + "</style>")
rep('const VERSION = "1.6";', 'const VERSION = "1.7";')
rep('<div id="toast" role="status">', '<div id="toast" role="status" popover="manual">')

# icons and sketches
rep("const ICON = {\n", """const ICON = {
  pause: '<circle cx="12" cy="12" r="9"/><path d="M10 9v6M14 9v6"/>',
  backup: '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
  device: '<rect x="4" y="5" width="16" height="11" rx="2"/><path d="M2 20h20"/>',
""")
rep("const SK = {\n", """const SK = {
  sw: '<circle cx="42" cy="22" r="11" style="fill:var(--c-sw)" stroke="none" opacity=".4"/><rect x="11" y="12" width="42" height="30" rx="5"/><path d="M5 49h54l-4 6H9z"/><path d="M27 21l-6 6 6 6M37 21l6 6-6 6"/>',
  str: '<circle cx="45" cy="18" r="10" style="fill:var(--c-str)" stroke="none" opacity=".4"/><path d="M5 56h54M13 56V12M33 56V12M51 56V26M13 12h20M13 27h38M13 42h38"/><path d="M13 27l20-15M33 42l18-15" stroke-dasharray="3 4.5"/>',
  ai: '<circle cx="31" cy="31" r="13" style="fill:var(--c-ai)" stroke="none" opacity=".35"/><path d="M28 7c2 13 7 18 20 20-13 2-18 7-20 20-2-13-7-18-20-20 13-2 18-7 20-20z"/><path d="M50 40c1 5 3 7 8 8-5 1-7 3-8 8-1-5-3-7-8-8 5-1 7-3 8-8z"/>',
  ent: '<circle cx="44" cy="40" r="11" style="fill:var(--c-ent)" stroke="none" opacity=".4"/><rect x="7" y="21" width="50" height="32" rx="6"/><path d="M23 21v-5c0-2 2-4 4-4h10c2 0 4 2 4 4v5M7 35c8 5 17 7 25 7s17-2 25-7M32 39v6"/>',
  more: '<circle cx="24" cy="18" r="9" fill="#6f9be8" stroke="none" opacity=".5"/><path d="M8 18h9M31 18h25M8 32h29M51 32h5M8 46h5M27 46h29"/><circle cx="24" cy="18" r="6"/><circle cx="44" cy="32" r="6"/><circle cx="20" cy="46" r="6"/>',
""")

# toast above dialogs (the top layer used to hide it)
rep_between("function toast(msg) {", "\n", """function toast(msg) {
  const t = $("#toast"); t.textContent = msg; t.classList.add("on");
  if (t.showPopover) { try { t.hidePopover(); } catch (e) {} try { t.showPopover(); } catch (e) {} }
  clearTimeout(toastT); toastT = setTimeout(() => { t.classList.remove("on"); if (t.hidePopover) try { t.hidePopover(); } catch (e) {} }, 2600);
}""")

# discard: confirm on the button itself, then close and say so
rep_between('  "discard-timer"() {', "\n", '''  "discard-timer"(el) {
    if (UI.armed !== "discard") {
      UI.armed = "discard"; if (el) { el.textContent = "Confirm: discard, log nothing"; el.classList.remove("quiet"); }
      setTimeout(() => { if (UI.armed === "discard") { UI.armed = null; if (el && el.isConnected) { el.textContent = "Discard"; el.classList.add("quiet"); } } }, 6000); return;
    }
    UI.armed = null; S.timer = null; save(); closeDlg(); render(); toast("Session discarded. Nothing was logged.");
  },
  "item-clear"(el) {
    const id = el.dataset.it; if (!arm("clr" + id)) return; let n = 0;
    for (const x of S.sessions) if (x.it === id && !x.del) { x.del = 1; touch(x); n++; }
    const i = item(id); if (i) { i.next = ""; touch(i); }
    save(); render(); toast(`Cleared ${n} session${n === 1 ? "" : "s"}. Hours are back to zero.`);
  },
  "to-plan"(el) { S.planTrack = el.dataset.tr; S.view = "plan"; UI.touchedG = false; UI.openI = null; save(); render(); toTop(); },
  "theme-set"(el) { S.settings.theme = el.dataset.t; save(); render(); },''')
rep('<button class="btn" type="button" data-act="dlg-close">Keep running</button>', '<button class="btn" type="button" data-act="dlg-close">Close, keep the timer running</button>')
rep('''        <button class="btn sm" data-act="item-edit" data-it="${esc(i.id)}">Edit</button></div></div>` : "")''',
    '''        <button class="btn sm" data-act="item-edit" data-it="${esc(i.id)}">Edit</button>${lm > 0 ? `<button class="btn sm quiet danger" data-act="item-clear" data-it="${esc(i.id)}">${UI.armed === "clr" + i.id ? `Confirm: clear ${hrs(lm)} h` : "Clear logged hours"}</button>` : ""}</div></div>` : "")''')

# shared pieces brought into line
rep('<div class="row" style="margin-left:auto"><button class="btn sm" data-act="wk-nav" data-dir="1">', '<div class="head-r"><button class="btn sm" data-act="wk-nav" data-dir="1">')
rep('''<div class="card-h"><span class="chip">${esc(track(tm.tr).name)} · in session</span>''', '''<div class="card-h"><span class="chip">${ico(tm.tr, 15)}${esc(track(tm.tr).name)} · in session</span>''')
rep('''<div class="card-h" style="align-items:center"><h3>Needs attention</h3>''', '''<div class="card-h" style="align-items:center">${eb("bell", "Needs attention")}''')
rep('''${hrs(st.mins)}${goal ? " / " + hnum(goal) : ""} h this week${goal ?''', '''${hrs(st.mins)}${goal ? " / " + hnum(goal) : ""} h<span class="wl">this week</span>${goal ?''')

TRACK = r'''function viewTrack() {
  const trId = S.planTrack || "sw", tr = track(trId), s = trackStats(trId), L = logged(), t = todayIso(), tm = S.timer, pd = planData(trId, L);
  const wk = monday(t), wr = weekStatus(wk).rows.find(r => r.tr.id === trId), ps = S.proofs.filter(p => p.tr === trId && !p.del);
  const running = !!tm && tm.tr === trId, cur = running ? (tm.it && item(tm.it)) : s.open[0];
  const coming = s.open.filter(i => !cur || i.id !== cur.id).slice(0, 4);
  const where = i => { const [a, b] = stageOf(i); return b ? `${a} · ${b}` : a; };
  const head = `<div class="today-head">${sketch(trId)}<div class="th-text"><h2>${esc(tr.name)}</h2><p class="lede num">${s.done.length} of ${s.all.length} items done · ${hnum(s.remain)} h left${s.weeks ? ` · finish about ${s.finish}` : ""}</p></div>
    <div class="head-r wide"><button class="btn sm" data-act="to-plan" data-tr="${trId}">Open the queue in Plan</button></div></div>`;
  const h = [];
  const after = coming.length ? `<div class="after">${eb("layers", "Coming up")}` + coming.map(i => `<div class="nx"><i></i><span class="clamp1">${esc(i.t)}</span><span class="meta num">${i.h > 0 ? hnum(i.h) + " h" : ""}</span>${tm ? "<span></span>" : `<button class="btn sm quiet" data-act="start" data-tr="${trId}" data-it="${esc(i.id)}">Start</button>`}</div>`).join("") + `</div>` : "";
  if (running) {
    h.push(`<article class="card hero tk-a" style="--tc:var(--c-${trId})"><span class="eyebrow">${ico("today", 15)}In session${cur ? " · " + esc(where(cur)) : ""}</span><h1>${esc(cur ? cur.t : tm.label || tr.label || "")}</h1><div class="clock" id="clock">00:00</div>
      <div class="steps">Recall the last session (5 min) · Learn · Do · Test yourself · Log</div>${cur && cur.next ? `<div class="note">Pick up at: ${esc(cur.next)}</div>` : ""}
      <div class="row"><button class="btn pri lg" data-act="stop">Stop and log</button></div>${after}</article>`);
  } else if (cur) {
    const lm = L[cur.id] || 0;
    h.push(`<article class="card hero tk-a" style="--tc:var(--c-${trId})"><div class="card-h"><span class="eyebrow">${ico("today", 15)}Next up · ${esc(where(cur))}</span><span class="meta num">${cur.h > 0 ? `${hrs(lm)} of ${hnum(cur.h)} h` : ""}</span></div><h1>${esc(cur.t)}</h1>
      <div class="meta"><code>${esc(cur.id)}</code>${lessonTag(cur)}</div>${cur.h > 0 ? `<div class="bar"><i style="width:${Math.min(100, lm / (cur.h * 60) * 100)}%"></i></div>` : ""}
      ${cur.next ? `<div class="note">Pick up at: ${esc(cur.next)}</div>` : (cur.n ? `<div class="note">${esc(cur.n)}</div>` : "")}
      <div class="row">${tm ? `<span class="meta">A session is running in ${esc(track(tm.tr).name)}.</span>` : `<button class="btn pri lg" data-act="start" data-tr="${trId}" data-it="${esc(cur.id)}">Start session</button>`}<button class="btn lg" data-act="item-done" data-it="${esc(cur.id)}">Mark done</button></div>${after}</article>`);
  } else h.push(`<article class="card hero tk-a" style="--tc:var(--c-${trId})"><span class="eyebrow">${ico("proof", 15)}Queue finished</span><h1>Nothing left in ${esc(tr.name)}.</h1><p class="lede">Add the next item in Plan when there is one.</p></article>`);

  h.push(`<article class="card tk-b" style="--tc:var(--c-${trId})"><div class="card-h">${eb("pulse", "Progress")}<span class="meta num">${s.wkT ? `${hnum(s.wkT)} h a week planned` : "no weekly hours set"}</span></div>
    <div class="big num">${Math.round(s.pct)}<small>% of planned hours</small></div><div class="bar"><i style="width:${s.pct}%"></i></div>
    <div class="stats s2"><div class="stat"><b class="num">${hrs(wr.mins)}${wr.target > 0 ? ` / ${hnum(wr.target)}` : ""}</b><span>hours this week</span></div>
      <div class="stat"><b class="num">${hrs(s.mins)}</b><span>hours logged in total</span></div>
      <div class="stat"><b class="num">${hnum(s.remain)}</b><span>planned hours left</span></div>
      <div class="stat"><b class="num">${s.weeks ? esc(s.finish) : "—"}</b><span>${s.weeks ? "projected finish" : (s.remain > 0 ? "no weekly hours set" : "queue finished")}</span></div></div>
    <div class="sub-h">${eb("plan", `Stages (${pd.stages.length})`)}</div>
    <div class="sbars">${pd.stages.map(sg => `<div class="wkrow${sg.cur ? " cur" : ""}"><span class="clamp1" title="${esc(sg.name)}">${esc(sg.name)}</span><div class="bar"><i style="width:${sg.pct}%"></i></div><span class="r num">${sg.done}/${sg.count}</span></div>`).join("")}</div></article>`);

  const wks = []; let mx = 60, tot = 0;
  for (let k = 7; k >= 0; k--) { const w = addDays(wk, -7 * k), r = weekStatus(w).rows.find(x => x.tr.id === trId); wks.push({ w, k, m: r.mins }); mx = Math.max(mx, r.mins); tot += r.mins; }
  h.push(`<article class="card tk-c" style="--tc:var(--c-${trId})"><div class="card-h">${eb("week", "Last eight weeks")}<span class="meta num">${hrs(tot)} h in all</span></div><div class="dstack w8">` +
    wks.map(x => `<div class="dcol${x.k === 0 ? " now" : ""}"><span class="num">${x.m ? hrs(x.m) : ""}</span><div class="dwrap"><div class="dbar" style="height:${x.m / mx * 100}%">${x.m ? `<i title="${hrs(x.m)} h"></i>` : ""}</div></div><b>${fmtDate(x.w, { day: "numeric", month: "short" })}</b></div>`).join("") + `</div></article>`);

  const ss = live().filter(x => x.tr === trId).sort((a, b) => b.ts - a.ts);
  h.push(`<article class="card tk-d"><div class="card-h" style="align-items:center">${eb("today", `Recent sessions (${ss.length})`)}<button class="btn sm" data-act="past">Log a past session</button></div><div class="scroll">` +
    (ss.length ? ss.slice(0, 8).map(x => `<div class="srow"><div>${esc(sessionLabel(x))}${x.off ? ` <span class="tag warn">off plan</span>` : ""}<div class="meta">${fmtDate(x.d)}${x.note ? ` · ${esc(x.note)}` : ""}</div></div>
      <div class="row"><span class="num">${hrs(x.m)} h</span><button class="btn sm quiet danger" data-act="del-session" data-id="${x.id}">${UI.armed === x.id ? "Confirm" : "Delete"}</button></div></div>`).join("") : `<div class="empty">No sessions in ${esc(tr.name)} yet. The first one starts with the card above.</div>`) + `</div></article>`);

  const prods = S.items.filter(i => i.tr === trId && i.prod && i.st !== "removed").sort((a, b) => a.o - b.o), pd2 = ps.filter(p => p.done).length;
  h.push(`<article class="card tk-e" style="--tc:var(--c-${trId})"><div class="card-h" style="align-items:center">${eb("proof", "Proof")}<span class="meta num">${pd2} of ${ps.length} in hand</span></div><div class="bar"><i style="width:${ps.length ? pd2 / ps.length * 100 : 0}%"></i></div><div class="scroll">` +
    (ps.length ? ps.map(p => `<div class="arow"><span class="${p.done ? "done-t" : ""}">${esc(p.t)}</span><span class="tag${p.done ? " good" : ""}">${p.done ? "Done" : "Open"}</span></div>`).join("") : `<div class="empty">No proofs set for this track.</div>`) +
    (prods.length ? `<div class="sub-h">${eb("layers", "Products")}</div>` + prods.map(i => `<div class="arow"><span>${esc(i.t)}</span><span class="tag${i.st === "done" ? " good" : ""}">${i.st === "done" ? "Finished · built with AI" : (L[i.id] ? `${hrs(L[i.id])} h so far` : "Not started")}</span></div>`).join("") : "") +
    `</div><div class="row" style="margin-top:auto"><button class="btn sm" data-act="view" data-v="proof">Open Proof</button></div></article>`);
  return head + `<div class="dash tkpage">${h.join("")}</div>`;
}
'''
rep_between("function viewTrack() {", "function stageOf(i) {", TRACK)

MORE = r'''function viewMore() {
  const p = S.pause, t = todayIso(), act = pauseOn(t), tg = S.settings.targets, total = Object.values(tg).reduce((a, b) => a + b, 0), th = S.settings.theme || "auto";
  const head = `<div class="today-head">${sketch("more")}<div class="th-text"><h2>Settings and backup</h2><p class="lede">The weekly split, pauses for paid work, and the backup that keeps laptop and phone in step.</p></div></div>`;
  const h = [];
  h.push(`<article class="card st-a"><div class="card-h">${eb("week", "Weekly split")}<span class="meta num">Full week: ${hnum(total)} h</span></div><form data-form="settings">
    <div class="splitg">` + SEED.tracks.map(tr => `<label style="--tc:var(--c-${tr.id})"><span>${ico(tr.id === "rev" ? "review" : tr.id, 14)}${esc(tr.name)}</span><input type="number" name="t_${tr.id}" id="st-${tr.id}" min="0" max="60" step="0.5" value="${tg[tr.id] || 0}"></label>`).join("") + `</div>
    <div class="grid2"><label>Targets start (a Monday)<input type="date" name="start" id="st-start" value="${S.settings.start}"></label><label>Ramp: week 1 total (h)<input type="number" name="r0" id="st-r0" min="0" max="80" step="0.5" value="${S.settings.ramp[0] ?? ""}"></label><label>Ramp: week 2 total (h)<input type="number" name="r1" id="st-r1" min="0" max="80" step="0.5" value="${S.settings.ramp[1] ?? ""}"></label></div>
    <div class="row"><button class="btn pri" type="submit">Save split</button></div></form></article>`);
  h.push(`<article class="card st-b"><div class="card-h">${eb("pause", "Pause for an engagement")}${p && p.until >= t ? `<span class="tag warn">${act ? "Paused" : "Scheduled"}</span>` : ""}</div>` + (p && p.until >= t ?
    `<div><b>${esc(p.reason || "Engagement")}</b></div><div class="meta">${fmtDate(p.from)} to ${fmtDate(p.until)} · minimum ${hnum(p.min)} h a week</div><div class="row" style="margin-top:auto"><button class="btn" data-act="end-pause">End the pause</button></div>` :
    `<p class="lede">When paid work or life takes over, pause. The weekly target drops to a minimum and every queue stays where it is.</p>
     <form data-form="pause"><label>What for<input type="text" name="reason" id="pz-r" placeholder="e.g. Site supervision job" maxlength="80"></label>
     <div class="grid2"><label>From<input type="date" name="from" id="pz-f" value="${t}" required></label><label>Until<input type="date" name="until" id="pz-u" value="${addDays(t, 13)}" required></label><label>Minimum hours a week<input type="number" name="min" id="pz-m" min="0" max="40" step="0.5" value="${S.settings.pauseMin}"></label></div>
     <div class="row"><button class="btn" type="submit">Start the pause</button></div></form>`) + `</article>`);
  h.push(`<article class="card st-c"><div class="card-h">${eb("backup", "Backup and moving between devices")}<span class="meta">${S.lastExport ? "Last export " + fmtDate(iso(new Date(S.lastExport))) : "No export yet"}</span></div>
    <p class="lede">Your data lives on this device only. Export a backup weekly. To bring phone and laptop together, export on one and import with Merge on the other.</p>
    <div class="row"><button class="btn pri" data-act="export">Export backup</button><button class="btn" data-act="export-csv">Export sessions (CSV)</button><button class="btn" data-act="copy-backup">Copy backup as text</button></div>
    <div class="sub-h">${eb("layers", "Import")}</div><label>A backup file from the other device<input type="file" id="imp-file" accept=".json,application/json"></label>
    <div class="row"><button class="btn" data-act="import" data-mode="merge">Merge into this device</button><button class="btn quiet danger" data-act="import" data-mode="replace">${UI.armed === "replace" ? "Confirm: replace everything" : "Replace this device's data"}</button></div></article>`);
  h.push(`<article class="card st-d"><div class="card-h" style="align-items:center">${eb("theme", "Appearance")}<div class="seg" role="group" aria-label="Theme">${[["auto", "Auto"], ["light", "Light"], ["dark", "Dark"]].map(([v, n]) => `<button data-act="theme-set" data-t="${v}" aria-pressed="${v === th}">${n}</button>`).join("")}</div></div>
    <div class="sub-h">${eb("device", "This device")}</div>
    <div><div class="arow"><span>Version</span><span class="meta num">${VERSION}</span></div><div class="arow"><span>Stored in</span><span class="meta">${esc(DB.mode)}</span></div><div class="arow"><span>Sessions logged</span><span class="meta num">${live().length}</span></div></div>
    <div class="row"><button class="btn sm" data-act="persist">Ask the browser to protect this data</button></div>
    <div class="danger-z"><p class="meta">Start over clears sessions, ideas and edits and reloads the original plan. Export a backup first.</p><div class="row"><button class="btn quiet danger" data-act="reset">${UI.armed === "reset" ? "Confirm: erase and reload the plan" : "Reset this device"}</button></div></div></article>`);
  return head + `<div class="dash stpage">${h.join("")}</div>`;
}

'''
rep_between("function viewMore() {", "const VIEWS = {", MORE)
open(p, "w", encoding="utf-8").write(s)
print("ok 1.7")
