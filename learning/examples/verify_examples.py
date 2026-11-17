"""Verify teaching examples; no Neo4j, LLM API, or production data access."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from importlib.metadata import version
import csv, json, math, sqlite3, sys
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal
from rdflib.namespace import XSD
from owlrl import DeductiveClosure, RDFS_Semantics, OWLRL_Semantics
from pyshacl import validate
sys.stdout.reconfigure(encoding="utf-8")
HERE=Path(__file__).resolve().parent
CASE=HERE.parent/"case"
EX=Namespace("https://example.org/fab/")
checks=[]
def ok(name, condition, detail=""):
    assert condition, name + ": " + detail
    checks.append(dict(name=name,status="PASS",detail=detail))
def table(name):
    with (CASE/name).open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def clone(g):
    h=Graph()
    for t in g:h.add(t)
    return h
eq=table("equipment.csv"); runs=table("runs.csv"); obs=table("observations.csv"); people=table("people.csv")
docs=json.loads((CASE/"documents.json").read_text(encoding="utf-8"))
dmap={d["id"]:d for d in docs}; rmap={r["id"]:r for r in runs}
emap={e["id"]:e for e in eq};pmap={p["id"]:p for p in people}
for rows in (eq,runs,obs,people):
    ok("unique IDs: "+rows[0]["id"],len({x["id"] for x in rows})==len(rows))
ok("table rows",sum(map(len,[eq,runs,obs,people]))==34)
manifest=json.loads((CASE/"manifest.json").read_text(encoding="utf-8"))
ok("snapshot includes all recorded runs",all(datetime.fromisoformat(r["occurred_at"])<=datetime.fromisoformat(manifest["snapshot"]) for r in runs))
ok("run foreign keys",all(r["equipment"] in emap and r["used_document"] in dmap and r["operator"] in pmap for r in runs))
ok("observation foreign keys",all(o["run"] in rmap for o in obs))
def valid_doc(d,equipment,at):
    t=datetime.fromisoformat(at)
    return d["kind"]=="procedure" and equipment in d["scope"] and datetime.fromisoformat(d["valid_from"])<=t and (not d["valid_to"] or t<datetime.fromisoformat(d["valid_to"]))
ok("all recorded procedures apply in synthetic baseline",all(valid_doc(dmap[r["used_document"]],r["equipment"],r["occurred_at"]) for r in runs))
boundary="2026-11-03T00:00:00+09:00"
ok("half-open version boundary",not valid_doc(dmap["D01"],"E01",boundary) and valid_doc(dmap["D02"],"E01",boundary))
at=rmap["RUN002"]["occurred_at"]
available=[d["id"] for d in docs if valid_doc(d,"E01",at) and datetime.fromisoformat(d["known_from"])<=datetime.fromisoformat(at)]
ok("late ingestion means no available valid E01 procedure",available==[],str(available))
def evidence_exists(ref):
    if "#" not in ref:return False
    src,key=ref.split("#",1)
    if src in dmap:return key in dmap[src]["paragraphs"]
    lookup={"equipment.csv":emap,"runs.csv":rmap,"observations.csv":{x["id"]:x for x in obs},"people.csv":pmap}
    return key in lookup.get(src,{})
claims=json.loads((CASE/"claims.json").read_text(encoding="utf-8"))
questions=json.loads((CASE/"questions.json").read_text(encoding="utf-8"))
ok("44 claims with existing evidence",len(claims)==44 and all(evidence_exists(c["source"]) for c in claims))
ok("18 questions evidence references",len(questions)==18 and all(evidence_exists(e) for q in questions for e in q["evidence"]))
ok("hypothesis remains distinct",claims[42]["epistemic"]=="hypothesis" and claims[43]["epistemic"]=="experience")
conn=sqlite3.connect(":memory:")
for name,rows in [("runs",runs),("equipment",eq)]:
    fields=list(rows[0])
    conn.execute('CREATE TABLE '+name+' ('+', '.join('"'+f+'" TEXT' for f in fields)+')')
    conn.executemany('INSERT INTO '+name+' VALUES ('+','.join('?' for _ in fields)+')',[[r[f] for f in fields] for r in rows])
sql="""SELECT r.id, r.lot, e.id AS equipment, r.occurred_at, r.used_document
FROM runs AS r JOIN equipment AS e ON e.id=r.equipment
WHERE r.lot='L02' ORDER BY r.occurred_at"""
rows=conn.execute(sql).fetchall()
ok("SQL L02 both events",[(r[0],r[2]) for r in rows]==[("RUN008","E03"),("RUN002","E01")],str(rows))
g=Graph().parse(HERE/"model.ttl",format="turtle")
shape=Graph().parse(HERE/"shapes.ttl",format="turtle")
result=list(g.query((HERE/"query.rq").read_text(encoding="utf-8")))
ok("SPARQL teaching subset",[(str(x[0]),str(x[1]),str(x[2])) for x in result]==[(str(EX.RUN002),str(EX.E01),str(EX.D02))])
inferred=clone(g);DeductiveClosure(RDFS_Semantics).expand(inferred)
ok("RDFS subclass inference",(EX.E01,RDF.type,EX.Equipment) in inferred and (EX.E01,RDF.type,EX.Equipment) not in g)
dom=clone(g);dom.add((EX.Something,EX.usedEquipment,EX.E01))
DeductiveClosure(RDFS_Semantics).expand(dom)
ok("domain infers a type",(EX.Something,RDF.type,EX.Run) in dom)
ow=Graph()
ow.add((EX.hasCanonical, RDF.type, OWL.ObjectProperty))
ow.add((EX.hasCanonical, RDF.type, OWL.FunctionalProperty))
ow.add((EX.record,EX.hasCanonical,EX.a));ow.add((EX.record,EX.hasCanonical,EX.b))
DeductiveClosure(OWLRL_Semantics).expand(ow)
ok("OWL RL functional property equality",(EX.a,OWL.sameAs,EX.b) in ow)
good,_,_=validate(g,shacl_graph=shape,inference="none")
ok("SHACL complete record",bool(good))
bad=clone(g);bad.remove((EX.RUN002,EX.usedDocument,None))
bad_ok,_,bad_report=validate(bad,shacl_graph=shape,inference="none")
ok("SHACL missing document rejected",not bad_ok and "MinCountConstraintComponent" in bad_report)
wrong=clone(g);wrong.remove((EX.RUN002,EX.usedDocument,None));wrong.add((EX.RUN002,EX.usedDocument,EX.D01))
wrong_ok,_,_=validate(wrong,shacl_graph=shape,inference="none")
ok("SHACL wrong-but-well-formed document passes",bool(wrong_ok))
ok("temporal check rejects wrong document",not valid_doc(dmap["D01"],"E01",at))
precision=18/20;recall=18/24;f1=2*precision*recall/(precision+recall)
ok("evaluation arithmetic",math.isclose(precision,.9) and math.isclose(recall,.75) and math.isclose(f1,9/11))
upper=1-.05**(1/100)
ok("zero-error illustrative upper bound",.029<upper<.030,str(upper))
ok("review queue arithmetic",1000*.10*3==300 and 240/3==80)
report={"date":datetime.now(timezone(timedelta(hours=9))).date().isoformat(),"environment":{"python":sys.version.split()[0],**{x:version(x) for x in ("rdflib","pyshacl","owlrl")}},
        "checks":checks,"not_executed":["Neo4j server/Cypher","NVIDIA Auto Ontology deployment","Microsoft GraphRAG pipeline","RAPTOR pipeline","LLM extraction or benchmark"],
        "scope":"Synthetic case consistency and small examples. Not real-world semantic correctness or full OWL DL conformance."}
(HERE/"verification_results.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"passed":len(checks),"environment":report["environment"]},ensure_ascii=False))
