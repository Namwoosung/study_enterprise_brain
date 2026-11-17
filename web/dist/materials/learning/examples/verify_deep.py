"""Executable counterexamples for deep chapters. No production data or LLM calls."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,math
from rdflib import Graph,Namespace,RDF,RDFS
from pyshacl import validate
EX=Namespace("https://example.org/deep/")
PREFIX="@prefix ex: <https://example.org/deep/> . @prefix sh: <http://www.w3.org/ns/shacl#> . "
checks=[]
def check(name,value):
    assert value,name
    checks.append({"name":name,"status":"PASS"})
def conforms(data,shape,inference="none"):
    return bool(validate(data,shacl_graph=Graph().parse(data=PREFIX+shape,format="turtle"),inference=inference)[0])
g=Graph();g.add((EX.r,EX.forLot,EX.l))
base="ex:S a sh:NodeShape; TARGET; sh:property [sh:path ex:usedDocument;sh:minCount 1]."
check("targetClass can miss an untyped record",conforms(g,base.replace("TARGET","sh:targetClass ex:Run")))
check("targetSubjectsOf detects missing field",not conforms(g,base.replace("TARGET","sh:targetSubjectsOf ex:forLot")))
g=Graph();g.add((EX.r,EX.usedEquipment,EX.e));g.add((EX.usedEquipment,RDFS.range,EX.Equipment))
shape="ex:S a sh:NodeShape;sh:targetNode ex:r;sh:property [sh:path ex:usedEquipment;sh:class ex:Equipment]."
check("range alone without inference fails class check",not conforms(g,shape))
check("RDFS range inference changes class result",conforms(g,shape,"rdfs"))
g=Graph();g.add((EX.r,EX.usedEquipment,EX.e));g.add((EX.e,RDF.type,EX.InspectionTool));g.add((EX.InspectionTool,RDFS.subClassOf,EX.Equipment))
check("SHACL class honors subclass path without general inference",conforms(g,shape))
check("candidate and conditional matching recall",math.isclose(.92*.9,.828))
edges=[("A","B"),("B","C")];seen={"A"}
while True:
    new=seen|{b for a,b in edges if a in seen}|{a for a,b in edges if b in seen}
    if new==seen:break
    seen=new
check("connected components can bridge unlike endpoints",seen=={"A","B","C"})
# New independently tested examples are appended before the report in later batches.
report={"date":datetime.now(timezone(timedelta(hours=9))).date().isoformat(),"checks":checks,"scope":"Synthetic counterexamples; not a full OWL DL reasoner, trained ER model, or performance benchmark."}
Path(__file__).with_name("deep_verification_results.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"passed":len(checks)},ensure_ascii=False))
