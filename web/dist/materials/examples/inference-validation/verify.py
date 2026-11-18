"""Execute RDFS/SHACL comparisons from U06, without claiming full OWL reasoning."""
from pathlib import Path
import re, json
from rdflib import Graph, Namespace, RDF
from owlrl import DeductiveClosure, RDFS_Semantics
from pyshacl import validate

root = Path(__file__).resolve().parents[2]
text=(root/'units/U06/01-inference-and-validation.md').read_text(encoding='utf-8')
blocks=re.findall(r'```turtle\n(.*?)\n```',text,re.S)
graphs=[Graph().parse(data=b,format='turtle') for b in blocks]
assert len(graphs)==5
ex=Namespace('https://example.org/check/')
sh=Namespace('http://www.w3.org/ns/shacl#')
data=graphs[0]+graphs[1]
inferred=Graph()+data
DeductiveClosure(RDFS_Semantics).expand(inferred)
assert (ex.J17,RDF.type,ex.Maintenance) in inferred
assert not list(inferred.objects(ex.J17,ex.performedBy))
wrong=graphs[1]+graphs[3]
DeductiveClosure(RDFS_Semantics).expand(wrong)
assert (ex.M17,RDF.type,ex.Person) in wrong

def run(g,inference):
    conforms,report,_=validate(g,shacl_graph=graphs[4],inference=inference)
    return {'conforms':bool(conforms),'components':sorted(set(str(c).split('#')[-1] for c in report.objects(None,sh.sourceConstraintComponent)))}

missing=run(data,'none')
assert missing=={'conforms':False,'components':['MinCountConstraintComponent']}
typed=Graph()+data
typed.add((ex.J17,ex.performedBy,ex.P1));typed.add((ex.P1,RDF.type,ex.Person))
assert run(typed,'none')['conforms']
untyped=Graph()+data
untyped.add((ex.J17,ex.performedBy,ex.P1))
before=run(untyped,'none');after=run(untyped,'rdfs')
assert before=={'conforms':False,'components':['ClassConstraintComponent']}
assert after['conforms']
report={'missing_performer':missing,'typed_performer':run(typed,'none'),'untyped_before_inference':before,'untyped_after_rdfs':after,'range_infers_manual_as_person':True,'limits':['Not full OWL consistency verification','Not verification of real work performer','Synthetic data only']}
(Path(__file__).parent/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
