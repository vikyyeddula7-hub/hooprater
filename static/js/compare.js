(function(){
  const state={a:null,b:null};
  setup("search-a","results-a","card-a","a");
  setup("search-b","results-b","card-b","b");
  function setup(iid,did,cid,slot){
    const input=document.getElementById(iid),drop=document.getElementById(did),card=document.getElementById(cid);
    if(!input)return;let t;
    input.addEventListener("input",()=>{const q=input.value.trim();clearTimeout(t);if(q.length<2){drop.classList.add("hidden");return;}t=setTimeout(async()=>{const r=await fetch(`/api/search?q=${encodeURIComponent(q)}`);const ps=await r.json();render(drop,ps,slot,card,input);},250);});
    input.addEventListener("click",()=>input.select());
    document.addEventListener("click",e=>{if(!input.contains(e.target)&&!drop.contains(e.target))drop.classList.add("hidden");});
  }
  function render(el,players,slot,card,input){
    if(!players.length){el.classList.add("hidden");return;}
    el.innerHTML=players.map(p=>`<a href="#" data-id="${p.id}" data-name="${p.name}" data-team="${p.team||""}"><span class="sr-name">${p.name}</span>${p.team?`<span class="sr-team">${p.team}</span>`:""}</a>`).join("");
    el.classList.remove("hidden");
    el.querySelectorAll("a").forEach(a=>a.addEventListener("click",async e=>{
      e.preventDefault();input.value=a.dataset.name;el.classList.add("hidden");
      const res=await fetch(`/api/player/${a.dataset.id}`);const data=await res.json();
      if(data.error){card.textContent="Not found";return;}
      state[slot]=data;renderCard(card,data);if(state.a&&state.b)renderTable();
    }));
  }
  function renderCard(el,data){
    const s=data.stats,r=data.rating;
    el.classList.remove("empty");
    el.innerHTML=`<div style="text-align:center;padding:1rem;"><img src="${s.headshot_url}" style="height:120px;object-fit:contain;" onerror="this.src='/static/img/silhouette.svg'"/><div style="font-family:var(--font-head);font-weight:900;font-size:1.2rem;text-transform:uppercase;margin-top:.5rem;">${s.name}</div><div style="font-family:var(--font-mono);font-size:.7rem;color:var(--text-dim);">${s.position} · ${s.team}</div><div style="font-family:var(--font-head);font-size:3rem;font-weight:900;color:var(--accent2);line-height:1;margin-top:.75rem;">${r}</div><div style="font-family:var(--font-mono);font-size:.6rem;color:var(--text-dim);letter-spacing:.12em;">OVR (NBA 2K26)</div></div>`;
  }
  function renderTable(){
    const a=state.a.stats,b=state.b.stats,ra=state.a.rating,rb=state.b.rating;
    const rows=[
      {label:"OVR Rating (2K26)",va:ra,vb:rb,fmt:v=>v,higher:true},
      {label:"Points",va:a.pts,vb:b.pts,fmt:v=>parseFloat(v).toFixed(1),higher:true},
      {label:"Rebounds",va:a.reb,vb:b.reb,fmt:v=>parseFloat(v).toFixed(1),higher:true},
      {label:"Assists",va:a.ast,vb:b.ast,fmt:v=>parseFloat(v).toFixed(1),higher:true},
      {label:"Steals",va:a.stl,vb:b.stl,fmt:v=>parseFloat(v).toFixed(1),higher:true},
      {label:"Blocks",va:a.blk,vb:b.blk,fmt:v=>parseFloat(v).toFixed(1),higher:true},
      {label:"Turnovers",va:a.tov,vb:b.tov,fmt:v=>parseFloat(v).toFixed(1),higher:false},
      {label:"FG%",va:a.fg_pct*100,vb:b.fg_pct*100,fmt:v=>parseFloat(v).toFixed(1)+"%",higher:true},
      {label:"3PT%",va:a.fg3_pct*100,vb:b.fg3_pct*100,fmt:v=>parseFloat(v).toFixed(1)+"%",higher:true},
      {label:"FT%",va:a.ft_pct*100,vb:b.ft_pct*100,fmt:v=>parseFloat(v).toFixed(1)+"%",higher:true},
      {label:"True Shooting%",va:a.ts_pct*100,vb:b.ts_pct*100,fmt:v=>parseFloat(v).toFixed(1)+"%",higher:true},
      {label:"+/- Per Game",va:a.plus_minus,vb:b.plus_minus,fmt:v=>(v>0?"+":"")+parseFloat(v).toFixed(1),higher:true},
      {label:"Minutes",va:a.min,vb:b.min,fmt:v=>parseFloat(v).toFixed(1),higher:true},
      {label:"Games Played",va:a.gp,vb:b.gp,fmt:v=>v,higher:true},
    ];
    const trs=rows.map(row=>{
      const ab=row.higher?row.va>row.vb:row.va<row.vb,bb=row.higher?row.vb>row.va:row.vb<row.va;
      return `<tr><td class="cat-col">${row.label}</td><td class="${ab?"better":""}">${row.fmt(row.va)}</td><td class="${bb?"better":""}">${row.fmt(row.vb)}</td></tr>`;
    }).join("");
    const wrap=document.getElementById("compare-table-wrap");
    wrap.innerHTML=`<div class="compare-table-outer"><table class="compare-table"><thead><tr><th class="cat-col">Stat</th><th>${a.name}</th><th>${b.name}</th></tr></thead><tbody>${trs}</tbody></table></div>`;
    wrap.classList.remove("hidden");
  }
})();
