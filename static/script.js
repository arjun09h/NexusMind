const sendbutton=document.getElementById("sendbutton");
const userinput=document.getElementById("userinput");
const chatbody=document.getElementById("chat-body");
sendbutton.addEventListener("click",Sendmessage);
userinput.addEventListener("keypress",function(event){
        if(event.key==="Enter"){
            Sendmessage();
        }
    }
)
function Sendmessage(){
    const message=userinput.value.trim();
    if(message==="") return;  // IGNORE EMPTY MESSAGES
    const usermessage=document.createElement("div");
    usermessage.classList.add("user-message");
    usermessage.textContent=message;
    chatbody.appendChild(usermessage);
    userinput.value=""; //after sending empty the text box
    chatbody.scrollTop=chatbody.scrollHeight;

    setTimeout(() => {
        const botmessage=document.createElement("div");
        botmessage.classList.add("bot-message");
        botmessage.textContent=getbotresponse(message);
        chatbody.appendChild(botmessage);
        chatbody.scrollTop=chatbody.scrollHeight;
    },500);
}
function getbotresponse(message){
    const responses={
        "hi":"Hello! How can I help you?",
        "how are you?":"I'm a bot, but I'm functioning as expected!",
        "what is your name?":"I'm ChatBot, your virtual assistant.",
        "bye":"Goodbye! Have a great day!"
    };
    return responses[message.toLowerCase()] || "I'm sorry, I don't understand that.";}
