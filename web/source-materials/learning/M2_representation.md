# M2. 무엇을 어떤 의미로 표현해야 연결할 수 있는가?

이전: [M1](M1_problem.md) · [교재 안내](README.md) · 다음: [M3](M3_acquisition.md)

> 학습 목표: 개체·개념·사건·주장을 구분하고, Ontology·스키마·KG·DB의 역할을 설명한다. RDF/OWL·Property Graph 예제에서 질의·추론·검증의 차이를 읽는다.

<a id="m2-01"></a>
## 1. 문장 하나에 숨어 있는 여러 선택

“L02는 E01에서 검사했다”를 가장 단순하게 그리면 다음과 같다.

~~~text
L02 ──검사에 사용한 장비──> E01
~~~

그런데 L02를 재검사했다면? 다른 시점에 다른 장비를 사용했다면? 검사 때마다 적용 절차가 바뀌었다면? 로트와 장비 사이의 선 하나에 모든 의미를 넣기 어려워진다.

이 사례에서는 **작업 발생 자체를 RUN002라는 대상**으로 만든다.

~~~mermaid
flowchart LR
  R["RUN002 · 검사 작업"] -->|"forLot"| L["L02"]
  R -->|"usedEquipment"| E["E01"]
  R -->|"usedDocument"| D["D02"]
  R -->|"occurredAt"| T["11/03 10:00 KST"]
~~~

이것은 교재의 모델링 선택이다. 모든 관계를 사건 노드로 만들어야 하는 규칙이 아니다. 시점·근거·여러 참여자를 함께 다뤄야 해서 작업을 식별 가능하게 만든 것이다. 단순 관계로 충분한 질문이라면 더 작은 모델도 가능하다.

이제 같은 L02에 RUN008과 RUN002를 연결하면 코팅 작업과 검사 작업을 구별할 수 있다. “L02의 장비”라는 단일 필드로 두 사실을 덮어쓰는 일을 피한다.

<a id="m2-02"></a>
## 2. 개념, 개체, 이름은 서로 다르다

**개념 또는 클래스**는 어떤 종류를 말하는지 정한다. Equipment는 장비라는 종류이고 InspectionTool은 검사장비라는 더 구체적인 종류다. **개체 또는 인스턴스**는 실제로 구별할 대상을 말한다. E01이 여기에 해당한다.

“검사기 1호”는 개체 자체가 아니라 사람이 사용하는 이름이다. E01과 E02는 같은 이름을 가질 수 있다. 이름이 같다는 사실에서 개체가 같다는 결론이 따라오지 않는다.

| 표현 | 의미 | 흔한 오류 |
|---|---|---|
| InspectionTool is-a Equipment | 검사장비 종류는 장비 종류에 포함 | E01을 Equipment의 하위 클래스로 만들기 |
| E01 instance-of InspectionTool | E01은 검사장비의 한 개체 | 종류와 실제 자산 혼합 |
| E05 part-of E01 | 센서 모듈이 장비의 구성 부분 | 부품을 장비의 하위 종류로 만들기 |
| E01 label “검사기 1호” | 표시 이름 | 이름을 전역 유일 ID로 쓰기 |

클래스와 인스턴스의 구분, 이름과 개념의 분리는 온톨로지 설계의 기본이다. [Ontology Development 101, 클래스 계층·명명 관련 설명](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html)

<a id="m2-03"></a>
## 3. 용어집에서 Ontology까지: 필요한 표현력을 선택한다

개발자는 “스키마”를 테이블 구조나 JSON 필드 제약으로 떠올리기 쉽다. 그 구조만으로 업무 의미가 완전히 정해지지는 않는다. status라는 필드가 있어도 그것이 승인 상태인지 장비 상태인지 알 수 없다.

| 수단 | 이 사례에서 하는 일 |
|---|---|
| 용어집 | 장비·로트·작업이 무엇인지 사람이 읽는 정의 |
| 통제 어휘 | 같은 의미의 선호 이름과 별칭 관리 |
| Taxonomy | 검사장비→장비처럼 종류의 계층 정리 |
| 스키마 | 작업에 어떤 필드·관계를 어떤 타입으로 기록할지 정의 |
| Ontology | 개념·관계·공리의 의미를 명시하여 공유·추론의 기반 제공 |
| Knowledge Graph | 실제 개체·관계·맥락을 연결해 지식을 표현한 결과 |

