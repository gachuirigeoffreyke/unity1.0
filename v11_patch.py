"""2.1: Library gets an overview tab, a tab per track, and nested stages > volumes > lessons. Runs after v10_patch.py."""
import os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "template.html")
s = open(p, encoding="utf-8").read()
css = open(os.path.join(here, "v11_style.css"), encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
def rep_between(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i); s = s[:i] + new + s[j:]
rep("</style>", css + "</style>")
rep('const VERSION = "2.0";', 'const VERSION = "2.1";')

VIEW = r'''function volStats(v) {
  const ms = v.secs.map((x, k) => ({ x, k, i: x.it && item(x.it) })).filter(o => o.x.mod);
  const done = ms.filter(o => o.i && o.i.st === "done").length, nxt = ms.find(o => o.i && o.i.st === "open"), pos = (S.readPos || {})[v.id];
  const first = ms.find(o => o.i);
  return { ms, done, nxt, pos, go: pos != null ? pos : (nxt ? nxt.k : 0), stage: first ? stageOf(first.i)[0] : "Other volumes", o: first ? first.i.o : 1e9 };
}
function libOpen(key, dflt) { UI.libSet = UI.libSet || {}; return key in UI.libSet ? UI.libSet[key] : dflt; }
function viewLibrary() {
  const L = logged(), trs = SEED.tracks.filter(t => !t.recurring), all = VOLS.map(v => ({ v, s: volStats(v) }));
  let tab = UI.libTab || "home"; if (tab !== "home" && !trs.some(t => t.id === tab)) tab = "home";
  const mods = all.reduce((a, o) => a + o.s.ms.length, 0);
  const head = `<div class="today-head">${sketch("read")}<div class="th-text"><h2>Library</h2><p class="lede num">${volsReady ? `${VOLS.length} volume${VOLS.length === 1 ? "" : "s"} · ${mods} lessons. Open one to read; the reading timer logs the time to its item.` : "Loading the volumes…"}</p></div></div>`;
  const tabs = `<div class="ftabs" role="tablist" aria-label="Library"><button class="ftab" role="tab" data-act="lib-tab" data-tr="home" style="--tc:var(--ink)" aria-selected="${tab === "home"}">${ico("home", 16)}Overview</button>` +
    trs.map(t => `<button class="ftab" role="tab" data-act="lib-tab" data-tr="${t.id}" style="--tc:var(--c-${t.id})" aria-selected="${t.id === tab}">${ico(t.id, 16)}${esc(t.name)}<span class="meta num">${all.filter(o => o.v.tr === t.id).length}</span></button>`).join("") + `</div>`;
  let body;
  if (tab === "home") {
    const lr = readPos(), r = S.rt, ri = r && item(r.it);
    const nexts = trs.map(t => { const it = nextItem(t.id); return it && LMAP[it.id] ? { t, it } : null; }).filter(Boolean);
    body = `<div class="lv home"><section><div class="pbox"><div class="card-h">${eb("read", "Continue reading")}</div>` + (lr ? `<h3>${esc(lr.v.secs[lr.k].t)}</h3><div class="meta">${esc(lr.v.title)}</div>` +
        (r ? `<div class="note">Reading time not yet logged: ${Math.round(rtMs() / 60000)} min${ri ? " on " + esc(ri.id) : ""}.</div>` : "") +
        `<div class="row"><button class="btn pri" data-act="read-open" data-vol="${esc(lr.v.id)}" data-s="${lr.k}">Back to the lesson</button>${r ? `<button class="btn" data-act="rt-log">Log it now</button>` : ""}</div>` : `<div class="empty">Nothing opened yet. Pick a track tab, or start with a next-up lesson below.</div>`) + `</div>` +
      (nexts.length ? `<div class="sect-h">${eb("today", "Next-up lessons")}</div><div>` + nexts.map(o => `<button class="vmod" data-act="read-item" data-it="${esc(o.it.id)}" style="--tc:var(--c-${o.t.id})"><span class="chip">${ico(o.t.id, 15)}</span><span class="t clamp1">${esc(o.it.t)}</span><span class="meta num">${esc(o.it.id)}</span></button>`).join("") + `</div>` : "") +
      `<div class="sect-h" style="margin-top:6px">${eb("layers", "By track")}</div><div class="tgrid">` + trs.map(t => {
        const vs = all.filter(o => o.v.tr === t.id), n = vs.reduce((a, o) => a + o.s.ms.length, 0), d = vs.reduce((a, o) => a + o.s.done, 0);
        const open = S.items.filter(i => i.tr === t.id && i.st === "open" && !i.prod), miss = open.filter(i => !LMAP[i.id]).length;
        return `<button class="tmini" data-act="lib-tab" data-tr="${t.id}" style="--tc:var(--c-${t.id})"><span class="tname">${ico(t.id, 18)}${esc(t.name)}</span><span class="big num">${vs.length}<small>volume${vs.length === 1 ? "" : "s"} · ${n} lessons</small></span><div class="bar"><i style="width:${n ? d / n * 100 : 0}%"></i></div><span class="meta num">${d} of ${n} lessons done</span><span class="meta num">${miss} of ${open.length} open items still need a lesson</span></button>`;
      }).join("") + `</div></section>
      <section><div class="pbox"><div class="card-h">${eb("backup", "Add a volume")}</div><p class="lede">When a new volume is written, add its <code>.md</code> file here. It files itself under the right track and stage. It stays on this device, so add it on the phone too.</p>
        <label>Volume files<input type="file" id="vol-file" accept=".md,.markdown,.txt,text/markdown,text/plain" multiple></label><div class="row"><button class="btn" data-act="vol-import">Add to the library</button></div></div></section></div>`;
  } else {
    const vs = all.filter(o => o.v.tr === tab).sort((a, b) => a.s.o - b.s.o || a.v.name.localeCompare(b.v.name)), nx = nextItem(tab), nxV = nx && LMAP[nx.id] ? LMAP[nx.id].v : null;
    const stages = []; for (const o of vs) { let g = stages.find(x => x.name === o.s.stage); if (!g) stages.push(g = { name: o.s.stage, vols: [] }); g.vols.push(o); }
    const curStage = (stages.find(g => g.vols.some(o => o.v.id === nxV)) || stages[0] || {}).name;
    body = `<div class="lv" style="--tc:var(--c-${tab})"><section><div class="sect-h">${eb("layers", `${esc(track(tab).name)} volumes (${vs.length})`)}<span class="meta num">${vs.reduce((a, o) => a + o.s.done, 0)} of ${vs.reduce((a, o) => a + o.s.ms.length, 0)} lessons done</span></div>` +
      (stages.length ? stages.map(g => {
        const sk = "s|" + tab + "|" + g.name, n = g.vols.reduce((a, o) => a + o.s.ms.length, 0), d = g.vols.reduce((a, o) => a + o.s.done, 0);
        return `<details class="lstage${g.name === curStage ? " cur" : ""}" data-lib="${esc(sk)}"${libOpen(sk, g.name === curStage) ? " open" : ""}><summary><i class="chev"></i><span>${esc(g.name)}</span><span class="meta num">${g.vols.length} volume${g.vols.length === 1 ? "" : "s"} · ${d}/${n} lessons</span></summary><div class="lvols">` +
          g.vols.map(({ v, s: st }) => { const vk = "v|" + v.id; return `<details class="lvol" data-lib="${esc(vk)}"${libOpen(vk, v.id === nxV) ? " open" : ""}><summary><i class="chev"></i><span class="vt"><b>${esc(v.title)}</b><div class="bar"><i style="width:${st.ms.length ? st.done / st.ms.length * 100 : 0}%"></i></div></span><span class="meta num">${st.done}/${st.ms.length} lessons${v.shipped ? "" : " · imported"}</span></summary>
            <div class="vbody"><div class="vmods">${st.ms.map(o => `<button class="vmod${o.i && o.i.st === "done" ? " done" : ""}" data-act="read-open" data-vol="${esc(v.id)}" data-s="${o.k}"><code>${esc(o.x.mod)}</code><span class="t clamp1">${esc(o.x.t)}</span><span class="meta num">${o.i && nx && o.i.id === nx.id ? `<span class="tag sug">Next</span> ` : ""}${o.i && L[o.i.id] ? hrs(L[o.i.id]) + " h" : ""}</span></button>`).join("")}</div>
            <div class="row"><button class="btn sm pri" data-act="read-open" data-vol="${esc(v.id)}" data-s="${st.go}">${st.pos != null ? "Continue" : "Open"}</button><button class="btn sm quiet" data-act="read-open" data-vol="${esc(v.id)}" data-s="0">From the start</button><span class="meta num">${v.secs.length} sections in all</span>${v.shipped ? "" : `<button class="btn sm quiet danger" data-act="vol-del" data-id="${esc(v.id)}">${UI.armed === "vol" + v.id ? "Confirm: remove" : "Remove"}</button>`}</div></div></details>`; }).join("") + `</div></details>`;
      }).join("") : `<div class="empty">${volsReady ? `No ${esc(track(tab).name)} volumes yet. Ask Claude for the first one, then add its file on the Overview tab.` : "Loading…"}</div>`) + `</section></div>`;
  }
  return head + tabs + `<div class="folder">${body}</div>`;
}
'''
rep_between("function viewLibrary() {", "function viewRead() {", VIEW)
rep('  "read-item"(el) {', '''  "lib-tab"(el) { UI.libTab = el.dataset.tr; S.view = "library"; save(); render(); },
  "read-item"(el) {''')
rep('''document.addEventListener("toggle", e => { if (e.target.classList && e.target.classList.contains("rd-toc")) UI.tocOpen = e.target.open; }, true);''',
    '''document.addEventListener("toggle", e => { const t = e.target; if (!t.classList) return; if (t.classList.contains("rd-toc")) UI.tocOpen = t.open; if (t.dataset && t.dataset.lib) { UI.libSet = UI.libSet || {}; UI.libSet[t.dataset.lib] = t.open; } }, true);''')
# after an import, land on that volume's track tab
rep('''await loadVols(); toast(`${n} volume${n === 1 ? "" : "s"} added`);''', '''await loadVols(); const nv = vol(fs[fs.length - 1].name); if (nv) { UI.libTab = nv.tr; UI.libSet = UI.libSet || {}; UI.libSet["v|" + nv.id] = true; UI.libSet["s|" + nv.tr + "|" + volStats(nv).stage] = true; render(); } toast(`${n} volume${n === 1 ? "" : "s"} added`);''')
open(p, "w", encoding="utf-8").write(s)
print("ok 2.1")
