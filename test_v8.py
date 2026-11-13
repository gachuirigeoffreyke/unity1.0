from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome", args=["--no-sandbox"])
    for w,h in ((1366,768),(390,844)):
        ctx=b.new_context(viewport={"width":w,"height":h}); pg=ctx.new_page()
        pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None); pg.on("pageerror", lambda e: errs.append("PAGEERR "+str(e)))
        pg.goto("http://localhost:8765/"); pg.wait_for_selector(".dash")
        st=lambda: pg.evaluate("JSON.parse(JSON.stringify(S))")
        # start on a track page, then discard
        pg.evaluate("S.planTrack='sw';S.view='track';render()"); pg.wait_for_selector(".tk-a")
        print(w, "track cards:", pg.locator(".tkpage>article").count(), "| head:", pg.locator(".th-text h2").inner_text())
        pg.click(".tk-a [data-act=start]"); pg.wait_for_selector("#clock"); pg.locator("#main [data-act=stop]").first.click(); pg.wait_for_selector("#dform")
        pg.click("[data-act=dlg-close]"); print("  close keeps timer:", not pg.locator("#dlg").evaluate("d=>d.open"), bool(st()["timer"]))
        pg.locator("#main [data-act=stop]").first.click(); pg.click("[data-act=discard-timer]"); print("  after 1st press:", pg.locator("[data-act=discard-timer]").inner_text(), "| open", pg.locator("#dlg").evaluate("d=>d.open"))
        pg.click("[data-act=discard-timer]"); pg.wait_for_timeout(200)
        print("  discarded: dlg open", pg.locator("#dlg").evaluate("d=>d.open"), "| timer", st()["timer"], "| sessions", len(st()["sessions"]), "| toast:", pg.locator("#toast").inner_text(), pg.locator("#toast").evaluate("t=>getComputedStyle(t).opacity"))
        # log, then clear hours from Plan
        pg.evaluate("S.planTrack='sw';S.view='track';render()"); pg.click(".tk-a [data-act=start]"); pg.locator("#main [data-act=stop]").first.click(); pg.fill("#f-m","45"); pg.click("#dform button[type=submit]")
        it=st()["sessions"][0]["it"]; pg.evaluate("S.view='track';render()"); print("  logged:", pg.evaluate(f"logged()['{it}']"), "| recent rows", pg.locator(".tk-d .srow").count())
        pg.click("[data-act=to-plan]"); pg.wait_for_selector(".board"); print("  plan track:", st()["planTrack"], st()["view"])
        pg.locator(f"details.item[data-i='{it}'] summary").click(); pg.click("[data-act=item-clear]"); print("  armed label:", pg.locator("[data-act=item-clear]").inner_text())
        pg.click("[data-act=item-clear]"); print("  cleared:", pg.evaluate(f"logged()['{it}']||0"), "| live", pg.evaluate("live().length"))
        # settings
        pg.evaluate("S.view='more';render()"); pg.click("[data-act=theme-set][data-t=dark]"); print("  theme:", pg.evaluate("document.documentElement.dataset.theme"), "| cards", pg.locator(".stpage>article").count())
        pg.fill("#st-ai","5"); pg.click("form[data-form=settings] button[type=submit]"); print("  split ai:", st()["settings"]["targets"]["ai"])
        # overflow check on every page
        for v in ("home","today","week","plan","ideas","proof","more","track"):
            pg.evaluate(f"S.view='{v}';render()"); pg.wait_for_timeout(120)
            ov=pg.evaluate("(()=>{const m=document.querySelector(w>899?'#inner':'html');return m.scrollWidth-m.clientWidth})()".replace("w>899", "true" if w>899 else "false"))
            if ov>1: print("  H-OVERFLOW", v, ov)
        ctx.close()
    b.close()
print("ERRORS:", errs)
