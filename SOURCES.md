# 학습 자료 조사 목록과 읽기 경로

주요 출처 확인: 2026-11-17 · 교재 반영 목록 개정: 2026-11-18 (Asia/Seoul)  
대응 계획: [LEARNING_PLAN.md 2.0](./LEARNING_PLAN.md)

아래 링크는 학습 계획과 Markdown 교재 작성에 활용한 자료다. 교재 작성 중 표준의 해당 절, 주요 연구의 방법론, 제품 공식 설명을 추가 대조했다. 주장별 확인 부분과 실제 실행 범위는 [교재 출처 기록](learning/EVIDENCE.md)에 정리했다. 전체 자료 정독과 모든 구현의 재현을 완료했다는 뜻은 아니다. 변경되는 제품 문서는 2026-11-17 확인 기준이며 후속 구현 시 릴리스·커밋을 고정한다.

**39개 항목을 사용자가 모두 정독하는 계획이 아니다.** 이 목록은 교재 제작자의 근거 자료 목록이다. 사용자는 [M1~M8 교재](learning/README.md)를 중심으로 공부하고 단원별 지정 원문 일부를 대조한다. 필수 읽기 분량과 선택 심화를 분리해 16시간 핵심 경로에 맞춘다.

| ID | 자료 | 성격·버전 | 읽을 범위·활용 | 주의점 |
|---|---|---|---|---|
| S01 | [Building a Second Brain Foundation](https://www.buildingasecondbrain.com/foundation) | 원저자 측 방법론 자료, 변경 가능 | 개인 지식 관리, CODE | 개인 생산성 효과의 독립 실증 근거로 사용하지 않음 |
| S02 | [Introducing Enterprise Brain — WRITER](https://writer.com/blog/enterprise-brain/) | 공급사 발표, 2026-09-09 | Enterprise Brain의 제품명 사용례 | 분야 전체의 표준 정의나 독립 성능 평가가 아님 |
| S03 | [Introduction to Information Retrieval](https://nlp.stanford.edu/IR-book/) | Manning, Raghavan, Schütze, 교과서, 2008 | 색인·랭킹·벡터 공간·평가, 특히 8장 | 현대 RAG 전체를 설명하는 자료는 아님 |
| S04 | [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://proceedings.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html) | Lewis et al., NeurIPS 2020 | 모델 구성, 검색·생성 결합, 실험 조건 | 원논문의 학습 구조와 현재 실무형 파이프라인을 구분 |
| S05 | [Knowledge Graphs](https://arxiv.org/abs/2003.02320) | Hogan et al., ACM Computing Surveys 2021; arXiv v6 | 데이터 모델, 스키마·동일성·맥락, 추론·구축·품질 | 분야 개관용. 개별 제품 동작은 공식 문서로 보완 |
| S06 | [Ontology Development 101](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html) | Noy & McGuinness, Stanford, 2001 | 범위·재사용·용어·클래스·속성·인스턴스, 역량 질문 | 설계 원리를 사용하고 오래된 도구·표준 설명은 최신 조사로 구분 |
| S07 | [RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/) | W3C Recommendation, 2014 | RDF 그래프·데이터셋, IRI·literal·blank node | 기초 기준 버전. 후속 버전의 지위를 따로 조사 |
| S08 | [RDF Schema 1.1](https://www.w3.org/TR/2014/REC-rdf-schema-20140225/) | W3C Recommendation, 2014 | 클래스·속성·subClassOf·domain·range | 추론과 유효성 검사를 혼동하지 않도록 예제 대조 |
| S09 | [SPARQL 1.1 Overview](https://www.w3.org/TR/sparql11-overview/) | W3C Recommendation, 2013 | 질의·갱신·프로토콜 문서의 관계 | 문법 세부는 연결된 Query Language 규격에서 확인 |
| S10 | [OWL 2 Overview](https://www.w3.org/TR/2012/REC-owl2-overview-20121211/) | W3C Recommendation, 2012, 2판 | 문서 체계, 구문·의미·프로파일의 관계 | OWL을 단순 그래프 포맷으로 설명하지 않음 |
| S11 | [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/) | W3C Recommendation, 2012, 입문 설명 | 클래스·속성·공리, 열린 세계·동일성, 추론 예시 | 규범적 세부는 구조 명세·의미론 문서로 추적 |
| S12 | [Shapes Constraint Language (SHACL)](https://www.w3.org/TR/shacl/) | W3C Recommendation, 2017 기준 | shapes, target, constraint, validation report | 1.2 등 후속 문서의 초안·권고 지위를 구별 |
| S13 | [PROV-O](https://www.w3.org/TR/prov-o/) | W3C Recommendation, 2013 | Entity·Activity·Agent, 생성·파생·책임 | 기술적 출처 기록과 내용의 사실성 보장은 다름 |
| S14 | [Neo4j Graph database concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) | 공식 제품 문서, 변경 가능 | 라벨·노드·관계·속성, Cypher 예제 | Neo4j 특성을 모든 그래프 DB의 정의로 일반화하지 않음 |
| S15 | [Neo4j documentation](https://neo4j.com/docs/) | 공식 문서 포털 | Cypher, 제약·인덱스, 운영, 드라이버, 라이선스·에디션 조건 탐색 | 링크된 실제 문서와 적용 버전을 추가 기록 |
| S16 | [Neo4j GraphRAG for Python](https://neo4j.com/docs/neo4j-graphrag-python/current/index.html) | 공식 패키지 문서, current | 검색기·파이프라인·호환 조건·예제 | Microsoft GraphRAG와 구분. 실행 전 버전 고정 |
| S17 | [LLMs4OL: Large Language Models for Ontology Learning](https://arxiv.org/abs/2307.16648) | Babaei Giglou et al., ISWC 2023 연구; 저자 공개본 | 유형 분류·분류체계 발견·비계층 관계 추출, 평가 조건 | 일부 과제 결과를 완전 자동 온톨로지 품질 보장으로 해석하지 않음 |
| S18 | [NVIDIA/auto-ontology](https://github.com/NVIDIA/auto-ontology) | NVIDIA 공식 저장소, main | README, 모델·매핑·관계·지표·출처·인증, 실행 예제 | 프로젝트 고유 개념과 W3C OWL의 의미를 대조. 커밋·의존성 고정 필요 |
| S19 | [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/) | Edge et al., Microsoft Research, 2024 연구 | 그래프 추출·커뮤니티 요약·전체 질문 평가 | 출판사 페이지에서 연결된 논문 본문·판본도 확인 |
| S20 | [Microsoft GraphRAG documentation](https://microsoft.github.io/graphrag/) | 공식 구현 문서, 변경 가능 | 인덱싱·질의·설정·입출력 | 현재 구현과 원논문 사이 변경점 기록 |
| S21 | [GraphRAG Query Engine](https://microsoft.github.io/graphrag/query/overview/) | 공식 구현 문서, 변경 가능 | local·global·DRIFT·basic의 구분 | 기본 경로는 local/global 원리·근거 추적. 설치·실행과 추가 방식은 선택 심화 |
| S22 | [RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval](https://arxiv.org/abs/2401.18059) | Sarthi et al., 2024, ICLR 논문 공개본 | 재귀 임베딩·군집·요약, 검색 전략, 실험·제거 실험 | 모든 Tree RAG를 RAPTOR로 정의하지 않음 |
| S23 | [RAPTOR ICLR proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/8a2acd174940dbca361a6398a4f9df91-Paper-Conference.pdf) | ICLR 2024 학회 공개본 | 방법론·평가의 출판본 대조 | 수치 인용 시 표·설정·모델·데이터를 함께 기록 |
| S24 | [How microchips are made — ASML](https://www.asml.com/en/technology/all-about-microchips/how-microchips-are-made) | 반도체 장비 제조사 공식 교육 자료, 변경 가능 | 웨이퍼 위 제조, 공정·장비·검사의 기본 맥락 | 기업별 실제 운영 절차나 합성 사건의 원인을 입증하는 자료가 아님 |
| S25 | [End-to-End Entity Resolution for Big Data: A Survey](https://arxiv.org/abs/1905.06397) | Christophides et al., 저자 공개본, v3 2020 | 식별·후보 찾기·매칭·통합 흐름 | 논문 전체 정독보다 개념·절차 선별. 대규모 알고리즘 구현은 심화 |
| S26 | [A Comprehensive Survey on Automatic Knowledge Graph Construction](https://arxiv.org/abs/2302.05019) | Zhong et al., 저자 공개본 2023; [ACM 출판본](https://doi.org/10.1145/3618295) | 획득·정제·변화, 개체·관계 추출과 통합 과제 | 공개본과 출판본 판본을 구분. 교재 세부는 실제 사용할 본문 확인 |
| S27 | [R2RML: RDB to RDF Mapping Language](https://www.w3.org/TR/r2rml/) | W3C Recommendation, 2012 | Introduction·Overview, 관계형 데이터 매핑, 가상 접근·RDF 생성 대안 | 전체 문법 정독은 제외. 모든 기업 시스템에 채택해야 하는 기술로 제시하지 않음 |
| S28 | [SKOS Primer](https://www.w3.org/TR/skos-primer/) | W3C Working Group Note, 2009 | 기본 concept scheme·label·semantic relation 예제 | 입문 안내. 규범 정의는 S29로 확인 |
| S29 | [SKOS Reference](https://www.w3.org/TR/skos-reference/) | W3C Recommendation, 2009 | 어휘·개념·라벨·관계의 의미 대조 | 단순 어휘 관리와 OWL 공리 모델을 같은 것으로 설명하지 않음 |
| S30 | [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) | W3C Working Group Note, 2016 | Introduction·품질 측정·차원·정책 | Recommendation이 아님. 품질의 완전한 정의나 보편 합격 기준을 제공한다고 해석하지 않음 |
| S31 | [Data on the Web Best Practices](https://www.w3.org/TR/dwbp/) | W3C Recommendation, 2017 | 메타데이터·출처·품질·버전·식별자 관련 권고 | 기업 내부 운영에 적용한 구체 설계는 교재의 응용으로 표시 |
| S32 | [Space Shuttle Guidance, Navigation, and Rendezvous Knowledge Capture Reports](https://ntrs.nasa.gov/citations/20110023477) | John L. Goodman, NASA NTRS 기술 보고서, 2011, JSC-66136 Revision 1 | 지식 포착 접근, PDF 파일 33·36·37쪽 본문 확인 | 인터뷰·맥락·1차 기록의 결합을 참고. 반도체 업무 표준이 아님 |
| S33 | [NASA Lessons Learned](https://www.nasa.gov/nasa-lessons-learned/) | NASA 공식 운영 사례 설명, 변경 가능 | 사건·교훈·권고의 기록과 재사용 관점 | 타 산업의 지식 관리 사례. 암묵지를 모두 문서화할 수 있다는 증거로 쓰지 않음 |
| S34 | [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/) | W3C Recommendation, 2013 | §2 기본 패턴 질의 | 작은 예제의 데이터 범위와 결과를 함께 표시 |
| S35 | [Cypher MERGE](https://neo4j.com/docs/cypher-manual/current/clauses/merge/) | Neo4j 공식 current 문서 | 패턴 매칭·생성·동시성 주의 | 문법 참고이며 서버 실행 결과가 아님 |
| S36 | [GraphRAG Local Search](https://microsoft.github.io/graphrag/query/local_search/) | Microsoft GraphRAG 공식 문서 | Entity-based Reasoning·Methodology | 원문·그래프 정보를 결합하는 구체 모드 |
| S37 | [GraphRAG Global Search](https://microsoft.github.io/graphrag/query/global_search/) | Microsoft GraphRAG 공식 문서 | Whole Dataset Reasoning·Methodology | 커뮤니티 보고서 활용. 이 사례의 성능을 입증하지 않음 |
| S38 | [HNSW](https://arxiv.org/abs/1603.09320) | Malkov & Yashunin, 공개본 v4, 2018 | 초록의 근접 이웃 검색용 그래프 구조 | 업무 관계를 표현하는 KG와 구분하는 데 사용 |
| S39 | [Evaluation in information retrieval](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-in-information-retrieval-1.html) | S03의 평가 장 직접 링크 | Precision·recall·F1 | 교재의 수치는 합성 산술 예시이며 검색 실측치가 아님 |

## 교재와 연결되는 선별 읽기

아래는 읽을 범위를 지정하는 지침이다. 실제 교재에 사용한 절·예제는 [출처 확인 기록](learning/EVIDENCE.md)에서 확인한다. 문서 전체를 순서대로 읽게 하지 않는다.

| 단원 | 사용자가 대조할 핵심 부분 | 교재 제작자가 추가 확인할 부분 |
|---|---|---|
| M1 | S24 제조 기본 흐름, S06 역량 질문 | S01 개인 지식 관리, S02 제품 사용례, S05 기업 KG |
| M2 | S07 triple, S11 작은 추론 예제, S14 그래프 모델 | S08~S10 질의·의미의 세부, S28~S29 통제 어휘 대안 |
| M3 | S27 매핑 개요, S32~S33에서 선정한 지식 포착 사례 | S26 획득 분류, 문서 파싱·표 처리의 선택 도구 공식 문서 |
| M4 | S25 개체 식별 흐름, S18 How it works | S17 과제·평가, S26 통합·정제, 사용할 제품 버전 |
| M5 | S12 검증 예제, S30 품질의 목적 적합성 | S11 추론과 검증의 차이, S03 평가 원리, 검토 방법의 추가 근거 |
| M6 | S13 출처·파생 예제, S31 버전·출처 관련 권고 | S27 가상 접근, 선택 구현체의 갱신·권한 공식 문서 |
| M7 | S21 local/global, S22~S23에서 선정한 RAPTOR 구성·검색 그림 | S04·S19 원논문 실험 조건, S16·S20 현재 구현과 차이 |
| M8 | 앞 단원의 근거 카드 재사용 | 설계 선택의 논리, 반례, 사례의 일관성 대조 |

교재에서 추가로 필요한 반도체 용어, 파싱 도구 동작, 검토 전략의 효과, 권한 구현은 해당 내용을 실제로 기술하기 전에 근거를 보강한다. 아직 선정하지 않은 자료나 실행하지 않은 결과를 확인된 것으로 표시하지 않는다.

## 후속 자료를 추가하는 기준

1. 실제 단원의 질문에 답하는 자료만 추가한다. 참고문헌 개수 자체를 목표로 삼지 않는다.
2. 표준은 해당 규격의 원문, 알고리즘은 원논문·저자 구현, 제품은 공식 문서·코드를 우선한다.
3. 공식 제품 소개는 기능·사용례 확인에 활용하고 성능·정확성·비용은 별도 검증한다.
4. 논문 결과는 데이터·모델·기준선·평가 방법·통계·실패 조건을 기록한다.
5. 공개 구현은 라이선스, 릴리스·커밋, 의존성, 재현 가능성을 확인한다.
6. Entity resolution·출처·검증·갱신 등은 개정 계획의 핵심 개념으로 포함한다. 알고리즘 상세, 제품 운영, 대규모 실험은 필요에 따라 선택 심화 자료를 추가한다.

## 인용 작성 예시

> [논문 결과] 저자들은 특정 데이터와 모델 설정에서 개선을 보고했다. 이 결과를 다른 조직 데이터의 성능 보장으로 일반화하지 않는다. — 저자, 연도, 논문 제목, 표 번호, URL.

> [자체 실험] 고정한 평가셋에서 구성 A의 근거 누락이 구성 B보다 적었다. — 실험 ID, 데이터 해시, 코드 커밋, 모델·설정, 반복 횟수, 측정값.

> [설계 제안] 권한 변경 시 원문에서 파생한 요약과 캐시의 접근 정책도 검증하도록 설계한다. — 제안의 이유, 대응하는 위협 시나리오, 구현 후 확인할 검증 방법.
