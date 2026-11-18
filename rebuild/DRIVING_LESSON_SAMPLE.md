# 설명 표본 — 같은 사람이 같은 차를 세 번 운전했다면

이 문서는 새 교재의 **설명 방식과 깊이를 검토하기 위한 본문 표본**입니다. 전체 교재나 웹 프로토타입의 완성본은 아닙니다. 이 내용을 바탕으로 도해가 포함된 세 가지 화면을 제작합니다.

목표는 RDF·Property Graph의 정의를 외우는 것이 아닙니다. 같은 사실을 두 방식으로 직접 표현하고, 구조가 달라지는 이유를 설명하는 것입니다. 익숙한 RDB도 함께 비교합니다.

## 1. 먼저 저장할 사실부터 정해 봅시다

민수는 같은 차 CarA를 세 번 운전했습니다. 각 운전의 시작 시각·거리·탑승 인원을 기록했습니다. 이 표에서 탑승 인원은 운전자를 포함한 수로 정하겠습니다.

| 운전 기록 | 사람 | 차 | 시작 시각 | 거리(km) | 탑승 인원 |
|---|---|---|---|---:|---:|
| drive1 | 민수 | CarA | 11월 1일 09:00 | 12 | 2 |
| drive2 | 민수 | CarA | 11월 1일 14:00 | 18 | 1 |
| drive3 | 민수 | CarA | 11월 2일 10:00 | 9 | 3 |

민수와 CarA는 같은 대상입니다. 달라지는 것은 **세 번의 운전 사건**입니다. ‘민수가 CarA를 운전한다’는 관계의 종류와 ‘11월 1일 오전에 한 운전’이라는 개별 발생을 구별해야 합니다.

이 자료로 두 가지 질문에 답해 보겠습니다.

- 민수는 CarA를 언제, 몇 번 운전했나요?
- 세 번의 운전 거리를 합치면 몇 km인가요?

정답은 세 번과 39km입니다. 어느 데이터 모델을 선택하든 이 사실이 보존되어야 합니다.

## 2. RDF로 사람과 차를 한 번 연결해 봅시다

RDF에서는 한 진술을 주어·술어·목적어의 세 부분으로 적습니다. 이 세 부분의 묶음을 triple이라고 부릅니다.

~~~text
주어: 민수       술어: 운전한다       목적어: CarA
~~~

RDF 파일에 적기 전에 대상에 식별자를 붙이겠습니다. 사람에게는 Minsu, 차에는 CarA, 운전 관계에는 drives라는 이름을 사용하겠습니다. 회사마다 같은 짧은 이름을 쓸 수 있으므로 이 이름이 어느 어휘에 속하는지도 함께 지정합니다.

~~~turtle
@prefix ex: <https://example.org/driving/> .
ex:Minsu ex:drives ex:CarA .
~~~

ex:Minsu는 https://example.org/driving/Minsu라는 긴 IRI를 짧게 적은 것입니다. IRI는 여기서 대상을 식별하는 이름입니다. ex:는 우리가 정한 접두사이며, prefix 선언은 짧은 표기를 어느 긴 이름으로 펼칠지 알려줍니다.

따라서 위 파일에서 prefix 선언은 데이터 triple에 포함되지 않습니다. 실제 진술은 둘째 줄의 한 개입니다. 주어는 ex:Minsu, 술어는 ex:drives, 목적어는 ex:CarA입니다.

