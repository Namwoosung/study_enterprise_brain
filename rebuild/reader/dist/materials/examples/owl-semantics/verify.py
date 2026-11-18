"""Selected OWL-RL entailments only; not an OWL 2 DL consistency test."""
from pathlib import Path
import re, json
from rdflib import Graph, Namespace, RDF, OWL
from owlrl import DeductiveClosure, OWLRL_Semantics

course=Path(__file__).resolve().parents[2]
graph=Graph();count=0
for name in ['02-classes-relations-and-inference.md','03-quantifiers-and-cardinality.md']:
    for block in re.findall(r'```turtle\n(.*?)```',(course/'units/U06'/name).read_text(encoding='utf-8'),re.S):
        graph.parse(data=block,format='turtle');count+=1
ex=Namespace('https://example.org/owl-lesson/')
DeductiveClosure(OWLRL_Semantics).expand(graph)
checks={
    'subclass':(ex.J17,RDF.type,ex.Maintenance) in graph,
    'equivalent_class':(ex.J17,RDF.type,ex.PartChange) in graph,
    'subproperty':(ex.J17,ex.performedBy,ex.P1) in graph,
    'inverse':(ex.P1,ex.performs,ex.J17) in graph,
    'sameas_property':(ex.E01,ex.serial,next(graph.objects(ex.NE017,ex.serial))) in graph,
    'max_one_implies_equality':(ex.P1,OWL.sameAs,ex.P2) in graph,
}
assert all(checks.values()),checks
print(json.dumps({'turtle_blocks_parsed':count,'selected_OWL_RL_checks':checks,
 'limits':['No complete OWL 2 DL consistency engine','No live knowledge extraction','No real-world fact validation']},indent=2))
