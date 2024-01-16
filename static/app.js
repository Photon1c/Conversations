console.log('Start of app.js');

function init() {
    console.log('init function called');

    // Function to make an asynchronous request to the server
    async function makeRequest(conversation) {
        try {
            const response = await fetch('/converse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(conversation)
            });

            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status} - ${response.statusText}`);
            }

            const responseData = await response.json();
            return responseData.conversation;
        } catch (error) {
            console.error('Error during request:', error);
            return [];
        }
    }

    function displayConversation(conversation) {
        console.log('Received conversation:', conversation);

        const container = document.getElementById('conversation-container');
        container.innerHTML = '';

        conversation.forEach(message => {
            const role = message.role === 'user' ? 'User' : 'Agent';
            const content = `${role}: ${message.content}`;
            const messageElement = document.createElement('div');
            messageElement.className = `message ${role.toLowerCase()}`;
            messageElement.textContent = content;
            container.appendChild(messageElement);
        });
    }

    async function startConversation(event) {
        event.preventDefault(); // Prevent default form submission
        console.log('button clicked');
        const loadingCircle = document.getElementById('loading');
        loadingCircle.style.display = 'inline-block';
        // Disable the "Start Conversation" button
        const startButton = document.getElementById('startButton');
        startButton.disabled = true;

        const form = document.getElementById('conversationForm');
        const formData = new FormData(form); // Get form data
        const conversation = Object.fromEntries(formData.entries()); // Convert FormData to JSON-like object
        console.log('Form data:', formData);
        // After the conversation is done, hide the loading circle and enable the button
        loadingCircle.style.display = 'none';
        startButton.disabled = false;
        try {
            console.log('Making request with data:', conversation);
            const completedConversation = await makeRequest(conversation);
            displayConversation(completedConversation); // Update the page with the conversation
            console.log('Received response:', completedConversation);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    // Add event listener to the form submission
    const form = document.getElementById('conversationForm');
    form.addEventListener('submit', startConversation);

    console.log(document.getElementById('conversation-container'));
}

document.addEventListener('DOMContentLoaded', init);
