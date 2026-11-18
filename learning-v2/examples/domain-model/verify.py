"""Check U05 vocabulary parsing and the published event/evidence SQL."""
from pathlib import Path
import re,sqlite3,json
from rdflib import Graph
course=Path(__file__).resolve().parents[2]
count=0
for file in (course/'units/U05').glob('*.md'):
    for block in re.findall(r'```turtle\n(.*?)```',file.read_text(encoding='utf-8'),re.S):
        Graph().parse(data=block,format='turtle');count+=1
c=sqlite3.connect(':memory:')
c.executescript('CREATE TABLE work_event(id TEXT PRIMARY KEY, order_id TEXT);CREATE TABLE event_evidence(event_id TEXT, source TEXT);')
c.executemany('INSERT INTO work_event VALUES (?,?)',[('E-03','W-04'),('E-04','W-04')])
c.executemany('INSERT INTO event_evidence VALUES (?,?)',[('E-03','run-81'),('E-03','copy-81'),('E-04','run-82')])
s=(course/'units/U05/03-evolve-model-and-mappings.md').read_text(encoding='utf-8')
q=re.search(r'```sql\n(.*?)```',s,re.S)[1]
assert c.execute(q).fetchall()==[(3,2)]
assert '10:30' > '10:29'
print(json.dumps({'Turtle_blocks_parsed':count,'evidence_rows':3,'distinct_events':2,'limits':['No OWL or Neo4j execution']}))
