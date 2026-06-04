function toggleRoster(btn){
  const card=btn.closest(".team-card"),full=card.querySelector(".full-roster"),prev=card.querySelector(".roster-preview");
  if(full.classList.contains("hidden")){full.classList.remove("hidden");prev.classList.add("hidden");btn.textContent="Hide Roster ▴";}
  else{full.classList.add("hidden");prev.classList.remove("hidden");btn.textContent="See Full Roster ▾";}
}
