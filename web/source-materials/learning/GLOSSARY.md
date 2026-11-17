# 용어와 혼동하기 쉬운 구분

이 표는 본문을 읽은 뒤 찾는 복습 도구다. 정확한 적용 범위·예제·출처는 연결된 단원에서 확인한다. 특히 제품 이름과 연구 범주를 구분한다.

## 목적·표현·저장·활용

| 용어 | 이 교재에서의 뜻 | 혼동 주의 | 본문 |
|---|---|---|---|
| Second Brain | 개인이 외부 기록을 활용하는 지식 관리 접근 | 특정 그래프 DB나 AI 알고리즘이 아님 | [M1](M1_problem.md#m1-02) |
| Enterprise Brain | 조직 지식의 의미·근거·활용을 연결하는 시스템이라는 작업 용어 | 특정 제품 사용례와 분야 전체의 정의를 구분 | [M1](M1_problem.md#m1-02) |
| Knowledge Graph, KG | 개체·관계·맥락을 그래프 형태로 표현한 지식 | 그래프에 넣었다고 사실성이 보장되지 않음 | [M1](M1_problem.md#m1-03) |
| Graph DB | 그래프 모델을 저장·질의하는 DB 범주 | KG의 의미·품질 정책 전체와 같지 않음 | [M2](M2_representation.md#m2-06) |
| Neo4j | Property Graph 기반 DB 제품 | Ontology나 Graph RAG 전체의 동의어가 아님 | [M2](M2_representation.md#m2-06) |
| Property Graph | 노드·관계와 그 속성으로 표현하는 모델 | RDF와 의미가 자동으로 동일하게 변환되지는 않음 | [M2](M2_representation.md#m2-06) |
| Vector RAG | 벡터 유사도 검색을 근거 선택에 사용하는 구성 | 점수는 사실성·승인·시점을 직접 보장하지 않음 | [M7](M7_retrieval.md#m7-02) |
| Graph RAG | 관계 구조를 활용해 답변 근거를 구성하는 접근 범주 | 반드시 Microsoft 구현이라는 뜻은 아님 | [M7](M7_retrieval.md#m7-03) |
| Microsoft GraphRAG | 그래프·커뮤니티 요약 등을 사용하는 특정 연구·프로젝트 | 일반 Graph RAG와 구별 | [M7](M7_retrieval.md#m7-03) |
| Tree RAG | 계층을 검색에 활용하는 방식을 묶어 설명하는 용어 | 이 교재에서 단일 표준 알고리즘으로 정의하지 않음 | [M7](M7_retrieval.md#m7-04) |
| RAPTOR | 재귀적인 군집·요약 계층을 검색에 활용하는 연구 | 모든 항목이 단일 부모를 갖는 단순 트리로만 이해하지 않음 | [M7](M7_retrieval.md#m7-04) |
| HNSW | 벡터의 근접 이웃 탐색에 쓰는 그래프 기반 색인 방법 | 검색용 근접 간선은 업무 관계가 아님 | [M7](M7_retrieval.md#m7-02) |

## 의미를 모델링하는 말

| 용어 | 핵심 의미 | 사례·주의 | 본문 |
|---|---|---|---|
| Competency question | 모델이 답할 수 있어야 할 질문 | “RUN002에 적용된 절차는?” | [M1](M1_problem.md#m1-05) |
| Entity / Instance | 구별해서 다룰 대상 / 특정 종류의 개체 | E01과 Equipment를 구분 | [M2](M2_representation.md#m2-02) |
| Class | 개체들을 분류하는 종류 | InspectionTool은 Equipment의 하위 종류 | [M2](M2_representation.md#m2-02) |
| Mention | 원문에서 대상을 언급한 표현 | ‘검사기 1호’만으로 E01인지 E02인지 모름 | [M4](M4_integration.md#m4-01) |
| Taxonomy | 종류·주제 등의 계층 분류 | 클래스 포함과 부품 관계를 혼동하지 않음 | [M2](M2_representation.md#m2-03) |
| Schema | 데이터 구조·타입·관계 등의 약속 | 필드 구조만으로 업무 의미가 전부 정해지지 않음 | [M2](M2_representation.md#m2-03) |
| Ontology | 개념·관계·공리의 의미를 명시하는 모델 | 범위·표현력은 목적에 맞춰 선택 | [M2](M2_representation.md#m2-03) |
| SKOS | 개념·라벨·의미 관계로 지식 조직 체계를 표현하는 W3C 체계 | broader를 자동으로 OWL subClassOf로 읽지 않음 | [M2](M2_representation.md#m2-03) |
| RDF | triple 기반 데이터 모델 | Turtle은 그 표현 문법 중 하나 | [M2](M2_representation.md#m2-04) |
| IRI | 자원 식별에 쓰는 국제화 식별자 | 다른 IRI가 반드시 다른 현실 대상인 것은 아님 | [M2](M2_representation.md#m2-04) |
| Literal | 문자열·날짜 등 값 | 문서 ID를 단순 문자열로 둘지 자원으로 연결할지 선택 | [M2](M2_representation.md#m2-04) |
| RDFS | RDF의 클래스·속성 등에 의미를 부여하는 어휘 | domain은 필수 타입 누락 거절 명령이 아님 | [M2](M2_representation.md#m2-05) |
| OWL | 더 풍부한 클래스·속성 공리를 표현하는 W3C 언어 | 현실 사실 검증기나 DB 제약 전체와 같지 않음 | [M2](M2_representation.md#m2-05) |
| Open world | 기록의 부재를 곧 거짓으로 보지 않는 의미 해석 | 승인 기록 없음 ≠ 미승인 확인 | [M2](M2_representation.md#m2-05) |
| Entailment / Inference | 주어진 데이터·공리의 의미상 따라오는 결론 / 이를 구하는 과정 | 전제가 잘못되면 현실에 맞는 결론을 보장하지 못함 | [M2](M2_representation.md#m2-05) |
| SPARQL / Cypher | 각각 RDF / Neo4j 그래프 질의에 사용하는 언어 | 문법과 추론·검증 기능을 구분 | [M2](M2_representation.md#m2-07) |
| SHACL | 데이터 그래프가 명시한 shape 조건을 만족하는지 검사하는 W3C 언어 | 작성하지 않은 조건까지 검사하지 않음 | [M5](M5_validation.md#m5-02) |

## 획득·통합·품질·운영

| 용어 | 핵심 의미 | 사례·주의 | 본문 |
|---|---|---|---|
| Mapping | 원천 구조와 목표 표현의 대응 | used_document의 업무 의미 확인 | [M3](M3_acquisition.md#m3-02) |
| R2RML | 관계형 자료의 RDF 매핑을 기술하는 W3C 언어 | 모든 데이터를 반드시 복제하라는 뜻은 아님 | [M3](M3_acquisition.md#m3-02) |
| Parsing / Extraction | 형식에서 내용을 읽기 / 의미 있는 항목을 얻기 | 표 열 읽기 오류와 관계 해석 오류를 분리 | [M3](M3_acquisition.md#m3-03) |
| Tacit knowledge / Elicitation | 경험·숙련에 포함된 지식 / 이를 드러내기 위한 활동 | 기록된 경험은 즉시 공식 절차가 되지 않음 | [M3](M3_acquisition.md#m3-04) |
| Entity resolution | 여러 설명이 같은 대상을 가리키는지 판단하는 문제 | 유사도와 동일성은 다름 | [M4](M4_integration.md#m4-01) |
| Blocking | 매칭할 후보 쌍을 좁히는 단계 | 후보에서 정답이 빠질 수 있음 | [M4](M4_integration.md#m4-03) |
| Ontology learning | 개념·관계·계층 등 모델의 일부를 찾아 만드는 작업 | 모델에 개별 사건을 추가하는 것과 구분 | [M4](M4_integration.md#m4-06) |
| Ontology alignment | 서로 다른 모델의 개념·관계를 대응시키는 작업 | 이름이 비슷하다고 의미가 같지는 않음 | [M4](M4_integration.md#m4-06) |
| Ontology population | 모델에 맞는 개체·사실을 채우는 작업 | 모델 생성과 다른 평가 과제 | [M4](M4_integration.md#m4-06) |
| Auto ontology | 자동 모델 생성·정렬 등을 가리키는 다양한 표현 | 프로젝트별 자동화 범위 확인 필요 | [M4](M4_integration.md#m4-06) |
| Claim / Evidence | 검토할 주장 / 그 주장을 지지하는 근거 | 원문 존재와 내용 지지는 다름 | [M5](M5_validation.md#m5-03) |
| Precision / Recall | 출력 중 정답 비율 / 전체 정답 중 찾은 비율 | 두 분모를 바꾸어 읽지 않음 | [M5](M5_validation.md#m5-06) |
| Provenance / Lineage | 생성·변환·책임의 출처 정보 / 데이터의 흐름·의존 관계 | 용례가 겹치며 URL 하나보다 넓게 다룸 | [M6](M6_lifecycle.md#m6-03) |
| PROV-O | Entity·Activity·Agent 등의 출처 관계를 표현하는 W3C ontology | 여기서 Agent는 LLM Agent에 한정되지 않음 | [M6](M6_lifecycle.md#m6-03) |
| Valid time / Known time | 업무적으로 적용되는 시간 / 서비스가 알게 된 시간이라는 사례 구분 | D02는 발효 후에 수집됨 | [M6](M6_lifecycle.md#m6-01) |
| Materialization / Virtual access | 결과를 만들어 저장 / 원천을 질의하여 접근 | 갱신 지연·원천 부하 등 선택 조건 비교 | [M6](M6_lifecycle.md#m6-06) |

**헷갈리면 먼저 비교할 다섯 쌍:** 이름과 대상 · 종류와 부품 · 추론과 검증 · 가설 기록과 사실 승인 · 문서 발효와 서비스 수집.
