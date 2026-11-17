# 콘텐츠 대응표와 후속 웹 전환 기준

이 표는 교재의 내용이 웹 학습 페이지에서 빠지지 않게 하기 위한 기준이다. **2026-11-18에 웹의 54개 학습 구간으로 반영했다.** 아래 시각화 열은 설계 후보이며, 실제 구현한 인터랙션과 대응 경로는 문서 끝에 기록한다.

Markdown 본문은 전체 학습 내용의 기준이다. 웹에서는 문장·배치를 바꿀 수 있지만, 정의뿐 아니라 조건·반례·합성 표시·출처·해설·선택 심화도 보존한다.

## 내용 ID

명시적인 HTML anchor를 내용 ID로 사용한다. 각 범위는 해당 anchor부터 다음 anchor 직전까지이며, 마지막 범위는 파일 끝까지다. 따라서 별도 ID가 없는 확인 문제·해설도 빠지지 않는다.

| 내용 ID와 본문 | 필수 보존 내용 | 유용할 수 있는 표현 |
|---|---|---|
| [M1-01](M1_problem.md#m1-01) | RAG 이후 남는 의미·근거 문제 | 같은 질문의 근거 비교 |
| [M1-02](M1_problem.md#m1-02) | Second Brain·기업 요구·작업 정의·제품 사용례 | 개인/조직 요구 비교 |
| [M1-03](M1_problem.md#m1-03) | 전체 구성·KG와 DB·검색의 역할 | 전체 관계도 |
| [M1-04](M1_problem.md#m1-04) | 최소 반도체 배경·합성 범위 | 대상·작업 그림 |
| [M1-05](M1_problem.md#m1-05) | 역량 질문·그래프 없는 대안 | 질문 선택 카드 |
| [M1-06](M1_problem.md#m1-06) | 확인 문제·해설·설명 과제 | 답 펼치기 |
| [M2-01](M2_representation.md#m2-01) | Run 사건 모델과 선택 이유 | 관계/사건 표현 비교 |
| [M2-02](M2_representation.md#m2-02) | 개체·종류·이름·부품 구분 | 구분 연습 |
| [M2-03](M2_representation.md#m2-03) | 용어집·스키마·ontology·SKOS 선택 | 표현력 비교 |
| [M2-04](M2_representation.md#m2-04) | RDF triple·IRI·literal·blank node·Turtle | 문장/triple 변환 |
| [M2-05](M2_representation.md#m2-05) | RDFS·OWL·열린 세계·동일성·추론/검증 | 선언에 따른 결과 변화 |
| [M2-06](M2_representation.md#m2-06) | Property Graph·Neo4j·MERGE·제약 | RDF/Property Graph 병렬 표현 |
| [M2-07](M2_representation.md#m2-07) | SPARQL·Cypher·데이터 부분집합 | 질의와 결과 |
| [M2-08](M2_representation.md#m2-08) | 주장·출처·named graph 한계·문제·해설 | 주장/사실 상태 비교 |
| [M3-01](M3_acquisition.md#m3-01) | 수집·원천 카드 | 원천에서 후보까지 |
| [M3-02](M3_acquisition.md#m3-02) | 정형 매핑·SQL·R2RML·역할 | 행→관계 매핑 |
| [M3-03](M3_acquisition.md#m3-03) | 파싱·추출·부정·조건·추출 지시 | 원문/후보 대조 |
| [M3-04](M3_acquisition.md#m3-04) | 암묵지·인터뷰·맥락·한계 | 질문을 통한 경험 구체화 |
| [M3-05](M3_acquisition.md#m3-05) | 경험 검토·재사용·변환 불확실성 | 증거 종류 표시 |
| [M3-06](M3_acquisition.md#m3-06) | 확인 문제·해설·과제 | 답 펼치기 |
| [M4-01](M4_integration.md#m4-01) | mention·entity·resolution | 언급과 대상 매핑 |
| [M4-02](M4_integration.md#m4-02) | 매칭 근거·8개 판단 예 | 병합/분리 선택 |
| [M4-03](M4_integration.md#m4-03) | 후보 생성·비교량·누락·복구 | 후보 축소와 놓치는 정답 |
| [M4-04](M4_integration.md#m4-04) | 의미 충돌·원천 권위·범위 | 충돌 자료 대조 |
| [M4-05](M4_integration.md#m4-05) | 스키마 우선·귀납·반복 접근 | 선택 조건 비교 |
| [M4-06](M4_integration.md#m4-06) | ontology 학습/정렬/채우기·LLMs4OL·NVIDIA | 자동화 대상 분해 |
| [M4-07](M4_integration.md#m4-07) | 병합 오류 전파·sameAs·문제·해설 | 잘못된 병합 전후 |
| [M5-01](M5_validation.md#m5-01) | 검증 분석의 여섯 층·DQV 지위 | 검사 범위 비교 |
| [M5-02](M5_validation.md#m5-02) | SHACL 대상·조건·통과/실패의 의미 | D02/D01/누락 바꾸기 |
| [M5-03](M5_validation.md#m5-03) | 원문 지지·검토 독립성 | 인용 존재/의미 지지 비교 |
| [M5-04](M5_validation.md#m5-04) | V01~V10 오류 분류 | 오류 찾기 연습 |
| [M5-05](M5_validation.md#m5-05) | 검토 정책·병목 계산·대안 | 후보량·시간 조절 |
| [M5-06](M5_validation.md#m5-06) | P/R/F1·표본 0오류 가정·한계 | 분모 비교 |
| [M5-07](M5_validation.md#m5-07) | 다차원 상태·문제·해설 | 승인 정보 펼치기 |
| [M6-01](M6_lifecycle.md#m6-01) | 사건·유효·수집 시간 | 시간축과 질의 시점 |
| [M6-02](M6_lifecycle.md#m6-02) | 버전·반개구간·이력 | 현재/과거 조회 |
| [M6-03](M6_lifecycle.md#m6-03) | PROV·변환·책임·재현 | 원천→결과 추적 |
| [M6-04](M6_lifecycle.md#m6-04) | 변경 전파·철회·색인·캐시 | 의존 결과 강조 |
| [M6-05](M6_lifecycle.md#m6-05) | 원문과 파생 정보의 권한 | 사용자별 허용 근거 |
| [M6-06](M6_lifecycle.md#m6-06) | 복제·가상·혼합·책임 | 저장/질의 선택 비교 |
| [M6-07](M6_lifecycle.md#m6-07) | 확인 문제·해설·과제 | 답 펼치기 |
| [M7-01](M7_retrieval.md#m7-01) | 근거 구성과 답변 범위 | 검색 흐름 |
| [M7-02](M7_retrieval.md#m7-02) | 벡터·유사도·필터·HNSW 구분 | 관련성/유효성 비교 |
| [M7-03](M7_retrieval.md#m7-03) | 경로 조회·MS Local/Global·Neo4j 구분 | 질문별 선택 경로 |
| [M7-04](M7_retrieval.md#m7-04) | 문서 계층·RAPTOR·soft cluster·검색 전략 | 원문/요약 계층 |
| [M7-05](M7_retrieval.md#m7-05) | 세 질문·실패·구축/질의 비용 | 질문별 근거 비교 |
| [M7-06](M7_retrieval.md#m7-06) | Agent 전달·벤치마크 조건 | 근거 계약 예시 |
| [M7-07](M7_retrieval.md#m7-07) | 문제·해설·실험 설계 과제 | 답 펼치기 |
| [M8-01](M8_synthesis.md#m8-01) | 통합 목적과 의미 | 개념 연결도 |
| [M8-02](M8_synthesis.md#m8-02) | L02 전체 사건·시점·가설·응답 | 근거 지도 |
| [M8-03](M8_synthesis.md#m8-03) | A·B·C 대안과 선택 조건 | 조건별 설계 비교 |
| [M8-04](M8_synthesis.md#m8-04) | 학습 노트·3/10분 설명·발표자 연결 | 설명 체크 |
| [M8-05](M8_synthesis.md#m8-05) | 청중 질문 12개 | 질문 카드 |
| [M8-06](M8_synthesis.md#m8-06) | 종합 평가·해설·설계 변경 과제 | 자체 평가 |

## 최초 요청 범위의 대응

| 요청한 개념 | 주 설명 | 연결 학습 |
|---|---|---|
| Enterprise Brain, Second Brain | M1 | M8의 전체 구성 |
| Ontology, Auto ontology | M2·M4 | M3 획득, M5 검증, M6 변경 |
| Knowledge Graph | M1·M2 | M4 통합, M7 활용 |
| Graph DB, Neo4j | M2 | SQL 대안·예제·M8 선택 |
| W3C RDF/OWL | M2 | M5 SHACL, M6 PROV, 실행 예제 |
| Vector RAG, Graph RAG, Tree RAG | M7 | M1 출발 문제, M8 선택 조건 |

추가 개념인 entity resolution, competency questions, SKOS, R2RML, SHACL, provenance, 시점·버전·권한, 품질 평가, 검토 정책은 연결·검증이라는 사용자의 학습 목적을 설명하기 위해 포함했다.

## 함께 옮겨야 할 보조 자료

- [사례 안내](case/README.md), [원문 14개](case/CORPUS.md), CSV·JSON: 표의 단위·필드 의미·합성 표시를 유지한다.
- [용어집](GLOSSARY.md): 본문의 정확한 위치로 이동할 수 있게 한다.
- [출처 확인 기록](EVIDENCE.md), [조사 목록](../SOURCES.md): 원문 링크와 확인 범위를 유지한다.
- [실행 안내](examples/README.md), 코드·검증 결과: 실제 실행과 문법 참고를 구분한다.
- 각 단원의 확인 문제와 해설: 답을 미리 보지 않고 생각할 수 있게 구성할 수 있다.

## 웹 반영 결과 — 2026-11-18

추가 심화 단원은 learning/deep 아래에 두고 d1-01 같은 별도 내용 ID로 관리한다. 기본 54개 구간을 대체하지 않으며, 웹의 심화 학습 화면과 web/coverage.json에 같은 방식으로 반영한다.

M1-01~M8-06의 54개 내용 ID는 웹의 각 학습 구간으로 연결된다. 주소 규칙은 예를 들어 #/learn/m5/m5-02이며, 정확한 대응은 web/coverage.json에 기록한다. 각 구간은 원문의 설명·조건·예제·출처를 보존하고, 확인 문제의 해설은 사용자가 펼쳐서 읽게 했다.

별도로 구현한 학습 기능은 개체 연결 판단(M4-02), 추론/검증 비교(M2-05), 구조/시점 검증(M5-02), 검토 용량 계산(M5-05), 유효/수집 시점 비교(M6-01), 검색 방식별 근거 구성(M7-05)이다. 검색 방식 비교는 실제 검색 성능 실험이 아닌 설명용 흐름이다.

사례 원문·CSV는 사례 탐색 화면, 18개 질문은 설명 연습 화면, 용어집·출처·개발자 실습은 참고 화면에 반영했다. 원본 자료도 웹에 함께 포함했다. 메모·책갈피·완료 표시는 현재 브라우저에 저장한다.