경계는 모든 프로젝트에서 칼같이 나뉘지 않는다. 온톨로지에도 스키마 역할이 있고, 스키마에도 일부 의미가 담긴다. 중요한 것은 **현재 정의가 무엇을 말하며 무엇을 말하지 않는지**다.

별칭과 주제 분류만 필요하면 SKOS 같은 통제 어휘 표현이 적절할 수 있다. SKOS의 broader는 개념 간 의미 계층이며 OWL 클래스의 subClassOf와 자동으로 같은 뜻이 되지 않는다. 공식적으로 풍부한 공리와 추론이 필요하면 OWL을 검토한다. [SKOS Primer §2](https://www.w3.org/TR/skos-primer/), [SKOS Reference §8](https://www.w3.org/TR/skos-reference/)

### 작은 설계 결정

질문이 “검사기라는 말로 검사장비 문서를 찾아줘”라면 별칭 사전으로 시작할 수 있다. 질문이 “검사장비로 분류된 모든 자산은 장비 조회에 포함되어야 한다”라면 종류의 포함 관계가 필요하다. “검사장비와 센서 모듈은 이 모델에서 서로 겹치면 안 된다”면 분리 공리 또는 검증 규칙도 검토한다.

처음부터 가장 강한 표현 체계를 선택하는 것이 항상 좋은 것은 아니다. 유지할 수 있는 의미를 정확히 정의하는 것이 먼저다.

<a id="m2-04"></a>
## 4. RDF: 세 칸의 데이터 모델

RDF 1.1의 기본 단위는 주어·술어·목적어 triple이다. 주어는 IRI 또는 blank node, 술어는 IRI, 목적어는 IRI·blank node·literal이 될 수 있다. IRI는 자원을 식별하고 literal은 문자열·날짜 같은 값이다. [RDF 1.1 Concepts §3](https://www.w3.org/TR/rdf11-concepts/#section-rdf-graph)

아래는 RDF를 Turtle 문법으로 쓴 예다. ex:는 긴 IRI의 접두어를 줄여 쓴 것이다.

~~~turtle
@prefix ex: <https://example.org/fab/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:RUN002
  ex:forLot ex:L02 ;
  ex:usedEquipment ex:E01 ;
  ex:usedDocument ex:D02 ;
  ex:occurredAt "2026-11-03T10:00:00+09:00"^^xsd:dateTime .
~~~

이 코드는 네 triple을 표현한다. 세미콜론은 같은 주어를 계속 쓰는 문법이다. RDF가 Turtle이라는 뜻은 아니다. RDF는 데이터 모델이고 Turtle·JSON-LD 등은 그 데이터를 표현하는 문법이다.

IRI가 웹 주소 모양이라고 반드시 그 주소에 웹페이지가 있어야 하는 것은 아니다. 여기의 example.org는 교재의 식별 공간이다. 반대로 “같은 장비를 가리키는 IRI”라는 합의는 저절로 생기지 않는다. M4에서 식별 정책을 다룬다.

blank node는 이름을 부여하지 않은 자원을 표현할 때 쓰지만, 외부 시스템에서 안정적으로 갱신·참조할 ID가 필요하면 설계상 안정된 식별자를 택할 수 있다. 이는 데이터의 의미와 운영 요구를 함께 고려하는 선택이다.

<a id="m2-05"></a>
## 5. RDFS와 OWL: 적힌 것에서 무엇이 따라오는가?

다음 두 문장을 가정하자.

~~~turtle
ex:InspectionTool rdfs:subClassOf ex:Equipment .
ex:E01 a ex:InspectionTool .
~~~

RDFS 의미 아래에서는 E01이 Equipment라는 결론도 따라온다. 이때 저장된 triple과 논리적으로 따라오는 triple은 구분할 수 있다. 질의 엔진이 어떤 추론을 적용하는지에 따라 결과가 달라질 수 있다. [RDF Schema §3.3~3.4](https://www.w3.org/TR/2014/REC-rdf-schema-20140225/)

더 주의할 예는 domain이다.

~~~turtle
ex:usedEquipment rdfs:domain ex:Run .
ex:Something ex:usedEquipment ex:E01 .
~~~

이 선언은 Something이 Run이라는 결론을 유도한다. “Something에 Run 타입이 없으니 데이터 입력을 거절하라”는 DB 검증 명령으로 읽으면 안 된다. [RDF Schema §3.2](https://www.w3.org/TR/2014/REC-rdf-schema-20140225/#ch_domain)

OWL은 클래스·관계의 더 풍부한 공리를 표현할 수 있다. 예를 들어 종류의 서로 배타적인 관계, 동일 개체, 관계의 성질 등을 정의한다. 다만 두 가지 전제가 개발자의 일반적인 데이터 검사 기대와 다를 수 있다.

- **열린 세계:** 기록되지 않은 사실은 아직 모르는 것일 수 있다. 승인 기록이 없다는 것과 승인되지 않았다는 주장은 다르다.
- **고유 이름을 자동 가정하지 않음:** 다른 IRI 두 개가 반드시 다른 현실 개체라고 자동 결론내리지 않는다.

예를 들어 어떤 관계가 함수적이라는 OWL 공리 아래 하나의 주체에 두 목적어가 붙으면, 조건에 따라 두 목적어가 같은 개체라는 결론이 나올 수 있다. 데이터베이스의 “값 두 개니까 무조건 오류”와 같은 의미가 아니다. [OWL Primer §4.7, §5.3, §6.1](https://www.w3.org/TR/owl2-primer/)

따라서 추론의 질문은 **“이 공리와 데이터가 참일 때 무엇이 따라오는가?”**이고, 검증의 질문은 **“이 제출 데이터가 우리가 정한 조건을 만족하는가?”**다. 현실의 사실성은 원문·측정·검토를 별도로 봐야 한다.

<a id="m2-06"></a>
## 6. Property Graph와 Neo4j: 같은 사건을 다른 표현으로

Neo4j의 Property Graph는 노드·관계에 속성을 붙이고 노드에 라벨을 부여한다. 관계에는 방향과 타입이 있다. RDF의 모든 것을 같은 방식으로 자동 번역한다기보다, 필요한 의미를 어떤 구조에 담을지 정한다. [Neo4j Graph database concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/)

~~~cypher
MERGE (l:Lot {id: 'L02'})
MERGE (e:Equipment {id: 'E01'})
MERGE (d:Document {id: 'D02'})
MERGE (r:Run {id: 'RUN002'})
SET r.occurredAt = datetime('2026-11-03T10:00:00+09:00')
MERGE (r)-[:FOR_LOT]->(l)
MERGE (r)-[:USED_EQUIPMENT]->(e)
MERGE (r)-[:USED_DOCUMENT]->(d);
~~~

이 예제는 학습용 빈 DB에서 읽을 코드다. 전체 파일에는 ID 유일성 제약을 포함한다. MERGE는 지정한 패턴으로 존재 여부를 찾거나 생성하는 동작이지, 두 이름이 같은 현실 장비인지 판단하는 기능이 아니다. 동시 실행에서 중복 방지까지 고려하려면 적절한 제약과 트랜잭션 설계가 필요하다. [Cypher MERGE 문서](https://neo4j.com/docs/cypher-manual/current/clauses/merge/)

RDF의 IRI 식별·어휘 의미, Property Graph의 라벨·속성을 변환할 때 같은 정보가 보존되는지 확인해야 한다. 특히 출처·언어 태그·타입·공리 같은 의미를 생략하면 모양이 비슷해도 같은 모델이 아니다.

<a id="m2-07"></a>
## 7. 질의해 보면 모델의 선택이 드러난다

SPARQL 예제:

~~~sparql
PREFIX ex: <https://example.org/fab/>
SELECT ?run ?equipment ?document
WHERE {
  ?run ex:forLot ex:L02 ;
       ex:usedEquipment ?equipment ;
       ex:usedDocument ?document .
}
~~~

Cypher 예제:

~~~cypher
MATCH (:Lot {id: 'L02'})<-[:FOR_LOT]-(r:Run)-[:USED_EQUIPMENT]->(e)
MATCH (r)-[:USED_DOCUMENT]->(d)
RETURN r.id, e.id, d.id;
~~~

두 코드는 각각의 그래프에서 연결 패턴을 찾는다. 위 작은 부분집합의 결과는 RUN002, E01, D02다. 전체 사례에서는 L02의 코팅 작업 RUN008도 있으므로 필터 없는 같은 의미의 질의는 그 작업까지 고려해야 한다. **작은 예제의 한 행을 전체 데이터의 유일한 정답으로 일반화하지 않는다.** [SPARQL 1.1 §2, 기본 패턴 질의](https://www.w3.org/TR/sparql11-query/)

실제 RDF 예제·질의는 [model.ttl](examples/model.ttl), [query.rq](examples/query.rq)에 있다. RDF 파싱·질의·일부 추론은 실행 검증하고, Neo4j 코드는 공식 문서와 대조하되 서버 실행은 하지 않았다. 상세 범위는 [실행 안내](examples/README.md)를 참고한다.

<a id="m2-08"></a>
## 선택 심화: 주장 자체를 기록하면 무엇이 달라지는가?

D07의 가설을 다음처럼 저장하면 안 된다.

~~~text
E01 ──caused──> I01
~~~

원문은 원인이라고 확정하지 않았다. 대신 “C043이라는 주장은 D07에서 나왔고 가설 상태이며 E01 점검 필요성을 말한다”고 표현할 수 있다. 여기서 주장 노드와 그 내용, 근거, 상태를 나눈다.

RDF 1.1에서는 statement reification이나 별도 주장·사건 모델을 쓸 수 있다. named graph도 묶음과 출처 관리에 활용할 수 있지만, 그래프 이름만으로 표준화된 출처·진실 의미가 자동 생기지는 않는다. 어떤 문장이 주장되었는지와 그 문장을 사실로 채택했는지의 정책을 명시해야 한다. [RDF Schema §5.3](https://www.w3.org/TR/2014/REC-rdf-schema-20140225/#ch_reificationvocab), [RDF Concepts §4](https://www.w3.org/TR/rdf11-concepts/#section-dataset)

복잡도가 커지면 다음을 따져본다. 모든 관계마다 주장 노드를 둘 것인가, 근거가 중요한 관계에만 둘 것인가? 원천에 있는 사실과 추론으로 만든 사실의 갱신 책임은 같은가? 더 많은 구조는 표현력을 주지만 검토와 유지 비용도 만든다.

## 확인 문제

1. E05 part-of E01을 E05 subClassOf E01로 바꾸면 왜 잘못되는가?
2. RDF와 Turtle, Ontology와 Neo4j의 관계를 각각 설명하라.
3. usedEquipment의 domain을 Run으로 선언하면 잘못된 주어 입력을 자동 거절하는가?
4. OWL에서 필수 관계가 있다는 공리와 SHACL의 minCount 검사는 같은가?
5. RUN002에 적용된 절차를 추적할 때 작업 노드가 주는 이점은 무엇인가?

### 해설

1. 두 자산의 구성 관계를 종류의 포함 관계로 바꾼다. 둘 다 이 사례의 개체다.
2. RDF는 데이터 모델, Turtle은 표현 문법이다. Ontology는 의미 모델이고 Neo4j는 저장·질의 구현 수단이다.
3. 아니다. 그 주어가 Run이라는 결론을 유도할 수 있다.
4. 아니다. OWL은 의미·함의에 관한 공리, SHACL은 선택한 데이터 그래프의 조건 검사다. M5에서 실제 실패 예를 본다.
5. 시점·로트·장비·문서·근거를 같은 사건에 붙여, 다른 작업의 조건과 섞이지 않게 한다.

**3분 설명:** RUN002를 그리며 “왜 장비 이름 두 개를 선으로 연결하는 것만으로 부족한가”를 설명하라. RDF와 Neo4j는 마지막에 표현 선택으로 소개한다.
