"""Rebuild the synthetic teaching corpus. No real company data or LLM calls."""
from pathlib import Path
import csv, json
ROOT = Path(__file__).resolve().parents[1] / "case"
ROOT.mkdir(parents=True, exist_ok=True)
def csv_file(name, rows):
    with (ROOT/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def js(name, data):
    (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
equipment=[
 dict(id="E01",label="NORTH 검사장비",site="NORTH",serial="SN101",kind="InspectionTool",alias="검사기 1호",parent=""),
 dict(id="E02",label="SOUTH 검사장비",site="SOUTH",serial="SN202",kind="InspectionTool",alias="검사기 1호",parent=""),
 dict(id="E03",label="NORTH 코팅장비",site="NORTH",serial="SN303",kind="CoatingTool",alias="코터 A",parent=""),
 dict(id="E04",label="SOUTH 코팅장비",site="SOUTH",serial="SN404",kind="CoatingTool",alias="코터 B",parent=""),
 dict(id="E05",label="E01 센서 모듈",site="NORTH",serial="SN505",kind="Component",alias="검사기 1호 센서",parent="E01"),
]
people=[dict(id=f"P{i:02}",role=role,team=team) for i,(role,team) in enumerate([
 ("NORTH 장비 담당","EQUIPMENT"),("품질 검토 담당","QUALITY"),("문서 승인 담당","PROCESS"),
 ("SOUTH 장비 담당","EQUIPMENT"),("지식 데이터 담당","DATA")],1)]
runs=[]
inspections=[]
for i in range(1,7):
    south=i in (3,5)
    day=2 if i==1 else 3 if i<=4 else 4
    time=f"2026-11-{day:02}T{8+i:02}:00:00+09:00"
    doc="D03" if south else "D01" if i==1 else "D02"
    runs.append(dict(id=f"RUN{i:03}",lot=f"L{i:02}",equipment="E02" if south else "E01",
                     step="INSPECT",occurred_at=time,used_document=doc,operator="P04" if south else "P01"))
    inspections.append(dict(id=f"OBS{i:03}",run=f"RUN{i:03}",metric="review_flag",value="yes" if i==2 else "no",unit="boolean"))
for i in range(1,7):
    south=i in (3,5); day=2 if i==1 else 3 if i<=4 else 4
    runs.append(dict(id=f"RUN{i+6:03}",lot=f"L{i:02}",equipment="E04" if south else "E03",
                     step="COAT",occurred_at=f"2026-11-{day:02}T07:{i:02}:00+09:00",
                     used_document="D04",operator="P04" if south else "P01"))
    inspections.append(dict(id=f"OBS{i+6:03}",run=f"RUN{i+6:03}",metric="record_complete",value="yes",unit="boolean"))
csv_file("equipment.csv",equipment);csv_file("people.csv",people)
csv_file("runs.csv",runs);csv_file("observations.csv",inspections)
# Intervals are [valid_from, valid_to). None means no known scheduled end in this case.
documents=[
 dict(id="D01",title="NORTH 검사 절차 v1",kind="procedure",scope=["E01"],version=1,
      valid_from="2026-11-01T00:00:00+09:00",valid_to="2026-11-03T00:00:00+09:00",
      known_from="2026-11-01T08:00:00+09:00",access="internal",owner="P03",
      paragraphs={"p1":"E01 검사 작업에 적용한다. 작업자는 로트 식별자와 절차 버전을 작업 기록에 남긴다.",
                  "p2":"이 문서의 적용 종료는 2026-11-03 00:00 KST이다. D02로 대체된다."}),
 dict(id="D02",title="NORTH 검사 절차 v2",kind="procedure",scope=["E01"],version=2,
      valid_from="2026-11-03T00:00:00+09:00",valid_to=None,
      known_from="2026-11-04T08:00:00+09:00",access="internal",owner="P03",
      paragraphs={"p1":"E01 검사 작업에 적용한다. 2026-11-03 00:00 KST부터 D01을 대체한다.",
                  "p2":"로트 식별자, 절차 버전, 검사 화면에 표시된 로트 식별자의 확인 여부를 기록한다. 특정 불량 원인을 규정하는 문서는 아니다."}),
 dict(id="D03",title="SOUTH 검사 절차 v1",kind="procedure",scope=["E02"],version=1,
      valid_from="2026-11-01T00:00:00+09:00",valid_to=None,
      known_from="2026-11-01T08:00:00+09:00",access="internal",owner="P03",
      paragraphs={"p1":"E02 검사 작업에 적용한다. 장비 식별자, 로트 식별자, 절차 버전을 기록한다. NORTH E01의 D02로 대체되지 않는다."}),
 dict(id="D04",title="코팅 작업 기록 절차",kind="procedure",scope=["E03","E04"],version=1,
      valid_from="2026-11-01T00:00:00+09:00",valid_to=None,
      known_from="2026-11-01T08:00:00+09:00",access="internal",owner="P03",
      paragraphs={"p1":"E03 또는 E04의 코팅 작업에서 장비, 로트, 시각을 기록한다. 수치 공정 조건은 본 교육용 자료에 포함하지 않는다."}),
 dict(id="D05",title="장비 별칭·구성 설명",kind="manual",scope=["E01","E02","E05"],access="internal",owner="P01",
      paragraphs={"p1":"NORTH의 검사기 1호는 E01(SN101), SOUTH의 검사기 1호는 E02(SN202)다.",
                  "p2":"E05(SN505)는 E01의 센서 모듈이다. 장비 전체와 센서 모듈은 서로 다른 자산이다."}),
 dict(id="D06",title="이슈 I01 최초 기록",kind="issue",scope=["L02","RUN002"],access="internal",owner="P02",
      paragraphs={"p1":"2026-11-03 RUN002의 OBS002에서 review_flag=yes가 기록되어 I01 검토를 시작했다.",
                  "p2":"원인은 미확정이다. review_flag는 검토 요청 여부이며 웨이퍼 불량률이나 확정 불량 판정이 아니다."}),
 dict(id="D07",title="I01 검토 회의록",kind="meeting",scope=["L02","E01"],access="quality",owner="P02",
      paragraphs={"p1":"담당자는 센서 상태와 기록 화면을 확인할 필요가 있다는 가설을 제안했다.",
                  "p2":"E01이 문제의 원인이라는 결론은 내리지 않았다. 이 회의록은 품질팀 열람 자료다."}),
 dict(id="D08",title="I01 검토 상태 갱신",kind="issue_update",scope=["L02","E01"],access="internal",owner="P02",
      paragraphs={"p1":"2026-11-04 현재 I01은 추가 근거 수집 중이다. 특정 장비가 원인이라는 확정 결론은 없다."}),
 dict(id="D09",title="NORTH 담당자 경험 인터뷰",kind="interview",scope=["E01"],access="internal",owner="P01",
      paragraphs={"p1":"가끔 화면에 이전 작업 정보가 남아 보이는 상황을 본 적이 있다. 나는 작업 기록과 화면의 로트 식별자를 함께 확인한다.",
                  "p2":"발생 빈도나 원인은 측정하지 않았다. 이 발언은 경험 공유이며 공식 작업 절차를 대체하지 않는다."}),
 dict(id="D10",title="SOUTH 담당자 회고",kind="retrospective",scope=["E02"],access="internal",owner="P04",
      paragraphs={"p1":"회의에서 검사기 1호라고만 부르면 NORTH 장비와 혼동된다. 다음부터 사이트 코드도 함께 말하자는 의견이다."}),
 dict(id="D11",title="NORTH 절차 개정 공지",kind="change_notice",scope=["D01","D02"],access="internal",owner="P03",
      paragraphs={"p1":"D02는 2026-11-02 배포되고 2026-11-03 00:00 KST 발효된다. 지식 서비스에는 2026-11-04 08:00 KST에 수집되었다.",
                  "p2":"2026-11-03의 수집 완료 상태만 사용하면 D02 본문을 보지 못한다. 이는 데이터 수집 지연 사례다."}),
 dict(id="D12",title="예전 FAQ 복사본",kind="faq",scope=["E01"],access="internal",owner="P05",
      paragraphs={"p1":"검사 절차는 D01을 참고하면 된다.",
                  "p2":"이 문서는 개정 공지 이전의 비승인 참고 메모다. 최신 승인 절차 여부를 확인해야 한다."}),
 dict(id="D13",title="E01 유지보수 기록 발췌",kind="maintenance",scope=["E01","E05"],access="internal",owner="P01",
      paragraphs={"p1":"2026-11-02 18:00 KST에 E01의 E05 연결 상태를 점검했다.",
                  "p2":"이 점검 기록만으로 이후 I01의 원인을 판단할 수 없다."}),
 dict(id="D14",title="접근 정책 설명",kind="policy",scope=["D07"],access="internal",owner="P05",
      paragraphs={"p1":"D07 원문은 quality 권한을 가진 사용자에게만 제공한다. D07에서만 도출된 파생 문장도 일반 사용자에게 그대로 노출하지 않는다.",
                  "p2":"다른 공개된 근거에서 독립적으로 확인된 내용은 해당 근거와 정책으로 별도 판단한다."}),
]
js("documents.json",documents)
lines=["# 공통 사례 원문 — 합성 자료\n",
       "모든 기록·절차·인물·사건은 교육용이다. 실제 기업의 규정이나 반도체 공정 조언이 아니다. 표의 식별자는 CSV·JSON과 동일하다.\n",
       "실제 기본 개념의 근거와 사례의 정답 기준은 [사례 안내](README.md)를 참고한다.\n"]
for d in documents:
    lines += [f'<a id="{d["id"].lower()}"></a>\n',f'## {d["id"]} · {d["title"]}\n',
              f'유형: {d["kind"]} · 범위: {", ".join(d["scope"])} · 접근: {d["access"]} · 책임: {d["owner"]}\n']
    if "valid_from" in d:
        lines += [f'유효 구간: [{d["valid_from"]}, {d["valid_to"] or "종료 미지정"}) · 서비스 수집: {d["known_from"]}\n']
    for k,v in d["paragraphs"].items():lines += [f'**{d["id"]}#{k}** — {v}\n']
(ROOT/"CORPUS.md").write_text("\n".join(lines),encoding="utf-8")
claims=[]
for r in runs:
    for predicate,field in [("forLot","lot"),("usedEquipment","equipment"),("usedDocument","used_document")]:
        claims.append(dict(id=f"C{len(claims)+1:03}",subject=r["id"],predicate=predicate,
                           object=r[field],source=f"runs.csv#{r['id']}",epistemic="recorded",status="source_supported"))
extras=[
 ("E05","partOf","E01","D05#p2","recorded"),
 ("E01","locatedAt","NORTH","equipment.csv#E01","recorded"),
 ("E02","locatedAt","SOUTH","equipment.csv#E02","recorded"),
 ("I01","concerns","L02","D06#p1","recorded"),
 ("I01","hasState","unresolved","D08#p1","recorded"),
 ("D02","supersedes","D01","D02#p1","policy"),
 ("E01","needsSensorCheck","I01","D07#p1","hypothesis"),
 ("P01","reportsExperience","screen_context_check","D09#p1","experience"),
]
for a,b,c,d,e in extras:claims.append(dict(id=f"C{len(claims)+1:03}",subject=a,predicate=b,object=c,source=d,epistemic=e,status="source_supported"))
js("claims.json",claims)
questions=[
 ("Q01","RUN001에 기록된 장비는?","E01",["runs.csv#RUN001"]),
 ("Q02","RUN002에 기록된 절차는?","D02",["runs.csv#RUN002"]),
 ("Q03","RUN001 시점 E01의 유효 절차는?","D01",["runs.csv#RUN001","D01#p1","D01#p2"]),
 ("Q04","RUN002 시점 E01의 유효 절차는?","D02",["runs.csv#RUN002","D02#p1"]),
 ("Q05","E01과 E02는 같은 장비인가?","아니다. 사이트와 serial이 다르다.",["equipment.csv#E01","equipment.csv#E02","D05#p1"]),
 ("Q06","E05는 E01의 다른 이름인가?","아니다. E01의 구성 모듈이다.",["D05#p2"]),
 ("Q07","I01의 원인이 E01이라고 확정되었는가?","아니다. 원인 미확정이며 인과 결론을 내릴 수 없다.",["D06#p2","D08#p1"]),
 ("Q08","OBS002의 yes는 불량률인가?","아니다. 검토 요청 플래그다.",["observations.csv#OBS002","D06#p2"]),
 ("Q09","D02가 E02에도 적용되는가?","이 사례에서는 아니다.",["D02#p1","D03#p1"]),
 ("Q10","담당자 경험은 공식 절차인가?","아니다.",["D09#p2"]),
 ("Q11","D02는 언제 서비스에 수집되었는가?","2026-11-04T08:00:00+09:00",["D11#p1"]),
 ("Q12","2026-11-03 서비스가 D02 본문을 이미 알고 있었는가?","이 수집 모델에서는 아니다.",["D11#p2"]),
 ("Q13","일반 사용자에게 D07 고유 파생 주장을 제공해도 되는가?","이 사례 정책에서는 안 된다.",["D14#p1"]),
 ("Q14","최신 절차 질의에 D12만 사용해도 되는가?","안 된다. 승인·유효 시점을 확인한다.",["D12#p2","D02#p1"]),
 ("Q15","로트 L02와 연결되는 작업 장비는?","E03와 E01",["runs.csv#RUN008","runs.csv#RUN002"]),
 ("Q16","장비 점검이 I01의 원인을 증명하는가?","아니다.",["D13#p2"]),
 ("Q17","현재 자료로 다음 주 불량률을 계산할 수 있는가?","자료 부족. 불량률 정의·관측·예측 모델도 제공되지 않았다.",[]),
 ("Q18","핵심 기록 문제의 예시는?","장비 별칭 혼동, 절차 개정 수집 지연, 오래된 참고 메모",["D10#p1","D11#p2","D12#p2"]),
]
js("questions.json",[dict(id=a,question=b,expected=c,evidence=d) for a,b,c,d in questions])
js("manifest.json",dict(synthetic=True,timezone="Asia/Seoul",tables=4,table_rows=sum(map(len,[equipment,people,runs,inspections])),
     documents=len(documents),claims=len(claims),questions=len(questions),snapshot="2026-11-04T18:00:00+09:00"))
print(json.dumps(dict(tables=4,rows=34,documents=len(documents),claims=len(claims),questions=len(questions)),ensure_ascii=False))
