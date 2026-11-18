# U16 RAG 평가 근거 기록

확인일 2026-11-19. [검색 평가](../units/U16/01-retrieval-evaluation.md), [답변·실험 평가](../units/U16/02-answer-quality-and-experiment.md).

| 주장 | 확인한 절과 자료 | 적용 범위 |
| --- | --- | --- |
| Precision/recall의 분모, 순위 제한, 질의별 평균 | [Introduction to Information Retrieval §8.3–8.4](https://nlp.stanford.edu/IR-book/pdf/08eval.pdf), [NIST TREC Common Evaluation Measures §§1–2](https://trec.nist.gov/pubs/trec21/appendices/measures.pdf) | 조각을 하나의 평가 단위로 고정하고 P@k 분모를 k로 명시합니다. 필요 근거가 하나도 없는 Q6의 재현율은 평균에서 제외했습니다. |
| 첫 골드 항목의 역순위와 질문 평균 | [NIST TREC, Reciprocal Rank](https://trec.nist.gov/presentations/TREC8/removed/tsld051.htm) | 첫 골드 뒤의 내용은 무시하는 지표라는 점을 다중 근거 Q2로 확인합니다. |
| 답변을 주장 단위로 분리한 뒤 컨텍스트의 지지 여부를 계산 | [Es et al., RAGAS, EACL 2024 §3 Faithfulness 및 Answer Relevance](https://aclanthology.org/2024.eacl-demo.16.pdf#page=3) | 분자·분모의 관계를 설명합니다. 제공된 근거를 토대로 한 수업의 사람 라벨을 사용했습니다. RAGAS 패키지를 실행한 결과가 아닙니다. |
| 인용이 주장 전체를 지지하는지와 개별 인용이 관련 있는지 분리 | [Gao et al., ALCE, EMNLP 2023 §3.3 및 Figure 3](https://aclanthology.org/2023.emnlp-main.398.pdf#page=4) | 본문 예는 주장별 단일 인용이라 두 분자가 같습니다. ALCE의 NLI와 여러 인용의 결합을 구현하지 않았습니다. |
| 판정 순서·장황성 편향과 대응 | [Zheng et al., MT-Bench and Chatbot Arena, arXiv v4 §§3.3–3.4](https://arxiv.org/html/2306.05685#S3.SS3) | 순서 바꾸기·기준 답 사용의 근거입니다. 특정 업무의 자동 판정 신뢰도를 보증하지 않습니다. |
| GraphRAG 논문의 평가 기준과 일반화 한계 | [Edge et al., arXiv v2 §3.3, §4.1, §5.1, §6.1](https://arxiv.org/html/2404.16130#S3.SS3) | 두 도메인의 전역 이해 질문에 대한 모델의 쌍 비교입니다. 현업 승인자 정확도나 시험 코드 조회 점수로 옮기지 않습니다. |
| RAPTOR의 비교 조건과 군집 설계 분리 실험 | [Sarthi et al., arXiv v1 §4 Controlled Baseline Comparisons, Appendix B](https://arxiv.org/html/2401.18059#S4) | 모델·검색 구조·데이터와 단일 요소 ablation의 차이를 설명합니다. 사례 점수는 합성입니다. |
| RAG-Sequence/Token과 당시 QA 평가 조건 | [Lewis et al., NeurIPS 2020 §§2–4](https://papers.neurips.cc/paper_files/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf#page=2) | 고전 RAG를 모든 현대 시스템의 동일 기준선으로 부르지 않습니다. |
| 튜닝·최종 평가 데이터 분리 | [NIST, How to TREC](https://trec.nist.gov/howto.html) | 검색용 원문과 평가 질문·라벨의 역할을 구분합니다. |

[fixture](../examples/rag-eval/evaluation.json)에 질문별 답변 가능 여부, 원문 ID, 세 방식의 합성 순위, 답변 주장과 인용을 고정했습니다. [검산](../examples/rag-eval/verify.py)에서 원문 ID가 앞 단원 기준 파일에 존재하는지, P/R/RR, 평균, 답변·인용 계산을 검사합니다. 답변 생성이나 평가 모델은 실행하지 않았습니다.
