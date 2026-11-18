# 기업 지식 학습 웹

현재 기본 화면은 `learning-v2/` 교재를 기반으로 한 B안입니다. 설명 본문과 관련 비교 예제를 나란히 읽고 좁은 화면에서는 설명 사이에서 예제를 확인합니다. Knowledge Graph·수집/추출·동일성·검토, Auto ontology, Vector/Graph/Tree RAG와 평가를 우선 제공합니다. 자동 KG 구축 survey는 별첨입니다. 나머지 기초·운영·통합 단원은 이어 확장합니다.

## 실행과 빌드

프로젝트 루트에서 실행합니다.

```powershell
.\.venv\Scripts\python.exe web/build_v2.py
.\.venv\Scripts\python.exe -m http.server 4173 --bind 127.0.0.1 --directory web/dist
```

`http://127.0.0.1:4173`에서 읽습니다. `dist/index.html`을 직접 열어도 본문을 볼 수 있지만 브라우저 저장소의 일관된 사용에는 HTTP 주소를 권장합니다. 필요한 변환 패키지는 `requirements.txt`에 고정했습니다.

`build_v2.py`는 상위 교재와 읽기 구성 요소를 `source-materials-v2/`, `course-reader/`로 복사합니다. 독립 Sites 체크아웃에서도 이 스냅샷을 사용해 같은 출력물을 만들 수 있습니다. 원문·fixture·근거 기록은 `dist/materials/`에 함께 배포합니다. 기존 `build.py`는 이전 버전 제작용이며 기본 빌드가 아닙니다.

## 읽기 기능과 자료 보존

수업 안 목차, 본문 전체 검색, 수업 이동, 원문 보기, 메모·책갈피·학습 표시·이어서 읽기와 JSON 기록 내려받기를 제공합니다. 날짜별 관계 경로, Local/Global의 입력, 요약 계층과 선택 컨텍스트, 온톨로지 후보의 채택 근거, 사람 검토 용량을 본문과 대조할 수 있습니다. 화면은 동봉 fixture의 결과를 보여 주며 실제 LLM·Neo4j·검색 엔진을 호출하지 않습니다.

새 기록은 `knowledge-lab-v2`에 저장합니다. `knowledge-lab-v1`은 덮어쓰지 않으며 내려받기에 함께 포함됩니다. 예전 완료 표시를 새 수업의 완료로 바꾸지 않습니다. `legacy/index.html`에서 이전 교재와 기록을 열 수 있고 예전 `#/…` 주소도 이쪽으로 안내합니다. 브라우저 기록은 다른 기기로 자동 동기화되지 않습니다.

## 검증

```powershell
node --check web/dist/reader.js
$env:READER_TEST_BASE='http://127.0.0.1:4173'
$env:READER_TEST_DIST='C:/Users/namws/study_enterprise_brain/web/dist'
.\.venv\Scripts\python.exe rebuild/reader/check_reader.py
```

본문과 자료 링크, 전체 수업의 데스크톱·모바일 가로 넘침, 예제 조작, 검색, 기록 저장·복원·내려받기와 이전 기록 보존을 확인합니다. 개별 예제의 산술·질의 검증은 교재의 `examples/`에서 실행합니다. 실제 학습 효과나 상용 시스템의 성능을 측정한 검사는 아닙니다.

## 배포

기존 `.openai/hosting.json`의 Site ID와 owner-private 범위를 유지합니다. Sites source helper가 소스 commit/push와 패키징을 담당하고 정확히 그 커밋의 정적 출력물을 배포합니다. 루트 GitHub commit/push와 Sites 배포는 별도 기록합니다.
