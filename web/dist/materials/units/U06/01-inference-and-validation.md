# 같은 데이터에서 추론과 검증이 다른 답을 내는 이유

정비 기록에 담당자가 빠졌습니다. 누군가는 ‘온톨로지에서 담당자는 사람이라고 정했으니 오류가 나겠죠’라고 말합니다. 또 다른 사람은 ‘추론하면 담당자를 채워 줄 겁니다’라고 말합니다. 두 설명 모두 실제 규칙과 입력을 확인해야 합니다.

이번에는 작은 RDF 데이터를 놓고 어떤 결론을 더 알 수 있는지, 어떤 입력 요건을 만족하지 못했는지 따로 확인합니다. 추론과 검증이라는 이름만 구분하는 데서 끝내지 않고, **같은 데이터·서로 다른 규칙·서로 다른 결과**를 보겠습니다.

## 1. 입력 데이터와 규칙을 먼저 나눕니다

다음은 교육용 정비 사건 하나입니다. `Replacement`는 부품 교체 사건이라는 클래스입니다. `Maintenance`는 정비 수행이라는 상위 클래스입니다. `E01`은 장비이고 `J17`은 사건입니다.

```turtle
@prefix ex: <https://example.org/check/> .
ex:J17 a ex:Replacement ;
    ex:equipment ex:E01 .
```

현재 J17의 담당자는 적혀 있지 않습니다. 이제 클래스와 관계의 의미를 정하는 규칙을 별도로 추가하겠습니다.

```turtle
@prefix ex: <https://example.org/check/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:Replacement rdfs:subClassOf ex:Maintenance .
ex:performedBy rdfs:domain ex:Maintenance ;
    rdfs:range ex:Person .
```

