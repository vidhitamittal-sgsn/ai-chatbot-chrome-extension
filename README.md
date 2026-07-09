# ai-chatbot-chrome-extension
A chrome extension that is an AI chatbot which will answer questions about the user's screen.

## 🛠️ Prerequisites

Before getting started, ensure you have the following installed on your machine:
* **Google Chrome Browser**
* **Python 3.10+**
* An **OpenAI Developer API Key** 
---

## 🚀 Setup Instructions

### 1. Backend Installation (Python)

1. Clone or navigate to your project directory:
   ```bash
   cd path/to/your/project-folder
1. Install the required Python packages:
   ```bash
   pip install fastapi uvicorn openai pydantic python-dotenv 
3. Create a file named .env in the root of your project directory and add your OpenAI API key:
   - Code snippet: OPENAI_API_KEY= your_secret_key 
5. Run the local development server:
   ```bash
   python app.py
6. The terminal should indicate that Uvicorn is successfully running on http://127.0.0.1:8000

### 2. Frontend Installation (Chrome Extension)
1. Open Google Chrome and navigate to the extensions management page by entering: chrome://extensions/
2. In the top-right corner, switch the Developer mode toggle to ON.
3. In the top-left corner, click the Load unpacked button.
4. Select the folder containing your extension files (manifest.json, popup.html, popup.js).

🎯 How to Use
1. Navigate to any webpage you want to interact with.
2. Click the Extension icon in your Chrome toolbar and pin the Screen AI Assistant.
3. Click the extension icon to reveal the chat interface layout.
4. Type a question regarding what you can see in your browser window and hit Send (or press Enter).
5. The AI will look at your screen snapshot and return a highly context-specific response.
