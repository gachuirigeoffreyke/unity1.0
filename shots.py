"""Audit screenshots: every page and surface, at laptop / wide / phone, light + dark."""
import sys, os
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
SEED = """(()=>{const t=todayIso();const mk=(d,m,tr,it)=>S.sessions.push({id:uid('S'),d,ts:parse(d).getTime()+4e7,m,tr,it,label:'',mode:1,note:'',off:false,u:Date.now()});
 [[0,95,'sw','FSE.C01.M01'],[0,60,'str','STR.SETUP'],[1,150,'sw','FSE.C01.M02'],[2,45,'ai','AI.F01'],[3,200,'sw','FSE.C01.M02'],[5,30,'ent','ENT.01'],[6,120,'str','STR.SETUP'],[8,240,'sw','FSE.C01.M03'],[9,320,'str','STR.V01.M01'],[12,80,'ai','AI.F01'],[15,60,'sw','FSE.C02.M01'],[20,140,'sw','FSE.C01.M01'],[27,90,'sw','FSE.C01.M01']].forEach(a=>mk(addDays(t,-a[0]),a[1],a[2],a[3]));
 const it=item('FSE.C01.M01'); it.st='done'; it.doneAt=addDays(t,-1); const i2=item('FSE.C01.M02'); if(i2) i2.next='Resume at the rebase exercise';
 const mi=(x,st,d,o)=>S.ideas.push(Object.assign({id:uid('I'),ts:Date.now()-d*864e5,text:x,st,u:Date.now()},o||{}));
 mi('Wind-load calculator for canopies','parked',2);mi('Write up the Sigenergy lessons','parked',9);mi('Chama: SMS reminders','scheduled',4,{tr:'sw'});mi('Learn Rust this month','dropped',5);
 S.proofs[0].done=1; S.proofs[0].ev='github.com/…/workbench'; render();})()"""
errs = []
def run(b, name, w, h, scheme, phone=False):
    ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme); pg = ctx.new_page()
    pg.on("pageerror", lambda e: errs.append(name + " " + str(e))); pg.on("console", lambda m: errs.append(name + " " + m.text) if m.type == "error" else None)
    pg.goto("http://localhost:8765/"); pg.wait_for_selector(".dash"); pg.evaluate(SEED); pg.wait_for_timeout(300)
    shot = lambda n, full=phone: pg.screenshot(path=f"{out}/{name}-{n}.png", full_page=full)
    go = lambda js: (pg.evaluate(js), pg.wait_for_timeout(250))
    for v in ("home", "today", "week", "plan", "ideas", "proof", "more"):
        go(f"S.view='{v}';render();toTop()"); shot(v)
    for tb in ("sw", "str"):
        go(f"UI.portTab='{tb}';S.view='proof';render();toTop()"); shot("port-" + tb)
    go("UI.portTab='home'")
    for tr in ("sw", "str"):
        go(f"S.planTrack='{tr}';S.view='track';render();toTop()"); shot("track-" + tr)
    if name in ("lap-light", "wide-dark", "phone-light"):
        go("S.view='today';render()")
        pg.locator("[data-act=attn]").first.click(); pg.wait_for_timeout(350); shot("attn", False); pg.locator("#attn [data-act=attn]").click(); pg.wait_for_timeout(300)
        pg.locator("[data-act=start]").first.click(); pg.wait_for_timeout(1200); shot("timer", False)
        go("S.view='home';render()"); shot("timer-home", False)
        pg.locator("[data-act=stop]").first.click(); pg.wait_for_timeout(300); shot("dlg-log", False)
        pg.fill("#f-m", "40"); pg.click("#dform button[type=submit]"); pg.wait_for_timeout(200); shot("toast", False)
        go("S.view='ideas';render()"); pg.locator("[data-act=idea-promote]").first.click(); pg.wait_for_timeout(300); shot("dlg-promote", False); pg.keyboard.press("Escape")
        go("S.view='today';render()"); pg.locator("[data-act=off-plan]").first.click(); pg.wait_for_timeout(300); shot("dlg-off", False); pg.keyboard.press("Escape")
        go("S.view='plan';render()"); pg.locator("[data-act=add-item]").first.click(); pg.wait_for_timeout(300); shot("dlg-add", False); pg.keyboard.press("Escape")
        if not phone:
            pg.hover("#rail .ritem"); pg.wait_for_timeout(600); shot("rail", False)
    ctx.close()
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--no-sandbox"])
    run(b, "lap-light", 1366, 768, "light"); run(b, "lap-dark", 1366, 768, "dark")
    run(b, "wide-dark", 1920, 1050, "dark"); run(b, "wide-light", 1920, 1050, "light")
    run(b, "phone-light", 390, 844, "light", True); run(b, "phone-dark", 390, 844, "dark", True)
    b.close()
print("ERRORS:", errs)