`rdfs:subClassOf`는 하위 클래스의 모든 개체가 상위 클래스에도 속한다는 뜻입니다. 따라서 Replacement인 J17은 Maintenance에도 속합니다. 이 결론은 입력 파일에 직접 적은 문장이 아니라 입력과 규칙에서 따라 나오는 문장입니다. 이를 **함의되는 진술**이라고 부릅니다. 추론은 정해진 의미와 규칙에 따라 이런 결론을 다루는 과정입니다. [RDFS §3.4](https://www.w3.org/TR/rdf-schema/#ch_subclassof)

하지만 아직 performedBy 관계가 없습니다. domain과 range는 담당자 관계를 반드시 입력하라는 요구가 아닙니다. ‘그 관계가 있는 경우 양쪽 대상은 어떤 종류인가’를 뜻합니다. 지금 입력에서는 담당자 이름이 생기지도 않고, 이 속성이 없다는 이유만으로 누락 오류를 내지도 않습니다.

## 2. domain과 range가 뜻하는 것을 거꾸로 읽어 보기

이번에는 J18에 관계 하나만 적었습니다.

```turtle
@prefix ex: <https://example.org/check/> .
ex:J18 ex:performedBy ex:P1 .
```

앞 규칙과 함께 읽으면 J18은 Maintenance, P1은 Person이라고 결론 낼 수 있습니다. 관계가 있으니 그 관계의 주어·목적어 타입을 따라 추론한 것입니다.

| 데이터 | 규칙 | 따라오는 결론 |
|---|---|---|
| J18 performedBy P1 | performedBy domain Maintenance | J18 type Maintenance |
| J18 performedBy P1 | performedBy range Person | P1 type Person |

이제 실수로 P1 자리에 매뉴얼 M17을 넣었다고 합시다.

```turtle
@prefix ex: <https://example.org/check/> .
ex:J18 ex:performedBy ex:M17 .
ex:M17 a ex:Manual .
```

같은 range 규칙은 M17을 Person으로도 분류합니다. ‘매뉴얼이 들어왔으니 거부하라’는 동작과 다릅니다. RDFS만으로는 Manual과 Person이 반드시 서로 겹치지 않는다는 규칙도 없습니다. 이런 결과가 이상하다면 원천 매핑·어휘 사용·추가 의미 규칙을 검토해야 합니다. [RDFS §3.1~3.2와 §4](https://www.w3.org/TR/rdf-schema/#ch_range)

두 가지를 기억하면 됩니다. domain/range는 추론 근거이며, 이름이 업무 상식에 어긋나 보인다는 인상만으로 논리적 모순이 되지는 않습니다. ‘부적합한 입력을 막는다’라는 목적에는 별도의 검사 조건을 작성할 수 있습니다.

## 3. SHACL로 제출 요건을 명시합니다

이제 ‘모든 정비 수행에는 담당자가 정확히 한 명 있어야 하고, 담당자는 Person으로 분류돼 있어야 한다’는 제출 요건을 만들겠습니다. SHACL은 RDF 데이터가 정한 조건을 만족하는지 검사하는 언어입니다. 검사할 데이터 그래프와 조건을 담는 shapes graph를 구분합니다. [SHACL 소개](https://www.w3.org/TR/shacl/#introduction)

```turtle
@prefix ex: <https://example.org/check/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

ex:MaintenanceShape a sh:NodeShape ;
    sh:targetClass ex:Maintenance ;
    sh:property [
        sh:path ex:performedBy ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:class ex:Person
    ] .
```

`sh:`는 SHACL 어휘의 접두사입니다. shape는 검사 조건의 묶음입니다. `sh:NodeShape`는 노드에 적용할 묶음이고, `sh:targetClass`는 어느 클래스의 개체들을 검사 대상으로 삼을지 정합니다. `sh:property` 안은 특정 속성 경로에 대한 조건입니다.

대괄호 `[...]`는 Turtle에서 이름을 따로 붙이지 않은 blank node를 적는 표기입니다. 즉 바깥 shape와 안의 속성 조건 묶음을 연결합니다. `sh:path`는 대상 노드에서 어떤 관계를 따라 나온 값들을 검사하는지 지정합니다. 여기서는 performedBy입니다.

minCount 1은 값이 최소 하나, maxCount 1은 최대 하나라는 요구입니다. 따라서 합치면 정확히 하나입니다. `sh:class ex:Person`은 그 값이 Person 클래스에 속하는지 검사합니다. 여기서 클래스 소속을 판단하는 방법과 사전 추론 설정이 실제 결과에 영향을 줄 수 있습니다. [SHACL class](https://www.w3.org/TR/shacl/#ClassConstraintComponent), [SHACL cardinality](https://www.w3.org/TR/shacl/#MinCountConstraintComponent)

## 4. 어떤 데이터를 실제로 검사했나요

첫 데이터의 J17은 Replacement로 명시돼 있고, Replacement가 Maintenance의 하위 클래스라는 정보가 있습니다. SHACL의 class target은 데이터 그래프에 있는 클래스 계층도 따라 검사 대상을 찾을 수 있습니다. 따라서 규칙 그래프를 검사 데이터와 합쳐 넘기면 J17은 이 shape의 대상입니다. 단지 `inference='none'`이라고 설정했다고 계층에 따른 대상 선택까지 사라진다고 가정하면 안 됩니다.

동봉 예제는 다음 두 실행을 나눕니다.

| 실행 | 검사 데이터 | 예상 결과 |
|---|---|---|
| A | J17의 타입·장비 + 클래스 계층·domain/range 규칙 | 담당자 0명이므로 minCount 위반 |
| B | A + J17 performedBy P1 + P1 type Person | 지정한 shape 통과 |

검증 보고서에서 `focusNode`는 문제의 대상인 J17, `resultPath`는 performedBy, `sourceConstraintComponent`는 MinCountConstraintComponent입니다. 이 이름들을 보면 단순히 ‘실패’가 아니라 어떤 노드의 어떤 조건이 부족한지 찾을 수 있습니다. `conforms`는 지정한 검사 조건을 만족하는지 나타내는 결과입니다. [SHACL validation report](https://www.w3.org/TR/shacl/#validation-report)

실행 B가 통과했다고 P1이 실제 작업자였음이 증명되지는 않습니다. 입력에 그렇게 적혀 있고 지정한 조건을 충족했을 뿐입니다. 근거 문서를 확인하거나 원천 작업 기록과 대조하는 별도 검증이 필요합니다. 반대로 담당자가 실제로 있었어도 기록에서 누락되면 실행 A는 실패합니다. 업무 현실과 제출 데이터의 요건을 구분해야 합니다.

## 5. 추론을 먼저 하면 검증 결과가 달라질 수 있습니다

P1의 명시적인 Person 타입을 빼고 `J17 performedBy P1`만 남긴다고 해 보겠습니다. 그래프에는 여전히 range Person 규칙이 있습니다.

- RDFS 추론을 먼저 적용하면 P1 type Person이 따라옵니다. 그 결과를 검사하면 class 조건을 충족할 수 있습니다.
- 이 예제에서 추론 없이 검사하면 P1에는 Person 소속 근거가 없어 class 조건을 위반합니다. 단, 앞서 설명한 SHACL의 클래스 계층 처리와 RDFS의 range 추론을 같은 동작으로 혼동하지 마세요.

이 차이는 어느 쪽 도구가 잘못됐다는 뜻이 아닙니다. 검사에 사용할 데이터와 의미 규칙이 달라진 것입니다. 실무에서는 ‘원천이 타입을 명시했는가’를 검사할지, ‘추론으로도 Person임을 알면 충분한가’를 정해야 합니다. 후자에서 잘못된 목적어 M17이 range 때문에 Person으로 분류될 수도 있으므로 이 설정의 의미를 이해해야 합니다.

동봉 검증은 A의 누락·B의 통과 외에도 이 타입 누락 사례를 같은 fixture에서 추론 전후로 비교합니다. 엔진 이름과 설정을 기록해 같은 결과를 재현할 수 있게 합니다. SHACL이 전체 OWL 추론기를 내장한다고 가정하지 않습니다.

## 6. OWL의 열린 세계에서 누락은 무엇을 뜻하나요

OWL에서는 기록에 없다는 사실만으로 실세계에서도 없다고 결론 내리지 않는 열린 세계 가정을 사용합니다. J17의 담당자가 적혀 있지 않으면 ‘담당자가 없었다’고 바로 말할 수 없습니다. 아직 모르는 것일 수 있습니다. 데이터베이스의 조회 결과가 비었다는 것과 도메인에 그 사실이 없다는 결론의 차이를 생각해 보세요. [OWL 2 Primer §3](https://www.w3.org/TR/owl2-primer/#Modeling_Knowledge:_Basic_Notions)

‘모든 정비는 어떤 담당자를 가진다’라는 존재 조건을 OWL로 선언하면, 그 정비가 존재할 때 담당자인 무언가도 존재해야 한다는 의미를 표현할 수 있습니다. 이 조건은 입력 파일에 담당자 ID를 반드시 적어야 한다는 요구와 다릅니다. 또한 추론기가 이름이 있는 새 작업자 레코드를 자동 생성해 현장의 누군지 알아낸다는 뜻도 아닙니다. 그런 구현 동작과 실세계 식별은 별개입니다.

숫자 제한도 주의해서 읽습니다. ‘담당자가 최대 한 명’이라는 OWL 조건 아래 J17에 이름이 다른 두 담당자를 적었다면, 그 두 이름이 같은 대상을 가리키는 해석이 가능한지 살펴야 합니다. OWL은 이름이 다르다는 이유만으로 항상 서로 다른 개체라고 가정하지 않습니다. 두 사람이 다르다는 근거까지 선언되면 상황은 달라집니다. 반면 SHACL maxCount는 데이터에서 검사 경로로 얻은 서로 다른 값 노드의 수를 검사합니다. 공리의 논리 의미와 제출값 개수를 섞어 설명해서는 안 됩니다. [OWL Primer의 개체 동일성과 cardinality 설명](https://www.w3.org/TR/owl2-primer/)

이 절의 OWL 사례는 의미를 해석한 설명입니다. 동봉 실행은 RDFS와 SHACL 사례에 한정하며 OWL 전체 일관성 검사를 실행한 결과가 아닙니다. OWL의 표현력과 프로파일, 일관성은 후속 수업에서 더 다룹니다.

## 7. 자신의 예로 차이를 설명하기

**문제 1:** 문서의 author 속성에 range Person을 정했습니다. author가 누락된 문서에 오류가 나나요?

**해설:** 그 규칙만으로 필수 입력을 검사하지 않습니다. 관계가 있다면 목적어 타입을 추론하는 근거가 됩니다. author 최소 하나를 요구하려면 SHACL 같은 조건으로 minCount를 정할 수 있습니다.

**문제 2:** 담당자 P1을 연결했지만 P1 타입은 없었습니다. 추론 후에는 class 검사를 통과했습니다. 원천 데이터가 올바른 Person 타입을 명시했다고 보고해도 되나요?

**해설:** 명시 입력과 추론 결과가 다릅니다. 원천은 관계만 적었고 타입은 규칙에서 따라왔습니다. 검토 목적이 타입을 원천이 명시했는지 확인하는 것이라면 다른 검사나 출처 구분이 필요합니다.

**문제 3:** 누락을 검사했더니 J17이 아예 검사 대상이 아니었습니다. 담당자가 잘 기록됐다는 뜻인가요?

**해설:** target 선택을 먼저 확인해야 합니다. 데이터에서 정비 클래스 소속이나 클래스 계층을 찾지 못했을 수 있습니다. 통과 결과를 해석하려면 검사 대상·데이터·조건·추론 설정을 함께 보아야 합니다. 문법적으로 맞는 shape만으로 원하는 모든 기록이 검사되는 것은 아닙니다.
