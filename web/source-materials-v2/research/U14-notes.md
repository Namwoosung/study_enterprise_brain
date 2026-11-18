# U14 그래프 활용 RAG 근거 기록

확인일 2026-11-19. [경로 수업](../units/U14/01-follow-evidence-path.md), [Microsoft 방식 수업](../units/U14/02-communities-local-global.md), [질의·운영 수업](../units/U14/03-query-and-operate.md).

| 주장 | 실제 확인한 자료·절 | 적용과 제한 |
| --- | --- | --- |
| 원문의 TextUnit, 개체·관계 설명, 선택적 Covariate, 계층 커뮤니티와 보고서 | [Microsoft GraphRAG Indexing Dataflow, Knowledge Model, Phases 1–6](https://microsoft.github.io/graphrag/index/default_dataflow/) | 산출물별 역할을 예제 표에 반영했습니다. 문서의 기본 데이터 흐름에 한해 설명하며 도구 설정·버전마다 창 크기와 필드가 달라질 수 있습니다. |
| LLM 추출·통합, 논문 실험의 개체 문자열 일치와 간선 가중치 | [Edge et al., From Local to Global, arXiv v2, §3.1.2–3.1.3](https://arxiv.org/html/2404.16130#S3.SS1.SSS2) | 관계와 출처 검토를 분리합니다. 추출을 승인 사실 검증으로 제시하지 않습니다. |
| Hierarchical Leiden, 수준별 보고서, 높은 수준에서 입력 설명이 길 때의 대체 | [Edge et al., §3.1.4–3.1.5 및 §4.1.2의 커뮤니티 수준 조건](https://arxiv.org/html/2404.16130#S3.SS1.SSS4) | 그림의 커뮤니티와 보고서는 직접 만든 예시입니다. 수준 간에 분할되지 않은 커뮤니티는 논문 비교 조건에서 다음 수준으로 투영했습니다. |
| Local Search에서 개체 설명 임베딩 매칭, 관계·보고서·원문 후보, 한 컨텍스트 창 | [Microsoft GraphRAG Local Search, Methodology](https://microsoft.github.io/graphrag/query/local_search/#methodology) | 실제 검색의 인덱스·결과는 실행하지 않았습니다. 질의별 후보 테이블은 구성 요소의 역할을 설명합니다. |
| Global Search의 커뮤니티 수준 및 map/reduce | [Edge et al., §3.1.6](https://arxiv.org/html/2404.16130#S3.SS1.SSS6), [Microsoft GraphRAG Global Search, Methodology](https://microsoft.github.io/graphrag/query/global_search/#methodology) | 논문의 0–100 유용성 및 0 제거, 공식 문서의 중간 요점별 중요도·예산을 설명합니다. 모의 Map 점수와 순위에 모델 품질을 부여하지 않습니다. |
| 직접 그래프 질의, 벡터 이후 Cypher, 모델이 스키마를 보고 생성하는 Text2Cypher | [Neo4j GraphRAG User Guide, Vector + Cypher, Hybrid Cypher and Text2Cypher Retriever](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html) | 구현 예시이며 Microsoft 검색 모드의 동작으로 일반화하지 않습니다. 접근 규칙은 응용 설계 예입니다. |
| 방향과 관계 패턴, SPARQL 변수·조건 | [Neo4j Cypher Manual, MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/match/), [SPARQL 1.1 Query Language, §2, §5.1, §6, §10.2, §17.3–17.4](https://www.w3.org/TR/sparql11-query/) | Cypher와 SPARQL은 별도 스키마를 가정합니다. 구문에 따른 결과는 예상 결과로 제시하며 DB 실행 측정은 포함하지 않습니다. |

## 예제 및 검토 범위

- 공통 합성 사례의 원문 위치·내용, 관계·시행일, 보고서·중간 점수는 [fixture](../examples/rag-graph/graph.json)에 정리했습니다. Python 표준 라이브러리 [검증](../examples/rag-graph/verify.py)은 현재·과거·경계일의 경로와 컨텍스트, 잘못 붙인 G09의 사건 번호 불일치, 모의 Map 점수 정렬을 확인합니다.
- 기간 필터는 시작일 포함·종료일 제외입니다. 서술과 데이터에서 CR-119는 4월 1일, CR-121은 4월 2일에 각각 시작합니다. 보고서 수준과 날짜 조건을 혼동하지 않도록 현재 관계를 묻는 질문은 대장 근거를 사용합니다.
- 범용 그래프 활용·Microsoft GraphRAG·KG의 차이, 잘못 연결한 개체와 관계, 후보의 중복을 별도 예에서 설명했습니다. GraphRAG 성능 수치, LLM·Leiden·그래프 DB 성능 실측은 다루지 않습니다.
- [독립 검토](../reviews/U14-priority-review.md)의 U14-L01 자료 수·관계 방향·모의 근거 위치, U14-L02 계층 용어·보고서의 공급사 이름, U14-L03 필수 MATCH 및 권한 예를 수정했습니다. 독립 검토에서 같은 RDF 스키마를 써서 SPARQL을 실행했고, 공개 구현 HEAD에서 Microsoft Local/Global의 동작을 확인했습니다.
