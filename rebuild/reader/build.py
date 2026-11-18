"""Build the selected B reading layout for written v2 lessons; no deployment."""
from pathlib import Path
from html import escape
import json, re, importlib.util, shutil, os
import markdown
from panels import panel as evidence_panel

HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('COURSE_PROJECT_ROOT',HERE.parents[1]))
COURSE=Path(os.environ.get('COURSE_SOURCE',ROOT/'learning-v2'))
OUT=Path(os.environ.get('COURSE_OUTPUT',HERE/'dist'))
OUT.mkdir(exist_ok=True)
manifest=json.loads((COURSE/'manifest.json').read_text(encoding='utf-8'))
lessons=[dict(l,unit=u['id']) for u in manifest['units'] for l in u['lessons']]
routes={l['path']:l['id']+'.html' for l in lessons}
comparison_path=HERE/'comparison_builder.py'
if not comparison_path.exists():comparison_path=ROOT/'rebuild/prototypes/build.py'
spec=importlib.util.spec_from_file_location('comparison_builder',comparison_path)
comparison=importlib.util.module_from_spec(spec)
spec.loader.exec_module(comparison)
events=comparison.events_from_turtle((COURSE/'units/U04/02-events-and-property-graphs.md').read_text(encoding='utf-8'))
for name,target in [('reading.css','comparison.css'),('reading.js','comparison.js')]:
    bundled=HERE/target
    shutil.copy2(bundled if bundled.exists() else ROOT/'rebuild/prototypes'/name,OUT/target)
for name in ['reader.css','reader.js']:
    shutil.copy2(HERE/name,OUT/name)
glossary=json.loads((HERE/'glossary.json').read_text(encoding='utf-8'))
(OUT/'glossary.js').write_text('window.COURSE_GLOSSARY='+json.dumps(glossary,ensure_ascii=False).replace('</','<\\/')+';',encoding='utf-8')
shutil.copytree(COURSE,OUT/'materials',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))

def render(source):
    source=source.replace('<details>','<details markdown="1">')
    body=markdown.markdown(source,extensions=['fenced_code','tables','toc','md_in_html'])
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
        if target.exists():return 'href="materials/'+escape(rel,quote=True)+(sep+frag if sep else '')+'"'
        raise ValueError(f'Unresolved course resource: {origin}: {url}')
    return re.sub(r'href="([^"]+)"',replace,body)

def aside(lesson,body):
    special=evidence_panel(lesson,COURSE)
    if special:return special
    if lesson['id']=='U04-L02':
        return comparison.comparison(events)+'<script id="event-data" type="application/json">'+json.dumps(events,ensure_ascii=False)+'</script>'
    if lesson['id']=='U13-L01':
        return '''<section class="trace"><h2>같은 질문의 근거 선택</h2><p>모의 데이터에서 단계별로 남은 청크입니다. 실제 검색 서비스의 성능 측정이 아닙니다.</p><ol><li>조건 필터 후 벡터 상위 3개<br><code>D05a · D02b · D02a</code></li><li>어휘 검색 상위 3개<br><code>D04a · D02a · D05a</code></li><li>결합 후 재정렬<br><code>D02a → D04a → D05a → D02b</code></li><li>100자 근거 예산<br><strong>D02a + D04a = 88자</strong></li></ol><p>D04a는 필수 기록 항목을 담습니다. 벡터 상위 3개만 사용하면 이 근거가 빠집니다.</p></section>'''
    if lesson['id']=='U06-L01':
        return '''<section class="trace"><h2>같은 규칙, 다른 입력</h2><p>본문과 동봉 실행에서 확인한 결과를 비교합니다.</p><label for="validation-case">검사할 입력</label><select id="validation-case"><option value="missing">담당자 관계 없음</option><option value="typed">담당자와 Person 타입 있음</option><option value="untyped">담당자만 있고 타입 없음</option></select><div id="validation-result" aria-live="polite"></div><p>브라우저에서 추론기를 실행하는 기능은 아닙니다. Python 실행 결과의 대조 화면입니다.</p></section>'''
    heads=re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',body)
    return '<nav class="lesson-outline" aria-label="수업 안 목차"><h2>이 수업에서</h2>'+''.join('<a href="#'+i+'">'+t+'</a>' for i,t in heads)+'</nav>'

