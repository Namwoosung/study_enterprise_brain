# 누락값과 중복 매칭 때문에 집계가 바뀌는 경우

J3의 수행자는 기록되지 않았습니다. 작업 자체는 남겨 두고 수행자 칸만 비워 보여 주고 싶습니다. 반면 실제 수행자를 확인한 건만 보고 싶을 때는 J3를 빼야 합니다. 둘은 다른 질문이고, 필수 패턴과 선택 패턴이 그 차이를 만듭니다.

## 필수 패턴은 연결이 없으면 결과 행도 없습니다

다음 질의는 모든 Work 중 수행자 관계가 있는 것만 찾습니다.

```sparql
PREFIX ex: <https://example.org/query/>
SELECT ?work ?p WHERE {
  ?work a ex:Work ; ex:performedBy ?p .
}
ORDER BY ?work
```

J1·P1, J2·P1 두 행이고 J3는 없습니다. 이것으로 ‘J3에는 실제 수행자가 없었다’는 현실의 부정을 증명하지는 않습니다. 현재 조회한 그래프에 맞는 관계를 찾지 못했습니다. 원천 누락·매핑 오류·권한 제외·실제 미정 중 무엇인지는 별도 조사해야 합니다.

## OPTIONAL은 기준 행을 유지합니다

```sparql
PREFIX ex: <https://example.org/query/>
SELECT ?work ?p WHERE {
  ?work a ex:Work .
  OPTIONAL { ?work ex:performedBy ?p . }
}
ORDER BY ?work
```

