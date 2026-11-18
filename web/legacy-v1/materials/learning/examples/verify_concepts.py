from pathlib import Path
import re,json,math
from rdflib import Graph,Namespace
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name,ok):
    assert ok,name
    checks.append(name)
rdf=(ROOT/"concepts/C05_rdf.md").read_text(encoding="utf-8")
blocks=re.findall(r"~~~turtle\n(.*?)\n~~~",rdf,re.S)
for n,b in enumerate(blocks):
    g=Graph().parse(data=b,format="turtle")
    check(f"Turtle block {n+1} parses",len(g)>0)
g=Graph().parse(data=blocks[1],format="turtle")
check("RUN002 example contains exactly four triples",len(g)==4)
g.parse(data=blocks[1].replace("RUN002","RUN008").replace("E01","E03").replace("D02","D04"),format="turtle")
query=re.search(r"~~~sparql\n(.*?)\n~~~",(ROOT/"concepts/C09_query_reading.md").read_text(encoding="utf-8"),re.S)[1]
short=lambda x:str(x).rsplit("/",1)[-1]
rows=[tuple(short(x) for x in row) for row in g.query(query)]
check("Published SPARQL returns the two stated rows",rows==[("RUN002","E01","D02"),("RUN008","E03","D04")])
ex=Namespace("https://example.org/fab/")
g.remove((ex.RUN008,ex.usedDocument,ex.D04))
check("Mandatory document pattern excludes undocumented run",len(list(g.query(query)))==1)
optional=query.replace("ex:usedEquipment ?equipment ;\n       ex:usedDocument ?document .","ex:usedEquipment ?equipment .\n  OPTIONAL { ?run ex:usedDocument ?document . }")
rows=list(g.query(optional))
check("OPTIONAL retains undocumented run with unbound document",len(rows)==2 and any(r.document is None for r in rows))
check("Cosine orthogonal and aligned unit vectors",math.isclose(math.cos(math.pi/2),0,abs_tol=1e-12) and math.cos(0)==1)
retrieved={"A","B","X","Y"};gold={"A","B","C"}
check("Precision and recall use different denominators",len(gold&retrieved)/len(retrieved)==.5 and math.isclose(len(gold&retrieved)/len(gold),2/3))
check("Accepted error rate is conditional on coverage",math.isclose(2/90,.022222222222222222))
check("Review capacity and backlog example",240//3==80 and 100-240//3==20)
meta=json.loads((ROOT/"concepts/manifest.json").read_text(encoding="utf-8"))
check("All fourteen concept chapters present",len(meta)==14)
for m,p in zip(meta,sorted((ROOT/"concepts").glob("C[0-9][0-9]_*.md"))):
    s=p.read_text(encoding="utf-8")
    anchors=re.findall(r'<a id="([^"]+)"></a>',s)
    check(m["id"]+" has ordered sections, sources and self-check",anchors==[f'{m["id"]}-{i:02}' for i in range(1,len(anchors)+1)] and len(anchors)>=6 and "https://" in s and "### 해설" in s and "생략 가능" in s)
report={"passed":len(checks),"checks":checks,"scope":"Synthetic RDF/SPARQL and arithmetic checks; no Neo4j server, LLM benchmark, or production pipeline execution."}
Path(__file__).with_name("concept_verification_results.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
