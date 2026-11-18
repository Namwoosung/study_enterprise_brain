# 다음 실행을 위한 저장소·빌드·배포 인수인계

확인 기준: 2026-11-18. 다음 실행 시작 때 git 상태·도구·사이트 상태를 다시 확인한다. 이 문서의 SHA·프로세스·라이브러리 정보는 확인 시점의 기록이며 영구 상태가 아니다.

## 1. 작업 위치와 현재 산출물

- 작업 루트: `C:/Users/namws/study_enterprise_brain`
- 셸: PowerShell. Python 가상환경: `.venv/Scripts/python.exe`.
- 루트 Git remote: `https://github.com/Namwoosung/study_enterprise_brain.git`, 현재 branch `main`.
- 이전 교재 구현의 마지막 root commit: `5fb21403697b4b95c269f505894c1583d3cad04d`.
- `web/.git`는 Sites용 별도 Git 저장소다. 루트는 web 파일을 일반 파일로 추적한다. submodule이 아니다. 별도 저장소를 제거하거나 루트에 mode 160000 gitlink로 바꾸지 않는다.
- 기존 교재: `learning/M*.md`, `learning/concepts/`, `learning/deep/`.
- 기존 원천: `learning/case/`, 실행 예제: `learning/examples/`.
- 이전 출처: `SOURCES.md`, `learning/EVIDENCE.md`, `learning/concepts/RESEARCH.md`, `learning/deep/RESEARCH.md`.
- 실제 실패 분석: `REBUILD_PLAN.md`. 새 계획의 실행 기준은 `rebuild/START_HERE.md`와 관련 2.0 명세다.
- 운행 표본: `rebuild/DRIVING_LESSON_SAMPLE.md`, `verify_sample.py`, `sample_verification.json`. 11개 검사는 RDF 구문·데이터·SPARQL·RDF/XML 동등성·SQL 산술에 관한 것이다. Neo4j 실행 또는 학습 효과 검증이 아니다.

## 2. 현재 웹 구조와 바꿔야 할 부분

현재 웹은 vanilla JS/CSS와 Python Markdown 빌드다. 서버·DB·유료 LLM 호출이 필수인 앱이 아니다.

| 경로 | 현재 역할 | 개편 시 주의 |
|---|---|---|
| web/build.py | root learning을 source-materials로 복사, M/C/D 앵커 파싱, dist 생성 | 기존 단원 수·파일 패턴·단락 형식을 새 교재 제약으로 사용하지 않음 |
| web/app.js | COURSE 렌더링, 라우트·검색·메모·실습 | 새 단원/수업 metadata 기반으로 변경, 구 기록 보존 |
| web/styles.css, index.html | 현 화면 | 선택한 디자인 기준으로 재작성 가능 |
| web/source-materials/ | 독립 Sites 저장소에 포함할 원문 snapshot | 새 교재·예제·출처를 포함하도록 입력 경로 변경 |
| web/dist/ | 실제 정적 배포 산출물 | 사용하지 않는 옛 라우트/본문이 남지 않게 빌드 범위 확인 |
| web/coverage.json | 옛 앵커-화면 대응 | 새 의미 단위의 대응으로 교체. 숫자 일치가 설명 보존 증거는 아님 |
| web/test_web.py, test_concepts.py | 기존 기능 검사 | 옛 160개 구간 등 hardcode를 새 manifest 기준으로 수정 |
| web/.openai/hosting.json | Sites ID, static.directory=dist | 동일 project_id 보존 |

새 기능을 만들기 위해 React 등 대규모 프레임워크로 바꿀 필요는 없다. 구현 복잡도와 유지 필요성을 보고 결정한다. 선택 이유를 DECISIONS에 기록한다. 내용을 충분히 담고 읽기·탐색·인터랙션이 명확히 동작하는지가 우선이다.

## 3. 새 파일 구조 제안

다음 구조를 기본으로 시작하고 실제 수업 길이·도해 요구에 맞게 조정한다. 아직 이 디렉터리/파일들이 제작되었다는 뜻은 아니다.

