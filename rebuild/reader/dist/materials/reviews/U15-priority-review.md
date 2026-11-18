# U15 Tree RAG 독립 기술·설명 검토

2026-11-19. [요약 계층 수업](../units/U15/01-build-summary-levels.md) 8,591자, [검색 비교 수업](../units/U15/02-compare-two-retrieval-modes.md) 6,815자, 총 15,406 Unicode 문자와 [RAPTOR 조사 기록](../research/U15-notes.md), [fixture](../examples/rag-tree/tree.json), [검증 스크립트](../examples/rag-tree/verify.py)를 대조했습니다. 이 검토에서는 원고를 수정하지 않았습니다.

## 설명을 보강할 자리

| 위치 | 검토 결과 |
| --- | --- |
| L01 57행, T03의 소프트 멤버십 | 두 부모 배정은 0.72·0.28이 모두 0.25를 초과하므로 표, 데이터, 코드가 일치합니다. T03 원문에는 대여품이 후속 창구를 옮기는 내용이 없습니다. T03을 S2에 의도적으로 겹쳐 넣은 이유를 ‘예약 유지와 반납 기한을 구별하는 넓은 주제에 시간 단서로 포함했다’ 정도로 쓰면 원문에 없는 이동을 배우지 않습니다. T07의 수령 때 번호 기록과 반납의 연결은 원문에 있습니다. |
| L02 11행, 길이 정의 | 100단위는 표의 합성 비용이며 문자를 세거나 토크나이저가 반환한 수치가 아닙니다. ‘노드 텍스트 길이만 셉니다’는 바로 앞의 합성 값 고지를 보완해 ‘표의 모의 노드 길이 값만 합산합니다’로 좁힐 수 있습니다. |
| L02 80행, 연습 1 | S2보다 T02의 수치가 높다는 비교를 질문 앞에 두면 같은 후보로 비교했다는 인상이 생깁니다. S2는 S1과 경쟁하고, T02는 0층에서 가지가 확장됐을 때만 고려된다는 점을 질문에서도 먼저 묻습니다. 현 해설의 의미는 맞습니다. |
| L02 57행, 넓은 질문의 비교 | 통합 방식의 R1·S1·S2, 길이 96은 성립합니다. 같은 질문의 층별 k=1 결과도 R1→S1→T01, 길이 84로 손으로 따라갈 수 있습니다. 함께 보이면 넓은 질문의 반납·기록 단계가 두 방식에서 어떤 상세도로 남는지도 직접 비교할 수 있습니다. |

## 원논문과 구현 대조

- ICLR 공개 출판 PDF의 §3 및 그림 1–3, §4와 §4.1, 부록 B와 E 및 F를 해당 주장 가까이 대조했습니다. 그림 1은 여러 최상위 노드를 보여 줍니다. 한 루트 R1은 교육 예제의 선택입니다. 공개 코드의 기본 축소 차원 10에서는 현재 층 노드가 11개 이하이면 다음 층 제작을 멈춥니다. 따라서 예제의 리프 8개로 기본 설정에서 R1이 생성됐다고 추정할 수 없습니다. 수업은 수작업 구성임을 명시합니다. [ICLR 출판 PDF §3](https://openreview.net/pdf?id=GN921JHCRw#page=3), [저자 구현의 층 종료](https://github.com/parthsarthi03/raptor/blob/7da1d48a7e1d7dec61a63c9d9aae84e2dfaa5767/raptor/cluster_tree_builder.py#L87)
- 저자 공개 저장소 HEAD `7da1d48a7e1d7dec61a63c9d9aae84e2dfaa5767`을 내려받아 `GMM_cluster`의 위치별 확률과 엄격한 `>` 임계값, `perform_clustering`의 넓은 군집과 그 내부 군집을 확인했습니다. 복수 소속으로 한 리프가 여러 부모 아래에 나타날 수 있고, 이 toy 계층의 각 간선은 층 하나를 낮추므로 방향 순환이 없습니다. [군집 코드](https://github.com/parthsarthi03/raptor/blob/7da1d48a7e1d7dec61a63c9d9aae84e2dfaa5767/raptor/cluster_utils.py#L60)
- 같은 커밋에서 통합 검색은 코사인 거리 순서로 최대 `top_k`까지 보다가 첫 예산 초과에서 중단합니다. 층별 검색은 후보를 고른 후 자식 ID를 중복 제거하고 선택된 텍스트들을 연결합니다. 층별 함수에는 통합 검색과 같은 `max_tokens` 누적 중단이 없습니다. 두 검색에 같은 100단위를 쓴 조건과 서로 다른 후보 선택·종료 정책이 본문에서 구별됩니다. [검색 코드](https://github.com/parthsarthi03/raptor/blob/7da1d48a7e1d7dec61a63c9d9aae84e2dfaa5767/raptor/tree_retriever.py#L158)
- 출판본 그림 3은 QASPER 일부에 대해 층별 top-k 및 통합 후보 예산을 바꿔 비교하고, 후속 실험에 통합 검색을 채택한 이유를 설명합니다. 부록 B는 같은 SBERT·UnifiedQA·통합 검색 아래 의미 군집과 인접 원문을 묶는 대안을 비교합니다. 부록 E의 허구 전파 설명은 표본에 대한 관찰로 읽었습니다. [ICLR 출판 PDF 그림 3·§4](https://openreview.net/pdf?id=GN921JHCRw#page=6), [부록 B](https://openreview.net/pdf?id=GN921JHCRw#page=16), [공개 저자본 부록 E](https://arxiv.org/html/2401.18059v1#A5)
- 작은 조각을 검색하고 해당 조각이 나온 큰 원문을 반환하는 부모-자식 검색 설명이 공식 문서와 일치합니다. [LangChain ParentDocumentRetriever](https://reference.langchain.com/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever)

## 예제 확인

- `python learning-v2/examples/rag-tree/verify.py` 통과. 전체 11개 노드의 원문 또는 요약, 리프 위치, 본문의 길이와 두 점수가 fixture와 일치함을 독립 스크립트로 대조했습니다.
- 좁은 질문의 층별 k=1은 R1→S2→T03, 100단위로 시간만 확인할 수 있습니다. 통합은 T03→T02, 77단위로 시간과 증빙을 확인합니다. 후속 S2 추가가 113단위여서 종료합니다. 예산 65에서는 T03만 남습니다. 넓은 질문의 통합은 R1→S1→S2, 96단위입니다.
- 두 수업에 목차, 부모-자식 검색, 재귀 요약 계층의 구별과 원문·중간·최종 요약의 차이, 두 검색의 후보와 예산, 손실과 출처로 돌아가는 예가 있습니다. 범용 Tree RAG를 RAPTOR에 한정하거나 요약이 항상 향상된다고 주장하지 않습니다. 원논문 설정의 실제 LLM·토크나이저·임베딩·UMAP·GMM 재실행과 웹 화면 검증은 이 검토 범위에 포함하지 않았습니다.
