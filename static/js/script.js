document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const form = document.querySelector('.chat-input-form');
    const userInputField = document.getElementById('user-input-field');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = userInputField.value;
        userInputField.value = '';

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', 'you');
        messageDiv.innerHTML = `<div class="chat-question">${question}</div>`;
        chatMessages.appendChild(messageDiv);

        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `question=${encodeURIComponent(question)}`
        });

        const answer = await response.text();

        const answerDiv = document.createElement('div');
        answerDiv.classList.add('chat-message', 'bot');
        answerDiv.innerHTML = `<div class="chat-answer">${answer}</div>`;
        chatMessages.appendChild(answerDiv);

        chatMessages.scrollTop = chatMessages.scrollHeight;
    });
});
