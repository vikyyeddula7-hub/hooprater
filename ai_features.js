// ai_features.js — Feature 1 (Player Analysis) + Feature 2 (NL Search)

// ── Feature 1: AI Player Analysis button ─────────────────────────────────────
(function () {
  const btn = document.getElementById("ai-analyze-btn");
  if (!btn) return;

  const playerId = btn.dataset.playerId;
  const output   = document.getElementById("ai-analysis-output");

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    btn.textContent = "Analyzing…";
    output.classList.remove("hidden");
    output.innerHTML = `<div class="ai-loading">🤖 Generating analysis<span class="ai-dots">...</span></div>`;

    try {
      const res  = await fetch(`/api/ai/analyze_player/${playerId}`);
      const data = await res.json();

      if (data.error) {
        output.innerHTML = `<div class="ai-error">⚠ ${data.error}</div>`;
      } else {
        // Convert newlines to paragraphs
        const html = data.analysis
          .split("\n\n")
          .filter(Boolean)
          .map(p => `<p>${p.replace(/\n/g,"<br>")}</p>`)
          .join("");
        output.innerHTML = `
          <div class="ai-analysis-header">
            <span class="ai-badge">🤖 AI Analysis</span>
            <span class="ai-model">Claude AI</span>
          </div>
          <div class="ai-analysis-body">${html}</div>`;
      }
    } catch (e) {
      output.innerHTML = `<div class="ai-error">⚠ Network error. Please try again.</div>`;
    }

    btn.disabled = false;
    btn.textContent = "🤖 Regenerate Analysis";
  });
})();

// ── Feature 1: Tennis AI Analysis ────────────────────────────────────────────
(function () {
  const btn = document.getElementById("ai-tennis-analyze-btn");
  if (!btn) return;

  const rank   = btn.dataset.rank;
  const output = document.getElementById("ai-tennis-analysis-output");

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    btn.textContent = "Analyzing…";
    output.classList.remove("hidden");
    output.innerHTML = `<div class="ai-loading">🤖 Generating analysis<span class="ai-dots">...</span></div>`;

    try {
      const res  = await fetch(`/api/ai/analyze_tennis/${rank}`);
      const data = await res.json();

      if (data.error) {
        output.innerHTML = `<div class="ai-error">⚠ ${data.error}</div>`;
      } else {
        const html = data.analysis.split("\n\n").filter(Boolean)
          .map(p => `<p>${p.replace(/\n/g,"<br>")}</p>`).join("");
        output.innerHTML = `
          <div class="ai-analysis-header">
            <span class="ai-badge">🤖 AI Analysis</span>
            <span class="ai-model">Claude AI</span>
          </div>
          <div class="ai-analysis-body">${html}</div>`;
      }
    } catch (e) {
      output.innerHTML = `<div class="ai-error">⚠ Network error. Please try again.</div>`;
    }
    btn.disabled = false;
    btn.textContent = "🤖 Regenerate Analysis";
  });
})();

// ── Feature 2: Natural Language Search ───────────────────────────────────────
(function () {
  const input   = document.getElementById("nl-search-input");
  const btn     = document.getElementById("nl-search-btn");
  const output  = document.getElementById("nl-search-output");
  const grid    = document.getElementById("player-grid");
  const counter = document.getElementById("grid-count");
  if (!input || !btn) return;

  async function doSearch() {
    const q = input.value.trim();
    if (!q) return;

    btn.disabled = true;
    btn.textContent = "Searching…";

    // Show loading state in grid
    if (output) {
      output.innerHTML = `<div class="nl-loading">🤖 Finding players matching "<em>${q}</em>"…</div>`;
      output.classList.remove("hidden");
    }

    try {
      const res  = await fetch(`/api/ai/nl_search?q=${encodeURIComponent(q)}`);
      const data = await res.json();

      if (data.error) {
        if (output) output.innerHTML = `<div class="ai-error">⚠ ${data.error}</div>`;
        return;
      }

      const matchedNames = new Set(data.results.map(p => p.name));
      const allCards = grid ? Array.from(grid.querySelectorAll(".player-card")) : [];

      if (allCards.length > 0) {
        // Filter the existing grid
        let visible = 0;
        allCards.forEach(card => {
          const nameEl = card.querySelector(".card-name");
          const name = nameEl ? nameEl.textContent.trim() : "";
          const show = matchedNames.has(name);
          card.style.display = show ? "" : "none";
          if (show) visible++;
        });
        if (counter) counter.textContent = `Showing ${visible} players matching "${q}"`;
        if (output) output.innerHTML = visible > 0
          ? `<div class="nl-result-info">🤖 Found ${visible} players matching "<strong>${q}</strong>" — <button class="nl-clear-btn" onclick="clearNLSearch()">Clear search</button></div>`
          : `<div class="nl-result-info">🤖 No players matched "<strong>${q}</strong>" — <button class="nl-clear-btn" onclick="clearNLSearch()">Clear</button></div>`;
      }
    } catch (e) {
      if (output) output.innerHTML = `<div class="ai-error">⚠ Network error.</div>`;
    }

    btn.disabled = false;
    btn.textContent = "Search";
  }

  btn.addEventListener("click", doSearch);
  input.addEventListener("keydown", e => { if (e.key === "Enter") doSearch(); });
})();

window.clearNLSearch = function () {
  const grid = document.getElementById("player-grid");
  const counter = document.getElementById("grid-count");
  const output = document.getElementById("nl-search-output");
  const input = document.getElementById("nl-search-input");
  if (grid) Array.from(grid.querySelectorAll(".player-card")).forEach(c => c.style.display = "");
  if (counter) counter.textContent = "Showing all players · Ranked by NBA 2K26 OVR";
  if (output) output.classList.add("hidden");
  if (input) input.value = "";
};
