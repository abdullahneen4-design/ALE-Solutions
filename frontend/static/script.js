// Chatbot
const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

sendBtn.addEventListener("click", async () => {
    const message = userInput.value.trim();
    if(!message) return;
    appendMessage("You", message);
    userInput.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    });

    const data = await response.json();
    appendMessage("NEEN Bot", data.reply);
});

function appendMessage(sender, text){
    const p = document.createElement("p");
    p.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Consultation Form
const consultForm = document.getElementById("consult-form");
const consultReply = document.getElementById("consult-reply");

consultForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = {
        name: consultForm.name.value,
        email: consultForm.email.value,
        phone: consultForm.phone.value,
        message: consultForm.message.value
    };
    
    const response = await fetch("/consultation", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(formData)
    });

    const data = await response.json();
    consultReply.textContent = data.reply;
    consultForm.reset();
});
