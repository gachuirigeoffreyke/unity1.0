"""1.8: Proof becomes Portfolio, with an overview tab and a tab per track. Runs after v8_patch.py."""
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "template.html")
s = open(p, encoding="utf-8").read()
css = open(os.path.join(here, "v9_style.css"), encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)

def rep_between(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i); s = s[:i] + new + s[j:]

rep("</style>", css + "</style>")
rep('const VERSION = "1.7";', 'const VERSION = "1.8";')
rep('["ideas", "Ideas"], ["proof", "Proof"]]', '["ideas", "Ideas"], ["proof", "Portfolio"]]')

# data: portfolio entries, seeded once, carried in backups
rep("function migrate() {", r'''const PST = { building: "Building", shipped: "Shipped", scoped: "Scoped", paused: "Paused" };
const PMODE = { "": "Build mode not set", personal: "Built personally", ai: "Built with AI", agents: "Directing agents" };
const PSEED = [
  ["P01", "Chama App", "Contribution, loan and M-Pesa reconciliation records for a savings group. Client product.", "building", "ai", "Release date being reset."],
  ["P02", "Backbone ERP core + Forecourt PMO", "Multi-tenant ERP platform; Forecourt PMO is the first module. Lead startup product.", "paused", "", "Waits for the startup criteria."],
  ["P03", "POS module", "Point of sale with eTIMS and an M-Pesa till. A Backbone ERP module.", "scoped", "", "Part of the paused startup build."],
  ["P04", "Field Management / CRM module", "Work orders, technicians, site visits and SLAs. A Backbone ERP module.", "scoped", "", "Part of the paused startup build."],
  ["P05", "Planty Pal", "Plant-commerce storefront, adding services in later phases. Own business.", "scoped", "", ""],
  ["P06", "Farm Management System", "Farm records and offline field capture, plus IoT sensors. Own use first.", "scoped", "", ""],
  ["P07", "Parent-Child App", "Parental controls and monitoring, plus child learning and guidance.", "scoped", "", "Policy review comes first."],
  ["P08", "TSW (THE SECRET WEAPON)", "Local-first personal OS for mastery across six tracks. Own tool.", "scoped", "", "Design volumes in progress."],
  ["P09", "Tourism website", "Website for a new company serving international tourists to Kenya. Possible client.", "scoped", "", "Quotation being prepared."]
].map((a, k) => ({ id: a[0], tr: "sw", name: a[1], desc: a[2], st: a[3], mode: a[4], note: a[5], ev: "", on: "", o: (k + 1) * 10 }));
const PRANK = { building: 0, shipped: 1, scoped: 2, paused: 3 };
const port = trId => S.port.filter(e => !e.del && (!trId || e.tr === trId)).sort((a, b) => PRANK[a.st] - PRANK[b.st] || a.o - b.o);
function migrate() {
  if (!Array.isArray(S.port)) S.port = PSEED.map(x => ({ ...x, u: 0 }));''')
rep("pause: null, pauses: [], timer: null,", "port: PSEED.map(x => ({ ...x, u: 0 })), pause: null, pauses: [], timer: null,")
rep('for (const k of ["items", "sessions", "ideas", "proofs", "criteria"])', 'for (const k of ["items", "sessions", "ideas", "proofs", "criteria", "port"])')

# track page card
rep('${eb("proof", "Proof")}<span class="meta num">${pd2} of ${ps.length} in hand</span>', '${eb("proof", "Portfolio")}<span class="meta num">${pd2} of ${ps.length} targets met</span>')
rep_between('    (prods.length ? `<div class="sub-h">${eb("layers", "Products")}</div>`', '    `</div><div class="row" style="margin-top:auto"><button class="btn sm" data-act="view" data-v="proof">Open Proof</button>',
  '''    (port(trId).length ? `<div class="sub-h">${eb("layers", `Entries (${port(trId).length})`)}</div>` + port(trId).slice(0, 5).map(e => `<div class="arow"><span>${esc(e.name)}</span><span class="tag${e.st === "shipped" ? " good" : e.st === "building" ? " sug" : ""}">${PST[e.st]}</span></div>`).join("") : "") +
''')
rep('<button class="btn sm" data-act="view" data-v="proof">Open Proof</button></div></article>`);\n  return head + `<div class="dash tkpage">',
    '<button class="btn sm" data-act="port-tab" data-tr="${trId}">Open the ${esc(tr.name)} portfolio</button></div></article>`);\n  return head + `<div class="dash tkpage">')

