# OWL 공리를 추가하면 어떤 결론이 생기나요?

정비 사건 J17은 교체 작업입니다. ‘교체 작업은 정비 수행의 한 종류’라는 분류만으로도 J17을 정비 검색에 포함할 수 있습니다. 이번에는 “승인자와 수행자가 같은 사람인가?”, “두 부서의 클래스 이름을 같게 봐도 되는가?”, “문서와 실물은 겹치지 않는가?”까지 표현해 보겠습니다. OWL은 이런 문장을 기계가 해석할 수 있는 의미로 적는 언어입니다. 자연어로 적은 업무 규칙 전부를 자동으로 이해하는 엔진은 아닙니다.

기준은 W3C **OWL 2 Recommendation, Second Edition(2012-12-11)**입니다. 예제는 합성이고, OWL 2 Direct Semantics에 따른 논리적 결과와 동봉 OWL-RL 규칙 실행 결과를 구분합니다. RDF에 적었다는 사실만으로 저장소가 그 공리를 실행하지는 않습니다. [OWL 2 문서 안내](https://www.w3.org/TR/owl2-overview/)

## 하위 클래스와 동치 클래스는 다른 약속입니다

`Replacement`는 교체 작업, `Maintenance`는 정비 수행, `PartChange`는 다른 시스템이 쓰는 작업 종류라고 정의합니다.

```turtle
@prefix ex: <https://example.org/owl-lesson/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
ex:Replacement rdfs:subClassOf ex:Maintenance .
ex:Replacement owl:equivalentClass ex:PartChange .
ex:J17 a ex:Replacement .
```

앞 단원처럼 `ex:`는 예제 주소를 줄이고, `a`는 타입 관계입니다. `owl:equivalentClass`는 두 클래스에 속하는 개체 범위가 같다고 선언합니다. 이 입력에서는 J17이 Maintenance와 PartChange에도 속합니다. 반대로 PartChange로만 분류된 J18도 Replacement로 분류할 수 있습니다. 단순한 하위 관계에서는 상위 Maintenance인 J19가 자동으로 Replacement가 되지 않습니다.

| 입력으로 알려진 타입 | 위 공리에서 따라오는 타입 | 따라오지 않는 결론 |
|---|---|---|
| J17은 Replacement | Maintenance, PartChange | 실제 작업을 검증했다는 판정 |
| J18은 PartChange | Replacement, Maintenance | 모든 정비가 교체라는 문장 |
| J19는 Maintenance | 이 두 세부 타입은 아직 미상 | J19가 Replacement라는 문장 |

동치는 ‘이름이 비슷하다’, ‘검색에서 같이 찾고 싶다’보다 강합니다. 한 시스템의 PartChange가 계획된 교체까지 포함하고 다른 시스템의 Replacement가 실제 수행만 뜻하면 두 범위가 다릅니다. 그때 동치 공리를 넣으면 계획을 실제 수행으로 분류하는 결론이 생길 수 있습니다. 정의·긍정 예·반례로 범위를 확인해야 하는 이유입니다. [OWL 2 Primer, Class Hierarchies](https://www.w3.org/TR/owl2-primer/#Class_Hierarchies)

## 서로소 클래스가 오류를 드러내는 방식

문서 `Document`와 실물 장비 `PhysicalEquipment`를 이 모델에서 겹치지 않게 정했다고 합시다.

```turtle
@prefix ex: <https://example.org/owl-lesson/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
ex:Document owl:disjointWith ex:PhysicalEquipment .
ex:D1 a ex:Document .
```

`disjointWith`는 두 클래스가 공통 개체를 갖지 않는다는 뜻입니다. 그 뒤 D1에 PhysicalEquipment 타입까지 붙이면 어느 해석에서도 두 조건을 동시에 만족할 수 없습니다. 입력과 공리를 함께 만족할 해석이 없다는 **불일관성(inconsistency)**을 찾을 수 있습니다. 이때 추론기가 ‘문서 타입이 틀렸으니 그것만 지워라’고 업무 정답을 자동 선택하는 것은 아닙니다. 어느 입력이나 공리를 고칠지는 원천과 정의를 확인합니다.

서로소 선언 없이 D1이 두 타입에 속하면 OWL은 그 겹침을 허용할 수 있습니다. 현실에서 다른 종류처럼 보인다는 직관이 공리로 자동 들어가지 않습니다. 같은 단어도 역할에 따라 다르므로, 예를 들어 ‘검사 대상’은 실물이나 문서를 모두 포함할 수 있게 설계할 수 있습니다. 공리의 강도는 모델의 의도에 맞춰 정해야 합니다.

또 하나 구별할 상황이 있습니다. `ImpossibleThing`이라는 클래스가 두 서로소 클래스의 하위라고만 선언하고 그 클래스의 개체는 아직 없다고 합시다. 이 클래스의 범위가 비어 있으면 전체 모델은 여전히 만족할 수 있습니다. 클래스가 개체를 가질 수 없는 **불만족 클래스**와, 온톨로지 전체가 불일관한 것은 같은 말이 아닙니다. 여기에 `x a ImpossibleThing`을 추가하면 공통 개체를 요구하므로 전체 충돌이 생깁니다. [OWL 2 Direct Semantics, Class Expression Axioms와 Inference Problems](https://www.w3.org/TR/owl2-direct-semantics/)

## 역관계·하위 속성을 읽어 봅니다

정비에서 사람으로 `performedBy`, 사람에서 정비로 `performs`를 쓴다면 둘을 역관계로 선언할 수 있습니다.

```turtle
@prefix ex: <https://example.org/owl-lesson/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
ex:performedBy owl:inverseOf ex:performs .
ex:replacedBy rdfs:subPropertyOf ex:performedBy .
ex:J17 ex:replacedBy ex:P1 .
```

이 예에서 `replacedBy`는 ‘이 교체 작업을 수행한 사람’을 뜻하도록 정했습니다. ‘장비를 대신한 새 장비’라는 다른 의미로 쓰지 않습니다. 첫 결과는 J17 performedBy P1이고, 그 역관계를 사용하면 P1 performs J17입니다. 역관계가 새 수행 사건을 추가하는 것은 아닙니다. 하나의 관계 사실을 반대 방향으로도 읽는 것입니다. 하위 속성도 반대 방향으로 일반화하지 않습니다. 모든 수행자를 교체 수행자로 분류할 근거는 없습니다.

사용자는 반대 방향으로 찾고 싶을 때 역관계를 질의로만 표현할 수도 있습니다. 저장소에 모든 역관계를 물리적으로 중복 저장할 필요가 있는지는 실행 방식에 달렸습니다. 물리적으로 저장하면 새 원천 관계를 정정할 때 파생 역관계도 갱신해야 합니다. 추론의 의미와 저장·질의 전략을 분리하면 이 선택을 설명할 수 있습니다. [OWL 2 Structural Specification, InverseObjectProperties](https://www.w3.org/TR/owl2-syntax/#Inverse_Object_Properties)

## is-a와 part-of의 전이를 섞지 않습니다

하위 클래스는 집합 포함입니다. P8이 Pump 클래스의 개체이고 Pump가 Component의 하위이면 P8은 Component입니다. 반면 P8이 E01의 부품이라는 관계는 P8이 E01과 같은 유형이라는 의미가 아닙니다.

부품 관계를 전이적으로 쓰고 싶다면 별도 정의가 필요합니다. 예를 들어 `containedIn`을 순수한 물리적 포함으로 한정하고 전이를 합의하면 P8 containedIn U1, U1 containedIn E01에서 P8 containedIn E01을 얻을 수 있습니다. 하지만 ‘정비 계약의 부품 목록에 등장함’과 ‘현재 실제로 설치됨’을 같은 관계로 섞으면 전이 결론이 틀릴 수 있습니다. 시각이 다른 두 장착 사실을 무조건 연결하는 것도 문제입니다. 규칙의 문법보다 관계의 정의가 먼저입니다.

OWL의 전이 속성 선언은 일반적인 연결 도달과 관련되지만, 어느 관계에나 붙여 ‘똑똑한 그래프’로 만드는 스위치가 아닙니다. 부모 관계를 전이로 두면 조부모를 부모로도 읽는 결론이 생기는 것처럼, 기대하는 업무 의미에 맞는지를 반례로 시험합니다. [OWL 2 Structural Specification, TransitiveObjectProperty](https://www.w3.org/TR/owl2-syntax/#Transitive_Object_Properties)

## 같은 이름이 아니라 같은 개체라고 말할 때

두 시스템 주소 `ex:E01`과 `ex:NE017`이 동일한 실물을 가리킨다는 합의를 다음처럼 적을 수 있습니다.

```turtle
@prefix ex: <https://example.org/owl-lesson/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
ex:E01 owl:sameAs ex:NE017 .
ex:NE017 ex:serial "S100" .
```

동일성 의미를 사용하는 추론에서 E01에도 serial S100이 적용됩니다. 이것은 검색 별칭 목록을 달아준 것보다 강한 선언입니다. 한쪽이 자산 대장 **문서**, 다른 쪽이 실제 **장비**라면 서로를 같은 개체라 선언할 이유가 없습니다. 대장 문서가 장비를 기술한다는 관계를 쓰는 편이 맞습니다.

반대로 주소가 다르다는 사실만으로 두 개체가 반드시 별개라고 가정하지 않는 것이 OWL의 중요한 특성입니다. `differentFrom`이나 여러 개체의 상이성을 명시하는 공리를 사용할 수 있습니다. 실제로 서로 다른 두 장비임을 원천에서 확인했다면 그 상이성을 모델에 반영할지 정합니다. 이 차이가 다음 수업의 개수 제한에서 예상치 못한 동일성 결론을 만드는 이유입니다. [OWL 2 Structural Specification, Individual Equality·Inequality](https://www.w3.org/TR/owl2-syntax/#Individual_Equality)

## 설명 연습

**1.** ‘교체 계획’과 ‘교체 수행’을 같은 상위의 서로 다른 하위로 두었습니다. 자동 프로그램이 두 클래스에 equivalentClass를 붙입니다. 무엇을 검사할까요?

계획만 있고 수행은 없는 예가 두 범위의 반례입니다. 동치를 넣으면 이 계획이 수행으로도 분류될 수 있습니다. 이름 유사도 대신 정의·업무 질문·개체의 분류 변화를 확인합니다.

**2.** ‘문서와 장비는 겹치지 않는다’고 선언했는데 D1이 두 타입입니다. 어느 것을 자동 삭제할까요?

충돌은 찾았지만 어느 전제가 틀렸는지 아직 알 수 없습니다. D1이 가리키는 대상, 매핑과 원천을 확인해 잘못된 타입이나 식별 병합 또는 부적절한 서로소 선언을 고칩니다.

**3.** 역관계가 추론되어 사람에서 작업을 찾을 수 있습니다. 원래 관계가 두 개가 된 것이므로 작업도 두 번 세나요?

같은 J17을 서로 다른 방향으로 참조한 것입니다. 사건 ID를 세면 한 건입니다. 파생 관계 수와 실제 수행 횟수는 다릅니다.
