const toc=document.getElementById('toc');
const toggle=document.getElementById('toggleToc');
const layout=document.querySelector('.layout');
function setToc(open){if(!toc)return;toc.hidden=!open;toggle.setAttribute('aria-expanded',String(open));layout.classList.toggle('toc-hidden',!open);}
if(toc){setToc(innerWidth>760);toggle.addEventListener('click',()=>setToc(toc.hidden));toc.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{if(innerWidth<=760)setToc(false);}));document.addEventListener('keydown',e=>{if(e.key==='Escape'){setToc(false);toggle.focus();}});}
const progress=document.querySelector('.progress');
if(progress){let pending=false;function updateProgress(){const height=document.documentElement.scrollHeight-innerHeight;progress.style.width=(height>0?Math.min(100,scrollY/height*100):0)+'%';pending=false;}addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(updateProgress);}},{passive:true});updateProgress();}
const directorySearch=document.getElementById('directorySearch');
if(directorySearch){directorySearch.addEventListener('input',()=>{const q=directorySearch.value.trim().toLowerCase();let count=0;document.querySelectorAll('[data-book]').forEach(a=>{a.hidden=!a.dataset.book.toLowerCase().includes(q);if(!a.hidden)count++;});document.getElementById('directoryCount').textContent=count+' / 66 卷'+(count===0?' · 未找到，请更换关键词':'');});}