VIEW = r'''function portCard(e, L) {
  const ms = e.id === "P01" ? S.items.filter(i => i.prod && i.st !== "removed").sort((a, b) => a.o - b.o) : [];
  const ev = e.ev ? (/^https?:\/\//.test(e.ev) ? `<a href="${esc(e.ev)}" target="_blank" rel="noopener">${esc(e.ev.replace(/^https?:\/\//, ""))}</a>` : esc(e.ev)) : "No evidence yet";
  return `<div class="pcard ${e.st}"><div class="tags"><code>${esc(e.id.startsWith("PF") ? "" : e.id)}</code><span class="tag${e.st === "shipped" ? " good" : e.st === "building" ? " sug" : e.st === "paused" ? " warn" : ""}">${PST[e.st]}${e.st === "shipped" && e.on ? " " + fmtDate(e.on, { day: "numeric", month: "short", year: "numeric" }) : ""}</span><span class="tag">${PMODE[e.mode || ""]}</span></div>
    <h3>${esc(e.name)}</h3>${e.desc ? `<div class="meta">${esc(e.desc)}</div>` : ""}${e.note ? `<div class="note">${esc(e.note)}</div>` : ""}
    ${ms.length ? `<div class="pms">${ms.map(i => `<div class="arow"><span class="${i.st === "done" ? "done-t" : ""}">${esc(i.t)}</span><span class="tag${i.st === "done" ? " good" : ""}">${i.st === "done" ? "Done" : (L[i.id] ? `${hrs(L[i.id])} h so far` : "Not started")}</span></div>`).join("")}</div>` : ""}
    <div class="foot"><span class="ev">${ev}</span><button class="btn sm" data-act="port-edit" data-id="${esc(e.id)}">Edit</button></div></div>`;
}
function portDlg(e, trId) {
  const isNew = !e; trId = e ? e.tr : trId;
  const opt = (o, cur) => Object.entries(o).map(([k, v]) => `<option value="${k}"${k === cur ? " selected" : ""}>${v}</option>`).join("");
  openDlg(`<h2>${isNew ? "Add to the " + esc(track(trId).name) + " portfolio" : "Edit portfolio entry"}</h2>
    <label>Name<input type="text" name="name" id="pe-n" value="${esc(e ? e.name : "")}" required maxlength="120"></label>
    <label>What it is, in one line<input type="text" name="desc" id="pe-d" value="${esc(e ? e.desc : "")}" maxlength="240"></label>
    <div class="grid2"><label>Status<select name="st" id="pe-st">${opt(PST, e ? e.st : "scoped")}</select></label><label>How it is built<select name="mode" id="pe-m">${opt(PMODE, e ? e.mode || "" : "")}</select></label></div>
    <div class="grid2"><label>Evidence: a link or file name<input type="text" name="ev" id="pe-ev" value="${esc(e ? e.ev : "")}" maxlength="300"></label><label>Shipped on<input type="date" name="on" id="pe-on" value="${esc(e ? e.on : "")}"></label></div>
    <label>Note<textarea name="note" id="pe-note">${esc(e ? e.note : "")}</textarea></label>
    <div class="row"><button class="btn pri" type="submit">Save</button><button class="btn" type="button" data-act="dlg-close">Cancel</button>${e ? `<button class="btn quiet danger" type="button" data-act="port-del" data-id="${esc(e.id)}">Remove</button>` : ""}</div>`,
    d => {
      const v = { name: d.name.trim(), desc: (d.desc || "").trim(), st: d.st, mode: d.mode || "", ev: (d.ev || "").trim(), on: d.on || "", note: (d.note || "").trim() };
      if (v.st === "shipped" && !v.on) v.on = todayIso();
      if (isNew) S.port.push(touch({ id: uid("PF"), tr: trId, o: Math.max(0, ...S.port.map(x => x.o || 0)) + 10, ...v })); else touch(Object.assign(e, v));
      save();
    });
}
function viewProof() {
  const cr = S.criteria.filter(c => !c.del), crDone = cr.filter(c => c.done).length, allDone = cr.length && crDone === cr.length;
  const psAll = S.proofs.filter(p => !p.del), L = logged(), all = port(), trs = SEED.tracks.filter(t => !t.recurring);
  let tab = UI.portTab || "home"; if (tab !== "home" && !trs.some(t => t.id === tab)) tab = "home";
  const head = `<div class="today-head">${sketch("proof")}<div class="th-text"><h2>Portfolio</h2><p class="lede num">${all.filter(e => e.st === "shipped").length} shipped and ${all.filter(e => e.st === "building").length} in progress of ${all.length} entries · ${psAll.filter(p => p.done).length} of ${psAll.length} six-month targets met</p></div></div>`;
  const tabs = `<div class="ftabs" role="tablist" aria-label="Portfolios"><button class="ftab" role="tab" data-act="port-tab" data-tr="home" style="--tc:var(--ink)" aria-selected="${tab === "home"}">${ico("home", 16)}Overview</button>` +
    trs.map(t => `<button class="ftab" role="tab" data-act="port-tab" data-tr="${t.id}" style="--tc:var(--c-${t.id})" aria-selected="${t.id === tab}">${ico(t.id, 16)}${esc(t.name)}<span class="meta num">${port(t.id).length}</span></button>`).join("") + `</div>`;
  let body;
  if (tab === "home") {
    const now = all.filter(e => e.st === "building");
    body = `<div class="pv home"><section><div class="sect-h">${eb("today", `In progress (${now.length})`)}</div>` +
      (now.length ? `<div class="pcards">${now.map(e => `<div style="display:contents;--tc:var(--c-${e.tr})">${portCard(e, L)}</div>`).join("")}</div>` : `<div class="empty">Nothing is being built right now. Open a track and set an entry to Building when you start one.</div>`) +
      `<div class="sect-h" style="margin-top:6px">${eb("layers", "By track")}</div><div class="tgrid">` + trs.map(t => {
        const ps = psAll.filter(p => p.tr === t.id), d = ps.filter(p => p.done).length, es = port(t.id), sh = es.filter(e => e.st === "shipped").length;
        return `<button class="tmini" data-act="port-tab" data-tr="${t.id}" style="--tc:var(--c-${t.id})"><span class="tname">${ico(t.id, 18)}${esc(t.name)}</span><span class="big num">${sh}<small>of ${es.length} shipped</small></span><div class="bar"><i style="width:${ps.length ? d / ps.length * 100 : 0}%"></i></div><span class="meta num">${d} of ${ps.length} six-month targets met</span></button>`;
      }).join("") + `</div></section>
      <section><div class="pbox"><div class="card-h">${eb("proof", "Before the startup resumes")}<span class="tag${allDone ? " good" : ""}">${allDone ? "Ready" : "Not yet"}</span></div>
      <div class="big num">${crDone}<small>of ${cr.length} met</small></div><div class="bar"><i style="width:${cr.length ? crDone / cr.length * 100 : 0}%"></i></div>
      ${allDone ? `<div class="banner good"><b>Every criterion is met.</b> Set the date and resume the startup build.</div>` : ""}<div>` +
      cr.map(c => `<div class="prow"><input type="checkbox" id="cc-${c.id}" data-chg="crit-done" data-id="${c.id}"${c.done ? " checked" : ""}><label for="cc-${c.id}" class="${c.done ? "done-t" : ""}"><span>${esc(c.t)}</span><button class="btn sm quiet" type="button" data-act="crit-del" data-id="${c.id}">Remove</button></label></div>`).join("") +
      `</div><form class="inline" data-form="add-crit"><input type="text" name="t" id="nc-t" placeholder="Add a criterion" required maxlength="200" aria-label="New criterion"><button class="btn" type="submit">Add</button></form></div></section></div>`;
  } else {
    const tr = track(tab), ps = psAll.filter(p => p.tr === tab), d = ps.filter(p => p.done).length, es = port(tab);
    const hint = { sw: "an app, a library, a deployed service", str: "a design project, a calculation tool, a drawing set", ai: "a shipped AI feature, an evaluation suite, an agent-built project", ent: "the registered company, a customer conversation write-up, a first sale" }[tab] || "a piece of finished work";
    body = `<div class="pv tr" style="--tc:var(--c-${tab})"><section><div class="sect-h">${eb("proof", "Six-month targets")}<span class="meta num">${d} of ${ps.length} met</span></div><div class="bar"><i style="width:${ps.length ? d / ps.length * 100 : 0}%"></i></div><div>` +
      ps.map(p => `<div class="prow"><input type="checkbox" id="pc-${p.id}" data-chg="proof-done" data-id="${p.id}"${p.done ? " checked" : ""}><label for="pc-${p.id}" class="${p.done ? "done-t" : ""}"><span>${esc(p.t)}</span></label>
        <input type="text" id="pe-${p.id}" data-chg="proof-ev" data-id="${p.id}" value="${esc(p.ev)}" placeholder="Evidence: a link, file name or date" aria-label="Evidence"></div>`).join("") +
      `</div><form class="inline" data-form="add-proof"><input type="hidden" name="tr" value="${tab}"><input type="text" name="t" id="np-t-${tab}" placeholder="Add a target" required maxlength="200" aria-label="New ${esc(tr.name)} target"><button class="btn" type="submit">Add</button></form></section>
      <section><div class="sect-h">${eb("layers", `${esc(tr.name)} portfolio (${es.length})`)}<button class="btn sm" data-act="port-add" data-tr="${tab}">Add an entry</button></div>` +
      (es.length ? `<div class="pcards">${es.map(e => portCard(e, L)).join("")}</div>` : `<div class="empty">Nothing here yet. Add the first piece of work you can show: ${hint}.</div>`) + `</section></div>`;
  }
  return head + tabs + `<div class="folder">${body}</div>`;
}

'''
rep_between("function viewProof() {", "function viewMore() {", VIEW)
rep('  "to-plan"(el) {', '''  "port-tab"(el) { UI.portTab = el.dataset.tr; S.view = "proof"; save(); render(); if (!el.closest(".ftabs")) toTop(); },
  "port-add"(el) { portDlg(null, el.dataset.tr); },
  "port-edit"(el) { portDlg(S.port.find(e => e.id === el.dataset.id)); },
  "port-del"(el) {
    if (UI.armed !== "pdel") { UI.armed = "pdel"; el.textContent = "Confirm: remove this entry"; el.classList.remove("quiet"); setTimeout(() => { if (UI.armed === "pdel") UI.armed = null; }, 6000); return; }
    UI.armed = null; const e = S.port.find(x => x.id === el.dataset.id); if (e) { e.del = 1; touch(e); } save(); closeDlg(); render();
  },
  "to-plan"(el) {''')
open(p, "w", encoding="utf-8").write(s)
print("ok 1.8")
