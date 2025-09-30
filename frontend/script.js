function addMessage(text, sender = "bot") {
  const chatContainer = document.getElementById("chat-container");

  // Cria a linha da mensagem
  const messageRow = document.createElement("div");
  messageRow.className = `message-row ${sender}`;
  
  // Cria a mensagem em si
  const messageDiv = document.createElement("div");
  messageDiv.className = "chat-message";
  messageDiv.textContent = text;

  // Cria o horário
  const timeSpan = document.createElement("span");
  timeSpan.className = "time";
  const now = new Date();
  timeSpan.textContent = now.toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"});

  // Monta o bloco
  messageRow.appendChild(messageDiv);
  messageRow.appendChild(timeSpan);

  // Joga no chat
  chatContainer.appendChild(messageRow);

  // Scroll automático pro final
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addOpportunity(opportunity) {
  const chatContainer = document.getElementById("chat-container");
  
  const messageRow = document.createElement("div");
  messageRow.className = "message-row bot";
  
  const opportunityDiv = document.createElement("div");
  opportunityDiv.className = "opportunity-card";
  opportunityDiv.innerHTML = `
    <div class="opportunity-title">${opportunity.title}</div>
    <div class="opportunity-org">${opportunity.organization}</div>
    ${opportunity.deadline ? `<div class="opportunity-deadline">Deadline: ${opportunity.deadline}</div>` : ''}
    ${opportunity.url ? `<a href="${opportunity.url}" target="_blank" class="opportunity-link">View Details</a>` : ''}
  `;
  
  const timeSpan = document.createElement("span");
  timeSpan.className = "time";
  const now = new Date();
  timeSpan.textContent = now.toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"});
  
  messageRow.appendChild(opportunityDiv);
  messageRow.appendChild(timeSpan);
  chatContainer.appendChild(messageRow);
  
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Mensagem inicial
addMessage("Hi! I'm your AI opportunity scout. Tell me what you're looking for - scholarships, fellowships, or accelerator programs! For example: 'I'm looking for climate tech scholarships for graduate students' or 'Show me accelerator programs in Europe'.");

// Enviar mensagem com Enter ou Botão
document.getElementById("send-button").addEventListener("click", sendMessage);
document.getElementById("chat-input").addEventListener("keypress", function(e) {
  if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
  const input = document.getElementById("chat-input");
  const text = input.value.trim();

  if (text) {
    // Adiciona a mensagem do usuário
    addMessage(text, "user");
    input.value = "";

    // Show loading
    const loadingId = addMessage("Please be patiante I am looking through the web ( the web is very big )", "bot");

    try {
      // Lightweight intent extraction for better results
      const lower = text.toLowerCase();
      let inferredType = null;
      if (lower.includes("accelerator")) inferredType = "accelerator";
      else if (lower.includes("fellowship")) inferredType = "fellowship";
      else if (lower.includes("scholarship")) inferredType = "scholarship";

      // Pick a reasonable keyword (first significant word)
      let keyword = "technology";
      const words = text.split(/\s+/).filter(w => w.length > 3);
      if (words.length > 0) keyword = words[0].replace(/[^a-zA-Z0-9-]/g, "");

      // Build URL with inferred params
      const url = inferredType
        ? `/api/search?keyword=${encodeURIComponent(keyword)}&type=${encodeURIComponent(inferredType)}`
        : `/api/search?keyword=${encodeURIComponent(keyword)}`;

      // Call local API
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      const data = await response.json();

      // Remove loading message
      const loadingElement = document.querySelector('.message-row.bot:last-child');
      if (loadingElement) loadingElement.remove();

      // When no results, show friendly message
      if (!Array.isArray(data) || data.length === 0) {
        addMessage("Sorry, I found nothing for you... :(", "bot");
        return;
      }

      // Adiciona resposta da IA
      addMessage("Found " + data.length + " opportunities for you!", "bot");

      // Adiciona oportunidades
      data.forEach(opp => {
        addOpportunity(opp);
      });
      
    } catch (error) {
      console.error("Error calling the API:", error);
      addMessage("Oops! Something went wrong. Please try again.", "bot");
    }
  }
}
