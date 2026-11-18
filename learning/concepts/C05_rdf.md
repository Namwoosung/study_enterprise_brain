# C5. RDF Graph — 진술을 교환 가능한 그래프로 표현하기

**목표:** triple·IRI·literal·blank node·dataset을 읽고 RDF 표현의 장점과 맥락 모델링 한계를 설명한다.

<a id="c5-01"></a>
## 1. RDF는 그래프 그림도 XML 파일도 아니다

RDF(Resource Description Framework)는 정보를 진술의 집합으로 표현하는 데이터 모델이다. 기본 단위 triple은 주어(subject), 술어(predicate), 목적어(object)다. RDF 그래프는 triple의 집합이며 순서는 의미를 만들지 않는다. [RDF 1.1 Concepts §3](https://www.w3.org/TR/rdf11-concepts/#section-rdf-graph)

~~~text
RUN002 — usedEquipment → E01
RUN002 — usedDocument  → D02
~~~

첫 문장의 주어는 작업, 술어는 장비 사용 관계, 목적어는 장비다. “문서에 같은 단어가 등장한다”가 아니라 어떤 대상이 어떤 대상과 어떤 관계에 있다고 명시한다.

이 모델을 Turtle, RDF/XML, JSON-LD 등 여러 구문으로 기록할 수 있다. 파일 확장자와 추상 데이터 모델을 구분한다. 같은 그래프를 다른 구문으로 바꾸어도 핵심 진술은 유지될 수 있다. RDF/XML을 읽기 어렵다는 이유로 RDF 자체를 XML 문법과 동일시하지 않는다. [RDF 1.1 Primer §5](https://www.w3.org/TR/rdf11-primer/#section-graph-syntax)

<a id="c5-02"></a>
## 2. IRI·literal·blank node의 역할

IRI는 대상이나 관계를 식별하는 이름이다. "E01"이라는 문자열 값과 E01이라는 장비의 식별자는 구분해야 한다. Literal은 문자열·숫자·날짜 같은 값이다. Blank node는 명시적 전역 IRI를 붙이지 않은 자원을 나타내며, 단순한 null 값이 아니다.

RDF 1.1에서 주어는 IRI 또는 blank node, 술어는 IRI, 목적어는 IRI·blank node·literal이 될 수 있다. Literal에는 datatype 또는 언어 태그가 있다. [RDF Concepts §3](https://www.w3.org/TR/rdf11-concepts/#section-triples)

~~~turtle
@prefix ex: <https://example.org/fab/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:E01 ex:label "검사기 1호"@ko ;
       ex:serialNumber "SN101" .
ex:RUN002 ex:startedAt "2026-11-03T10:00:00+09:00"^^xsd:dateTime .
~~~

example.org는 이 교재의 예시 namespace다. label의 한국어 문자열은 사람이 읽는 이름이고 ex:E01은 시스템이 연결할 대상이다. 서로 다른 장비가 같은 label을 가질 수 있다. 식별자 관리 정책이 없으면 IRI를 써도 중복·오병합 문제가 남는다.

<a id="c5-03"></a>
## 3. Turtle을 읽는 데 필요한 최소 문법

~~~turtle
@prefix ex: <https://example.org/fab/> .
ex:RUN002 a ex:Run ;
    ex:forLot ex:L02 ;
    ex:usedEquipment ex:E01 ;
    ex:usedDocument ex:D02 .
~~~

a는 rdf:type의 축약이다. 세미콜론은 같은 주어를 이어 쓴다. 마침표는 해당 문장 묶음을 끝낸다. 따라서 위 코드는 RUN002에 관한 네 triple이다. 접두사 ex:는 긴 IRI를 짧게 쓰는 약속이며 임의의 텍스트 문자열을 자동으로 현실의 자산에 연결해 주는 기능은 아니다.

실습에서는 이를 네 개의 별도 줄로 풀어 읽으면 충분하다. 모든 Turtle 문법을 암기할 필요는 없다. “RUN002는 Run이다”, “L02를 위한 작업이다”, “E01을 사용했다”, “D02를 사용했다”라는 뜻을 설명할 수 있으면 된다. [Turtle 예제를 포함한 RDF Primer](https://www.w3.org/TR/rdf11-primer/)

<a id="c5-04"></a>
## 4. 심화: 여러 원천을 합치면 무엇이 달라지는가?

같은 IRI를 사용하는 진술은 합쳐 읽기 쉬워진다. 장비 목록에 E01의 일련번호, 작업 목록에 RUN002와 E01의 관계가 있으면 E01을 중심으로 연결한다. 하지만 같은 문자열만 보고 서로 다른 현실 대상을 같은 IRI로 발급했다면 잘못 합쳐진다.

RDF 그래프가 집합이라는 점도 중요하다. 동일 triple을 두 번 기록했다고 “증거가 두 개”라는 정보를 표현하는 것은 아니다. 두 독립 출처가 같은 주장을 지지한다면 출처별 주장 또는 그래프 단위를 별도로 관리해야 한다.

데이터셋은 기본 그래프와 이름 있는 그래프들의 구성을 제공한다. 이름 있는 그래프를 원천·버전 단위로 활용할 수 있지만, 그래프 이름만 붙이면 출처·신뢰·권한의 의미가 자동 정의되지는 않는다. 운영 규약과 메타데이터가 필요하다. [RDF Concepts §4](https://www.w3.org/TR/rdf11-concepts/#section-dataset)

<a id="c5-05"></a>
## 5. 심화: 관계에 시간·출처를 붙이는 방법

"RUN002 usedEquipment E01"이라는 관계 자체에 출처를 달고 싶다면 어떻게 할까? RDF 1.1의 기본 triple을 넘어서 사건·주장 자원을 모델링하거나 reification 어휘 등을 검토할 수 있다. 여기서는 발표에 필요한 **주장 노드 패턴**을 사용한다.

~~~text
Claim17 → subject → RUN002
Claim17 → predicate → usedEquipment
Claim17 → object → E01
Claim17 → source → runs.csv의 해당 행
Claim17 → reviewStatus → source_supported
~~~

이는 교재의 설명용 패턴이지 RDF 표준 reification 구문 그대로가 아니다. Claim17의 구조를 만들었다고 본래 triple이 자동으로 주장되는 것도 아니다. 데이터 처리 규약으로 언제 운영 그래프에 반영할지 정해야 한다.

관계의 시간과 사건의 시간도 구분한다. 작업 시작 시각과 주장을 수집한 시각은 다르다. PROV-O는 파생·생성·책임을 표현하는 어휘를 제공하지만, 사실 승인 정책은 따로 설계한다. [PROV-O](https://www.w3.org/TR/prov-o/)

<a id="c5-06"></a>
## 6. RDF가 유리한 조건과 부담

공유 식별자·어휘로 데이터를 교환하거나 서로 다른 조직의 의미 모델을 연결할 때 RDF 생태계가 후보가 된다. SPARQL 질의, RDFS·OWL 의미, SHACL 검증을 공통 규격으로 조합할 수 있다는 점이 중요하다.

반면 IRI 발급·어휘 대응·맥락 표현·그래프 관리 정책을 설계해야 한다. “표를 triple로 바꾸기만 하면 끝”이 아니다. 단순 집계만 필요한 테이블을 무조건 RDF로 옮기는 이득은 별도로 입증해야 한다. 이 비교는 교재의 선택 기준이며 제품 성능 우열을 측정한 결과가 아니다.

Blank node는 외부 참조·갱신에 어려움을 줄 수 있으므로 장기간 여러 시스템에서 식별해야 하는 장비·작업에는 안정적인 IRI를 고려한다. 모든 blank node를 금지한다는 뜻은 아니다. 익명 구조가 필요한 경우와 지속 식별이 필요한 경우를 나눈다.

<a id="c5-07"></a>
## 7. 읽고 설명할 수 있는지 확인하기

**꼭 설명:** triple, 식별자와 문자열, 직렬화와 모델, 여러 원천 병합, named graph의 역할과 한계. **생략 가능:** 모든 구문 문법, 엔진 내부 triple index 설계, 후속 RDF 버전 전체 기능.

**확인 질문:** 같은 triple을 세 번 넣으면 세 독립 증거가 되는가? "E01"과 ex:E01은 같은가? 그래프 이름 D07이 권한 정책까지 자동 적용하는가?

### 해설

집합의 동일 triple은 출처 횟수를 보존하지 않는다. 문자열 값과 자원 식별자는 다르다. 그래프 이름의 의미와 접근 통제는 명시적 메타데이터·서비스 정책으로 구현해야 한다.
