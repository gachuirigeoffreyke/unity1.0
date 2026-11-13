import json, sys
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome", args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":390,"height":844}, accept_downloads=True)
    pg=ctx.new_page()
    pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.on("pageerror", lambda e: errs.append("PAGEERR "+str(e)))
    pg.goto("http://localhost:8765/"); pg.wait_for_selector("article.card"); print("home hero:", pg.locator(".hero h1").inner_text()[:50], "| tcards", pg.locator(".tmini").count()); pg.click("#bnav [data-v=today]"); pg.wait_for_selector(".cols article.card")
    st=lambda: pg.evaluate("JSON.parse(JSON.stringify(S))")
    print("cards", pg.locator("article.card").count(), "| start", st()["settings"]["start"], "| top:", pg.locator("#topmeta").inner_text())
    print("first card:", pg.locator("article.card h3").first.inner_text()[:70])
    pg.screenshot(path="/tmp/today-m.png", full_page=True)
    # session
    pg.locator("article.card [data-act=start]").first.click(); pg.wait_for_timeout(1300)
    print("clock", pg.locator("#clock").inner_text(), "| title", pg.title())
    pg.reload(); pg.wait_for_selector("#clock"); print("timer survives reload:", pg.locator("#clock").inner_text())
    pg.click("[data-act=stop]"); pg.fill("#f-m","50"); pg.check("#f-fin"); pg.fill("#f-next","n/a"); pg.select_option("#f-mode","1"); pg.click("#dform button[type=submit]")
    s=st(); print("sessions", len(s["sessions"]), s["sessions"][0]["m"], s["sessions"][0]["it"], "done:", [i["id"] for i in s["items"] if i["st"]=="done"])
    print("new first card:", pg.locator("article.card h3").first.inner_text()[:70])
    # second session unfinished w/ next note
    pg.locator("article.card [data-act=start]").nth(1).click(); pg.click("[data-act=stop]"); pg.fill("#f-m","90"); pg.fill("#f-next","Resume at worked problem 2"); pg.click("#dform button[type=submit]")
    print("pick-up notes shown:", pg.locator(".note").all_inner_texts()[:3])
    # idea capture + promote
    pg.fill("#cap-today","Build a rebar schedule generator"); pg.click("form[data-form=capture] button")
    pg.click("#bnav [data-v=ideas]"); pg.click("[data-act=idea-promote]"); pg.select_option("#id-tr","str")
    opts=pg.locator("#id-gave option").all_inner_texts(); print("give-way options:", opts[:3])
    pg.select_option("#id-gave", index=2); pg.click("#dform button[type=submit]")
    s=st(); print("idea:", s["ideas"][0]["st"], "| gave:", s["ideas"][0].get("gave","")[:50], "| str next:", pg.evaluate("nextItem('str').t")[:40], "| set aside:", [i["id"] for i in s["items"] if i["st"]=="later"])
    # off plan -> park
    pg.click("#bnav [data-v=today]"); pg.click("[data-act=off-plan]"); pg.fill("#op-l","Watch a Rust tutorial"); pg.click("#dform button[value=park]")
    print("ideas after park:", len(st()["ideas"]), "timer:", st()["timer"])
    pg.click("[data-act=off-plan]"); pg.fill("#op-l","Fix laptop audio"); pg.click("#dform button[value=start]"); pg.wait_for_selector("#clock")
    pg.click("[data-act=stop]"); pg.fill("#f-m","70"); pg.click("#dform button[type=submit]")
    print("nudges:", [t[:60] for t in pg.locator(".banner.warn").all_inner_texts()])
    # plan
    pg.click("#bnav [data-v=plan]"); pg.wait_for_selector("details.grp")
    print("open groups:", pg.locator("details.grp[open]").count(), "items visible:", pg.locator("details.item").count())
    pg.locator("details.item summary").nth(1).click(); pg.wait_for_selector("details.item[open] .acts")
    before=pg.evaluate("openItems('sw').slice(0,3).map(i=>i.id)")
    pg.click("details.item[open] [data-act=item-top]"); after=pg.evaluate("openItems('sw').slice(0,3).map(i=>i.id)"); print("do-next:", before, "->", after)
    pg.locator("details.grp summary").nth(2).click(); pg.wait_for_timeout(200); print("open groups after click:", pg.locator("details.grp[open]").count())
    pg.click("[data-act=add-item]"); pg.fill("#ei-t","Read Clean Architecture ch. 1-5"); pg.select_option("#ei-pos","top"); pg.click("#dform button[type=submit]")
    print("sw next:", pg.evaluate("nextItem('sw').t"))
    pg.click("[data-act=plan-track][data-tr=str]"); pg.wait_for_timeout(150); pg.screenshot(path="/tmp/plan-m.png", full_page=False)
    # week
    pg.click("#bnav [data-v=week]"); pg.fill("#wk-note","Mornings worked."); pg.click("form[data-form=close-week] button[type=submit]")
    print("week closed:", pg.locator(".tag.good").count(), "| rows:", pg.locator(".srow").count())
    pg.screenshot(path="/tmp/week-m.png", full_page=True)
    # pause
    pg.click(".ibtn[data-v=more]"); pg.fill("#pz-r","Site job"); pg.click("form[data-form=pause] button[type=submit]")
    pg.click("#bnav [data-v=today]"); print("pause banner:", pg.locator(".banner").first.inner_text()[:60].replace("\n"," "), "| goal:", pg.evaluate("weekPlan(monday(todayIso())).goal"))
    pg.click("[data-act=end-pause]"); print("pause ended:", st()["pause"], "| future week goals:", pg.evaluate("[0,1,2,3].map(i=>weekPlan(addDays(S.settings.start,7*i)).goal)"), pg.evaluate("Object.values(weekPlan(S.settings.start).per).map(x=>Math.round(x*100)/100)"))
    # export / import
    pg.click(".ibtn[data-v=more]")
    with pg.expect_download() as d: pg.click("[data-act=export]")
    path=d.value.path(); bk=json.load(open(path)); print("backup:", bk["format"], len(bk["sessions"]), "sessions")
    pg.set_input_files("#imp-file", path); pg.click("[data-act=import][data-mode=merge]"); pg.wait_for_timeout(300); print("after merge sessions:", len(st()["sessions"]))
    with pg.expect_download() as d: pg.click("[data-act=export-csv]")
    print(open(d.value.path()).read().splitlines()[:2])
    # proof
    pg.evaluate("S.view=\"proof\";render()"); pg.locator("[data-chg=proof-done]").first.check(); print("proof done:", sum(x["done"] for x in st()["proofs"]))
    # offline + persistence
    pg.wait_for_timeout(800); print("sw controller:", pg.evaluate("!!navigator.serviceWorker.controller || navigator.serviceWorker.ready.then(()=>true)"))
    pg.reload(); pg.wait_for_selector("#main h2"); ctx.set_offline(True); pg.reload(); pg.wait_for_selector("#main h2")
    print("offline reload ok; sessions:", len(st()["sessions"]), "| storage:", pg.evaluate("DB.mode"))
    ctx.set_offline(False)
    pg.click("#bnav [data-v=today]"); pg.screenshot(path="/tmp/today-m2.png", full_page=True)
    pg.set_viewport_size({"width":1280,"height":820}); pg.screenshot(path="/tmp/today-d.png")
    pg.click("#nav [data-v=plan]"); pg.click("[data-act=plan-track][data-tr=sw]"); pg.wait_for_timeout(150); pg.screenshot(path="/tmp/plan-d.png")
    print("ERRORS:", errs)
    b.close()

