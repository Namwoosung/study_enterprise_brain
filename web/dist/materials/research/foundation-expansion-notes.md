# 기초 확장의 근거·실행 범위

2026-11-19. 보조 에이전트 사용량 한도 이후 주 작성자가 U01~U03·U06~U07을 집필하고 확인했습니다. U05 추가 두 수업은 에이전트가 중단 전 작성한 결과를 읽어 통합합니다. 추가 독립 검토가 완료됐다고 표시하지 않습니다.

## 근거 연결

- U01: [Second Brain 원저자 측](https://www.buildingasecondbrain.com/foundation)의 CODE와 [PARA](https://fortelabs.com/blog/para/)의 행동 중심 네 범주를 확인했습니다. 개발 회고 사례는 자체 설계입니다. [WRITER 소개](https://writer.com/blog/enterprise-brain/)의 2026-09-09 제품 사용례와 공유 GTM 맥락은 기업 전체의 표준 정의와 구분합니다.
- U02: [PostgreSQL 18 recursive CTE](https://www.postgresql.org/docs/18/queries-with.html#QUERIES-WITH-RECURSIVE), [Neo4j 실행 계획](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/execution-plans/), [Expand All](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/operators/operators-detail/#query-plan-expand-all), [인덱스](https://neo4j.com/docs/cypher-manual/current/indexes/performance-indexes/using-indexes/)를 읽었습니다. 층별 노드 8·관계 15·경로 9는 자체 합성 예이며 실제 DB hits가 아닙니다. EXPLAIN 추정과 PROFILE 실행, Rows와 DB hits, 캐시 조건을 구분합니다.
- U03: [값의 종류](https://neo4j.com/docs/cypher-manual/current/values-and-types/property-structural-constructed/), [null](https://neo4j.com/docs/cypher-manual/current/values-and-types/working-with-null/), [elementId](https://neo4j.com/docs/cypher-manual/current/functions/scalar/#functions-elementid), [MERGE](https://neo4j.com/docs/cypher-manual/current/clauses/merge/), [constraints](https://neo4j.com/docs/cypher-manual/current/schema/constraints/create-constraints/), [트랜잭션](https://neo4j.com/docs/operations-manual/current/database-internals/transaction-management/), [드라이버 재시도](https://neo4j.com/docs/python-manual/current/transactions/)와 [DELETE](https://neo4j.com/docs/cypher-manual/current/clauses/delete/)를 대조했습니다. current 문서의 제품별·에디션별 성격을 명시하고 내부 ID를 영속 업무 ID로 사용하지 않습니다.
- U05: SKOS 개념·상하·매핑과 OWL 클래스/동일성을 구분한 두 수업을 읽었습니다. PROV 작성 활동과 정비 수행의 관계, 신규 작업지시 CLOSE 상태를 실제 수행으로 자동 변환하지 않는 사례를 확인했습니다. 기존01의 Q1~Q8과 신규 Q9의 기간·집계 단위를 보존합니다. 본문의 Turtle 파싱은 별도 예제에서 확인합니다.
- U06: [OWL 2 Overview](https://www.w3.org/TR/owl2-overview/), [Primer](https://www.w3.org/TR/owl2-primer/), [Structural Specification](https://www.w3.org/TR/owl2-syntax/), [Direct Semantics](https://www.w3.org/TR/owl2-direct-semantics/), [Profiles](https://www.w3.org/TR/owl2-profiles/) 및 SHACL §4.2와 OWL-RL 도구 문서를 확인했습니다. 임의의 클래스 충돌을 자동 삭제로 설명하지 않고, 불만족 클래스와 전체 불일관성, some/only/개수·동일성, 해석과 입력 검사를 원래 예로 전개합니다.
- U07: [SPARQL 1.1 §2·5·6·9·11·13·16](https://www.w3.org/TR/sparql11-query/)과 Neo4j MATCH·OPTIONAL MATCH·집계 함수를 대조합니다. 필수/선택 패턴, 필터 위치, 작업/값에 적용하는 DISTINCT, 경로와 끝점 집합을 같은 자료의 중간 행으로 확인합니다.

## 실행

- `examples/relational-graph/verify_paths.py`: 본문에서 SQL을 직접 읽어 SQLite 3.50.4로 A·B·X·Z를 반환했습니다. 순환을 넣으면 멈추지만 자기 P도 들어오는 반례를 확인합니다.
- `examples/owl-semantics/verify.py`: 본문의 Turtle 7블록을 읽어 RDFLib 7.6.0·owlrl로 하위 타입·동치 타입·하위 속성·역관계·sameAs의 속성 전파·최대 1의 동일성 결론을 확인합니다. OWL 2 DL 전체의 일관성 검사나 이름 없는 존재 생성은 실행하지 않았습니다.
- `examples/query-reading/verify.py`: 동일 합성 dataset에서 본문 SPARQL 11개를 실행해 기본 매칭·필터·집계·선택값·중복 제거·그룹·도달·named graph를 대조합니다. Cypher는 문서에 따른 예상 결과이며 서버를 실행하지 않았습니다.

이 실행들은 정답의 일부를 재현하는 검사입니다. 수업을 읽은 사람의 이해나 제품의 성능을 측정하지 않습니다.
