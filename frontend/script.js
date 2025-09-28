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

    // Mostra loading
    const loadingId = addMessage("🤔 Searching for opportunities...", "bot");

    try {
      // Chama a API local
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: text })
      });

      const data = await response.json();
      
      // Remove loading message
      const loadingElement = document.querySelector('.message-row.bot:last-child');
      if (loadingElement) loadingElement.remove();
      
      // Adiciona resposta da IA
      addMessage(data.response, "bot");
      
      // Adiciona oportunidades se houver
      if (data.opportunities && data.opportunities.length > 0) {
        data.opportunities.forEach(opp => {
          addOpportunity(opp);
        });
      }
      
    } catch (error) {
      console.error("Erro ao chamar a API:", error);
      addMessage("Oops! Algo deu errado. Tente novamente.", "bot");
    }
  }
}
