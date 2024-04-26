function extractContext() {
    // Extract the top 3 contextually relevant snippets from the DOM
    const elements = document.querySelectorAll('p, h1, h2, h3, li');
    let textContent = [];
    elements.forEach(el => {
        textContent.push(el.textContent.trim());
    });

    // Send context to the background for further processing with LangChain semantic chunking
    sendContextToBackground(textContent.join('\n'));
}

function sendContextToBackground(context) {
    chrome.runtime.sendMessage({ action: "processContext", context: context });
}

// Execute the content script
const context = extractContext();
sendContextToBackground(context);
