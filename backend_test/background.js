chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "processRequest") {
        // Handle response generation based on user input and context using LM Studio Text Embeddings
        getEmbeddings(request.userPrompt)
            .then(embeddings => {
                processWithLangChain(embeddings, request.context)
                    .then(response => sendResponse({responseText: response}))
                    .catch(error => console.error('Error in LM Studio processing:', error));
            })
            .catch(err => console.error('Error getting embeddings:', err));
        return true; // Required to keep sendResponse open
    } else if (request.action === "processContext") {
        // Posting context to local server for semantic chunking after getting embeddings
        getEmbeddings(request.context).then(embeddings => {
            const xhr = new XMLHttpRequest();
            xhr.open("POST", "http://localhost:5000/processContext");
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    console.log('Context processed with LM Studio embeddings: ', xhr.responseText);
                }
            };
            xhr.send(JSON.stringify({ embeddings }));
        }).catch(err => console.error('Error getting embeddings for context:', err));
    }
});

async function getEmbeddings(text) {
    const response = await fetch('http://localhost:1234/v1/embeddings', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            input: text,
            model: 'model-identifier-here' // Specify the model identifier here
        })
    });

    if (!response.ok) {
        throw new Error('Failed to get embeddings from LM Studio');
    }

    const data = await response.json();
    return data.data;
}



async function processWithLangChain(userPrompt, context) {
    // Simulate API call to LangChain server for semantic processing
    const response = await fetch('http://localhost:5000/langchainProcess', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ prompt: userPrompt, context: context })
    });

    if (!response.ok) {
        throw new Error('Failed to process with LangChain');
    }

    const data = await response.json();
    return data.processedResponse;
}
