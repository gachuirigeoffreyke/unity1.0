"""1.6: floating top bar, Ideas and Proof pages. Runs after v6_patch.py."""
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "template.html")
s = open(p, encoding="utf-8").read()
css = open(os.path.join(here, "v7_style.css"), encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)

def rep_between(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i); s = s[:i] + new + s[j:]

rep("</style>", css + "</style>")
rep('const VERSION = "1.5";', 'const VERSION = "1.6";')
rep("  plan: '<circle cx=\"47\"", "  proof: '<circle cx=\"33\" cy=\"27\" r=\"13\" fill=\"#f2c94c\" stroke=\"none\" opacity=\".6\"/><circle cx=\"32\" cy=\"26\" r=\"15\"/><path d=\"M23 39l-5 18 14-7 14 7-5-18\"/><path d=\"M25 26l5 5 9-10\" stroke=\"#22a06b\" stroke-width=\"2.8\"/>',\n  plan: '<circle cx=\"47\"")

VIEWS = r'''function viewIdeas() {
  const now = Date.now(), age = i => Math.floor((now - i.ts) / 864e5), ageTxt = n => n < 1 ? "today" : n + " d ago";
  const parked = S.ideas.filter(i => i.st === "parked").sort((a, b) => b.ts - a.ts);
  const inplan = S.ideas.filter(i => i.st === "promoted" || i.st === "scheduled").sort((a, b) => (b.u || 0) - (a.u || 0));
  const dropped = S.ideas.filter(i => i.st === "dropped").sort((a, b) => (b.u || 0) - (a.u || 0));
  const oldest = parked.length ? Math.max(...parked.map(age)) : 0;
  const head = `<div class="today-head">${sketch("bulb")}<div class="th-text"><h2>Ideas</h2><p class="lede">Every new idea lands here first. It stays safe, and the plan stays intact until you decide.</p></div></div>`;
  const h = [`<article class="card capbar"><form class="inline" data-form="capture"><input type="text" name="text" id="cap-ideas" placeholder="A new idea, in one line" required maxlength="300" aria-label="New idea"><button class="btn pri lg" type="submit">Park it</button></form>
    <div class="hsteps"><span><b class="hn">1</b>Park it the moment it appears</span><span><b class="hn">2</b>Decide at the weekly close</span><span><b class="hn">3</b>Promote only by choosing what gives way</span></div></article>`];
  h.push(`<article class="card id-a"><div class="card-h">${eb("ideas", `Parked (${parked.length})`)}<span class="meta num">${parked.length ? `oldest ${ageTxt(oldest)}` : ""}</span></div>` + (parked.length ?
    `<div class="ilist">` + parked.map(i => `<div class="icard"><div>${esc(i.text)}</div><div class="meta">Parked ${fmtDate(iso(new Date(i.ts)))} · ${ageTxt(age(i))}${age(i) > 7 ? ` <span class="tag warn">Waiting over a week</span>` : ""}</div>
      <div class="row"><button class="btn sm pri" data-act="idea-promote" data-id="${i.id}">Promote</button><button class="btn sm" data-act="idea-schedule" data-id="${i.id}">Schedule</button><button class="btn sm quiet" data-act="idea-drop" data-id="${i.id}">Drop</button></div></div>`).join("") + `</div>
     <div class="meta" style="margin-top:auto">Promote puts it at the top of a queue. Schedule adds it to the end, so nothing current moves.</div>` :
    `<div class="empty">Nothing parked. When something pulls at you mid-session, write it here and carry on.</div>`) + `</article>`);
  h.push(`<article class="card id-b"><div class="card-h">${eb("plan", `In the plan (${inplan.length})`)}</div>` + (inplan.length ? inplan.slice(0, 30).map(i => `<div class="icard q"><div>${esc(i.text)}</div><div class="meta"><span class="tag good">${i.st === "promoted" ? "Promoted" : "Scheduled"}</span>${i.tr ? `<span class="chip" style="--tc:var(--c-${i.tr})">${esc(track(i.tr).name)}</span>` : ""}</div>${i.gave ? `<div class="meta">Gave way: ${esc(i.gave)}</div>` : ""}</div>`).join("") : `<div class="empty">Ideas you promote or schedule show here.</div>`) + `</article>`);
  h.push(`<article class="card id-c"><div class="card-h">${eb("close", `Dropped (${dropped.length})`)}</div>` + (dropped.length ? dropped.slice(0, 30).map(i => `<div class="icard q"><div class="done-t">${esc(i.text)}</div><div class="row"><button class="btn sm quiet" data-act="idea-restore" data-id="${i.id}">Restore</button></div></div>`).join("") : `<div class="empty">Dropping is a decision too. Dropped ideas can be restored from here.</div>`) + `</article>`);
  return head + `<div class="dash idpage">${h.join("")}</div>`;
}

function viewProof() {
  const cr = S.criteria.filter(c => !c.del), crDone = cr.filter(c => c.done).length, allDone = cr.length && crDone === cr.length;
  const psAll = S.proofs.filter(p => !p.del), L = logged();
  const head = `<div class="today-head">${sketch("proof")}<div class="th-text"><h2>Proof</h2><p class="lede num">${psAll.filter(p => p.done).length} of ${psAll.length} proofs in hand. What you can show in six months, and what must be true before the startup resumes.</p></div></div>`;
  const cards = SEED.tracks.filter(t => !t.recurring).map(tr => {
    const ps = psAll.filter(p => p.tr === tr.id), d = ps.filter(p => p.done).length;
    return `<article class="card trk" style="--tc:var(--c-${tr.id})"><div class="card-h" style="align-items:center"><span class="tname">${ico(tr.id, 18)}${esc(tr.name)}</span><span class="meta num">${d} of ${ps.length}</span></div><div class="bar"><i style="width:${ps.length ? d / ps.length * 100 : 0}%"></i></div><div>` +
      ps.map(p => `<div class="prow"><input type="checkbox" id="pc-${p.id}" data-chg="proof-done" data-id="${p.id}"${p.done ? " checked" : ""}><label for="pc-${p.id}" class="${p.done ? "done-t" : ""}"><span>${esc(p.t)}</span></label>
        <input type="text" id="pe-${p.id}" data-chg="proof-ev" data-id="${p.id}" value="${esc(p.ev)}" placeholder="Evidence: a link, file name or date" aria-label="Evidence"></div>`).join("") +
      `</div><form class="inline" data-form="add-proof" style="margin-top:auto"><input type="hidden" name="tr" value="${tr.id}"><input type="text" name="t" id="np-t-${tr.id}" placeholder="Add a proof" required maxlength="200" aria-label="New ${esc(tr.name)} proof"><button class="btn" type="submit">Add</button></form></article>`;
  }).join("");
  const prods = S.items.filter(i => i.prod && i.st !== "removed").sort((a, b) => a.o - b.o);
  const right = `<article class="card"><div class="card-h">${eb("proof", "Before the startup resumes")}<span class="tag${allDone ? " good" : ""}">${allDone ? "Ready" : "Not yet"}</span></div>
      <div class="big num">${crDone}<small>of ${cr.length} met</small></div><div class="bar"><i style="width:${cr.length ? crDone / cr.length * 100 : 0}%"></i></div>
      ${allDone ? `<div class="banner good"><b>Every criterion is met.</b> Set the date and resume the startup build.</div>` : ""}<div>` +
      cr.map(c => `<div class="prow"><input type="checkbox" id="cc-${c.id}" data-chg="crit-done" data-id="${c.id}"${c.done ? " checked" : ""}><label for="cc-${c.id}" class="${c.done ? "done-t" : ""}"><span>${esc(c.t)}</span><button class="btn sm quiet" type="button" data-act="crit-del" data-id="${c.id}">Remove</button></label></div>`).join("") +
      `</div><form class="inline" data-form="add-crit"><input type="text" name="t" id="nc-t" placeholder="Add a criterion" required maxlength="200" aria-label="New criterion"><button class="btn" type="submit">Add</button></form></article>
    <article class="card"><div class="card-h">${eb("layers", "Products")}<span class="meta num">${prods.filter(i => i.st === "done").length} of ${prods.length} finished</span></div>` +
      (prods.length ? prods.map(i => `<div class="arow"><span>${esc(i.t)}</span><span class="tag${i.st === "done" ? " good" : ""}">${i.st === "done" ? "Finished · built with AI" : (L[i.id] ? `${hrs(L[i.id])} h so far` : "Not started")}</span></div>`).join("") : `<div class="empty">Finished products appear here.</div>`) + `</article>`;
  return head + `<div class="dash prpage"><div class="pr-a pgrid">${cards}</div><div class="pr-b">${right}</div></div>`;
}

'''
rep_between("function viewIdeas() {", "function viewMore() {", VIEWS)
open(p, "w", encoding="utf-8").write(s)
print("v7 patched", len(s))
