from pathlib import Path
import json
from playwright.sync_api import sync_playwright, expect

here=Path(__file__).resolve().parent
out=here/'qa';out.mkdir(exist_ok=True)
manifest=json.loads((here/'dist/manifest.json').read_text(encoding='utf-8'))
lessons=[l for u in manifest['units'] for l in u['lessons']]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for width,height in [(1500,1000),(390,844)]:
        page=browser.new_page(viewport={'width':width,'height':height})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        for lesson in lessons:
            page.goto((here/'dist'/(lesson['id']+'.html')).as_uri())
            assert page.locator('article').inner_text().strip()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),lesson['id']
            assert page.locator('.course-links a').count()==len(lessons)
            if lesson['id']=='U04-L02':
                if width<790:assert page.locator('article .reader-example').count()==1
                page.get_by_role('radio',name='drive3').check()
                expect(page.locator('[data-value="distanceKm"]')).to_have_text(['9','9'])
                page.locator('.reader-example').scroll_into_view_if_needed()
                page.screenshot(path=out/f'rdf-{width}.png')
            if lesson['id']=='U06-L01':
                if width<790:assert page.locator('article .reader-example').count()==1
                page.locator('#validation-case').select_option('untyped')
                expect(page.locator('#validation-result')).to_contain_text('RDFS')
            if lesson['id']=='U13-L01':
                page.locator('.reader-example').scroll_into_view_if_needed()
                page.screenshot(path=out/f'rag-{width}.png')
        assert not errors,errors
        page.close()
    browser.close()
print(f'{len(lessons)} lessons: desktop/mobile render, navigation and example correspondence passed')