```text
learning-v2/
  README.md                    # 독자의 학습 시작점·경로
  manifest.json                # 단원/수업 ID, 순서, 선수 지식, 원문·도해 경로
  glossary.md                  # 짧은 정의 + 실제로 설명하는 본문 위치
  units/
    U01/ ... U18/
      01-<lesson>.md            # 자연스러운 분량의 수업
      review.md                # 단원별 최종 검토 증거
    S01/
  research/
    sources.json               # 출처 판본·확인 범위·주장 연결
    Uxx-notes.md               # 조사 중 판단과 남은 확인
  cases/
    README.md                  # 합성 사례와 실제 분야 사실의 구분
    equipment-maintenance/
    process-quality/
    parts-supplier/
  examples/
    <example-id>/              # 기준 입력·예상/실제 출력·검증 코드
  figures/
    <figure-id>.svg            # 정확한 개념 도해, 필요하면 JSON 데이터
  reviews/                     # 상세 기술/설명 검토
rebuild/
  STATE.json, WORKLOG.md, DECISIONS.md
  prototypes/                  # 실제 내용의 디자인 3안, 아직 미제작
web/
  ...                          # 선택 후 현재 웹을 개편
```

manifest에서 단원과 수업을 분리한다. 수업 ID는 안정적으로 유지하고, title/path/prerequisites/learning_outcomes/figures/examples/source_ids를 연결할 수 있게 한다. 파일 순서나 제목만으로 ID를 재생성해 메모를 깨뜨리지 않는다. 커다란 범용 CMS부터 만들지 말고 실제 첫 수업에 필요한 최소 구조를 먼저 만든다.

웹이 Markdown을 그대로 복제할 필요는 없지만 **핵심 설명·해석·예제·출처가 어디에 보존됐는지** 추적할 수 있어야 한다. 도해와 인터랙션을 별도 구성 요소로 넣고 본문을 줄이는 자동 요약기를 만들지 않는다. 정적 SVG의 텍스트·색·크기와 실제 브라우저 렌더링을 확인한다.

## 4. 로컬 확인 명령

아래는 현재 구조의 기준 명령이다. 새 빌드로 바꾸면 이 문서와 web README를 함께 갱신한다. 변경하지 않은 입력에 대해 검사를 무조건 반복하지 않는다.

```powershell
git status --short
git -C web status --short
.\.venv\Scripts\python.exe web/build.py
node --check web/app.js
.\.venv\Scripts\python.exe -m http.server 4173 --bind 127.0.0.1 --directory web/dist
```

서버 실행은 장기 명령이므로 별도 세션에서 사용한다. 이미 4173이 쓰이고 있으면 어떤 프로세스인지 확인하거나 새 포트를 사용한다. 소유 불명 프로세스를 종료하지 않는다. 서버가 살아 있다고 가정하지 않는다.

```powershell
.\.venv\Scripts\python.exe web/test_web.py
.\.venv\Scripts\python.exe web/test_concepts.py
.\.venv\Scripts\python.exe rebuild/verify_sample.py
git diff --check
```

기존 환경에 Python Markdown, RDFLib, pySHACL/owlrl, Playwright/Chromium이 설치되어 있다. 설치 여부·필요 버전을 확인한 뒤 부족할 때만 설치한다. 기존 예제의 `requirements.txt`와 출력 기록을 참고한다. 새 알고리즘 검증 때문에 관계 없는 전체 테스트를 계속 반복하지 않는다.

## 5. 사용자 기록과 구 자료 보존

기존 localStorage 키·구조를 먼저 읽고, 구 노트와 책갈피를 별도 보존하거나 내보내도록 한다. 같은 개념을 다룬다는 이유만으로 새 U단원의 완료 상태를 옛 C/M/D 완료에서 자동 생성하지 않는다. 구 링크는 이전 자료 보기 또는 새 위치 안내로 연결한다.

기존 원천 사례와 출처는 삭제보다 검증·전환을 우선한다. 사이트의 기본 학습 경로는 새 교재로 대체하고, 구 자료는 필요하면 명확히 ‘이전 버전’으로 분리한다. 기존 자료를 계속 새 본문처럼 노출하여 두 버전의 설명을 혼동시키지 않는다.

## 6. 루트와 Sites Git을 함께 다루기

시작과 commit 직전에 두 저장소의 상태를 각각 확인한다. 계획·Markdown은 루트에 저장한다. 웹 변경은 Sites helper가 별도 소스 저장소에 commit/push하며, 같은 web 파일을 루트 GitHub에도 반영한다.

주의: 중첩 `.git` 때문에 루트의 `git add web`가 새 web 파일 전체를 추가하지 못할 수 있다. 기존 추적 파일과 신규 파일의 staged diff를 반드시 확인한다. 이때 web 디렉터리를 submodule로 추가하는 해결책은 사용하지 않는다.

