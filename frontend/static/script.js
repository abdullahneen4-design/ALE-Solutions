const chatWindow = document.getElementById("chatWindow");
const sendBtn = document.getElementById("sendBtn");

sendBtn.addEventListener("click", async () => {
    const input = document.getElementById("userMessage");
    const message = input.value.trim();
    if (!message) return;

    addMessage("user", message);
    input.value = "";
    
    addMessage("ai", "⏳ Väntar på AI...");

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });
        const data = await res.json();
        updateLastAIMessage(data.reply);
    } catch {
        updateLastAIMessage("❌ Fel med servern.");
    }
});

function addMessage(sender, text) {
    const msg = document.createElement("div");
    msg.classList.add("message");
    msg.classList.add(sender === "user" ? "user-msg" : "ai-msg");
    msg.innerText = text;
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function updateLastAIMessage(text) {
    const aiMessages = chatWindow.querySelectorAll(".ai-msg");
    if (aiMessages.length) {
        aiMessages[aiMessages.length - 1].innerText = text;
    }
}

// Consultation
const consultBtn = document.getElementById("consultBtn");
const consultResponse = document.getElementById("consultResponse");

consultBtn.addEventListener("click", async () => {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const message = document.getElementById("message").value;

    consultResponse.innerText = "⏳ Skickar meddelande...";
    try {
        const res = await fetch("/consultation", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, phone, message })
        });
        const data = await res.json();
        consultResponse.innerText = data.reply;
    } catch {
        consultResponse.innerText = "❌ Fel med servern.";
    }
});
