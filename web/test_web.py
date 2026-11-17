from pathlib import Path
import json,re
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"qa";OUT.mkdir(exist_ok=True)
base="http://127.0.0.1:4173"
results=[];errors=[]
def passed(label):results.append(label)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context(viewport={"width":1440,"height":1000},device_scale_factor=1)
    page=context.new_page()
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.on("console",lambda m:errors.append(m.text) if m.type=="error" else None)
    def go(route):
        page.goto(base+route)
        page.wait_for_load_state("networkidle")
    go("/#/home")
    expect(page.locator(".course-row")).to_have_count(8)
    page.screenshot(path=str(OUT/"home-desktop.png"),full_page=True)
    passed("desktop home and eight learning chapters")
    page.locator("[data-node='E01']").click()
    expect(page.locator("#case-detail")).to_contain_text("SN101")
    passed("graph node navigation")
    page.locator("[data-case-tab='runs']").click()
    expect(page.locator("#row-RUN008")).to_contain_text("E03")
    expect(page.locator("#row-RUN002")).to_contain_text("E01")
    passed("case rows retain both L02 events")
    go("/#/case/D07")
    expect(page.locator("#document-view")).to_contain_text("원인이라는 결론은 내리지 않았다")
    page.locator("#doc-filter").fill("D11")
    expect(page.locator(".doc-button")).to_have_count(1)
    page.locator(".doc-button").click()
    expect(page.locator("#document-view")).to_contain_text("2026-11-04 08:00")
    passed("document filters and original evidence")
    go("/#/learn/m4/m4-02")
    page.locator("[data-identity='E01']").click()
    expect(page.locator("#identity-result")).to_contain_text("NORTH")
    page.locator("[data-identity='E02']").click()
    expect(page.locator("#identity-result")).to_contain_text("맞습니다")
    passed("entity matching feedback")
    go("/#/learn/m5/m5-02")
    page.locator("#document-select").select_option("D01")
    expect(page.locator("#validation-result .status-line").nth(0)).to_contain_text("통과")
    expect(page.locator("#validation-result .status-line").nth(1)).to_contain_text("불일치")
    page.screenshot(path=str(OUT/"validation-desktop.png"),full_page=True)
    page.locator("#document-select").select_option("none")
    expect(page.locator("#validation-result")).to_contain_text("실패")
    passed("structure vs temporal validation")
    page.locator("#section-note").fill("구조 통과는 사실성 보장이 아니다.")
    page.locator("#bookmark").click()
    page.reload();page.wait_for_load_state("networkidle")
    expect(page.locator("#section-note")).to_have_value("구조 통과는 사실성 보장이 아니다.")
    expect(page.locator("#bookmark")).to_have_attribute("aria-pressed","true")
    page.locator("#toggle-done").click()
    expect(page.locator("#toggle-done")).to_contain_text("취소")
    passed("notes bookmarks and completion persist")
    page.locator("#notes-open").click()
    expect(page.locator("#notes-content")).to_contain_text("구조 통과는 사실성 보장이 아니다.")
    with page.expect_download() as d:page.locator("#export-notes").click()
    assert d.value.suggested_filename.endswith(".md")
    page.locator("[data-close='notes-dialog']").click()
    passed("notes export")
    go("/#/learn/m5/m5-05")
    expect(page.locator("#queue-result")).to_contain_text("300분 / 240분")
    expect(page.locator("#queue-result")).to_contain_text("80개 / 20개")
    page.locator("#review-rate").fill("5")
    expect(page.locator("#queue-result")).to_contain_text("150분 / 240분")
    passed("review queue arithmetic")
    go("/#/learn/m6/m6-01")
    expect(page.locator("#time-result")).to_contain_text("수집 전")
    page.locator("#known-time").select_option("after")
    expect(page.locator("#time-result")).to_contain_text("가능")
    page.locator("#event-time").select_option("RUN001")
    expect(page.locator("#time-result")).to_contain_text("D01")
    passed("valid and known time controls")
    go("/#/learn/m7/m7-05")
    page.locator("[data-mode='graph']").click()
    expect(page.locator("#retrieval-result")).to_contain_text("RUN008")
    page.locator("#retrieval-question").select_option("cause")
    expect(page.locator("#retrieval-result")).to_contain_text("원인 미확정")
    passed("retrieval modes maintain uncertainty")
    page.locator("#search-open").click()
    page.locator("#search-input").fill("SHACL")
    assert page.locator(".search-result").count()>0
    page.locator(".search-result").first.click()
    expect(page.locator("#search-dialog")).not_to_be_visible()
    passed("full course search navigation")
    go("/#/learn/m1/m1-06")
    expect(page.locator("details.answer")).to_have_count(1)
    assert not page.locator("details.answer").get_attribute("open")
    page.locator("details.answer summary").click()
    assert page.locator("details.answer").get_attribute("open") is not None
    passed("explanations remain hidden until requested")
    go("/#/practice")
    expect(page.locator(".practice-card")).to_have_count(18)
    page.locator("[data-answer='Q07']").fill("현재 자료로 원인 미확정")
    page.reload();page.wait_for_load_state("networkidle")
    expect(page.locator("[data-answer='Q07']")).to_have_value("현재 자료로 원인 미확정")
    passed("eighteen practice questions and saved answers")
    coverage=json.loads((ROOT/"coverage.json").read_text(encoding="utf-8"))
    for item in coverage:
        go("/"+item["route"])
        expect(page.locator(".article")).to_be_visible()
        assert len(page.locator(".article").inner_text())>80,item["id"]
    passed("all 54 mapped sections render")
    for key in ["glossary","evidence","sources","examples","plan","case-guide"]:
        go("/#/resource/"+key)
        expect(page.locator(".article")).to_be_visible()
    passed("reference and developer resources")
    # Generated content links resolve to actual app routes or packaged source files.
    links=page.evaluate("Object.values(COURSE.resources).map(x=>x.html).join('')+COURSE.chapters.flatMap(c=>c.sections.map(s=>s.html)).join('')")
    from html.parser import HTMLParser
    class Links(HTMLParser):
        def __init__(self):super().__init__();self.links=[]
        def handle_starttag(self,tag,attrs):
            for k,v in attrs:
                if k=="href":self.links.append(v)
    parser=Links();parser.feed(links)
    for link in parser.links:
        if link.startswith("materials/"):assert (ROOT/"dist"/link.split("#")[0]).exists(),link
        if link.startswith("#/learn/"):
            parts=link.split("/")
            assert any(c["id"]==parts[2] for c in page.evaluate("COURSE.chapters")),link
            if len(parts)>3:assert any(s["id"]==parts[3] for c in page.evaluate("COURSE.chapters") for s in c["sections"]),link
    passed("packaged materials and generated lesson links resolve")
    mobile=browser.new_context(viewport={"width":390,"height":844},is_mobile=True,device_scale_factor=1)
    mp=mobile.new_page();mp.on("pageerror",lambda e:errors.append(str(e)))
    for route in ["/#/home","/#/learn/m5/m5-02","/#/learn/m2/m2-04","/#/case/D02","/#/resource/glossary","/#/practice"]:
        mp.goto(base+route);mp.wait_for_load_state("networkidle")
        assert mp.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1"),route
    mp.goto(base+"/#/home");mp.wait_for_load_state("networkidle")
    mp.screenshot(path=str(OUT/"home-mobile.png"),full_page=True)
    mp.locator("#menu").click()
    expect(mp.locator("#sidebar")).to_have_class(re.compile("open"))
    mp.locator(".chapter-nav a").nth(4).click()
    expect(mp.locator(".lesson-title")).to_be_visible()
    assert "open" not in mp.locator("#sidebar").get_attribute("class")
    passed("mobile layouts and navigation")
    mobile.close();context.close();browser.close()
assert not errors,errors
report={"checks":results,"passed":len(results),"console_errors":errors,"viewports":["1440x1000","390x844"],"coverage_sections":54}
(OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
