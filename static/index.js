document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.querySelector(".input-field input");
    const sendButton = document.querySelector(".input-field button");
    const chatBox = document.querySelector(".box");

    sendButton.addEventListener("click", function() {
        const userInput = inputField.value;
        if (userInput.trim() !== "") {
            // Create a new message div
            const userMessage = document.createElement("div");
            userMessage.classList.add("item", "right");
            const messageText = document.createElement("div");
            messageText.classList.add("msg");
            messageText.innerHTML = `<p>${userInput}</p>`;
            userMessage.appendChild(messageText);

            // Append the new message to the chat box
            chatBox.appendChild(userMessage);

            // Clear the input field
            inputField.value = "";

            // Scroll the chat box to the bottom
            chatBox.scrollTop = chatBox.scrollHeight;

            // Send the user input to the server and get a response
            fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: userInput })
            })
            .then(response => response.json())
            .then(data => {
                // Create a new bot message div
                const botMessage = document.createElement("div");
                botMessage.classList.add("item");
                const botMessageText = document.createElement("div");
                botMessageText.classList.add("msg");
                botMessageText.innerHTML = `<p>${data.response}</p>`;
                botMessage.appendChild(botMessageText);

                // Append the new bot message to the chat box
                chatBox.appendChild(botMessage);

                // Scroll the chat box to the bottom
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .catch(error => console.error("Error:", error));
        }
    });
});