첫 패턴이 세 작업을 기준으로 만듭니다. 선택 패턴은 맞는 수행자를 붙이고, 없으면 ?p를 **미바인딩(unbound)** 상태로 둡니다. 바인딩은 변수가 어떤 값과 연결됐다는 뜻입니다. J3는 행이 남되 ?p에 RDF 항목이 연결되지 않습니다. ‘담당자 미상’이라는 문자열이 저장된 것과 다릅니다. [SPARQL 1.1 §6](https://www.w3.org/TR/sparql11-query/#optionals)

Cypher에서는 다음처럼 읽습니다.

```cypher
MATCH (w:Work)
OPTIONAL MATCH (w)-[:PERFORMED_BY]->(p:Person)
RETURN w.id AS work, p.id AS person
ORDER BY work
```

매칭되지 않는 J3의 p는 null입니다. OPTIONAL MATCH는 앞에서 얻은 행을 유지하며 해당 선택 패턴에서 못 찾은 값을 null로 내보냅니다. RDF의 unbound와 Cypher의 null은 각각의 언어에서 해석해야 하며, 같은 누락 표시 글자로 화면에 나타나도 모든 연산의 의미가 같지는 않습니다. [Neo4j OPTIONAL MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/optional-match/)

## 선택 패턴 안팎의 조건은 목적이 다릅니다

P1의 이름이 ‘민수’라고 합시다. 아래 SPARQL은 P1을 수행자로 가진 작업에는 사람을 붙이고, 다른 작업에는 선택값을 붙이지 않습니다.

```sparql
PREFIX ex: <https://example.org/query/>
SELECT ?work ?p WHERE {
  ?work a ex:Work .
  OPTIONAL {
    ?work ex:performedBy ?p .
    FILTER(?p = ex:P1)
  }
}
ORDER BY ?work
```

조건이 OPTIONAL 안이므로 J3도 남습니다. 이를 밖으로 옮겨 `FILTER(?p = ex:P1)`를 전체 기준 행에 적용하면 J3의 ?p가 바인딩되지 않아 해당 조건을 참으로 만족하지 못하고 빠집니다. 필터 위치는 포맷 취향이 아니라 결과의 차이입니다.

Cypher에서 OPTIONAL MATCH 바로 다음에 붙인 WHERE는 그 선택 패턴의 일부입니다. 이를 ‘선택 후 전체 행 필터’로 자동 해석하면 안 됩니다. 후처리 조건을 명확히 하려면 `WITH`로 앞의 변수들을 다음 단계에 넘긴 뒤 필터를 적용할 수 있습니다.

```cypher
MATCH (w:Work)
OPTIONAL MATCH (w)-[:PERFORMED_BY]->(p:Person)
WITH w, p
WHERE p.id = 'P1'
RETURN w.id AS work
ORDER BY work
```

여기서 WITH는 중간 결과에서 유지할 변수를 다음 단계에 넘기는 구문입니다. 이 질의는 J1·J2만 남깁니다. J3까지 보여 주면서 선택된 수행자만 P1으로 제한하는 질의와 다릅니다. 외워서 옮기기보다 ‘기준 행을 남길 것인가, 조건이 맞는 행만 남길 것인가’를 먼저 문장으로 적습니다.

## 보고서가 늘어나면 같은 작업이 반복됩니다

작업의 근거 보고서를 추가합니다. J1에는 D1a·D1b, J2에는 D2가 있고 J3는 아직 없습니다. 두 보고서가 같은 작업 J1을 기술한다는 설정입니다. 각각이 별개의 수행을 뜻하지 않습니다.

```sparql
PREFIX ex: <https://example.org/query/>
SELECT ?work ?minutes ?report WHERE {
  ?work a ex:Work ; ex:minutes ?minutes .
  OPTIONAL { ?work ex:report ?report . }
}
ORDER BY ?work ?report
```

| work | minutes | report |
|---|---:|---|
| J1 | 10 | D1a |
| J1 | 10 | D1b |
| J2 | 20 | D2 |
| J3 | 10 | 바인딩 없음 |

이 결과의 minutes를 그대로 더하면 50입니다. 실제 입력의 세 작업 소요시간 합은 40입니다. 보고서 연결이 J1을 두 번 펼쳤기 때문입니다. RDF 그래프가 트리플의 집합이라는 사실과 SELECT 결과에 중복된 투영값이 나오는 것은 모순이 아닙니다. 서로 다른 보고서까지 포함한 매칭이 여러 개였고, 그 과정에서 작업의 시간이 반복됐습니다. 속성 그래프에서도 여러 보고서와 연결된 패턴을 펼치면 같은 집계 문제가 생길 수 있습니다.

집계 대상인 작업을 먼저 한 번씩 정한 다음 더할 수 있습니다.

```sparql
PREFIX ex: <https://example.org/query/>
SELECT (COUNT(?work) AS ?works) (SUM(?minutes) AS ?total) WHERE {
  {
    SELECT DISTINCT ?work ?minutes WHERE {
      ?work a ex:Work ; ex:minutes ?minutes .
      OPTIONAL { ?work ex:report ?report . }
    }
  }
}
```

안쪽 SELECT는 작업·시간 쌍을 고유하게 만듭니다. 이 예는 한 작업에 소요시간 하나만 있다는 전제이므로 세 행입니다. 바깥에서 3건·40분을 얻습니다. `SUM(DISTINCT ?minutes)`로 고치면 어떨까요? 고유한 **시간값**이 10·20 두 개라서 30이 됩니다. 다른 작업 J1·J3의 시간이 우연히 같다는 이유로 하나를 잃었습니다. DISTINCT가 무엇에 적용되는지 읽어야 하는 이유입니다.

Cypher에서도 `WITH DISTINCT w`처럼 작업을 먼저 고유하게 만든 뒤 w.minutes를 합칠 수 있습니다. 본문 표의 보고서 목록까지 유지해야 하면 먼저 작업별로 보고서들을 `collect`하여 한 행에 묶는 방식도 있습니다. `collect`는 여러 값을 목록으로 모으는 집계입니다. 업무 사건을 한 번 세는 것과 원천들을 모두 보여 주는 요구를 함께 만족할 수 있습니다.

## GROUP BY에 해당하는 묶음을 읽습니다

“장비별 작업 수와 시간 합”은 장비를 기준으로 그룹을 나눕니다.

```sparql
PREFIX ex: <https://example.org/query/>
SELECT ?equipment (COUNT(?work) AS ?works) (SUM(?minutes) AS ?total) WHERE {
  ?work a ex:Work ; ex:equipment ?equipment ; ex:minutes ?minutes .
}
GROUP BY ?equipment
ORDER BY ?equipment
```

E01은 2건·30분, E02는 1건·10분입니다. 그룹마다 다른 작업들을 모아 COUNT와 SUM을 계산합니다. 여기에는 보고서 패턴을 넣지 않아 그 중복은 발생하지 않습니다. Cypher는 반환하는 비집계 표현이 그룹 키 역할을 하는 경우가 있으므로 SPARQL의 GROUP BY를 단어 그대로 붙이지 않습니다. 같은 질문을 각 언어의 규칙으로 읽습니다.

## 설명 연습

**1.** OPTIONAL 후 COUNT(*)와 COUNT(?p)는 같나요?

이 입력에서는 전체 행은 3개, ?p 값이 있는 행은 2개입니다. COUNT(*)는 행, COUNT(?p)는 바인딩된 해당 표현을 세므로 다릅니다. DISTINCT ?p를 세면 P1 한 사람입니다.

**2.** 보고서가 둘인 J1에 DISTINCT minutes를 적용해 중복을 없앴습니다. 왜 합계가 40이 아니라 30인가요?

값이 같은 J3의 10분도 함께 합쳐졌습니다. 사건 ID와 그 사건의 값을 먼저 한 단위로 정해야 합니다.

**3.** 모든 작업을 보여 주려는데 수행자 ID 조건을 OPTIONAL 바깥에서 필터했습니다. 어느 행부터 확인할까요?

수행자 누락인 J3가 남는지 봅니다. 기준 행을 유지하려던 질문이라면 선택 패턴의 조건을 다시 구성해야 합니다. 조건에 맞는 수행이 있는 작업만 원하는 질문이었다면 행이 빠지는 것이 의도한 결과입니다.
