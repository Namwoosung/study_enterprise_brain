# 개발자 실습과 실제 검증 범위

이 폴더는 교재 설명 중 작은 부분을 실행해서 확인하기 위한 예제다. 전체 Enterprise Brain이나 RAG 제품을 구현한 저장소는 아니다. 합성 자료만 사용하며 실제 반도체 시스템·LLM API에 접근하지 않는다.

## 파일 역할

| 파일 | 역할 |
|---|---|
| [build_case.py](build_case.py) | 공통 사례 CSV·JSON·읽기용 CORPUS.md 생성 |
| [model.ttl](model.ttl) | RUN001·RUN002를 중심으로 한 RDF 부분집합 |
| [shapes.ttl](shapes.ttl) | 작업의 필수 값·개수·타입 검사 |
| [query.rq](query.rq) | L02의 작업·장비·문서를 찾는 SPARQL |
| [model.cypher](model.cypher) | 같은 작은 사례를 Neo4j에 표현하는 참고 코드 |
| [verify_examples.py](verify_examples.py) | 사례 일관성·SQL·SPARQL·추론·검증·산술 확인 |
| [requirements.txt](requirements.txt) | 실행에 사용한 핵심 Python 패키지 버전 |
| [verification_results.json](verification_results.json) | 실제 실행한 검사 결과와 미실행 항목 |

전체 사례에는 작업이 12건, L02의 작업이 2건 있다. model.ttl은 검사 작업 RUN001·RUN002 두 건, model.cypher는 RUN002 한 건을 표현한다. 두 작은 예제에서 L02 결과는 RUN002 한 건이다. 전체 CSV와 예제별 데이터 범위가 다르다는 점을 잊지 않는다.

## PowerShell 실행

프로젝트 루트 C:\Users\namws\study_enterprise_brain에서 실행한다. 이미 제공된 .venv가 있으면 설치 과정을 반복할 필요 없이 마지막 명령으로 검증할 수 있다.

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r learning/examples/requirements.txt
.\.venv\Scripts\python.exe learning/examples/verify_examples.py
~~~

검증 스크립트는 SQLite 메모리 DB와 메모리 RDF 그래프를 사용한다. 결과는 verification_results.json에 기록한다. 서버·API 키가 필요 없다.

사례 데이터를 의도적으로 재생성할 때만 다음 명령을 쓴다. 생성한 CSV·JSON·CORPUS.md를 수정해 두었다면 해당 편집은 생성 원본의 값으로 덮어쓴다. 영구 수정은 build_case.py에 먼저 반영한다.

~~~powershell
.\.venv\Scripts\python.exe learning/examples/build_case.py
.\.venv\Scripts\python.exe learning/examples/verify_examples.py
~~~

## 확인한 결과

2026-11-18 최종 재실행에서 Python 3.14.6, rdflib 7.6.0, pyshacl 0.40.2, owlrl 7.6.2로 **26개 검사 통과**를 확인했다. 이 수는 의미 품질 점수가 아니라 실행된 assertion 수다.

| 검사 묶음 | 확인한 것 | 확인하지 않은 것 |
|---|---|---|
| 사례 일관성 | ID·행 수·참조·스냅샷·적용 시점·근거 위치 | 합성 기록의 현실 반도체 사실성 |
| SQL | L02의 두 사건 RUN008·RUN002 조회 | 대용량 DB 성능 |
| RDF·SPARQL | Turtle 파싱·작은 연결 질의 | 모든 RDF 엔진의 호환성 |
| RDFS·OWL RL | 하위 클래스·domain 추론, 함수적 관계의 동일성 예 | 전체 OWL DL 일관성 판정·완전성 |
| SHACL | 정상 통과, 필수 문서 누락 실패, 구조는 맞지만 틀린 D01 통과 | 모든 업무 규칙·모든 shape 기능 |
| 별도 시점 검사 | D01을 RUN002 문서로 사용하면 거부 | 현실의 모든 예외 규정 |
| 산술 | P/R/F1·표본 예시·검토량 계산 | 모델 품질·실제 조직 처리량 |

### 꼭 관찰할 결과

RUN002의 문서를 D02에서 D01로 바꾸어도 작은 SHACL shape는 통과한다. 둘 다 Document이기 때문이다. 하지만 별도의 시점 검사는 D01이 RUN002에 적용되지 않는다고 판단한다.

이는 “SHACL은 날짜를 다룰 수 없다”는 뜻이 아니다. **이 shape가 그 조건을 기술하지 않았다**는 뜻이다. 검증 범위를 추가할지, 별도 프로그램과 결합할지 설계해야 한다.

## 실행하지 않은 것

Neo4j 서버와 Cypher 코드, NVIDIA Auto Ontology 배포, Microsoft GraphRAG와 RAPTOR 파이프라인, LLM 추출·검색 성능 실험은 실행하지 않았다. 공식 문서·논문에 근거해 작동 방식을 설명했으며, 실행 결과를 만들어 넣지 않았다.

model.cypher는 공식 문법을 참고한 학습용 코드다. 직접 시험하려면 별도의 빈 학습용 DB에서 사용하고 설치한 Neo4j 버전의 문법·제약 지원을 확인한다. MERGE는 현실 개체의 동일성을 판정하지 않으며, 유일성 제약도 모든 업무 의미를 검증하지 않는다.

Python 의존성을 고정한 것은 이 예제의 재현성을 돕기 위한 것이다. 현재 최신 버전이나 운영 배포용 권장 조합이라는 주장은 아니다.
