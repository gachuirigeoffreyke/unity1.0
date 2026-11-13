import json, sys
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome", args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":390,"height":844}, accept_downloads=True)
    pg=ctx.new_page()
    pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.on("pageerror", lambda e: errs.append("PAGEERR "+str(e)))
    pg.goto("http://localhost:8765/"); pg.wait_for_selector("article.card")
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
    pg.click("#nav [data-v=ideas]"); pg.click("[data-act=idea-promote]"); pg.select_option("#id-tr","str")
    opts=pg.locator("#id-gave option").all_inner_texts(); print("give-way options:", opts[:3])
    pg.select_option("#id-gave", index=2); pg.click("#dform button[type=submit]")
    s=st(); print("idea:", s["ideas"][0]["st"], "| gave:", s["ideas"][0].get("gave","")[:50], "| str next:", pg.evaluate("nextItem('str').t")[:40], "| set aside:", [i["id"] for i in s["items"] if i["st"]=="later"])
    # off plan -> park
    pg.click("#nav [data-v=today]"); pg.click("[data-act=off-plan]"); pg.fill("#op-l","Watch a Rust tutorial"); pg.click("#dform button[value=park]")
    print("ideas after park:", len(st()["ideas"]), "timer:", st()["timer"])
    pg.click("[data-act=off-plan]"); pg.fill("#op-l","Fix laptop audio"); pg.click("#dform button[value=start]"); pg.wait_for_selector("#clock")
    pg.click("[data-act=stop]"); pg.fill("#f-m","70"); pg.click("#dform button[type=submit]")
    print("nudges:", [t[:60] for t in pg.locator(".banner.warn").all_inner_texts()])
    # plan
    pg.click("#nav [data-v=plan]"); pg.wait_for_selector("details.grp")
    print("open groups:", pg.locator("details.grp[open]").count(), "items visible:", pg.locator("details.item").count())
    pg.locator("details.item summary").nth(1).click(); pg.wait_for_selector("details.item[open] .acts")
    before=pg.evaluate("openItems('sw').slice(0,3).map(i=>i.id)")
    pg.click("details.item[open] [data-act=item-top]"); after=pg.evaluate("openItems('sw').slice(0,3).map(i=>i.id)"); print("do-next:", before, "->", after)
    pg.locator("details.grp summary").nth(2).click(); pg.wait_for_timeout(200); print("open groups after click:", pg.locator("details.grp[open]").count())
    pg.click("[data-act=add-item]"); pg.fill("#ei-t","Read Clean Architecture ch. 1-5"); pg.select_option("#ei-pos","top"); pg.click("#dform button[type=submit]")
    print("sw next:", pg.evaluate("nextItem('sw').t"))
    pg.click("[data-act=plan-track][data-tr=str]"); pg.wait_for_timeout(150); pg.screenshot(path="/tmp/plan-m.png", full_page=False)
    # week
    pg.click("#nav [data-v=week]"); pg.fill("#wk-note","Mornings worked."); pg.click("form[data-form=close-week] button[type=submit]")
    print("week closed:", pg.locator(".tag.good").count(), "| rows:", pg.locator(".srow").count())
    pg.screenshot(path="/tmp/week-m.png", full_page=True)
    # pause
    pg.click("#nav [data-v=more]"); pg.fill("#pz-r","Site job"); pg.click("form[data-form=pause] button[type=submit]")
    pg.click("#nav [data-v=today]"); print("pause banner:", pg.locator(".banner").first.inner_text()[:60].replace("\n"," "), "| goal:", pg.evaluate("weekPlan(monday(todayIso())).goal"))
    pg.click("[data-act=end-pause]"); print("pause ended:", st()["pause"], "| future week goals:", pg.evaluate("[0,1,2,3].map(i=>weekPlan(addDays(S.settings.start,7*i)).goal)"), pg.evaluate("Object.values(weekPlan(S.settings.start).per).map(x=>Math.round(x*100)/100)"))
    # export / import
    pg.click("#nav [data-v=more]")
    with pg.expect_download() as d: pg.click("[data-act=export]")
    path=d.value.path(); bk=json.load(open(path)); print("backup:", bk["format"], len(bk["sessions"]), "sessions")
    pg.set_input_files("#imp-file", path); pg.click("[data-act=import][data-mode=merge]"); pg.wait_for_timeout(300); print("after merge sessions:", len(st()["sessions"]))
    with pg.expect_download() as d: pg.click("[data-act=export-csv]")
    print(open(d.value.path()).read().splitlines()[:2])
    # proof
    pg.click("#nav [data-v=proof]"); pg.locator("[data-chg=proof-done]").first.check(); print("proof done:", sum(x["done"] for x in st()["proofs"]))
    # offline + persistence
    pg.wait_for_timeout(800); print("sw controller:", pg.evaluate("!!navigator.serviceWorker.controller || navigator.serviceWorker.ready.then(()=>true)"))
    pg.reload(); pg.wait_for_selector("#main h2"); ctx.set_offline(True); pg.reload(); pg.wait_for_selector("#main h2")
    print("offline reload ok; sessions:", len(st()["sessions"]), "| storage:", pg.evaluate("DB.mode"))
    ctx.set_offline(False)
    pg.click("#nav [data-v=today]"); pg.screenshot(path="/tmp/today-m2.png", full_page=True)
    pg.set_viewport_size({"width":1280,"height":820}); pg.screenshot(path="/tmp/today-d.png")
    pg.click("#nav [data-v=plan]"); pg.click("[data-act=plan-track][data-tr=sw]"); pg.wait_for_timeout(150); pg.screenshot(path="/tmp/plan-d.png")
    print("ERRORS:", errs)
    b.close()
