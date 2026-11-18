# U04 기술·설명 검토

검토일 2026-11-18. 검토 대상은 U04의 언어, 반복 사건 비교, 진술·문맥 수업 원고 세 편입니다. 아래는 주 작성자가 수정 전 대조할 수 있도록 검토 당시 위치를 기록한 결과입니다.

## 기술 검토

| 우선순위 | 위치와 발견 | 수정 및 확인 방법 |
| --- | --- | --- |
| 수정 | [언어 수업](../units/U04/01-rdf-language.md) §1, §6, §7. 원문 절을 지정한 세 링크의 fragment가 해당 W3C HTML에 존재하지 않았습니다. HTML의 `id`와 `a name`에 대해 W3C 절 링크 15개를 확인했습니다. | RDF Primer 도입은 [§1](https://www.w3.org/TR/rdf11-primer/#section-Introduction), Turtle의 blank node는 [§2.6](https://www.w3.org/TR/turtle/#BNodes), RDF/XML의 노드·속성 문법은 [§2.2](https://www.w3.org/TR/rdf-syntax-grammar/#section-Syntax-node-property-elements)로 연결합니다. |
| 수정 | [사건 수업](../units/U04/02-events-and-property-graphs.md) §9. 현재 세 운전은 각각 거리 하나를 가지므로 SPARQL의 `COUNT(?d)`와 `SUM(?km)`가 의도한 값과 일치합니다. `drive2`에 기존 거리 18을 보존한 채 거리 20을 추가하면 RDFLib 결과가 `4, 59`입니다. 쿼리는 이벤트 ID 집합이 아니라 패턴이 반환한 행의 바인딩을 집계합니다. | 본문에 “예제는 사건마다 거리 값 하나를 기록하므로 사건마다 매칭 행이 하나 생깁니다”를 보탭니다. 개정 거리와 원래 거리 중 어느 값을 합칠지는 별도 선정 규칙이 필요합니다. [SPARQL 1.1 §18.5.1.2–3](https://www.w3.org/TR/sparql11-query/#defn_aggCount) |
| 확인 | [문맥 수업](../units/U04/03-statements-and-context.md) §2, §3, §5. Reification만으로 원 진술이 함의되지 않는 설명과 dataset에서 default graph와 named graph를 구별하는 설명이 규격에 맞습니다. RDF 1.2 고정판의 CRD 날짜 및 최신 Recommendation 링크도 대조했습니다. | 출처 링크가 있다고 사실이 채택되지는 않는다는 설명을 유지합니다. RDF 1.2 구현 검증은 남아 있고 교재의 실행 범위는 RDF 1.1입니다. [RDF 1.1 Semantics D.1](https://www.w3.org/TR/rdf11-mt/#reification), [RDF Concepts §4](https://www.w3.org/TR/rdf11-concepts/#section-dataset), [RDF 1.2 고정판](https://www.w3.org/TR/2026/CRD-rdf12-concepts-20261116/) |

독립 확인에서는 저장소 가상 환경의 RDFLib 7.6.0으로 네 가지를 대조했습니다. JSON-LD의 `{"@id":"ex:M17"}`는 문서 IRI에 연결되고, 같은 자리의 `"ex:M17"`은 문자열 리터럴이 됩니다. 사건 Turtle과 Cypher의 날짜·거리·탑승 인원은 세 건 모두 일치합니다. 두 번째 거리 값을 넣은 SPARQL 결과에서 집계의 가정을 확인했습니다. TriG의 default graph에는 출처 연결이 들어 있고 부품 사용 진술은 `graphR17`에 들어 있어, 예제의 `GRAPH ?g`는 `graphR17/P7`을 반환합니다. Cypher 쪽 확인은 원고에 적힌 속성값 대조이며 Neo4j 엔진 실행은 대기 상태입니다.

## 설명 검토

| 우선순위 | 위치와 독자가 맞닥뜨릴 질문 | 수정 및 확인 방법 |
| --- | --- | --- |
| 수정 | [언어 수업](../units/U04/01-rdf-language.md) §3, §6. 예제를 읽으면 IRI, 값, blank node의 역할을 알 수 있지만, 독자가 처음 새 트리플을 써 볼 때 문자열을 주어로 둬도 되는지, blank node를 관계 이름 자리에 둬도 되는지 설명에서 확인하기 어렵습니다. | blank node까지 소개한 뒤 세 자리 표로 허용되는 term을 정리합니다. RDF 1.1에서 주어는 IRI 또는 blank node, 술어는 IRI, 목적어는 IRI·blank node·literal을 사용할 수 있습니다. 새 관측 예에서 어떤 자리에 각 항목을 배치할 수 있는지 시험합니다. [RDF Concepts §3.1](https://www.w3.org/TR/rdf11-concepts/#section-triples) |
| 수정 | [사건 수업](../units/U04/02-events-and-property-graphs.md) §10 끝. JSON-LD를 다음 예제에서 설명한다는 안내와 실제 배열이 맞지 않습니다. 세 직렬화 비교는 앞의 언어 수업 §7에 있고, 뒤의 문맥 수업은 진술과 dataset입니다. | 언어 수업 §7로 연결하고, 다음 수업에서는 사건과 출처가 있는 주장을 구별한다고 안내합니다. |
| 보완 | [사건 수업](../units/U04/02-events-and-property-graphs.md) §9. `?d`와 `?km`는 설명하지만, 처음 질의를 본 독자가 집계 전 각 사건과 거리의 대응을 중간에 읽을 수 있는 표시는 없습니다. 첫 절이 묻는 시작 시각은 §8의 SQL이나 원천 표에서 읽을 수 있고, §9의 두 집계 쿼리에서는 읽을 수 없습니다. | `drive1/12`, `drive2/18`, `drive3/9`가 집계 전 매칭 행이라는 해설을 추가하고, §9가 세 건의 횟수와 이동거리 합을 비교하는 위치임을 명확히 합니다. |
| 확인 | [언어 수업](../units/U04/01-rdf-language.md) §8과 [문맥 수업](../units/U04/03-statements-and-context.md) §6. 연습은 각각 클래스 소속과 라벨의 주어, 사건의 개수와 기록의 개수를 독자가 본문으로 돌아가 설명할 수 있게 구성돼 있습니다. | 실습 환경이 없어도 코드 해설과 예상 결과를 읽어 답할 수 있습니다. 사건 비교 도해의 선택과 코드 대응, 화면 폭·키보드 검토는 실제 프로토타입에서 확인해야 합니다. |

## 수정 후 재확인

- 언어 수업 §1, §6, §7의 세 링크를 수정한 뒤, 이 기록을 포함해 W3C 절 링크 17개의 fragment가 각각 HTML에 존재함을 확인했습니다.
- 언어 수업 §6에 RDF 1.1 트리플 자리별 허용 요소와 예가 들어갔습니다. 문자열 주어와 술어를 왜 사용할 수 없는지 설명하는 문장도 확인했습니다.
- 사건 수업 §9의 집계 전제, 두 거리 값의 반례, `COUNT(DISTINCT ?d)`로 사건 수를 따로 셌을 때도 거리 선택이 남는다는 설명을 확인했습니다. §10은 JSON-LD를 앞 수업에 연결하고, 뒤 수업의 진술·문맥 주제를 안내합니다.
- 사건 수업 §9에 집계 직전 세 매칭 행을 그대로 제시하는 것은 선택적 보완으로 남았습니다. Neo4j 실행과 도해의 실제 화면 동작은 이번 검토 범위 밖입니다. 세 편의 원고 검토는 B01/B03의 근거이며, 단원 전체의 완료 상태는 이후 도해와 웹에서의 대응을 확인한 뒤 판단합니다.


## 2026-11-19 integration recheck
Root added pre-aggregation match rows and AS column-name explanation. Prototype keyboard/data correspondence checked separately in rebuild/prototypes/QA.md.
