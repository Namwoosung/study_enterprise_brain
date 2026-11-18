from pathlib import Path
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
import json, os, re
from playwright.sync_api import sync_playwright, expect

here=Path(__file__).resolve().parent
out=here/'qa';out.mkdir(exist_ok=True)
dist=Path(os.environ.get('READER_TEST_DIST',here/'dist')).resolve()
base=os.environ.get('READER_TEST_BASE',dist.as_uri()).rstrip('/')
manifest=json.loads((dist/'manifest.json').read_text(encoding='utf-8'))
lessons=[l for u in manifest['units'] for l in u['lessons']]
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for k in ['href','src']:
            if k in a:self.links.append(a[k])
for file in [dist/'index.html',*[dist/(l['id']+'.html') for l in lessons]]:
    parsed=Links();parsed.feed(file.read_text(encoding='utf-8'))
    for href in parsed.links:
        u=urlsplit(href)
        if u.scheme or u.netloc:assert u.scheme in ['https','http','mailto'],(file.name,href);continue
        if not u.path:continue
        target=(file.parent/unquote(u.path)).resolve()
        assert target.is_relative_to(dist) and target.exists(),(file.name,href)
    if file.name!='index.html':
        original=dist/'materials'/next(l['path'] for l in lessons if file.stem==l['id'])
        assert original.exists()
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for width,height in [(1500,1000),(390,844)]:
        page=browser.new_page(viewport={'width':width,'height':height})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        for lesson in lessons:
            page.goto(base+'/'+lesson['id']+'.html')
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
                assert page.locator('article details ol li').count()==4
                page.locator('.reader-example').scroll_into_view_if_needed()
                page.screenshot(path=out/f'rag-{width}.png')
            if lesson['id']=='U14-L01':
                page.locator('#evidence-choice').select_option('2026-03-20')
                expect(page.locator('.evidence-result')).to_contain_text('\ubc15\uc815\uc6b0')
                assert page.locator('.evidence-result svg rect').count()==4
                page.locator('.reader-example').scroll_into_view_if_needed();page.screenshot(path=out/f'graph-{width}.png')
            if lesson['id']=='U14-L02':
                page.locator('#evidence-choice').select_option('global')
                expect(page.locator('.evidence-result')).to_contain_text('R-A1')
                expect(page.locator('.evidence-result')).to_contain_text('Map')
            if lesson['id']=='U15-L01':
                page.locator('#evidence-choice').select_option('narrow-collapsed')
                expect(page.locator('.decision-status')).to_contain_text('77')
                assert page.locator('.selected-node').count()==3 # T03 is shared by two branches
                page.locator('.summary-tree button').filter(has_text=re.compile('^T02$')).click()
                expect(page.locator('.source-evidence').first).to_contain_text('T02')
                page.locator('.reader-example').scroll_into_view_if_needed();page.screenshot(path=out/f'tree-{width}.png')
            if lesson['id']=='U12-L02':
                page.locator('#evidence-choice').select_option('K07')
                expect(page.locator('.decision-status')).to_contain_text('\uc218\uc815')
                expect(page.locator('.evidence-result')).to_contain_text('D4#1')
            if lesson['id']=='U11-L02':
                page.locator('#evidence-choice').select_option('spike')
                expect(page.locator('.decision-status')).to_contain_text('404')
            if lesson['id'].startswith('S01'):
                page.locator('#evidence-choice').select_option('coref')
                expect(page.locator('.decision-status')).to_contain_text('E01')
        assert not errors,errors
        page.close()
    page=browser.new_page(accept_downloads=True)
    page.goto(base+'/index.html')
    page.locator('#home-search').fill('blocking')
    assert page.locator('#home-results a[href^="U10"]').count()>0
    page.goto(base+'/U14-L01.html')
    page.evaluate("localStorage.setItem('knowledge-lab-v1',JSON.stringify({notes:{old:'preserved'},completed:['old']}))")
    page.locator('#lesson-note').fill('Explain with another example.')
    page.locator('#lesson-complete').check();page.locator('#lesson-bookmark').check();page.reload()
    expect(page.locator('#lesson-note')).to_have_value('Explain with another example.')
    expect(page.locator('#lesson-complete')).to_be_checked()
    expect(page.locator('#lesson-bookmark')).to_be_checked()
    with page.expect_download() as download:page.locator('#export-learning').click()
    saved=out/'records.json';download.value.save_as(saved)
    records=json.loads(saved.read_text(encoding='utf-8'))
    assert records['legacy']['notes']['old']=='preserved'
    assert records['learning']['notes']['U14-L01']=='Explain with another example.'
    page.goto(base+'/index.html')
    expect(page.locator('#continue-learning')).to_have_attribute('href','U14-L01.html')
    page.screenshot(path=out/'home.png',full_page=True)
    browser.close()
print(f'{len(lessons)} lessons: local resources, desktop/mobile render, evidence interactions, full-text search, notes/restore/export and legacy preservation passed')
