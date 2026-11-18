const nav=document.querySelector('#course-nav');
document.querySelector('#menu-toggle')?.addEventListener('click',event=>{const open=nav.classList.toggle('open');event.currentTarget.setAttribute('aria-expanded',String(open));});
document.querySelector('#lesson-search')?.addEventListener('input',event=>{const q=event.target.value.trim().toLocaleLowerCase();for(const link of document.querySelectorAll('.course-links a'))link.hidden=!link.textContent.toLocaleLowerCase().includes(q);});
for(const link of document.querySelectorAll('.course-links a'))if(link.pathname===location.pathname)link.setAttribute('aria-current','page');
// Place each example beside the text on desktop and at its relevant step on mobile.
const panel=document.querySelector('.reader-example');
if(panel){const original=document.createComment('desktop example position');panel.before(original);const media=matchMedia('(max-width:790px)');const headings=[...document.querySelectorAll('.lesson article > h2')];let target;
if(panel.querySelector('.comparison'))target=headings.find(h=>h.textContent.startsWith('7.'));
else if(panel.querySelector('#validation-case'))target=headings.find(h=>h.textContent.startsWith('5.'));
else if(panel.querySelector('.trace'))target=headings.find(h=>h.textContent.startsWith('생성기에'));
const place=()=>{if(media.matches&&target)target.before(panel);else original.after(panel);};media.addEventListener('change',place);place();}
const validation=document.querySelector('#validation-case');
if(validation){const messages={missing:'담당자 0명: minCount 위반. 추론도 실제 담당자의 이름을 알아내지 못합니다.',typed:'담당자 1명 + Person 타입: 지정한 shape 통과. 실제 작업자라는 사실 검증은 별도입니다.',untyped:'추론 없음: class 위반. RDFS 추론 뒤: range 규칙으로 Person이 따라와 통과합니다.'};const show=()=>document.querySelector('#validation-result').textContent=messages[validation.value];validation.addEventListener('change',show);show();}
