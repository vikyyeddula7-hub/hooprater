(function(){
  const input=document.getElementById("search-input"),dropdown=document.getElementById("search-results");
  if(!input||!dropdown)return;
  let t;
  input.addEventListener("input",()=>{
    const q=input.value.trim();clearTimeout(t);
    if(q.length<2){dropdown.classList.add("hidden");return;}
    t=setTimeout(async()=>{
      const r=await fetch(`/api/search?q=${encodeURIComponent(q)}`);
      const players=await r.json();
      if(!players.length){dropdown.classList.add("hidden");return;}
      dropdown.innerHTML=players.map(p=>`<a href="/player/${p.id}"><span class="sr-name">${p.name}</span>${p.team?`<span class="sr-team">${p.team}</span>`:""}</a>`).join("");
      dropdown.classList.remove("hidden");
    },250);
  });
  document.addEventListener("click",e=>{if(!input.contains(e.target)&&!dropdown.contains(e.target))dropdown.classList.add("hidden");});
})();
