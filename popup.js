document.getElementById('send-btn').addEventListener('click', () => handleSend());
document.getElementById('user-input').addEventListener('keypress', function(e) {
  if (e.key === 'Enter') handleSend();
});

let globalChatHistory = [];

document.addEventListener('DOMContentLoaded', () => loadSuggestions());

async function handleSend(forcedQuestion = null) {
  const inputEl = document.getElementById('user-input');
  const question = forcedQuestion ? forcedQuestion : inputEl.value.trim();
  if (!question) return;

  appendMessage('User', question, 'user');
  globalChatHistory.push({ role: 'user', text: question });
  
  if(!forcedQuestion) inputEl.value = '';
  
  document.getElementById('suggestions-container').innerHTML = '';

  const chatBox = document.getElementById('chat-box');
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'message ai';
  loadingDiv.innerText = 'AI is examining your screen...';
  chatBox.appendChild(loadingDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab) throw new Error("No active tab found.");

    const screenshotUrl = await chrome.tabs.captureVisibleTab(null, { format: 'jpeg', quality: 75 });
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
    globalChatHistory.push({ role: 'ai', text: data.answer });

    loadSuggestions();

  } catch (error) {
    loadingDiv.remove();
    appendMessage('Error', error.message, 'error');
  }
}

async function loadSuggestions() {
  const container = document.getElementById('suggestions-container');
  container.innerHTML = '<span style="font-size:11px; color:#666; padding-left:4px;">Contextualizing follow-ups...</span>';
  
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab) return;
    
    const screenshotUrl = await chrome.tabs.captureVisibleTab(null, { format: 'jpeg', quality: 50 });
    const base64Image = screenshotUrl.split(',')[1];
    
    const response = await fetch('http://127.0.0.1:8000/api/suggest-questions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        image_data: base64Image,
        chat_history: globalChatHistory 
      })
    });
    
    if (!response.ok) throw new Error();
    const data = await response.json();
    
    container.innerHTML = '';
    
    data.suggestions.forEach(question => {
      const chip = document.createElement('div');
      chip.className = 'suggestion-chip';
      chip.innerText = question;
      
      chip.addEventListener('click', () => {
        handleSend(question); 
      });
      container.appendChild(chip);
    });
    
  } catch (err) {
    container.innerHTML = ''; 
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