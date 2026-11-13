"""1.3: HAMWE name, Chama folded into Software, centred top bar, new Today page. Runs after v3_patch.py."""
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "template.html")
s = open(p, encoding="utf-8").read()
css = open(os.path.join(here, "v4_style.css"), encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)

def rep_between(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i); s = s[:i] + new + s[j:]

rep("</style>", css + "</style>")
s = s.replace("UNITY", "HAMWE")
rep('const VERSION = "1.2";', '''const VERSION = "1.3";
// The Chama build is a product inside the Software track, not a track of its own.
SEED.tracks = SEED.tracks.filter(t => t.id !== "build");
SEED.items.forEach(i => { if (i.tr === "build") { i.tr = "sw"; i.g = "Products"; i.prod = 1; } });
function migrate() {
  for (const i of S.items) if (i.tr === "build" || i.id.startsWith("BLD.")) { i.tr = "sw"; i.g = "Products"; i.prod = 1; }
  for (const x of S.sessions) if (x.tr === "build") x.tr = "sw";
  if (S.timer && S.timer.tr === "build") S.timer.tr = "sw";
  delete S.settings.targets.build; if (S.planTrack === "build") S.planTrack = "sw";
}''')
rep("  const have = new Set(S.items.map(i => i.id));", "  migrate();\n  const have = new Set(S.items.map(i => i.id));")
rep('  save(); render(); toast(mode === "replace"', '  migrate(); save(); render(); toast(mode === "replace"')
rep('''${i.st === "later" ? `<span class="tag">Set aside</span>` : ""}''',
    '''${i.st === "later" ? `<span class="tag">Set aside</span>` : ""}${i.prod ? `<span class="tag${i.st === "done" ? " good" : ""}">${i.st === "done" ? "Finished product · built with AI" : "Product"}</span>` : ""}''')
rep("  plus: '", '''  review: '<path d="M4 12a8 8 0 0113.7-5.7L20 8M20 4v4h-4M20 12a8 8 0 01-13.7 5.7L4 16M4 20v-4h4"/>',
  layers: '<path d="M12 3l9 5-9 5-9-5 9-5zM3 13l9 5 9-5"/>',
  pulse: '<path d="M3 12h4l2.5-6 4 12 2.5-6H21"/>',
  plus: \'''')
rep("function applyTheme() {", '''const eb = (k, text) => `<span class="eyebrow">${ico(k, 15)}${text}</span>`;
function applyTheme() {''')
rep('<span class="eyebrow">Tracks</span>', '${eb("layers", "Tracks")}')
rep('<span class="eyebrow">Consistency</span>', '${eb("pulse", "Consistency")}')
rep('<span class="eyebrow">This week</span>', '${eb("week", "This week")}')
rep('<span class="eyebrow">Review</span>', '${eb("review", "Review")}')
rep('<span class="eyebrow">After this</span>', '${eb("today", "After this")}')

