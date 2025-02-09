import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from deep_translator import GoogleTranslator
import config  # Import config.py

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of supported languages (including Sinhala)
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Russian": "ru",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Hindi": "hi",
    "Japanese": "ja",
    "Sinhala (සිංහල)": "si"  # Added Sinhala
}

# Start command with inline buttons
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🌍 Select Language", callback_data="select_lang")],
        [
         InlineKeyboardButton("📢 Channel", url=config.CHANNEL_LINK),
         InlineKeyboardButton("💬 Group", url=config.GROUP_LINK),
        ],
        [InlineKeyboardButton("👤 Owner", url=f"tg://user?id={config.OWNER_ID}")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to the Google Translate Bot! 🌍\nSelect a language below:", reply_markup=reply_markup)

# Language selection handler
def select_language(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(lang, callback_data=f"lang_{code}")] for lang, code in LANGUAGES.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text("Select the language to translate into:", reply_markup=reply_markup)

# Text translation handler
def translate_text(update: Update, context: CallbackContext):
    user_text = update.message.text
    user_id = update.message.from_user.id

    # Check if user has chosen a language before
    target_lang = context.user_data.get("language", "en")

    translated_text = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
    update.message.reply_text(f"Translated ({target_lang}): {translated_text}")

# Handle language button click
def language_selected(update: Update, context: CallbackContext):
    query = update.callback_query
    selected_lang_code = query.data.split("_")[1]
    
    context.user_data["language"] = selected_lang_code
    query.message.reply_text(f"✅ Language set to {selected_lang_code.upper()}\nNow send me text to translate!")

# Main function to start the bot
def main():
    updater = Updater(config.TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(select_language, pattern="^select_lang$"))
    dp.add_handler(CallbackQueryHandler(language_selected, pattern="^lang_"))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_text))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()