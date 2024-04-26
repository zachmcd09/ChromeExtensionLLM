async function sendUserPrompt() {
  const userInput = document.getElementById('userInput').value;
  const pageContent = await getPageContent(); // Function to retrieve content from background.js
  try {
      const response = await chrome.runtime.sendMessage({
          action: 'processRequest',
          userPrompt: userInput,
          context: pageContent
      });
      document.getElementById('response').textContent = response.responseText;
  } catch (error) {
      console.error('Error sending message:', error);
  }
}

async function getPageContent() {
  const message = await chrome.runtime.sendMessage({ action: 'getPageContent' });
  return message.pageContent;
}
