"""Verify only the executable claims of the proposed teaching sample."""
from pathlib import Path
import re,json,sqlite3
from rdflib import Graph,Namespace
from rdflib.compare import isomorphic
root=Path(__file__).resolve().parent
source=(root.parent.parent/"units/U04/02-events-and-property-graphs.md").read_text(encoding="utf-8")
blocks=re.findall(r"~~~turtle\n(.*?)\n~~~",source,re.S)
graphs=[Graph().parse(data=b,format="turtle") for b in blocks]
checks=[]
def check(label,ok):
    assert ok,label
    checks.append(label)
check("One direct relation is one triple",len(graphs[0])==1)
check("Repeating the identical triple does not encode three events",len(graphs[1])==1)
check("One event has six triples in the selected model",len(graphs[2])==6)
check("Three events have eighteen triples",len(graphs[3])==18)
ex=Namespace("https://example.org/driving/")
g=graphs[3]
for name,km,persons in [("drive1",12,2),("drive2",18,1),("drive3",9,3)]:
    d=ex[name]
    check(name+" retains participant and measurements",
          g.value(d,ex.driver)==ex.Minsu and g.value(d,ex.vehicle)==ex.CarA
          and int(g.value(d,ex.distanceKm))==km and int(g.value(d,ex.passengers))==persons)
q=re.search(r"~~~sparql\n(.*?)\n~~~",source,re.S)[1]
row=list(g.query(q))[0]
check("Published SPARQL returns three events and 39km",tuple(map(int,row))==(3,39))
xml=re.search(r"~~~xml\n(.*?)\n~~~",source,re.S)[1]
check("Turtle and RDF/XML encode the same graph",isomorphic(graphs[0],Graph().parse(data=xml,format="xml")))
db=sqlite3.connect(":memory:")
db.execute("CREATE TABLE Person (id TEXT PRIMARY KEY)")
db.execute("CREATE TABLE Car (id TEXT PRIMARY KEY)")
db.execute("CREATE TABLE Drive (drive_id TEXT PRIMARY KEY, person_id TEXT REFERENCES Person(id), car_id TEXT REFERENCES Car(id), started_at TEXT, distance_km INTEGER, passengers INTEGER)")
db.execute("INSERT INTO Person VALUES ('Minsu')")
db.execute("INSERT INTO Car VALUES ('CarA')")
rows=[("drive1","Minsu","CarA","2026-11-01T09:00:00+09:00",12,2),("drive2","Minsu","CarA","2026-11-01T14:00:00+09:00",18,1),("drive3","Minsu","CarA","2026-11-02T10:00:00+09:00",9,3)]
db.executemany("INSERT INTO Drive VALUES (?,?,?,?,?,?)",rows)
sql=re.search(r"~~~sql\n(.*?)\n~~~",source,re.S)[1]
out=db.execute(sql).fetchall()
check("Published SQL preserves three ordered events",out==[(r[0],r[3],r[4],r[5]) for r in rows])
check("Relational and RDF aggregation agree",db.execute("SELECT COUNT(*),SUM(distance_km) FROM Drive").fetchone()==(3,39))
report={"checks":checks,"passed":len(checks),"limits":["Cypher was not executed on Neo4j.","These checks do not establish learner comprehension or approve a design."]}
(root/"sample_verification.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
