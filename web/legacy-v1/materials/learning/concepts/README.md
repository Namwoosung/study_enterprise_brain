# 개념 학습 — 기초에서 내부 원리와 발표 설명까지

2026-11-18 작성. 기간 제한 없이 필요한 개념을 이해하기 위한 별도 경로다. 기존 M1~M8은 수집·연결·검증의 적용 과정으로 유지한다. 처음에는 이 C1~C14를 읽고 M 단원으로 연결한다. D 단원은 추가 반례·실행 원리를 보완한다.

각 단원은 무엇인지·왜 필요한지 → 구성 요소와 작동 방식 → 합성 반도체 사례 → 심화 선택·실패 조건 → 발표 수준·확인 문제로 이어진다. 모든 개념의 기초와 판단에 필요한 심화를 본문에 담고, 실제 구현에만 필요한 세부는 생략 가능 범위를 명시했다. 기존 내용의 난도를 높이는 대신 빠졌던 설명 층을 추가한다.

## 권장 순서

| 순서 | 단원 | 질문 |
|---|---|---|
| 1 | [Second Brain · Enterprise Brain](C01_brains.md) | 개인 기억에서 조직의 공유 지식으로 무엇이 달라질까? |
| 2 | [Knowledge Graph](C02_knowledge_graph.md) | 연결된 데이터가 어떻게 지식으로 활용될까? |
| 3 | [Ontology](C03_ontology.md) | 같은 말을 같은 뜻으로 쓰게 하려면? |
| 4 | [Semantic Web · W3C](C04_semantic_web.md) | 표준은 어떤 상호운용을 가능하게 할까? |
| 5 | [RDF Graph](C05_rdf.md) | 한 진술을 어떻게 교환 가능한 그래프로 적을까? |
| 6 | [RDFS · OWL · SHACL](C06_semantics.md) | 의미를 추론하는 것과 입력을 검사하는 것은 어떻게 다를까? |
| 7 | [Property Graph](C07_property_graph.md) | 노드와 관계에 속성을 붙이면 무엇이 달라질까? |
| 8 | [Graph DB · Neo4j](C08_graphdb_neo4j.md) | 그래프 저장소가 맡는 책임은 어디까지일까? |
| 9 | [Cypher · SPARQL 읽기](C09_query_reading.md) | 이 쿼리는 어떤 질문에 답하고 무엇을 빠뜨릴까? |
| 10 | [Auto ontology](C10_auto_ontology.md) | 무엇을 자동 생성하고 어떤 결과를 검토할까? |
| 11 | [Vector RAG](C11_vector_rag.md) | 비슷한 표현을 찾는 것이 왜 근거 검색에 도움이 될까? |
| 12 | [Graph RAG](C12_graph_rag.md) | 관계는 근거를 어떻게 조립해 줄까? |
| 13 | [Tree RAG](C13_tree_rag.md) | 세부와 전체 맥락을 어떻게 함께 찾을까? |
| 14 | [전체 연결과 발표 점검](C14_connections.md) | 이 개념들을 어떻게 한 설명으로 연결할까? |

## 요청 용어의 포함 위치

Enterprise Brain·Second Brain → C1, Knowledge Graph → C2, ontology → C3·C6, Semantic Web·W3C → C4, RDF graph·RDF → C5, OWL → C6, Property graph → C7, Graph db·Neo4j → C8, Cypher·SPARQL → C9, Auto ontology → C10, Vector rag → C11, graph rag → C12, tree rag → C13. C14에서 전부 연결한다.

## 읽는 방법

1. 첫 설명을 읽고 사례를 자신의 말로 풀어 본다.
2. 심화 구간에서 어떤 가정이 깨질 때 결과가 달라지는지 확인한다.
3. 마지막 질문에 먼저 답한 뒤 해설을 연다.
4. 웹의 구간 메모에 정의·예·한계를 한 문장씩 남긴다.
5. 쿼리는 의미를 읽는다. 설치·문법 전체 암기는 목표가 아니다.

[조사 근거와 확인 범위](RESEARCH.md) · [기존 적용 교재](../README.md) · [추가 심화](../deep/README.md)

제품 사용례는 제품 전체의 독립 성능 평가가 아니다. 교재의 합성 계산·모델링 제안은 출처에서 관측한 실증 결과와 구분한다. 직접 실행한 검사는 [개념 예제 검사](../examples/verify_concepts.py) 및 그 결과 파일에 한정한다.