필요하면 Sites helper가 commit한 web 추적 파일 목록(`git -C web ls-files`)을 기준으로 루트의 일반 파일을 개별 staging한다. 일반적인 path별 `git add`로 신규 파일이 반영되지 않으면 Python `subprocess.run`의 **인자 배열**로 각 파일의 `git hash-object -w`와 `git update-index --add --cacheinfo <mode> <hash> web/<path>`를 호출할 수 있다. 파일 모드는 web index에서 확인한다. 원래 루트에 있던 web 파일 중 실제 삭제된 파일만 root index에서 제거한다. 임의 경로·공백·유니코드에 안전하게 처리하고 `.git`·토큰·qa 임시 파일은 제외한다.

루트에서 `git ls-files --stage web/index.html`이 일반 파일 mode인 것을 확인하고, `git diff --cached --stat` 및 신규 파일 목록을 검토한다. `git reset --hard`, 강제 push, web/.git 삭제는 필요하지 않다. 사용자 변경이 있으면 함께 덮어쓰지 않는다. 새 브랜치가 필요하면 `codex/` prefix를 쓴다.

## 7. 기존 사이트 유지와 배포

기존 사이트 URL:

https://enterprise-knowledge-lab-namws.sheermackerel2.chatgpt.site

기존 project_id:

`appgprj_6afcc73c30a081919784724ac346bf41`

이전 확인된 사이트 소스 commit:

`b82005b1f351f7d434a8644d53c60d46b67e6ad7`

이전 확인된 saved version:

`appgprj_6afcc73c30a081919784724ac346bf41~appgver_c78461fa319c81919c69eed090586fd5`

현재 audience는 배포 전에 `get_site`로 재확인한다. 이전에는 owner-private였으며 공개 전환은 요청되지 않았다. 새 Site를 만들지 않는다.

배포할 때 호스트 catalog의 Sites SKILL.md를 읽는다. 현재 경로는 `C:/Users/namws/.codex/plugins/cache/openai-curated-remote/sites/1.1.6/skills/sites/SKILL.md`이며 설치 버전에 따라 바뀔 수 있다. 관련 도구는 ALL_TOOLS에서 sites/get_site/create_source_repository_write_credential/save_version_and_deploy_private 등을 검색한다.

작업 시작 시 기존 Sites 소스의 최신 상태를 확인하고, helper의 opening 절차로 로컬 소스와 상태를 맞춘다. 원격 변경을 덮어쓰지 않는다. 웹 편집 뒤 검증이 끝나면 helper로 소스 동기화·commit/push·패키징한다.

```text
node C:/Users/namws/.codex/plugins/cache/openai-curated-remote/sites/1.1.6/scripts/site-workflow.mjs --project-id appgprj_6afcc73c30a081919784724ac346bf41
```

실행 cwd는 `web`, tty 세션을 사용한다. `Ready ... stdin` 이후 write_stdin으로 JSON을 보낸다. 구조는 `{credential, source, commands, archivePath}`이며 `source`는 세션에서 받은 **완전한 이전 opening 결과**, commands는 아직 안 한 검사/빌드의 인자 배열이다. opening에서는 archivePath를 생략한다. packaging에서는 절대경로 `C:/Users/namws/study_enterprise_brain/site-deployment.tar.gz`를 쓸 수 있다.

자격증명은 도구 응답에서 세션 메모리로만 다룬다. shell 인자·파일·출력·git·문서에 토큰을 남기지 않는다. `work_proxy` 같은 인증 모드이면 해당 모드의 공식 helper 절차를 따른다. 이전 세션 변수나 토큰이 남아 있다고 가정하지 않는다.

helper가 반환한 project_id/commit_sha/archive를 그대로 비공개 버전 저장·배포 도구에 전달한다. 실패 시 같은 배포 상태를 이어 확인하며 중복 Site나 버전을 무작정 만들지 않는다. 실제 페이지의 핵심 콘텐츠·라우트·도해가 의도대로 보이는지도 확인한다. 루트 GitHub push와 Sites 배포는 서로 다른 작업이며 하나로 다른 하나의 완료를 주장하지 않는다.

## 8. 최종 보고에 포함할 사실

새 본편·survey와 웹의 실제 완료 범위, 주요 개선, 실제 검증, 남은 제한, root commit/push, Sites 배포 URL/상태를 구분한다. 자동 검사나 AI 검토로 사용자의 실제 이해를 보장했다고 표현하지 않는다. 개편 전의 옛 성공 기록을 새 버전 검증으로 재사용하지 않는다.
