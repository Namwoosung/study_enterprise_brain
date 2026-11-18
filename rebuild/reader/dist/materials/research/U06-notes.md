# U06 추론과 검증 수업 근거·실행

2026-11-19. 이 수업은 U06 전체 중 RDFS와 SHACL의 차이를 깊게 설명하는 첫 부분이다.

| 근거 | 읽은 범위와 적용 |
|---|---|
| [RDFS](https://www.w3.org/TR/rdf-schema/) | §3.1~3.4, §4. domain/range/class 포함의 의미. U04 조사에서 재사용 후 수업별 대조 |
| [SHACL](https://www.w3.org/TR/shacl/) | introduction, class targets, ClassConstraintComponent, Min/MaxCount, validation report. target과 검사 값, 보고서 항목을 예에 대응 |
| [OWL2 Primer](https://www.w3.org/TR/owl2-primer/) | §3의 OWL과 database 비교, 개체 동일성·cardinality·존재 제한 설명. 열린 세계와 입력 누락의 차이 |

실행: `.venv/Scripts/python.exe learning-v2/examples/inference-validation/verify.py`.

RDFLib/OWL-RL의 RDFS closure, pySHACL에서 inference none/rdfs를 비교했다. 누락 담당자는 minCount 위반, 타입이 명시된 담당자는 통과, 타입 미명시는 추론 전 ClassConstraintComponent 위반·RDFS 추론 후 통과했다. 잘못된 매뉴얼 목적어도 range 때문에 Person이 따라오는 것을 확인했다. SHACL의 subclass-aware target 선택은 RDFS range 추론과 분리해 설명했다.

OWL 전체 일관성·동일성 추론을 실행한 것은 아니다. 존재/최대 개수 제한 설명은 규격 의미에 따른 설명이며 해당 엔진 전체 동작을 인증하지 않는다. 향후 OWL 공리별 입력/출력, 일관성, 프로파일 수업을 추가해야 한다.
