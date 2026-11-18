# U12 자동 온톨로지 독립 기술·설명 검토

2026-11-19. [무엇을 학습하는가](../units/U12/01-what-gets-learned.md), [문서에서 후보를 만들기](../units/U12/02-documents-to-ontology.md), [검토와 배포](../units/U12/03-review-and-release.md), [NVIDIA 사례](../units/U12/04-nvidia-auto-ontology.md)의 총 30,020자와 [fixture](../examples/auto-ontology/inspection.json) 및 [근거 기록](../research/U12-notes.md)을 독립적으로 읽었습니다.

## 사례 결과에 영향을 주는 수정

| 위치 | 확인한 문제 | 수정 후 확인할 결과 |
| --- | --- | --- |
| L03 57행, I-43의 검사 결과 | “I-43은 이관분으로 검사 결과에서 제외됩니다”가 바로 위의 Q3 확정 검사 2건과 충돌하는 것으로 읽힙니다. fixture와 스크립트에서 I-43은 판정값 검증만 범위 밖이고, 확정 검사 기록 집계에는 포함됩니다. | “신규 I-99는 판정값 검증에서 반려됩니다. 이관된 I-43은 이 검증의 적용 대상에서 제외되지만 Q3의 확정 검사 기록 수에는 포함됩니다”처럼 각각의 검사를 표시합니다. |
| L02 D4#1, L03 44·46행, fixture의 날짜 | 발행일을 기준으로 신규 확정 기록을 검사한다고 서술하지만, fixture의 하나뿐인 `date`를 10월 업무 기록 질의와 신규 발행 규칙이 같이 사용합니다. 예제의 I-51 10월 12일이 검사일과 발행일을 겸한다는 가정이 빠져 있습니다. 검사일과 발행일이 경계를 사이에 두면 다른 판정이 가능합니다. | 교육 예제에서는 두 날짜를 동일하게 놓았다고 밝혀 검산 범위를 명시하거나 `issued_on`을 분리하고 발행일 경계 반례를 추가합니다. I-43 이관 예외는 두 날짜와 별도로 유지합니다. |
| L02 40–68행, K06의 근거 필드 | 프롬프트가 “근거 구간이 없으면 evidence를 빈 배열로 둔다”고 했는데, K06 JSON에는 원인을 확인할 수 없다는 D3#2가 evidence로 들어갑니다. 이 잘못된 연결을 설명하려는 모의 출력은 아래에서 분명하지만, “두 항목 모두 형식은 맞고 원문이 연결돼 있습니다”만 읽으면 프롬프트 지시까지 충족한 것으로 오해할 수 있습니다. | K06은 형식상 유효하더라도 근거 선택은 지시를 어겼다고 명시합니다. D3#2를 ‘후보가 참고한 위치’로 유지하면, 승인기에서는 원인 주장의 증거로 인정할 수 없음을 보여 줍니다. |

## 개념·예제 대조

- L01의 클래스와 개체, 스키마 유도와 모델 합의, 원천 매핑과 모델 간 정렬, KG 구축 범위를 서로 다른 입력·산출물로 설명합니다. 두 방법의 공통점과 실제 E-17의 오류를 모두 보여 줍니다.
- L02의 역순환은 OWL에서 곧바로 모순이라는 설명을 피하고, 두 포함의 의미를 집합 범위 일치로 풀었습니다. 후보 개념과 개별 자산의 ID, 대체 이름과 개체 병합, 클래스·속성·제약을 각각 구별합니다. 원문 범위가 없는 인과 후보의 기각 역시 질문과 예에 연결됩니다.
- L03의 K01·K02·K05·수정 K07 변경 목록은 fixture에서 확인할 수 있습니다. 표의 자동화 단계에서 담당자가 알아야 할 근거·승인·회귀 책임을 부여했습니다. SHACL의 `minCount`와 `maxCount`는 RDF 그래프에서 포커스 노드의 값 노드 개수를 평가합니다. Python fixture에서 쓰는 0·1·2 판정 예제는 둘째 위반의 값이 서로 다르므로 해당 효과와 일치합니다. [W3C SHACL §4.2](https://www.w3.org/TR/shacl/#core-components-count)
- LLMs4OL 원본 §3 및 §4.1·4.3의 표 3과 대조했습니다. A는 WordNet 등에서 용어 유형 지정, B는 방향 있는 유형 쌍의 하위 여부, C는 지정 비계층 관계의 유형 쌍 판정입니다. WordNet GPT-3.5 91.7, UMLS C Flan-T5-XL 제로샷 49.5와 미세조정 53.1은 표와 일치합니다. 표의 측정으로 판정할 수 없는 엔드투엔드 승인·배포 성능을 주장하지 않습니다. [LLMs4OL arXiv v2](https://arxiv.org/html/2307.16648v2#S4.T3)
- `python learning-v2/examples/auto-ontology/verify.py`를 독립 실행했습니다. v1.1의 Q1은 I-51·적합, Q2는 E-17·E-18, Q3은 확정 기록 2·요청 1입니다. 이관 I-43은 검증 적용 대상 밖이며, 0값·2값 모의 신규 행은 위반입니다. SQLite에서 2행·100이 조인으로 4행·200이 됐습니다.

## NVIDIA 프로젝트 확인

- `git ls-remote https://github.com/NVIDIA/auto-ontology.git HEAD`로 현재 공개 HEAD가 본문과 같은 `778ccdef75536bee5653306f8ded655924e4ada8`임을 재확인했습니다. 해당 체크아웃의 `run_ingest`, `process_table`, `extract_term`, `_run_semantic_compilation`, `semantic_fk`, `check_query`, 모델 교환 `router`와 `service`를 대조했습니다. 도구의 기능과 합성 데이터의 진실성 검토가 구별됩니다. [공식 아키텍처](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/docs/architecture.md)
- 값 조인 검사는 적어도 한 행을 돌려주는지 확인하며, 일반 질의가 예외를 내면 텍스트 캐스팅을 시도합니다. 문서와 코드가 선언 관계를 우선하고 연결·설정에 따라 검사를 수행하는 설명과 맞습니다. 동작하는 질의도 집계 단위를 위반할 수 있다는 합성 예를 확인했습니다. [코드의 조인 검사](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/semantic/semantic_fk.py#L753)
- 문서의 `check_answerable`은 질문의 개체를 추출하고 후보를 찾은 뒤 거리 기준 내 후보가 있는 개체 비중을 계산합니다. 질문 처리 시 에이전트가 사용할 수 있는 MCP 기능이며, 일반 채팅에 항상 앞서 실행되는 단계로 설명하지 않습니다. `check_query`는 카탈로그·검색 테이블 범위를 검사합니다. YAML과 선택적인 Ossie ZIP은 서로 다른 출력이고 세 문서 구성은 코드와 일치합니다. [답변 가능성 검사](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/docs/architecture.md#check-answerability), [내보내기 구현](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/server/model_interchange/service.py#L198)
- NVIDIA 서버·모델 재실행과 웹 화면 검증은 이 기술·독해 검토에 포함하지 않았습니다. 정확성을 결정하는 근거 조각과 일반 공리를 독자가 본문만으로 구별할 수 있습니다.