nav=''.join('<div class="nav-unit"><p>'+escape(u['id']+' · '+u['title'])+'</p>'+''.join('<a href="'+l['id']+'.html" data-title="'+escape(l['title'],quote=True)+'">'+escape(l['title'])+'</a>' for l in u['lessons'])+'</div>' for u in manifest['units'] if u['lessons'])
search=[]
for n,l in enumerate(lessons):
    origin=COURSE/l['path'];body=links(render(origin.read_text(encoding='utf-8')),origin)
    title=re.search(r'<h1[^>]*>(.*?)</h1>',body)[1];body=re.sub(r'<h1[^>]*>.*?</h1>','',body,count=1)
    previous=lessons[n-1] if n else None;following=lessons[n+1] if n+1<len(lessons) else None
    pager=''.join('<a href="'+item['id']+'.html">'+prefix+escape(item['title'])+'</a>' for item,prefix in [(previous,'이전 수업: '),(following,'다음 수업: ')] if item)
    html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(l['title'])}</title><link rel="stylesheet" href="comparison.css"><link rel="stylesheet" href="reader.css"></head><body><a class="skip" href="#lesson">본문으로 이동</a><header class="reader-header"><a href="index.html">기업 지식 학습 교재</a><span>개편 중인 본문 · 선택한 B안</span><button id="menu-toggle" aria-expanded="false" aria-controls="course-nav">수업 목록</button></header><div class="reader-grid"><nav id="course-nav" class="course-nav" aria-label="작성된 수업"><label for="lesson-search">수업 찾기</label><input id="lesson-search" type="search" placeholder="개념 또는 제목"><div class="course-links">{nav}</div><p>전체 과정 중 작성된 수업입니다. 전체 단원의 완성을 뜻하지 않습니다.</p></nav><main id="lesson" class="lesson"><header><p class="unit-name">{l['unit']}</p><h1>{title}</h1><a class="source-link" href="{origin.as_uri()}">Markdown 원문</a></header><article>{body}</article><nav class="pager" aria-label="수업 이동">{pager}</nav></main><aside class="reader-example">{aside(l,body)}</aside></div><script src="comparison.js"></script><script src="reader.js"></script></body></html>'''
    html=html.replace('<body>',f'<body class="view-b" data-lesson="{l["id"]}">')
    html=html.replace('</header><div class="reader-grid">','<button id="open-glossary">용어 찾기</button></header><div class="reader-grid">',1)
    html=html.replace('개편 중인 본문 · 선택한 B안','개념에서 원리와 적용까지')
    html=html.replace('aria-label="작성된 수업"','aria-label="학습 수업"')
    html=html.replace('전체 과정 중 작성된 수업입니다. 전체 단원의 완성을 뜻하지 않습니다.','기초·지식 구축·검색의 수업을 연결합니다. 논문 해설은 별첨에서 읽습니다.')
    html=html.replace('placeholder="개념 또는 제목"','placeholder="본문까지 검색"')
    html=html.replace(origin.as_uri(),'materials/'+l['path'])
    heads=re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',body)
    outline='<details class="inline-outline"><summary>수업 안에서 이동</summary>'+''.join('<a href="#'+i+'">'+t+'</a>' for i,t in heads)+'</details>'
    html=html.replace('<article>',outline+'<article>')
    controls='''<section class="study-note" aria-labelledby="note-title"><h2 id="note-title">내 말로 설명하기</h2><p>이 수업의 개념을 새 예로 설명하고, 아직 헷갈리는 점을 남겨 보세요.</p><textarea id="lesson-note" rows="6" aria-label="수업 메모"></textarea><div class="study-actions"><label><input type="checkbox" id="lesson-complete"> 학습 표시</label><label><input type="checkbox" id="lesson-bookmark"> 책갈피</label><button id="export-learning">기록 내려받기</button></div><p id="save-status" role="status">이 브라우저에 저장합니다.</p></section>'''
    html=html.replace('</article>','</article>'+controls)
    html=html.replace('<script src="reader.js">','<script src="search-index.js"></script><script src="glossary.js"></script><script src="reader.js">')
    (OUT/(l['id']+'.html')).write_text(html,encoding='utf-8')
    search.append({'id':l['id'],'title':l['title'],'text':re.sub('<[^>]+>',' ',body)})
(OUT/'search-index.js').write_text('window.LESSON_SEARCH='+json.dumps(search,ensure_ascii=False).replace('</','<\\/')+';',encoding='utf-8')
groups=[('Knowledge Graph와 지식 구축','문서에서 대상을 구분하고, 근거 있는 지식으로 연결합니다.',['U08','U09','U10','U11']),('Auto ontology','도메인 모델의 후보를 만들고 검토·개정하는 과정을 배웁니다.',['U12']),('RAG의 검색 구조와 평가','Vector·Graph·Tree의 중간 결과와 실패 원인을 비교합니다.',['U13','U14','U15','U16']),('별첨: 자동 KG 구축 survey','논문의 분류와 대표 접근을 사례로 따라 읽습니다.',['S01']),('기초를 다시 연결하기','그래프·RDF·ontology·추론을 필요한 위치에서 복습합니다.',['U01','U02','U03','U04','U05','U06','U07']),('운영과 반도체 통합 사례','변경·접근 정책을 유지하고 서로 다른 사례로 설명합니다.',['U17','U18'])]
sections=[]
for title,desc,ids in groups:
    selected=[l for l in lessons if l['unit'] in ids]
    if selected:sections.append('<section class="home-group" id="group-'+ids[0]+'"><h2>'+title+'</h2><p>'+desc+'</p><ol>'+''.join('<li><a href="'+l['id']+'.html">'+escape(l['title'])+'</a></li>' for l in selected)+'</ol></section>')
home='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>기업 지식 학습 교재</title><link rel="stylesheet" href="comparison.css"><link rel="stylesheet" href="reader.css"></head><body class="view-b"><header class="reader-header"><a href="index.html">기업 지식 학습 교재</a><span>의미를 설계하고, 근거를 연결하고, 필요한 지식을 찾기</span></header><main class="course-home"><header><p class="unit-name">학습 시작</p><h1>기업 지식이 만들어지고<br>답변의 근거가 되는 과정</h1><p class="home-intro">정의만 읽고 넘어가지 않도록, 원문과 데이터에서 시작해 중간 결과·비교·예외를 따라갑니다. 각 수업에서 설명을 읽고 예제를 대조한 뒤, 자신의 예로 다시 설명해 보세요.</p><a id="continue-learning" hidden>이어서 읽기</a></header><section class="home-search"><label for="home-search">개념이나 본문 내용 찾기</label><input id="home-search" type="search" placeholder="예: 동일 지시, community, 조건, 임베딩"><div id="home-results" aria-live="polite"></div></section>'''+''.join(sections)+'''<section class="home-records"><h2>학습 기록</h2><p>메모·책갈피·학습 표시는 이 브라우저에 저장됩니다. 이전 버전 기록도 덮어쓰지 않고 내려받을 수 있습니다.</p><button id="export-learning">기록 내려받기</button><p id="save-status" role="status"></p></section></main><script src="search-index.js"></script><script src="reader.js"></script></body></html>'''
quick='<nav class="course-jumps" aria-label="학습 영역 이동">'+''.join('<a href="#group-'+ids[0]+'">'+title+'</a>' for title,desc,ids in groups)+'</nav>'
home=home.replace('<section class="home-search">','<p class="reading-paths">처음부터 읽기: <a href="U01-L01.html">기업 지식과 그래프 기초</a> · 기초를 공부했다면: <a href="U08-L01.html">Knowledge Graph 구축부터</a></p>'+quick+'<section class="home-search">')
if (ROOT/'legacy-v1/index.html').exists():
    home=home.replace('<section class="home-records">','<section class="home-records"><p><a href="legacy/index.html">이전 버전 교재와 기록 보기</a></p>')
    home=home.replace('<script src="search-index.js">','<script>if(location.hash.startsWith("#/"))location.replace("legacy/index.html"+location.hash);</script><script src="search-index.js">')
(OUT/'index.html').write_text(home,encoding='utf-8')
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Built {len(lessons)} full lesson pages in {OUT}')
