// npm install --prefix /tmp/atlas-check jsdom (test-only dependency)
const fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const {JSDOM,VirtualConsole}=require('jsdom');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'geographical_bible.html'),'utf8');
const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
let opened='',clipPlays=0,spoken='';
const dom=new JSDOM(html,{url:'https://example.test/BIBLE/geographical_bible.html',runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
 w.scrollTo=()=>{};w.open=u=>{opened=u;return {}};w.HTMLElement.prototype.showModal=function(){this.setAttribute('open','')};w.HTMLElement.prototype.close=function(){this.removeAttribute('open')};
 w.SpeechSynthesisUtterance=class{constructor(t){this.text=t}};w.speechSynthesis={cancel(){},speak(u){spoken=u.text}};
 w.Audio=class{constructor(u){this.src=u;this.handlers={};this.currentTime=0}addEventListener(t,f){this.handlers[t]=f}load(){this.handlers.loadedmetadata?.()}async play(){clipPlays++}pause(){}};
}});
const w=dom.window,d=w.document,$=id=>d.getElementById(id),click=id=>$(id).click();
(async()=>{
 assert.equal(d.querySelectorAll('.facts li').length,6);assert.match(d.querySelector('h2').textContent,/גן עדן/);click('next');assert.match(d.querySelector('h2').textContent,/חדקל/);click('previous');
 const events=JSON.parse(fs.readFileSync(path.join(__dirname,'events.json'),'utf8'));
 for(const language of ['he','en']){
  if(d.documentElement.lang!==language)click('lang');
  let currentBook='בראשית';click('books');$('bookGrid').children[0].click();
  for(let i=0;i<events.length;i++){
   if(events[i].book!==currentBook){click('books');$('bookGrid').children[Object.keys(JSON.parse(fs.readFileSync(path.join(__dirname,'coverage.json'),'utf8')).books.reduce((a,b)=>(a[b.book]=1,a),{})).indexOf(events[i].book)].click();currentBook=events[i].book;}
   const localPosition=events.slice(0,i).filter(e=>e.book===events[i].book).length;
   $('events').value=String(localPosition);$('events').dispatchEvent(new w.Event('change'));
   assert.equal(d.querySelector('h2').textContent,events[i].title[language]);assert.equal(d.querySelector('.quote').textContent,events[i].quote[language]);assert.equal(d.querySelectorAll('.facts li').length,6);
   for(const a of d.querySelectorAll('.facts a'))assert.match(a.href,/^https:\/\//);
   if(events[i].image.src.startsWith('https://'))assert.ok(events[i].image.rights);else assert.ok(fs.existsSync(path.join(root,events[i].image.src)));
   click('gpt');const prompt=$('gptPrompt').value;assert.ok(prompt.includes(`${events[i].chapter}:${events[i].verse}`));for(const fact of events[i].facts)assert.ok(prompt.includes(fact[language]));click('openGPT');assert.equal(new URL(opened).origin,'https://chatgpt.com');assert.equal(new URL(opened).searchParams.get('q'),prompt);d.querySelector('[data-close="gptDialog"]').click();
   d.querySelector('.audio').click();await Promise.resolve();assert.ok(clipPlays||spoken);d.querySelector('.audio').click();
  }
 }
 click('books');assert.equal($('bookGrid').children.length,39);$('bookGrid').children[2].click();assert.ok(d.querySelector('.empty'));assert.equal($('gpt').disabled,true);click('books');$('bookGrid').children[0].click();assert.equal($('previous').disabled,true);
 click('reportBtn');assert.equal(d.querySelectorAll('#reportContent tr').length,40);assert.ok($('reportContent').textContent.includes('not a completed atlas'));
 assert.ok(JSON.parse(w.localStorage.getItem('geographical-bible-state')));assert.deepEqual(errors,[]);console.log(`PASS: ${events.length*2} bilingual event renders; all facts, verses, image paths, book menu, navigation, GPT prompts/URLs, progress table, local state and audio-handler mocks.`);console.log('NOT TESTED: actual media delivery, speech voices, CSS layout, real touch gestures, Android/PWA fullscreen.');dom.window.close();
})().catch(e=>{console.error(e);dom.window.close();process.exitCode=1});
