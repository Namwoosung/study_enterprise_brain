"""Build a portable static learning site from the approved Markdown corpus."""
from pathlib import Path
import csv,html,json,re,shutil
import markdown
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/"source-materials"
LIVE=ROOT.parent
if (LIVE/"learning/M1_problem.md").exists():
    shutil.copytree(LIVE/"learning",SOURCE/"learning",dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__"))
    for name in ("README.md","LEARNING_PLAN.md","SOURCES.md"):
        shutil.copy2(LIVE/name,SOURCE/name)
OUT=ROOT/"dist"
OUT.mkdir(exist_ok=True)
shutil.copytree(SOURCE,OUT/"materials",dirs_exist_ok=True)
for name in ("index.html","styles.css","app.js"):
    shutil.copy2(ROOT/name,OUT/name)
meta=[
("문제에서 출발하기","자료가 많은데, 왜 답은 어려울까?","Enterprise Brain과 조직 지식의 요구를 구분합니다.","흩어진 기록",["Enterprise Brain","Second Brain","Knowledge Graph"]),
("지식의 모양 정하기","이름을 연결하면 지식이 될까?","개체·사건·의미를 표현하고 질의합니다.","의미와 모델",["Ontology","RDF / OWL","Neo4j"]),
("자료에서 지식 얻기","문서·DB·경험에서 무엇을 얻을까?","매핑·추출·지식 도출의 차이를 배웁니다.","수집과 추출",["R2RML","정보 추출","암묵지"]),
("같은 대상을 연결하기","비슷한 이름은 같은 장비일까?","식별·충돌·자동 모델 생성의 범위를 판단합니다.","식별과 통합",["Entity resolution","Auto ontology"]),
("믿고 사용할 조건 찾기","검증을 통과하면 사실일까?","검사 범위와 사람의 검토 정책을 구분합니다.","검증과 검토",["SHACL","근거","품질 평가"]),
("변화 속에서 유지하기","어제 맞던 답은 오늘도 맞을까?","시점·출처·갱신·권한의 연결을 이해합니다.","변경과 운영",["PROV","버전","권한"]),
("근거를 찾아 답하기","검색 구조는 답을 어떻게 바꿀까?","Vector·Graph·Tree가 구성하는 근거를 비교합니다.","검색과 활용",["Vector RAG","Graph RAG","Tree RAG"]),
("내 언어로 설명하기","어떤 구성을 선택하고 설명할까?","한 사건을 끝까지 따라가며 대안을 설명합니다.","종합과 설명",["설계 비교","설명 연습"])
]
paths=sorted((SOURCE/"learning").glob("M[1-8]_*.md"))+sorted((SOURCE/"learning/deep").glob("D[1-9]_*.md"))+sorted((SOURCE/"learning/concepts").glob("C[0-9][0-9]_*.md"))
deep_meta={m["id"]:m for m in json.loads((SOURCE/"learning/deep/manifest.json").read_text(encoding="utf-8"))}
concept_meta={m["id"]:m for m in json.loads((SOURCE/"learning/concepts/manifest.json").read_text(encoding="utf-8"))}
def chapter_key(p):
    prefix=p.stem.split("_")[0].lower()
    return prefix[0]+str(int(prefix[1:]))
pathmap={p.relative_to(SOURCE).as_posix():chapter_key(p) for p in paths}
resources={"learning/GLOSSARY.md":"glossary","learning/EVIDENCE.md":"evidence","SOURCES.md":"sources","learning/case/README.md":"case-guide","learning/examples/README.md":"examples","LEARNING_PLAN.md":"plan","learning/README.md":"guide","learning/CONTENT_MAP.md":"content-map","README.md":"project"}
resources.update({"learning/deep/README.md":"deep-guide","learning/deep/RESEARCH.md":"deep-research"})
resources.update({"learning/concepts/README.md":"concept-guide","learning/concepts/RESEARCH.md":"concept-research"})

def convert_links(s,origin):
    def link(m):
        url=html.unescape(m[1])
        if url.startswith(("http:","https:","mailto:")):
            return 'href="'+html.escape(url,quote=True)+'" target="_blank" rel="noopener noreferrer"'
        raw,_,frag=url.partition("#")
        p=(origin.parent/raw).resolve() if raw else origin.resolve()
        try:key=p.relative_to(SOURCE.resolve()).as_posix()
        except ValueError:return m[0]
        if key in pathmap: dest="#/learn/"+pathmap[key]+("/"+frag if re.fullmatch(r"[mdc]\d+-\d\d",frag) else "")
        elif key=="learning/case/CORPUS.md":dest="#/case/"+(frag.upper() if frag else "D01")
        elif key in resources:dest="#/resource/"+resources[key]
        else:dest="materials/"+key+("#"+frag if frag else "")
        return 'href="'+html.escape(dest,quote=True)+'"'
    return re.sub(r'href="([^"]*)"',link,s)
def diagram(m):
    txt=m[1];nodes={};edges=[]
    for key,label in re.findall(r'(\w+)\["?([^"\]]+)"?\]',txt):nodes[key]=label
    for line in txt.splitlines()[1:]:
        clean=re.sub(r'\["?[^"\]]+"?\]',"",line.strip())
        found=re.match(r'(\w+)\s*(-->|---)(?:\|"([^"]+)"\|)?\s*(\w+)',clean)
        if found:
            a,arrow,label,b=found.groups()
            edges.append('<li><span>'+html.escape(nodes.get(a,a))+'</span><i>'+html.escape(label or ("연결" if arrow=="---" else "→"))+'</i><span>'+html.escape(nodes.get(b,b))+'</span></li>')
    return '<figure class="relation-figure"><figcaption>관계를 따라 읽기</figcaption><ul>'+"".join(edges)+'</ul></figure>'
def render(text,path):
    text=re.sub(r'~~~mermaid\s*\n(.*?)\n~~~',diagram,text,flags=re.S)
    result=markdown.markdown(text,extensions=["tables","fenced_code","sane_lists"])
    result=convert_links(result,path)
    result=re.sub(r'(<h3>해설</h3>)(.*?)(?=<p><strong>3분 설명|<h2>|<h3>|$)',lambda m:'<details class="answer"><summary>해설 확인하기</summary>'+m[2]+"</details>",result,flags=re.S)
    result=result.replace("<table>","<div class=\"table-scroll\" tabindex=\"0\"><table>").replace("</table>","</table></div>")
    return result
chapters=[];coverage=[]
for i,p in enumerate(paths):
    chapter_id=chapter_key(p)
    text=p.read_text(encoding="utf-8")
    matches=list(re.finditer(r'<a id="([mdc]\d+-\d\d)"></a>',text))
    sections=[]
    for n,m in enumerate(matches):
        body=text[m.end():matches[n+1].start() if n+1<len(matches) else len(text)].strip()
        heading=re.search(r'^## (.+)$',body,re.M)
        title=re.sub(r'^\d+\.\s*',"",heading[1]) if heading else "정리"
        body=body[:heading.start()]+body[heading.end():] if heading else body
        # Preserve every section, including final exercises and optional depth.
        section={"id":m[1],"title":title,"html":render(body,p),"text":re.sub(r'<[^>]+>'," ",render(body,p))}
        sections.append(section)
        coverage.append({"id":m[1],"source":p.relative_to(SOURCE).as_posix(),"route":f"#/learn/{chapter_id}/{m[1]}","characters":len(body)})
    intro=text[:matches[0].start()]
    goal=re.search(r'(?:> 학습 목표:|\*\*목표:\*\*)(.+)',intro)
    intro_extra="\n".join(line for line in intro.splitlines() if not line.startswith(("# ","[","> 학습 목표:","**목표:**"))).strip()
    info=concept_meta[chapter_id] if chapter_id.startswith("c") else deep_meta[chapter_id] if chapter_id.startswith("d") else dict(title=meta[i][0],question=meta[i][1],description=meta[i][2],phase=meta[i][3],tags=meta[i][4])
    chapter=dict(info)
    chapter.update(id=chapter_id,number=int(chapter_id[1:]),level="concept" if chapter_id.startswith("c") else "deep" if chapter_id.startswith("d") else "foundation",goal=goal[1].strip() if goal else info["description"],intro_html=render(intro_extra,p),file=p.relative_to(SOURCE/"learning").as_posix(),sections=sections)
    chapters.append(chapter)
docs=json.loads((SOURCE/"learning/case/documents.json").read_text(encoding="utf-8"))
tables={}
for name in ("equipment","people","runs","observations"):
    with (SOURCE/f"learning/case/{name}.csv").open(encoding="utf-8",newline="") as f:tables[name]=list(csv.DictReader(f))
data=dict(chapters=chapters,documents=docs,tables=tables,claims=json.loads((SOURCE/"learning/case/claims.json").read_text(encoding="utf-8")),questions=json.loads((SOURCE/"learning/case/questions.json").read_text(encoding="utf-8")),resources={k:{"title":(SOURCE/p).read_text(encoding="utf-8").splitlines()[0].lstrip("# "),"html":render((SOURCE/p).read_text(encoding="utf-8"),SOURCE/p)} for p,k in resources.items()},coverage=coverage)
(OUT/"content.js").write_text("window.COURSE = "+json.dumps(data,ensure_ascii=False)+";\n",encoding="utf-8")
(ROOT/"coverage.json").write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
assert len([x for x in coverage if x["id"].startswith("m")])==54
assert len([c for c in chapters if c["level"]=="deep"])==len(deep_meta)
assert len([c for c in chapters if c["level"]=="concept"])==len(concept_meta)
assert len(docs)==14
print(json.dumps({"chapters":len(chapters),"sections":len(coverage),"documents":len(docs),"resources":len(resources)},ensure_ascii=False))