TODAY = r'''function viewToday() {
  const t = todayIso(), wk = monday(t), st = weekStatus(wk), L = logged(), d = parse(t), tm = S.timer;
  const p = pauseOn(t), last = lastSession(), goal = st.plan.goal;
  const lede = st.plan.mode === "pause" ? `Engagement week. Minimum ${hnum(goal)} h.` :
    st.plan.mode === "warmup" ? `Warm-up days. Targets begin ${fmtDate(S.settings.start)}; anything you log now counts.` :
    st.plan.mode === "ramp" ? `Ramp week. Target ${hnum(goal)} h, building to ${hnum(st.plan.total)}.` : `Target ${hnum(goal)} h this week.`;
  let hint = "";
  if (p) hint = `<div class="banner"><div><b>Paused for: ${esc(p.reason || "an engagement")}</b>, until ${fmtDate(p.until)}. Your queues are frozen where you left them.</div><div class="row"><button class="btn sm" data-act="end-pause">End the pause now</button></div></div>`;
  else if (S.pause && S.pause.until < t) hint = `<div class="banner good"><div><b>Your engagement ended ${fmtDate(S.pause.until)}.</b> Each queue resumes at the same item.</div><div class="row"><button class="btn sm pri" data-act="end-pause">Resume the full plan</button></div></div>`;
  else if (!tm && !last) hint = `<div class="hint"><b>Start with one session.</b> Pick the suggested card, press Start, and stop when you have had enough. Nothing is behind.</div>`;
  else if (!tm && daysBetween(last.d, t) >= 3) hint = `<div class="hint"><b>Welcome back.</b> Your last session was ${fmtDate(last.d)}: ${esc(sessionLabel(last))}. The queues did not move while you were away.</div>`;
  const h = [`<div class="today-head"><div class="cal" aria-hidden="true"><span class="cal-m">${d.toLocaleDateString("en-GB", { month: "short" })}</span><span class="cal-d num">${d.getDate()}</span><span class="cal-w">${d.toLocaleDateString("en-GB", { weekday: "short" })}</span></div>
    <div class="th-text"><h2>${fmtDate(t, { weekday: "long", day: "numeric", month: "long" })}</h2><p class="lede">${lede}</p>${hint}</div></div>`];
  if (tm) {
    const it = tm.it && item(tm.it);
    h.push(`<article class="card trk running" style="--tc:var(--c-${tm.tr})">
      <div class="card-h"><span class="chip">${esc(track(tm.tr).name)} · in session</span>${tm.off ? `<span class="tag warn">Off the plan</span>` : ""}</div>
      <h3>${esc(it ? it.t : tm.label || track(tm.tr).label || "")}</h3><div class="clock" id="clock">00:00</div>
      <div class="steps">Recall the last session (5 min) · Learn · Do · Test yourself · Log</div>${it && it.next ? `<div class="note">Pick up at: ${esc(it.next)}</div>` : ""}
      <div class="row"><button class="btn pri" data-act="stop">Stop and log</button></div></article>`);
  }
  const sg = tm ? null : suggestions()[0], sugId = sg && (sg.r.target === 0 || sg.r.mins < sg.r.target * 60) ? sg.r.tr.id : null;
  const cards = st.rows.filter(r => !r.tr.recurring).map(r => {
    const tr = r.tr, it = nextItem(tr.id), sug = sugId === tr.id;
    const wkTxt = r.target > 0 ? `${hrs(r.mins)} / ${hnum(r.target)} h` : (r.mins ? `${hrs(r.mins)} h` : "");
    if (!it) return `<article class="card tk" style="--tc:var(--c-${tr.id})"><div class="card-h"><span class="chip">${ico(tr.id, 15)}${esc(tr.name)}</span><span class="meta num">${wkTxt}</span></div><h3>Queue finished</h3></article>`;
    const lm = L[it.id] || 0;
    return `<article class="card tk" style="--tc:var(--c-${tr.id})">
      <div class="card-h"><span class="chip">${ico(tr.id, 15)}${esc(tr.name)}</span><span class="row">${sug ? `<span class="tag sug">Suggested now</span>` : ""}<span class="meta num">${wkTxt}</span></span></div>
      <h3 class="clamp">${esc(it.t)}</h3>
      <div class="meta"><code>${esc(it.id)}</code>${it.h > 0 ? `<span class="num">${hrs(lm)} of ${hnum(it.h)} h</span>` : (lm ? `<span class="num">${hrs(lm)} h so far</span>` : "")}</div>
      ${it.h > 0 ? `<div class="bar"><i style="width:${Math.min(100, lm / (it.h * 60) * 100)}%"></i></div>` : ""}
      ${it.next ? `<div class="note">Pick up at: ${esc(it.next)}</div>` : (!it.c ? `<div class="meta">${lessonTag(it)}</div>` : "")}
      <div class="row"><button class="btn${sug ? " pri" : ""}" data-act="start" data-tr="${tr.id}" data-it="${esc(it.id)}">Start</button>
        <button class="btn" data-act="item-done" data-it="${esc(it.id)}">Mark done</button>
        <button class="btn quiet" data-act="open-plan" data-tr="${tr.id}">Queue</button></div></article>`;
  }).join("");
  const rv = st.rows.find(r => r.tr.recurring), closed = S.reviews[wk], rsug = rv && sugId === rv.tr.id;
  const due = S.items.filter(i => i.st === "done" && i.doneAt).sort((a, b) => a.doneAt < b.doneAt ? 1 : -1).slice(0, 4);
  const review = rv ? `<article class="card tk" style="--tc:var(--c-rev)">
    <div class="card-h"><span class="chip">${ico("review", 15)}Review</span>${rsug ? `<span class="tag sug">Suggested now</span>` : ""}</div>
    <div class="big num">${hrs(rv.mins)}<small>${rv.target > 0 ? `of ${hnum(rv.target)} h` : "h this week"}</small></div>
    <p class="lede">Flashcards, a re-quiz of what you finished, and the weekly close.</p>
    ${due.length ? due.map(i => `<div class="rq"><span class="clamp1">${esc(i.t)}</span><span class="meta num">${daysBetween(i.doneAt, t)} d</span></div>`).join("") : `<div class="meta">Finished items appear here for a re-quiz.</div>`}
    <div><span class="tag${closed ? " good" : ""}">${closed ? "Week closed" : "Week open"}</span></div>
    <div class="row"><button class="btn${rsug ? " pri" : ""}" data-act="start" data-tr="${rv.tr.id}">Start</button>${closed ? "" : `<button class="btn quiet" data-act="view" data-v="week">Close week</button>`}</div></article>` : "";
  const parked = S.ideas.filter(i => i.st === "parked").sort((a, b) => b.ts - a.ts);
  h.push(`<div class="today-grid"><section class="panel"><div class="card-h">${eb("today", "Next up")}<span class="meta num">${hrs(st.mins)}${goal ? " / " + hnum(goal) : ""} h this week</span></div>
      <div class="nu-grid"><div class="cols tgroup">${cards}</div>${review}</div></section>
    <section class="panel ideas-p"><div class="row" style="gap:14px;flex-wrap:nowrap"><div class="bulb">${ico("ideas", 34)}</div><div><h3>Caught an idea?</h3><p class="lede">Park it in one line, then get back to the session.</p></div></div>
      <form class="inline" data-form="capture"><input type="text" name="text" id="cap-today" placeholder="The idea, in one line" required maxlength="300" aria-label="Park an idea"><button class="btn" type="submit">Park</button></form>
      <div>${parked.length ? `<div class="card-h" style="margin-bottom:4px">${eb("ideas", `Parked (${parked.length})`)}<button class="btn sm quiet" data-act="view" data-v="ideas">Decide</button></div>` + parked.slice(0, 5).map(i => `<div class="irow clamp">${esc(i.text)}</div>`).join("") : `<div class="empty">Nothing parked. Ideas you catch mid-session wait here until you decide on them.</div>`}</div>
      <div class="tail"><button class="btn quiet" data-act="off-plan">Work on something not on the plan</button><button class="btn quiet" data-act="past">Log a past session</button></div></section></div>`);
  return h.join("");
}

'''
rep_between("function viewToday() {", "function viewWeek() {", TODAY)
open(p, "w", encoding="utf-8").write(s)
print("v4 patched", len(s))
