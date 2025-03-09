document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');

    sendButton.addEventListener('click', async function() {
        const userQuery = chatInput.value.trim();
        if (!userQuery) return;

        // Display user message
        const userMessage = document.createElement('div');
        userMessage.textContent = `You: ${userQuery}`;
        chatMessages.appendChild(userMessage);

        // Disable input and show loading state
        chatInput.disabled = true;
        chatInput.placeholder = 'Fetching response...';
        sendButton.disabled = true;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: userQuery })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            // Display chatbot response
            const botMessage = document.createElement('div');
            botMessage.textContent = `Reflash: ${data.response}`;
            chatMessages.appendChild(botMessage);
        } catch (error) {
            console.error('Error fetching chat response:', error);
            const errorMessage = document.createElement('div');
            errorMessage.textContent = 'Error fetching response. Please try again.';
            chatMessages.appendChild(errorMessage);
        } finally {
            // Re-enable input
            chatInput.disabled = false;
            chatInput.placeholder = 'Ask a question and let your database answer you';
            sendButton.disabled = false;
            chatInput.value = '';
        }
    });

    chatInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendButton.click();
        }
    });
}); 