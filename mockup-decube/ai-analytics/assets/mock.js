// Mockup bar: links between variants + "Show headings" outline (not part of the proposed design).
(function(){
  var pages=[['index.html','Overview'],['annotated.html','Current design + changes'],['variant-a.html','Variant A'],['variant-b.html','Variant B'],['variant-c.html','Variant C']];
  var here=location.pathname.split('/').pop()||'index.html';
  var bar=document.createElement('div');bar.className='mk-bar';
  bar.innerHTML='<b>Decube AI Analytics: page mockups</b>'+pages.map(function(p){return '<a href="'+p[0]+'"'+(p[0]===here?' class="on"':'')+'>'+p[1]+'</a>'}).join('')+'<span class="sp"></span><label><input type="checkbox" id="mkH"> Show headings</label>';
  document.body.insertBefore(bar,document.body.firstChild);
  var ol=document.createElement('div');ol.className='mk-outline';document.body.appendChild(ol);
  document.getElementById('mkH').addEventListener('change',function(e){
    document.body.classList.toggle('show-h',e.target.checked);
    ol.innerHTML='<div style="font-weight:700;margin-bottom:6px">Heading outline</div>'+Array.prototype.map.call((document.querySelector('main')||document).querySelectorAll('h1, h2, h3'),function(h){var l=h.tagName[1];return '<div class="l'+l+'"><b>H'+l+'</b>'+h.textContent.replace(/\s+/g,' ').trim()+'</div>'}).join('');
  });
})();
