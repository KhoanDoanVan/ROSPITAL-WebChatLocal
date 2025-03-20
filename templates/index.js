function sendMessage() {
  fetch("/data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: "Hello from the client!" })
  })
  .then(response => response.json())
  .then(data => {
    alert(data.message);
  })
  .catch(error => console.error("Error sending message:", error));
}

// Fetch initial message from server
fetch("/message")
  .then(response => response.json())
  .then(data => {
    document.getElementById("message").innerText = data.message;
  })
  .catch(error => console.error("Error fetching message:", error));