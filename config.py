import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
OWNER_ID = os.environ.get('OWNER_ID', '5917900136')
CHANNEL_LINK = os.environ.get('CHANNEL_LINK', 'https://t.me/DLKDevelopers')
GROUP_LINK = os.environ.get('GROUP_LINK', 'https://t.me/DevDLK')
REPO_LINK = os.environ.get('REPO_LINK', 'https://github.com/TEAM-DLK/Google-Translate-API')