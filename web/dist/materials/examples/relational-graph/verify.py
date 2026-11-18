"""Run the published SQL on its synthetic fixture, without claiming Cypher execution."""
from pathlib import Path
import sqlite3, re, json
root = Path(__file__).resolve().parents[2]
source = (root/'units/U02/01-same-question-two-models.md').read_text(encoding='utf-8')
db = sqlite3.connect(':memory:')
db.executescript('CREATE TABLE Person(id TEXT,name TEXT,team_id TEXT);CREATE TABLE Team(id TEXT,name TEXT,manager_id TEXT);CREATE TABLE Document(id TEXT,author_id TEXT,approver_id TEXT);')
db.executemany('INSERT INTO Person VALUES(?,?,?)',[('P1','민수','T1'),('P2','지연','T1'),('P3','현우','T2')])
db.executemany('INSERT INTO Team VALUES(?,?,?)',[('T1','정비팀','P2'),('T2','검사팀','P3')])
db.executemany('INSERT INTO Document VALUES(?,?,?)',[('D1','P1','P2'),('D2','P1','P3')])
query = re.search(r'```sql\n(.*?)\n```',source,re.S)[1]
out = db.execute(query).fetchall()
assert out == [('D1','민수','지연')]
report={'engine':'sqlite3 '+sqlite3.sqlite_version,'query_source':'units/U02/01-same-question-two-models.md','rows':out,'limits':['Cypher not executed','Not a performance benchmark']}
(Path(__file__).parent/'sql-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
