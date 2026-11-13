"""3.0: cards and spaced review. Runs after v11_patch.py."""
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "template.html")
s = open(p, encoding="utf-8").read()
css = open(os.path.join(here, "v12_style.css"), encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
rep("</style>", css + "</style>")
rep('const VERSION = "2.1";', 'const VERSION = "3.0";')
rep("const ICON = {\n", """const ICON = {
  cards: '<rect x="3" y="7" width="14" height="12" rx="2.5"/><path d="M7 7V5.500A1.500 1.500 0 018.500 4H19.500A1.500 1.500 0 0121 5.500V14.500A1.500 1.500 0 0119.500 16H17"/>',
""")
rep("const SK = {\n", """const SK = {
  cards: '<circle cx="42" cy="24" r="11" fill="#8fd3a8" stroke="none" opacity=".6"/><rect x="8" y="20" width="38" height="30" rx="5" transform="rotate(-6 27 35)"/><rect x="18" y="13" width="38" height="30" rx="5" transform="rotate(5 37 28)"/><path d="M27 25l18 1.500M26.500 32l12 1"/>',
""")
rep('for (const k of ["items", "sessions", "ideas", "proofs", "criteria", "port"])', 'for (const k of ["items", "sessions", "ideas", "proofs", "criteria", "port", "cards"])')
rep("function migrate() {\n", "function migrate() {\n  if (!Array.isArray(S.cards)) S.cards = [];\n")
rep("port: PSEED.map(x => ({ ...x, u: 0 })), pause: null,", "port: PSEED.map(x => ({ ...x, u: 0 })), cards: [], pause: null,")
rep('''  if (S.view !== "read" && S.rt && S.rt.start) rtPause("left");''', '''  if (S.view !== "read" && S.rt && S.rt.start) rtPause("left");
  if (S.view !== "review" && UI.rv) rvEnd(true);
  if (volsReady) syncCards();''')
rep('''  if (S.view === "read") fillLesson();''', '''  if (S.view === "read") fillLesson();
  if (S.view === "review") fillCard();''')
rep('''(id === "library" && S.view === "read") ? cur : ""}>${ico(id, 17)}''', '''(id === "library" && (S.view === "read" || S.view === "review")) ? cur : ""}>${ico(id, 17)}''')
rep('''(id === "library" && S.view === "read") ? cur : ""}>${ico(id)}''', '''(id === "library" && (S.view === "read" || S.view === "review")) ? cur : ""}>${ico(id)}''')

# Today and Home review cards
rep('''    <p class="lede">Flashcards, a re-quiz of what you finished, and the weekly close.</p>''', '''    <p class="lede">${cardQueue().all.length ? `${cardQueue().due.length} cards due and ${cardQueue().nw.length} new today.` : "No cards due today."} Card reviews log here on their own.</p>''')
rep('''    <div class="row"><button class="btn${rsug ? " pri" : ""}" data-act="start" data-tr="${rv.tr.id}">Start</button>${closed ? "" :''', '''    <div class="row">${cardQueue().all.length ? `<button class="btn pri" data-act="rv-start">Review cards (${cardQueue().all.length})</button>` : ""}<button class="btn${rsug && !cardQueue().all.length ? " pri" : ""}" data-act="start" data-tr="${rv.tr.id}">Start</button>${closed ? "" :''')
rep('''    `<div class="row">${tm ? "" : `<button class="btn" data-act="start" data-tr="rev">Start review</button>`}''', '''    `<div class="row">${cardQueue().all.length ? `<button class="btn pri" data-act="rv-start">Review cards (${cardQueue().all.length})</button>` : ""}${tm ? "" : `<button class="btn" data-act="start" data-tr="rev">Start review</button>`}''')
rep('''  if ((parse(t).getDay() + 6) % 7 >= 5 && !S.reviews[monday(t)])''', '''  if (cardQueue().due.length) a.push({ t: `${cardQueue().due.length} card${cardQueue().due.length > 1 ? "s" : ""} due for review`, v: "review", b: "Review" });
  if ((parse(t).getDay() + 6) % 7 >= 5 && !S.reviews[monday(t)])''')

# reader: add a card from the lesson
rep('''<div class="row">${nav}<button class="btn sm pri" data-act="read-close">''', '''<div class="row"><button class="btn sm" data-act="card-new" data-vol="${esc(v.id)}" data-it="${esc(x.it || "")}">${ico("cards", 15)}Add card</button>${nav}<button class="btn sm pri" data-act="read-close">''')

# Library: Cards tab and an overview box
rep('''aria-selected="${tab === "home"}">${ico("home", 16)}Overview</button>` +
    trs.map(t => `<button class="ftab" role="tab" data-act="lib-tab"''', '''aria-selected="${tab === "home"}">${ico("home", 16)}Overview</button><button class="ftab" role="tab" data-act="lib-tab" data-tr="cards" style="--tc:var(--c-rev)" aria-selected="${tab === "cards"}">${ico("cards", 16)}Cards<span class="meta num">${cardQueue().all.length}</span></button>` +
    trs.map(t => `<button class="ftab" role="tab" data-act="lib-tab"''')
rep('''let tab = UI.libTab || "home"; if (tab !== "home" && !trs.some(t => t.id === tab)) tab = "home";
  const mods''', '''let tab = UI.libTab || "home"; if (tab !== "home" && tab !== "cards" && !trs.some(t => t.id === tab)) tab = "home";
  const mods''')
rep('''      <section><div class="pbox"><div class="card-h">${eb("backup", "Add a volume")}</div>''', '''      <section><div class="pbox" style="--tc:var(--c-rev)"><div class="card-h">${eb("cards", "Cards")}<span class="meta num">${cardQueue().due.length} due · ${cardQueue().nw.length} new</span></div>
        <div class="row">${cardQueue().all.length ? `<button class="btn pri" data-act="rv-start">Review ${cardQueue().all.length} card${cardQueue().all.length === 1 ? "" : "s"}</button>` : `<span class="meta">Nothing due today.</span>`}<button class="btn" data-act="lib-tab" data-tr="cards">All cards</button></div>
        <div class="sub-h">${eb("ideas", "Quick card")}</div>${cardForm("q")}</div>
      <div class="pbox"><div class="card-h">${eb("backup", "Add a volume")}</div>''')
rep('''  } else {
    const vs = all.filter(o => o.v.tr === tab)''', '''  } else if (tab === "cards") {
    body = cardsTab();
  } else {
    const vs = all.filter(o => o.v.tr === tab)''')

CARDS = r'''/* ---------- cards: spaced review ---------- */
const NEW_PER_DAY = 10, RATE = ["Again", "Hard", "Good", "Easy"];
function quizPairs(v) {
  const L = v.lines, out = [], Q = {}, A = {};
  const grab = (from, stop) => {
    const res = []; let cur = null, fence = false;
    for (let n = from; n < L.length; n++) {
      const ln = L[n];
      if (/^\s*(```|~~~)/.test(ln)) { fence = !fence; if (cur) cur.t.push(ln); continue; }
      if (fence) { if (cur) cur.t.push(ln); continue; }
      if (stop.test(ln)) break;
      const m = /^(\d+)\.\s+(.*)$/.exec(ln);
      if (m) { cur = { n: +m[1], t: [m[2]] }; res.push(cur); continue; }
      if (cur) { if (/^\S/.test(ln) && !/^[-*>|]/.test(ln) && L[n - 1].trim() === "") break; cur.t.push(ln.replace(/^ {1,4}/, "")); }
      else if (ln.trim() && n > from + 4) break;
    }
    return res.map(x => ({ n: x.n, t: x.t.join("\n").trim() }));
  };
  let fence = false;
  L.forEach((ln, n) => {
    if (/^\s*(```|~~~)/.test(ln)) { fence = !fence; return; } if (fence) return;
    let m = /^(?:#{2,5}\s+|\*\*)Self-check quiz\s+([A-Z0-9]+\.Q\d+)/.exec(ln);
    if (m) { const sec = v.secs.find(x => x.a <= n && n < x.b); Q[m[1]] = { it: sec && sec.it, list: grab(n + 1, /^(#{1,6}\s|---\s*$|<\/?details|\*\*[A-Z])/) }; return; }
    m = /^<details><summary><b>([A-Z0-9]+\.Q\d+)<\/b>/.exec(ln);
    if (m) A[m[1]] = grab(n + 1, /^<\/details>/);
  });
  for (const id in Q) { if (!Q[id].it || !A[id]) continue; for (const q of Q[id].list) { const a = A[id].find(x => x.n === q.n); if (a && q.t && a.t) out.push({ key: id + "#" + q.n, it: Q[id].it, q: q.t, a: a.t }); } }
  return out;
}
function syncCards() {
  const have = new Set(S.cards.filter(c => c.key).map(c => c.key)); let n = 0, locked = 0;
  for (const v of VOLS) { v.quiz = v.quiz || quizPairs(v); for (const pr of v.quiz) { if (have.has(pr.key)) continue; const i = item(pr.it); if (!i || i.st !== "done") { locked++; continue; }
    S.cards.push(touch({ id: uid("C"), key: pr.key, src: "quiz", tr: i.tr, it: pr.it, vol: v.id, q: pr.q, a: pr.a, state: "new", due: "", ivl: 0, ease: 2.5, reps: 0, lapses: 0, ts: Date.now() + n })); n++; } }
  UI.locked = locked; if (n) { save(); setTimeout(() => toast(`Done. ${n} quiz card${n === 1 ? "" : "s"} released for review.`), 60); }
}
const cardsLive = () => S.cards.filter(c => !c.del);
function cardQueue(scope) {
  const t = todayIso(), cs = cardsLive().filter(c => !scope || c.tr === scope);
  const due = cs.filter(c => c.state !== "new" && c.due <= t).sort((a, b) => a.due < b.due ? -1 : a.due > b.due ? 1 : a.ts - b.ts);
  const left = Math.max(0, NEW_PER_DAY - (S.cardDay && S.cardDay.d === t ? S.cardDay.n : 0));
  const nw = cs.filter(c => c.state === "new").sort((a, b) => (a.src === "own" ? 0 : 1) - (b.src === "own" ? 0 : 1) || a.ts - b.ts).slice(0, left);
  return { due, nw, all: [...due, ...nw] };
}
function nextIvl(c, g) {
  if (c.state !== "review") return [0, 1, c.reps ? 3 : 2, 5][g];
  return g === 0 ? 0 : Math.max(c.ivl + 1, Math.round(c.ivl * (g === 1 ? 1.2 : g === 2 ? c.ease : c.ease * 1.3)));
}
const ivlText = d => d === 0 ? "in this round" : d < 30 ? d + " d" : d < 365 ? Math.round(d / 30.4 * 10) / 10 + " mo" : Math.round(d / 365 * 10) / 10 + " y";
function rateCard(c, g) {
  const ivl = nextIvl(c, g), t = todayIso();
  if (c.state === "new") { if (!S.cardDay || S.cardDay.d !== t) S.cardDay = { d: t, n: 0 }; S.cardDay.n++; }
  if (c.state === "review") { if (g === 0) { c.lapses++; c.ease = Math.max(1.3, c.ease - .2); } else if (g === 1) c.ease = Math.max(1.3, c.ease - .15); else if (g === 3) c.ease += .15; }
  c.reps++; c.last = t;
  if (g === 0) { c.state = "learn"; c.ivl = 0; c.due = t; } else { c.state = "review"; c.ivl = ivl; c.due = addDays(t, ivl); }
  touch(c);
}
function rvStart(scope) {
  const q = cardQueue(scope || "").all; if (!q.length) { toast("No cards are due."); return false; }
  if (UI.rv) rvEnd(true);
  UI.rv = { q: q.map(c => c.id), show: false, n: 0, ms: 0, t0: Date.now(), scope: scope || "", from: S.view === "review" ? "library" : S.view, done: null };
  S.view = "review"; return true;
}
function rvEnd(quiet) {
  const r = UI.rv; if (!r) return; UI.rv = null; if (r.done || !r.n) return;
  const mins = Math.max(1, Math.round(r.ms / 60000));
  if (!S.timer) { S.sessions.push(touch({ id: uid("S"), d: todayIso(), ts: Date.now(), m: mins, tr: "rev", it: null, label: "Card review", mode: null, note: `${r.n} card${r.n === 1 ? "" : "s"}`, off: false, cards: 1 })); if (!quiet) toast(`Logged ${mins} min of review`); save(); return mins; }
  save(); return 0;
}
function cardForm(sfx, trDefault) {
  const trs = SEED.tracks.filter(t => !t.recurring);
  return `<form class="cform" data-form="card-add"><label>Front: the question<textarea name="q" id="cq-${sfx}" required maxlength="2000" placeholder="One clear question"></textarea></label>
    <label>Back: the answer<textarea name="a" id="ca-${sfx}" required maxlength="4000"></textarea></label>
    <div class="row"><select name="tr" id="ct-${sfx}" aria-label="Track" style="width:auto;flex:1 1 140px">${trs.map(t => `<option value="${t.id}"${t.id === (trDefault || UI.cardTr || "sw") ? " selected" : ""}>${esc(t.name)}</option>`).join("")}</select><button class="btn pri" type="submit">Add card</button></div></form>`;
}
function cardDlg(c, preset) {
  const trs = SEED.tracks.filter(t => !t.recurring), isNew = !c, tr = c ? c.tr : preset.tr;
  openDlg(`<h2>${isNew ? "Add a card" : "Edit card"}</h2>${isNew && preset.it ? `<p class="meta">Tied to <code>${esc(preset.it)}</code></p>` : ""}
    <label>Front: the question<textarea name="q" id="cd-q" required maxlength="2000">${esc(c ? c.q : "")}</textarea></label>
    <label>Back: the answer<textarea name="a" id="cd-a" required maxlength="4000" style="min-height:110px">${esc(c ? c.a : "")}</textarea></label>
    <label>Track<select name="tr" id="cd-tr">${trs.map(t => `<option value="${t.id}"${t.id === tr ? " selected" : ""}>${esc(t.name)}</option>`).join("")}</select></label>
    <div class="row"><button class="btn pri" type="submit">Save</button><button class="btn" type="button" data-act="dlg-close">Cancel</button>${c ? `<button class="btn quiet danger" type="button" data-act="card-del" data-id="${esc(c.id)}">Delete</button>` : ""}</div>`,
    d => {
      const q = d.q.trim(), a = d.a.trim(); if (!q || !a) return false;
      if (isNew) { S.cards.push(touch({ id: uid("C"), key: "", src: "own", tr: d.tr, it: preset.it || "", vol: preset.vol || "", q, a, state: "new", due: "", ivl: 0, ease: 2.5, reps: 0, lapses: 0, ts: Date.now() })); toast("Card added. It joins today's new cards."); }
      else { Object.assign(c, { q, a, tr: d.tr }); touch(c); HTMLC.delete("card:" + c.id); }
      save();
    });
}
function cardsTab() {
  const t = todayIso(), cs = cardsLive(), qd = cardQueue(), trs = SEED.tracks.filter(x => !x.recurring), f = UI.cardF || "", qs = (UI.cardQ || "").toLowerCase();
  const list = cs.filter(c => (!f || c.tr === f) && (!qs || (c.q + " " + c.a).toLowerCase().includes(qs))).sort((a, b) => (a.state === "new" ? "9" : a.due) < (b.state === "new" ? "9" : b.due) ? -1 : 1), max = UI.cardMax || 40;
  const dueTxt = c => c.state === "new" ? "New" : c.due <= t ? "Due" : `in ${daysBetween(t, c.due)} d`;
  return `<div class="lv home" style="--tc:var(--c-rev)"><section>
    <div class="stats s2"><div class="stat"><b class="num">${qd.due.length}</b><span>due today</span></div><div class="stat"><b class="num">${qd.nw.length}</b><span>new today, of ${NEW_PER_DAY} a day</span></div><div class="stat"><b class="num">${cs.length}</b><span>cards in all</span></div><div class="stat"><b class="num">${UI.locked || 0}</b><span>waiting on unfinished lessons</span></div></div>
    <div class="row">${qd.all.length ? `<button class="btn pri lg" data-act="rv-start">Review ${qd.all.length} card${qd.all.length === 1 ? "" : "s"}</button>` : `<span class="meta">Nothing due today. Finishing a lesson releases its quiz cards.</span>`}${trs.map(x => { const n = cardQueue(x.id).all.length; return n && n < qd.all.length ? `<button class="btn" data-act="rv-start" data-tr="${x.id}">${esc(x.name)} only (${n})</button>` : ""; }).join("")}</div>
    <div class="sect-h" style="margin-top:6px">${eb("layers", `All cards (${list.length})`)}</div>
    <div class="cfilt"><input type="text" id="card-q" data-inp="card-q" value="${esc(UI.cardQ || "")}" placeholder="Search cards" aria-label="Search cards"><div class="seg" role="group" aria-label="Track filter"><button data-act="card-f" data-tr="" aria-pressed="${!f}">All</button>${trs.map(x => `<button data-act="card-f" data-tr="${x.id}" aria-pressed="${f === x.id}">${esc(x.name)}</button>`).join("")}</div></div>
    <div class="clist">` + (list.length ? list.slice(0, max).map(c => `<div class="crow" style="--tc:var(--c-${c.tr})"><span class="q"><span class="clamp1">${esc(c.q.replace(/\s+/g, " "))}</span><span class="meta">${ico(c.tr, 13)} ${c.src === "own" ? "Your card" : esc(c.key.replace("#", " · question "))}${c.lapses ? ` · missed ${c.lapses}×` : ""}</span></span><span class="tag due${c.state !== "new" && c.due <= t ? " sug" : ""}">${dueTxt(c)}</span><button class="btn sm" data-act="card-edit" data-id="${esc(c.id)}">Edit</button></div>`).join("") +
      (list.length > max ? `<div class="row" style="padding-top:10px"><button class="btn sm" data-act="card-more">Show ${Math.min(40, list.length - max)} more</button></div>` : "") : `<div class="empty">${cs.length ? "No cards match." : "No cards yet. Write one on the right, add one from inside a lesson, or finish a lesson to release its quiz cards."}</div>`) + `</div></section>
    <section><div class="pbox"><div class="card-h">${eb("cards", "Write a card")}</div><p class="lede">Your own cards join the day's new cards ahead of the quiz cards. Markdown, code and <code>$maths$</code> work on both sides.</p>${cardForm("c")}</div>
    <div class="pbox"><div class="card-h">${eb("review", "How reviews work")}</div><p class="howto">Rate each card after you answer it in your head. <b>Again</b> brings it back in the same round. <b>Hard</b>, <b>Good</b> and <b>Easy</b> push it further out each time; the button shows how far. Up to ${NEW_PER_DAY} new cards a day, every due card shown. Review time logs to the Review hours by itself.</p></div></section></div>`;
}
function viewReview() {
  if (!UI.rv && !rvStart("")) { S.view = "library"; UI.libTab = "cards"; return viewLibrary(); }
  const r = UI.rv, c = S.cards.find(x => x.id === r.q[0]), total = r.n + r.q.length;
  const head = `<div class="today-head">${sketch("cards")}<div class="th-text"><h2>Review</h2><p class="lede num">${r.done ? "Round finished" : `${r.n} rated · ${r.q.length} to go${r.scope ? " · " + esc(track(r.scope).name) + " only" : ""}`}</p></div><div class="head-r"><button class="btn sm" data-act="rv-end">${r.done ? "Close" : "End review"}</button></div></div>`;
  if (r.done || !c) {
    const d = r.done || { n: r.n, mins: 0 };
    return head + `<div class="rvwrap"><article class="card rvdone"><div class="big num">${d.n}<small>card${d.n === 1 ? "" : "s"} reviewed</small></div><p class="lede">${d.mins ? `${d.mins} min logged to Review.` : S.timer ? "Counted inside the running session." : ""} ${cardQueue().all.length ? `${cardQueue().all.length} more can be reviewed today.` : "Nothing else is due today."}</p>
      <div class="row" style="justify-content:center">${cardQueue().all.length ? `<button class="btn pri" data-act="rv-start">Keep going</button>` : ""}<button class="btn" data-act="lib-tab" data-tr="cards">All cards</button><button class="btn" data-act="view" data-v="today">Back to Today</button></div></article></div>`;
  }
  const src = c.src === "own" ? "Your card" : c.key.replace("#", " · question ");
  return head + `<div class="rvwrap" style="--tc:var(--c-${c.tr})"><div class="bar"><i style="width:${total ? r.n / total * 100 : 0}%"></i></div>
    <article class="card fc"><div class="fc-top"><span class="chip">${ico(c.tr, 15)} ${esc(track(c.tr).name)}</span><span>${esc(src)}${c.state === "new" ? " · new" : c.lapses ? ` · missed ${c.lapses}×` : ""}</span></div>
      <div class="prose" id="card-q-body">${HTMLC.get("card:" + c.id) ? HTMLC.get("card:" + c.id).q : esc(c.q)}</div>
      ${r.show ? `<div class="back"><div class="prose" id="card-a-body">${HTMLC.get("card:" + c.id) ? HTMLC.get("card:" + c.id).a : esc(c.a)}</div></div>` : ""}
      <div class="fc-act">${r.show ? `<div class="rate">${RATE.map((n, g) => `<button class="btn${g === 2 ? " pri" : ""}" data-act="rv-rate" data-g="${g}"><span>${n} <span class="kbd">${g + 1}</span></span><small>${ivlText(nextIvl(c, g))}</small></button>`).join("")}</div>` : `<button class="btn pri lg" data-act="rv-show">Show answer <span class="kbd">Space</span></button>`}
        <div class="row" style="justify-content:space-between"><button class="btn sm quiet" data-act="card-edit" data-id="${esc(c.id)}">Edit this card</button>${c.it && LMAP[c.it] ? `<button class="btn sm quiet" data-act="read-item" data-it="${esc(c.it)}">Open its lesson</button>` : ""}</div></div></article></div>`;
}
async function fillCard() {
  const r = UI.rv; if (!r || r.done) return; const c = S.cards.find(x => x.id === r.q[0]); if (!c) return; const k = "card:" + c.id;
  if (!HTMLC.has(k)) { await loadLibs(); HTMLC.set(k, { q: mdHtml(c.q), a: mdHtml(c.a) }); }
  if (UI.rv !== r || r.q[0] !== c.id) return; const h = HTMLC.get(k), q = $("#card-q-body"), a = $("#card-a-body"); if (q) q.innerHTML = h.q; if (a) a.innerHTML = h.a;
}
document.addEventListener("keydown", e => {
  if (!S || S.view !== "review" || !UI.rv || UI.rv.done || $("#dlg").open || /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) || e.ctrlKey || e.metaKey || e.altKey) return;
  if (!UI.rv.show && (e.key === " " || e.key === "Enter")) { e.preventDefault(); ACT["rv-show"](); }
  else if (UI.rv.show && /^[1-4]$/.test(e.key)) { e.preventDefault(); ACT["rv-rate"]({ dataset: { g: String(+e.key - 1) } }); }
});
document.addEventListener("input", e => { if (e.target.dataset && e.target.dataset.inp === "card-q") { UI.cardQ = e.target.value; UI.cardMax = 40; const pos = e.target.selectionStart; render(); const el = $("#card-q"); if (el) { el.focus(); el.setSelectionRange(pos, pos); } } });

'''
rep("/* ---------- library: lesson volumes, reader, reading timer ---------- */", CARDS + "/* ---------- library: lesson volumes, reader, reading timer ---------- */")
rep("const VIEWS = { library: viewLibrary,", "const VIEWS = { review: viewReview, library: viewLibrary,")
rep('  "lib-tab"(el) {', '''  "rv-start"(el) { if (rvStart(el && el.dataset.tr || "")) { save(); render(); toTop(); } },
  "rv-show"() { if (UI.rv) { UI.rv.show = true; render(); } },
  "rv-rate"(el) {
    const r = UI.rv; if (!r || !r.show) return; const c = S.cards.find(x => x.id === r.q[0]); if (!c) return; const g = +el.dataset.g, now = Date.now();
    r.ms += Math.min(120000, now - r.t0); r.t0 = now; rateCard(c, g); r.q.shift(); if (g === 0) r.q.push(c.id); else r.n++; r.show = false;
    if (!r.q.length) { const n = r.n, from = r.from; const mins = rvEnd(true) || 0; UI.rv = { q: [], n, done: { n, mins }, from, scope: "" }; }
    save(); render(); toTop();
  },
  "rv-end"() { const from = UI.rv && UI.rv.from; rvEnd(false); S.view = from && from !== "review" && from !== "read" ? from : "library"; save(); render(); toTop(); },
  "card-new"(el) { const v = vol(el.dataset.vol); cardDlg(null, { tr: v ? v.tr : "sw", it: el.dataset.it || "", vol: el.dataset.vol || "" }); },
  "card-edit"(el) { const c = S.cards.find(x => x.id === el.dataset.id); if (c) cardDlg(c); },
  "card-del"(el) {
    if (UI.armed !== "cdel") { UI.armed = "cdel"; el.textContent = "Confirm: delete this card"; el.classList.remove("quiet"); setTimeout(() => { if (UI.armed === "cdel") UI.armed = null; }, 6000); return; }
    UI.armed = null; const c = S.cards.find(x => x.id === el.dataset.id); if (c) { c.del = 1; touch(c); if (UI.rv) { UI.rv.q = UI.rv.q.filter(id => id !== c.id); UI.rv.show = false; if (!UI.rv.q.length) { const n = UI.rv.n, from = UI.rv.from, mins = rvEnd(true) || 0; UI.rv = { q: [], n, done: { n, mins }, from, scope: "" }; } } } save(); closeDlg(); render();
  },
  "card-f"(el) { UI.cardF = el.dataset.tr; UI.cardMax = 40; render(); },
  "card-more"() { UI.cardMax = (UI.cardMax || 40) + 40; render(); },
  "lib-tab"(el) {''')
rep('''  "add-proof"(d) {''', '''  "card-add"(d) { const q = (d.q || "").trim(), a = (d.a || "").trim(); if (!q || !a) return; UI.cardTr = d.tr; S.cards.push(touch({ id: uid("C"), key: "", src: "own", tr: d.tr, it: "", vol: "", q, a, state: "new", due: "", ivl: 0, ease: 2.5, reps: 0, lapses: 0, ts: Date.now() })); save(); toast("Card added. It joins today's new cards."); },
  "add-proof"(d) {''')
s = s.replace("M7 7V5.500A1.500 1.500 0 018.500 4H19.500A1.500 1.500 0 0121 5.500V14.500A1.500 1.500 0 0119.500 16H17", "M7 7V5.5A1.5 1.5 0 018.5 4h11A1.5 1.5 0 0121 5.5v9a1.5 1.5 0 01-1.5 1.5H17").replace("M27 25l18 1.500M26.500 32l12 1", "M27 25l18 1.5M26.5 32l12 1")
open(p, "w", encoding="utf-8").write(s)
print("ok 3.0")
