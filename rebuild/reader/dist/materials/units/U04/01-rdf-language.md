# 데이터의 이름을 공유하는 방법: RDF를 처음부터 읽기

회사에 장비 대장과 정비 기록이 따로 있다고 해 보겠습니다. 대장의 `equipment_id=E01`과 정비 기록의 `machine=E01`을 연결하려면 두 값이 같은 장비를 뜻하는지 알아야 합니다. 두 시스템에서 우연히 같은 문자열을 사용했을 수도 있습니다. 데이터를 합치는 프로그램은 컬럼 이름이나 짧은 코드만 보고 이 의미를 확신할 수 없습니다.

RDF를 공부할 때는 이 문제를 출발점으로 삼으면 좋습니다. 무엇을 가리키는 이름인지, 어떤 관계를 말하는지, 연결되는 것이 다른 대상인지 단순한 값인지를 명시해 보겠습니다. 문법을 읽은 뒤에는 같은 정보를 다른 파일 형식으로 적어도 왜 같은 그래프가 될 수 있는지 설명할 수 있을 것입니다.

이 수업의 장비·문서·사건은 교육용 합성 사례입니다. 실제 반도체 공정의 운전 조건이나 원인을 규정하지 않습니다. 비교 기준은 RDF 1.1입니다.

## 1. 사람이 읽는 문서에서 시스템이 연결할 수 있는 데이터로

웹페이지에 ‘장비 E01의 정비 매뉴얼은 M17이다’라고 쓰면 사람은 문장을 읽고 뜻을 파악합니다. 여러 회사의 시스템이 이를 함께 사용하려면 더 명시적인 약속이 필요합니다. `E01`은 우리 회사의 실제 장비인지, 장비 제품군인지, 매뉴얼 안의 예제 코드인지부터 맞아야 합니다.

