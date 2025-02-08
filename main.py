import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send me text to translate or a ZIP file.")

# Text translation handler
def translate_text(update: Update, context: CallbackContext):
    user_text = update.message.text
    translated_text = GoogleTranslator(source='auto', target='en').translate(user_text)
    update.message.reply_text(f"Translated: {translated_text}")

# Handle ZIP file uploads
def handle_document(update: Update, context: CallbackContext):
    file = update.message.document
    if file.mime_type == "application/zip":
        file_id = file.file_id
        file_info = context.bot.get_file(file_id)
        file_path = f"{file.file_name}"

        file_info.download(file_path)
        update.message.reply_text(f"Received and saved: {file.file_name}")

# Main function to start the bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_text))
    dp.add_handler(MessageHandler(Filters.document.mime_type("application/zip"), handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()