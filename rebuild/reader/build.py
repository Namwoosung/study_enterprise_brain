"""Build the selected B reading layout for written v2 lessons; no deployment."""
from pathlib import Path
from html import escape
import json, re, importlib.util, shutil
import markdown

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
COURSE=ROOT/'learning-v2'
OUT=HERE/'dist'
OUT.mkdir(exist_ok=True)
manifest=json.loads((COURSE/'manifest.json').read_text(encoding='utf-8'))
lessons=[dict(l,unit=u['id']) for u in manifest['units'] for l in u['lessons']]
routes={l['path']:l['id']+'.html' for l in lessons}
spec=importlib.util.spec_from_file_location('comparison_builder',ROOT/'rebuild/prototypes/build.py')
comparison=importlib.util.module_from_spec(spec)
spec.loader.exec_module(comparison)
events=comparison.events_from_turtle((COURSE/'units/U04/02-events-and-property-graphs.md').read_text(encoding='utf-8'))
shutil.copy2(ROOT/'rebuild/prototypes/reading.css',OUT/'comparison.css')
shutil.copy2(ROOT/'rebuild/prototypes/reading.js',OUT/'comparison.js')
for name in ['reader.css','reader.js']:
    shutil.copy2(HERE/name,OUT/name)

def render(source):
    body=markdown.markdown(source,extensions=['fenced_code','tables','toc'])
    body=body.replace('<table>','<div class="table-scroll" tabindex="0"><table>').replace('</table>','</table></div>')
    body=body.replace('<pre>','<pre tabindex="0">')
    return body

def links(body,origin):
    def replace(match):
        url=match[1]
        if '://' in url or url.startswith('#'):return match[0]
        raw,sep,frag=url.partition('#')
        target=(origin.parent/raw).resolve()
        try:rel=target.relative_to(COURSE.resolve()).as_posix()
        except ValueError:return match[0]
        if rel in routes:return 'href="'+routes[rel]+(sep+frag if sep else '')+'"'
        return 'href="'+escape(target.as_uri(),quote=True)+'"'
    return re.sub(r'href="([^"]+)"',replace,body)

def aside(lesson,body):
    if lesson['id']=='U04-L02':
        return comparison.comparison(events)+'<script id="event-data" type="application/json">'+json.dumps(events,ensure_ascii=False)+'</script>'
    if lesson['unit']=='U13':
        return '''<section class="trace"><h2>같은 질문의 근거 선택</h2><p>모의 데이터에서 단계별로 남은 청크입니다. 실제 검색 서비스의 성능 측정이 아닙니다.</p><ol><li>조건 필터 후 벡터 상위 3개<br><code>D05a · D02b · D02a</code></li><li>어휘 검색 상위 3개<br><code>D04a · D02a · D05a</code></li><li>결합 후 재정렬<br><code>D02a → D04a → D05a → D02b</code></li><li>100자 근거 예산<br><strong>D02a + D04a = 88자</strong></li></ol><p>D04a는 필수 기록 항목을 담습니다. 벡터 상위 3개만 사용하면 이 근거가 빠집니다.</p></section>'''
    if lesson['unit']=='U06':
        return '''<section class="trace"><h2>같은 규칙, 다른 입력</h2><p>본문과 동봉 실행에서 확인한 결과를 비교합니다.</p><label for="validation-case">검사할 입력</label><select id="validation-case"><option value="missing">담당자 관계 없음</option><option value="typed">담당자와 Person 타입 있음</option><option value="untyped">담당자만 있고 타입 없음</option></select><div id="validation-result" aria-live="polite"></div><p>브라우저에서 추론기를 실행하는 기능은 아닙니다. Python 실행 결과의 대조 화면입니다.</p></section>'''
    heads=re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',body)
    return '<nav class="lesson-outline" aria-label="수업 안 목차"><h2>이 수업에서</h2>'+''.join('<a href="#'+i+'">'+t+'</a>' for i,t in heads)+'</nav>'

nav=''.join('<a href="'+l['id']+'.html" data-title="'+escape(l['title'],quote=True)+'">'+escape(l['unit']+' '+l['title'])+'</a>' for l in lessons)
for n,l in enumerate(lessons):
    origin=COURSE/l['path'];body=links(render(origin.read_text(encoding='utf-8')),origin)
    title=re.search(r'<h1[^>]*>(.*?)</h1>',body)[1];body=re.sub(r'<h1[^>]*>.*?</h1>','',body,count=1)
    previous=lessons[n-1] if n else None;following=lessons[n+1] if n+1<len(lessons) else None
    pager=''.join('<a href="'+item['id']+'.html">'+prefix+escape(item['title'])+'</a>' for item,prefix in [(previous,'이전 수업: '),(following,'다음 작성 수업: ')] if item)
    html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(l['title'])}</title><link rel="stylesheet" href="comparison.css"><link rel="stylesheet" href="reader.css"></head><body><a class="skip" href="#lesson">본문으로 이동</a><header class="reader-header"><a href="index.html">기업 지식 학습 교재</a><span>개편 중인 본문 · 선택한 B안</span><button id="menu-toggle" aria-expanded="false" aria-controls="course-nav">수업 목록</button></header><div class="reader-grid"><nav id="course-nav" class="course-nav" aria-label="작성된 수업"><label for="lesson-search">수업 찾기</label><input id="lesson-search" type="search" placeholder="개념 또는 제목"><div class="course-links">{nav}</div><p>전체 과정 중 작성된 수업입니다. 전체 단원의 완성을 뜻하지 않습니다.</p></nav><main id="lesson" class="lesson"><header><p class="unit-name">{l['unit']}</p><h1>{title}</h1><a class="source-link" href="{origin.as_uri()}">Markdown 원문</a></header><article>{body}</article><nav class="pager" aria-label="수업 이동">{pager}</nav></main><aside class="reader-example">{aside(l,body)}</aside></div><script src="comparison.js"></script><script src="reader.js"></script></body></html>'''
    html=html.replace('<body>','<body class="view-b">')
    (OUT/(l['id']+'.html')).write_text(html,encoding='utf-8')
shutil.copy2(OUT/(lessons[0]['id']+'.html'),OUT/'index.html')
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Built {len(lessons)} full lesson pages in {OUT}')
