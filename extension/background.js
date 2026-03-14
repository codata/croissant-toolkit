chrome.action.onClicked.addListener((tab) => {
    chrome.sidePanel.open({ tabId: tab.id });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "extractContent") {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (!tabs[0]) {
                sendResponse({ error: "No active tab found" });
                return;
            }

            const tabId = tabs[0].id;

            chrome.scripting.executeScript(
                {
                    target: { tabId },
                    files: ["content.js"],
                },
                () => {
                    if (chrome.runtime.lastError) {
                        sendResponse({ error: chrome.runtime.lastError.message });
                        return;
                    }

                    chrome.tabs.sendMessage(tabId, { action: "extract" }, (response) => {
                        if (chrome.runtime.lastError) {
                            sendResponse({ error: chrome.runtime.lastError.message });
                            return;
                        }
                        sendResponse(response);
                    });
                }
            );
        });
        return true;
    }
});
