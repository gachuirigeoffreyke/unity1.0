"""2.0: Library, lesson reader and reading timer. Runs after v9_patch.py."""
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "template.html")
s = open(p, encoding="utf-8").read()
css = open(os.path.join(here, "v10_style.css"), encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)

def rep_between(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i); s = s[:i] + new + s[j:]

rep("</style>", css + "</style>")
rep('const VERSION = "1.8";', 'const VERSION = "2.0";')

rep("const ICON = {\n", """const ICON = {
  read: '<path d="M12 6.5c-2.2-1.6-5.2-2-8-1.5v13c2.8-.5 5.8 0 8 1.5 2.2-1.5 5.2-2 8-1.5v-13c-2.8-.5-5.8-.1-8 1.5zM12 6.5v13"/>',
  library: '<path d="M12 6.5c-2.2-1.6-5.2-2-8-1.5v13c2.8-.5 5.8 0 8 1.5 2.2-1.5 5.2-2 8-1.5v-13c-2.8-.5-5.8-.1-8 1.5zM12 6.5v13"/>',
""")
rep("const SK = {\n", """const SK = {
  read: '<circle cx="44" cy="22" r="11" fill="#f2c94c" stroke="none" opacity=".55"/><path d="M32 17c-6-5-15-6-24-4v36c9-2 18-1 24 4 6-5 15-6 24-4V13c-9-2-18-1-24 4zM32 17v36"/><path d="M14 23c4-.6 8-.2 12 1.5M14 31c4-.6 8-.2 12 1.5M38 24.5c4-1.7 8-2.1 12-1.5"/>',
""")

# storage for imported volumes
rep("  put(v) {\n    if (this.db) { try { this.db.transaction(\"kv\", \"readwrite\")", '''  getK(k) {
    return new Promise(res => {
      if (this.db) { try { const q = this.db.transaction("kv").objectStore("kv").get(k); q.onsuccess = () => res(q.result || null); q.onerror = () => res(null); } catch (e) { res(null); } }
      else { try { const v = localStorage.getItem("unity.k." + k); res(v ? JSON.parse(v) : null); } catch (e) { res(null); } }
    });
  },
  putK(k, v) {
    if (this.db) { try { this.db.transaction("kv", "readwrite").objectStore("kv").put(v, k); return true; } catch (e) { /* fall through */ } }
    try { localStorage.setItem("unity.k." + k, JSON.stringify(v)); return true; } catch (e) { return false; }
  },
  put(v) {
    if (this.db) { try { this.db.transaction("kv", "readwrite")''')

# nav: Library in the top bar and the phone bar
rep('["plan", "Plan"], ["ideas", "Ideas"], ["proof", "Portfolio"]]', '["plan", "Plan"], ["library", "Library"], ["ideas", "Ideas"], ["proof", "Portfolio"]]')
rep('''.map(([id, n]) => `<button data-act="view" data-v="${id}"${S.view === id ? cur : ""}>${ico(id, 17)}${n}${id === "ideas" ? badge : ""}</button>`).join("");''',
    '''.map(([id, n]) => `<button data-act="view" data-v="${id}"${S.view === id || (id === "library" && S.view === "read") ? cur : ""}>${ico(id, 17)}${n}${id === "ideas" ? badge : ""}</button>`).join("");''')
rep('[["home", "Home"], ["today", "Today"], ["week", "Week"], ["plan", "Plan"], ["ideas", "Ideas"], ["more", "More"]]', '[["home", "Home"], ["today", "Today"], ["week", "Week"], ["plan", "Plan"], ["library", "Library"], ["ideas", "Ideas"], ["more", "More"]]')
rep('''${S.view === id || (id === "home" && S.view === "track") ? cur : ""}>${ico(id)}${n}''', '''${S.view === id || (id === "home" && S.view === "track") || (id === "library" && S.view === "read") ? cur : ""}>${ico(id)}${n}''')
rep('''$("#topmeta").innerHTML = (S.timer ? `<button class="pill" data-act="view" data-v="today" aria-label="Session running, open Today"><i class="live"></i><span id="clock2">00:00</span></button>` : "") +''',
    '''$("#topmeta").innerHTML = (S.timer ? `<button class="pill" data-act="view" data-v="today" aria-label="Session running, open Today"><i class="live"></i><span id="clock2">00:00</span></button>` : (S.rt && S.view !== "read" ? `<button class="pill" data-act="read-item" data-it="${esc(S.rt.it)}" aria-label="Reading paused, back to the lesson" title="Reading paused. Back to the lesson">${ico("read", 15)}<span>${rtText()}</span></button>` : "")) +''')
