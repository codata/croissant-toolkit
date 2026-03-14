function extractPageContent() {
    const getMeta = (name) => {
        const el = document.querySelector(`meta[name="${name}"], meta[property="${name}"]`);
        return el ? el.getAttribute("content") || "" : "";
    };

    const headings = Array.from(document.querySelectorAll("h1, h2, h3"))
        .map((h) => h.textContent.trim())
        .filter(Boolean)
        .slice(0, 30);

    const links = Array.from(document.querySelectorAll("a[href]"))
        .map((a) => a.href)
        .filter((href) => href.startsWith("http"))
        .slice(0, 50);

    const images = Array.from(document.querySelectorAll("img"))
        .map((img) => ({
            src: img.src,
            alt: img.alt || "",
        }))
        .filter((img) => img.src)
        .slice(0, 20);

    const keywords = getMeta("keywords")
        .split(",")
        .map((k) => k.trim())
        .filter(Boolean);

    const bodyText = (document.body.innerText || "").slice(0, 5000);

    return {
        url: window.location.href,
        title: document.title || "",
        description: getMeta("description") || getMeta("og:description") || "",
        keywords,
        headings,
        links,
        images,
        body_text: bodyText,
        lang: document.documentElement.lang || "en",
    };
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "extract") {
        sendResponse(extractPageContent());
    }
});
