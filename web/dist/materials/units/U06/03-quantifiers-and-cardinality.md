# ‘있다’, ‘모두’, ‘하나’는 입력 검사와 어떻게 다른가요?

“모든 정비 수행에는 사람이 담당한다”고 모델에 썼습니다. 담당자 값이 빠진 J17을 넣으면 오류일까요? 열린 세계의 존재 공리라면 그렇지 않을 수 있습니다. 이 수업에서는 존재·전칭·개수 제한이 각각 무엇을 요구하는지 작은 해석으로 따라가겠습니다. ‘온톨로지는 추론, SHACL은 검증’이라는 문장만 외우면 놓치기 쉬운 차이입니다.

## 열린 세계는 무엇을 모른다고 남기나요?

J17을 Maintenance로 알고 있지만 담당자 문장이 없다고 합시다. 지금 주어진 자료에서 알 수 있는 것은 J17이 정비라는 점과 **우리가 담당자 연결을 확보하지 못했다**는 점입니다. 다른 자료에 담당자가 있을 가능성을 배제하지 않습니다. OWL의 열린 세계 관점에서는 명시된 진술의 부재만으로 부정을 도출하지 않습니다. [OWL 2 Primer, Open World Assumption](https://www.w3.org/TR/owl2-primer/#Open_World_Assumption)

닫힌 자료 범위에서 “이 파일에 담당자 필드가 있나”를 검사하는 일은 가능합니다. SHACL로 현재 데이터 그래프의 값 개수를 검사하거나 애플리케이션에서 필수 값을 확인합니다. 같은 업무가 열린 세계 의미 해석과 제한된 입력 검증을 함께 사용할 수 있습니다. 어느 자료 묶음을 어느 시점에서 검사했는지를 표시해야 합니다.

## someValuesFrom: 조건에 맞는 값이 적어도 하나

다음은 “정비 수행마다 사람인 담당자가 적어도 한 명 있다”라는 존재 제한입니다.

```turtle
@prefix ex: <https://example.org/owl-lesson/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
ex:Maintenance rdfs:subClassOf [
  a owl:Restriction ;
  owl:onProperty ex:performedBy ;
  owl:someValuesFrom ex:Person
] .
ex:J17 a ex:Maintenance .
```

대괄호 `[...]`는 여기서 이름 없는 제한 노드를 만듭니다. `owl:Restriction`은 속성에 관한 조건을 표현하는 클래스 표현입니다. `onProperty`는 어떤 속성인지, `someValuesFrom`은 그 값 가운데 적어도 하나가 어느 클래스에 속하는지를 적습니다. J17이 정비이면 이 제한도 만족해야 합니다. [OWL 2 Structural Specification, Existential Quantification](https://www.w3.org/TR/owl2-syntax/#Existential_Quantification)

이 조건을 만족하는 해석에는 J17의 담당자인 어떤 사람이 있습니다. 그 사람이 우리가 아는 P1인지 P2인지는 결정되지 않습니다. 입력에 그 주소를 적지 않았어도 해석이 가능하므로 곧바로 불일관해지지 않습니다. 또한 이 의미만으로 저장소가 이름 붙인 새 사람 노드를 실제로 삽입해야 한다는 결론은 없습니다. 어떤 엔진은 필요한 존재를 내부적으로 다루고, 어떤 규칙 프로파일은 이 표현의 지원 범위가 다릅니다.

J17에 담당자 P1이 한 명 있고 P1이 Person이면 조건을 만족할 증거가 생깁니다. 담당자로 P1·P2 둘이 있으면 여전히 이 존재 조건을 만족할 수 있습니다. ‘적어도 하나’에는 ‘나머지도 모두 사람’이나 ‘오직 한 명’이 들어 있지 않습니다.

## allValuesFrom: 값이 있다면 그 값은 모두 조건에 맞음

같은 틀에서 `someValuesFrom`을 `allValuesFrom`으로 바꾸어 보겠습니다.

```turtle
@prefix ex: <https://example.org/owl-lesson/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
ex:Maintenance rdfs:subClassOf [
  a owl:Restriction ;
  owl:onProperty ex:performedBy ;
  owl:allValuesFrom ex:Person
] .
```

이 조건은 정비의 performedBy 값이 있으면 그 값이 모두 Person임을 뜻합니다. 값이 하나도 없을 때도 ‘사람이 아닌 담당자가 있다’는 반례가 없으므로 만족할 수 있습니다. **모두 사람**과 **사람이 존재**는 다른 말입니다. 정비 J18에 performedBy M17을 연결했는데 M17이 매뉴얼 문서라면, 이 제한으로 M17을 Person으로도 해석해야 합니다. 문서와 사람을 서로소로 선언해 두었다면 충돌이 생깁니다. 서로소가 없으면 두 타입을 가진 해석을 허용할 수 있습니다. [OWL 2 Structural Specification, Universal Quantification](https://www.w3.org/TR/owl2-syntax/#Universal_Quantification)

| 상황 | some Person | only Person |
|---|---|---|
| 알려진 연결이 없음 | 사람 담당자가 존재하는 해석을 요구, 이름은 미상 | 값의 존재 자체를 요구하지 않음 |
| P1 한 명이 연결되고 Person | 그 값으로 존재 조건을 충족 | 알려진 값은 조건에 맞음 |
| P1·P2 연결 | 최소 하나가 Person이면 존재 조건 충족 가능 | 둘 다 Person이어야 함 |

표의 `only Person`은 전칭 제한을 읽기 쉬운 말로 쓴 것입니다. 두 조건을 함께 선언하면 ‘사람인 값이 하나 이상 있고, 모든 값이 사람’이라는 효과가 생깁니다. 그래도 값이 한 명뿐이라는 뜻은 아닙니다.

## 정확히 한 명이면 두 주소가 들어올 때 어떻게 되나요?

다음 상황에서는 검사 ‘최종 책임자’를 사람 한 명으로 정의합니다. 이것은 이 교재의 합의이며 모든 정비 업무의 보편 규칙이 아닙니다. 수행자는 여러 명일 수 있으므로 별도 `responsiblePerson` 속성을 씁니다.

```text
J20은 Inspection이며 responsiblePerson이 정확히 1개
J20 responsiblePerson P1
J20 responsiblePerson P2
```

OWL에서는 서로 다른 주소 P1·P2가 같은 사람을 가리킬 수 있습니다. 따라서 두 주소가 입력됐다는 것만으로 정확히 1개 조건과 반드시 충돌하지 않습니다. 두 값이 같은 개체라고 해석해야 조건을 만족할 수 있습니다. 이 예의 공리와 두 연결을 함께 적용하면 P1과 P2가 동일하다는 결론이 나올 수 있습니다. DB의 ‘두 행이면 개수 위반’이라는 기대와 다른 부분입니다.

여기에 **P1과 P2는 서로 다른 사람**이라는 공리까지 있으면 같은 사람으로 읽을 수 없습니다. 그러면 한 개체뿐이어야 한다는 조건과 충돌해 불일관합니다. 실제로 서로 다른 두 사람을 잘못 넣은 것인지, ‘최종 책임자’가 한 명이라는 모델이 틀렸는지 검토해야 합니다. [OWL 2 Structural Specification, Cardinality Restrictions](https://www.w3.org/TR/owl2-syntax/#Object_Property_Cardinality_Restrictions)

Turtle로 최대 한 개 제한을 적는 예는 다음과 같습니다. `xsd:nonNegativeInteger`는 0 이상 정수 자료형이고 `"1"^^...`는 문자열처럼 보이는 표기를 그 정수값으로 해석하도록 지정합니다.

```turtle
@prefix ex: <https://example.org/owl-lesson/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:Inspection rdfs:subClassOf [
  a owl:Restriction ;
  owl:onProperty ex:responsiblePerson ;
  owl:maxCardinality "1"^^xsd:nonNegativeInteger
] .
ex:J20 a ex:Inspection ;
  ex:responsiblePerson ex:P1, ex:P2 .
```

최대 한 개이므로 0개도 허용하는 제한입니다. 정확히 한 개는 최소와 최대를 모두 요구하는 효과입니다. 특정 클래스에 속하는 값만 세는 **qualified cardinality**도 있으나, 이 수업의 값은 모두 같은 책임자 관계이고 비한정 개수 제한을 사용했습니다. 문법의 종류를 암기하는 것보다 무엇을 세고 어느 이름을 같은 개체로 볼 수 있는지 확인해야 합니다.

## 같은 입력을 SHACL로 검사하면

값을 제출하는 입력 규칙은 “책임자 IRI 한 개를 기록해야 한다”로 정할 수 있습니다. 앞 수업의 모양에서 `sh:path`를 responsiblePerson, `minCount`와 `maxCount`를 1로 지정하면 현재 데이터의 값 노드를 셉니다. P1과 P2라는 서로 다른 RDF 항목이 둘 있으면 이 검사에서는 값 두 개입니다. OWL 의미에서 동일하다는 결론과 어떤 전처리로 동일 ID를 통합했는지를 검사 설정에 포함해야 합니다. 두 이름이 sameAs로 연결됐다는 이유만으로 모든 SHACL 실행이 자동으로 하나로 접어 세는 것은 아닙니다. [SHACL §4.2, Cardinality Constraint Components](https://www.w3.org/TR/shacl/#core-components-count)

| 제출 상태 | OWL 최대 1 조건의 해석 | 이번 입력 규칙 |
|---|---|---|
| 연결 0개 | 최대 조건만으로 허용 가능 | minCount 1 위반 |
| P1 하나 | 조건과 양립 가능 | 개수 조건 통과 |
| P1·P2 두 이름, 상이성 미선언 | 같은 개체라는 해석을 요구 | 원래 두 값 노드를 세면 maxCount 위반 |
| P1·P2와 서로 다름 선언 | 최대 1과 충돌 | 개수 위반도 발견 |

이 차이 때문에 OWL을 입력 폼의 필수값 규칙으로만 이해하면 결과를 잘못 예상합니다. 반대로 SHACL이 통과했다고 ‘실제로 이 사람이 책임자’가 증명되지는 않습니다. 값의 존재와 내용의 사실성을 서로 다른 증거로 확인합니다.

## 닫힌 범위를 명시하는 문장은 별도 정보입니다

‘J20의 책임자로 **알려진** 이름은 P1뿐’과 ‘J20의 책임자는 **오직** P1’도 다릅니다. 전자는 확보한 자료의 목록이고 후자는 다른 책임자가 없다는 제한입니다. 논리적으로 후자까지 표현하려면 그 범위를 제한하는 문장이 있어야 합니다. 원천 명단이 완전한지 확인하지 않고 조회 결과 한 행을 그대로 ‘유일한 담당자’로 말하면 근거보다 강해집니다.

정비가 완료됐는데 담당자 원문이 없다는 사정도 세 가지로 갈라집니다. 담당자가 있었으나 기록을 못 찾은 경우, 입력 규칙을 어겨 기록을 누락한 경우, 실제로 누가 책임자인지 조직도 결정하지 못한 경우입니다. 같은 null로 보이더라도 조사·입력 반려·업무 책임 합의가 각각 필요합니다. 논리 도구가 대신 선택해 줄 수 있는 문제는 아닙니다.

## 설명 연습

**1.** only Person을 선언했으므로 J17에 Person 한 명을 자동 삽입해도 되나요?

그 제한은 값이 있을 때의 타입만 요구합니다. 존재를 요구하지도, 어느 사람인지 알려 주지도 않습니다. some Person이 추가돼도 그 사람이 누구인지 특정하는 자료는 별도로 필요합니다.

**2.** 최대 1 제한을 넣고 P1·P2를 입력했더니 추론 결과에서 둘이 같은 사람으로 연결됐습니다. 데이터 정합이 해결됐다고 볼까요?

공리와 입력을 동시에 만족하려는 동일성 결론입니다. 실세계에서 같은 사람이라는 독립 근거를 발견한 것이 아닙니다. 실제 다른 사람이라면 입력이나 공리를 고쳐야 합니다.

**3.** 원문은 “이번 보고서에는 P1만 기록됐다”고 말합니다. “현장에는 P1만 참여했다”로 바꿔도 될까요?

문서의 기록 범위와 현장의 참여자 범위가 다릅니다. 전체 참여 명단이라는 확인이 없다면 기록한 이름과 미확인 범위를 그대로 유지합니다.
