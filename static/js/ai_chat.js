// ai_chat.js — Feature 6: Floating Conversational Chat Widget

(function () {
  // Only mount if AI is available (injected by template)
  if (!window.AI_AVAILABLE) return;

  const history = []; // [{role, content}]

  // ── Build widget HTML ──────────────────────────────────────────────────────
  const widget = document.createElement("div");
  widget.id = "ai-chat-widget";
  widget.innerHTML = `
    <button id="chat-toggle" title="Ask AI Assistant">
      <span id="chat-toggle-icon">🤖</span>
    </button>
    <div id="chat-panel" class="hidden">
      <div id="chat-header">
        <span>🤖 AI Assistant</span>
        <button id="chat-close">✕</button>
      </div>
      <div id="chat-messages">
        <div class="chat-msg assistant">
          <div class="chat-bubble">Hey! I'm your HoopRater AI. Ask me anything about NBA players, teams, or ATP tennis — like <em>"Who is the best center this season?"</em> or <em>"Compare Sinner vs Alcaraz."</em></div>
        </div>
      </div>
      <div id="chat-input-row">
        <input id="chat-input" type="text" placeholder="Ask about players, teams, tennis…" autocomplete="off"/>
        <button id="chat-send">↑</button>
      </div>
    </div>
  `;
  document.body.appendChild(widget);

  // Inject styles
  const style = document.createElement("style");
  style.textContent = `
    #ai-chat-widget { position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 9999; font-family: var(--font-body, sans-serif); }
    #chat-toggle { background: var(--accent, #e8523a); border: none; border-radius: 50%; width: 54px; height: 54px; cursor: pointer; font-size: 1.4rem; box-shadow: 0 4px 20px rgba(0,0,0,.4); transition: transform .2s; display: flex; align-items: center; justify-content: center; }
    #chat-toggle:hover { transform: scale(1.1); }
    #chat-panel { position: absolute; bottom: 66px; right: 0; width: 340px; background: var(--bg2, #111); border: 1px solid var(--border, #242a35); border-radius: 14px; box-shadow: 0 16px 48px rgba(0,0,0,.6); overflow: hidden; display: flex; flex-direction: column; }
    #chat-panel.hidden { display: none; }
    #chat-header { display: flex; align-items: center; justify-content: space-between; padding: .75rem 1rem; background: var(--accent, #e8523a); color: #fff; font-family: var(--font-head, sans-serif); font-weight: 700; font-size: .9rem; letter-spacing: .05em; }
    #chat-close { background: none; border: none; color: #fff; cursor: pointer; font-size: 1rem; padding: 0; }
    #chat-messages { height: 320px; overflow-y: auto; padding: 1rem; display: flex; flex-direction: column; gap: .75rem; }
    .chat-msg { display: flex; }
    .chat-msg.user { justify-content: flex-end; }
    .chat-bubble { max-width: 82%; padding: .55rem .85rem; border-radius: 14px; font-size: .82rem; line-height: 1.5; }
    .chat-msg.user .chat-bubble { background: var(--accent, #e8523a); color: #fff; border-bottom-right-radius: 4px; }
    .chat-msg.assistant .chat-bubble { background: var(--bg3, #181d24); color: var(--text, #e8ecf4); border-bottom-left-radius: 4px; border: 1px solid var(--border, #242a35); }
    .chat-msg.assistant .chat-bubble em { color: var(--accent2, #f0a500); font-style: normal; }
    .chat-typing .chat-bubble::after { content: "●●●"; animation: typing 1s infinite; }
    @keyframes typing { 0%,100%{opacity:.3} 50%{opacity:1} }
    #chat-input-row { display: flex; gap: .5rem; padding: .75rem; border-top: 1px solid var(--border, #242a35); }
    #chat-input { flex: 1; background: var(--bg3, #181d24); border: 1px solid var(--border, #242a35); border-radius: 8px; color: var(--text, #e8ecf4); font-size: .82rem; padding: .5rem .75rem; outline: none; }
    #chat-input:focus { border-color: var(--accent, #e8523a); }
    #chat-send { background: var(--accent, #e8523a); border: none; border-radius: 8px; color: #fff; cursor: pointer; font-size: 1rem; padding: .4rem .7rem; transition: background .2s; }
    #chat-send:hover { background: #c8412a; }
    #chat-send:disabled { opacity: .4; cursor: not-allowed; }
  `;
  document.head.appendChild(style);

  // ── Event listeners ────────────────────────────────────────────────────────
  const panel  = document.getElementById("chat-panel");
  const input  = document.getElementById("chat-input");
  const send   = document.getElementById("chat-send");
  const msgs   = document.getElementById("chat-messages");

  document.getElementById("chat-toggle").addEventListener("click", () => {
    panel.classList.toggle("hidden");
    if (!panel.classList.contains("hidden")) input.focus();
  });
  document.getElementById("chat-close").addEventListener("click", () => {
    panel.classList.add("hidden");
  });
  send.addEventListener("click", sendMessage);
  input.addEventListener("keydown", e => { if (e.key === "Enter") sendMessage(); });

  function appendMsg(role, text) {
    const div = document.createElement("div");
    div.className = `chat-msg ${role}`;
    div.innerHTML = `<div class="chat-bubble">${text.replace(/\n/g,"<br>")}</div>`;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    return div;
  }

  async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    send.disabled = true;

    appendMsg("user", text);
    history.push({ role: "user", content: text });

    // Typing indicator
    const typing = appendMsg("assistant", "");
    typing.classList.add("chat-typing");

    try {
      const res = await fetch("/api/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history })
      });
      const data = await res.json();
      typing.remove();

      const reply = data.reply || data.error || "Sorry, something went wrong.";
      appendMsg("assistant", reply);
      history.push({ role: "assistant", content: reply });

      // Keep history manageable (last 10 exchanges)
      if (history.length > 20) history.splice(0, 2);
    } catch (err) {
      typing.remove();
      appendMsg("assistant", "Network error — please try again.");
    }

    send.disabled = false;
    input.focus();
  }
})();