RDF 그래프는 이런 triple의 집합입니다. 이 정의 때문에 **동일한 triple을 다시 적는 것만으로 서로 다른 발생 사건을 구별할 수 없습니다.** [RDF 1.1 Concepts §3](https://www.w3.org/TR/rdf11-concepts/#section-rdf-graph)

## 3. 같은 줄을 세 번 쓰면 세 번의 운전이 될까요?

~~~turtle
@prefix ex: <https://example.org/driving/> .
ex:Minsu ex:drives ex:CarA .
ex:Minsu ex:drives ex:CarA .
ex:Minsu ex:drives ex:CarA .
~~~

파일에는 세 줄을 적었지만 세 줄의 주어·술어·목적어가 모두 같습니다. 그래프로 읽으면 같은 진술 한 개입니다. 여기에는 오전 운전과 오후 운전을 구분할 정보가 없습니다.

그렇다면 drives에 시각과 거리를 붙이면 될까요? ex:drives라는 IRI 자체를 주어로 삼아 설명하는 것은 가능합니다. 하지만 그것은 **‘운전한다’라는 관계 종류 자체**에 대한 설명입니다. drive1의 거리와 drive2의 거리를 구분할 개별 운전의 식별자는 여전히 없습니다.

문제는 RDF로 운전을 표현할 수 없다는 것이 아닙니다. 현재 표현에는 ‘누가 어떤 차를 운전하는가’만 있고, ‘어느 운전 사건인가’가 빠져 있다는 것입니다.

## 4. 개별 운전에 이름을 붙이면 해결할 수 있습니다

첫 운전 자체를 drive1이라는 대상으로 만들겠습니다. 그러면 drive1에 운전자·차·시각·거리·인원을 각각 연결할 수 있습니다.

여기서 한 가지를 더 말하고 싶습니다. ‘drive1은 운전 사건이다.’ 이처럼 어떤 대상이 어떤 종류에 속하는지 적을 때 rdf:type을 사용합니다.

다음 이름들을 먼저 구별해 보세요.

| 표기 | 이 예제에서 뜻하는 것 |
|---|---|
| ex:Drive | ‘운전 사건’이라는 종류, 즉 클래스 |
| ex:drive1 | 첫 번째 실제 운전 사건을 가리키는 개체 |
| rdf:type | 왼쪽 대상이 오른쪽 클래스의 개체임을 나타내는 RDF 어휘 |
| ex:driver | 운전 사건과 운전자를 연결하기 위해 우리가 정한 관계 |
| ex:vehicle | 운전 사건과 차량을 연결하기 위해 우리가 정한 관계 |
| ex:startedAt | 운전 사건의 시작 시각 |
| ex:distanceKm | 운전 사건의 거리. 이 예제에서는 단위를 km로 고정 |
| ex:passengers | 운전자를 포함한 탑승 인원 |

rdf:도 ex:처럼 접두사입니다. 차이는 우리가 이 예에서 만든 어휘가 아니라 RDF가 정한 어휘의 namespace에 연결한다는 것입니다.

~~~text
rdf:type
→ http://www.w3.org/1999/02/22-rdf-syntax-ns#type
~~~

rdf:type의 오른쪽에 오는 ex:Drive는 이 예제의 도메인 클래스입니다. rdf:type이 ‘Drive라는 모든 도메인 용어를 미리 알고 있다’는 뜻은 아닙니다. 우리가 정한 도메인 클래스에 대해, 공통의 type 관계를 사용하는 것입니다.

RDFS라는 다른 어휘도 나중에 만납니다. 예를 들어 rdfs:subClassOf는 종류 사이의 포함 관계를, rdfs:label은 사람이 읽는 이름을 표현할 때 사용합니다. **drive1이 Drive의 개체라는 관계**와 **Drive가 어떤 더 큰 종류의 하위 클래스라는 관계**는 다릅니다. [RDFS의 클래스·속성 어휘](https://www.w3.org/TR/rdf-schema/)

## 5. 첫 운전은 다음 여섯 문장으로 적습니다

시각은 평범한 문자열만으로 남기지 않고 날짜·시각 값임을 표시하겠습니다. xsd:는 데이터 타입 이름을 짧게 적는 접두사입니다. ^^ 뒤에는 앞의 문자열을 어떤 데이터 타입의 값으로 해석할지 씁니다.

예를 들어 "2026-11-01T09:00:00+09:00"^^xsd:dateTime은 +09:00 시간대의 날짜·시각 값입니다. "12"^^xsd:integer는 정수 12입니다. 정수라고 표시했다고 단위가 자동으로 km가 되는 것은 아닙니다. 단위는 이 예제에서 distanceKm라는 속성의 의미로 정했습니다.

~~~turtle
@prefix ex: <https://example.org/driving/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:drive1 rdf:type ex:Drive .
ex:drive1 ex:driver ex:Minsu .
ex:drive1 ex:vehicle ex:CarA .
ex:drive1 ex:startedAt "2026-11-01T09:00:00+09:00"^^xsd:dateTime .
ex:drive1 ex:distanceKm "12"^^xsd:integer .
ex:drive1 ex:passengers "2"^^xsd:integer .
~~~

한 줄씩 읽어 봅시다.

1. drive1은 Drive 종류의 사건입니다.
2. 그 사건의 운전자는 민수입니다.
3. 그 사건에 사용한 차는 CarA입니다.
4. 그 사건은 11월 1일 오전 9시에 시작했습니다.
5. 그 사건에서 이동한 거리는 12km입니다.
6. 그 사건의 탑승 인원은 운전자를 포함해 두 명입니다.

여섯 문장의 주어가 모두 ex:drive1입니다. 덕분에 시각·거리·인원을 하나의 사건에 정확히 묶을 수 있습니다. W3C의 n-ary relation 설명도 관계를 새로운 개체로 나타내고 참여자·값을 연결하는 모델링 패턴을 다룹니다. [W3C n-ary relations](https://www.w3.org/TR/swbp-n-aryRelations/)

이것은 운전 사건을 모델링한 것입니다. ‘누가 어떤 문장을 주장했는가’를 표현하는 진술 메타데이터와는 목적이 다릅니다. 두 문제는 출처를 다루는 후속 수업에서 비교합니다.

## 6. 세 운전을 모두 표현하면 무엇이 늘어나나요?

같은 구조를 drive2와 drive3에도 적용합니다. 아직 축약 문법을 사용하지 않고 triple 하나를 한 줄에 적겠습니다.

~~~turtle
@prefix ex: <https://example.org/driving/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:drive1 rdf:type ex:Drive .
ex:drive1 ex:driver ex:Minsu .
ex:drive1 ex:vehicle ex:CarA .
ex:drive1 ex:startedAt "2026-11-01T09:00:00+09:00"^^xsd:dateTime .
ex:drive1 ex:distanceKm "12"^^xsd:integer .
ex:drive1 ex:passengers "2"^^xsd:integer .

ex:drive2 rdf:type ex:Drive .
ex:drive2 ex:driver ex:Minsu .
ex:drive2 ex:vehicle ex:CarA .
ex:drive2 ex:startedAt "2026-11-01T14:00:00+09:00"^^xsd:dateTime .
ex:drive2 ex:distanceKm "18"^^xsd:integer .
ex:drive2 ex:passengers "1"^^xsd:integer .

ex:drive3 rdf:type ex:Drive .
ex:drive3 ex:driver ex:Minsu .
ex:drive3 ex:vehicle ex:CarA .
ex:drive3 ex:startedAt "2026-11-02T10:00:00+09:00"^^xsd:dateTime .
ex:drive3 ex:distanceKm "9"^^xsd:integer .
ex:drive3 ex:passengers "3"^^xsd:integer .
~~~

사건 하나당 타입 한 문장, 사람·차 두 문장, 시각·거리·인원 세 문장입니다. 따라서 이 표현에서는 **6 × 3 = 18개 triple**입니다.

민수와 차를 세 개씩 복제한 것은 아닙니다. 서로 다른 세 사건이 같은 사람·차를 참조합니다. 사람의 이름·타입, 차량 속성, 클래스 선언 등을 더 적으면 triple 수는 늘어나므로 18은 이 예제의 범위에서 센 값입니다.

## 7. Property Graph에서는 어떻게 표현할까요?

이번에는 Neo4j의 Property Graph 모델을 기준으로 보겠습니다. 사람과 차를 각각 노드로 만들고, 두 노드 사이에 DROVE 관계를 세 개 만듭니다. 관계 각각에 시작 시각·거리·탑승 인원을 붙입니다. 노드뿐 아니라 관계도 속성을 가질 수 있습니다. [Neo4j Graph database concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/)

아래 코드는 작은 예제를 만드는 Cypher입니다. p와 c는 이 코드 안에서 노드를 가리키는 변수입니다. Person과 Car는 노드 라벨이고, DROVE는 관계 타입입니다. 관계별 속성은 대괄호 안 중괄호에 들어갑니다.

~~~cypher
CREATE (p:Person {id: 'Minsu', name: '민수'}),
       (c:Car {id: 'CarA'})
CREATE (p)-[:DROVE {
  startedAt: datetime('2026-11-01T09:00:00+09:00'),
  distanceKm: 12, passengers: 2
}]->(c)
CREATE (p)-[:DROVE {
  startedAt: datetime('2026-11-01T14:00:00+09:00'),
  distanceKm: 18, passengers: 1
}]->(c)
CREATE (p)-[:DROVE {
  startedAt: datetime('2026-11-02T10:00:00+09:00'),
  distanceKm: 9, passengers: 3
}]->(c)
~~~

세 관계의 시작 노드·끝 노드·타입이 같아도 서로 다른 관계로 만들 수 있습니다. 이번 표현에서는 운전의 개별 발생을 관계 하나가 나타냅니다. RDF 사건 모델에서는 그 역할을 drive1 같은 자원이 맡았습니다.

그렇다고 Property Graph에서는 사건을 노드로 만들면 안 되는 것은 아닙니다. 운전에 사고 기록·승인·동승자 개체·여러 문서를 더 연결해야 한다면 Drive 노드가 더 편할 수도 있습니다. 처음에는 두 노드 사이의 발생을 관계 속성으로 표현하고, 요구가 늘어날 때 사건 노드 대안을 검토하는 것입니다.

## 8. RDB로 이미 할 수 있던 일도 함께 봅시다

관계형 모델에서도 표현할 수 있습니다. Person·Car 테이블이 있고 Drive 테이블에 운전자 ID와 차량 ID를 외래키로 저장하면 됩니다. 각 운전은 Drive의 서로 다른 행입니다.

~~~sql
SELECT drive_id, started_at, distance_km, passengers
FROM Drive
WHERE person_id = 'Minsu' AND car_id = 'CarA'
ORDER BY started_at;
~~~

이 쿼리는 처음 표의 세 운전 기록을 반환합니다. 사람 이름·차량 설명이 필요하면 해당 테이블을 JOIN할 수 있습니다. 따라서 그래프 모델의 장점을 설명할 때 ‘RDB에서는 관계를 표현할 수 없다’고 말하면 안 됩니다.

비교할 것은 같은 정보를 어떻게 조직하고, 원하는 질문을 어떤 구조·질의로 표현하는가입니다. 복잡한 연결 탐색과 실행 비용은 더 큰 사례에서 따로 측정해야 합니다.

## 9. 두 그래프에서 같은 질문을 해보겠습니다

RDF 예제에는 SPARQL로 질문할 수 있습니다. ?d는 조건을 만족하는 운전 사건, ?km는 그 사건의 거리 값입니다. 같은 ?d가 type·driver·vehicle·distance 조건에 반복되므로 모두 같은 운전 사건에 대한 조건입니다.

~~~sparql
PREFIX ex: <https://example.org/driving/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT (COUNT(?d) AS ?drives) (SUM(?km) AS ?totalKm)
WHERE {
  ?d rdf:type ex:Drive .
  ?d ex:driver ex:Minsu .
  ?d ex:vehicle ex:CarA .
  ?d ex:distanceKm ?km .
}
~~~

Property Graph 예제에서는 관계를 r이라는 변수로 잡고 관계 수·관계 속성을 집계합니다.

~~~cypher
MATCH (:Person {id: 'Minsu'})-[r:DROVE]->(:Car {id: 'CarA'})
RETURN count(r) AS drives, sum(r.distanceKm) AS totalKm
~~~

이 예제의 기대 결과는 둘 다 drives=3, totalKm=39입니다. RDF 예제의 SPARQL과 대응 SQL은 동봉 검사에서 실행했습니다. Cypher는 이번 표본에서는 읽기용으로 제시했으며 Neo4j 서버 실행 검증은 아직 하지 않았습니다.

이제 ‘RDF는 사건을 대상으로 삼아 값을 연결했고, 이 Property Graph 예는 관계의 개별 발생에 값을 붙였다’는 차이를 데이터와 질의 양쪽에서 설명할 수 있습니다.

## 10. ‘RDF 모델과 Turtle 구문이 다르다’는 말도 실제로 확인해 봅시다

앞의 가장 작은 사실인 ‘민수가 CarA를 운전한다’는 같은 그래프를 Turtle과 RDF/XML로 적을 수 있습니다. §2에서 쓴 Turtle을 XML 형태로 적으면 다음과 같습니다.

~~~xml
<rdf:RDF
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:ex="https://example.org/driving/">
  <rdf:Description rdf:about="https://example.org/driving/Minsu">
    <ex:drives rdf:resource="https://example.org/driving/CarA"/>
  </rdf:Description>
</rdf:RDF>
~~~

rdf:about은 설명하는 주어를, ex:drives 요소는 술어를, rdf:resource는 목적어 자원의 IRI를 표시합니다. 두 namespace 선언은 접두사를 어떤 IRI로 해석할지 정합니다. XML의 열고 닫는 태그 때문에 더 길어 보이지만 읽어 낸 진술은 같습니다.

~~~text
주어: https://example.org/driving/Minsu
술어: https://example.org/driving/drives
목적어: https://example.org/driving/CarA
~~~

**RDF는 이 진술들을 구성하는 데이터 모델이고, Turtle·RDF/XML은 그것을 파일에 적는 구문입니다.** 두 파일을 파서로 읽어 같은 그래프인지 확인할 수 있습니다. 이번 표본의 검사에서도 두 결과가 같음을 확인합니다. [RDF Primer의 구문 예제](https://www.w3.org/TR/rdf11-primer/#section-graph-syntax)

여기서는 두 표현을 읽을 만큼만 배웠습니다. JSON-LD까지 같은 자리에서 이름만 추가하지 않고, 실제 JSON과 RDF를 연결할 필요가 생기는 다음 예제에서 설명합니다.

## 11. 반도체 작업으로 옮겨 보면

‘민수가 CarA를 세 번 운전했다’를 ‘L02 로트를 E01 장비에서 세 번 작업했다’로 바꿔 보세요. 작업마다 시각·사용 절차·측정값이 다르다면 **어느 작업의 정보인가**를 보존해야 한다는 문제는 같습니다.

작업에 담당자·문서·관측 결과·검토 이력이 더 연결된다면, RDF든 Property Graph든 작업을 독립 사건으로 모델링할 수 있습니다. 모델을 고르는 기준은 ‘선이 적어 보이는가’가 아니라 우리가 묻는 질문과 관리할 지식을 정확히 담는가입니다.

이 예는 원리를 옮기는 가상 사례이며 기존 합성 corpus의 RUN002 등을 세 번 발생한 것으로 바꾸지는 않습니다.

## 12. 이해를 확인할 질문

먼저 설명해 보고 해설을 읽어 보세요.

1. 동일한 RDF triple을 세 번 쓰면 왜 세 운전이 보존되지 않나요?
2. ex:drive1 rdf:type ex:Drive에서 세 항목은 각각 어떤 역할인가요?
3. 차의 색상을 저장할 때는 운전 사건에 붙여야 할까요, 차량에 붙여야 할까요?
4. drive2의 거리만 바꾸려면 각 모델에서 무엇을 찾아야 할까요?
5. 운전마다 승인자·사고 기록·여러 동승자를 연결해야 한다면 Property Graph에서도 Drive 노드를 고려할 이유는 무엇인가요?

### 해설

1. 세 진술이 완전히 같고 RDF 그래프는 triple의 집합이기 때문입니다. 사건별 식별 정보를 추가해야 합니다.
2. drive1은 구체 사건, rdf:type은 클래스 소속을 나타내는 관계, Drive는 사건의 종류입니다.
3. 특정 시점의 차 색상을 어떻게 관리할지는 요구에 따라 달라지지만, 우선 ‘차 자체의 속성’과 ‘개별 운전의 속성’을 구분해야 합니다. 현재 색상을 단순 기록한다면 차량에 붙입니다. 색상 변경 이력까지 필요하면 시점 표현이 추가됩니다.
4. RDF에서는 drive2 자원의 거리 진술을, 관계 기반 Property Graph에서는 두 번째 운전을 나타내는 관계를 찾아 바꿉니다. 운영에서는 시간값만으로 식별하지 않고 안정적인 업무 ID를 부여하는 방안도 검토합니다.
5. 사건 자체를 여러 관계의 중심으로 참조하기 쉬워지기 때문입니다. 관계 속성 방식만 정답이라고 고정하지 않습니다.

## 웹 도해 제작 명세

이 부분은 집필자를 위한 명세이며 실제 수업 화면에서는 제작 설명 대신 그림으로 구현합니다.

- 상단에 원자료 세 행. 한 사건을 선택하면 양쪽 그림·코드에서 같은 사건만 강조.
- 왼쪽 RDF: 민수·CarA를 공유하고 drive1~3을 각각 배치. 사건 하나를 펼치면 type·사람·차·값의 여섯 연결이 드러남.
- 오른쪽 Property Graph: 같은 사람·차 두 노드 사이의 세 관계를 분리해서 배치. 각 관계의 시각·거리·인원을 가까이 표시.
- ‘한 번 → 세 번’을 선택하면 추가되는 구조가 보임. 기본 화면의 복잡도를 줄이되 전체 표현을 정적으로 볼 수 있음.
- 표시 개수는 사건 진술 6→18, 관계 1→3으로 범위를 정확히 표기. 이 수를 성능 우열로 시각화하지 않음.
- 아래에서 같은 질의를 실행한 기대 결과 3·39를 대조. 실행하지 않은 엔진은 기대 결과로 명시.
- 모바일은 같은 사건을 유지한 채 위아래 비교. 색뿐 아니라 사건 ID·선 패턴으로 대응.

이 표본의 비교 기준은 RDF 1.1과 Neo4j의 Property Graph입니다. 이후 RDF 1.2 확장은 별도 심화에서 다룹니다.
