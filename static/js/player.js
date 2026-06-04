(function(){
  const btn=document.getElementById("theme-toggle");
  const saved=localStorage.getItem("theme")||"dark";
  if(saved==="light")document.body.classList.add("light");
  if(btn){btn.textContent=document.body.classList.contains("light")?"🌙":"☀️";btn.addEventListener("click",()=>{document.body.classList.toggle("light");const l=document.body.classList.contains("light");localStorage.setItem("theme",l?"light":"dark");btn.textContent=l?"🌙":"☀️";});}
  const hero=document.getElementById("ovr-hero"),counter=document.getElementById("ovr-counter");
  if(!hero||!counter)return;
  const target=parseInt(hero.dataset.target,10),start=performance.now(),startVal=Math.max(0,target-30),dur=900;
  function tick(now){const p=Math.min((now-start)/dur,1),e=1-Math.pow(1-p,3);counter.textContent=Math.round(startVal+(target-startVal)*e);if(p<1)requestAnimationFrame(tick);}
  new IntersectionObserver(entries=>{if(entries[0].isIntersecting){requestAnimationFrame(tick);}},{threshold:0.3}).observe(hero);
})();
