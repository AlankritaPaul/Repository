# 🤖 Python AI Terminal Chatbot

A fast, interactive, and responsive terminal chatbot powered by OpenAI's Large Language Models. Built with continuous conversational memory, real-time response streaming, colorized terminal UI, and convenient in-chat commands.

---

## ✨ Features

- **No Account Required Out-of-the-Box**: Includes Free AI Cloud mode enabled by default. You can start chatting immediately without creating an OpenAI account or entering a credit card!
- **Continuous Conversation Loop**: Natural, multi-turn chat experience in your terminal that remembers prior context.
- **Real-Time Token Streaming**: Watch the AI generate responses live in real time.
- **Environment Variable Driven**: Seamlessly switch between Free AI Mode and official OpenAI (`gpt-4o-mini`, `gpt-4o`) via `.env` or system environment variables.
- **Cross-Platform Styled UI**: Clean, color-coded terminal messages with support for Windows, macOS, and Linux.
- **Interactive In-Chat Commands**:
  - `/help` - View available commands.
  - `/clear` or `/reset` - Clear chat memory and start fresh.
  - `/model <name>` - Switch models on the fly (e.g., `gpt-4o`, `gpt-4o-mini`).
  - `/system <prompt>` - Dynamically update the AI persona / instructions.
  - `/history` - View message and turn count.
  - `exit` or `quit` - Cleanly exit the session.
- **Robust Error Handling**: Friendly, actionable error messages for network issues and quota limits.

---

## 📋 Prerequisites

- **Python (advanced version)** installed on your system.
- *(Optional)* An **OpenAI API Key** if you wish to use official OpenAI models instead of the free tier.

---

## 🚀 Quick Start Guide

### 1. Clone the Repository

```bash
git clone https://github.com/AlankritaPaul/Repository.git
cd Repository
```

### 2. Create and Activate a Virtual Environment

It is recommended to use a virtual environment to manage dependencies:

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
.\venv\Scripts\activate.bat
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

---

## 🔑 Setting Up Your API Key

The chatbot requires an OpenAI API key provided through the `OPENAI_API_KEY` environment variable. You can configure this in one of two ways:

### Option A: Using a `.env` file (Recommended)

1. Copy the provided `.env.example` template to `.env`:
   ```bash
   # On Windows (PowerShell or CMD)
   copy .env.example .env

   # On macOS / Linux
   cp .env.example .env
   ```

2. Open `.env` in any text editor and replace the placeholder with your actual OpenAI API key:
   ```env
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. *(Optional)* You can also configure a preferred model or custom system instructions:
   ```env
   OPENAI_MODEL=gpt-4o-mini
   SYSTEM_PROMPT=You are a helpful, friendly, and intelligent AI assistant.
   ```

> [!CAUTION]
> **Never commit your `.env` file or hardcode your API key into git!**
> The `.gitignore` file in this repository is pre-configured to ensure `.env` is never committed.

---

### Option B: Setting the Environment Variable Directly in Terminal

If you prefer not to use a `.env` file, set the environment variable in your terminal session before running the chatbot:

- **Windows PowerShell:**
  ```powershell
  $env:OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  ```

- **Windows Command Prompt (CMD):**
  ```cmd
  set OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```

- **macOS / Linux (Bash / Zsh):**
  ```bash
  export OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  ```

---

## 💬 Running the Chatbot

Once your environment and API key are configured, start the chatbot with:

```bash
python chatbot.py
```

### Example Usage:

```text
============================================================
           🤖 Python AI Terminal Chatbot
============================================================
 Model: gpt-4o-mini
 Commands: Type /help for commands or exit to quit.
------------------------------------------------------------

You > Hello! Can you explain recursion in one simple sentence?
AI > Recursion is a programming technique where a function calls itself to solve smaller instances of the same problem until reaching a stopping condition.

You > Can you give a tiny Python example?
AI > def countdown(n):
    if n <= 0:
        print("Blast off!")
    else:
        print(n)
        countdown(n - 1)

countdown(3)

You > exit

👋 Goodbye! Have a wonderful day.
```

---

## 🛠️ Interactive In-Chat Commands

While in the chat loop, you can execute the following commands at any prompt:

| Command | Description |
| :--- | :--- |
| `/help` | Displays the list of available commands |
| `/clear` or `/reset` | Clears conversation history to start a brand new topic |
| `/model <name>` | Switches the OpenAI model in real-time (e.g. `/model gpt-4o`) |
| `/system <prompt>` | Updates the AI assistant's persona or behavioral instructions |
| `/history` | Displays current turn count and message history length |
| `exit` or `quit` | Gracefully closes the chat session |

---

## ⚙️ Configuration Reference

| Variable | Default | Description |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | *(Required)* | Your secret API key from OpenAI |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model identifier (e.g. `gpt-4o-mini`, `gpt-4o`) |
| `SYSTEM_PROMPT` | `"You are a helpful, friendly, and intelligent AI assistant."` | Base instructions guiding the AI's behavior |

---

## 📁 Repository Structure

```
Repository/
├── .env.example       # Template environment variable file
├── .gitignore         # Prevents secrets, cache, and virtual environments from tracking
├── chatbot.py         # Main application script
├── requirements.txt   # Python package dependencies
└── README.md          # Complete project guide and documentation
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
