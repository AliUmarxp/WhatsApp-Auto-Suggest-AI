# 💬 WhatsApp Auto-Suggest AI (Local Copilot)

A fully offline, Python-based WhatsApp Live Typing Assistant that acts as your casual friend. It runs in the background and magically provides 3 context-aware auto-reply suggestions whenever you copy (`Ctrl+C`) an incoming message from WhatsApp Web/Desktop.

It uses **GPT4All** to run lightweight models entirely on your local CPU.

> [!TIP]
> **Pro Tip for Better Responses:** This app defaults to a 1.5B parameter model (Qwen2) to run smoothly on laptops with 8GB RAM. However, if your PC has a dedicated GPU or more RAM, you should update `ai_engine.py` to use a heavy **7B+ parameter model** (like Llama-3-8B-Instruct or Mistral). Alternatively, for the best human-like logic, you can easily modify the script to connect to the **OpenAI API**!

---

## 🌟 Features
- **100% Offline & Private:** Your chats never leave your PC. It uses `gpt4all` for local LLM inference.
- **Copy-to-Trigger:** Invisible background listener. Just highlight a message, press `Ctrl+C`, and the AI Assistant pops up instantly.
- **Auto-Type (Ctrl+V):** Click any suggestion, and it instantly pastes the reply into WhatsApp and hits enter.
- **Chat History Backup:** Keeps a private backup log of your chats and AI inferences in `chat_history.txt`.
- **CPU Optimized:** Tuned `n_ctx` and tokens limits for laptops without dedicated GPUs to run models smoothly.
- **Auto-Hide Stealth Mode:** The GUI completely vanishes from the screen when done, remaining actively loaded in RAM to eliminate delay.

---

## 🛠️ Prerequisites
- OS: Windows 10/11
- Python 3.10+
- RAM: Minimum 8GB

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/WhatsApp-AI-Assistant.git
   cd WhatsApp-AI-Assistant
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Required AI Model:**
   - The script by default uses `qwen2-1_5b-instruct-q4_0.gguf`. You can download this (or any) `.gguf` local model through the official GPT4All GUI, and this script will automatically locate and load it.

---

## 💻 How to Use

1. **Start the Assistant:**
   - Open your Anaconda/Python Terminal and run `python main.py` **OR**
   - Simply double-click `Run_Assistant.vbs` to trigger the Python script completely hidden in the background without any black windows.
2. **Copy Text:**
   - Open WhatsApp Web. Select the message your friend sent you and press `Ctrl+C`.
3. **Select a Reply:**
   - The Assistant box will magically appear on your screen with exactly 3 contextual suggestions.
4. **Send:**
   - Click your favorite reply. The Assistant will auto-paste the message back into WhatsApp and hit Enter!

---

## 🧠 File Structure
- `main.py`: The Tkinter UI, Background Threadding, and Clipboard Monitor.
- `ai_engine.py`: Encapsulates the GPT4All logic, Model Parameters, and Prompt Engineering templates.
- `window_manager.py`: Utilities to track WhatsApp active states.
- `Run_Assistant.vbs`: A VBScript macro used to hide the python terminal. 

Enjoy your new AI-powered Chat Copilot! 🚀
