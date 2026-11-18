# 기업 지식을 이해하고 구축하는 학습 교재

Knowledge Graph·Auto ontology·RAG의 우선 범위를 확장하고 본문과 예제가 연결된 학습 웹으로 제공합니다. 자동 KG 구축 survey는 세 수업의 별첨입니다. 나머지 기초·운영·통합 단원은 계속 확장하고 있습니다.

[학습 웹 시작](../web/dist/index.html)에서 전체 작성 수업과 본문 검색을 이용할 수 있습니다. 이미 그래프·RDF 기초를 공부했다면 U08 지식 모델링 → U09~U11 구축·검토 → U12 자동 온톨로지 → U13~U16 검색·평가 순으로 읽습니다. S01은 U09 이후 병행하면 좋습니다.

## 우선 학습 범위

| 영역 | 읽기 시작 | 배우는 과정 |
|---|---|---|
| Knowledge Graph | [U08 연결된 지식](units/U08/01-from-links-to-knowledge.md) | 모델·주장·근거 → 정형 매핑과 문장 추출 → 개체 정합과 통합 → 검증·검토·암묵지 |
| Auto ontology | [U12 무엇을 학습하는가](units/U12/01-what-gets-learned.md) | 일반 모델과 개별 사실 → 개념·공리 후보 → 평가·개정 → NVIDIA 프로젝트의 의미 계층 |
| RAG | [U13 검색 추적](units/U13/01-retrieval-trace.md) | Vector·혼합 검색과 문맥 → 관계 경로·Microsoft GraphRAG → RAPTOR 계층 → 공정한 평가 |
| 논문 별첨 | [S01 survey 읽기](units/S01/01-reading-map-and-acquisition.md) | 획득 → 학습 기법·정제 → 조건·변화·저장 및 대표 기법의 평가 |

## 지금 읽을 수 있는 수업

- [기업은 무엇을 기억하고 설명해야 할까요](units/U01/01-company-memory.md)
- [같은 질문을 표와 그래프로 따라가기](units/U02/01-same-question-two-models.md)
- [속성 그래프의 노드·관계와 Neo4j](units/U03/01-property-graph.md)
- [RDF의 식별자·값·타입·구문을 처음부터 읽기](units/U04/01-rdf-language.md)
- [반복 사건을 RDF와 속성 그래프로 표현하기](units/U04/02-events-and-property-graphs.md)
- [사건·주장·문서·named graph 구분하기](units/U04/03-statements-and-context.md)
- [장비 정비 기록에서 도메인 온톨로지 설계하기](units/U05/01-domain-model.md)
- [추론과 검증이 다른 결과를 내는 이유](units/U06/01-inference-and-validation.md)
- [연결망에서 Knowledge Graph로 발전시키기](units/U08/01-from-links-to-knowledge.md)
- [정비 질문 한 건을 Vector RAG 안에서 추적하기](units/U13/01-retrieval-trace.md)

기본 문법에 익숙하다면 두 번째 수업부터 읽고, 모르는 표기가 나오면 첫 수업에서 정확한 위치를 찾으세요. 데이터 모델의 비교를 배운 뒤에는 세 번째 수업에서 출처와 사실 채택의 문제로 발전시킵니다. 각 수업에는 설명 문제와 해설이 있습니다.

새 교재의 전체 범위는 [단원별 제작 명세](../rebuild/CURRICULUM_BLUEPRINT.md), 실제 진행 상태는 [STATE.json](../rebuild/STATE.json)에서 확인할 수 있습니다. 출처는 본문 해당 설명 가까이에 제공하고, 제작 중 실제 확인한 범위는 research/에 기록합니다.

위 목록은 작성된 수업이며 단원 전체가 모두 완성됐다는 뜻은 아닙니다. RDF·ontology·RAG의 대표 설명 방식을 먼저 작성했고, 기초와 응용을 연결하는 나머지 수업을 이어서 제작합니다. 화면 구성 비교는 [읽기 화면 세 가지](../rebuild/prototypes/index.html)에서 확인할 수 있습니다.

사용자가 선택한 B안으로 이어 읽을 수 있는 [개편 중 학습 화면](../rebuild/reader/dist/index.html)을 제공합니다. 현재 작성된 수업을 연결한 로컬 통합본입니다.

## 예제의 의미

장비 코드·운행·문서·사건은 합성 자료입니다. 일반 개념을 설명하기 위한 예시이며 실제 반도체 작업 지침이나 원인 분석 결과가 아닙니다. 실행한 파싱·질의와 손으로 도출한 결과, 모의 검색 값은 구분하여 표시합니다.
