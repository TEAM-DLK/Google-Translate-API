import os
import zipfile
import logging
from googletrans import Translator
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize translator
translator = Translator()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Function to handle text messages
def translate_text(update: Update, context: CallbackContext):
    user_text = update.message.text
    translated_text = translator.translate(user_text, dest='en').text
    update.message.reply_text(f"Translated: {translated_text}")

# Function to handle ZIP file uploads
def handle_document(update: Update, context: CallbackContext):
    file = update.message.document
    if file.mime_type == "application/zip":
        file_id = file.file_id
        file_info = context.bot.get_file(file_id)
        file_path = f"{file.file_name}"

        file_info.download(file_path)
        update.message.reply_text(f"Received and saved: {file.file_name}")

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send me text to translate or a ZIP file.")

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
