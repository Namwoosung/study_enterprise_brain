"""Check scope, time correction, repeated executions and audience on the synthetic corpus."""
from pathlib import Path
from datetime import datetime
import json

data=json.loads((Path(__file__).parent/'corpus.json').read_text(encoding='utf-8'))
docs={doc['id']:doc for doc in data['documents']};tables=data['tables']
assert len(docs)==30 and len(tables)==7
assert len(set(asset['id'] for asset in tables['assets']))==2
assert len(set(asset['model'] for asset in tables['assets']))==1
work=tables['maintenance'][0]
before=[o['id'] for o in tables['observations'] if datetime.fromisoformat(o['at'])>datetime.fromisoformat(work['reported_end_r2'])]
after=[o['id'] for o in tables['observations'] if datetime.fromisoformat(o['at'])>datetime.fromisoformat(work['corrected_end_r3'])]
assert before==['O1','O2'] and after==[]
events={e['event']:e for e in tables['wafer_history']}
registrations={}
for check in tables['inspection']:
    event=events[check['event']]
    registrations[check['id']]=(check['image_count']>=3 if event['product']=='Blue' and event['date']>='2026-11-10' else None)
assert registrations=={'V31':False,'V32':True,'V33':None}
assert len({e['wafer'] for e in events.values()})==2
assert len({e['event'] for e in events.values() if e['wafer']=='L24/W01'})==2
report_access=set.intersection(*(set(docs[i]['access']) for i in ['C02','C05','C08']))
assert report_access=={'procurement'}
def approved_replacement(environment,adapter,version):
    return environment=='T1' and adapter=='AD1' and version=='4.2'
assert approved_replacement('T1','AD1','4.2')
assert not approved_replacement('T1','AD1','4.3')
assert not approved_replacement('production','AD1','4.2')
print(json.dumps({'documents':len(docs),'table_kinds':len(tables),'A_post_completion_r2':before,
 'A_post_completion_r3':after,'B_file_requirements':registrations,'C_combined_audience':sorted(report_access),
 'C_approval_scope_checks':3,'limits':['Synthetic policy arithmetic only','No extraction model, graph engine or production authorization implementation']},indent=2))
