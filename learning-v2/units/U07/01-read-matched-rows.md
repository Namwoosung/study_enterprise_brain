# Cypher와 SPARQL에서 패턴이 결과 행이 되는 과정

그래프의 점과 선을 이해했어도 쿼리에 같은 변수가 여러 번 나오면 헷갈릴 수 있습니다. 이번 단원은 언어의 모든 문법을 익히는 과정이 아닙니다. 질문에서 어떤 패턴을 찾고, 어느 대상을 같은 변수로 묶으며, 그 결과가 몇 행이 되는지 읽는 연습입니다. Cypher는 Neo4j의 속성 그래프, SPARQL 1.1은 RDF 그래프를 기준으로 비교합니다. 두 언어가 모든 세부 의미를 공유하는 것은 아닙니다.

## 먼저 같은 질문에 필요한 자료를 고정합니다

합성 정비 자료입니다. 소요 시간은 모두 분 단위이고, 원천이 기록한 값입니다. 실제 반도체 작업 시간이나 표준 절차를 뜻하지 않습니다.

| 작업 | 대상 장비 | 수행자 | 소요 시간 |
|---|---|---|---:|
| J1 | E01 | P1 민수 | 10 |
| J2 | E01 | P1 민수 | 20 |
| J3 | E02 | 미수록 | 10 |

이 단원에서는 작업을 두 모델 모두 독립 대상으로 둡니다. 속성 그래프에서도 사건을 노드로 둘 수 있다는 U03의 선택을 사용했습니다. RDF에서는 `minutes`가 작업에서 정수값으로 가는 술어이며, 속성 그래프에서는 작업 노드의 속성입니다.

```text
J1 → equipment → E01
J1 → performedBy → P1
J1의 minutes = 10
```

RDF 입력 일부는 다음과 같습니다. 세미콜론은 같은 주어 J1을 이어 쓰고 `10`은 Turtle에서 정수값으로 읽습니다.

```turtle
@prefix ex: <https://example.org/query/> .
ex:J1 a ex:Work ; ex:equipment ex:E01 ;
  ex:performedBy ex:P1 ; ex:minutes 10 .
ex:P1 a ex:Person ; ex:name "민수" .
```

속성 그래프에서는 Work 라벨의 J1에 id·minutes 속성을 두고, 장비 노드로 `ON_EQUIPMENT`, 사람 노드로 `PERFORMED_BY` 관계를 둡니다. RDF의 술어 이름과 Neo4j 관계 타입의 대소문자가 우연히 다르다는 점은 본질이 아닙니다. 모델에서 어느 부분을 값과 연결로 표현했는지를 읽으면 됩니다.

## 질문에서 같은 대상을 묶습니다

질문은 “E01에서 정비한 작업 ID와 수행자 이름은?”입니다.

```cypher
MATCH (w:Work)-[:ON_EQUIPMENT]->(:Equipment {id:'E01'}),
      (w)-[:PERFORMED_BY]->(p:Person)
RETURN w.id AS work, p.name AS person
ORDER BY work
```

`MATCH`는 조건을 만족하는 패턴을 찾습니다. `(w:Work)`는 Work 라벨의 노드를 w로, `(p:Person)`은 사람 노드를 p로 가리킵니다. 이름 없는 장비 괄호에는 변수 대신 ID 조건만 적었습니다. 두 번째 줄의 w는 첫 줄에서 찾은 **그 작업**이어야 합니다. 쉼표로 연결한 패턴을 같은 매칭 안에서 만족해야 하므로 장비가 E01이고 수행자도 있는 작업이 남습니다. `RETURN`은 출력 열, `AS`는 열의 별명이고 `ORDER BY`는 그 출력의 정렬입니다. [Neo4j MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/match/)

RDF의 대응 질의는 다음과 같습니다.

```sparql
PREFIX ex: <https://example.org/query/>
SELECT ?work ?person WHERE {
  ?work a ex:Work ; ex:equipment ex:E01 ; ex:performedBy ?p .
  ?p ex:name ?person .
}
ORDER BY ?work
```

