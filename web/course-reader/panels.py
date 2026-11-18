"""Evidence-driven side examples; no live model or database calls."""
from html import escape
import json

def selector(title,description,choices,data,kind):
    options=''.join('<option value="'+escape(k,quote=True)+'">'+escape(v)+'</option>' for k,v in choices)
    return '<section class="trace evidence-demo" data-demo="'+kind+'"><h2>'+title+'</h2><p>'+description+'</p><label for="evidence-choice">비교할 항목</label><select id="evidence-choice">'+options+'</select><div class="evidence-result" aria-live="polite"></div><script type="application/json" class="demo-data">'+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+'</script></section>'

def panel(lesson,course):
    key=lesson['id']
    if key=='U11-L02':
        raw=json.loads((course/'examples/construction/quality.json').read_text(encoding='utf-8'))['daily'];capacity=raw['reviewers']*raw['minutes_per_reviewer'];h=raw['high'];m=raw['medium'];low=raw['low'];base=h['count']*h['minutes']+m['count']*m['minutes']
        data={'all':{'title':'대상 전체를 사람 검토','workload':base+low['count']*low['minutes'],'capacity':capacity,'reason':'규칙 격리 뒤 216건을 모두 검토합니다. 전수 검토도 시간과 판단 기준이 필요합니다.'},'risk':{'title':'필수 검토 + 낮은 위험군 표본','workload':base+raw['audits']*low['minutes'],'capacity':capacity,'reason':'고위험 36건·중위험 24건을 검토하고 낮은 위험군 8건을 감사합니다. 표본 오류율이 0이라는 보장은 없습니다.'},'spike':{'title':'고위험 10건 추가','workload':base+raw['audits']*low['minutes']+raw['high_spike']*h['minutes'],'capacity':capacity,'reason':'기존 정책의 대상에 고위험 10건이 더 들어왔습니다. 표본만 줄여도 필수 검토가 용량을 넘습니다.'}}
        data['spike']['title']='낮은 위험군 10건을 고위험으로 재분류'
        data['spike']['reason']='전체 유입은 같고 낮은 위험군이 10건 줄었습니다. 필수 검토가 늘어나 감사 표본을 생략해도 용량을 12분 넘습니다.'
        return selector('사람 검토의 처리 용량','본문의 합성 시간 예입니다. 실제 인력 수요나 대기시간 예측이 아닙니다.',[(k,v['title']) for k,v in data.items()],data,'review-capacity')
    if key=='U14-L02':
        raw=json.loads((course/'examples/rag-graph/graph.json').read_text(encoding='utf-8'))
        data={'local':{'title':'Local · CR-119 승인 기록','entities':raw['local_context']['entities'],'reports':[(i,raw['reports'][i]['text']) for i in raw['local_context']['reports']],'sources':[(i,*raw['sources'][i]) for i in raw['local_context']['text_units']]},'global':{'title':'Global · 업무 기록 방식의 변화','entities':[],'reports':[(i,raw['reports'][i]['text']) for i in ['R-A1','R-A2','R-B1']],'points':raw['global_map_points'],'sources':[]}}
        return selector('Local과 Global이 읽는 자료','합성 사례의 중간 산출물을 비교합니다. 입력 질문과 검색 방식이 함께 달라집니다.',[(k,v['title']) for k,v in data.items()],data,'graphrag-context')
    if lesson['unit']=='U15':
        raw=json.loads((course/'examples/rag-tree/tree.json').read_text(encoding='utf-8'))
        cases={'narrow-traversal':('좁은 질문 · 층별 탐색',['R1','S2','T03'],100),'narrow-collapsed':('좁은 질문 · 전 층 통합',['T03','T02'],77),'broad-collapsed':('넓은 질문 · 전 층 통합',['R1','S1','S2'],96)}
        data={k:{'title':v[0],'selected':v[1],'length':v[2],'question':raw['questions']['narrow' if k.startswith('narrow') else 'broad'],'nodes':raw['nodes']} for k,v in cases.items()}
        return selector('계층과 최종 컨텍스트','모의 점수와 길이 단위를 사용합니다. 같은 노드가 두 가지에 나타나도 같은 ID의 자료입니다.',[(k,v[0]) for k,v in cases.items()],data,'tree-context')
    if key=='U14-L01':
        raw=json.loads((course/'examples/rag-graph/graph.json').read_text(encoding='utf-8'));data={}
        for date,change,supplier,person,ids in [('2026-04-10','CR-119','한빛정밀','김하늘',['G01','G02','G03','G04']),('2026-03-20','CR-106','세림밸브','박정우',['G01','G02','G05','G06'])]:
            data[date]={'nodes':['W-207','VL-042',change,person],'supplier':supplier,'evidence':[[e,*raw['sources'][e]] for e in ids]}
        return selector('관계 경로와 원문 근거','현장 밸브 VL-042로 범위를 정했습니다. 기준일을 바꾸면 적용 변경 건과 원문 근거도 달라집니다.',[(d,d+' 기준') for d in data],data,'graph-path')
    if key in ('U12-L02','U12-L03'):
        raw=json.loads((course/'examples/auto-ontology/inspection.json').read_text(encoding='utf-8'))
        proposals={'K02':'식각 장비를 공정 장비의 하위 클래스로 둔다.','K04':'공정 장비를 식각 장비의 하위 클래스로도 둔다.','K07':'모든 검사 항목의 판정을 정확히 하나로 제한한다.'}
        data={k:{'proposal':v,**raw['candidate_decisions'][k],'sources':[(i,raw['documents'][i]) for i in raw['candidate_decisions'][k]['evidence']]} for k,v in proposals.items()}
        return selector('후보에서 채택된 모델로','생성한 문장과 채택한 모델은 다릅니다. 근거와 적용 범위를 대조해 보세요.',[(k,k+' · '+v) for k,v in proposals.items()],data,'ontology-candidate')
    if lesson['unit']=='S01':
        data={
            'mention':{'title':'원문 언급','output':'E01, 이 장비, P7, 새 펌프 P8','reason':'문서의 글자 구간입니다. 아직 기준 개체 ID가 아닙니다.'},
            'coref':{'title':'동일 지시','output':'E01 ↔ 이 장비','reason':'같은 대상을 가리킵니다. P7과 P8은 같은 종류라도 별개의 실물입니다.'},
            'relation':{'title':'관계와 사건','output':'교체 사건 → 제거 P7 / 설치 P8 / 대상 E01','reason':'참여자 역할과 원문 위치를 보존합니다. 추출 결과를 그래프 모델에 매핑해야 합니다.'},
            'condition':{'title':'주장과 조건','output':'P7 마모 → 알람 원인 가능성 / 시험 미확인','reason':'가능성과 부정을 버리면 확정 인과로 과장됩니다. 사실 채택은 별도 판단입니다.'}
        }
        return selector('같은 문단에서 다른 작업 찾기','별첨 1의 합성 문단을 과제별로 나눕니다. 모델 실행 결과가 아닌 설명용 전개입니다.',[(k,v['title']) for k,v in data.items()],data,'survey-process')
    return None
