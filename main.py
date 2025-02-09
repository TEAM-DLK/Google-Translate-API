import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

# Initialize environment
load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Handle different deep-translator versions
try:
    # Try new version class method
    ALL_LANGUAGES = GoogleTranslator.get_supported_languages(as_dict=True)
except TypeError:
    # Fallback to old version instance method
    translator = GoogleTranslator(source='auto', target='en')
    ALL_LANGUAGES = translator.get_supported_languages(as_dict=True)

# Configuration from environment variables
CONFIG = {
    "TOKEN": os.environ.get('TELEGRAM_BOT_TOKEN'),
    "OWNER_ID": os.environ.get('OWNER_ID'),
    "CHANNEL_LINK": os.environ.get('CHANNEL_LINK', '#'),
    "GROUP_LINK": os.environ.get('GROUP_LINK', '#'),
    "REPO_LINK": os.environ.get('REPO_LINK', '#')
}

def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("🌍 Popular", callback_data="popular_lang"),
            InlineKeyboardButton("🌐 All Languages", callback_data="all_lang_0")
        ],
        [
            InlineKeyboardButton("📢 Channel", url=CONFIG["CHANNEL_LINK"]),
            InlineKeyboardButton("💬 Group", url=CONFIG["GROUP_LINK"]),
        ],
        [
            InlineKeyboardButton("👤 Owner", url=f"tg://user?id={CONFIG['OWNER_ID']}"),
            InlineKeyboardButton("📁 Repo", url=CONFIG["REPO_LINK"]),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        update.message.reply_text("🌍 Translate Bot - Select Language:", reply_markup=reply_markup)
    else:
        update.callback_query.edit_message_text("🌍 Translate Bot - Select Language:", reply_markup=reply_markup)

# Rest of the handlers from previous implementation
# [Include the show_popular_languages, show_all_languages, 
#  language_selected, and translate_text functions here]

def main():
    if not CONFIG["TOKEN"]:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return

    updater = Updater(CONFIG["TOKEN"])
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(show_popular_languages, pattern='^popular_lang$'))
    dp.add_handler(CallbackQueryHandler(show_all_languages, pattern='^all_lang_'))
    dp.add_handler(CallbackQueryHandler(language_selected, pattern='^lang_'))
    dp.add_handler(CallbackQueryHandler(start, pattern='^start_menu$'))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_text))

    updater.start_polling()
    logger.info("Bot started successfully")
    updater.idle()

if __name__ == '__main__':
    main()