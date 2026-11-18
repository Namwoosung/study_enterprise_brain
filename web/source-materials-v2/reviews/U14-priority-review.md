# U14 Graph RAG 독립 기술·설명 검토

2026-11-19. 검토 대상은 `01-follow-evidence-path.md` 8,156자, `02-communities-local-global.md` 9,563자, `03-query-and-operate.md` 8,561자, 총 26,280 Unicode 문자와 `examples/rag-graph/graph.json`, 검증 스크립트, [U14 근거 기록](../research/U14-notes.md)입니다. 아래 줄 번호는 해당 초안 기준입니다.

## 결과에 영향을 주는 수정 사항

| 위치 | 문제와 확인 근거 | 수정 후 확인할 결과 |
| --- | --- | --- |
| [L03 §Cypher](../units/U14/03-query-and-operate.md#cypher), 초안 28행 | `MATCH (c)-[a:APPROVED_BY]->(person:Person)`은 관계가 존재하는지 확인합니다. 승인 원문 G04를 읽을 수 없거나 `a.source`가 비어 있어도 관계가 남아 있으면 행이 반환됩니다. 원문 회수 실패와 관계 부재를 동일시하면 U14-L01의 권한·출처 설명과도 충돌합니다. [Neo4j Cypher MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/match/) | 관계가 없을 때는 행이 빠지고, 관계가 있으나 원문을 회수하지 못했을 때는 조회 행은 남아도 승인자 답을 보류하는 식으로 설명합니다. |
| [L02](../units/U14/02-communities-local-global.md) 58·90행, [fixture](../examples/rag-graph/graph.json) 46·56행 | Map의 R-A2 요점은 ‘지정 공급사가 한빛정밀로 변경’이라고 답합니다. 표시된 R-A2 본문에는 공급사 이름이 없습니다. Global에 보고서 본문을 전달하는 설계에서 15점 요점의 고유명사 근거가 빠져 있습니다. | Map 요점에서 회사 이름을 빼거나 R-A2 본문과 fixture의 해당 보고서를 같은 근거 G03으로 보강합니다. |
| [L03](../units/U14/03-query-and-operate.md) 80행, [L02](../units/U14/02-communities-local-global.md) 58행 | 권한 설명에서 R-A2의 문장이라고 인용한 “김하늘이 승인했다”가 앞에서 읽은 R-A2와 fixture에 없습니다. 원래 보고서와 그 변형을 독자가 구별할 표지가 필요합니다. | 해당 문장을 넣은 가상 보고서 버전이라고 밝히거나, 보고서 본문을 변경한다면 fixture·Local 설명도 함께 대조합니다. |

## 설명 검토와 일치 확인

- L01 11행의 ‘아래 네 기록’은 11개 행 전체를 예고하므로, ‘아래 기록’으로 쓰거나 ‘현재 답에 필요한 네 근거와 다른 시점·부품의 대비 자료’로 역할을 설명합니다.
- L01 103행 연습의 `이별 → CR-121`은 그림과 fixture의 방향 `CR-121 → 이별`과 반대입니다. 순회 방향과 관계의 의미가 수업 목표이므로 같은 방향을 씁니다.
- L02 63행 ‘낮은 수준’과 ‘높은 수준’은 같은 수업 그림의 ‘상세도가 낮은 수준’과 ‘상세도가 높은 수준’에 대응하는 방향을 혼동할 수 있습니다. 논문 설명의 leaf-level은 ‘말단 커뮤니티’, higher-level은 ‘상위 커뮤니티’로 부르면 A/A1 예를 바로 대조할 수 있습니다. 원 논문은 말단의 요소 설명을 한도까지 넣고, 상위에서는 공간이 부족할 때 하위 설명 묶음을 짧은 보고서로 대체합니다. [Edge 외 §3.1.5](https://arxiv.org/html/2404.16130v2#S3.SS1.SSS5)
- L01 82행은 ID를 클릭하면 원문 페이지·행을 연다고 표현합니다. 이 합성 원문이 실제 문서로 연결된다는 뜻으로 읽히지 않도록, 예제에서는 조각 ID와 위 표의 위치를 대조한다는 설명과 실제 응용의 링크 설계를 구분합니다. 웹의 근거 표시 기능은 별도 확인합니다.

## 검산과 출처 확인

- `python learning-v2/examples/rag-graph/verify.py` 실행 통과. 4월 10일과 4월 1일에는 CR-119·한빛정밀·김하늘·G01/G02/G03/G04가 나왔고, 3월 20일에는 CR-106·세림밸브·박정우·G01/G02/G05/G06이 나왔습니다. 잘못된 경로가 반환한 G09는 CR-121 행입니다. 모의 Map 점수 상위 세 개의 90·88·84 순서도 확인했습니다.
- RDFLib 7.6.0에서 fixture 관계와 날짜를 본문 스키마의 RDF 트리플로 옮긴 뒤 본문의 SPARQL을 실행했습니다. 4월 10일과 4월 1일에는 CR-119·한빛정밀·김하늘, 3월 20일에는 CR-106·세림밸브·박정우가 반환됐습니다. CR-119의 승인 관계 트리플만 제거하면 4월 10일 결과는 0행입니다. Cypher와 Microsoft GraphRAG의 모델 실행은 검토 범위에 포함하지 않았습니다.
- Edge 등의 arXiv v2 §3.1.3–3.1.6에서 문자열 완전 일치, 발생 횟수 기반 관계 가중치, 계층 Leiden 분할, 말단·상위 보고서 구성, Global의 Map/Reduce를 대조했습니다. 공식 문서의 Local, Global 및 Neo4j retriever 설명도 대조했습니다. [Edge 외](https://arxiv.org/html/2404.16130v2#S3.SS1.SSS3), [Microsoft Local](https://microsoft.github.io/graphrag/query/local_search/#methodology), [Microsoft Global](https://microsoft.github.io/graphrag/query/global_search/#methodology), [Neo4j retrievers](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html#text2cypher-retriever)
- Microsoft 공개 소스 HEAD `34b2b67ae4601ad0b47bcd179fbe3f2a23aa0857`을 내려받아 Local의 개체 매핑과 보고서·관계·원문 문맥 합성, Global의 Map 배치와 양의 점수 요점 선별·내림차순 정렬을 확인했습니다. 초안이 개체 중심 혼합 입력과 보고서 위주 전역 입력을 설명한 방식과 일치합니다. [Local mixed context](https://github.com/microsoft/graphrag/blob/34b2b67ae4601ad0b47bcd179fbe3f2a23aa0857/packages/graphrag/graphrag/query/structured_search/local_search/mixed_context.py#L91), [Global search](https://github.com/microsoft/graphrag/blob/34b2b67ae4601ad0b47bcd179fbe3f2a23aa0857/packages/graphrag/graphrag/query/structured_search/global_search/search.py#L142)

## 단원 계약 대조

세 수업 전체에 범용 그래프 활용 RAG, KG와 Graph DB의 역할, 고정 그래프 경로와 생성 질의, 벡터 혼합, Microsoft Local·Global이 각자 어떤 입력을 받는지 들어 있습니다. 출발 후보 VL-042/VL-142에서 작업과 효력 날짜를 검사한 뒤 네 개 원문으로 돌아가는 흐름을 따라갈 수 있습니다. 초안은 벡터와 경로를 같은 자료·동일 생성예산에서 모의 비교했고, 문서 하나로 충분한 U13의 D02a 사례도 제시합니다. 승인 관계 한 건의 오염과 G17의 예외 누락은 서로 다른 오류 전파를 보여 줍니다. 구축·증분 갱신·권한·실행 제약을 본문 사례로 설명하고 연습 해답도 갖췄습니다. 위 수정사항을 통합한 후 근거 선택 도해와 모바일 화면에서 동일한 내용이 보이는지는 별도의 통합 검토 대상입니다.
