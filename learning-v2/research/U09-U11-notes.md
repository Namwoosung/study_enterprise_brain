# U09–U11 근거와 확인 기록

2026-11-19. 범위는 정형·반정형·비정형 원천에서 후보를 만들고, 동일성을 검토한 뒤, 품질·사람 검토·암묵지를 관리하는 세 단원입니다. 예제의 표시 코드, 설비, 문서, 추출·매칭 결과, 심사 시간, 인터뷰 내용은 모두 교육용 합성입니다.

## U09 근거

| 본문의 기술 주장 | 읽은 근거 및 범위 | 이 교재의 적용과 제한 |
|---|---|---|
| 본문 추출과 표의 구조 해석은 별도 문제 | [자동 KG 구축 survey §3.1–3.2](https://arxiv.org/html/2302.05019#S3), [pypdf 공식 문서 Why Text Extraction is hard와 OCR vs. Text Extraction](https://github.com/py-pdf/pypdf/blob/main/docs/user/extract-text.md) | 표·캡션·각주에서 다른 단서가 사라질 수 있습니다. pypdf나 OCR을 이 합성 PDF 경로에서 실행하지 않았습니다. |
| 관계형 행의 주소·멤버 속성과 조인에서 RDF를 생성 | [W3C R2RML 2012 Recommendation §1, §4.1, §5, §6.1–6.3, §7.2–7.4, §8 및 §11.1–11.2](https://www.w3.org/TR/r2rml/) | 북동·남동의 두 열 조인과 존재하지 않는 목적어를 전개했습니다. 처리기의 가상 제공·물질화 구현을 규격이 허용한다는 점만 보장합니다. R2RML 엔진 출력은 예상 결과입니다. |
| 언급 탐지, 유형, 목록 연결, 공지시는 다른 결과 | [자동 KG 구축 survey §4.1.1–4.1.3 및 §4.2](https://arxiv.org/html/2302.05019#S4) | 서로 다른 유형의 신호, 기준 목록·문서 안 묶음 차이를 반영했습니다. 적합한 ID가 없는 경우 문서 임시 대상을 보존하는 것은 운영 설계 예입니다. |
| 사전 범주와 자유 표현의 관계 추출, 문장 경계와 사건 역할 | [자동 KG 구축 survey §4.3.1–4.3.3, §4.3.6](https://arxiv.org/html/2302.05019#S4.SS3), [Wadden et al. 2019 §2 Task and Model 및 §3 평가](https://aclanthology.org/D19-1585.pdf) | 사건 단서와 역할 분해, 관계 분류와 평가 기준을 참고했습니다. 연구 모델의 성능을 비교하거나 본문 예제에 전이하지 않았습니다. |
| 사실과 조건의 연결을 각각 다룰 수 있음 | [자동 KG 구축 survey §6.1](https://arxiv.org/html/2302.05019#S6.SS1) | 근거가 지시하는 확정·부정·가설·조건의 별도 보존을 정비 합성 사례에서 보여줍니다. 모델에 따라 지원 범위가 다릅니다. |
| 구조화 출력의 필요한 필드와 타입 제약 | [Understanding JSON Schema, object의 properties·required 항목](https://json-schema.org/understanding-json-schema/reference/object) | 조건부 계획의 예시 JSON은 수작업 생성입니다. 특정 LLM, 제약 생성 엔진, 판단 성능을 실측하지 않았습니다. |

## U10 근거

| 본문의 기술 주장 | 읽은 근거 및 범위 | 이 교재의 적용과 제한 |
|---|---|---|
| ER에서 블록 후보·판정·클러스터는 별도이며, 틀린 연결이 전이로 파급 | [Christophides et al., End-to-End Entity Resolution for Big Data §2, §3 도입, §5 도입과 Preliminaries, §6 Connected Components와 Multi-source ER 단락](https://arxiv.org/html/1905.06397) | 10개 레코드의 쌍과 클러스터를 따로 확인했습니다. 논문의 벤치마크는 숫자 근거로 쓰지 않았습니다. |
| KG fusion에는 속성 정렬과 동일 개체 연결 등이 포함 | [자동 KG 구축 survey §5.2.1–5.2.3](https://arxiv.org/html/2302.05019#S5.SS2) | 스키마 의미를 먼저 맞춘 뒤 여러 행의 후보를 비교했습니다. 대표 레코드와 원천 주장, 시점·정정을 보존하는 방안은 예제의 운영 설계입니다. |
| OWL에서 같은 개체임을 선언하는 것의 의미 | [OWL 2 RDF Mapping 2012 Recommendation §2 표 1의 SameIndividual 대응](https://www.w3.org/TR/owl2-mapping-to-rdf/), [OWL 2 Direct Semantics 2012 Recommendation §2.3.6 표 10](https://www.w3.org/TR/owl2-direct-semantics/#Assertions) | 두 이름을 같은 실물에 붙이는 선언의 함의를 설명했습니다. 문자열 별칭과 원천 레코드 간 참조에는 다른 관계를 씁니다. OWL 엔진을 실행하지 않았습니다. |

## U11 근거

| 본문의 기술 주장 | 읽은 근거 및 범위 | 이 교재의 적용과 제한 |
|---|---|---|
| SHACL은 모양과 데이터의 관계를 검사하며 보고서는 검사 범위를 갖는다 | [W3C SHACL 2017 Recommendation §2.1.3, §3.4–3.6, §4.1.3, §4.2.1](https://www.w3.org/TR/shacl/) | 최소 근거 IRI 모양과 대상 선택을 적용한 **예상 결과**입니다. 원문의 충실성이나 세계 사실 검증은 별도로 정의했습니다. |
| 데이터 품질을 여러 관점과 지표로 기록 | [Zaveri et al. §4.2의 syntactic validity·semantic accuracy와 나머지 품질 차원 구획](https://journals.sagepub.com/doi/10.3233/SW-150175), [DQV 2016 Working Group Note §4.3–4.5 및 §4.8–4.10](https://www.w3.org/TR/vocab-dqv/) | 후보 검사 여섯 가지는 교재의 편집 분류입니다. DQV는 지표·측정 기록의 어휘이며 운영 임계값이 주어지지는 않습니다. |
| Active learning은 학습용 라벨을 적극적으로 고르며, 불확실성은 그 전략 중 하나 | [Settles, Active Learning Literature Survey §1.2, §2.3, §3.1](https://research.cs.wisc.edu/techreports/2009/TR1648.pdf) | 학습과 품질 추정 표본의 목표가 다름을 설명했습니다. 검토 대기열·가중 표본 숫자는 교육용 설계입니다. |
| 중요한 경험과 결정 배경의 기록, 사건 뒤 기대와 실제 비교 | [Flanagan 1954, 도입 327쪽과 연구 배경](https://www.analytictech.com/mb870/readings/flanagan.pdf#page=1), [NASA Knowledge Management의 critical knowledge 안내](https://www.nasa.gov/learning-resources/for-professionals/appel-knowledge-management/), [Space Shuttle Tacit Knowledge Capture 소개](https://www.nasa.gov/history/history-publications-and-resources/oral-histories/space-shuttle-tkc/), [NASA AAR 1–2쪽](https://www.nasa.gov/wp-content/uploads/2025/09/after-action-review-v3.pdf), [NASA Knowledge Transfer의 tacit/explicit 설명](https://www.nasa.gov/wp-content/uploads/2025/09/knowledge-transfer.pdf) | 사례의 구체적 행동을 묻는 중요 사건 접근과 NASA의 목적과 절차를 확인했습니다. 질문 표와 E17 판정은 합성 기록팀 사례입니다. |

## 실제 실행과 자가 확인

- 저장소에서 `py learning-v2/examples/construction/verify.py`를 실행했습니다. Python 3.14.6, SQLite 3.50.4에서 종료 코드 0이었습니다. U09의 정형 조인 3행과 잘못된 단일 키 조인의 두 구역, 1.3 W의 값, 13개 span, 합성 주장 정밀도·재현율 3/5를 검산했습니다.
- 두 시설의 동일 이름과 시설별 N03이 처음 등장하는 곳을 대조했습니다. U09는 Q-17에 북동 링크를 제안하면서 문서 안 장비 공지시와 대장 링크를 분리합니다. U09의 부품은 문서 안 임시 ID이고 U10은 나중에 들어온 서명 등록부로 실물 ID를 판정합니다. 적용 조건·비동시 시간값·가설이 사건 확정으로 변경되지 않는지 확인했습니다.
- U10의 10개 레코드에서 전체 45쌍, 초기 후보 9쌍, 같은 실물 쌍 4/5 포함, 대응표 확인 후 10쌍과 5/5 포함을 확인했습니다. 잘못된 연결 성분에서 여섯 개의 틀린 동일성을 얻었고 철회 후 정답 그룹을 재현했습니다.
- U11의 전수·위험별 정책 936분·344분과 360분 용량, 분기 이동 시 404분, 별도 이중 검토 시 368분을 확인했습니다. 층화 표본의 가중 추정 1/13과 현지 날짜→UTC 세 건을 확인했습니다. 주어진 작업시간을 이용한 산술 검사는 실제 대기시간·심사 정확도·암묵지 전달 효과를 측정하지 않습니다.
- 표현 점검에서 정규화 규칙 오류의 파급, 근거가 있는 주장과 실제 사건의 차이, 워크플로우의 보류와 반려, 후보 점수와 확률의 관계를 읽기 흐름 안에서 점검했습니다. 문장 몇 곳의 모호한 표현과 오탈자를 수정했습니다.

## 독립 검토와 수정

- [U09 독립 검토](../reviews/U09-priority-review.md)의 C2 span 지적을 반영했습니다. 13개 언급에 더해 S2의 두 단서 표현 좌표를 검산합니다. 작업 이름과 설명 절을 구분하고 채점 fixture의 A-17 미관찰 라벨도 수정했습니다. 검토자의 RDFLib 7.6.0 파싱은 R2RML 매핑 **구문** 24개 트리플을 확인했습니다.
- [U10 독립 검토](../reviews/U10-priority-review.md)의 지적에 따라 `owl:sameAs` 예문에서 비교 대상이 원천 레코드가 가리키는 장비 IRI임을 명시했습니다.
- [U11 독립 검토](../reviews/U11-priority-review.md)의 지적에 따라 T1의 교대 메모·검색 설정의 버전과 위치를 보완했습니다. 중요 사건 접근의 원논문 근거를 추가했습니다. 검토자는 RDFLib 7.6.0과 pySHACL 0.40.2로 원고의 모양에서 근거 없음·IRI·문자열·비대상의 네 경우를 각각 false·true·false·true로 확인했습니다.

웹 화면에서 표·코드 블록의 모바일 가독성과 탐색 흐름을 확인할 작업이 남습니다.