Semantic Web은 웹의 정보를 시스템이 의미 있는 데이터로 공유하고 연결하는 방향을 다룹니다. 여기서 의미를 명시한다는 것은 컴퓨터가 인간처럼 모든 내용을 이해하게 만든다는 뜻이 아닙니다. 이름과 관계, 분류와 규칙을 공통의 표현으로 적어 프로그램이 이를 처리할 수 있게 한다는 뜻입니다. 데이터를 연결하는 표현과 그 위에서 의미를 기술하는 어휘를 함께 배우게 됩니다. [W3C RDF Primer의 도입과 사용 목적](https://www.w3.org/TR/rdf11-primer/#section-Introduction)

HTML의 `article`이나 `nav`를 잘 사용하는 일도 웹 문서 구조를 개선하지만, 지금 배울 RDF 데이터 모델과 같은 층의 일은 아닙니다. RDF의 질문은 ‘이 데이터가 가리키는 대상과 관계를 다른 시스템에 어떻게 전달하는가’입니다.

W3C는 웹 기술의 표준화 기구입니다. RDF·RDFS·OWL·SPARQL 문서들을 접할 때는 문서 이름만큼 상태도 보아야 합니다. Recommendation은 표준 권고 문서이고, Working Group Note는 해설이나 참고 설계를 담기도 합니다. 예를 들어 RDF 1.1 Concepts는 Recommendation이며 RDF 1.1 Primer는 Working Group Note입니다. 따라서 Primer에서 입문 설명을 배우고 세부 정의는 Concepts로 대조하는 읽기 방식이 가능합니다. ‘W3C 페이지에 있다’는 이유로 모든 자료가 동일한 규범적 지위를 갖지는 않습니다. [Concepts 상태](https://www.w3.org/TR/rdf11-concepts/), [Primer 상태](https://www.w3.org/TR/rdf11-primer/)

## 2. 한 문장을 세 자리로 나누기

다음 합성 기록을 보겠습니다.

> 장비 E01은 매뉴얼 M17을 사용한다.

이를 세 부분으로 나누면 다음과 같습니다.

| 자리 | 내용 | 이 문장에서 하는 일 |
|---|---|---|
| 주어 subject | 장비 E01 | 무엇에 관해 말하는가 |
| 술어 predicate | 매뉴얼을 사용한다 | 어떤 관계인가 |
| 목적어 object | 매뉴얼 M17 | 무엇과 연결되는가 |

세 자리의 묶음이 triple, 즉 트리플입니다. 자연어 문장을 이렇게 나누는 것은 RDF를 배우기 위한 출발점입니다. 실제 RDF에서는 긴 문장을 그대로 세 칸에 잘라 넣기보다 대상과 관계에 식별자를 붙입니다. 아래 코드에서는 `https://example.org/fab/`라는 예제용 이름 공간을 사용합니다.

```turtle
@prefix ex: <https://example.org/fab/> .
ex:E01 ex:usesManual ex:M17 .
```

`ex:E01`이 장비, `ex:usesManual`이 관계, `ex:M17`이 문서입니다. 맨 끝의 마침표는 이 트리플을 끝냅니다. 첫 줄의 prefix 선언은 짧은 이름을 해석하는 방법을 알려 주며, 여기서 장비에 관한 사실을 추가하는 트리플은 아닙니다.

이름을 모두 펼치면 다음 세 IRI가 됩니다.

```text
https://example.org/fab/E01
https://example.org/fab/usesManual
https://example.org/fab/M17
```

IRI는 Internationalized Resource Identifier의 줄임말로, 국제 문자를 지원하는 자원 식별자입니다. 이 예제에서는 장비·관계·문서를 구분하는 이름으로 사용합니다. 주소처럼 생겼어도 실제 장비 자체를 인터넷에서 내려받는다는 뜻은 아닙니다. 웹에서 설명 문서가 반환되도록 설계할 수 있지만, 식별과 문서 제공은 구분해서 생각해야 합니다. [RDF Concepts §1.3, §3.2](https://www.w3.org/TR/rdf11-concepts/#section-IRIs)

이제 `ex:`를 `fab:`으로 바꾸어 보세요. 두 접두사가 똑같이 `https://example.org/fab/`에 연결되어 있다면 `fab:E01`과 `ex:E01`은 같은 IRI의 다른 축약 표기입니다. 반대로 다른 회사가 `ex:`를 `https://other.example/equipment/`에 연결하면 같은 `ex:E01`이라는 글자도 다른 IRI로 펼쳐집니다. 그러므로 접두사의 철자만 보고 동일성을 판단해서는 안 됩니다.

## 3. 대상의 이름과 값은 왜 구분할까요

장비에는 문서뿐 아니라 사람이 읽을 이름도 필요합니다.

```turtle
@prefix ex: <https://example.org/fab/> .
ex:E01 ex:displayName "검사 장비 1호" .
```

목적어가 이번에는 따옴표로 감싸져 있습니다. `"검사 장비 1호"`는 문자열 값인 literal입니다. `ex:M17`처럼 별도로 식별한 대상을 가리키는 것과 역할이 다릅니다. 예를 들어 문서 M17에는 작성자·개정일·관련 장비를 계속 연결할 수 있습니다. 문자열 `"M17"`만 남기면 그 값이 문서의 식별자라는 합의를 별도로 설명해야 합니다.

반대로 모든 문자열을 노드로 바꿀 이유도 없습니다. 표시용 이름을 그냥 값으로 두는 것은 자연스러운 선택입니다. 다른 대상과 연결해야 하는지, 독립적으로 관리해야 하는지를 보며 선택합니다.

값의 종류를 명확히 하고 싶다면 데이터 타입을 표시할 수 있습니다.

```turtle
@prefix ex: <https://example.org/fab/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:E01 ex:inspectionCount "3"^^xsd:integer .
```

`xsd:`는 XML Schema의 데이터 타입 이름들을 줄여 적는 접두사입니다. RDF를 XML 문서로 써야 해서 등장한 것이 아닙니다. 여기서는 정수 타입 이름을 재사용합니다. `^^` 뒤에 오는 `xsd:integer`는 앞 문자열을 정수 값으로 해석하게 합니다. 타입 표시가 없는 문자열 `"3"`과 정수 3을 담는 값은 같은 RDF term이 아닙니다. 애플리케이션에서 연산하려면 이 차이가 중요합니다.

단위는 별개입니다. `"3"^^xsd:integer`만으로 세 번인지, 3초인지, 부품 세 개인지 알 수 없습니다. 여기서는 `inspectionCount`를 검사 횟수로 정의했기 때문에 횟수로 읽습니다. 여러 단위를 다뤄야 한다면 값과 단위를 함께 모델링해야 합니다. 이 부분은 도메인 의미 설계로 이어집니다.

문자열의 언어를 알려 주는 표기도 있습니다.

```turtle
@prefix ex: <https://example.org/fab/> .
ex:E01 ex:displayName "검사 장비 1호"@ko .
ex:E01 ex:displayName "Inspection tool 1"@en .
```

`@ko`와 `@en`은 한국어·영어 언어 태그입니다. `@prefix`의 `@`와 혼동하지 마세요. 하나는 선언을 시작하는 표기이고 다른 하나는 해당 문자열의 언어를 나타냅니다. 이 장비의 이름이 여러 언어로 있다는 사실을 표현할 수 있습니다. [Turtle §2.4~2.5](https://www.w3.org/TR/turtle/#sec-iri)

## 4. rdf:type은 무엇이고, rdfs:는 왜 또 등장하나요

지금까지는 장비가 문서를 사용한다는 관계와 장비의 이름을 적었습니다. 이제 ‘E01은 장비다’라는 분류도 말해 보겠습니다.

```turtle
@prefix ex: <https://example.org/fab/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
ex:E01 rdf:type ex:Equipment .
```

`ex:E01`은 구체적인 장비, `ex:Equipment`는 장비라는 클래스, `rdf:type`은 대상이 그 클래스의 개체임을 나타내는 관계입니다. 클래스는 여러 개체를 같은 종류로 묶어 설명하기 위해 사용합니다. E01 한 대와 ‘장비라는 종류’를 같은 것으로 생각하면 뒤의 추론 예제를 이해하기 어렵습니다.

`rdf:`는 우리가 만든 도메인 어휘인 `ex:`와 달리 RDF의 공통 어휘를 가리킵니다. `rdf:type`은 긴 이름 `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`의 축약입니다. 타입 이름인 `Equipment`를 RDF가 미리 알고 있다는 뜻은 아닙니다. 우리가 만든 클래스에 공통의 소속 관계를 사용하는 것입니다.

Turtle에서는 술어 자리에 오는 `a`를 `rdf:type`의 축약으로 쓸 수 있습니다. 따라서 다음은 같은 진술입니다.

```turtle
@prefix ex: <https://example.org/fab/> .
ex:E01 a ex:Equipment .
```

여기에 사람이 읽기 좋은 클래스 이름을 달고 싶다면 `rdfs:label`을 사용할 수 있습니다. RDFS는 RDF Schema의 어휘로, 클래스·속성의 관계를 설명하는 데 쓰입니다.

```turtle
@prefix ex: <https://example.org/fab/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:Equipment rdfs:label "장비"@ko .
```

이번 주어는 E01이 아니라 Equipment입니다. ‘개별 장비의 이름’과 ‘장비라는 클래스에 붙인 이름’이 다르기 때문입니다. 같은 문법을 쓰더라도 무엇을 설명하는지 따라 읽어야 합니다. 이어질 U06에서는 `rdfs:subClassOf`로 클래스 사이의 포함 관계를 설명합니다. [RDFS §3.3, §3.4, §3.6](https://www.w3.org/TR/rdf-schema/#ch_type)

## 5. 긴 코드를 짧게 적어도 트리플은 사라지지 않습니다

동일한 장비에 여러 정보를 붙이면 주어를 계속 반복하게 됩니다. Turtle의 세미콜론은 주어를 이어 쓰게 합니다.

```turtle
@prefix ex: <https://example.org/fab/> .
ex:E01 a ex:Equipment ;
    ex:usesManual ex:M17 ;
    ex:displayName "검사 장비 1호" .
```

첫 줄의 주어 E01을 다음 두 술어에서도 공유합니다. 세미콜론은 이전 주어를 유지한 채 새 술어·목적어를 시작합니다. 따라서 위 코드는 세 트리플입니다. 맨 마지막의 마침표가 현재 묶음을 끝냅니다.

하나의 술어에 목적어가 여러 개라면 쉼표를 쓸 수 있습니다.

```turtle
@prefix ex: <https://example.org/fab/> .
ex:E01 ex:usesManual ex:M17, ex:M18 .
```

이 코드는 E01→usesManual→M17과 E01→usesManual→M18의 두 트리플입니다. M17과 M18이 순서 있는 목록이라는 뜻은 아닙니다. ‘첫 매뉴얼’과 ‘둘째 매뉴얼’이라는 순서까지 필요하면 다른 표현을 설계해야 합니다. 줄 수·세미콜론 수·트리플 수를 혼동하지 않는 연습이 필요합니다. [Turtle §2.2~2.3](https://www.w3.org/TR/turtle/#predicate-lists)

## 6. 이름 없는 대상을 표현하는 blank node

어떤 보고서가 ‘장비 E01의 관측값 하나는 7이며 교육용 단위 U를 사용한다’고 썼다고 합시다. 이 관측 묶음을 내부적으로 연결할 필요는 있지만 외부에서 공유할 IRI를 아직 붙이지 않았습니다.

```turtle
@prefix ex: <https://example.org/fab/> .
ex:E01 ex:hasReading _:r1 .
_:r1 ex:value 7 ; ex:unit "U" .
```

`_:r1`은 blank node를 이 문서에서 가리키는 표지입니다. `r1`이라는 전역 식별자를 배정한 것이 아닙니다. 같은 문서 안에서는 같은 blank node를 다시 가리킬 수 있지만, 다른 파일의 `_:r1`을 보고 같은 관측이라고 합쳐서는 안 됩니다. 반대로 회사의 여러 시스템에서 같은 관측을 안정적으로 참조해야 한다면 IRI를 부여하는 편이 적합할 수 있습니다.

여기서 `7`은 Turtle이 정수로 적을 수 있게 제공하는 축약 표기입니다. 앞에서 본 `"7"^^xsd:integer`와 대응합니다. `"U"`는 실제 반도체 측정 단위가 아닌 예제 값입니다. [RDF Concepts §3.4](https://www.w3.org/TR/rdf11-concepts/#section-blank-nodes), [Turtle §2.5.2, §2.6](https://www.w3.org/TR/turtle/#BNodes)

세 종류의 term을 배웠으니 어느 자리에 쓸 수 있는지도 정리하겠습니다. 이 표는 RDF 1.1 기준입니다.

| 트리플의 자리 | 허용되는 요소 | 예 |
|---|---|---|
| 주어 | IRI 또는 blank node | ex:E01, _:r1 |
| 술어 | IRI | ex:hasReading, rdf:type |
| 목적어 | IRI, blank node, literal | ex:M17, _:r1, 정수 7 |

따라서 따옴표 문자열을 술어로 적거나 literal을 주어로 쓰면 이 모델의 일반 트리플이 아닙니다. 객체의 별도 속성을 계속 연결하려면 IRI나 blank node로 나타내고, 단순 값은 목적어 literal로 연결하는 이유를 여기서도 확인할 수 있습니다.

## 7. 파일 형식을 바꿔도 같은 사실이 남는지 확인하기

다시 가장 작은 사실 하나로 돌아가겠습니다.

```turtle
@prefix ex: <https://example.org/fab/> .
ex:E01 ex:usesManual ex:M17 .
```

이를 RDF/XML로 적으면 다음과 같습니다.

```xml
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:ex="https://example.org/fab/">
  <rdf:Description rdf:about="https://example.org/fab/E01">
    <ex:usesManual rdf:resource="https://example.org/fab/M17"/>
  </rdf:Description>
</rdf:RDF>
```

바깥 `rdf:RDF`는 RDF/XML 문서의 묶음입니다. `xmlns`는 XML에서 접두사를 선언합니다. `rdf:Description`의 `rdf:about`은 현재 설명의 주어를 지정합니다. 안쪽의 `ex:usesManual` 요소가 술어이며 `rdf:resource`가 목적어의 IRI를 나타냅니다. XML의 태그를 하나씩 따라가면 결국 같은 E01→usesManual→M17이 남습니다. [RDF/XML §2.2~2.6](https://www.w3.org/TR/rdf-syntax-grammar/#section-Syntax-node-property-elements)

JSON에 익숙한 개발자라면 JSON-LD 형태도 읽을 수 있습니다.

```json
{
  "@context": {"ex": "https://example.org/fab/"},
  "@id": "ex:E01",
  "ex:usesManual": {"@id": "ex:M17"}
}
```

`@context`는 이 문서의 짧은 이름 해석을 제공합니다. 바깥의 `@id`는 주어의 식별자입니다. `ex:usesManual` 키가 관계이고 그 값에 있는 `@id`가 연결할 대상의 식별자입니다. 만약 안쪽 값을 단순 문자열 `"ex:M17"`로 바꾸면 이 context에서는 대상 IRI를 가리키는 것과 같지 않습니다. JSON의 중첩 모양만 보고 RDF 연결을 추정하지 말고 식별자와 값의 차이를 읽어야 합니다. [JSON-LD 1.1의 기본 개념](https://www.w3.org/TR/json-ld11/#basic-concepts)

세 코드를 각각의 파서로 읽으면 같은 한 트리플을 얻을 수 있습니다. 이처럼 데이터 모델은 표현하려는 요소와 관계의 규칙이고, 직렬화 구문은 이를 파일의 글자로 기록하는 방식입니다. XML 태그가 많다는 인상은 RDF/XML이라는 구문의 특징이지 모든 RDF가 XML이라는 뜻이 아닙니다. 반대로 JSON-LD를 쓴다고 모든 JSON이 저절로 의미 있는 연결 데이터가 되는 것도 아닙니다. 코드의 context·식별자·어휘 의미가 필요합니다.

## 8. 어디까지 배웠는지 직접 설명해 보기

다음 코드를 네 개의 자연어 문장으로 바꿔 보세요.

```turtle
@prefix ex: <https://example.org/fab/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:E02 a ex:Equipment ;
    ex:usesManual ex:M17, ex:M18 .
ex:Equipment rdfs:label "장비"@ko .
```

**해설:** E02는 Equipment의 개체입니다. E02는 M17을 사용합니다. E02는 M18을 사용합니다. Equipment 클래스에는 한국어 이름 ‘장비’가 있습니다. 마지막 문장은 E02의 개별 이름을 지정하지 않습니다. prefix 선언 두 줄도 이 네 트리플에 포함되지 않습니다.

이제 동료가 ‘`ex:M17`과 `"M17"`은 같은 거 아니야?’라고 묻는다고 생각해 보세요. 전자는 예제 namespace로 확장한 IRI로 문서 대상을 가리키고, 후자는 문자열 값입니다. 다른 기록을 그 문서에 연결하거나 문서 속성을 조회하려면 어떤 대상으로 연결하는지 명시되어야 한다고 설명할 수 있습니다.

다음 수업에서는 이 표기를 사용해 **같은 사람이 같은 차를 세 번 운전한 사건**을 표현합니다. 이번에 배운 타입과 값 표현이 왜 필요한지, RDF와 속성 그래프가 그 사건을 어떤 구조로 담는지 비교할 것입니다. [반복 사건 비교 수업](02-events-and-property-graphs.md)
