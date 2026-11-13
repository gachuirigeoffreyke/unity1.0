from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome", args=["--no-sandbox"])
    for w,h in ((1366,768),(390,844)):
        ctx=b.new_context(viewport={"width":w,"height":h}); pg=ctx.new_page()
        pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None); pg.on("pageerror", lambda e: errs.append("PAGEERR "+str(e)))
        pg.goto("http://localhost:8765/"); pg.wait_for_selector(".dash")
        # simulate an older install with no portfolio, then reload
        pg.evaluate("delete S.port; DB.put(S)"); pg.wait_for_timeout(300); pg.reload(); pg.wait_for_selector(".dash")
        print(w, "seeded after upgrade:", pg.evaluate("S.port.length"), pg.evaluate("S.port[0].name"))
        pg.evaluate("S.view='proof';render()"); print("  tabs:", pg.locator(".ftab").all_inner_texts(), "| in progress:", pg.locator(".pv.home .pcard h3").all_inner_texts(), "| criteria:", pg.locator(".pbox .prow").count())
        pg.click(".tmini[data-tr=sw]"); print("  sw cards:", pg.locator(".pcard").count(), "| chama milestones:", pg.locator(".pcard.building .pms .arow").count(), "| targets:", pg.locator(".pv.tr .prow").count())
        pg.locator("[data-act=port-edit]").nth(4).click(); name=pg.input_value("#pe-n"); pg.select_option("#pe-st","shipped"); pg.select_option("#pe-m","personal"); pg.fill("#pe-ev","https://example.org/app"); pg.click("#dform button[type=submit]")
        e=pg.evaluate(f"S.port.find(x=>x.name=={name!r})"); print("  edited:", e["name"], e["st"], e["mode"], e["on"], "| link:", pg.locator(".pcard.shipped .ev a").count())
        pg.click(".ftab[data-tr=str]"); print("  str empty:", pg.locator(".pv.tr .empty").inner_text()[:50]); pg.click("[data-act=port-add]"); pg.fill("#pe-n","Two-storey RC frame design"); pg.click("#dform button[type=submit]"); print("  str entries:", pg.locator(".pcard").count())
        pg.click("[data-act=port-edit]"); pg.click("[data-act=port-del]"); pg.click("[data-act=port-del]"); print("  removed:", pg.locator(".pcard").count(), pg.locator("#dlg").evaluate("d=>d.open"))
        pg.evaluate("S.planTrack='sw';S.view='track';render()"); print("  track card:", pg.locator(".tk-e .eyebrow").first.inner_text(), pg.locator(".tk-e .arow").count()); pg.click(".tk-e [data-act=port-tab]"); print("  ->", pg.evaluate("S.view+'/'+UI.portTab"))
        pg.evaluate("S.view='more';render()"); pg.click("[data-act=reset]"); pg.click("[data-act=reset]"); pg.wait_for_timeout(200); pg.evaluate("S.view='proof';render()"); print("  after reset entries:", pg.evaluate("S.port.length"))
        ov=pg.evaluate("(()=>{const m=document.querySelector('%s');return m.scrollWidth-m.clientWidth})()" % ("#inner" if w>899 else "html")); print("  overflow:", ov)
        ctx.close()
    b.close()
print("ERRORS:", errs)
