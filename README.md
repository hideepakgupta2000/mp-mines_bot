# mp-mines_bot 

A Telegram bot designed for fetching and processing mining-related data (e.g., eMM11 entries) for Madhya Pradesh users. It supports:

- Interactive querying of data via the `/start` command  
- Fetching entries by specifying a range and district  
- Automatically logging into a mining portal to process data  
- Generating downloadable PDFs from results  

---

##  Features

- **User-friendly flow**: Prompt users for a start number, end number, and district via inline conversation.  
- **Asynchronous fetching**: Data is collected and presented to users efficiently using `asyncio`.  
- **Automated processing**: Bot logs into a backend system, retrieves relevant details, and stores them for further actions.  
- **PDF generation**: Easily convert data into PDF files and deliver them directly via Telegram.  
- **Session management**: Supports restart or exit options and cleans up per-user sessions automatically.

---

##  File Overview

| File | Purpose |
|------|---------|
| `bot.py` | Core bot logic using `python-telegram-bot`; handles user interactions, fetching, processing, and PDF delivery. |
| `mp_fetch_data.py` (or `mp_mining.py`) | Contains functions for logging into the mining site and fetching data. |
| `requirements.txt` | Lists dependencies required to run the bot in a virtual environment. |
| `.gitignore` | Specifies untracked files/folders (e.g., `venv`, logs, PDFs). |

---

##  Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/hideepakgupta2000/mp-mines_bot.git
   cd mp-mines_bot

2. **Create a virtual environment (venv)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Configure your bot token**
   You can just open bot.py and replace the placeholder BOT_TOKEN with your actual Telegram bot token.
   
6. **Install dependencies**
   python bot.py

