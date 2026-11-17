# 기업 지식 연구실 — 웹 학습 페이지

기준 콘텐츠는 상위 프로젝트의 learning/ Markdown 교재다. 8개 단원을 54개의 학습 구간으로 나누고, 관계 지도·사례 원문·실습·설명 연습·근거를 연결했다.

## 사용하기

dist/index.html을 브라우저에서 직접 열어도 읽을 수 있다. 학습 기록의 안정적인 저장과 개발 중 확인에는 로컬 HTTP 서버를 권장한다.

프로젝트 루트에서 PowerShell:

~~~powershell
.\.venv\Scripts\python.exe -m http.server 4173 --bind 127.0.0.1 --directory web/dist
~~~

브라우저에서 http://127.0.0.1:4173 을 연다. 종료하려면 서버를 실행한 터미널에서 Ctrl+C를 누른다.

## 학습 기능

- 학습 지도: 여덟 질문과 이어서 읽기.
- 본문: 짧은 구간, 단원 내 목차, 글자 크기, 원문 다운로드.
- 사례 탐색: L02의 관계 지도, 문서 14개 검색, 원천 표 4개.
- 설명 연습: 정답을 먼저 보여주지 않는 질문 18개와 근거.
- 개념 실습 6종: 추론·검증, 동일성 판단, 문서 검증, 검토 용량, 시점, 검색 방식.
- 검색: 교재 전체 구간의 제목·본문·주제.
- 내 기록: 구간별 메모·책갈피·완료 표시·연습 답안, Markdown 내보내기.

기록은 브라우저 localStorage에 저장한다. 다른 기기와 동기화하지 않는다. 실제 LLM·검색 엔진·Neo4j 서버 호출은 없다. D07 권한 표시는 합성 정책을 설명하는 학습 자료이며 실제 권한 통제의 구현 데모가 아니다.

## 콘텐츠를 수정하고 빌드하기

상위 learning/이 있으면 build.py가 최신 교재를 source-materials/로 복사한다. 독립된 웹 저장소에서는 포함된 source-materials/를 사용한다. dist/materials/에 원본을 함께 배포한다.

~~~powershell
.\.venv\Scripts\python.exe -m pip install -r web/requirements.txt
.\.venv\Scripts\python.exe web/build.py
node --check web/app.js
~~~

단독 체크아웃에서는 현재 폴더에서 python build.py를 실행한다. 새 구간을 추가하면 build.py의 구간 수 검증과 학습 대응표를 함께 수정한다.

- index.html: 페이지 틀
- styles.css: 반응형 레이아웃·읽기 스타일
- app.js: 이동·검색·학습 기록·실습
- build.py: Markdown 변환·링크 변환·원천 패키징
- coverage.json: 원문 ID와 웹 구간 대응
- source-materials/: 재현 가능한 교재 스냅샷
- dist/: 바로 배포 가능한 정적 파일
- .openai/hosting.json: Sites 식별자와 정적 배포 경로

## 검증

Python Playwright와 Chromium으로 데스크톱 1440×1000, 모바일 390×844를 확인했다. test_web.py는 학습 구간 전체, 원문·링크, 실습 결과, 검색, 저장·복원, 노트 다운로드, 해설 펼치기, 모바일 메뉴와 가로 넘침을 검사한다.

~~~powershell
.\.venv\Scripts\python.exe -m pip install playwright
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe web/test_web.py
~~~

테스트 전에 4173 포트의 서버를 실행한다. 결과·스크린샷은 qa/에 저장되며 배포 소스에는 포함하지 않는다. 기능 검사 18개 묶음을 통과했고 브라우저 오류는 없었다. 접근성 전체 인증이나 모든 브라우저의 호환성을 검증했다는 의미는 아니다.

## 배포

Sites의 비공개 개인 사이트로 배포한다. 지정된 Site ID를 재사용하며 새 Site를 반복 생성하지 않는다. 소스 동기화와 배포 패키징은 Sites의 site-workflow 도구를 사용한다. 사용자 학습 메모는 배포 파일에 포함되지 않는다.
