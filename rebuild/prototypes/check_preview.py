"""Exercise the offline previews in Chromium and capture the review images."""

import os
from pathlib import Path
from urllib.parse import unquote, urlsplit

from playwright.sync_api import expect, sync_playwright


HERE = Path(__file__).resolve().parent
SHOTS = HERE / "screenshots"
SIZES = {"desktop": (1400, 900), "mobile": (390, 844)}


def check_rendering(page, view, viewport):
    assert page.evaluate("document.documentElement.scrollWidth === innerWidth")
    assert page.locator(".part").count() == 12
    assert page.locator(".sample").count() >= 2

    for anchor in page.locator("a[href^='#']").all():
        target = anchor.get_attribute("href")[1:]
        assert page.locator(f"[id='{target}']").count() == 1, target
    sources = page.locator(".part a[href^='https://']")
    assert sources.count() >= 5
    assert sources.first.get_attribute("href") == (
        "https://www.w3.org/TR/rdf11-concepts/#section-rdf-graph"
    )
    assert page.locator(".table-scroll").count() >= 2
    originals = page.locator("a[href$='.md']")
    assert originals.count() >= 3
    for original in originals.all():
        assert (HERE / unquote(urlsplit(original.get_attribute("href")).path)).is_file()

    if viewport == "mobile":
        table = page.locator("#section-1 .table-scroll")
        table.focus()
        page.keyboard.press("ArrowRight")
        expect(table).to_be_focused()
        assert table.evaluate("element => element.scrollWidth > element.clientWidth")
        assert table.get_attribute("tabindex") == "0"
        part = page.locator("#section-6 pre")
        assert part.evaluate("element => element.scrollWidth > element.clientWidth")
        assert part.get_attribute("tabindex") == "0"
        if view == "b":
            assert page.locator("#section-5 + .workbench + #section-6").count() == 1
            assert page.locator(".workbench .comparison").evaluate(
                "element => getComputedStyle(element).position"
            ) == "static"


def check_comparison(page, view, viewport):
    comparison = page.locator("#compare-events")
    if view == "b" and viewport == "desktop":
        page.goto((HERE / "b.html").as_uri() + "#section-7")
        expect(comparison).to_have_attribute("data-focus", "pg")
        assert 62 <= comparison.bounding_box()["y"] < 85
    else:
        comparison.scroll_into_view_if_needed()
        page.evaluate("document.getElementById('compare-events').scrollIntoView()")

    assert comparison.locator("svg.rdf path.triple").count() == 6
    assert comparison.locator("svg.pg .relationship").count() == 3
    if viewport == "mobile":
        graph_scroll = comparison.locator(".rdf-panel .diagram-scroll")
        assert graph_scroll.get_attribute("tabindex") == "0"
        graph_scroll.focus()
        page.keyboard.press("ArrowRight")
        expect(graph_scroll).to_be_focused()
        page.wait_for_function("element => element.scrollLeft > 0", arg=graph_scroll.element_handle())
        graph_scroll.evaluate("element => { element.scrollLeft = 0; }")
    expect(comparison.locator(".active")).to_have_attribute("data-relationship", "drive1")
    expected = {
        "drive1": ("2026-11-01T09:00:00+09:00", "12", "2"),
        "drive2": ("2026-11-01T14:00:00+09:00", "18", "1"),
        "drive3": ("2026-11-02T10:00:00+09:00", "9", "3"),
    }
    comparison.get_by_role("radio", name="drive1").focus()
    for i, (drive, (time, distance, passengers)) in enumerate(expected.items()):
        if i:
            page.keyboard.press("ArrowRight")
        expect(comparison.get_by_role("radio", name=drive)).to_be_checked()
        expect(comparison.locator(".active")).to_have_attribute("data-relationship", drive)
        expect(comparison.locator("svg.rdf [data-value='iri']")).to_have_text("ex:" + drive)
        expect(comparison.locator("svg.rdf [data-value='distanceKm']")).to_have_text(distance)
        expect(comparison.locator("svg.rdf [data-value='passengers']")).to_have_text(passengers)
        expect(comparison.locator("time")).to_have_attribute("datetime", time)
        expect(comparison.locator("[data-value='triples']")).to_contain_text(
            f'ex:{drive} ex:distanceKm "{distance}"'
        )
        expect(comparison.locator("[data-value='cypher']")).to_contain_text(
            f"distanceKm: {distance}, passengers: {passengers}"
        )
    page.keyboard.press("ArrowLeft")
    page.screenshot(path=SHOTS / f"{view}-{viewport}-comparison.png", animations="disabled")
    if viewport == "mobile":
        comparison.locator(".diagram-scroll").evaluate_all(
            "elements => elements.forEach(element => { element.scrollLeft = element.scrollWidth; })"
        )
        page.screenshot(path=SHOTS / f"{view}-{viewport}-comparison-right.png", animations="disabled")

    detail = comparison.locator("summary")
    detail.focus()
    page.keyboard.press("Enter")
    expect(comparison.locator("details")).to_have_attribute("open", "")
    expect(comparison.locator("[data-value='cypher']")).to_be_visible()
    page.keyboard.press("Enter")
    expect(comparison.locator("[data-value='cypher']")).to_be_hidden()


