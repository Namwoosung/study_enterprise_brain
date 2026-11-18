# 기업 지식을 이해하고 구축하는 학습 교재

프로그래밍 경험이 있는 학습자가 기업 지식의 의미 설계·수집·연결·검증·검색·변경 관리를 기초부터 설명할 수 있도록 구성했습니다. 본편 U01~U18과 survey 별첨 S01, 총 56수업입니다. 정의에 이어 원문·데이터·중간 결과·대안·반례와 설명 연습·해설을 제공합니다. 출처는 각 주장과 가까운 곳에 연결했습니다.

[비공개 학습 웹](https://enterprise-knowledge-lab-namws.sheermackerel2.chatgpt.site) · [로컬 학습 웹](../web/dist/index.html)

## 어디에서 시작할까요?

처음부터 연결하려면 U01→U07의 기초를 읽은 뒤 U08→U12의 지식 구축, U13→U16의 검색·평가, U17→U18의 운영·통합으로 진행합니다. 이미 그래프·RDF·기초 질의를 공부했다면 U08부터 시작하고 필요한 기초를 본문 검색과 용어 찾기로 복습할 수 있습니다. 기초 단원 끝의 설명 문제를 먼저 풀어 보고 이유까지 설명할 수 있는 부분은 넘어가도 됩니다. 진단은 강제 잠금이나 자격 판정이 아닙니다.

S01은 논문 *A Comprehensive Survey on Automatic Knowledge Graph Construction*을 따라 읽는 별첨입니다. 본편을 논문 목차로 대체하지 않습니다. U09 이후 병행하면 acquisition·refinement·evolution과 대표 연구의 입력·출력·평가를 연결하기 쉽습니다.

## 전체 단원

### U01 기업 지식과 Enterprise/Second Brain

- [기업은 무엇을 기억하고, 무엇을 설명해야 할까요](units/U01/01-company-memory.md)
- [개인 메모가 팀의 기억이 되려면](units/U01/02-personal-notes-to-shared-memory.md)

### U02 RDB와 Graph DB

- [같은 질문을 표와 그래프로 따라가기](units/U02/01-same-question-two-models.md)
- [경로가 길어지면 무엇을 계산하나요?](units/U02/02-variable-paths-and-query-work.md)
- [그래프 DB를 선택할 때 실행 계획에서 읽을 것](units/U02/03-read-plans-and-choose.md)

### U03 Property Graph와 Neo4j

- [속성 그래프에서 무엇을 노드와 관계로 만들까요](units/U03/01-property-graph.md)
- [속성값·식별자·시간을 잘못 정하면 생기는 일](units/U03/02-values-identity-and-time.md)
- [파일 재적재·제약·트랜잭션이 맡는 책임](units/U03/03-ingestion-and-constraints.md)

### U04 Semantic Web·W3C·RDF

- [데이터의 이름을 공유하는 방법: RDF를 처음부터 읽기](units/U04/01-rdf-language.md)
- [같은 사건을 RDF와 속성 그래프로 표현하기](units/U04/02-events-and-property-graphs.md)
- [사건이 일어났다는 말과 문서가 그렇게 주장한다는 말](units/U04/03-statements-and-context.md)

### U05 Ontology 도메인 설계

- [장비 정비 기록에서 도메인 온톨로지 설계하기](units/U05/01-domain-model.md)
- [이름과 의미를 재사용할 때 일치하는 범위를 정하기](units/U05/02-reuse-vocabularies-and-models.md)
- [모델을 개정한 뒤 같은 질문에 다시 답하기](units/U05/03-evolve-model-and-mappings.md)

### U06 RDFS·OWL·SHACL

- [같은 데이터에서 추론과 검증이 다른 답을 내는 이유](units/U06/01-inference-and-validation.md)
- [OWL 공리를 추가하면 어떤 결론이 생기나요?](units/U06/02-classes-relations-and-inference.md)
- [‘있다’, ‘모두’, ‘하나’는 입력 검사와 어떻게 다른가요?](units/U06/03-quantifiers-and-cardinality.md)
- [추론 결과를 저장할지, 질문할 때 계산할지](units/U06/04-profiles-and-deployment.md)

### U07 Cypher·SPARQL 읽기

- [Cypher와 SPARQL에서 패턴이 결과 행이 되는 과정](units/U07/01-read-matched-rows.md)
- [누락값과 중복 매칭 때문에 집계가 바뀌는 경우](units/U07/02-optional-and-aggregation.md)
- [경로·그래프 범위·결과 형태를 구별해 읽기](units/U07/03-paths-graphs-and-results.md)

### U08 Knowledge Graph

- [연결된 자료를 질문에 답하는 Knowledge Graph로 발전시키기](units/U08/01-from-links-to-knowledge.md)
- [고객의 보고를 어떤 지식으로 보여 줄까요?](units/U08/02-model-and-evidence-design.md)
- [같은 질문으로 세 가지 구축 방식을 비교하기](units/U08/03-build-and-evolve.md)

### U09 수집·정형 매핑·정보 추출

- [표의 한 행에서 근거가 있는 주장까지](units/U09/01-sources-and-mapping.md)
- [정비 문장에서 지식 후보를 추출하기](units/U09/02-mentions-and-events.md)
- [표와 본문이 섞인 문서를 읽고 추출 결과를 채점하기](units/U09/03-conditional-extraction.md)

### U10 Entity resolution·통합

- [서로 다른 기록에서 같은 장비를 찾기](units/U10/01-blocking-and-matching.md)
- [하나의 잘못된 연결이 다섯 레코드를 합칠 때](units/U10/02-clusters-and-correction.md)
- [같은 장비의 서로 다른 값들을 통합하기](units/U10/03-fusion-with-provenance.md)

### U11 검증·사람 검토·암묵지

- [형식에 맞는 주장, 원문에 맞는 주장, 사실로 확인된 주장](units/U11/01-validate-the-claim.md)
- [검토 대기열에 무엇을 보낼지 결정하기](units/U11/02-review-capacity-and-evidence.md)
- [숙련자의 판단을 조건이 붙은 지식으로 옮기기](units/U11/03-capture-conditional-knowledge.md)

### U12 Auto ontology·자동 구축

- [자동 온톨로지 구축에서 무엇을 학습할까요](units/U12/01-what-gets-learned.md)
- [검사 문서에서 개념과 공리 후보를 만드는 과정](units/U12/02-documents-to-ontology.md)
- [후보를 평가하고 온톨로지 개정을 배포하기](units/U12/03-review-and-release.md)
- [NVIDIA Auto Ontology가 데이터베이스에서 만드는 의미 계층](units/U12/04-nvidia-auto-ontology.md)

### U13 Vector RAG

- [정비 질문 한 건을 Vector RAG 안에서 추적하기](units/U13/01-retrieval-trace.md)
- [같은 자료에서도 질문에 따라 검색을 바꾸기](units/U13/02-query-design-and-failures.md)

### U14 Graph RAG

- [부품 교체 기록에서 승인 근거까지 경로를 따라가기](units/U14/01-follow-evidence-path.md)
- [문서 전체의 변화를 묻는다면 무엇을 검색하나요?](units/U14/02-communities-local-global.md)
- [그래프 질의를 선택하고 틀린 관계의 파급을 따라가기](units/U14/03-query-and-operate.md)

### U15 Tree RAG·RAPTOR

- [여러 문서의 조각을 묶어 요약 계층 만들기](units/U15/01-build-summary-levels.md)
- [같은 질문을 두 방식으로 검색해 컨텍스트 비교하기](units/U15/02-compare-two-retrieval-modes.md)

### U16 RAG 평가

- [같은 질문과 근거로 검색을 비교하기](units/U16/01-retrieval-evaluation.md)
- [맞는 답, 근거가 있는 답, 인용이 정확한 답 비교하기](units/U16/02-answer-quality-and-experiment.md)

### U17 지식의 변경·출처·권한

- [‘지금 맞는 답’과 ‘그때 알던 답’을 구별하기](units/U17/01-time-versions-and-provenance.md)
- [정정·철회가 파생 지식으로 전파되는 과정](units/U17/02-retraction-and-incremental-change.md)
- [권한이 원문에서 답변까지 이어지게 설계하기](units/U17/03-permissions-and-operating-evidence.md)

### U18 반도체 통합 사례·설명 연습

- [통합 사례 A: 정비 기록에서 원인 가설까지](units/U18/01-equipment-case.md)
- [통합 사례 B: 웨이퍼 이력과 문서의 적용 범위](units/U18/02-wafer-documents-and-inspection.md)
- [통합 사례 C: 같은 부품, 대체 부품, 조건부 경험](units/U18/03-parts-suppliers-and-experience.md)
- [시스템 선택을 설명하고 청중의 질문에 답하기](units/U18/04-design-and-explain.md)

### S01 자동 KG 구축 survey 해설

- [별첨 1: 자동 KG 구축 survey를 읽는 지도와 지식 획득](units/S01/01-reading-map-and-acquisition.md)
- [별첨 2: 학습 방법을 비교하고 추출 결과를 정제하기](units/S01/02-methods-and-refinement.md)
- [별첨 3: 조건·변화·저장과 논문을 읽은 뒤의 판단](units/S01/03-evolution-and-reading-conclusions.md)


## 웹에서 공부하기

사용자가 선택한 B안은 본문과 관련 비교 예제를 나란히 보여 줍니다. 좁은 화면에서는 설명 사이로 예제가 이동합니다. RDF/속성 그래프 사건 비교, 추론/입력 검사, 온톨로지 후보 검토, 날짜별 그래프 경로, Local/Global 입력, RAPTOR 요약 계층, 집계 단위와 원천 탐색을 본문과 대조합니다. 핵심 설명은 조작하지 않아도 본문·표·코드에서 읽을 수 있습니다.

본문 전체 검색, 단원·수업 안 목차, 용어의 짧은 설명과 본 수업 연결, 메모·책갈피·학습 표시·이어서 읽기와 JSON 내려받기를 제공합니다. 기존 교재와 기록은 legacy에 보존하며 새 수업의 완료로 자동 바꾸지 않습니다. 기록은 브라우저에 저장되고 기기 간 자동 동기화되지 않습니다.

## 예제와 근거의 범위

반도체 조직의 장비·문서·수치·회사·사건은 교육용 합성입니다. U18의 [30개 원천과 7종 표](examples/integrated/corpus.json)는 실제 제조 절차·공정 규격이 아닙니다. 개념과 모델링을 배우기 위한 자료입니다.

본문은 공식 규격·제품 문서·원논문을 우선 사용하며 제품 사례와 일반 원리를 구분합니다. NVIDIA Auto Ontology와 Microsoft GraphRAG의 구현 설명은 확인한 커밋·문서 범위를 연구 기록에 남겼습니다. Survey는 실제 읽은 공개 v1을 기준으로 출판 메타데이터와 구분했습니다.

RDF/SPARQL·SQLite·SHACL·선택 OWL-RL 규칙·산술은 동봉 Python에서 실행했습니다. Cypher는 공식 문서에 따라 예상 결과를 도출했으며 Neo4j 서버를 실행하지 않았습니다. 임베딩·추출·생성·GraphRAG/RAPTOR의 전체 실행이나 실제 성능 벤치마크는 수행하지 않았습니다. 모의 점수와 사람의 설명용 출력을 실측으로 해석하지 않습니다.

제작 근거는 research/, 검토와 수정은 reviews/, 예제와 실행 코드는 examples/에 있습니다. [전체 완료 검토](../rebuild/FINAL_ACCEPTANCE.md)는 각 범위와 검증의 한계를 기록합니다. 자동 검사와 AI 검토가 실제 학습자의 이해를 측정하거나 보장한 것은 아닙니다.