rep('<div class="th-text"><h2>Settings and backup</h2><p class="lede">The weekly split, pauses for paid work, and the backup that keeps laptop and phone in step.</p></div></div>`;',
    '<div class="th-text"><h2>Settings and backup</h2><p class="lede">The weekly split, pauses for paid work, and the backup that keeps laptop and phone in step.</p></div><div class="head-r"><button class="btn sm" data-act="view" data-v="proof">Portfolio</button></div></div>`;')

# Read lesson buttons
rep('''        <button class="btn quiet" data-act="open-plan" data-tr="${tr.id}">Queue</button></div></article>`;''',
    '''        ${LMAP[it.id] ? `<button class="btn quiet" data-act="read-item" data-it="${esc(it.id)}">Read</button>` : `<button class="btn quiet" data-act="open-plan" data-tr="${tr.id}">Queue</button>`}</div></article>`;''')
rep('''<button class="btn lg" data-act="view" data-v="today">All of today</button></div>${after(sgs.slice(1, 3))}''', '''${readBtn(it, "lg")}<button class="btn lg" data-act="view" data-v="today">All of today</button></div>${after(sgs.slice(1, 3))}''')
rep('''<button class="btn lg" data-act="item-done" data-it="${esc(cur.id)}">Mark done</button></div>${after}</article>`);''', '''${readBtn(cur, "lg")}<button class="btn lg" data-act="item-done" data-it="${esc(cur.id)}">Mark done</button></div>${after}</article>`);''')
rep('''<div class="row"><button class="btn pri" data-act="stop">Stop and log</button></div></article>`);''', '''<div class="row"><button class="btn pri" data-act="stop">Stop and log</button>${readBtn(it)}</div></article>`);''')
rep('''<div class="row"><button class="btn pri lg" data-act="stop">Stop and log</button></div>${after(sgs''', '''<div class="row"><button class="btn pri lg" data-act="stop">Stop and log</button>${readBtn(it, "lg")}</div>${after(sgs''')
rep('''<div class="row"><button class="btn pri lg" data-act="stop">Stop and log</button></div>${after}</article>`);''', '''<div class="row"><button class="btn pri lg" data-act="stop">Stop and log</button>${readBtn(cur, "lg")}</div>${after}</article>`);''')
rep('''<button class="btn pri" data-act="start" data-tr="${trId}" data-it="${esc(nx.id)}">Start session</button><button class="btn" data-act="item-done" data-it="${esc(nx.id)}">Mark done</button></div></div>` : `<div class="nextbox"><h3>Queue finished''',
    '''<button class="btn pri" data-act="start" data-tr="${trId}" data-it="${esc(nx.id)}">Start session</button>${readBtn(nx)}<button class="btn" data-act="item-done" data-it="${esc(nx.id)}">Mark done</button></div></div>` : `<div class="nextbox"><h3>Queue finished''')
rep('''        <button class="btn sm" data-act="item-edit" data-it="${esc(i.id)}">Edit</button>${lm > 0 ?''', '''        ${readBtn(i, "sm")}<button class="btn sm" data-act="item-edit" data-it="${esc(i.id)}">Edit</button>${lm > 0 ?''')
rep('''function lessonTag(i) {
  if (i.c) return''', '''function lessonTag(i) {
  if (i.c || LMAP[i.id]) return''')

