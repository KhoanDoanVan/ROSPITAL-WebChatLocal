function sendMessage() {
  const inputField = document.getElementById("chat-input");
  const message = inputField.value.trim();

  if (message === "") return;

  // Display user message
  addMessage(message, "user-message");

  // Show typing animation
  showTypingAnimation();

  // Send to server
  fetch('/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ question: message })
  })
  .then(response => response.json())
  .then(data => {

    removeTypingAnimation();

    if(data.answer) {
      addMessage(data.answer, "server-message");
    } else {
      addMessage("Error: Can't receive answer from Server", "error-message");
    }

  })
  .catch(error => {
    console.error('Error:', error);
    removeTypingAnimation();
    addMessage("Error connect to server", "error-message")
  })

  inputField.value = "";
}

function addMessage(text, className) {
  const chatBox = document.getElementById("chat-box");
  const msgElement = document.createElement("p");

  // Format message
  msgElement.innerHTML = text.replace(/\n/g, "<br>");  
  msgElement.classList.add("chat-message", className);
  
  chatBox.appendChild(msgElement);
  
  // Scroll
  chatBox.scrollTop = chatBox.scrollHeight;
}

// function showTypingAnimation() {
//   const chatBox = document.getElementById("chat-box");
//   const typingIndicator = document.createElement("p");
//   typingIndicator.id = "typing-animation";
//   typingIndicator.classList.add("chat-message", "server-message", "typing-animation");
//   typingIndicator.textContent = "";
//   chatBox.appendChild(typingIndicator);
//   chatBox.scrollTop = chatBox.scrollHeight;
// }

function showTypingAnimation() {
  const chatBox = document.getElementById("chat-box");
  const typingIndicator = document.createElement("div");
  typingIndicator.id = "typing-animation";
  typingIndicator.classList.add("chat-message", "server-message", "typing-animation");

  for (let i = 0; i < 3; i++) {
    const dot = document.createElement("span");
    typingIndicator.appendChild(dot);
  }

  chatBox.appendChild(typingIndicator);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to remove typing animation
function removeTypingAnimation() {
  const typingIndicator = document.getElementById("typing-animation");
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

// Fetch initial message from server
fetch("/message")
  .then(response => response.json())
  .then(data => {
    addMessage(data.message, "server-message");
  })
  .catch(error => console.error("Error fetching message:", error));