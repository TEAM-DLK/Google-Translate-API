import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OWNER_ID = os.getenv('OWNER_ID')
CHANNEL_LINK = os.getenv('CHANNEL_LINK')
GROUP_LINK = os.getenv('GROUP_LINK')