# a session start closes any reading stretch first; reading pauses outside the reader
rep('''  if (S.timer) { toast("A session is already running. Stop it first."); return; }
  S.timer = {''', '''  if (S.timer) { toast("A session is already running. Stop it first."); return; }
  rtClose(true);
  S.timer = {''')
rep('''  if (!VIEWS[S.view]) S.view = "home";
  applyTheme();''', '''  if (!VIEWS[S.view]) S.view = "home";
  if (S.view !== "read" && S.rt && S.rt.start) rtPause("left");
  applyTheme();''')
rep('''  $("#main").innerHTML = VIEWS[S.view]();
  tick();''', '''  $("#main").innerHTML = VIEWS[S.view]();
  if (S.view === "read") fillLesson();
  tick();''')
rep('''  const c = $("#clock"), c2 = $("#clock2");''', '''  rtTick();
  const c = $("#clock"), c2 = $("#clock2");''')
rep('''document.addEventListener("visibilitychange", () => { if (document.hidden && S) { clearTimeout(saveT); DB.put(S); } else if (S) render(); });''',
    '''document.addEventListener("visibilitychange", () => {
  if (!S) return;
  if (document.hidden) { if (S.rt && S.rt.start) rtPause("hidden"); clearTimeout(saveT); DB.put(S); }
  else if (S.view === "read") { lastAct = Date.now(); if (S.rt && !S.rt.start && S.rt.why === "hidden") { S.rt.start = Date.now(); S.rt.why = ""; } renderNav(); rtTick(); }
  else render();
});
for (const ev of ["pointerdown", "keydown", "wheel", "touchmove"]) document.addEventListener(ev, noteAct, { passive: true });
document.addEventListener("scroll", noteAct, { passive: true, capture: true });''')
rep('''  migrate();
  const have = new Set(S.items.map(i => i.id));''', '''  migrate();
  if (S.rt && S.rt.start) { S.rt.start = null; S.rt.why = "left"; }
  loadVols();
  const have = new Set(S.items.map(i => i.id));''')

