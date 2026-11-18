# U13 검색 추적 수업 근거 기록

확인일 2026-11-18. 대상은 [검색 추적 수업](../units/U13/01-retrieval-trace.md)과 [문서·청크 데이터](../examples/rag-trace/trace.json)입니다.

| 주장 ID | 자료와 실제 확인 구간 | 본문에 적용한 내용 | 적용 범위 |
| --- | --- | --- | --- |
| U13-C01 | [Lewis et al., NeurIPS 2020, Fig. 1과 §2.1 Models, §2.2 Retriever, §2.3 Generator, §2.4 Training](https://papers.neurips.cc/paper_files/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf#page=2) | 생성기 파라미터와 외부 문단 인덱스의 역할, DPR 질문·문단 인코더의 내적 검색, 응답 전체와 토큰별 문단 확률 결합의 차이, 고정 문서 인코더·인덱스와 질문 인코더·생성기 미세조정. | 논문의 BART 입력은 문단 하나와 질문을 결합합니다. §2.1은 문단별 생성 확률을 결합하므로 수업의 단일 프롬프트 구성과 계산 구조가 다릅니다. 논문의 평가 수치는 사용하지 않았습니다. |
| U13-C02 | [Manning, Raghavan & Schütze, Introduction to Information Retrieval, §6.3.1 Dot products](https://nlp.stanford.edu/IR-book/html/htmledition/dot-products-1.html) | 코사인 분모에 두 벡터의 길이가 들어가고, 길이 정규화 후의 내적과 일치합니다. 제곱합·제곱근과 예제 산술로 풉니다. | 교과서 예제는 어휘 기반 벡터입니다. 청크에 부여한 좌표와 검색 품질에 대한 증거로 쓰지 않습니다. |
| U13-C03 | [Malkov & Yashunin, arXiv v4, §3–4 및 알고리즘 2·5](https://arxiv.org/pdf/1603.09320#page=4), [Azure AI Search, About ANN](https://learn.microsoft.com/en-us/azure/search/vector-search-ranking#about-ann) | 높은 층의 진입점에서 이웃을 탐색하고 아래층으로 내려가며 후보를 좁힙니다. 근사 탐색 결과는 전수 검색 결과와 대조할 수 있습니다. | 검색용 연결을 업무 지식 그래프의 의미 관계로 해석할 수 없다는 설명은 두 구조의 역할을 적용한 교재 비교입니다. HNSW 인덱스 실행, 재현율, 응답 시간 측정은 범위 밖입니다. |
| U13-C04 | [Azure AI Search, Common chunking techniques](https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents#common-chunking-techniques) | 고정 길이, 문서 제목·문장 구조에 따른 나누기, 겹치는 영역으로 문맥 보존을 설명합니다. | 청크 분리 전후의 검색 순위는 합성 벡터에 따른 모의 결과입니다. 테이블 원본은 합성 자료를 설명하는 본문 도해입니다. |
| U13-C05 | [Azure AI Search, How embedding models are used in vector queries](https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-generate-embeddings#how-embedding-models-are-used-in-vector-queries), [Lewis et al., §2.2 Retriever](https://papers.neurips.cc/paper_files/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf#page=3) | Azure 사용 예는 인덱싱과 검색에 동일 임베딩 모델을 사용합니다. DPR은 호환되는 질문·문단 인코더를 짝지어 사용합니다. | 특정 공급사의 벡터 차원, 입력 형식, 모델 성능은 이 수업에서 결론 내리지 않습니다. |
| U13-C06 | [Azure AI Search, Set the filter mode](https://learn.microsoft.com/en-us/azure/search/vector-search-filters#set-the-filter-mode) | 적용 조건과 상위 k 제한의 순서에 따라 후보를 놓칠 수 있습니다. 제품 문서의 ‘strictPostFilter’ 설명이 전체 상위 k 확정 후 필터의 예입니다. | 수업은 일곱 건을 하나의 목록으로 전수 비교합니다. 제품의 분할 처리와 HNSW 탐색 재현율을 수업 계산에서 예측하지 않습니다. |
| U13-C07 | [Introduction to Information Retrieval, Okapi BM25: a non-binary model](https://nlp.stanford.edu/IR-book/html/htmledition/okapi-bm25-a-non-binary-model-1.html) | 단어 빈도와 문서 길이, 전체 문서에 걸친 단어 빈도를 이용하는 점수 방식입니다. | 수업의 네 단어 가중 합은 표기 일치 원리를 보여주는 별도 계산입니다. |
| U13-C08 | [Azure AI Search, How RRF ranking works](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking#how-rrf-ranking-works) | 각 목록에서 위치에 따른 역수를 계산하고, 청크 ID별로 더해 통합합니다. | 상수 60은 수업의 선택입니다. 검색 서비스에서 산출한 점수는 사용하지 않았습니다. |
| U13-C09 | [Azure AI Search, Semantic capabilities and limitations](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview#semantic-capabilities-and-limitations) | 재정렬의 입력은 기존 검색 후보입니다. 순위를 다시 매기는 것만으로 검색 목록 밖의 글을 다시 가져오지 않습니다. | 0–3점은 문서의 역할을 드러내기 위한 모의 점수입니다. Azure 서비스 점수와 비교할 수 없습니다. |

## 예제와 검산

- 합성 예제는 문서 6건과 기본 청크 7건으로 구성했습니다. 2026-04-10에 D01a는 만료, D03a는 다른 장비입니다. 2026-02-15에는 기준을 뒷받침하는 매뉴얼 판본이 D01 v2입니다.
- Python 3.14.6 표준 라이브러리로 JSON을 읽고 코사인, 날짜·장비 필터, 문자 일치 점수, RRF, 모의 재정렬, 글자 수를 계산했습니다. 저장소 루트에서 python learning-v2/examples/rag-trace/verify.py로 재현할 수 있습니다. 기본 벡터 후보는 D05a·D02b·D02a, 어휘 후보는 D04a·D02a·D05a입니다. 최종 근거는 D02a·D04a이며 원문 88자와 본문에 제시한 인용 두 건이 일치합니다. [검산 스크립트](../examples/rag-trace/verify.py)
- 분할 실험은 D02a를 D02-s1과 D02-s2로 교체합니다. 수치가 들어 있는 D02-s2는 벡터와 어휘 양쪽 상위 3개에서 빠집니다. 재정렬과 100자 예산 적용 뒤 근거는 D04a·D02-s1이며 원문은 77자입니다.
- 실행으로 확인한 부분은 합성 데이터의 산술과 조건 비교입니다. PDF 파싱기·임베딩 모델·ANN 인덱스·재정렬 모델·LLM은 호출하지 않았습니다. 예제 답변은 사람이 쓴 추적용 예시입니다.

## B06 수업 확장

2026-11-19. [질문별 검색 설계 수업](../units/U13/02-query-design-and-failures.md)을 추가했습니다. 앞 수업의 D01~D06과 [확장 자료 D07~D08](../examples/rag-trace/query-design.json)에서 판정·기록을 따로 찾는 어휘 점수, 질문의 기준일과 장비 유지, 후보의 규정·관측 역할을 비교합니다. [검산](../examples/rag-trace/verify_query_design.py)은 실제 합성 문자열, 날짜 필터, 88자 예산과 잘린 검색의 두 동점 후보를 확인합니다.

| 주장 ID | 자료와 실제 확인 구간 | 적용 범위 |
| --- | --- | --- |
| U13-C10 | [Ma et al., Query Rewriting in Retrieval-Augmented Large Language Models, §3.1 Rewrite-Retrieve-Read](https://aclanthology.org/2023.emnlp-main.322.pdf#page=3) | 원 질문에서 검색문을 만들고 원 질문과 검색 문맥을 함께 읽히며, 필요한 경우 여러 검색문을 만드는 배경입니다. 논문의 평가·학습 구성을 운영 예제로 일반화하지 않습니다. |
| U13-C11 | [Liu et al., Lost in the Middle, TACL 2024, §2.1 Experimental Setup 및 §2.3 Results and Discussion](https://aclanthology.org/2024.tacl-1.9.pdf#page=3) | 다중 문서 구성에서 정답 위치와 다른 문서 수를 통제한 실험을 설명합니다. 이 교재 예제에 대한 입력 위치 실험과 모델 실행은 하지 않았습니다. |

단일 사실·여러 근거·판본 효력·경향 질문에 적합한 자료 범위의 차이를 비교합니다. 평가 방법은 U16에서 다룹니다. 요약·키워드 설계와 모든 문서 파싱기의 성능을 결론 내리지 않습니다.
