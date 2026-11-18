# U03 첫 수업의 근거와 검토 범위

2026-11-19. 사용자 선택 B안의 로컬 통합에도 포함했다. 단원 전체 ready가 아닌 첫 수업이다.

- Neo4j 공식 [graph concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/)의 nodes/labels/relationships/properties를 기준으로 제품 모델을 설명했다.
- [MERGE](https://neo4j.com/docs/cypher-manual/current/clauses/merge/)의 matching·전체 패턴·identifying constraints·concurrent relationship merges를 확인했다. 관계 병합의 잠금 동작과 노드 식별 속성의 고유성 요구를 구분했다.
- [Create constraints](https://neo4j.com/docs/cypher-manual/current/schema/constraints/create-constraints/)에서 고유성과 존재 제약, 에디션 표시를 확인했다. 고유성이 필수 입력까지 요구하지 않음을 반영했다.
- [Query plans](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/execution-plans/)의 논리/물리 계획과 EXPLAIN/PROFILE 구분을 이전 U02와 연결했다.

Cypher는 공식 문서와 패턴을 대조한 읽기용 예상 결과이며 Neo4j 서버 실행은 하지 않았다. 검토에서 변수와 영구 업무 ID, 라벨 다중 지정과 클래스 포함 공리, 관계 속성과 사건 노드, 제약과 실세계 동일성의 혼동을 점검했다. 운영/트랜잭션 예는 교재의 합성 설계 설명이다. 후속 수업에서 제약·색인·모델 변경의 구체 사례와 실행 환경 범위를 보강한다.
