import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Bot configuration settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
GROUP_LINK = os.getenv("GROUP_LINK")
CHANNEL_LINK = os.getenv("CHANNEL_LINK")