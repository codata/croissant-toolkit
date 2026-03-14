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
            chrome.tabs.sendMessage(tabs[0].id, { action: "extract" }, (response) => {
                if (chrome.runtime.lastError) {
                    sendResponse({ error: chrome.runtime.lastError.message });
                    return;
                }
                sendResponse(response);
            });
        });
        return true;
    }
});
