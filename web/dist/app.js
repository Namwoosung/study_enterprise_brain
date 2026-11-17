/* Browser-local learning; no model or benchmark calls. */
(function learningApp(){
'use strict';
const C=window.COURSE, $=s=>document.querySelector(s), esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const KEY='knowledge-lab-v1';
let state={completed:[],bookmarks:[],notes:{},answers:{},last:'m1-01',font:17};
try{Object.assign(state,JSON.parse(localStorage.getItem(KEY)||'{}'))}catch{}
let route=[],currentSection=null,currentChapter=null,caseTab='documents',selectedDoc='D01';
const sections=C.chapters.flatMap(ch=>ch.sections.map(s=>({...s,chapter:ch})));
const findSection=id=>sections.find(s=>s.id===id);
const href=s=>'#/learn/'+s.chapter.id+'/'+s.id;
function save(){try{localStorage.setItem(KEY,JSON.stringify(state))}catch{toast('브라우저 저장 공간을 사용할 수 없습니다. 노트를 내려받아 보관하세요.');}}
function toast(s){$('#toast').textContent=s;$('#toast').classList.add('show');clearTimeout(toast.timer);toast.timer=setTimeout(()=>$('#toast').classList.remove('show'),2300)}
function nav(){const active=route[0]||'home';$('#sidebar').innerHTML=`
<a class="brand" href="#/home"><span class="brand-mark"><svg viewBox="0 0 30 30" aria-hidden="true"><path d="M8 7L23 15L8 23Z" fill="none" stroke="white" stroke-width="1.5"/><circle cx="8" cy="7" r="3" fill="white"/><circle cx="23" cy="15" r="3" fill="white"/><circle cx="8" cy="23" r="3" fill="white"/></svg></span>기업 지식 연구실</a>
<nav class="nav-main"><a href="#/home" class="${active==='home'?'active':''}"><span class="nav-icon">⌘</span>학습 지도</a><a href="#/case" class="${active==='case'?'active':''}"><span class="nav-icon">◇</span>사례 탐색</a><a href="#/practice" class="${active==='practice'?'active':''}"><span class="nav-icon">✓</span>설명 연습</a><a href="#/resource/glossary" class="${active==='resource'?'active':''}"><span class="nav-icon">▤</span>용어와 근거</a></nav>
<nav class="nav-main"><a href="#/deep"><span class="nav-icon">⌕</span>심화 학습</a></nav><p class="nav-label">차근차근 배우기</p><ol class="chapter-nav">${C.chapters.filter(ch=>ch.level!=='deep').map(ch=>{const done=ch.sections.every(s=>state.completed.includes(s.id));return `<li><a href="#/learn/${ch.id}" class="${currentChapter?.id===ch.id?'active':''}" ${currentChapter?.id===ch.id?'aria-current="page"':''}><span class="chapter-index ${done?'done':''}">${done?'✓':ch.number}</span><span>${ch.title}</span></a></li>`}).join('')}</ol>
<div class="sidebar-bottom"><div class="progress-label"><span>나의 학습 진행</span><span>${state.completed.length} / ${sections.length}</span></div><div class="progress-track"><div class="progress-fill" style="width:${state.completed.length/sections.length*100}%"></div></div><div class="sidebar-foot">완료 표시는 직접 남깁니다.<br>이해가 어려웠던 곳은 다시 방문하세요.</div></div>`;
}
const nodeInfo={
L02:{title:'L02 · 하나의 로트',type:'학습의 출발점',text:'코팅 RUN008과 검사 RUN002를 연결합니다. “어느 장비를 거쳤나?”를 묻는다면 검사 장비만 찾아서는 충분하지 않습니다.',refs:['RUN008','RUN002'],section:'m2-01'},
RUN008:{title:'RUN008 · 코팅 작업',type:'기록된 사건',text:'11월 3일 07:02, L02를 E03에서 작업했습니다. 사용 문서는 D04입니다. 작업별로 시점과 문서를 묶어야 다른 사건과 섞이지 않습니다.',refs:['D04'],section:'m3-02'},
RUN002:{title:'RUN002 · 검사 작업',type:'기록된 사건',text:'11월 3일 10:00, L02를 E01에서 검사했고 사용 문서로 D02를 기록했습니다. OBS002의 yes는 검토 요청이며 확정 불량 판정이 아닙니다.',refs:['D02','D06'],section:'m2-01'},
E03:{title:'E03 · NORTH 코팅장비',type:'구별되는 자산',text:'L02의 코팅 작업에 사용한 장비입니다. 검사장비 E01과 다른 작업에 참여합니다.',refs:['D04'],section:'m3-02'},
E01:{title:'E01 · NORTH 검사장비',type:'이름과 대상의 구분',text:'별칭은 검사기 1호, 일련번호는 SN101입니다. SOUTH의 E02도 같은 별칭을 쓰지만 다른 자산입니다. 센서 E05는 부품이지 별칭이 아닙니다.',refs:['D05'],section:'m4-02'},
D02:{title:'D02 · 개정 절차',type:'유효 시각과 수집 시각',text:'11월 3일 00:00에 발효했지만 서비스에 본문을 수집한 것은 11월 4일 08:00입니다. 당시 유효한 문서와 당시 서비스가 읽을 수 있던 문서를 구분합니다.',refs:['D02','D11'],section:'m6-01'},
I01:{title:'I01 · 원인 미확정',type:'아직 말할 수 없는 것',text:'검토 요청을 기록한 이슈입니다. 장비를 사용했다는 경로, 점검 이력, 담당자의 가설만으로 원인을 확정할 수 없습니다.',refs:['D06','D08'],section:'m5-03'}
};
function graph(selected=''){
const nodes=[['L02',90,155,110,62,'major','로트'],['RUN008',245,60,126,58,'','코팅 작업'],['RUN002',245,223,126,58,'','검사 작업'],['E03',426,42,91,50,'','장비'],['E01',426,165,91,50,'','장비'],['D02',426,255,91,50,'','절차'],['I01',245,337,126,50,'','원인 미확정']];
return `<svg class="graph-svg" viewBox="0 0 550 425" role="group" aria-label="L02의 작업과 근거 관계 지도. 노드를 선택하면 설명을 볼 수 있습니다."><path class="graph-edge" d="M145 155C172 90 182 88 245 89M145 217C175 252 190 252 245 252M371 89L426 67M371 252C400 252 396 190 426 190M371 252C397 252 400 280 426 280"/><path class="graph-edge dashed" d="M308 281L308 337"/><text x="184" y="117" fill="#7a8eac" font-size="10">작업 이력</text><text x="319" y="314" fill="#7a8eac" font-size="10">검토 요청</text>${nodes.map(([id,x,y,w,h,cl,label])=>`<g class="graph-node ${cl} ${selected===id?'selected':''}" data-node="${id}" role="button" tabindex="0" aria-label="${id} ${label} 설명"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10"/><text x="${x+w/2}" y="${y+23}" font-weight="700">${id}</text><text class="node-small" x="${x+w/2}" y="${y+41}">${label}</text></g>`).join('')}</svg>`;
}
function deepPage(){
$('#breadcrumb').textContent='심화 학습 / 내부 원리와 설계 판단';
const deep=C.chapters.filter(ch=>ch.level==='deep');
$('#main').innerHTML=`<div class="content-wrap"><div class="home-heading"><div><h1>한 단계 아래로 내려가기</h1><p>정의 다음에 남는 질문을, 반례와 계산으로 풀어봅니다.</p></div><a class="secondary" href="#/resource/deep-research">조사 근거</a></div><div class="study-tip" style="margin:0 0 30px">기본 경로를 유지한 채 필요한 주제부터 확장합니다. <strong>작동 원리 → 작은 반례 → 설계 선택 → 확인 문제</strong> 순서로 읽으세요.</div><div class="roadmap">${deep.map(ch=>`<a class="course-row" href="#/learn/${ch.id}"><span class="course-num">${ch.number}</span><div><h3>${ch.title}</h3><p>${ch.description}</p><div class="tags">${ch.tags.map(t=>`<span class="tag">${t}</span>`).join('')}</div><p class="subtle" style="margin-top:12px">먼저 읽기: ${(ch.prerequisites||[]).map(id=>C.chapters.find(c=>c.id===id)?.title||id).join(', ')}</p></div></a>`).join('')}</div></div>`;
}
function home(){
const last=findSection(state.last)||sections[0],started=state.completed.length>0||state.last!=='m1-01';
$('#breadcrumb').textContent='학습 지도';
$('#main').innerHTML=`<div class="content-wrap"><div class="home-heading"><div><h1>연결하고, 검증하고, 설명하기</h1><p>반도체 사례로 배우는 기업 지식의 구성 원리</p></div><span class="date-label">개발자를 위한 4–5일 학습</span></div>
<section class="hero"><div class="hero-copy"><h2>흩어진 기록은<br>어떻게 지식이 될까?</h2><p>작업 기록 한 줄에서 시작해<br>대상과 관계를 연결하고, 근거를 확인하며,<br>신뢰할 수 있는 답변까지 따라갑니다.</p><a class="primary" href="${started?href(last):'#/learn/m1/m1-01'}">${started?'이어서 학습하기':'첫 질문부터 시작하기'}<span aria-hidden="true">↗</span></a><span class="hero-note">${started?esc(last.chapter.title)+' · '+esc(last.title):'RAG 기본 지식이 있다면 바로 시작할 수 있어요.'}</span></div><div class="hero-graph">${graph()}<div class="graph-caption"><span><i class="dot"></i>노드를 눌러 관계를 살펴보세요</span><span>교육용 합성 사례</span></div></div></section>
<div class="section-heading"><div><h2>여덟 질문으로 이어지는 학습</h2><p>앞에서 배운 구분이 다음 단계의 판단 기준이 됩니다.</p></div><a href="#/resource/plan">학습 계획 보기</a></div>
<div class="roadmap">${C.chapters.filter(ch=>ch.level!=='deep').map(ch=>{const done=ch.sections.filter(s=>state.completed.includes(s.id)).length;return `<a class="course-row" href="#/learn/${ch.id}"><span class="course-num">${String(ch.number).padStart(2,'0')}</span><div><h3>${ch.title}</h3><p>${ch.description}</p><div class="tags">${ch.tags.map(t=>`<span class="tag">${t}</span>`).join('')}</div>${done?`<span class="row-status">${done}/${ch.sections.length} 완료</span>`:''}</div></a>`}).join('')}</div>
<div class="study-tip"><strong>읽은 뒤, 한 번 설명해 보세요.</strong><br>“무엇을 알게 되었나”, “어떤 조건에서 틀릴 수 있나”, “무슨 근거로 말할 수 있나”를 짧게 남깁니다. 정의를 아는 것에서 판단하고 설명하는 단계로 나아가는 연습입니다.</div></div>`;
}
const labs={'m2-05':'inference','m4-02':'identity','m5-02':'validation','m5-05':'queue','m6-01':'time','m7-05':'retrieval'};
function labShell(title,desc,body){return `<section class="lab" aria-label="${title}"><div class="lab-head"><h3>${title}</h3><p>${desc}</p></div><div class="lab-body">${body}</div></section>`}
function labHTML(type){
if(type==='inference')return labShell('직접 비교 · 추론과 검증','같은 입력에 대해 두 시스템이 서로 다른 질문을 합니다.',`<p>Something usedEquipment E01이 기록되어 있습니다.<br>Something에 Run 타입을 직접 적지 않았다면?</p><div class="lab-controls"><button class="choice active" data-infer="rdfs" aria-pressed="true">RDFS domain 해석</button><button class="choice" data-infer="shape" aria-pressed="false">명시적 타입 검사</button></div><div id="infer-result" class="lab-result good">usedEquipment의 domain이 Run이면, Something이 Run이라는 타입을 <strong>추론</strong>합니다. 입력 거절 규칙으로 읽지 않습니다.</div>`);
if(type==='identity')return labShell('판단 연습 · 같은 이름, 다른 대상','이름만 보지 말고 사이트·일련번호·구성 관계를 함께 확인하세요.',`<p><strong>SOUTH의 검사기 1호</strong>라는 표현을 발견했습니다. 어디에 연결할까요?</p><div class="lab-controls"><button class="choice" data-identity="E01">E01 · NORTH / SN101</button><button class="choice" data-identity="E02">E02 · SOUTH / SN202</button><button class="choice" data-identity="E05">E05 · E01 센서</button></div><div id="identity-result" class="lab-result" role="status">후보를 선택하고 판단 근거를 확인하세요.</div><p class="result-note">별칭과 사이트 정보의 근거: <a href="#/case/D05">D05 원문</a></p>`);
if(type==='validation')return labShell('검증 실험 · 통과했는데 왜 틀릴까?','교재의 작은 shape와 별도 시점 검사를 규칙으로 재현합니다. 실제 SHACL 엔진은 개발자 예제에서 실행했습니다.',`<p>RUN002는 <strong>11월 3일 10:00, E01</strong>의 작업입니다. 사용 문서를 바꿔 보세요.</p><label class="control-label" for="document-select">RUN002에 연결할 문서</label><select id="document-select"><option value="D02">D02 · 개정 절차</option><option value="D01">D01 · 이전 절차</option><option value="none">문서 누락</option></select><div id="validation-result" aria-live="polite"></div>`);
if(type==='queue')return labShell('검토 용량 · 어디서 병목이 생길까?','고정 평균을 가정한 합성 계산입니다. 실제 대기 시간 예측이 아닙니다.',`<div class="range-heading"><label for="review-rate">하루 1,000개 중 검토할 비율</label><output id="rate-label">10%</output></div><input id="review-rate" type="range" min="1" max="50" value="10"><div class="range-heading"><label for="review-time">항목 하나를 검토하는 시간</label><output id="time-label">3분</output></div><input id="review-time" type="range" min="1" max="10" value="3"><div id="queue-result" aria-live="polite"></div><p class="result-note">검토 비율을 낮추는 것만이 답은 아닙니다. 중복 제거·원문 대조 화면·반복 오류 수정도 함께 검토합니다.</p>`);
if(type==='time')return labShell('시간 비교 · 유효한 문서와 알고 있던 문서','사건의 시점과 서비스가 본문을 확보한 시점을 따로 움직여 봅니다.',`<div class="timeline"><div class="time-point on">11월 2일<strong>D02 배포</strong></div><div class="time-point on">11월 3일 00:00<strong>D02 발효</strong></div><div class="time-point">11월 4일 08:00<strong>서비스 수집</strong></div></div><label class="control-label" for="event-time">조회할 작업</label><select id="event-time"><option value="RUN002">RUN002 · 11월 3일 10:00</option><option value="RUN001">RUN001 · 11월 2일 09:00</option></select><label class="control-label" for="known-time">서비스의 정보 상태</label><select id="known-time"><option value="before">11월 3일 12:00 · D02 본문 수집 전</option><option value="after">11월 4일 12:00 · D02 본문 수집 후</option></select><div id="time-result" aria-live="polite"></div><p class="result-note">D01에서 대체 문서의 ID를 안다고 D02 본문까지 읽은 것은 아닙니다. <a href="#/case/D11">D11 근거 보기</a></p>`);
if(type==='retrieval')return labShell('검색 방식 비교 · 어떤 근거를 가져올까?','검색을 실제 실행한 결과가 아닌, 이 사례의 가능한 처리 흐름을 비교합니다.',`<label class="control-label" for="retrieval-question">답하려는 질문</label><select id="retrieval-question"><option value="local">L02는 어떤 장비를 거쳤나?</option><option value="global">자료에 나타난 기록 문제는?</option><option value="cause">I01의 원인은 무엇인가?</option></select><div class="lab-controls"><button class="choice active" data-mode="vector" aria-pressed="true">Vector</button><button class="choice" data-mode="graph" aria-pressed="false">Graph</button><button class="choice" data-mode="tree" aria-pressed="false">Tree</button></div><div id="retrieval-result" aria-live="polite"></div>`);
return '';
}
function lesson(){
let ch=C.chapters.find(c=>c.id===route[1])||C.chapters[0];
let s=route[2]?ch.sections.find(s=>s.id===route[2]):ch.sections.find(s=>!state.completed.includes(s.id))||ch.sections[0];
if(!s){notFound();return}
currentChapter=ch;currentSection=s;state.last=s.id;save();
const sequence=sections.filter(x=>x.chapter.level===ch.level),idx=sequence.findIndex(x=>x.id===s.id),prev=sequence[idx-1],next=sequence[idx+1],done=state.completed.includes(s.id),bookmarked=state.bookmarks.includes(s.id);
$('#breadcrumb').textContent=ch.phase+' / '+(ch.sections.indexOf(s)+1)+'번째 질문';
$('#main').innerHTML=`<div class="lesson-layout"><div class="lesson-main"><div class="lesson-phase">${String(ch.number).padStart(2,'0')} ${ch.level==='deep'?'심화 · ':''}${ch.title}</div><h1 class="lesson-title">${s.title}</h1><p class="goal">${ch.goal}</p><div class="lesson-toolbar"><span>${ch.sections.indexOf(s)+1} / ${ch.sections.length} 구간 · ${Math.max(2,Math.round(s.text.length/450))}분 읽기</span><div class="toolbar-actions"><div class="reader-size"><button class="small-button" id="font-down" aria-label="본문 글자 줄이기">가−</button><button class="small-button" id="font-up" aria-label="본문 글자 키우기">가＋</button></div><button class="small-button" id="bookmark" aria-pressed="${bookmarked}">${bookmarked?'책갈피 저장됨':'책갈피'}</button><a class="small-button" href="materials/learning/${ch.file}" download>원문</a></div></div>
${labs[s.id]?labHTML(labs[s.id]):''}<article class="article">${s===ch.sections[0]?ch.intro_html||'':''}${s.html}</article>
<div class="lesson-footer">${prev?`<a class="secondary" href="${href(prev)}">이전 구간</a>`:'<a class="secondary" href="#/home">학습 지도</a>'}<button class="primary" id="complete-next">${done?(next?'다음 구간으로':'설명 연습으로'):(next?'이해했어요 · 다음 구간':'이해했어요 · 설명 연습')}</button><button class="small-button" id="toggle-done">${done?'완료 표시 취소':'이 구간만 완료 표시'}</button></div></div>
<aside class="lesson-rail"><div class="outline-block"><p class="rail-heading">이번 단원의 흐름</p><ol class="section-nav">${ch.sections.map(x=>`<li><a href="#/learn/${ch.id}/${x.id}" class="${x.id===s.id?'active':''}" ${x.id===s.id?'aria-current="step"':''}>${state.completed.includes(x.id)?'<span class="checked">✓</span>':''}${x.title}</a></li>`).join('')}</ol></div><div><label class="rail-heading" for="section-note">내 말로 정리하기</label><textarea class="note-area" id="section-note" placeholder="무엇을 알았나요? 어떤 조건에서 틀릴 수 있나요?">${esc(state.notes[s.id]||'')}</textarea><p class="note-caption" id="note-status">입력한 내용은 이 브라우저에 저장됩니다.</p><a class="small-button" href="#/case">공통 사례 살펴보기</a></div></aside></div>`;
initLab();
$('#section-note').addEventListener('input',e=>{state.notes[s.id]=e.target.value;save();$('#note-status').textContent='저장됨 · 이 브라우저에서 이어 쓸 수 있어요.'});
$('#bookmark').onclick=()=>{state.bookmarks=bookmarked?state.bookmarks.filter(id=>id!==s.id):[...state.bookmarks,s.id];save();lesson();toast(bookmarked?'책갈피를 해제했습니다.':'책갈피에 저장했습니다.')};
$('#font-down').onclick=()=>setFont(-1);$('#font-up').onclick=()=>setFont(1);
$('#complete-next').onclick=()=>{if(!state.completed.includes(s.id))state.completed.push(s.id);save();location.hash=next?href(next):'#/practice'};
$('#toggle-done').onclick=()=>{state.completed=done?state.completed.filter(id=>id!==s.id):[...state.completed,s.id];save();lesson();nav()};
}
function setFont(delta){state.font=Math.min(22,Math.max(14,state.font+delta));document.documentElement.style.setProperty('--body-size',state.font+'px');save()}
function initLab(){
if($('#document-select')){$('#document-select').onchange=validateDemo;validateDemo()}
if($('#review-rate')){$('#review-rate').oninput=queueDemo;$('#review-time').oninput=queueDemo;queueDemo()}
if($('#event-time')){$('#event-time').onchange=timeDemo;$('#known-time').onchange=timeDemo;timeDemo()}
if($('#retrieval-question')){$('#retrieval-question').onchange=retrievalDemo;retrievalDemo()}
}
function validateDemo(){
const d=$('#document-select').value,exists=d!=='none',valid=d==='D02';
$('#validation-result').innerHTML=`<div class="status-list"><div class="status-line"><span>구조 · Document가 하나 있는가?</span><span class="${exists?'pass':'fail'}">${exists?'통과':'실패'}</span></div><div class="status-line"><span>시점 · 해당 작업에 유효한가?</span><span class="${valid?'pass':'fail'}">${valid?'통과':exists?'불일치':'판단할 문서 없음'}</span></div></div><div class="lab-result ${valid?'good':'warn'}">${valid?'D02는 구조 조건을 만족하고 RUN002 시점에 E01에 적용됩니다. 이 두 검사로 모든 현실 사실이 검증된 것은 아닙니다.':exists?'D01도 Document이므로 구조 검사는 통과합니다. 하지만 11월 3일 00:00에 유효 기간이 끝났습니다. <strong>구조 통과와 업무 적합성은 다릅니다.</strong>':'usedDocument가 없으므로 최소 개수 조건을 만족하지 않습니다. 먼저 누락된 원천 기록을 확인해야 합니다.'}</div>`;
}
function queueDemo(){
const rate=+$('#review-rate').value,time=+$('#review-time').value,count=rate*10,minutes=count*time,capacity=Math.floor(240/time),backlog=Math.max(0,count-capacity);
$('#rate-label').textContent=rate+'%';$('#time-label').textContent=time+'분';
$('#queue-result').innerHTML=`<div class="status-list"><div class="status-line"><span>하루 검토 대상</span><strong>${count}개</strong></div><div class="status-line"><span>필요 시간 / 가용 시간</span><strong>${minutes}분 / 240분</strong></div><div class="status-line"><span>하루 처리 가능 / 미처리</span><strong>${capacity}개 / ${backlog}개</strong></div></div><div class="lab-result ${backlog?'warn':'good'}">${backlog?`같은 조건이 계속되면 하루 ${backlog}개씩 미처리 항목이 쌓입니다.`:'현재 평균 가정으로는 검토 시간이 충분합니다. 오류를 충분히 발견하는지는 별도 평가해야 합니다.'}</div>`;
}
function timeDemo(){
const event=$('#event-time').value,after=$('#known-time').value==='after',old=event==='RUN001',doc=old?'D01':'D02',available=old||after;
$('.timeline .time-point:last-child').classList.toggle('on',after);
$('#time-result').innerHTML=`<div class="status-list"><div class="status-line"><span>작업 시점에 유효한 문서</span><strong>${doc}</strong></div><div class="status-line"><span>선택한 정보 상태에서 본문 제공</span><strong class="${available?'pass':'fail'}">${available?'가능':'수집 전'}</strong></div></div><div class="lab-result ${available?'good':'warn'}">${old?'나중에 D02를 수집해도 RUN001 당시의 적용 절차가 D02로 바뀌지는 않습니다. 과거 작업은 당시의 유효 구간으로 봅니다.':after?'이제 서비스는 D02 본문을 읽고 RUN002 당시의 절차를 재구성할 수 있습니다.':'D02가 유효하지만 서비스는 아직 본문을 갖고 있지 않습니다. 끝난 D01을 최신 문서처럼 대신 제공하면 안 됩니다.'}</div>`;
}
function retrievalDemo(){
const mode=$('[data-mode].active')?.dataset.mode||'vector',q=$('#retrieval-question').value;
const flow={vector:['질문 임베딩','유사 문서 + 필터','근거 원문'],graph:['대상 식별','관계·조건 조회','경로 + 원문'],tree:['질문 해석','요약·상세 계층 검색','원문 확인']}[mode];
const descriptions={
local:{vector:'L02 관련 조각을 검색합니다. RUN008과 RUN002를 모두 찾았는지 확인해야 합니다. 정확한 ID·메타데이터·SQL을 결합할 수도 있습니다.',graph:'L02에 연결된 두 작업에서 장비를 조회합니다. RUN008 → E03, RUN002 → E01이라는 경로와 원천 행을 함께 제시합니다.',tree:'상위 요약만으로는 두 작업의 정확한 장비 ID가 빠질 수 있습니다. 상세 기록까지 내려가거나 여러 수준을 함께 검색해야 합니다.'},
global:{vector:'D10·D11·D12처럼 서로 표현이 다른 자료를 빠짐없이 모아야 합니다. 유사한 상위 문서 몇 개가 전체 문제를 대표하는지 확인합니다.',graph:'예를 들어 커뮤니티 보고서를 활용하는 Microsoft Global Search 구조를 검토할 수 있습니다. 공식 설비 관계 조회와 같은 절차는 아닙니다.',tree:'식별 혼동·수집 지연·오래된 메모라는 하위 자료를 묶은 요약을 활용할 수 있습니다. 요약의 공통점은 원문으로 대조합니다.'},
cause:{vector:'원인 질문과 비슷한 D07의 가설을 찾아도 원인이 확인된 것은 아닙니다. D06·D08의 미확정 상태를 함께 읽습니다.',graph:'작업이 E01과 연결되었다고 E01이 원인이라는 관계가 생기지 않습니다. 그래프 경로의 의미를 지켜야 합니다.',tree:'요약 과정에서 “미확정”이라는 조건이 사라지면 답이 왜곡됩니다. 상위 요약에서도 불확실성을 보존해야 합니다.'}};
$('#retrieval-result').innerHTML=`<div class="mode-flow">${flow.map((f,i)=>`${i?'<i aria-hidden="true">›</i>':''}<span>${f}</span>`).join('')}</div><div class="lab-result">${descriptions[q][mode]}</div><p class="result-note">${q==='cause'?'제공된 자료의 답: 원인 미확정.':'필요한 답과 근거를 먼저 정한 뒤 구성을 비교합니다.'} 이 화면은 성능·검색 순위의 실측 결과가 아닙니다.</p>`;
}
function casePage(){
$('#breadcrumb').textContent='사례 탐색 / 원문과 연결';
selectedDoc=C.documents.some(d=>d.id===route[1])?route[1]:selectedDoc;
const selected=nodeInfo[route[1]]?route[1]:'L02';
$('#main').innerHTML=`<div class="content-wrap"><div class="home-heading"><div><h1>한 사건의 근거를 따라가기</h1><p>L02의 작업, 적용 절차, 검토 기록을 연결해 봅니다.</p></div><a class="secondary" href="#/resource/case-guide">사례 읽는 법</a></div><p class="synthetic-notice">모든 업무 기록은 교육용 합성 자료입니다. 실제 기업의 절차나 불량 원인 분석이 아닙니다.</p><div class="case-layout"><div class="case-map">${graph(selected)}<p>실선: 작업·사용 관계의 연결　점선: 검토 요청의 연결</p></div><div class="case-detail" id="case-detail"></div></div><div class="case-tabs" role="tablist" aria-label="사례 자료 유형">${[['documents','문서 14개'],['runs','작업 기록'],['equipment','장비 목록'],['observations','관측 기록'],['people','담당 역할']].map(([id,label])=>`<button role="tab" aria-selected="${caseTab===id}" class="${caseTab===id?'active':''}" data-case-tab="${id}">${label}</button>`).join('')}</div><div id="case-data"></div></div>`;
showNode(selected);showCaseData();
if(route[1]?.startsWith('D')){caseTab='documents';showCaseData();setTimeout(()=>$('#case-data')?.scrollIntoView({block:'start'}),50)}
}
function showNode(id){
const n=nodeInfo[id];if(!n||!$('#case-detail'))return;
$('.case-map')?.querySelectorAll('[data-node]').forEach(el=>el.classList.toggle('selected',el.dataset.node===id));
$('#case-detail').innerHTML=`<span class="eyebrow">${n.type}</span><h2>${n.title}</h2><p>${n.text}</p><a href="${href(findSection(n.section))}">관련 개념 학습하기 ↗</a><div class="source-chips">${n.refs.map(ref=>ref.startsWith('D')?`<a href="#/case/${ref}">${ref} 원문</a>`:`<button class="small-button" data-show-run="${ref}">${ref} 기록</button>`).join('')}</div>`;
}
function showCaseData(){
$$('[data-case-tab]').forEach(el=>{el.classList.toggle('active',el.dataset.caseTab===caseTab);el.setAttribute('aria-selected',String(el.dataset.caseTab===caseTab))});
if(caseTab==='documents'){
$('#case-data').innerHTML=`<input type="search" class="case-search" id="doc-filter" placeholder="문서 ID·제목·내용 검색" aria-label="사례 문서 검색"><div class="document-grid"><div class="doc-list" id="doc-list"></div><div class="document-view" id="document-view"></div></div>`;
renderDocList('');showDocument(selectedDoc);$('#doc-filter').oninput=e=>renderDocList(e.target.value);
}else{
const rows=C.tables[caseTab],keys=Object.keys(rows[0]);
const labels={id:'ID',lot:'로트',equipment:'장비',step:'작업',occurred_at:'발생 시각',used_document:'사용 문서',operator:'담당',label:'이름',site:'사이트',serial:'일련번호',kind:'유형',alias:'별칭',parent:'소속 자산',run:'작업 ID',metric:'지표',value:'값',unit:'단위',role:'역할',team:'팀'};
$('#case-data').innerHTML=`<div class="article"><div class="table-scroll" tabindex="0"><table><thead><tr>${keys.map(k=>`<th>${labels[k]||k}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr id="row-${r.id}">${keys.map(k=>`<td>${k==='used_document'?`<a href="#/case/${r[k]}">${r[k]}</a>`:esc(r[k])}</td>`).join('')}</tr>`).join('')}</tbody></table></div><p class="result-note">${caseTab==='observations'?'review_flag=yes는 검토 요청입니다. 불량률이나 확정 불량 판정이 아닙니다.':'CSV 원천의 값을 그대로 표시합니다. 표의 행과 문서의 주장을 함께 확인하세요.'}</p><a class="small-button" href="materials/learning/case/${caseTab}.csv" download>CSV 내려받기</a></div>`;
}
}
function renderDocList(query){
const docs=C.documents.filter(d=>JSON.stringify(d).toLowerCase().includes(query.toLowerCase()));
$('#doc-list').innerHTML=docs.length?docs.map(d=>`<button class="doc-button ${selectedDoc===d.id?'active':''}" data-doc="${d.id}"><span class="doc-id">${d.id} ${d.access==='quality'?'· 품질팀 제한':''}</span>${esc(d.title)}</button>`).join(''):'<p class="empty">일치하는 문서가 없습니다.</p>';
}
function showDocument(id){
const d=C.documents.find(x=>x.id===id)||C.documents[0];selectedDoc=d.id;
$('#document-view').innerHTML=`<h3>${d.id} · ${esc(d.title)}</h3><div class="metadata">유형: ${esc(d.kind)}<br>범위: ${d.scope.join(', ')} · 책임: ${d.owner}<br>접근: ${d.access==='quality'?'품질팀 전용 (사례 정책)':'내부'}${d.valid_from?`<br>유효: ${d.valid_from} ~ ${d.valid_to||'종료 미지정'}<br>본문 수집: ${d.known_from}`:''}</div>${Object.entries(d.paragraphs).map(([id,t])=>`<div class="para-id">${d.id}#${id}</div><p>${esc(t)}</p>`).join('')}<p class="result-note">합성 원문입니다.${d.id==='D07'?' 학습용으로 원문을 보여주며 실제 사용자 권한 제어를 구현한 화면은 아닙니다.':''}</p>`;
$$('[data-doc]').forEach(el=>el.classList.toggle('active',el.dataset.doc===d.id));
}
function $$(s){return [...document.querySelectorAll(s)]}
const resourceTabs=[['glossary','용어집'],['evidence','주장별 근거'],['sources','전체 출처'],['examples','개발자 실습'],['plan','학습 계획'],['deep-research','심화 근거']];
function resource(){
const id=route[1]||'glossary',r=C.resources[id];if(!r){notFound();return}
$('#breadcrumb').textContent='용어와 근거';
$('#main').innerHTML=`<div class="resource-page"><div class="resource-header"><h1>${esc(r.title)}</h1></div><nav class="resource-links">${resourceTabs.map(([key,label])=>`<a href="#/resource/${key}" class="${id===key?'active':''}">${label}</a>`).join('')}</nav><article class="article">${r.html}</article></div>`;
}
function practice(){
$('#breadcrumb').textContent='설명 연습 / 근거로 답하기';
$('#main').innerHTML=`<div class="content-wrap"><div class="home-heading"><div><h1>아는 것을 내 말로 설명하기</h1><p>먼저 답을 적고, 정답 근거와 비교해 보세요.</p></div><a class="secondary" href="#/learn/m8/m8-06">종합 자기 평가</a></div><div class="study-tip" style="margin:0 0 30px">답변이 길 필요는 없습니다. <strong>결론, 근거, 말할 수 없는 범위</strong>를 함께 적어 보세요. 자동 채점은 하지 않습니다.</div><div class="exercise-grid">${C.questions.map(q=>`<section class="practice-card"><div class="qno">${q.id}</div><h3>${esc(q.question)}</h3><textarea data-answer="${q.id}" aria-label="${q.id} 내 답변" placeholder="근거와 함께 설명해 보세요.">${esc(state.answers[q.id]||'')}</textarea><details><summary>답과 근거 비교하기</summary><p>${esc(q.expected)}</p><div class="source-chips">${q.evidence.map(ref=>ref.startsWith('D')?`<a href="#/case/${ref.split('#')[0]}">${ref}</a>`:`<span class="tag">${esc(ref)}</span>`).join('')}</div></details></section>`).join('')}</div></div>`;
$$('[data-answer]').forEach(el=>el.oninput=()=>{state.answers[el.dataset.answer]=el.value;save()});
}
function notFound(){$('#main').innerHTML='<div class="route-error"><h1>학습 구간을 찾지 못했어요.</h1><p>학습 지도에서 이어서 공부할 단원을 선택해 주세요.</p><a class="primary" href="#/home">학습 지도로</a></div>'}
function render(){
route=location.hash.replace(/^#\/?/,'').split('/').filter(Boolean);currentSection=null;currentChapter=null;
closeMenu();
if(route[0]==='learn')lesson();else if(route[0]==='deep')deepPage();else if(route[0]==='case')casePage();else if(route[0]==='resource')resource();else if(route[0]==='practice')practice();else home();
nav();document.title=(currentSection?currentSection.title+' — ':'')+'기업 지식 연구실';
window.scrollTo({top:0,behavior:'instant'});document.documentElement.style.setProperty('--body-size',state.font+'px');
}
function closeMenu(){$('#sidebar').classList.remove('open');$('#scrim').hidden=true;$('#menu').setAttribute('aria-expanded','false')}
function search(query){
const q=query.trim().toLowerCase();
if(!q){$('#search-results').innerHTML='<p class="empty">개념, 사례 ID, 궁금한 표현으로 찾아보세요.<br>예: 같은 장비 · SHACL · D02 · 암묵지</p>';return}
const terms=q.split(/\s+/),results=sections.filter(s=>terms.every(t=>(s.title+' '+s.text+' '+s.chapter.tags.join(' ')).toLowerCase().includes(t)));
$('#search-results').innerHTML=results.length?results.map(s=>{const plain=s.text.replace(/\s+/g,' '),at=plain.toLowerCase().indexOf(terms[0]),snippet=plain.slice(Math.max(0,at-40),Math.max(0,at-40)+150);return `<a class="search-result" href="${href(s)}" data-search-result><small>${s.chapter.title}</small><strong>${esc(s.title)}</strong><p>${esc(snippet)}…</p></a>`}).join(''):'<p class="empty">일치하는 내용이 없습니다.<br>더 짧은 용어나 다른 표현으로 찾아보세요.</p>';
}
function openSearch(){$('#search-dialog').showModal();search($('#search-input').value);$('#search-input').focus()}
function openNotes(){
const notes=Object.entries(state.notes).filter(([,v])=>v.trim()),bookmarks=state.bookmarks.map(findSection).filter(Boolean);
$('#notes-content').innerHTML=`<div class="note-actions"><button class="secondary" id="export-notes">노트 내려받기</button></div><h3>책갈피</h3>${bookmarks.length?bookmarks.map(s=>`<div class="note-item"><a href="${href(s)}" data-note-link>${esc(s.chapter.title)} / ${esc(s.title)}</a></div>`).join(''):'<p class="subtle">학습 구간에서 책갈피를 남길 수 있어요.</p>'}<h3 style="margin-top:25px">내 말로 정리한 내용</h3>${notes.length?notes.map(([id,t])=>{const s=findSection(id);return s?`<div class="note-item"><a href="${href(s)}" data-note-link>${esc(s.title)}</a><p>${esc(t)}</p></div>`:''}).join(''):'<p class="subtle">본문 옆 메모에 배운 내용을 짧게 적어 보세요.</p>'}<p class="subtle" style="margin-top:25px">이 기기의 브라우저에 저장됩니다. 다른 기기로 옮기기 전 내려받아 보관하세요.</p>`;
$('#notes-dialog').showModal();$('#export-notes').onclick=exportNotes;
}
function exportNotes(){
const text=['# 기업 지식 학습 노트','',...Object.entries(state.notes).filter(([,v])=>v.trim()).flatMap(([id,t])=>['## '+(findSection(id)?.title||id),'',t,'']),...Object.entries(state.answers).filter(([,v])=>v.trim()).flatMap(([id,t])=>['## '+id+' '+C.questions.find(q=>q.id===id)?.question,'',t,''])].join('\n');
const u=URL.createObjectURL(new Blob([text],{type:'text/markdown;charset=utf-8'})),a=document.createElement('a');a.href=u;a.download='기업-지식-학습노트.md';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);
}
$('#menu').onclick=()=>{const open=$('#sidebar').classList.toggle('open');$('#scrim').hidden=!open;$('#menu').setAttribute('aria-expanded',String(open))};
$('#scrim').onclick=closeMenu;$('#search-open').onclick=openSearch;$('#search-input').oninput=e=>search(e.target.value);$('#notes-open').onclick=openNotes;
document.addEventListener('keydown',e=>{
if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();if($('#search-dialog').open)$('#search-dialog').close();else openSearch()}
if(e.key==='Escape')closeMenu();
if((e.key==='Enter'||e.key===' ')&&e.target.matches('[data-node]')){e.preventDefault();e.target.dispatchEvent(new MouseEvent('click',{bubbles:true}))}
});
document.addEventListener('click',e=>{
const close=e.target.closest('[data-close]');if(close)$('#'+close.dataset.close).close();
if(e.target.closest('[data-search-result]'))$('#search-dialog').close();
if(e.target.closest('[data-note-link]'))$('#notes-dialog').close();
const node=e.target.closest('[data-node]');if(node){if(route[0]==='case')showNode(node.dataset.node);else location.hash='#/case/'+node.dataset.node}
const doc=e.target.closest('[data-doc]');if(doc)showDocument(doc.dataset.doc);
const tab=e.target.closest('[data-case-tab]');if(tab){caseTab=tab.dataset.caseTab;showCaseData()}
const run=e.target.closest('[data-show-run]');if(run){caseTab='runs';showCaseData();$('#row-'+run.dataset.showRun)?.scrollIntoView({block:'center'})}
const identity=e.target.closest('[data-identity]');if(identity){$$('[data-identity]').forEach(b=>{b.classList.toggle('active',b===identity);b.setAttribute('aria-pressed',String(b===identity))});const good=identity.dataset.identity==='E02';$('#identity-result').className='lab-result '+(good?'good':'warn');$('#identity-result').innerHTML=good?'맞습니다. D05는 SOUTH의 검사기 1호를 E02(SN202)로 정의합니다. 같은 별칭이어도 사이트가 다르면 다른 후보입니다.':identity.dataset.identity==='E05'?'E05는 E01의 센서 모듈입니다. 구성 관계를 동일성으로 바꾸면 안 됩니다.':'E01은 NORTH 장비입니다. 이름은 같지만 지금 표현의 사이트는 SOUTH입니다. 원문 맥락까지 비교하세요.'}
const infer=e.target.closest('[data-infer]');if(infer){$$('[data-infer]').forEach(b=>{b.classList.toggle('active',b===infer);b.setAttribute('aria-pressed',String(b===infer))});$('#infer-result').innerHTML=infer.dataset.infer==='rdfs'?'usedEquipment의 domain이 Run이면 Something이 Run이라는 타입을 <strong>추론</strong>합니다. 입력 거절 규칙으로 읽지 않습니다.':'“명시적으로 Run 타입이 기록되었는가?”라는 별도 검사라면 누락으로 판단할 수 있습니다. 어떤 데이터를 대상으로 어떤 조건을 검사하는지 정해야 합니다. 이 예시는 모든 SHACL 검사가 명시적 타입만 본다는 뜻이 아닙니다.'}
const mode=e.target.closest('[data-mode]');if(mode){$$('[data-mode]').forEach(b=>{b.classList.toggle('active',b===mode);b.setAttribute('aria-pressed',String(b===mode))});retrievalDemo()}
});
window.addEventListener('hashchange',render);render();
})();
