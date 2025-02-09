import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from deep_translator import GoogleTranslator
import config  # Make sure to create config.py with your credentials

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fetch all supported languages dynamically
ALL_LANGUAGES = GoogleTranslator.get_supported_languages(as_dict=True)
POPULAR_LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Russian": "ru",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Hindi": "hi",
    "Japanese": "ja",
    "Sinhala": "si"
}

# Start command with main menu
def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("🌍 Popular Languages", callback_data="popular_lang"),
            InlineKeyboardButton("🌐 All Languages", callback_data="all_lang_0")
        ],
        [
            InlineKeyboardButton("📢 Channel", url=config.CHANNEL_LINK),
            InlineKeyboardButton("💬 Group", url=config.GROUP_LINK),
        ],
        [
            InlineKeyboardButton("👤 Owner", url=f"tg://user?id={config.OWNER_ID}"),
            InlineKeyboardButton("📁 Repository", url=config.REPO_LINK),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        update.message.reply_text("Welcome to Google Translate Bot! 🌍\nSelect a language:", reply_markup=reply_markup)
    else:
        update.callback_query.message.edit_text("Welcome to Google Translate Bot! 🌍\nSelect a language:", reply_markup=reply_markup)

# Show popular languages
def show_popular_languages(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton(lang, callback_data=f"lang_{code}")] for lang, code in POPULAR_LANGUAGES.items()]
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="start_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Popular Languages:", reply_markup=reply_markup)

# Show all languages with pagination
def show_all_languages(update: Update, context: CallbackContext):
    query = update.callback_query
    page = int(query.data.split('_')[-1])
    
    all_langs = list(ALL_LANGUAGES.items())
    langs_per_page = 10
    total_pages = (len(all_langs) + langs_per_page - 1) // langs_per_page
    
    start_idx = page * langs_per_page
    end_idx = start_idx + langs_per_page
    current_langs = all_langs[start_idx:end_idx]

    keyboard = []
    for lang_name, lang_code in current_langs:
        keyboard.append([InlineKeyboardButton(lang_name, callback_data=f"lang_{lang_code}")])

    # Navigation buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"all_lang_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"all_lang_{page+1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="start_menu")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        f"🌐 Available Languages (Page {page+1}/{total_pages}):",
        reply_markup=reply_markup
    )

# Handle language selection
def language_selected(update: Update, context: CallbackContext):
    query = update.callback_query
    lang_code = query.data.split('_')[1]
    
    context.user_data["target_lang"] = lang_code
    query.answer()
    query.edit_message_text(f"✅ Language set to {ALL_LANGUAGES[lang_code]} ({lang_code.upper()})\nSend me text to translate!")

# Handle text translation
def translate_text(update: Update, context: CallbackContext):
    user_text = update.message.text
    target_lang = context.user_data.get("target_lang", "en")
    
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
        update.message.reply_text(f"🌐 Translation ({target_lang.upper()}):\n\n{translated}")
    except Exception as e:
        logger.error(f"Translation error: {e}")
        update.message.reply_text("❌ Translation failed. Please try again later.")

# Main function
def main():
    updater = Updater(config.TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(show_popular_languages, pattern='^popular_lang$'))
    dp.add_handler(CallbackQueryHandler(show_all_languages, pattern='^all_lang_'))
    dp.add_handler(CallbackQueryHandler(language_selected, pattern='^lang_'))
    dp.add_handler(CallbackQueryHandler(start, pattern='^start_menu$'))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_text))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()