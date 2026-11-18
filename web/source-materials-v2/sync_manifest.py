"""Register written lessons with stable filename-based IDs; do not infer readiness."""
from pathlib import Path
import json
root = Path(__file__).resolve().parent
path = root/'manifest.json'
manifest = json.loads(path.read_text(encoding='utf-8'))
for unit in manifest['units']:
    lessons=[]
    for p in sorted((root/'units'/unit['id']).glob('[0-9][0-9]-*.md')):
        title=next(line[2:] for line in p.read_text(encoding='utf-8').splitlines() if line.startswith('# '))
        lessons.append({'id':unit['id']+'-L'+p.name[:2], 'title':title, 'path':p.relative_to(root).as_posix()})
    unit['lessons']=lessons
path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'written_lessons':sum(len(u['lessons']) for u in manifest['units']), 'readiness':'managed separately in rebuild/STATE.json'}))
