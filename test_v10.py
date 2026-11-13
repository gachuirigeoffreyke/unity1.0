from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome", args=["--no-sandbox"])
    for w,h in ((1366,768),(390,844)):
        ctx=b.new_context(viewport={"width":w,"height":h}); pg=ctx.new_page()
        pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None); pg.on("pageerror", lambda e: errs.append("PAGEERR "+str(e)))
        pg.goto("http://localhost:8765/"); pg.wait_for_selector(".dash"); pg.wait_for_function("volsReady")
        print(w, "vols:", pg.evaluate("VOLS.map(v=>v.title.slice(0,18)+':'+v.secs.filter(x=>x.it).length+'/'+v.secs.length+':'+v.tr)"), "| lessons mapped:", pg.evaluate("Object.keys(LMAP).length"))
        pg.evaluate("S.view='library';render()"); print("  library tabs:", pg.locator(".ftab").count(), "| tiles", pg.locator(".lv .tmini").count()); pg.click(".tmini[data-tr=sw]"); print("  sw stages:", pg.locator(".lstage").count(), "open:", pg.locator(".lstage[open]").count(), "| vols:", pg.locator(".lvol").count(), "open:", pg.locator(".lvol[open]").count()); pg.locator(".lvol:not([open]) > summary").first.click(); pg.wait_for_timeout(100); pg.evaluate("render()"); print("  toggle survives render:", pg.locator(".lvol[open]").count())
        pg.evaluate("S.view='home';render()"); print("  home read btn:", pg.locator(".hero [data-act=read-item]").count())
        pg.evaluate("S.planTrack='sw';S.view='track';render()"); pg.click(".tk-a [data-act=read-item]"); pg.wait_for_selector("#lesson h2")
        print("  lesson:", pg.locator("#lesson h2").first.inner_text()[:50], "| tables", pg.locator("#lesson table").count(), "| code", pg.locator("#lesson pre").count(), "| timer:", pg.locator("#rtlbl").inner_text(), pg.evaluate("S.rt.it"))
        # simulate 3 minutes of reading, leave, come back, close
        pg.evaluate("S.rt.start-=180000"); pg.evaluate("S.view='today';render()"); print("  left -> paused:", pg.evaluate("S.rt.start===null && S.rt.why"), round(pg.evaluate("S.rt.acc")/60000,1), "min | pill:", pg.locator("#topmeta .pill").count())
        pg.evaluate("ACT['read-item']({dataset:{it:S.rt.it}})"); pg.wait_for_selector("#rtbox"); print("  back -> running:", pg.evaluate("!!S.rt.start"))
        pg.click("[data-act=rt-toggle]"); print("  manual pause:", pg.locator("#rtlbl").inner_text(), pg.locator("#rttog").inner_text()); pg.click("[data-act=read-nav][data-dir='1']"); pg.wait_for_timeout(300); print("  next section, still paused by me:", pg.evaluate("S.rt && S.rt.start===null"), "|", pg.locator("#lesson h2").first.inner_text()[:40])
        n0=pg.evaluate("live().length"); pg.locator("[data-act=read-close]").first.click(); s=pg.evaluate("live().slice(-1)[0]"); print("  closed:", pg.evaluate("live().length")-n0, "session(s)", s["m"], s["it"], s["note"], "| view", pg.evaluate("S.view"), "| rt", pg.evaluate("S.rt"))
        # short read is not logged
        pg.evaluate("UI.libTab='home';S.view='library';render()"); pg.locator(".vmod").first.click(); pg.wait_for_selector("#lesson h2"); n1=pg.evaluate("live().length"); pg.locator("[data-act=read-close]").first.click(); print("  short read logged:", pg.evaluate("live().length")-n1, "| toast:", pg.locator("#toast").inner_text())
        # idle pause
        pg.evaluate("openLesson('FSE-C02a-Python.md',4)"); pg.wait_for_selector("#rtbox"); pg.evaluate("lastAct-=6*60000; S.rt.start-=7*60000; rtTick()"); print("  idle:", pg.evaluate("S.rt.why"), round(pg.evaluate("S.rt.acc")/60000,1), "|", pg.locator("#rtlbl").inner_text())
        pg.mouse.wheel(0,200); pg.wait_for_timeout(200); print("  activity resumes:", pg.evaluate("!!S.rt.start"))
        # session start closes reading
        pg.evaluate("S.rt.acc+=5*60000"); pg.evaluate("S.view='today';render()"); n2=pg.evaluate("live().length"); pg.locator("#main [data-act=start]").first.click(); print("  start session logs reading:", pg.evaluate("live().length")-n2, "| rt", pg.evaluate("S.rt")); pg.locator("#main [data-act=stop]").first.click(); pg.click("[data-act=discard-timer]"); pg.click("[data-act=discard-timer]")
        # maths
        pg.evaluate("openLesson('STR-V01-Mechanics-Maths.md', VOLS.find(v=>v.id.startsWith('STR')).secs.findIndex(x=>x.mod==='V01.M01'))"); pg.wait_for_selector("#lesson math"); print("  maths:", pg.locator("#lesson math").count(), "| leftover $:", pg.locator("#lesson").inner_text().count("$"), "| details", pg.locator("#lesson details").count())
        pg.screenshot(path=f"/tmp/read-str-{w}.png")
        # import
        open("/tmp/FSE-C03a-Test.md","w").write("# FSE-C03a · Data and SQL, Part A\n\nIntro text.\n\n## [C03.M01] Relational model\n\nBody with `code` and a table.\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n## Answer key\n\nKeys.\n")
        pg.evaluate("UI.libTab='home';S.view='library';render()"); pg.set_input_files("#vol-file","/tmp/FSE-C03a-Test.md"); pg.click("[data-act=vol-import]"); pg.wait_for_function("VOLS.length===5"); it=pg.evaluate("VOLS.find(v=>v.id.includes('C03')).secs.map(x=>x.it||'-')"); print("  imported:", it, "| c flag:", pg.evaluate("(item('FSE.C03.M01')||{}).c"))
        print("  landed on tab:", pg.evaluate("UI.libTab"), "| imported vol open:", pg.locator(".lvol[open] [data-act=vol-del]").count()); pg.reload(); pg.wait_for_function("volsReady"); print("  survives reload:", pg.evaluate("VOLS.length")); pg.evaluate("UI.libTab='sw';UI.libSet={};VOLS.forEach(v=>{UI.libSet['v|'+v.id]=true;UI.libSet['s|sw|'+volStats(v).stage]=true});S.view='library';render()"); pg.click("[data-act=vol-del]"); pg.click("[data-act=vol-del]"); pg.wait_for_function("VOLS.length===4"); print("  removed ok")
        # offline
        pg.wait_for_timeout(1500); ctx.set_offline(True); pg.reload(); pg.wait_for_function("volsReady"); pg.evaluate("openLesson(VOLS[1].id,2)"); pg.wait_for_selector("#lesson h2"); print("  offline lesson ok:", pg.evaluate("VOLS.length"), pg.locator("#lesson table").count()); ctx.set_offline(False)
        for v in ("library","read"):
            pg.evaluate(f"S.view='{v}';render()"); pg.wait_for_timeout(200)
            print("  overflow", v, pg.evaluate("(()=>{const m=document.querySelector('%s');return m.scrollWidth-m.clientWidth})()" % ("#inner" if w>899 else "html")))
        ctx.close()
    b.close()
print("ERRORS:", errs)
