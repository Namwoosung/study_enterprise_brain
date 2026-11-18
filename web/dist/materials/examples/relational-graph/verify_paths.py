"""Run the published recursive CTE, including its explicit cycle counterexample."""
from pathlib import Path
import re, sqlite3, json
course=Path(__file__).resolve().parents[2]
source=(course/'units/U02/02-variable-paths-and-query-work.md').read_text(encoding='utf-8')
query=re.search(r'```sql\n(.*?)```',source,re.S)[1]
c=sqlite3.connect(':memory:')
c.execute('CREATE TABLE Contains(parent TEXT, child TEXT)')
c.executemany('INSERT INTO Contains VALUES (?,?)',[
    ('A','P'),('B','P'),('X','A'),('X','B'),('Z','X'),('Y','Q')])
assert c.execute(query).fetchall()==[('A',),('B',),('X',),('Z',)]
c.execute("INSERT INTO Contains VALUES ('P','Z')")
assert c.execute(query).fetchall()==[('A',),('B',),('P',),('X',),('Z',)]
assert 3+9+3==15 and 1+3+3+1==8 and 3*3*1==9
print(json.dumps({'engine':'SQLite '+sqlite3.sqlite_version,'ancestors':['A','B','X','Z'],
 'cycle_terminates_but_includes_self':True,'layered_example':{'nodes':8,'edges':15,'paths':9},
 'limits':['No Neo4j run','No performance measurement']}))
