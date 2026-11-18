# 개념 교재 조사 기록

확인일: 2026-11-18 (Asia/Seoul). 대상: C1~C14. 공식 규격·제품 공식 문서·원저자 자료·원논문을 우선 사용했다. 교재의 합성 사례·계산·설계 제안은 자료의 실증 결과와 구분했다.

## 자료와 반영 범위

| 교재 | 확인한 원문 | 반영한 내용·한계 |
|---|---|---|
| C1 | [Forte 공식 입문](https://fortelabs.com/blog/basboverview/) | CODE와 개인 재사용 목적. 효과를 독립 실험으로 검증한 자료로 쓰지 않음 |
| C1 | [WRITER Enterprise Brain](https://writer.com/blog/enterprise-brain/) | 2026-09-09 제품명·공유 맥락 사용례. 보편 표준 정의가 아님 |
| C2·C8 | [Hogan et al. 2021](https://arxiv.org/abs/2003.02320) | KG의 모델·스키마·동일성·맥락·구축을 개관. 제품 벤치마크로 사용하지 않음 |
| C3 | [Stanford Ontology 101](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html) | 범위·재사용·클래스·속성·역량 질문. 구형 도구 사용법을 현재 절차로 제시하지 않음 |
| C3 | [SKOS Primer](https://www.w3.org/TR/skos-primer/) | 통제 어휘·개념 체계. W3C Note로 표기 |
| C4 | [W3C Semantic Web 역사 페이지](https://www.w3.org/2001/sw/) | 공유·재사용 목표. 2013 동결 페이지임을 표기 |
| C4 | [Linked Data 설계 글](https://www.w3.org/DesignIssues/LinkedData.html) | 식별·HTTP·정보 제공·연결 원칙. 개인 설계 견해로 구분 |
| C4 | [W3C standards](https://www.w3.org/standards/) | 표준·초안·문서 지위 구별 |
| C5 | [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/) · [Primer](https://www.w3.org/TR/rdf11-primer/) | triple·집합·IRI·literal·blank node·dataset·구문 구분 |
| C6 | [RDFS](https://www.w3.org/TR/rdf-schema/) | subclass·domain·range의 의미 |
| C6 | [OWL 2 Overview](https://www.w3.org/TR/2012/REC-owl2-overview-20121211/) · [Primer](https://www.w3.org/TR/owl2-primer/) · [Profiles](https://www.w3.org/TR/owl2-profiles/) | 열린 세계·동일성·조건·표현력. 엔진 설정과 구별 |
| C6 | [SHACL](https://www.w3.org/TR/shacl/) | target·constraint·report. 원천 사실성 보장으로 사용하지 않음 |
| C1·C5 | [PROV-O](https://www.w3.org/TR/prov-o/) | Entity·Activity·Agent와 파생·출처. 승인 정책은 교재 설계 |
| C1·C4 | [R2RML](https://www.w3.org/TR/r2rml/) | 관계형→RDF 매핑 및 가상 접근·물리 생성 선택 |
| C7·C8 | [Neo4j graph concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) | 해당 제품 기준 라벨·관계·속성. 모든 제품 일반화 금지 |
| C8 | [인덱스](https://neo4j.com/docs/cypher-manual/current/indexes/search-performance-indexes/using-indexes/) · [계획](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/execution-plans/) · [트랜잭션](https://neo4j.com/docs/operations-manual/current/database-internals/transaction-management/) | 시작점·실행 계획·DB 처리 단위. 성능 실측 아님 |
| C8·C12 | [Neo4j GraphRAG for Python](https://neo4j.com/docs/neo4j-graphrag-python/current/index.html) | 별도 라이브러리·문서 범위. 설치·성능 검증 안 함 |
| C9 | [Cypher Overview](https://neo4j.com/docs/cypher-manual/current/introduction/cypher-overview/) · [MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/match/) · [OPTIONAL MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/optional-match/) | 읽기 패턴·선택 관계. Cypher 서버 실행 안 함 |
| C9 | [SPARQL Overview](https://www.w3.org/TR/sparql11-overview/) · [Query](https://www.w3.org/TR/sparql11-query/) | 기본 패턴·OPTIONAL·중복·질의 형태. 동봉 예제만 RDFLib 실행 |
| C10 | [LLMs4OL](https://arxiv.org/abs/2307.16648) | 용어 유형·분류체계·비계층 관계의 작업 분해 |
| C10 | [NVIDIA Auto Ontology](https://github.com/NVIDIA/auto-ontology#how-it-works) | 개념·매핑·관계·지표·계보·인증, Postgres/pgvector. README 확인·제품 실행 안 함 |
| C11 | [RAG 원논문](https://arxiv.org/abs/2005.11401) · [DPR](https://arxiv.org/abs/2004.04906) | 검색·생성, dual encoder 출발점. 현재 모든 파이프라인과 동일시하지 않음 |
| C11 | [HNSW](https://arxiv.org/abs/1603.09320) | ANN의 근접 그래프 구조. 업무 관계 KG와 구분 |
| C12 | [Microsoft Dataflow](https://microsoft.github.io/graphrag/index/default_dataflow/) | TextUnit·Entity·Relationship·커뮤니티 보고서 |
| C12 | [Local](https://microsoft.github.io/graphrag/query/local_search/) · [Global](https://microsoft.github.io/graphrag/query/global_search/) | 개체 기반 근거 조합·커뮤니티 보고서 결합. 실제 검색 실행 안 함 |
| C13 | [RAPTOR 원논문 §3](https://arxiv.org/html/2401.18059v1) | 재귀 요약·soft clustering·traversal/collapsed. 모든 Tree RAG의 정의가 아님 |
| C14 | [NASA 지식 포착 보고서](https://ntrs.nasa.gov/citations/20110023477) | 문서와 사람의 지식 이전. 제시한 인터뷰 질문은 교재 응용 |
| C14 | [Stanford IR 교과서](https://nlp.stanford.edu/IR-book/) | 검색 평가 개념의 기존 교재 참고자료. 이번 회차 포털·개별 HTML 절 재접속은 timeout; 수치는 교재의 독립 합성 계산 |

## 검증과 표현의 경계

- 공식 정의의 요약, 교재가 만든 사례, 설계 대안을 문장으로 구분했다.
- Enterprise Brain·Auto ontology·Tree RAG는 문맥별 범위를 명시한다.
- 안정적 학습 기준으로 RDF 1.1·OWL 2·SPARQL 1.1·SHACL 2017을 사용한다. 최신 규격 전부를 조사하거나 모든 엔진의 지원을 검증했다는 뜻이 아니다.
- 현재 제품 문서는 바뀔 수 있다. 설치·도입 시 버전·커밋 고정과 호환성 재확인이 필요하다.
- 코사인·정밀도·재현율·검토 용량은 합성 숫자의 계산 검증이다. 실모델 성능이나 실제 반도체 공정 지표가 아니다.
- [verify_concepts.py](../examples/verify_concepts.py)는 Markdown의 Turtle·SPARQL 예제 일부를 읽어 실행한다. Cypher는 문서와 대조한 읽기용 예제이며 서버에서 실행하지 않았다.
- 웹의 표현 전환·벡터 각도·계층 검색 예제는 원리 학습용이다. 벤치마크·실제 LLM 호출로 표시하지 않는다.
