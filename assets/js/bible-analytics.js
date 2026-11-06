/* Google Analytics 4 — Bible Project. No personal identifiers are sent. */
(function(){
  'use strict';
  if(location.hostname!=='naftali24.github.io'||!location.pathname.startsWith('/BIBLE/'))return;
  const measurementId='G-B3ZDM250VH';
  window.dataLayer=window.dataLayer||[];
  window.gtag=window.gtag||function(){window.dataLayer.push(arguments);};
  window.gtag('js',new Date());
  window.gtag('config',measurementId,{send_page_view:true});
  const tag=document.createElement('script');
  tag.async=true;
  tag.src='https://www.googletagmanager.com/gtag/js?id='+measurementId;
  document.head.appendChild(tag);
})();