with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome", args=["--no-sandbox"]); errs=[]
    for scheme in ("dark","light"):
        ctx=b.new_context(viewport={"width":1920,"height":1050}, color_scheme=scheme); pg=ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        pg.goto("http://localhost:8765/"); pg.wait_for_selector(".dash")
        pg.evaluate("""(()=>{const t=todayIso();const mk=(d,m,tr,it)=>S.sessions.push({id:uid('S'),d,ts:parse(d).getTime()+4e7,m,tr,it,label:'',mode:1,note:'',off:false,u:Date.now()});
          [[0,95,'sw','FSE.C01.M01'],[0,60,'str','STR.SETUP'],[1,150,'sw','FSE.C01.M02'],[2,45,'ai','AI.F01'],[3,200,'sw','FSE.C01.M02'],[5,30,'ent','ENT.01'],[6,120,'str','STR.SETUP'],[8,240,'sw','FSE.C01.M03'],[9,320,'str','STR.V01.M01'],[12,80,'ai','AI.F01'],[15,60,'sw','FSE.C02.M01']].forEach(a=>mk(addDays(t,-a[0]),a[1],a[2],a[3]));
          item('FSE.C01.M01').st='done'; S.ideas.push({id:uid('I'),ts:Date.now(),text:'Rebar schedule generator',st:'parked',u:1}); render();})()""")
        pg.wait_for_timeout(400); pg.screenshot(path=f"/tmp/home-{scheme}.png")
        if scheme=="light":
            pg.click("#nav [data-v=today]"); pg.wait_for_timeout(300); pg.screenshot(path="/tmp/today-light.png"); pg.click("#nav [data-v=week]"); pg.wait_for_timeout(300); pg.screenshot(path="/tmp/week-light.png"); pg.click("#nav [data-v=plan]"); pg.wait_for_timeout(300); pg.screenshot(path="/tmp/plan-light.png"); pg.click("[data-act=plan-view][data-v=road]"); pg.wait_for_timeout(200); pg.screenshot(path="/tmp/plan-road.png", clip={"x":80,"y":80,"width":1830,"height":420})
        if scheme=="dark":
            pg.hover("#rail .ritem"); pg.wait_for_timeout(600); pg.screenshot(path="/tmp/rail-hover.png"); pg.mouse.move(900,600); pg.wait_for_timeout(400); pg.click("[data-act=attn]"); pg.wait_for_timeout(350); pg.screenshot(path="/tmp/attn.png"); pg.click("#attn [data-act=attn]")
            pg.click("#rail [data-tr=str]"); pg.wait_for_timeout(400); print("rail width after click:", pg.evaluate("document.querySelector(\"#rail\").offsetWidth")); pg.screenshot(path="/tmp/track-dark.png")
            pg.click("#nav [data-v=today]"); pg.wait_for_timeout(300); pg.screenshot(path="/tmp/today-dark.png"); print("tracks:", pg.evaluate("SEED.tracks.map(t=>t.id).join()"), "| chama items:", pg.evaluate("S.items.filter(i=>i.prod).map(i=>i.tr+\":\"+i.g).join()"))
            pg.click("#nav [data-v=week]"); pg.wait_for_timeout(300); pg.screenshot(path="/tmp/week-dark.png"); pg.click("[data-act=wk-nav][data-dir=\"1\"]"); pg.wait_for_timeout(200); print("earlier week:", pg.locator(".th-text h2").inner_text(), "| sessions", pg.locator(".srow").count()); pg.click("[data-act=wk-nav][data-dir=\"0\"]"); pg.click("#nav [data-v=plan]"); pg.wait_for_timeout(300); pg.click("[data-act=plan-track][data-tr=str]"); pg.click("[data-act=plan-view][data-v=outline]"); pg.wait_for_timeout(200); pg.screenshot(path="/tmp/plan-dark.png"); n0=pg.locator(".col.shut").count(); pg.locator("[data-act=col-toggle]").nth(1).click(); pg.wait_for_timeout(150); print("cols", pg.locator(".col").count(), "shut", n0, "->", pg.locator(".col.shut").count(), "| outline lines", pg.locator("pre.md").inner_text().count(chr(10))); pg.click("[data-act=theme]"); print("theme ->", pg.evaluate("S.settings.theme"), pg.evaluate("document.documentElement.dataset.theme"))
            pg.click("[data-act=quick-idea]"); pg.fill("#qi-t","Quick idea"); pg.click("#dform button[type=submit]"); print("ideas:", pg.evaluate("S.ideas.length"))
        ctx.close()
    ctx=b.new_context(viewport={"width":390,"height":800}, color_scheme="dark"); pg=ctx.new_page(); pg.goto("http://localhost:8765/"); pg.wait_for_selector(".dash"); pg.click("#bnav [data-v=plan]"); pg.wait_for_timeout(300); pg.screenshot(path="/tmp/plan-phone.png", full_page=True)
    print("V2 ERRORS:", errs); b.close()

