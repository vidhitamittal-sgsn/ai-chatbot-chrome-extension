// document.getElementById('send-btn').addEventListener('click', handleSend);
// document.getElementById('user-input').addEventListener('keypress', function(e) {
//   if (e.key === 'Enter') handleSend();
// });

// async function handleSend() {
//   const inputEl = document.getElementById('user-input');
//   const question = inputEl.value.trim();
//   if (!question) return;

//   appendMessage('User', question, 'user');
//   inputEl.value = '';

//   const chatBox = document.getElementById('chat-box');
//   const loadingDiv = document.createElement('div');
//   loadingDiv.className = 'message ai';
//   loadingDiv.innerText = 'AI is thinking...';
//   chatBox.appendChild(loadingDiv);
//   chatBox.scrollTop = chatBox.scrollHeight;

//   try {
//     // 1. Get the active browser tab
//     const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
//     if (!tab) throw new Error("No active tab found.");

//     // 2. Inject a script to scrape the visible innerText of the page
//     const [scriptResult] = await chrome.scripting.executeScript({
//       target: { tabId: tab.id },
//       func: () => document.body.innerText
//     });

//     const pageContent = scriptResult.result || "";

//     // 3. Post the page content and question to the local Python backend
//     const response = await fetch('http://127.0.0.1:8000/api/chat', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({ page_content: pageContent, question: question })
//     });

//     loadingDiv.remove();

//     if (!response.ok) {
//       const errData = await response.json();
//       throw new Error(errData.detail || "Server error");
//     }

//     const data = await response.json();
//     appendMessage('AI', data.answer, 'ai');

//   } catch (error) {
//     loadingDiv.remove();
//     appendMessage('Error', error.message, 'error');
//   }
// }

// function appendMessage(sender, text, className) {
//   const chatBox = document.getElementById('chat-box');
//   const msgDiv = document.createElement('div');
//   msgDiv.className = `message ${className}`;
//   msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
//   chatBox.appendChild(msgDiv);
//   chatBox.scrollTop = chatBox.scrollHeight;
// }
document.getElementById('send-btn').addEventListener('click', handleSend);
document.getElementById('user-input').addEventListener('keypress', function(e) {
  if (e.key === 'Enter') handleSend();
});

async function handleSend() {
  const inputEl = document.getElementById('user-input');
  const question = inputEl.value.trim();
  if (!question) return;

  appendMessage('User', question, 'user');
  inputEl.value = '';

  const chatBox = document.getElementById('chat-box');
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'message ai';
  loadingDiv.innerText = 'AI is examining your screen...';
  chatBox.appendChild(loadingDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab) throw new Error("No active tab found.");
    const screenshotUrl = await chrome.tabs.captureVisibleTab(null, { format: 'jpeg', quality: 80 });
    const base64Image = screenshotUrl.split(',')[1];
    const response = await fetch('http://127.0.0.1:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image_data: base64Image, question: question })
    });

    loadingDiv.remove();

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || "Server error");
    }

    const data = await response.json();
    appendMessage('AI', data.answer, 'ai');

  } catch (error) {
    loadingDiv.remove();
    appendMessage('Error', error.message, 'error');
  }
}

function appendMessage(sender, text, className) {
  const chatBox = document.getElementById('chat-box');
  const msgDiv = document.createElement('div');
  msgDiv.className = `message ${className}`;
  msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}