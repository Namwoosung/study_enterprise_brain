"""Verify the published language and context lesson examples, not learning outcomes."""
from pathlib import Path
import re, json
from rdflib import Graph, Dataset, Namespace
from rdflib.compare import isomorphic

root = Path(__file__).resolve().parents[2]
unit = root / 'units/U04'
source = (unit / '01-rdf-language.md').read_text(encoding='utf-8')
blocks = re.findall(r'```turtle\n(.*?)\n```', source, re.S)
graphs = [Graph().parse(data=b, format='turtle') for b in blocks]
assert [len(g) for g in graphs] == [1,1,1,2,1,1,1,3,2,3,1,4]
xml = re.search(r'```xml\n(.*?)\n```', source, re.S)[1]
ld = re.search(r'```json\n(.*?)\n```', source, re.S)[1]
assert isomorphic(graphs[0], Graph().parse(data=xml, format='xml'))
assert isomorphic(graphs[0], Graph().parse(data=ld, format='json-ld'))
context = (unit / '03-statements-and-context.md').read_text(encoding='utf-8')
gs = [Graph().parse(data=b, format='turtle') for b in re.findall(r'```turtle\n(.*?)\n```', context, re.S)]
ex = Namespace('https://example.org/fab/')
assert (ex.E01, ex.usesPart, ex.P7) not in gs[2]
ds = Dataset().parse(data=re.search(r'```trig\n(.*?)\n```', context, re.S)[1], format='trig')
query = re.search(r'```sparql\n(.*?)\n```', context, re.S)[1]
assert list(ds.query(query)) == [(ex.graphR17, ex.P7)]
report = {
    'checks': ['12 Turtle examples parse with expected triple counts',
               'Turtle/RDFXML/JSONLD encode the same graph',
               'Reification example does not contain the original asserted triple',
               'Named graph query returns graphR17 and P7'],
    'limits': ['No Neo4j run', 'No RDF1.2 execution', 'No human learning outcome measurement']
}
(Path(__file__).parent / 'language-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
