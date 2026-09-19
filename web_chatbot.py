#!/usr/bin/env python3
"""
Web UI for AI Chatbot
=====================
A zero-dependency local web interface for the AI Chatbot that runs in your
browser without needing any external web framework.
"""

import sys
import os
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chatbot import get_client_and_config

PORT = 5000
client, model_name, display_name = get_client_and_config()
conversation_history = [
    {"role": "system", "content": "You are a friendly, helpful, and intelligent AI assistant."}
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0f172a;
            --surface: #1e293b;
            --surface-hover: #334155;
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --ai-bubble: #1e293b;
            --user-bubble: #6366f1;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--text);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            padding: 16px;
        }
        .chat-container {
            width: 100%;
            max-width: 800px;
            height: 90vh;
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }
        .header {
            padding: 18px 24px;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header-title {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .avatar {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #6366f1, #a855f7);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .title h1 { font-size: 16px; font-weight: 700; color: var(--text); }
        .title p { font-size: 12px; color: #10b981; display: flex; align-items: center; gap: 6px; }
        .title p::before {
            content: '';
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 10px #10b981;
        }
        .clear-btn {
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .clear-btn:hover { background: var(--surface-hover); color: var(--text); }
        .messages {
            flex: 1;
            padding: 24px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }
        .message {
            display: flex;
            gap: 12px;
            max-width: 80%;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
        .message.user { align-self: flex-end; flex-direction: row-reverse; }
        .message.ai { align-self: flex-start; }
        .message-bubble {
            padding: 14px 18px;
            border-radius: 16px;
            font-size: 14px;
            line-height: 1.6;
            word-break: break-word;
            white-space: pre-wrap;
        }
        .message.user .message-bubble {
            background: var(--user-bubble);
            color: #fff;
            border-bottom-right-radius: 4px;
        }
        .message.ai .message-bubble {
            background: var(--ai-bubble);
            color: var(--text);
            border: 1px solid var(--border);
            border-bottom-left-radius: 4px;
        }
        .suggestions {
            display: flex;
            gap: 8px;
            padding: 0 24px 12px;
            overflow-x: auto;
        }
        .chip {
            background: var(--surface);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 8px 14px;
            border-radius: 20px;
            font-size: 12px;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }
        .chip:hover {
            border-color: var(--primary);
            color: var(--text);
            background: var(--surface-hover);
        }
        .input-bar {
            padding: 18px 24px;
            background: var(--surface);
            border-top: 1px solid var(--border);
            display: flex;
            gap: 12px;
        }
        .input-bar input {
            flex: 1;
            background: #0f172a;
            border: 1px solid var(--border);
            color: var(--text);
            padding: 14px 18px;
            border-radius: 12px;
            font-size: 14px;
            outline: none;
            transition: border 0.2s;
        }
        .input-bar input:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2); }
        .send-btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 0 22px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .send-btn:hover { background: var(--primary-hover); transform: translateY(-1px); }
        .send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .typing { display: inline-flex; gap: 4px; padding: 4px 8px; }
        .typing span {
            width: 6px; height: 6px; background: var(--text-muted); border-radius: 50%;
            animation: blink 1.4s infinite;
        }
        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes blink { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <div class="header-title">
                <div class="avatar">🤖</div>
                <div class="title">
                    <h1>Python AI Chatbot</h1>
                    <p>Online & Ready</p>
                </div>
            </div>
            <button class="clear-btn" onclick="clearChat()">Reset Chat</button>
        </div>
        <div class="messages" id="messages">
            <div class="message ai">
                <div class="avatar" style="width:32px;height:32px;font-size:16px;">🤖</div>
                <div class="message-bubble">Hello! I am your AI Chatbot. I'm connected and working properly. Ask me anything!</div>
            </div>
        </div>
        <div class="suggestions">
            <div class="chip" onclick="useSuggestion('Tell me a funny programming joke!')">😄 Tell a joke</div>
            <div class="chip" onclick="useSuggestion('What are the best features of Python?')">🐍 Why Python?</div>
            <div class="chip" onclick="useSuggestion('Give me 3 creative coding project ideas')">💡 Project ideas</div>
            <div class="chip" onclick="useSuggestion('Explain how Large Language Models work in 2 sentences')">🧠 How AI works</div>
        </div>
        <div class="input-bar">
            <input type="text" id="userInput" placeholder="Type your question here and press Enter..." onkeydown="handleKey(event)" autofocus>
            <button class="send-btn" id="sendBtn" onclick="sendMessage()">Send ➔</button>
        </div>
    </div>

    <script>
        const messagesDiv = document.getElementById('messages');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');

        function appendMessage(role, text) {
            const msg = document.createElement('div');
            msg.className = 'message ' + role;
            const avatar = document.createElement('div');
            avatar.className = 'avatar';
            avatar.style.width = '32px';
            avatar.style.height = '32px';
            avatar.style.fontSize = '16px';
            avatar.textContent = role === 'user' ? '👤' : '🤖';

            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            bubble.textContent = text;

            msg.appendChild(avatar);
            msg.appendChild(bubble);
            messagesDiv.appendChild(msg);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            return bubble;
        }

        async function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;

            appendMessage('user', text);
            userInput.value = '';
            userInput.focus();

            sendBtn.disabled = true;
            const typingBubble = appendMessage('ai', '...');
            typingBubble.innerHTML = '<div class="typing"><span></span><span></span><span></span></div>';

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await res.json();
                typingBubble.textContent = data.reply || 'No response';
            } catch (err) {
                typingBubble.textContent = 'Error connecting to server. Please try again.';
            } finally {
                sendBtn.disabled = false;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
        }

        function handleKey(e) {
            if (e.key === 'Enter') sendMessage();
        }

        function useSuggestion(text) {
            userInput.value = text;
            sendMessage();
        }

        async function clearChat() {
            await fetch('/api/reset', { method: 'POST' });
            messagesDiv.innerHTML = `
                <div class="message ai">
                    <div class="avatar" style="width:32px;height:32px;font-size:16px;">🤖</div>
                    <div class="message-bubble">Conversation history cleared! How can I help you?</div>
                </div>
            `;
        }
    </script>
</body>
</html>
"""


class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        global conversation_history
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                user_msg = data.get("message", "").strip()

                conversation_history.append({"role": "user", "content": user_msg})

                response = client.chat.completions.create(
                    model=model_name,
                    messages=conversation_history
                )
                ai_reply = response.choices[0].message.content or ""
                conversation_history.append({"role": "assistant", "content": ai_reply})

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"reply": ai_reply}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/reset":
            conversation_history = [
                {"role": "system", "content": "You are a friendly, helpful, and intelligent AI assistant."}
            ]
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "cleared"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress routine HTTP log spam
        pass


def start_server():
    server = HTTPServer(("127.0.0.1", PORT), ChatHandler)
    print(f"Server started at http://127.0.0.1:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    start_server()
