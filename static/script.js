const sendbutton = document.getElementById("sendbutton");
const userinput = document.getElementById("userinput");
const chatbody = document.getElementById("chat-body");
sendbutton.addEventListener("click", Sendmessage);
userinput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        Sendmessage();
    }
}
)

function Sendmessage() {
    const message = userinput.value.trim();
    if (message === "") return;


    const usermessage = document.createElement("div");
    usermessage.classList.add("user-message");
    usermessage.textContent = message;
    chatbody.appendChild(usermessage);
    userinput.value = "";
    chatbody.scrollTop = chatbody.scrollHeight;

    const typingMessage = document.createElement("div");
    typingMessage.classList.add("bot-message");
    typingMessage.textContent = "Bot is typing...";
    chatbody.appendChild(typingMessage);
    chatbody.scrollTop = chatbody.scrollHeight;

    // Send message to Flask
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
        .then(response => response.json())
        .then(data => {
            chatbody.removeChild(typingMessage);
            const botmessage = document.createElement("div");
            botmessage.classList.add("bot-message");
            botmessage.textContent = data.reply;
            chatbody.appendChild(botmessage);
            chatbody.scrollTop = chatbody.scrollHeight;
        })
        .catch(() => {
            chatbody.removeChild(typingMessage);
            const botmessage = document.createElement("div");
            botmessage.classList.add("bot-message");
            botmessage.textContent = "Server is not responding.";
            chatbody.appendChild(botmessage);
            chatbody.scrollTop = chatbody.scrollHeight;
        });
}

