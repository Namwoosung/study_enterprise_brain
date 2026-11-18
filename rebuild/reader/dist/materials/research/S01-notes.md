# S01 survey 별첨의 판본·근거·검토

확인일: 2026-11-19. 별첨 3편은 원문을 번역하거나 모든 인용 연구를 재현한 자료가 아니다. 논문 분류와 대표 접근을 읽을 수 있게 하는 교재이며, 정비·장비·조건·수치 사례는 별도 합성 설명이다.

## 판본

- 직접 읽고 절 번호를 연결한 자료는 [arXiv v1](https://arxiv.org/html/2302.05019v1), 2023-02-10이다. §1~8의 지도와 해당 본문 구간을 확인했다. 특히 §3, §4.1~4.3, §5.1~5.2, §6, §7, §8.1~8.7을 별첨 세 편과 대조했다.
- DOI 10.1145/3618295의 Crossref API를 직접 조회해 online 2023-11-30, volume56/issue4, print2024-04-30을 확인했다. 출판사 전체 HTML은 이 실행에서 403이었다. 출판본 전체를 직접 읽었다고 표시하지 않는다. 공개본과 출판본의 절 번호를 무조건 같다고 가정하지 않는다.
- arXiv HTML의 머리말에 표시된 임시 DOI/권호 문자열을 정식 출판 정보로 재사용하지 않았다.

## 대표 방법의 보충 1차 자료

| 자료 | 실제 확인한 범위 | 사용 |
|---|---|---|
| [Lee et al. coreference](https://aclanthology.org/D17-1018.pdf) | §2 모델과 §3 평가. mention span/선행 언급과 묶음 평가 | 별첨1 coreference·별첨2 비교 |
| [Mintz et al. distant supervision](https://aclanthology.org/P09-1113.pdf) | 도입/§2~3 가정, §7.2 사람 표본 평가 | 자동 라벨의 노이즈와 평가 단위 |
| [DocRED](https://aclanthology.org/P19-1074.pdf) | §2 annotation, §3/Table4 평가 | 문서 단위 관계/근거·F1/Ign 설정 |
| [TransE](https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data.pdf) | §2 이동 벡터, §4.2/Table3 순위 평가 | 예측과 확인 사실 구분, MeanRank/Hits |
| [Prototypical Networks](https://arxiv.org/pdf/1703.05175) | §2.1~2.2 support/query와 클래스 평균 | few-shot 거리 예제. 관계 추출 성능 재현 아님 |
| [RDF Concepts](https://www.w3.org/TR/rdf11-concepts/), [OWL2 Overview](https://www.w3.org/TR/owl2-overview/) | 모델과 언어의 역할 | 저장 엔진과 표현 규격 구분 |

논문 수치의 최신 우열을 주장하지 않았다. 별첨의 2차원 벡터와 후보 순위, F1 산술은 직접 정한 교육용 값이다. 모델을 실행한 결과로 표시하지 않는다.

## 독립 검토 반영

독립 검토에서 판본 정보·본편 대응표·평가 단위·글자 수·타입과 실물 표의 혼동을 지적했다. 출판 메타데이터와 v1 기준을 명시하고, 본편 U08/U09/U10/U11/U12/U17 연결을 추가했다. 표는 모델 T20 대신 실물 E01의 부품 이력으로 맞췄고 잘못된 글자 수를 제거했다. 대표 방법 네 개의 평가 입력/출력/지표와 합성 계산을 보강했다. §2와 §6의 튜플 표기 순서 차이도 설명했다.

웹에서는 별첨을 독립된 묶음으로 표시하고, 같은 문단의 mention/coreference/relation/condition을 전환하는 도해를 제공한다. 학습자의 실제 이해를 AI 검토나 기능 검사만으로 보장했다고 주장하지 않는다.
