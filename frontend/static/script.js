// Chatbot
document.getElementById("sendBtn").addEventListener("click", async () => {
    const message = document.getElementById("userMessage").value;
    const chatResponse = document.getElementById("chatResponse");
    if (!message) return;

    chatResponse.innerText = "⏳ Väntar på AI...";
    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });
        const data = await res.json();
        chatResponse.innerText = data.reply;
    } catch {
        chatResponse.innerText = "❌ Fel med servern.";
    }
});

// Consultation
document.getElementById("consultBtn").addEventListener("click", async () => {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const message = document.getElementById("message").value;
    const consultResponse = document.getElementById("consultResponse");

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
