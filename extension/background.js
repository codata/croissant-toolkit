if (chrome.sidePanel) {
    chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true }).catch((error) => console.error(error));
}

chrome.action.onClicked.addListener((tab) => {
    if (typeof browser !== 'undefined' && browser.sidebarAction) {
        browser.sidebarAction.open();
    } else if (chrome.sidebarAction) {
        chrome.sidebarAction.open();
    }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "extractContent") {
        chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
            if (!tabs || !tabs[0]) {
                sendResponse({ error: "No active tab found" });
                return;
            }
            
            const tabId = tabs[0].id;
            
            chrome.tabs.sendMessage(tabId, { action: "extract" }, (response) => {
                if (chrome.runtime.lastError) {
                    // Fallback: If the content script isn't there (e.g., tab wasn't refreshed), inject it programmatically
                    chrome.scripting.executeScript({
                        target: { tabId: tabId },
                        files: ["content.js"]
                    }).then(() => {
                        // Wait a tiny bit for the listener to register, then try again
                        setTimeout(() => {
                            chrome.tabs.sendMessage(tabId, { action: "extract" }, (retryResponse) => {
                                if (chrome.runtime.lastError) {
                                    sendResponse({ error: "Cannot read this page type. Try on a normal website (not a new tab or chrome:// page)." });
                                } else {
                                    sendResponse(retryResponse);
                                }
                            });
                        }, 50);
                    }).catch((err) => {
                        sendResponse({ error: "Permission denied for this page (e.g., Chrome Web Store or internal page)." });
                    });
                    return;
                }
                sendResponse(response);
            });
        });
        return true;
    }
});
