(function(){
  const btn=document.getElementById("theme-toggle");
  const saved=localStorage.getItem("theme")||"dark";
  if(saved==="light")document.body.classList.add("light");
  if(btn){
    btn.textContent=document.body.classList.contains("light")?"🌙":"☀️";
    btn.addEventListener("click",()=>{
      document.body.classList.toggle("light");
      const l=document.body.classList.contains("light");
      localStorage.setItem("theme",l?"light":"dark");
      btn.textContent=l?"🌙":"☀️";
    });
  }
  const grid=document.getElementById("player-grid");
  const cards=grid?Array.from(grid.querySelectorAll(".player-card")):[];
  const counter=document.getElementById("grid-count");
  document.querySelectorAll(".ftab[data-filter]").forEach(b=>{
    b.addEventListener("click",()=>{
      document.querySelectorAll(".ftab[data-filter]").forEach(x=>x.classList.remove("active"));
      b.classList.add("active");
      const f=b.dataset.filter;let v=0;
      cards.forEach(c=>{const show=f==="all"||c.dataset.badge===f;c.style.display=show?"":"none";if(show)v++;});
      if(counter)counter.textContent=`Showing ${v} players · Ranked by NBA 2K26 OVR`;
    });
  });
  const sortSel=document.getElementById("sort-select");
  if(sortSel&&grid){
    sortSel.addEventListener("change",()=>{
      const k=sortSel.value;
      [...cards].sort((a,b)=>parseFloat(b.dataset[k])-parseFloat(a.dataset[k])).forEach((c,i)=>{
        const r=c.querySelector(".card-rank");if(r)r.textContent=`#${i+1}`;grid.appendChild(c);
      });
    });
  }
  // Teams filter
  const tgrid=document.getElementById("team-grid");
  const tcards=tgrid?Array.from(tgrid.querySelectorAll(".team-card")):[];
  const tcount=document.getElementById("team-count");
  document.querySelectorAll(".ftab[data-tfilter]").forEach(b=>{
    b.addEventListener("click",()=>{
      document.querySelectorAll(".ftab[data-tfilter]").forEach(x=>x.classList.remove("active"));
      b.classList.add("active");
      const f=b.dataset.tfilter;let v=0;
      tcards.forEach(c=>{const show=f==="all"||c.dataset.tbadge===f;c.style.display=show?"":"none";if(show)v++;});
      if(tcount)tcount.textContent=`Showing ${v} teams · Ranked by NBA 2K26 OVR`;
    });
  });
  const tsort=document.getElementById("team-sort");
  if(tsort&&tgrid){
    tsort.addEventListener("change",()=>{
      const k=tsort.value;
      [...tcards].sort((a,b)=>k==="ovr"?parseFloat(b.dataset.tovr)-parseFloat(a.dataset.tovr):a.dataset.tname.localeCompare(b.dataset.tname)).forEach(c=>tgrid.appendChild(c));
    });
  }
})();
