# 주장·출처 확인 기록

주요 출처 확인: **2026-11-17** · 교재 최종 점검: **2026-11-18**. 이 문서는 교재의 주요 주장에 대한 근거와 확인 범위를 기록한다. 전체 논문 정독, 모든 제품 설치, 모든 문장의 현실적 참을 보증하는 인증 문서는 아니다.

표준의 의미는 지정한 규격, 연구 방법은 원논문의 해당 부분, 제품은 공식 설명을 확인했다. 사례·계산·아키텍처 선택은 별도로 구분했다. 본문 인용 링크가 일차적인 근거이며, 아래 표는 이를 다시 찾는 색인이다.

## 주요 개념과 방법

| 기록 | 주장·사용 범위 | 근거와 확인 부분 | 교재 위치 |
|---|---|---|---|
| E01 | Second Brain의 CODE 설명 | [Forte Foundation](https://www.buildingasecondbrain.com/foundation), CODE 설명 | M1-02 |
| E02 | Enterprise Brain의 제품명 사용례 | [WRITER 소개](https://writer.com/blog/enterprise-brain/), 제품 소개. 보편 정의·독립 성능 근거로 사용하지 않음 | M1-02 |
| E03 | KG의 모델·식별·맥락·품질 구분 | [Hogan et al.](https://arxiv.org/abs/2003.02320), 개관과 관련 절 | M1-03 |
| E04 | 역량 질문으로 모델 범위 결정 | [Ontology Development 101](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html), Step 1 및 클래스·속성·인스턴스 설계 | M1-05, M2, M4-05 |
| E05 | RDF triple·자원·데이터셋의 의미 | [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/), §3~4 | M2-04·08 |
| E06 | 하위 클래스·domain·reification | [RDF Schema 1.1](https://www.w3.org/TR/2014/REC-rdf-schema-20140225/), §3·§5.3 | M2-05·08 |
| E07 | OWL의 열린 세계·동일성·속성 의미 | [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/), §4.7·§5.3·§6.1 | M2-05, M4-07 |
| E08 | SKOS 개념 관계와 클래스 관계 구분 | [SKOS Reference](https://www.w3.org/TR/skos-reference/), §8와 [Primer](https://www.w3.org/TR/skos-primer/) | M2-03 |
| E09 | Property Graph와 MERGE 의미 | [Neo4j 개념](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/), [MERGE](https://neo4j.com/docs/cypher-manual/current/clauses/merge/) | M2-06 |
| E10 | SPARQL 패턴 질의 | [SPARQL 1.1 Query](https://www.w3.org/TR/sparql11-query/), §2 | M2-07 |
| E11 | 관계형 자료 매핑과 가상/생성 대안 | [R2RML](https://www.w3.org/TR/r2rml/), Abstract·§2 | M3-02, M6-06 |
| E12 | KG 획득·정제·변화의 구분 | [Automatic KG Construction 서베이](https://arxiv.org/abs/2302.05019), 개요. 세부 알고리즘 성능 인용 없음 | M3-01 |
| E13 | 지식 포착에서 맥락·인터뷰·1차 기록의 역할 | [NASA Goodman 보고서 PDF](https://ntrs.nasa.gov/api/citations/20110023477/downloads/20110023477.pdf), PDF 33·36·37쪽. PDF 텍스트를 직접 확인 | M3-04 |
| E14 | 사건·교훈의 재사용 사례 | [NASA Lessons Learned](https://www.nasa.gov/nasa-lessons-learned/), 운영 소개 | M3-05 |
| E15 | Entity resolution 단계·후보 생성·통합 | [ER 서베이 v3](https://arxiv.org/html/1905.06397v3), §2~6·§8 | M4-01~04·07 |
| E16 | LLMs4OL의 개별 ontology 학습 과제 | [LLMs4OL v2](https://arxiv.org/html/2307.16648v2), §3~4 | M4-06 |
| E17 | NVIDIA Auto Ontology 고유 개념·검토 흐름 | [공식 README](https://github.com/NVIDIA/auto-ontology#how-it-works), How it works. 배포 미실행, 커밋 미고정 | M4-06 |
| E18 | SHACL 조건·대상·개수·타입 검증 | [SHACL](https://www.w3.org/TR/shacl/), §2~4 | M5-02 |
| E19 | 품질 정보와 목적 적합성 관점 | [DQV](https://www.w3.org/TR/vocab-dqv/), Introduction. Working Group Note임을 확인 | M5-01 |
| E20 | Precision·recall·F1 | [IR 교과서 평가 장](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-in-information-retrieval-1.html), 관련 절 | M5-06 |
| E21 | 출처 정보의 기본 요소 | [PROV-O](https://www.w3.org/TR/prov-o/), §3 | M6-03 |
| E22 | 버전·변경 이력 제공 관점 | [DWBP](https://www.w3.org/TR/dwbp/#dataVersioning), §8.6, BP7~8 | M6-02 |
| E23 | 외부 검색과 생성의 결합 | [RAG 원논문](https://proceedings.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html), 구성 개요. 현대 구현과 구분 | M1-01, M7-01 |
| E24 | Microsoft GraphRAG 구축 구조와 질의 모드 | [논문 v2](https://arxiv.org/html/2404.16130v2), 방법; 공식 [Local](https://microsoft.github.io/graphrag/query/local_search/)·[Global](https://microsoft.github.io/graphrag/query/global_search/), Methodology | M7-03 |
| E25 | RAPTOR의 재귀 군집·요약·검색 | [논문 v1](https://arxiv.org/html/2401.18059v1), Methods·Retrieval strategies. 실험 성능 수치 재인용 없음 | M7-04 |
| E26 | 근접 검색 그래프와 업무 관계의 구분 | [HNSW v4](https://arxiv.org/abs/1603.09320), 초록의 색인 목적 | M7-02 |
| E27 | Neo4j GraphRAG는 별도 패키지 | [공식 패키지 문서](https://neo4j.com/docs/neo4j-graphrag-python/current/index.html), 소개 | M7-03 |
| E28 | 반도체 제조·검사의 최소 배경 | [ASML 교육 자료](https://www.asml.com/en/technology/all-about-microchips/how-microchips-are-made), 제조 과정 | M1-04, 사례 안내 |

NASA 쪽수는 PDF 파일의 페이지 순서 기준이다. 독자의 뷰어가 내부 인쇄 쪽수를 표시하면 다르게 보일 수 있다.

## 표준·제품 버전의 적용 범위

예제의 기준은 RDF 1.1, RDFS 1.1, OWL 2 2판, SPARQL 1.1, SHACL 2017이다. 이것이 2026년 현재 모든 분야의 최신 규격이라는 주장은 아니다. 후속 규격의 기능은 이 교재 예제에 섞지 않았다.

제품의 current 문서와 GitHub main은 바뀔 수 있다. 제품 개념을 설명하는 데 사용했으며, 특정 릴리스의 설치·성능·완전한 재현성을 주장하지 않는다. 후속 구현 단계에서는 버전·커밋·실행 설정을 고정해야 한다.

RAPTOR·Microsoft GraphRAG는 위에 연결한 공개 판본의 방법 설명을 사용했다. 연구별 데이터·모델·평가 설정을 생략한 성능 수치를 교재의 비교 결론으로 사용하지 않았다.

## 자체 자료와 설계 제안

| 분류 | 대상 | 확인 방법과 한계 |
|---|---|---|
| 합성 원천 | D01~D14, CSV 34행, 주장 44개, 질문 18개 | 생성 코드·참조·시간 검사. 실제 기업 자료가 아님 |
| 교육 모델 | Run 노드, 주장 상태, 권한 정책 | 사례 질문을 설명하기 위한 선택. 업계 표준 모델이라고 주장하지 않음 |
| 검증 분석 틀 | 형식·구조·논리·근거·맥락·목적 | 교재의 분해. 공식 6단계 표준이 아님 |
| 검토 정책 비교 | 전수·불확실성·영향·표본·피드백 | 설계 후보. 효과를 실증했다는 주장이 아님 |
| 수학 예시 | P/R/F1, 오류 0건 표본, 검토 처리량 | 가정과 계산 검증. 실제 성능·허용 오류율 아님 |
| 조회·추론·검증 | Python 소형 예제 | [26개 실제 검사](examples/verification_results.json). 전체 OWL DL·Neo4j·RAG 실험 아님 |
| 종합 아키텍처 | A·B·C 후보, Agent 전달 예시 | 결정 조건을 논의하는 설계안. 최종 채택안이 아님 |

## 남아 있는 검증의 경계

- 실제 반도체 조직의 데이터·업무 규정·권한 정책은 제공받지 않았다.
- 합성 질문의 정답은 이 교재 원천에 한정한다. 현실 인과·수율 판단에 쓰지 않는다.
- 외부 표준과 예제의 핵심 의미는 대조했지만 실제 제품 전체의 동작을 검증하지 않았다.
- 2026-11-18에 웹 학습 페이지를 제작하고 [콘텐츠 대응표](CONTENT_MAP.md)의 54개 구간을 반영했다. 웹의 검색 비교 화면은 실제 RAG 실험이 아닌 설명용 흐름이며, 최종 발표 자료는 별도 단계다.
