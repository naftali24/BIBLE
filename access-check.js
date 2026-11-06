/* Bible Project — Naftali Davidovitz & AI. Client-side deterrent, not a security boundary. */
(function(){
  'use strict';
  const originOK=location.hostname==='naftali24.github.io' && location.pathname.startsWith('/BIBLE/');
  // A single short-lived entry permit is consumed by the first app opened.
  let allowed=false;
  try {
    const value=sessionStorage.getItem('naftali_bible_index_entry');
    const timestamp=Number(value);
    allowed=Number.isFinite(timestamp) && timestamp>0 && Date.now()-timestamp<2*60*1000;
    sessionStorage.removeItem('naftali_bible_index_entry');
  } catch (_) {}
  if(!originOK || !allowed){
    location.replace('https://naftali24.github.io/BIBLE/');
    return;
  }
  document.addEventListener('DOMContentLoaded',function(){
    if(!document.body || document.getElementById('naftali-project-credit'))return;
    const credit=document.createElement('div');
    credit.id='naftali-project-credit';
    credit.textContent='© 2026 Naftali Davidovitz & AI';
    credit.setAttribute('aria-label','Bible Project by Naftali Davidovitz and AI');
    Object.assign(credit.style,{position:'fixed',bottom:'2px',left:'5px',zIndex:'100',font:'10px Arial,sans-serif',color:'#f3d28d',textShadow:'0 1px 3px #000',opacity:'.7',pointerEvents:'none',maxWidth:'60vw',whiteSpace:'nowrap'});
    document.body.appendChild(credit);
  });
})();
