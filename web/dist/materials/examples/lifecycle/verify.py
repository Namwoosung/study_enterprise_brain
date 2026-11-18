"""Selected time and dependency-policy examples; not a production data lifecycle engine."""
from pathlib import Path
from datetime import datetime
import re,json
from rdflib import Graph,Namespace,RDF
course=Path(__file__).resolve().parents[2]
source=(course/'units/U17/01-time-versions-and-provenance.md').read_text(encoding='utf-8')
g=Graph()
for block in re.findall(r'```turtle\n(.*?)```',source,re.S):g.parse(data=block,format='turtle')
ex=Namespace('https://example.org/lifecycle/');prov=Namespace('http://www.w3.org/ns/prov#')
assert (ex.C12,prov.wasDerivedFrom,ex['M-v2']) in g
assert (ex.X5,prov.wasAssociatedWith,ex['Extractor-v3']) in g
times=[datetime.fromisoformat('2026-11-19T'+t+':00+09:00') for t in ['09:00','09:03','09:20','09:24']]
segments=[int((b-a).total_seconds()/60) for a,b in zip(times,times[1:])]
assert segments==[3,17,4] and sum(segments)==24
supports={'Q':{'D1','D2'},'R':{'D3'}}
active_sources={'D2'}
valid={claim for claim,evidence in supports.items() if evidence & active_sources}
assert valid=={'Q'}
assert not {'Q','R'} <= valid # summary that used both inputs must be reconsidered
print(json.dumps({'PROV_triples':len(g),'minutes':segments,'end_to_end':24,'alternative_support_survives':True,
 'combined_summary_requires_rebuild':True,'limits':['Toy policy, not an access-control implementation']}))
