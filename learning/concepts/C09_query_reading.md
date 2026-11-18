# C9. Cypher와 SPARQL — 쿼리를 읽고 답의 범위를 판단하기

**목표:** 두 언어의 패턴·필터·출력을 읽고 빈 결과·중복·집계가 뜻하는 것을 설명한다.

이 단원은 쿼리 언어 완전 정복 과정이 아니다. 같은 작은 자료를 두 방식으로 읽어, 발표 중 예제를 설명할 수준을 목표로 한다.

<a id="c9-01"></a>
## 1. 둘 다 원하는 모양을 선언한다

Cypher는 Neo4j의 대표적인 선언적 그래프 질의 언어다. SPARQL은 RDF 질의 언어를 포함하는 W3C 표준군이다. 둘 다 “어떤 패턴을 만족하는 값을 달라”고 표현할 수 있지만 데이터 모델과 상세 의미는 다르다. [Cypher Overview](https://neo4j.com/docs/cypher-manual/current/introduction/cypher-overview/), [SPARQL 1.1 Overview](https://www.w3.org/TR/sparql11-overview/)

이 단원의 별도 최소 데이터는 다음 두 사건만 포함한다. 기존 사례에서 고른 읽기용 부분집합이다.

| 작업 | 로트 | 장비 | 사용 문서 |
|---|---|---|---|
| RUN002 | L02 | E01 | D02 |
| RUN008 | L02 | E03 | D04 |

질문은 “L02의 작업별 장비와 문서는?”이다. 이 네 열만 보면 답을 알 수 있지만, 이를 그래프 패턴으로 읽는 연습을 한다.

<a id="c9-02"></a>
## 2. Cypher를 왼쪽부터 읽기

~~~cypher
MATCH (r:Run)-[:FOR_LOT]->(l:Lot {id: 'L02'}),
      (r)-[:USED_EQUIPMENT]->(e:Equipment),
      (r)-[:USED_DOCUMENT]->(d:Document)
RETURN r.id AS run, e.id AS equipment, d.id AS document
ORDER BY run
~~~

MATCH는 조건을 만족하는 그래프 패턴을 찾는다. r·l·e·d는 찾은 대상에 붙이는 변수다. :Run은 라벨이고 {id:'L02'}는 속성 조건이다. 같은 변수 r을 반복했으므로 세 관계는 **같은 작업**에 연결되어야 한다. RETURN은 보고 싶은 값을, ORDER BY는 출력 정렬을 정한다. [Cypher MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/match/)

기대 결과는 RUN002/E01/D02, RUN008/E03/D04다. 이 쿼리는 문서가 당시 유효했는지 검사하지 않는다. 그 조건은 데이터·필터를 추가해야 한다. 코드가 짧다는 것과 질문의 모든 의미가 반영되었다는 것은 다르다.

<a id="c9-03"></a>
## 3. SPARQL로 같은 질문 읽기

~~~sparql
PREFIX ex: <https://example.org/fab/>
SELECT ?run ?equipment ?document
WHERE {
  ?run a ex:Run ;
       ex:forLot ex:L02 ;
       ex:usedEquipment ?equipment ;
       ex:usedDocument ?document .
}
ORDER BY ?run
~~~

?로 시작하는 것은 변수다. WHERE의 triple 패턴을 함께 만족하는 바인딩을 찾고 SELECT의 열로 반환한다. ex:L02는 문자열 ID 조건이 아니라 특정 IRI다. 결과에는 보통 IRI가 들어오며 UI가 이를 짧게 표시할 수 있다. [SPARQL 기본 그래프 패턴](https://www.w3.org/TR/sparql11-query/#BasicGraphPatterns)

Cypher 예시의 라벨·id 속성과 RDF 예시의 rdf:type·IRI는 다른 모델링 선택이다. 결과가 같도록 설계한 것이지 두 언어가 모든 경우 일대일로 치환된다는 뜻은 아니다. SPARQL 예제는 동봉한 Python/RDFLib 검사로 실행하며 Cypher는 별도 Neo4j 서버에서 실행 검증하지 않은 읽기용 예제로 범위를 명시한다.

<a id="c9-04"></a>
## 4. 필터·선택 관계·빈 결과 읽기

WHERE 또는 FILTER는 결과 조건을 좁힌다. OPTIONAL MATCH(Cypher), OPTIONAL(SPARQL)은 일부 관계가 없어도 주된 매칭을 남기는 데 쓰인다. 선택 관계의 값은 각각 null 또는 unbound로 나타날 수 있다. 이 둘의 상세 의미를 완전히 같다고 취급하지 않는다. [Cypher OPTIONAL MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/optional-match/), [SPARQL OPTIONAL](https://www.w3.org/TR/sparql11-query/#optionals)

예를 들어 사용 문서 관계가 없는 작업을 필수 패턴으로 조회하면 그 작업 자체가 결과에서 빠질 수 있다. “결과에 작업 두 개가 있으니 누락이 없다”고 결론내리기 전에 전체 작업 수와 비교해야 한다.

빈 결과는 이 데이터셋·권한·시점·패턴에서 매칭을 찾지 못했다는 뜻이다. 현실에 대상이 없다는 증명은 아니다. 잘못된 관계 방향, 다른 namespace, 누락 데이터, 미실행 추론이 원인일 수 있다.

<a id="c9-05"></a>
## 5. 심화: 중복과 집계의 함정

한 작업에 문서 두 개와 관측값 세 개를 독립 연결해 함께 매칭하면 조합이 여섯 행으로 늘 수 있다. 이때 행 수를 작업 수로 세면 틀린다. 작업 개수를 묻는다면 무엇을 DISTINCT로 셀지 정해야 한다.

L02에는 코팅과 검사 두 작업이 있으므로 작업 수 2와 로트 수 1을 구분한다. RDF 그래프가 triple의 집합이라는 사실도 SPARQL 결과가 언제나 중복 없는 집합이라는 뜻은 아니다. 여러 패턴 매칭이 동일한 출력값을 만들 수 있다. [SPARQL 결과 수정·중복](https://www.w3.org/TR/sparql11-query/#modifiers)

집계 전에 업무 단위를 적는 습관이 중요하다. “검토 요청률”은 로트 기준인가, 검사 작업 기준인가, 관측 행 기준인가? 쿼리가 실행되어 숫자를 반환해도 분모가 틀리면 업무 답은 틀린다.

<a id="c9-06"></a>
## 6. 심화: 쿼리를 생성하는 AI를 어떻게 확인할까?

자연어를 Cypher·SPARQL로 바꾸는 모델은 구문상 유효한 잘못된 질문을 만들 수 있다. “사용 문서” 대신 “현재 최신 문서”를 찾는 쿼리도 정상 실행될 수 있다.

교재의 검토 순서는 대상 식별 → 관계 의미 → 시간·권한 조건 → 집계 단위 → 결과 근거다. 읽기 전용 권한, 허용 관계·필드, 결과 크기·시간 제한은 실행 통제의 예다. 이는 특정 모델의 정확도를 보장하는 공식이 아니라 운영 설계 제안이다.

SPARQL의 ASK는 조건 만족 여부, CONSTRUCT는 결과 RDF 그래프를 만드는 데 사용된다. SELECT만 알아도 이번 발표의 중심 예제는 읽을 수 있지만, 질의 결과가 항상 표만 나오는 것은 아니라는 점은 기억한다. [SPARQL 질의 형태](https://www.w3.org/TR/sparql11-query/#QueryForms)

<a id="c9-07"></a>
## 7. 발표에서 읽을 수 있으면 충분한 범위

**꼭 읽기:** 패턴의 노드·관계·방향·변수, 필터, 출력, OPTIONAL, DISTINCT·집계의 업무 단위. **생략 가능:** 모든 쓰기·삭제 구문, 고급 경로 문법, 옵티마이저 튜닝, SPARQL federation 구현.

**확인 질문:** 위 두 쿼리는 L02의 불량 원인을 답하는가? 문서 없는 작업이 빠질 수 있는가? 결과 행 수가 곧 작업 수인가?

### 해설

두 쿼리는 기록된 사용 관계만 조회하며 원인을 판정하지 않는다. 문서가 필수 패턴이면 문서 없는 작업은 빠질 수 있다. 여러 관계 조합이 결과 행을 늘릴 수 있으므로 고유 작업을 기준으로 집계해야 한다.
