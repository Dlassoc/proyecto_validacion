
const chatbotButton = document.getElementById('chatbot-button');
const chatbotWindow = document.getElementById('chatbot-window');
const chatbotClose = document.getElementById('chatbot-close');
const chatbotForm = document.getElementById('chatbot-form');
const chatbotInput = document.getElementById('chatbot-input');
const chatbotMessages = document.getElementById('chatbot-messages');

chatbotButton.addEventListener('click', () => {
    chatbotWindow.style.display = 'flex';
});

chatbotClose.addEventListener('click', () => {
    chatbotWindow.style.display = 'none';
});

chatbotForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const userMessage = chatbotInput.value.trim();
    if (!userMessage) return;

    // Mostrar mensaje del usuario
    const userMsgDiv = document.createElement('div');
    userMsgDiv.classList.add('user-message');
    userMsgDiv.textContent = userMessage;
    chatbotMessages.appendChild(userMsgDiv);

    chatbotInput.value = '';
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

    // Simular respuesta del bot con delay
    setTimeout(() => {
        const botMsgDiv = document.createElement('div');
        botMsgDiv.classList.add('bot-message');

        // Respuestas básicas
        let botResponse = "Lo siento, no te entiendo.";
        if (userMessage.toLowerCase().includes('hello') || userMessage.toLowerCase().includes('hi')) {
            botResponse = "Hello! How can I help you today?";
        } else if (userMessage.toLowerCase().includes('flight')) {
            botResponse = "Do you want information about flights?";
        }

        botMsgDiv.textContent = botResponse;
        chatbotMessages.appendChild(botMsgDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }, 800);
})
