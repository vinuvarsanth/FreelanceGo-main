document.addEventListener("DOMContentLoaded", function() {
    const chatContainer = document.getElementById("chat-container");
    const toggleChatBtn = document.getElementById("toggle-chat-btn");
    const closeBtn = document.getElementById("close-btn");

    toggleChatBtn.addEventListener("click", function() {
        chatContainer.classList.toggle("hidden");
        if (!chatContainer.classList.contains("hidden")) {
        const chatContainerHeight = chatContainer.clientHeight;
        toggleChatBtn.style.bottom = `${chatContainerHeight + 20}px`; // 20px padding
        } else {
        toggleChatBtn.style.bottom = "20px"; // Reset to initial position
        }
        toggleChatBtn.textContent = chatContainer.classList.contains("hidden") ? "Close Chat" : "Open Chat";
    });

    closeBtn.addEventListener("click", function() {
        chatContainer.classList.add("hidden");
        toggleChatBtn.textContent = "Open Chat";
        toggleChatBtn.style.bottom = "20px"; // Reset to initial position
    });
    });