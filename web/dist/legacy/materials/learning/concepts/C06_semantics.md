# C6. RDFS·OWL·SHACL — 의미, 추론, 검사의 경계

**목표:** RDF 위에 의미를 더하는 원리를 익히고 OWL과 데이터 검증을 구별한다.

<a id="c6-01"></a>
## 1. RDF만으로 부족한 것은 무엇인가?

RDF에 “E01은 InspectionTool”이라고 써도 InspectionTool과 Equipment의 관계는 아직 없다. RDFS는 클래스·속성·하위 클래스·domain·range 등의 어휘와 의미를 제공한다. [RDF Schema 1.1](https://www.w3.org/TR/rdf-schema/)

~~~text
E01 rdf:type InspectionTool
InspectionTool rdfs:subClassOf Equipment
따라오는 타입: E01 rdf:type Equipment
~~~

RDFS 의미를 처리하는 추론 설정에서 이 결론을 얻을 수 있다. 아무 엔진에 RDF 파일만 넣으면 무조건 자동 계산되는 것은 아니다. 명세의 의미, 엔진의 지원, 실행 설정을 나누어 확인한다.

이 예에서 추론은 없던 현실을 만들어 낸 것이 아니라 주어진 전제의 귀결을 표현한다. 최초의 E01 타입 자체가 잘못됐다면 추론된 Equipment 타입도 현실의 정확성을 보장하지 않는다.

<a id="c6-02"></a>
## 2. domain과 range를 입력 검사로 읽으면 안 된다

~~~text
usedEquipment rdfs:domain Run
usedEquipment rdfs:range Equipment
X usedEquipment Y
~~~

RDFS에서는 X가 Run, Y가 Equipment라는 타입을 도출할 수 있다. “Run이 아닌 X를 입력했으니 거절하라”는 DB CHECK 문장으로 읽지 않는다. domain·range는 관계 사용에 따른 해석을 제공한다. [RDFS domain·range](https://www.w3.org/TR/rdf-schema/#ch_domain)

예를 들어 L02에 잘못 usedEquipment를 붙였다면 L02를 Run으로도 분류할 수 있다. 모델링 오류가 타입 추가로 나타나는 것이다. 서로 양립하지 않는 타입이라는 추가 공리가 없다면 이것만으로 모순이 드러나지 않을 수도 있다.

또 domain을 여러 개 선언하면 보통 “이들 중 하나”가 아니라 각 domain에 속한다는 해석이 적용된다. 허용 타입 목록을 나열하는 입력 검사의 직관과 다르므로 주의한다.

<a id="c6-03"></a>
## 3. OWL은 무엇을 더 제공하는가?

OWL(Web Ontology Language)은 클래스·속성·개체에 관한 더 풍부한 공리를 표현하고 논리적 의미를 부여하는 언어다. RDFS보다 복잡한 클래스 조건, 동치·비양립성, 속성 특성, 개수 조건 등을 표현할 수 있다. [OWL 2 Overview](https://www.w3.org/TR/2012/REC-owl2-overview-20121211/)

**동치:** 같은 클래스의 두 이름 또는 같은 개체의 두 이름을 선언할 수 있다. **비양립성:** 어떤 두 클래스가 겹칠 수 없다고 선언할 수 있다. **역관계:** hasPart와 partOf처럼 방향이 반대인 관계를 연결할 수 있다. **추이성:** A가 B의 조상이고 B가 C의 조상이면 A가 C의 조상이라는 식의 성질이다.

모든 업무 관계를 추이적으로 만들면 안 된다. E01이 D02를 사용했고 D02가 D11을 인용했다고 E01이 D11을 사용했다고 할 수 없다. 공리의 편리함보다 의미가 맞는지가 먼저다. 실제 계층·역관계 예는 [OWL Primer](https://www.w3.org/TR/owl2-primer/)에서 확인한다.

<a id="c6-04"></a>
## 4. 심화: 열린 세계와 이름의 동일성

열린 세계 가정은 기록되지 않은 것을 곧바로 거짓으로 확정하지 않는 해석이다. RUN002의 문서가 안 보이면 “아직 기록하지 않았을 수 있다”. 반면 입력 완전성을 검사할 때는 “제출 파일에 문서 ID가 없다”는 사실을 오류로 삼을 수 있다. 두 판단은 목적이 다르다.

OWL에서는 이름이 다르다고 반드시 개체도 다르다고 전제하지 않는다. 최대 한 문서라는 조건 아래 D02와 Revision2가 연결되어 있으면 같은 개체로 해석될 여지가 있다. 다르다는 명시적 조건 등과 조합되면 결과가 달라진다. [OWL Primer의 열린 세계·동일성 설명](https://www.w3.org/TR/owl2-primer/#OWL_and_Databases)

따라서 “OWL max 1이 있으니 문서 ID 두 개를 입력하면 항상 DB 오류”라고 설명하면 안 된다. 실제 제출 데이터의 값 개수를 검사하는 수단을 따로 두는 이유다.

<a id="c6-05"></a>
## 5. 심화: some·only·개수 조건과 프로파일

“문서를 some 사용한다”는 해당 종류의 대상이 적어도 하나 존재한다는 조건이다. “사용 대상은 only Document”는 사용한 대상이 모두 Document라는 조건이며, 사용 대상의 존재 자체를 요구하지 않는다. “정확히 하나”는 어떤 클래스의 서로 다른 대상 수를 세는지까지 읽어야 한다. [OWL Primer Property Restrictions](https://www.w3.org/TR/owl2-primer/#Property_Restrictions)

OWL의 표현력과 추론 비용 사이에서 EL·QL·RL 같은 프로파일을 고려한다. 이들은 단순 상하 등급이 아니다. EL은 큰 분류 모델, QL은 데이터 질의 재작성, RL은 규칙 기반 처리를 검토하는 출발점이다. 전체 OWL의 모든 기능을 지원한다고 해석하지 않는다. [OWL 2 Profiles](https://www.w3.org/TR/owl2-profiles/)

구현자는 사용 공리와 엔진 지원 범위를 고정해야 하지만 발표자는 프로파일 문법을 전부 외울 필요는 없다. “표현을 풍부하게 할수록 어떤 추론을 어떤 비용으로 수행할지 확인한다”는 원리를 설명하면 된다. 자세한 반례와 실행 검사는 [D1](../deep/D1_semantics.md)에 있다.

<a id="c6-06"></a>
## 6. SHACL은 어떤 질문에 답하는가?

SHACL은 데이터 그래프가 shapes로 주어진 조건을 만족하는지 검증한다. target은 검사 대상을, path는 볼 속성 경로를, minCount·datatype·class 등은 조건을 정한다. 결과에는 통과 여부와 위반 정보가 포함될 수 있다. [SHACL Recommendation](https://www.w3.org/TR/shacl/)

이번 사례에서 “Run에 usedDocument가 적어도 하나 있어야 한다”를 검사할 수 있다. 하지만 사용 문서가 현실에서 올바른지까지 자동으로 알지는 못한다. 문서의 유효 시각·적용 대상·원문 지지 여부는 추가 조건과 데이터가 필요하다.

검사 대상 선택도 중요하다. Run 타입을 기준으로 검사하는데 타입 자체가 누락됐다면 해당 대상이 빠질 수 있다. 또한 사전 추론이 누락 타입을 보충하면 검사 결과가 바뀔 수 있다. 보고서에 데이터·shape·추론 설정·대상 수를 함께 남기는 이유다.

<a id="c6-07"></a>
## 7. 발표 수준과 세 가지 판정

**꼭 설명:** RDF는 표현, RDFS·OWL은 의미와 귀결, SHACL은 조건 검사라는 구분. 열린 세계·필수값·동일성의 함정. **생략 가능:** 설명 논리의 완전한 증명 이론, 모든 OWL 문법과 프로파일 제약.

**확인 질문:** “검사 통과”, “논리적으로 따라옴”, “현실에서 참”은 같은가?

### 해설

검사 통과는 지정 데이터·대상·조건 범위의 결과다. 논리적 귀결은 전제와 의미론에 상대적이다. 현실의 참은 원천·관측·업무 검증 문제까지 포함한다. 셋을 구별해야 “검증을 통과한 지식만 운영 그래프에 넣는다”라는 정책에서도 무엇을 검증했는지 설명할 수 있다.
