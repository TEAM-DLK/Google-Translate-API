```markdown
# 🌍 PolyGlot Bot - Telegram Translation Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/TEAM-DLK/Google-Translate-API)

A smart Telegram bot powered by Google Translate API that provides real-time translations in 100+ languages. Supports inline mentions, language detection, and user-friendly interfaces.

![Bot Demo](https://via.placeholder.com/800x400.png?text=https://t.me/DLKGTBOT)

## ✨ Features

- **100+ Languages**: Support for major languages and rare dialects
- **Auto-Detection**: Automatic source language recognition
- **User Sessions**: Remembers selected target language
- **Pagination**: Easy navigation through language lists
- **Multi-Platform**: Ready for Heroku deployment
- **Open Source**: MIT licensed

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Telegram Bot Token ([Get from @BotFather](https://t.me/BotFather))
- Heroku account (for deployment)

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/TEAM-DLK/Google-Translate-API.git
cd Google-Translate-API
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```env
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
OWNER_ID=YOUR_TELEGRAM_ID
```

4. Run the bot:
```bash
python main.py
```

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Show main menu with language options |
| `/about` | Display bot information and version |


## 🛠 Configuration

### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Your Telegram bot token |
| `OWNER_ID` | Yes | Your Telegram user ID |
| `CHANNEL_LINK` | No | Updates channel URL |
| `GROUP_LINK` | No | Support group URL |
| `REPO_LINK` | No | GitHub repository link |

## 🌎 Deployment

### Heroku Deployment
1. Click the [Deploy to Heroku](https://heroku.com/deploy) button
2. Set required config vars:
   - `TELEGRAM_BOT_TOKEN`
   - `OWNER_ID`
3. Deploy!

### Manual Heroku Setup
```bash
# Create new app
heroku create your-app-name

# Set config vars
heroku config:set TELEGRAM_BOT_TOKEN=your_token OWNER_ID=your_id

# Deploy
git push heroku main

# Check logs
heroku logs --tail
```

## 📚 Usage Examples

1. **Private Chat**:
   ```
   User: Hello world!
   Bot: 🌐 Translation (ES): Hola mundo!
   ```



2. **Language Selection**:
   ```
   User: /start
   Bot: Shows language selection keyboard
   ```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

[Code of Conduct](CODE_OF_CONDUCT.md)

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

Developer: [@達南佳亞](https://t.me/iiiIiiiAiiiMiii)  
Project Link: [GitHub Repository](https://github.com/TEAM-DLK/Google-Translate-API)
```
