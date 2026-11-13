from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome", args=["--no-sandbox"])
    for w,h in ((1366,768),(390,844)):
        ctx=b.new_context(viewport={"width":w,"height":h}); pg=ctx.new_page()
        pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None); pg.on("pageerror", lambda e: errs.append("PAGEERR "+str(e)))
        pg.goto("http://localhost:8765/"); pg.wait_for_selector(".dash"); pg.wait_for_function("volsReady")
        print(w, "quiz pairs per volume:", pg.evaluate("VOLS.map(v=>v.quiz.length)"), "| per quiz:", pg.evaluate("(()=>{const m={};VOLS.forEach(v=>v.quiz.forEach(q=>{const k=q.key.split('#')[0];m[k]=(m[k]||0)+1}));return Object.entries(m).map(e=>e.join(':')).join(' ')})()"))
        print("  cards at start:", pg.evaluate("S.cards.length"), "locked:", pg.evaluate("UI.locked"))
        print("  sample:", pg.evaluate("VOLS[0].quiz[3].q.slice(0,70)+' => '+VOLS[0].quiz[3].a.slice(0,70)"))
        # finish a lesson -> cards released
        pg.evaluate("ACT['item-done']({dataset:{it:'FSE.C01.M01'}})"); n=pg.evaluate("S.cards.length"); pg.wait_for_timeout(150); print("  released on done:", n, "| toast:", pg.locator("#toast").inner_text())
        pg.evaluate("ACT['item-done']({dataset:{it:'STR.V01.M04'}})"); print("  + STR:", pg.evaluate("S.cards.length"))
        q=pg.evaluate("cardQueue()"); print("  queue: due", len(q["due"]), "new", len(q["nw"]))
        pg.evaluate("S.view='today';render()"); pg.click("#main [data-act=rv-start]"); pg.wait_for_selector(".fc"); print("  review:", pg.locator(".th-text .lede").inner_text(), "| front:", pg.locator("#card-q-body").inner_text()[:60])
        pg.keyboard.press("Space"); pg.wait_for_selector(".rate"); print("  buttons:", [x.replace("\n"," ") for x in pg.locator(".rate .btn").all_inner_texts()])
        pg.keyboard.press("1"); pg.wait_for_timeout(100); print("  again -> still", pg.evaluate("UI.rv.q.length"), "in queue, rated", pg.evaluate("UI.rv.n"))
        for k in range(30):
            if pg.evaluate("!UI.rv || !!UI.rv.done"): break
            pg.click("[data-act=rv-show]"); pg.click(f"[data-act=rv-rate][data-g='{2 + k%2}']")
        print("  done:", pg.locator(".rvdone").inner_text().replace("\n"," ")[:110]); s=pg.evaluate("live().slice(-1)[0]"); print("  session:", s["tr"], s["m"], s["label"], s["note"])
        print("  states:", pg.evaluate("(()=>{const m={};S.cards.forEach(c=>{const k=c.state+':'+c.ivl;m[k]=(m[k]||0)+1});return m})()"), "| cardDay", pg.evaluate("S.cardDay.n"), "| new left today:", pg.evaluate("cardQueue().nw.length"))
        # time travel: cards come due, intervals grow
        pg.evaluate("S.cards.forEach(c=>{if(c.state==='review'){c.due=todayIso()}})"); c=pg.evaluate("(()=>{const c=S.cards.find(c=>c.state==='review'&&c.ivl===2);return [0,1,2,3].map(g=>nextIvl(c,g))})()"); print("  next intervals for a 2-day card:", c)
        # own cards: library quick add, cards tab, lesson
        pg.evaluate("UI.libTab='home';S.view='library';render()"); pg.fill("#cq-q","What is $E$ for S355 steel?"); pg.fill("#ca-q","$E = 210\\\\,000$ N/mm²"); pg.select_option("#ct-q","str"); pg.click(".cform button[type=submit]"); print("  quick add:", pg.evaluate("S.cards.slice(-1)[0].src+'/'+S.cards.slice(-1)[0].tr"), "| form cleared:", pg.input_value("#cq-q")=="" )
        pg.click(".ftab[data-tr=cards]"); print("  cards tab rows:", pg.locator(".crow").count(), "| stats:", pg.locator(".stat b").all_inner_texts()); pg.fill("#card-q","S355"); pg.wait_for_timeout(150); print("  search:", pg.locator(".crow").count(), "| focus kept:", pg.evaluate("document.activeElement.id"))
        pg.click("[data-act=card-edit]"); pg.fill("#cd-a","210 000 N/mm²"); pg.click("#dform button[type=submit]"); print("  edited:", pg.evaluate("S.cards.slice(-1)[0].a"))
        pg.evaluate("openLesson('FSE-C01-Workbench.md',4)"); pg.wait_for_selector("#lesson h2"); pg.click("[data-act=card-new]"); pg.fill("#cd-q","Front from lesson"); pg.fill("#cd-a","Back"); pg.click("#dform button[type=submit]"); c=pg.evaluate("S.cards.slice(-1)[0]"); print("  lesson card:", c["it"], c["tr"], c["src"]); pg.locator("[data-act=read-close]").first.click()
        pg.evaluate("UI.cardQ='';UI.cardF='sw';UI.libTab='cards';S.view='library';render()"); n0=pg.evaluate("cardsLive().length"); pg.locator("[data-act=card-edit]").first.click(); pg.click("[data-act=card-del]"); pg.click("[data-act=card-del]"); print("  delete:", n0, "->", pg.evaluate("cardsLive().length"))
        # deleted quiz card does not come back; reload keeps cards
        pg.evaluate("S.cards.find(c=>c.key).del=1; render()"); n1=pg.evaluate("S.cards.length"); pg.wait_for_timeout(500); pg.reload(); pg.wait_for_function("volsReady"); print("  after reload cards:", pg.evaluate("S.cards.length")==n1, "| own cards first in new:", pg.evaluate("(cardQueue().nw[0]||{}).src"))
        # maths card renders; ending early logs
        pg.evaluate("S.cardDay=null; S.cards.forEach(c=>{if(c.src==='own'&&c.tr==='str'){c.state='new'}})"); pg.evaluate("ACT['rv-start']({dataset:{tr:'str'}})"); pg.wait_for_selector(".fc"); pg.wait_for_selector("#card-q-body math"); print("  maths on card ok |", pg.locator(".th-text .lede").inner_text())
        pg.screenshot(path=f"/tmp/rv-{w}.png"); pg.click("[data-act=rv-show]"); pg.wait_for_timeout(200); pg.screenshot(path=f"/tmp/rv-{w}-back.png"); n2=pg.evaluate("live().length"); pg.click("[data-act=rv-rate][data-g='2']"); pg.click("[data-act=rv-end]"); print("  end early logs:", pg.evaluate("live().length")-n2, "| view:", pg.evaluate("S.view"))
        pg.evaluate("UI.cardF='';UI.libTab='cards';S.view='library';render()"); pg.wait_for_timeout(200); pg.screenshot(path=f"/tmp/cards-{w}.png", full_page=(w<900))
        for v in ("library","review"):
            pg.evaluate(f"S.view='{v}';render()"); pg.wait_for_timeout(150); print("  overflow", v, pg.evaluate("(()=>{const m=document.querySelector('%s');return m.scrollWidth-m.clientWidth})()" % ("#inner" if w>899 else "html")))
        ctx.close()
    b.close()
print("ERRORS:", errs)
