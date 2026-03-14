const API_BASE = "http://localhost:8000";

let currentCroissant = null;
let chatHistory = [];

const generateBtn = document.getElementById("generate-btn");
const statusEl = document.getElementById("status");
const outputEl = document.getElementById("croissant-output");
const jsonEl = document.getElementById("croissant-json");
const copyBtn = document.getElementById("copy-btn");
const downloadBtn = document.getElementById("download-btn");
const chatSection = document.getElementById("chat-section");
const chatHistoryEl = document.getElementById("chat-history");
const chatInput = document.getElementById("chat-input");
const chatSend = document.getElementById("chat-send");

function setStatus(text, type) {
    statusEl.textContent = text;
    statusEl.className = type;
}

function syntaxHighlight(json) {
    const str = JSON.stringify(json, null, 2);
    return str.replace(
        /("(\\u[\da-fA-F]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g,
        (match) => {
            let cls = "json-number";
            if (/^"/.test(match)) {
                cls = /:$/.test(match) ? "json-key" : "json-string";
            } else if (/true|false/.test(match)) {
                cls = "json-boolean";
            } else if (/null/.test(match)) {
                cls = "json-null";
            }
            return `<span class="${cls}">${match}</span>`;
        }
    );
}

function addChatMessage(role, content) {
    const msgEl = document.createElement("div");
    msgEl.className = `chat-message ${role}`;
    msgEl.textContent = content;
    chatHistoryEl.appendChild(msgEl);
    chatHistoryEl.scrollTop = chatHistoryEl.scrollHeight;
}

generateBtn.addEventListener("click", async () => {
    generateBtn.disabled = true;
    setStatus("Extracting page content...", "loading");

    chrome.runtime.sendMessage({ action: "extractContent" }, async (response) => {
        if (!response || response.error) {
            setStatus(`Extraction failed: ${response?.error || "Unknown error"}`, "error");
            generateBtn.disabled = false;
            return;
        }

        setStatus("Generating Croissant JSON-LD...", "loading");

        try {
            const res = await fetch(`${API_BASE}/generate-croissant`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(response),
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "API error");
            }

            const data = await res.json();
            currentCroissant = data.croissant;

            jsonEl.innerHTML = syntaxHighlight(currentCroissant);
            outputEl.classList.remove("hidden");
            chatSection.classList.remove("hidden");
            setStatus("Croissant generated successfully!", "success");
        } catch (err) {
            setStatus(`Error: ${err.message}`, "error");
        }

        generateBtn.disabled = false;
    });
});

copyBtn.addEventListener("click", () => {
    if (!currentCroissant) return;
    navigator.clipboard.writeText(JSON.stringify(currentCroissant, null, 2));
    copyBtn.textContent = "Copied!";
    setTimeout(() => { copyBtn.textContent = "Copy"; }, 1500);
});

downloadBtn.addEventListener("click", () => {
    if (!currentCroissant) return;
    const blob = new Blob([JSON.stringify(currentCroissant, null, 2)], { type: "application/ld+json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "croissant.json";
    a.click();
    URL.revokeObjectURL(url);
});

async function sendChatMessage() {
    const message = chatInput.value.trim();
    if (!message || !currentCroissant) return;

    chatInput.value = "";
    chatSend.disabled = true;
    addChatMessage("user", message);
    chatHistory.push({ role: "user", content: message });

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message,
                croissant: currentCroissant,
                history: chatHistory,
            }),
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "API error");
        }

        const data = await res.json();
        addChatMessage("assistant", data.response);
        chatHistory.push({ role: "assistant", content: data.response });
    } catch (err) {
        addChatMessage("assistant", `Error: ${err.message}`);
    }

    chatSend.disabled = false;
    chatInput.focus();
}

chatSend.addEventListener("click", sendChatMessage);
chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendChatMessage();
});
