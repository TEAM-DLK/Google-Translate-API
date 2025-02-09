import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
OWNER_ID = os.environ.get('OWNER_ID', '')
CHANNEL_LINK = os.environ.get('CHANNEL_LINK', 'https://t.me/your_channel')
GROUP_LINK = os.environ.get('GROUP_LINK', 'https://t.me/your_group')
REPO_LINK = os.environ.get('REPO_LINK', 'https://github.com/your_repo')