def check_navigation(page, view, viewport):
    if view == "c":
        page.get_by_role("navigation", name="학습 단계").get_by_text("비교").click()
        assert page.evaluate("location.hash") == "#step-4"
        expect(page.locator(".steps [aria-current]")).to_have_text("비교")
    elif viewport == "mobile":
        menu = page.locator(".small-contents")
        menu.locator("summary").click()
        menu.get_by_text("같은 질문과 결과").click()
        assert page.evaluate("location.hash") == "#section-9"
        expect(menu).not_to_have_attribute("open", "")
    else:
        page.goto((HERE / f"{view}.html").as_uri() + "#section-9")
    next_variant = page.locator(".variants a").filter(has_text="C" if view != "c" else "A")
    expect(next_variant).to_have_attribute("href", "c.html#section-9" if view != "c" else "a.html#section-8")
    next_variant.click()
    expected = "#section-9" if view != "c" else "#section-8"
    assert page.evaluate("location.hash") == expected


def main():
    SHOTS.mkdir(exist_ok=True)
    with sync_playwright() as playwright:
        executable = os.environ.get("PREVIEW_BROWSER")
        browser = playwright.chromium.launch(headless=True, executable_path=executable)
        print(f"Chromium {browser.version}")
        for viewport, (width, height) in SIZES.items():
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto((HERE / "index.html").as_uri())
            expect(page.locator(".choice h2 a")).to_have_count(3)
            assert page.evaluate("document.documentElement.scrollWidth === innerWidth")
            page.screenshot(path=SHOTS / f"index-{viewport}.png", animations="disabled")
            shared_body = None
            for view in "abc":
                page.goto((HERE / f"{view}.html").as_uri())
                sections = page.locator(".part > :not(.margin-note)").evaluate_all(
                    """elements => elements.map(element => {
                      const copy = element.cloneNode(true);
                      // Overflow depends on each layout's width. Keyboard region
                      // attributes may differ; educational markup must match.
                      copy.querySelectorAll('pre, .table-scroll').forEach(region => {
                        ['tabindex', 'role', 'aria-label'].forEach(key => region.removeAttribute(key));
                      });
                      return copy.outerHTML;
                    })"""
                )
                if shared_body is None:
                    shared_body = sections
                assert shared_body == sections, "The reading layouts must have identical core content."
                page.screenshot(path=SHOTS / f"{view}-{viewport}.png", animations="disabled")
                if viewport == "desktop":
                    page.screenshot(
                        path=SHOTS / f"{view}-full.jpg", full_page=True,
                        animations="disabled", quality=74,
                    )
                check_rendering(page, view, viewport)
                check_comparison(page, view, viewport)
                check_navigation(page, view, viewport)
                print(f"{view.upper()} {viewport} {width}x{height}: passed")
            assert not errors, errors
            page.close()
        browser.close()


if __name__ == "__main__":
    main()