`PREFIX`는 Turtle의 @prefix와 역할이 비슷한 주소 줄임표입니다. SPARQL에서는 끝에 마침표를 붙이는 prefix 문법을 쓰지 않습니다. 물음표로 시작하는 `?work`, `?p`, `?person`은 찾는 값을 담는 변수입니다. `WHERE { ... }` 안에 맞아야 할 트리플 패턴을 적습니다. `SELECT`는 결과에 보여 줄 변수입니다. `?p`는 연결에 필요하지만 여기서는 출력하지 않습니다. Turtle에서 읽던 `a`와 세미콜론도 이 패턴에서 같은 축약 역할을 합니다. [SPARQL 1.1 §2·§5](https://www.w3.org/TR/sparql11-query/#basicpatterns)

이 입력에서 어느 단계가 어떻게 좁혀지는지 봅니다. 아래 표는 의미를 이해하는 전개이며 엔진의 실제 실행 순서는 아닙니다.

| 논리 단계 | 작업 | 장비 | 사람 주소 | 출력 이름 |
|---|---|---|---|---|
| E01의 작업 | J1 | E01 | 아직 미지정 | 아직 미지정 |
| E01의 작업 | J2 | E01 | 아직 미지정 | 아직 미지정 |
| 수행자 연결 | J1 | E01 | P1 | 아직 미지정 |
| 수행자 연결 | J2 | E01 | P1 | 아직 미지정 |
| 이름 읽기 | J1 | E01 | P1 | 민수 |
| 이름 읽기 | J2 | E01 | P1 | 민수 |

SPARQL 결과의 `?work`는 ex:J1·ex:J2라는 IRI이고, Cypher의 w.id는 'J1'·'J2'라는 속성 문자열입니다. 같은 사건을 찾지만 반환값의 자료형은 다릅니다. 화면에서 접두사를 줄여 표시한다고 IRI가 문자열 코드와 똑같아진 것은 아닙니다. 서로 다른 시스템 사이에 옮길 때는 그 대응을 매핑으로 정합니다.

## 값 조건과 출력 제한

“E01의 작업 중 15분 이상 걸린 작업은?”으로 질문을 바꿉니다.

```cypher
MATCH (w:Work)-[:ON_EQUIPMENT]->(:Equipment {id:'E01'})
WHERE w.minutes >= 15
RETURN w.id AS work, w.minutes AS minutes
ORDER BY minutes DESC
LIMIT 5
```

`WHERE` 뒤는 비교 조건입니다. `>=`는 크거나 같음, `DESC`는 내림차순, `LIMIT 5`는 앞의 최대 다섯 행을 반환한다는 뜻입니다. 현재 입력에는 J2·20 한 행뿐입니다. LIMIT을 5로 두었다고 없는 다섯 작업을 만드는 것은 아닙니다.

```sparql
PREFIX ex: <https://example.org/query/>
SELECT ?work ?minutes WHERE {
  ?work a ex:Work ; ex:equipment ex:E01 ; ex:minutes ?minutes .
  FILTER(?minutes >= 15)
}
ORDER BY DESC(?minutes)
LIMIT 5
```

SPARQL은 `FILTER`에 표현식을 적어 현재 변수값을 검사합니다. 전체 `WHERE`는 패턴의 묶음이고, Cypher의 WHERE와 모양만 보고 같은 자리에 단어를 교체하면 안 됩니다. `minutes`가 문자열이라면 숫자 비교·합산의 해석이 달라질 수 있습니다. 입력 자료형까지 확인해야 합니다.

LIMIT만 있고 정렬이 없으면 어떤 순서를 보장하는지 기대하지 않습니다. ‘최근 작업’이면 작업 시각을 모델에 두고 시간 내림차순을 요청해야 합니다. ID가 큰 것을 최근이라고 가정하는 것은 ID 발급 정책이 보장할 때만 가능합니다.

## 같은 사람이 두 번 나오면 무엇을 센 걸까요?

첫 질의에서 이름만 선택하면 민수·민수 두 행입니다. 작업이 두 건이라 같은 사람을 두 번 매칭했습니다. `DISTINCT`로 중복 출력값을 없애면 민수 한 행이 됩니다. 하지만 다른 두 사람의 이름이 모두 민수라면 이름만 DISTINCT한 것은 사람 수가 아닙니다. 사람 ID를 기준으로 구별해야 합니다.

```sparql
PREFIX ex: <https://example.org/query/>
SELECT (COUNT(?work) AS ?works) (COUNT(DISTINCT ?p) AS ?people) WHERE {
  ?work a ex:Work ; ex:equipment ex:E01 ; ex:performedBy ?p .
}
```

괄호 안의 `COUNT`는 조건을 만족한 값의 개수를 집계하며 `AS ?works`가 결과 열 이름을 붙입니다. 현재 한 작업에 수행자 한 명뿐인 입력에서는 works=2, people=1입니다. 수행자가 여러 명으로 늘면 work가 사람마다 반복되므로 COUNT(?work)가 사건 수와 달라질 수 있습니다. 다음 수업에서 그 중간 행을 직접 늘려 보겠습니다. [SPARQL aggregates](https://www.w3.org/TR/sparql11-query/#aggregates), [Cypher aggregating functions](https://neo4j.com/docs/cypher-manual/current/functions/aggregating/)

## 설명 연습

**1.** 첫 질의의 두 번째 w를 다른 변수 x로 바꾸면 왜 같은 질문이 아닐 수 있나요?

E01의 작업 w와 수행자 연결을 갖는 작업 x를 같은 대상으로 묶는 조건이 사라집니다. 독립적인 매칭의 조합이 생길 수 있습니다. 변수 이름 자체보다 같은 변수를 재사용하는 위치가 중요합니다.

**2.** 사람 이름이 민수 두 행이니 수행자가 두 명이라고 해도 될까요?

이 입력에서는 P1 한 사람이 두 작업을 수행한 결과입니다. 작업·사람·이름의 집계 단위를 구별하고 사람 ID의 고유 수를 셉니다.

**3.** 쿼리를 읽으면서 이미 J2라는 답을 알았는데도 왜 자료형을 확인하나요?

실제 입력에서 20이 문자열이거나 시간 단위가 초이면 비교 조건의 의미가 달라집니다. 눈으로 읽는 숫자와 시스템이 해석하는 값·단위를 맞춰야 합니다.