LIB = r'''/* ---------- library: lesson volumes, reader, reading timer ---------- */
const SHIPPED = ["FSE-C01-Workbench.md", "FSE-C02a-Python.md", "FSE-C11a-CSFoundations.md", "STR-V01-Mechanics-Maths.md"];
let VOLS = [], LMAP = {}, volsReady = false, libsP = null, lastAct = Date.now();
const HTMLC = new Map();
const readBtn = (i, cls = "") => i && LMAP[i.id] ? `<button class="btn ${cls}" data-act="read-item" data-it="${esc(i.id)}">${ico("read", 15)}Read lesson</button>` : "";
function parseVol(name, text, shipped) {
  const lines = text.split(/\r?\n/), secs = []; let fence = false, title = "";
  lines.forEach((ln, n) => {
    if (/^\s*(```|~~~)/.test(ln)) { fence = !fence; return; } if (fence) return;
    if (!title && /^# +\S/.test(ln)) title = ln.replace(/^# +/, "").trim();
    const m = /^## +(.*)$/.exec(ln); if (!m) return;
    const mm = /^\[([A-Z0-9]+(?:\.[A-Z0-9]+)+)\]\s*(.*)$/.exec(m[1].trim());
    secs.push({ a: n, t: (mm ? mm[2] : m[1]).replace(/[*_`]/g, "").trim(), mod: mm ? mm[1] : "" });
  });
  if (!secs.length || secs[0].a > 0) secs.unshift({ a: 0, t: "About this volume", mod: "" });
  secs.forEach((x, k) => x.b = k + 1 < secs.length ? secs[k + 1].a : lines.length);
  title = title || name.replace(/\.(md|markdown|txt)$/i, "");
  const pre = (/^([A-Z]{2,6})[-·\s]/.exec(title) || /^([A-Z]{2,6})-/.exec(name) || [])[1] || "";
  const cnt = {};
  for (const x of secs) if (x.mod) { const it = S.items.find(i => i.id === pre + "." + x.mod) || S.items.find(i => i.id.endsWith("." + x.mod)); if (it) { x.it = it.id; cnt[it.tr] = (cnt[it.tr] || 0) + 1; } }
  const tr = Object.keys(cnt).sort((a, b) => cnt[b] - cnt[a])[0] || (pre === "STR" ? "str" : "sw");
  return { id: name, name, title, shipped, lines, secs, tr };
}
function indexVols() {
  LMAP = {}; HTMLC.clear(); let ch = false;
  VOLS.sort((a, b) => a.name.localeCompare(b.name));
  VOLS.forEach(v => v.secs.forEach((x, k) => { if (x.it) { LMAP[x.it] = { v: v.id, s: k }; const i = item(x.it); if (i && !i.c) { i.c = 1; i.src = i.src || v.name; touch(i); ch = true; } } }));
  if (ch) save();
}
async function loadVols() {
  const got = [];
  await Promise.all(SHIPPED.map(async n => { try { const r = await fetch("volumes/" + n); if (r.ok) got.push(parseVol(n, await r.text(), true)); } catch (e) { /* offline before first cache */ } }));
  const mine = (await DB.getK("vols")) || [];
  for (const m of mine) { const k = got.findIndex(v => v.id === m.name); const pv = parseVol(m.name, m.text, false); if (k >= 0) got[k] = pv; else got.push(pv); }
  VOLS = got; volsReady = true; indexVols(); render();
}
const vol = id => VOLS.find(v => v.id === id);
function loadLibs() {
  if (!libsP) libsP = Promise.all(["lib/marked.min.js", "lib/katex.min.js"].map(src => new Promise(res => { const el = document.createElement("script"); el.src = src; el.onload = () => res(true); el.onerror = () => res(false); document.head.appendChild(el); })));
  return libsP;
}
function mdHtml(src) {
  const math = [], keep = (tex, block) => { math.push({ tex, block }); return `@@M${math.length - 1}@@`; };
  let out = "";
  const seg = src.split(/((?:^|\n)[ \t]*(?:```|~~~)[\s\S]*?\n[ \t]*(?:```|~~~)[ \t]*(?=\n|$)|`[^`\n]+`)/);
  seg.forEach((p, k) => {
    out += k % 2 ? p : p.replace(/\$\$([\s\S]+?)\$\$/g, (m, t) => keep(t, true)).replace(/(^|[^\\$\w])\$([^\s$](?:[^$\n]*?[^\s$\\])?)\$(?![\w$])/g, (m, a, t) => a + keep(t, false));
  });
  let html = window.marked ? marked.parse(out, { gfm: true, breaks: true }) : `<pre>${esc(src)}</pre>`;
  html = html.replace(/@@M(\d+)@@/g, (m, k) => { const x = math[+k]; try { return window.katex ? (x.block ? `<div class="mathw">` : "") + katex.renderToString(x.tex, { displayMode: x.block, output: "mathml", throwOnError: false, strict: false }) + (x.block ? `</div>` : "") : esc(x.block ? `$$${x.tex}$$` : `$${x.tex}$`); } catch (e) { return esc(`$${x.tex}$`); } });
  const t = document.createElement("template"); t.innerHTML = html;
  t.content.querySelectorAll("script,style,iframe,object,embed,link,meta,form,base").forEach(e => e.remove());
  t.content.querySelectorAll("*").forEach(e => { for (const a of [...e.attributes]) if (/^on/i.test(a.name) || (/^(href|src|xlink:href)$/i.test(a.name) && /^\s*(javascript|data|vbscript):/i.test(a.value))) e.removeAttribute(a.name); });
  t.content.querySelectorAll("a[href]").forEach(a => { if (/^https?:/i.test(a.getAttribute("href"))) { a.target = "_blank"; a.rel = "noopener"; } else a.dataset.in = "1"; });
  t.content.querySelectorAll("table").forEach(tb => { const w = document.createElement("div"); w.className = "tblw"; tb.replaceWith(w); w.appendChild(tb); });
  return t.innerHTML;
}
function readPos() {
  const r = S.lastRead; if (!r) return null; const v = vol(r.v); if (!v) return null;
  return { v, k: Math.max(0, Math.min(v.secs.length - 1, r.s | 0)) };
}
async function fillLesson() {
  const el = $("#lesson"), p = readPos(); if (!el || !p) return;
  const key = p.v.id + "#" + p.k;
  if (!HTMLC.has(key)) { await loadLibs(); const x = p.v.secs[p.k]; HTMLC.set(key, mdHtml(p.v.lines.slice(x.a, x.b).join("\n"))); }
  const el2 = $("#lesson"), p2 = readPos(); if (el2 && p2 && p2.v.id + "#" + p2.k === key) el2.innerHTML = HTMLC.get(key);
}
function openLesson(vId, k, keepFrom) {
  const v = vol(vId); if (!v) { toast("That lesson is not on this device yet."); return; }
  if (S.view !== "read" && !keepFrom) UI.readFrom = S.view;
  S.lastRead = { v: vId, s: k }; S.readPos = S.readPos || {}; S.readPos[vId] = k; S.view = "read";
  const x = v.secs[k]; lastAct = Date.now();
  if (!S.timer) { if (x.it) rtStart(x.it, vId); else if (S.rt && S.rt.vol === vId && !S.rt.start && S.rt.why !== "user") { S.rt.start = Date.now(); S.rt.why = ""; } }
  save(); render(); toTop();
}
/* reading timer: counts while a lesson is open, pauses when you leave or go idle, logs when you close */
const rtMs = () => S.rt ? S.rt.acc + (S.rt.start ? Date.now() - S.rt.start : 0) : 0;
function rtText() { const s = Math.floor(rtMs() / 1000), hh = Math.floor(s / 3600); return (hh ? hh + ":" : "") + pad(Math.floor(s % 3600 / 60)) + ":" + pad(s % 60); }
function rtStart(itId, vId) {
  if (S.rt && S.rt.it !== itId) rtClose(true);
  if (!S.rt) { const i = item(itId); S.rt = { it: itId, tr: i ? i.tr : "sw", vol: vId, acc: 0, start: Date.now(), why: "" }; }
  else if (!S.rt.start && S.rt.why !== "user") { S.rt.start = Date.now(); S.rt.why = ""; }
}
function rtPause(why, at) { const r = S.rt; if (!r || !r.start) return; r.acc += Math.max(0, (at || Date.now()) - r.start); r.start = null; r.why = why; save(); }
function rtClose(quiet) {
  const r = S.rt; if (!r) return 0; rtPause("close"); const mins = Math.round(r.acc / 60000); S.rt = null;
  if (mins >= 2) { S.sessions.push(touch({ id: uid("S"), d: todayIso(), ts: Date.now(), m: mins, tr: r.tr, it: r.it, label: "", mode: null, note: "Reading", off: false, read: 1 })); toast(`Logged ${mins} min of reading`); }
  else if (!quiet) toast("Under two minutes, so nothing was logged.");
  save(); return mins;
}
function noteAct() {
  lastAct = Date.now();
  if (S && S.rt && !S.rt.start && S.rt.why === "idle" && S.view === "read" && !document.hidden) { S.rt.start = Date.now(); S.rt.why = ""; rtTick(); }
}
function rtTick() {
  const r = S && S.rt; if (!r) return;
  if (r.start && Date.now() - lastAct > 5 * 60000) rtPause("idle", Math.max(r.start, lastAct));
  else if (r.start && Date.now() - r.start > 60000) { r.acc += Date.now() - r.start; r.start = Date.now(); save(); }
  const b = $("#rclock"); if (b) b.textContent = rtText();
  const w = $("#rtbox"); if (w) { const on = !!r.start; if (w.dataset.on !== String(on)) { w.dataset.on = String(on); w.classList.toggle("on", on); const l = $("#rtlbl"), t = $("#rttog"); if (l) l.textContent = on ? "Reading" : r.why === "idle" ? "Paused: no activity for five minutes" : "Paused"; if (t) t.textContent = on ? "Pause" : "Resume"; } }
}
function viewLibrary() {
  const L = logged(), mods = VOLS.reduce((a, v) => a + v.secs.filter(x => x.mod).length, 0);
  const head = `<div class="today-head">${sketch("read")}<div class="th-text"><h2>Library</h2><p class="lede num">${volsReady ? `${VOLS.length} volume${VOLS.length === 1 ? "" : "s"} · ${mods} lessons. Open one to read; the reading timer logs the time to its item.` : "Loading the volumes…"}</p></div></div>`;
  const cards = VOLS.map(v => {
    const ms = v.secs.map((x, k) => ({ x, k })).filter(o => o.x.mod), done = ms.filter(o => o.x.it && item(o.x.it) && item(o.x.it).st === "done").length;
    const nxt = ms.find(o => o.x.it && item(o.x.it) && item(o.x.it).st === "open"), pos = (S.readPos || {})[v.id];
    const go = pos != null ? pos : (nxt ? nxt.k : 0);
    return `<article class="card vcard" style="--tc:var(--c-${v.tr})"><div class="card-h"><span class="chip">${ico(v.tr, 15)} ${esc(track(v.tr).name)}</span><span class="tag">${v.shipped ? "Built in" : "Imported"}</span></div><h3>${esc(v.title)}</h3>
      <div class="meta num">${ms.length} lesson${ms.length === 1 ? "" : "s"} · ${done} done · ${v.secs.length} sections</div><div class="bar"><i style="width:${ms.length ? done / ms.length * 100 : 0}%"></i></div>
      <div class="vmods">${ms.map(o => { const i = o.x.it && item(o.x.it); return `<button class="vmod${i && i.st === "done" ? " done" : ""}" data-act="read-open" data-vol="${esc(v.id)}" data-s="${o.k}"><code>${esc(o.x.mod)}</code><span class="t clamp1">${esc(o.x.t)}</span><span class="meta num">${i && L[i.id] ? hrs(L[i.id]) + " h" : ""}</span></button>`; }).join("")}</div>
      <div class="row" style="margin-top:auto;padding-top:6px"><button class="btn pri" data-act="read-open" data-vol="${esc(v.id)}" data-s="${go}">${pos != null ? "Continue" : "Open"}</button><button class="btn quiet" data-act="read-open" data-vol="${esc(v.id)}" data-s="0">From the start</button>${v.shipped ? "" : `<button class="btn quiet danger" data-act="vol-del" data-id="${esc(v.id)}">${UI.armed === "vol" + v.id ? "Confirm: remove" : "Remove"}</button>`}</div></article>`;
  }).join("");
  const lr = readPos(), r = S.rt, ri = r && item(r.it);
  const need = SEED.tracks.filter(t => !t.recurring).map(t => ({ t, n: S.items.filter(i => i.tr === t.id && i.st === "open" && !i.prod && !LMAP[i.id]).length, all: S.items.filter(i => i.tr === t.id && i.st === "open" && !i.prod).length }));
  const side = `<article class="card"><div class="card-h">${eb("read", "Continue reading")}</div>` + (lr ? `<h3>${esc(lr.v.secs[lr.k].t)}</h3><div class="meta">${esc(lr.v.title)}</div>` +
      (r ? `<div class="note">Reading time not yet logged: ${Math.round(rtMs() / 60000)} min${ri ? " on " + esc(ri.id) : ""}.</div>` : "") +
      `<div class="row"><button class="btn pri" data-act="read-open" data-vol="${esc(lr.v.id)}" data-s="${lr.k}">Back to the lesson</button>${r ? `<button class="btn" data-act="rt-log">Log it now</button>` : ""}</div>` : `<div class="empty">Nothing opened yet. Pick a lesson from a volume.</div>`) + `</article>
    <article class="card"><div class="card-h">${eb("backup", "Add a volume")}</div><p class="lede">When a new volume is written, add its <code>.md</code> file here. It stays on this device, so add it on the phone too.</p>
      <label>Volume files<input type="file" id="vol-file" accept=".md,.markdown,.txt,text/markdown,text/plain" multiple></label><div class="row"><button class="btn" data-act="vol-import">Add to the library</button></div></article>
    <article class="card"><div class="card-h">${eb("layers", "Lessons still to write")}</div>` + need.map(o => `<div class="arow" style="--tc:var(--c-${o.t.id})"><span>${esc(o.t.name)}</span><span class="meta num">${o.n} of ${o.all} open items</span></div>`).join("") + `<p class="meta">Items without a lesson show "Lesson not written yet". Ask Claude for the volume, then add it above.</p></article>`;
  return head + `<div class="dash lbpage"><div class="lb-a vcards">${cards || `<div class="empty">${volsReady ? "No volumes on this device. Go online once so the built-in ones download, or add a file." : "Loading…"}</div>`}</div><div class="lb-b">${side}</div></div>`;
}
function viewRead() {
  const p = readPos();
  if (!p) return `<div class="today-head">${sketch("read")}<div class="th-text"><h2>Library</h2><p class="lede">${volsReady ? "That lesson is not on this device." : "Opening the lesson…"}</p></div><div class="head-r"><button class="btn sm" data-act="view" data-v="library">Library</button></div></div>`;
  const v = p.v, k = p.k, x = v.secs[k], i = x.it && item(x.it), L = logged(), r = S.rt, on = !!(r && r.start);
  const head = `<div class="today-head">${sketch("read")}<div class="th-text"><h2>${esc(v.title)}</h2><p class="lede num">Section ${k + 1} of ${v.secs.length} · ${esc(track(v.tr).name)}</p></div><div class="head-r nophone"><button class="btn sm" data-act="view" data-v="library">Library</button></div></div>`;
  const toc = `<details class="card rd-toc" style="--tc:var(--c-${v.tr})"${window.matchMedia("(min-width:1100px)").matches || UI.tocOpen ? " open" : ""}><summary>${eb("plan", `Contents · ${k + 1} of ${v.secs.length}`)}</summary><div class="tocl">` +
    v.secs.map((y, n) => { const yi = y.it && item(y.it); return `<button class="toci${yi && yi.st === "done" ? " done" : ""}" data-act="read-open" data-vol="${esc(v.id)}" data-s="${n}" aria-current="${n === k}"><span>${esc(y.t)}</span>${y.mod ? `<small>${esc(y.mod.replace(/^.*\./, ""))}</small>` : ""}</button>`; }).join("") + `</div></details>`;
  const timer = S.timer ? `<div class="rt on"><i></i><span>A session is running. This reading counts inside it.</span></div>` :
    r ? `<div class="rt${on ? " on" : ""}" id="rtbox" data-on="${on}"><i></i><b id="rclock">${rtText()}</b><span id="rtlbl">${on ? "Reading" : r.why === "idle" ? "Paused: no activity for five minutes" : "Paused"}</span><button class="btn sm" data-act="rt-toggle" id="rttog">${on ? "Pause" : "Resume"}</button></div>` :
    `<div class="rt"><i></i><span>Not timed. The reading timer runs on lessons that belong to a plan item.</span></div>`;
  const nav = `<button class="btn sm" data-act="read-nav" data-dir="-1"${k === 0 ? " disabled" : ""}>‹ Previous</button><button class="btn sm" data-act="read-nav" data-dir="1"${k === v.secs.length - 1 ? " disabled" : ""}>Next ›</button>`;
  const main = `<article class="card rd-main"><div class="rd-bar">${timer}<div class="row">${nav}<button class="btn sm pri" data-act="read-close">${r ? "Close and log" : "Close"}</button></div></div>` +
    (i ? `<div class="rd-item" style="--tc:var(--c-${i.tr})"><span class="chip">${ico(i.tr, 15)} ${esc(track(i.tr).name)}</span><code>${esc(i.id)}</code><span class="num">${hrs(L[i.id] || 0)}${i.h > 0 ? ` of ${hnum(i.h)}` : ""} h logged</span>${i.st === "done" ? `<span class="tag good">Done</span>` : `<button class="btn sm quiet" data-act="item-done" data-it="${esc(i.id)}">Mark done</button>`}</div>` : "") +
    `<div class="prose" id="lesson">${HTMLC.get(v.id + "#" + k) || `<p class="meta">Opening…</p>`}</div><div class="rd-foot">${nav}</div></article>`;
  return head + `<div class="rd">${toc}${main}</div>`;
}

'''
rep("const VIEWS = { home: viewHome,", LIB + "const VIEWS = { library: viewLibrary, read: viewRead, home: viewHome,")

