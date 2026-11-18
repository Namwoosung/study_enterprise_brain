# U02 비교 수업 조사·실행 기록

2026-11-18. 이 파일은 U02-L01 부분 수업의 기록이다.

- [Neo4j graph concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/)의 노드·관계·라벨·속성 정의를 U04 조사 때 함께 확인했다.
- [Neo4j query plans](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/execution-plans/)의 lifecycle/EXPLAIN/PROFILE 설명을 읽었다. 그래프 모델과 물리 실행을 분리하는 설명에 적용했다.
- [PostgreSQL18 WITH queries §7.8.2](https://www.postgresql.org/docs/18/queries-with.html#QUERIES-WITH-RECURSIVE)의 반복 평가·하위 부품 예를 읽고, RDB도 가변 깊이 연결을 표현할 수 있음을 설명했다. 예제 SQL이 PostgreSQL 전용 재귀 질의를 실행한 것은 아니다.
- 동일 직원·팀·문서 합성 자료를 SQLite에 적재하고 본문 SQL을 실행해 D1·민수·지연을 확인했다. Cypher는 같은 모델에서 손으로 도출한 예상 결과다.
- 10^6 분기 계산은 겹침·제약·가지치기 없는 교육용 계산이며 그래프 DB 성능 실측이 아니다.

남은 일: 독립 설명 검토, 다양한 질문 유형·순회/색인 사례로 단원 확장. 본편 전체 ready 아님. SQL 재현 파일은 examples/relational-graph/verify.py에 있다.
