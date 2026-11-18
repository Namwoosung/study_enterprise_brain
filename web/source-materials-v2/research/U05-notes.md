# U05 모델 설계 수업 조사 기록

2026-11-18 확인. B01 표본에 해당하는 수업은 [장비 정비 기록에서 도메인 온톨로지 설계하기](../units/U05/01-domain-model.md)입니다. 이 기록의 상태는 **부분 초안 / 독립 검토 대기**입니다. 단원 전체 상태는 `ready`의 요건을 아직 충족하지 않았습니다.

## 읽은 자료와 확인한 주장

| 주장 ID | 확인한 자료와 본문 위치 | 확인한 주장과 적용 |
| --- | --- | --- |
| U05-C01 | Noy·McGuinness, *Ontology Development 101*, Stanford 기술 보고서 KSL-01-05, 2001, [PDF §1, p. 1](https://protege.stanford.edu/publications/ontology_development/ontology101.pdf#page=1) | 도메인의 어휘·관계·가정을 명시하면 사람과 시스템이 공유하고 재사용할 수 있습니다. 본문에서는 장비, 모델, 사건의 서로 다른 업무 의미를 사용했습니다. |
| U05-C02 | 같은 보고서 [§3 서두·Step 1, pp. 4–5](https://protege.stanford.edu/publications/ontology_development/ontology101.pdf#page=4) 및 [Steps 2–5, pp. 5–8](https://protege.stanford.edu/publications/ontology_development/ontology101.pdf#page=5)에서 목적/유지관리자, 역량 질문, 재사용, 용어 수집과 클래스·속성 의존 관계를 다룬 단락 | 질문이 필요한 범위와 표현 상세도를 정하는 데 쓰이고, 설계는 반복적으로 개정됩니다. 기존 어휘와 모델의 재사용을 후보로 검토한 뒤 사례의 정의와 대조하는 방식으로 적용했습니다. |
| U05-C03 | 같은 보고서 [§4.1의 is-a와 계층 전이, pp. 12–13](https://protege.stanford.edu/publications/ontology_development/ontology101.pdf#page=12) 및 [§4.6의 적용 목적과 표현 수준, p. 18](https://protege.stanford.edu/publications/ontology_development/ontology101.pdf#page=18), [OWL 2 Primer §4.1–4.2](https://www.w3.org/TR/owl2-primer/#Classes_and_Instances) | 하위 클래스에 속하는 각 개체는 상위 클래스에도 속합니다. 특정 제품 모델을 어떻게 표현할지는 표현하려는 정보와 답하려는 질문에 따라 달라집니다. |
| U05-C04 | *SKOS Simple Knowledge Organization System Reference*, W3C Recommendation, 2009-08-18, [§3.5.1](https://www.w3.org/TR/skos-reference/#concepts), [§5.1–5.5](https://www.w3.org/TR/skos-reference/#labels), [§8.1–8.3, §8.6.6](https://www.w3.org/TR/skos-reference/#semantic-relations) | SKOS의 대체·대표 이름, 직접 포괄 관계, 개념과 OWL 클래스의 형식적 구별을 확인했습니다. `skos:broader`와 `skos:broaderTransitive`의 의미 차이도 확인했으나 본문은 직접 포괄 링크와 하위 클래스의 차이에 집중합니다. |
| U05-C05 | *OWL 2 Web Ontology Language Primer (Second Edition)*, W3C Recommendation, 2012-12-11, 설명용 문서, [§2](https://www.w3.org/TR/owl2-primer/#What_is_OWL_2.3F), [§3](https://www.w3.org/TR/owl2-primer/#Modeling_Knowledge:_Basic_Notions), [§4.1–4.2](https://www.w3.org/TR/owl2-primer/#Classes_and_Instances), [§4.4의 객체 속성 도입](https://www.w3.org/TR/owl2-primer/#Object_Properties) | 공리, 개체 소속, 하위 클래스, 개체 간 관계를 직접 예로 확인했습니다. 추론과 문서 입력 구조 요구의 차이를 본문에서 교체 시간 입력 요구와 부품 교체의 분류로 대조했습니다. |

Stanford의 가이드는 당시 프레임 기반 도구를 예로 든 설계 자료입니다. [Stanford HTML §4.1](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html)의 한 문장은 하위 클래스 방향을 뒤집어 표시합니다. 같은 HTML §3 Step 4, PDF §4.1과 W3C OWL 2 Primer §4.2의 일치한 방향을 적용했습니다. Stanford의 슬롯 제약을 OWL 입력 검증처럼 옮기는 설명도 피했습니다.

SKOS Reference의 개념-클래스 분리 설명은 한쪽을 선언하면 다른 쪽을 자동으로 얻지 않는다는 의미로 적용했습니다. 형식에 따라 두 표현을 결합할 수도 있습니다. OWL 2 Primer는 Recommendation으로 발행된 설명용 문서이며, 정식 의미론이나 OWL 프로파일 전체를 확인한 상태는 아닙니다.

## 예제와 확인 범위

- 장비, 모델, 펌프, 장착 시각, 작업지시, 수행과 경보는 합성입니다. 장착의 효력 구간과 작업 건수의 집계 단위도 해당 사례의 합의입니다.
- 두 장비의 공통 모델 `M-20`, 두 개의 장착 구간, 두 수행 사건과 취소된 지시, 두 경보와 한 결함 확인을 기준으로 Q1–Q8의 답을 대조했습니다. 10:30 시각은 종료·시작이 같은 경계이고, 포함·제외를 적용하면 `P-17`만 남습니다. Q7의 ‘최초 설치’와 Q8의 미래 시점은 확보한 자료와 질문 범위의 한계를 드러냅니다.
- 본문의 장착과 교체 경로, 표의 키와 예시 화살표를 수작업으로 대조했습니다. DB에 적재하거나 OWL 추론기를 실행한 결과는 없습니다. 클래스 포함 결론은 OWL 2 Primer의 의미에 따라 손으로 도출했습니다.

## 다음 작업

1. 표본에 대한 독립 기술·설명 검토를 진행하고, 발견한 설명 공백과 수정 위치를 단원 검토 기록에 남깁니다.
2. 별도 수업에서 공개 원천 모델 재사용의 실제 판단과 용어 정렬, 공리의 버전 개정·회귀 검사를 다루고 KG survey 근거를 확인합니다.
3. 표본을 본편에 편입할 때 기준 예제 데이터와 재사용할 도해의 정합성을 확인합니다.
