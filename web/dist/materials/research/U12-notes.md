# U12 자동 온톨로지 조사와 예제 검증

확인일 2026-11-19. [무엇을 학습하는가](../units/U12/01-what-gets-learned.md), [문서와 후보](../units/U12/02-documents-to-ontology.md), [검토와 적용](../units/U12/03-review-and-release.md), [NVIDIA 사례](../units/U12/04-nvidia-auto-ontology.md). 독립 검토와 웹 구현 상태는 별도 관리합니다.

## 근거와 확인 범위

| 주장 ID | 읽은 근거 | 적용과 제한 |
| --- | --- | --- |
| U12-C01 | [Text2Onto, Cimiano·Völker, §2.1–2.4 및 §3](https://noah.nrw/ubbihs/download/pdf/5124767), [Cimiano, *Ontology Learning and Population from Text*](https://link.springer.com/book/10.1007/978-0-387-39252-3) | Text2Onto의 모델링 원형, 텍스트 기반 추출, 사용자 상호 작용, 말뭉치 변경을 후보 변경으로 추적하는 방식을 확인했습니다. 단원 예시의 후보 ID와 증거·승인 레코드는 자체 교육 설계입니다. |
| U12-C02 | [Hearst, 1992, §2](https://aclanthology.org/C92-2082.pdf#page=2), [Noy·McGuinness, *Ontology Development 101*, §3](https://protege.stanford.edu/publications/ontology_development/ontology101.pdf#page=4) | 문장 패턴으로 하위어를 찾는 접근과, 목적·역량 질문·재사용 모델로 범위를 좁히는 접근을 구별했습니다. 본문의 자산 번호 구별과 누락 문서 표본은 합성 예입니다. |
| U12-C03 | [Zhong 외, 자동 KG 구축 survey §2.1, §4, §5.2, §6](https://arxiv.org/html/2302.05019), [W3C R2RML §2의 표 매핑 예](https://www.w3.org/TR/r2rml/#overview) | KG 구축 전체와 개체 획득·정합·융합·변경의 관계 및 표에서 그래프를 만드는 매핑을 구별했습니다. 사내 매핑·정렬 정책은 수업의 예입니다. |
| U12-C04 | [LLMs4OL arXiv:2307.16648v2 §3, §4.1](https://arxiv.org/html/2307.16648v2#S3) | 개념적 여섯 단계와 평가한 A/B/C를 구별했습니다. A는 용어의 유형, B는 방향이 있는 타입 쌍의 분류 관계와 간접 포함, C는 지정된 비계층 관계의 타입 쌍 판정입니다. 원논문의 과제 번호를 사용했고 후속 대회 번호를 가져오지 않았습니다. |
| U12-C05 | [LLMs4OL v2 §3 및 §4.3 표 3, §5](https://arxiv.org/html/2307.16648v2#S4.SS3) | 프롬프트 템플릿과 제로샷·미세조정 범위를 확인했습니다. A/GPT-3.5/WordNet MAP@1은 91.7%, C/Flan-T5-XL/UMLS F1은 제로샷 49.5% 및 미세조정 53.1%입니다. 여기서 A와 C의 수치는 지표와 과제 데이터가 다르고 엔드투엔드 승인·운영 효과를 측정하지 않습니다. 본문 수치는 실험 재현 없이 원 표를 인용했습니다. |
| U12-C06 | [OWL 2 Primer §4.1, §4.2, §4.4, §4.5](https://www.w3.org/TR/owl2-primer/), [OWL 2 Direct Semantics §2.3–2.4, §3](https://www.w3.org/TR/owl2-direct-semantics/), [SHACL Recommendation §2.1, §4.2](https://www.w3.org/TR/shacl/) | 개체의 유형과 클래스 포함, 포함 양방향이 뜻하는 범위 동치, domain/range의 추론, 열린 세계에서의 존재와 실제 입력의 개수 검사 차이를 확인했습니다. 업무 날짜·이관분 정책을 선택한 이유는 D4#1입니다. |
| U12-C07 | [NVIDIA README Quickstart/How it works](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/README.md), [architecture Generate/Answer/Check answerability](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/docs/architecture.md), [`run_ingest`](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/ingestion_service/ingest.py#L82), [`extract_term`](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/semantic/term_extractor.py#L237), [`_run_semantic_compilation`](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/semantic/compile.py#L49) | 데이터베이스 카탈로그·임베딩 쓰기, 후보 열을 받는 프롬프트·대체 경로, 컴파일 순서와 공식 예시의 결과 형태를 확인했습니다. 제품 서버 및 모델 호출과 제품 성능 측정은 하지 않았습니다. |
| U12-C08 | [외래 키 해석](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/semantic/semantic_fk.py#L152), [조인 행 존재 검사](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/semantic/semantic_fk.py#L753), [`check_query`](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/retrieval/text_to_sql/react/run_sql.py#L355), [`submit`](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/retrieval/text_to_sql/react/loop.py#L81) | 선언 관계 우선, 설정과 연결 여부에 따른 확인, SQL 파싱·카탈로그·검색 범위 검사를 확인했습니다. 반복 주문 조인의 집계는 독자 설명용 합성 SQL입니다. |
| U12-C09 | [교환 스키마](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/server/model_interchange/schemas.py#L15), [교환 서비스](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/server/model_interchange/service.py#L198), [용어 편집 라우터](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/server/terms/router.py#L204) | native YAML·Ossie YAML·선택적 세 문서 ZIP과 용어 검토 속성의 구현을 확인했습니다. 선택적으로 내보낸 Ossie ontology와 함께 자동 생성된 OWL 공리나 OWL 추론기를 제공한다고 해석하지 않습니다. |

NVIDIA 확인은 `git ls-remote https://github.com/NVIDIA/auto-ontology.git HEAD`와 공개 저장소의 임시 폴더 shallow clone으로 했습니다. 두 결과가 모두 `778ccdef75536bee5653306f8ded655924e4ada8`이었고 커밋 작성 기록은 `2026-11-18T10:20:28-06:00`입니다. 본문 핀과 코드 라인 번호는 해당 작업 트리에서 대조했습니다.

## 실제 예제 확인

- [원천·모델·후보 fixture](../examples/auto-ontology/inspection.json)의 여덟 문장과 후보 ID를 수업과 대조하는 [검증 스크립트](../examples/auto-ontology/verify.py)를 실행했습니다.
- L02의 Turtle 블록을 RDFLib 7.6.0으로 파싱해 RDF 트리플 10개를 읽을 수 있음을 확인했습니다.
- `python learning-v2/examples/auto-ontology/verify.py`로 기준과 개정 모델의 Q1–Q3, 항목의 대장 상위 타입 소속, K04를 넣었을 때 클래스 포함의 양방향 경로를 확인했습니다. v1.1은 I-51·적합, 공정 장비 E-17·E-18, 확정 검사 2·요청 1입니다. 검증은 교육용 명명 클래스 도달 가능성 계산이며 범용 OWL 추론기 실행이 아닙니다.
- 신규 발행 규칙에서 판정 1개인 I-51은 통과, 이관 I-43 및 요청 R-52는 검사 범위 밖, 합성 신규 I-99(0개)와 I-98(2개)는 위반입니다. Python에서 조건을 확인했으며 SHACL 엔진 실행을 주장하지 않습니다.
- 같은 스크립트의 인메모리 SQLite 쿼리로 항목 2행 합계 100과 주문 코드로 조인한 4행 합계 200을 확인했습니다. 실행 환경은 Python 3.14.6, SQLite 3.50.4입니다. 이 실행은 제품의 SQL 생성이나 추론 정확도 평가와 별개입니다.

## 남은 검토

각 설명의 독립 기술·독해 검토와 승인된 학습 웹의 도해, 모바일 레이아웃 및 도해·본문 일치 검증을 별도로 기록합니다. 외부 모델 결과는 LLMs4OL 원 표와 NVIDIA 공식 예시에 한해 인용하며 이 단원 작업에서 재현하지 않았습니다.
