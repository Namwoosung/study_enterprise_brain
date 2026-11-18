# U04 조사와 검토 기록

확인일: 2026-11-18. 전체 규격을 정독·구현했다는 기록이 아니다. 아래 해당 설명의 원문 절을 열어 확인하고, 교재의 합성 예제로 적용했다.

| 근거 | 확인한 내용/범위 | 적용 위치 |
|---|---|---|
| [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/) | §1.1~1.8, §3의 term/그래프 정의, §4 dataset, §5 datatype | L01 식별/값/모델, L02 집합과 사건, L03 문맥 |
| [Turtle](https://www.w3.org/TR/turtle/) | §2.1~2.6의 triple·prefix·a·literal·blank node | L01 문법 예제 |
| [RDFS](https://www.w3.org/TR/rdf-schema/) | §3.3~3.6, §5.3 | L01 type/label, L03 reification |
| [RDF Primer](https://www.w3.org/TR/rdf11-primer/) | 문서 상태, 목차와 도입; 이전 표본의 직렬화 비교를 규격으로 추가 대조 | 입문 맥락, Note 지위 |
| [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/) | §2.2~2.6 기본 노드/속성/문서 표현 | L01의 최소 XML을 파싱 확인 |
| [JSON-LD1.1](https://www.w3.org/TR/json-ld11/) | basic concepts와 node reference/context 용어 | L01 최소 context/id 예제 |
| [n-ary relations](https://www.w3.org/TR/swbp-n-aryRelations/) | general issues, relation instance pattern1, reification과 구분 | L02 사건의 개체화. WG Note임 |
| [Neo4j concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) | introduction, nodes/labels/relationships/properties | L02 관계 속성 비교, 제품 모델 범위 |
| [RDF semantics](https://www.w3.org/TR/rdf11-mt/#reification) | D.1 reification, 원진술과의 entailment 구분 | L03 진술 채택과 설명의 구분 |
| [TriG](https://www.w3.org/TR/trig/) | §2 triple/graph statements | L03 dataset 예제 |
| [SPARQL1.1](https://www.w3.org/TR/sparql11-query/#rdfDataset) | §13 dataset/GRAPH | L03 source별 질의 |
| [RDF1.2 Concepts 고정판](https://www.w3.org/TR/2026/CRD-rdf12-concepts-20261116/) | 문서 상태와 abstract의 triple term/object 설명 | L03 후속 버전 경계, CRD 확인 |

## 실행과 해석

RDFLib로 L01의 12개 Turtle 블록을 파싱했다. 같은 한 트리플의 XML/JSON-LD 동등성은 isomorphic으로 확인했다. L03 TriG의 GRAPH 질의는 graphR17/P7을 반환했다. L02는 별도 verify.py에서 18 triple·3사건·39km와 SQL 결과를 확인했다. Cypher 엔진과 RDF1.2 구현은 실행하지 않았다.

‘reification 데이터에 원 트리플이 없다’는 프로그램 확인은 entailment 이론 전체를 테스트한 것이 아니다. 원 진술을 자동 함의하지 않는 의미는 규격 D.1을 근거로 한다.

## 설명 검토와 남은 일

- 처음 나오는 ex/rdf/rdfs/xsd, type/class/instance, ;/,/^^/@ko를 설명 위치와 연결했다.
- 사건 횟수와 문서 주장 횟수를 구분하는 반례를 추가했다.
- 18개 트리플은 선택한 모델의 사건 진술 수이며 성능 비교 수치가 아님을 설명했다.
- 아직 독립 검토자의 최종 검토와 웹 도해의 대응 확인이 남았다. 단원 ready로 표시하지 않는다.
- U04 범위 중 표현 비교 도해는 프로토타입에서 구현 중이며, 완성 후 코드·본문과 대조해야 한다.
