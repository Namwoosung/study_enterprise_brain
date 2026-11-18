# B안 학습 화면의 공통 컴파일러

사용자가 선택한 본문/예제 병렬 구조로 전체 교재를 변환합니다. 56수업의 본문·표·코드·해설·출처를 보존하며, 비교가 필요한 수업에 fixture 기반 예제를 추가합니다. 모바일에서는 관련 설명 사이로 예제를 옮깁니다.

[로컬 학습 시작](dist/index.html). 본문 검색, 수업 안 목차, 용어의 정의와 본 수업 연결, 메모·책갈피·학습 표시·이어 읽기·기록 내려받기를 제공합니다. 원문과 예제는 상대 주소의 materials/로 복사합니다.

프로젝트 루트에서 실행합니다.

```powershell
.\.venv\Scripts\python.exe learning-v2/sync_manifest.py
.\.venv\Scripts\python.exe rebuild/reader/build.py
```

운영 패키징은 `web/build_v2.py`를 사용합니다. 이 컴파일러와 비교 구성 요소, glossary.json, 교재를 독립 스냅샷으로 복사해 Sites 체크아웃에서도 빌드할 수 있습니다. 자세한 사용법은 [web 안내](../../web/README.md), 실제 검사는 [QA](QA.md), 콘텐츠의 확인 범위는 [최종 검토](../FINAL_ACCEPTANCE.md)에 기록합니다.