rep('  "to-plan"(el) {', '''  "read-item"(el) { const m = LMAP[el.dataset.it]; if (!m) { toast("No lesson for this item on this device yet."); return; } openLesson(m.v, m.s); },
  "read-open"(el) { openLesson(el.dataset.vol, +el.dataset.s); },
  "read-nav"(el) { const p = readPos(); if (!p) return; const k = p.k + (+el.dataset.dir); if (k >= 0 && k < p.v.secs.length) openLesson(p.v.id, k); },
  "read-close"() { rtClose(false); S.view = UI.readFrom && UI.readFrom !== "read" ? UI.readFrom : "library"; UI.readFrom = null; save(); render(); toTop(); },
  "rt-toggle"() { const r = S.rt; if (!r) return; if (r.start) rtPause("user"); else { r.start = Date.now(); r.why = ""; lastAct = Date.now(); save(); } rtTick(); },
  "rt-log"() { rtClose(false); render(); },
  async "vol-import"() {
    const fs = [...($("#vol-file").files || [])]; if (!fs.length) { toast("Choose one or more .md files first."); return; }
    const mine = (await DB.getK("vols")) || []; let n = 0;
    for (const f of fs) { const text = await f.text(); if (!/^## /m.test(text)) { toast(`${f.name} has no "## " sections, so it was skipped.`); continue; } const k = mine.findIndex(m => m.name === f.name); const rec = { name: f.name, text, ts: Date.now() }; if (k >= 0) mine[k] = rec; else mine.push(rec); n++; }
    if (!n) return; if (!DB.putK("vols", mine)) { toast("This device has no room to store the volume."); return; }
    await loadVols(); toast(`${n} volume${n === 1 ? "" : "s"} added`);
  },
  async "vol-del"(el) { const id = el.dataset.id; if (!arm("vol" + id)) return; const mine = ((await DB.getK("vols")) || []).filter(m => m.name !== id); DB.putK("vols", mine); if (S.lastRead && S.lastRead.v === id) S.lastRead = null; await loadVols(); toast("Volume removed"); },
  "to-plan"(el) {''')
# in-lesson links: contents anchors jump to the matching section
rep('''document.addEventListener("click", e => { const el = e.target.closest("[data-act]");''', '''document.addEventListener("click", e => {
  const a = e.target.closest("#lesson a[data-in]"); if (!a) return; e.preventDefault();
  const p = readPos(), slug = t => t.toLowerCase().replace(/[^a-z0-9]+/g, ""), want = slug(a.textContent || "");
  const k = p && want ? p.v.secs.findIndex(x => { const s2 = slug((x.mod ? x.mod : "") + x.t), s3 = slug(x.t); return s2 === want || s3 === want || (want.length > 5 && (s3.startsWith(want) || want.endsWith(s3))); }) : -1;
  if (k >= 0) openLesson(p.v.id, k);
});
document.addEventListener("toggle", e => { if (e.target.classList && e.target.classList.contains("rd-toc")) UI.tocOpen = e.target.open; }, true);
document.addEventListener("click", e => { const el = e.target.closest("[data-act]");''')
open(p, "w", encoding="utf-8").write(s)
print("ok 2.0")
