# 웹 학습 페이지 전달 기록

완료일: 2026-11-18 (Asia/Seoul)

- 학습 주소: [개념 학습 지도](https://enterprise-knowledge-lab-namws.sheermackerel2.chatgpt.site/#/concepts)
- 공개 범위: Sites 개인 비공개 유지
- 배포 상태: succeeded
- Site ID: appgprj_6afcc73c30a081919784724ac346bf41
- 배포 ID: appgdep_6afd1cf1baec8191803bdd93ee10bb04
- 배포 버전: appgprj_6afcc73c30a081919784724ac346bf41~appgver_c78461fa319c81919c69eed090586fd5
- 배포 소스 커밋: b82005b1f351f7d434a8644d53c60d46b67e6ad7

## 구성과 검증

개념 C1~C14의 94개 신규 구간을 추가했다. 기존 M1~M8 54개와 D1~D2 12개를 유지해 총 24단원·160구간이다. 문서 14개와 원천 표, 기존 설명 연습 18문항, 각 개념 단원의 확인 질문·접힌 해설을 제공한다.

새 경로는 요청 개념 전부의 기초·배경·특징·작동 원리·심화·선택 조건을 다룬다. 발표에서 필요한 수준과 생략 가능한 구현 세부를 구분했다. 기간 제한 없이 개념→사례 적용→추가 심화로 학습한다.

개념별·역할별 찾기와 표현 비교·벡터 방향·계층 검색의 새 실습 3종을 추가했다. 기존 6종과 합쳐 9종이다. 검색·메모·책갈피·진도에 신규 구간도 포함한다.

데스크톱 1440×1000과 모바일 390×844에서 기존 기능 검사 18개 묶음(전체 160구간·링크 포함), 신규 개념 기능 검사 8개 묶음을 통과했다. 콘솔 오류는 없었다. 화면 캡처로 개념 지도와 벡터 학습 화면을 확인했다.

Turtle·SPARQL·합성 계산·교재 구성 검사 25개를 통과했다. Cypher는 읽기용 예제로 공식 문서와 대조했으며 별도 Neo4j 서버에서 실행하지 않았다. 실제 LLM·RAG 벤치마크는 수행하지 않았다.

학습 기록은 해당 브라우저에 저장하며 기기 간 동기화하지 않는다. 노트 내려받기로 보관할 수 있다.

- [개념 교재](learning/concepts/README.md)
- [개념 조사 기록](learning/concepts/RESEARCH.md)
- [웹 실행·수정 안내](web/README.md)
- [내용 대응](web/coverage.json)
- [개념 예제 검사 결과](learning/examples/concept_verification_results.json)

web 폴더는 Sites의 별도 소스 저장소로 관리한다. 루트 GitHub 저장소에는 웹 파일도 함께 기록한다. QA 결과·스크린샷은 web/qa/에 로컬 보관하며 Git·배포에는 넣지 않는다.
