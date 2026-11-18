"""Execute all published U07 SPARQL examples on one declared synthetic dataset."""
from pathlib import Path
import re, json
from rdflib import Dataset, Namespace, RDF, Literal, URIRef

course=Path(__file__).resolve().parents[2]
ds=Dataset();g=ds.default_graph;ex=Namespace('https://example.org/query/')
files=sorted((course/'units/U07').glob('*.md'))
for file in files:
    for block in re.findall(r'```turtle\n(.*?)```',file.read_text(encoding='utf-8'),re.S):g.parse(data=block,format='turtle')
for work,equipment,minutes in [(ex.J1,ex.E01,10),(ex.J2,ex.E01,20),(ex.J3,ex.E02,10)]:
    g.add((work,RDF.type,ex.Work));g.add((work,ex.equipment,equipment));g.add((work,ex.minutes,Literal(minutes)))
g.add((ex.J2,ex.performedBy,ex.P1))
for work,report in [(ex.J1,ex.D1a),(ex.J1,ex.D1b),(ex.J2,ex.D2)]:g.add((work,ex.report,report))
for name in [ex.r1,ex.r2]:ds.graph(name).add((ex.J1,ex.equipment,ex.E01))
person_name=str(next(g.objects(ex.P1,ex.name)))
expected=[
    [('J1',person_name),('J2',person_name)],[('J2',20)],[(2,1)],
    [('J1','P1'),('J2','P1')],
    [('J1','P1'),('J2','P1'),('J3',None)],
    [('J1','P1'),('J2','P1'),('J3',None)],
    [('J1',10,'D1a'),('J1',10,'D1b'),('J2',20,'D2'),('J3',10,None)],
    [(3,40)],[('E01',2,30),('E02',1,10)],
    [('A',),('B',),('X',),('Z',)],[('r1',),('r2',)]
]
def normalize(x):
    if x is None:return None
    if isinstance(x,URIRef):return str(x).removeprefix(str(ex))
    return x.toPython()
results=[]
for file in files:
    for query in re.findall(r'```sparql\n(.*?)```',file.read_text(encoding='utf-8'),re.S):
        rows=[tuple(normalize(x) for x in row) for row in ds.query(query)]
        assert rows==expected[len(results)],(file.name,len(results),rows,expected[len(results)])
        results.append({'lesson':file.stem,'rows':len(rows)})
assert len(results)==11
print(json.dumps({'SPARQL_examples_executed':results,'limits':['No Neo4j execution','Not complete language conformance tests']},indent=2))
