# U15 RAPTOR 근거 기록

확인일 2026-11-19. [계층 구축](../units/U15/01-build-summary-levels.md), [두 탐색 비교](../units/U15/02-compare-two-retrieval-modes.md).

| 주장 | 읽은 자료와 구간 | 제한 |
| --- | --- | --- |
| 작은 조각으로 검색하고 더 큰 원문을 반환하는 부모-자식 검색 | [LangChain Reference, ParentDocumentRetriever](https://reference.langchain.com/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever) | 대표 구현입니다. 여기서는 반환 원문과 재귀 생성 요약의 차이를 설명합니다. |
| 조각·임베딩→군집→새 요약 텍스트→반복 | [Sarthi et al., ICLR 출판 PDF §3 및 Figure 1](https://proceedings.iclr.cc/paper_files/paper/2024/file/8a2acd174940dbca361a6398a4f9df91-Paper-Conference.pdf#page=3), [저자 구현 ClusterTreeBuilder](https://github.com/parthsarthi03/raptor/blob/7da1d48a7e1d7dec61a63c9d9aae84e2dfaa5767/raptor/cluster_tree_builder.py#L87) | 출판본은 여러 최상위 노드를 보여 줍니다. 이 교육 예제는 루트 하나이며, 기본 코드에서 여덟 조각으로 생성한 계층이 아닙니다. |
| UMAP의 이웃 범위, 로컬·글로벌 그룹, GMM 확률과 BIC 및 EM, 긴 군집 재처리 | [RAPTOR §3 Clustering Algorithm](https://arxiv.org/html/2401.18059#S3), [저자 구현 cluster_utils.py의 GMM_cluster, perform_clustering 및 RAPTOR_Clustering](https://github.com/parthsarthi03/raptor/blob/master/raptor/cluster_utils.py) | 모의 값의 소속을 확인했습니다. UMAP/GMM을 실행해 노드나 확률을 얻은 실험은 아닙니다. |
| 층별 상위 후보 이후 자식 탐색, 전 층 비교와 토큰 예산 | [RAPTOR §3 Querying, Figures 2–3 및 Appendix F](https://arxiv.org/html/2401.18059#S3), [저자 구현 tree_retriever.py](https://github.com/parthsarthi03/raptor/blob/master/raptor/tree_retriever.py) | 부록 의사 코드와 실제 공개 코드 표기에 차이가 있습니다. 본문 알고리즘의 코사인 비교·자식 단계와 공개 코드의 첫 예산 초과 중단을 설명합니다. 같은 예산은 교육 예제에서 맞췄으며 공개 코드의 두 함수가 동일 예산 규칙을 집행한다고 일반화하지 않습니다. |
| QASPER 일부 비교와 후속 실험 설정, 연속 조각 균형 트리 대비 ablation | [RAPTOR §3 Querying, §4 Controlled Baseline Comparisons, Appendix B §§B.1–B.2](https://arxiv.org/html/2401.18059#S4) | 실제 성능은 당시 데이터와 조건에 국한됩니다. 본 교재의 장비 사례에서 얻은 점수로 연결하지 않습니다. |
| 요약에서 근거 누락·허구 가능성, 제한 표본의 상위 전파 관찰 | [RAPTOR Appendix E §§E.1–E.3](https://arxiv.org/html/2401.18059#A5) | 오류가 항상 전파되거나 전파되지 않는다고 결론 내리지 않습니다. |

원문·요약·교육용 확률·점수·길이는 [fixture](../examples/rag-tree/tree.json)에 있습니다. [검증 스크립트](../examples/rag-tree/verify.py)는 표준 라이브러리로 복수 소속, 층별 연결, 두 질문의 서로 다른 문맥 및 예산 변경을 검사합니다. 원문 임베딩·군집·생성 모델은 실행하지 않았습니다. [독립 검토](../reviews/U15-priority-review.md)의 원문·소속 근거, 합성 길이 설명, 탐색 연습 및 넓은 질문 비교 제안을 반영했습니다.
