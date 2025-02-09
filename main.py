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
    ALL_LANGUAGES = GoogleTranslator.get_supported_languages(as_dict=True)
except TypeError:
    translator = GoogleTranslator(source='auto', target='en')
    ALL_LANGUAGES = translator.get_supported_languages(as_dict=True)

# Configuration from environment variables
CONFIG = {
    "TOKEN": os.environ.get('TELEGRAM_BOT_TOKEN'),
    "OWNER_ID": os.environ.get('OWNER_ID'),
    "CHANNEL_LINK": os.environ.get('CHANNEL_LINK', '#'),
    "GROUP_LINK": os.environ.get('GROUP_LINK', '#'),
    "REPO_LINK": os.environ.get('REPO_LINK', '#'),
    "BOT_VERSION": "2.1"
}

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

# ================= HANDLER FUNCTIONS =================
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>" if user.first_name else "there"
    
    start_text = (
        f"👋 Hello {user_mention}!\n\n"
        "🌍 <b>I'm PolyGlot Bot - Your Multilingual Translation Assistant</b>\n\n"
        "✨ <b>Features:</b>\n"
        "- Instant text translation to 100+ languages\n"
        "- Automatic language detection\n"
        "- User-friendly interface with language menus\n"
        "- Support for rare dialects\n\n"
        "🚀 <b>How to use:</b>\n"
        "1. Choose target language below\n"
        "2. Send any text message\n"
        "3. Get instant translation!\n\n"
        "📚 <b>Popular Languages:</b>\n"
        "English, Spanish, French, German, Russian, Chinese, Japanese, Arabic, Hindi"
    )

    keyboard = [
        [
            InlineKeyboardButton("🌟 Popular", callback_data="popular_lang"),
            InlineKeyboardButton("🌐 All Languages", callback_data="all_lang_0")
        ],
        [
            InlineKeyboardButton("📢 Updates", url=CONFIG["CHANNEL_LINK"]),
            InlineKeyboardButton("💬 Support", url=CONFIG["GROUP_LINK"]),
        ],
        [
            InlineKeyboardButton("👨💻 Developer", url=f"tg://user?id={CONFIG['OWNER_ID']}"),
            InlineKeyboardButton("📦 Source Code", url=CONFIG["REPO_LINK"]),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        update.message.reply_text(
            text=start_text,
            reply_markup=reply_markup,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    else:
        update.callback_query.edit_message_text(
            text=start_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

def about(update: Update, context: CallbackContext):
    about_text = (
        f"🤖 <b>PolyGlot Bot v{CONFIG['BOT_VERSION']}</b>\n\n"
        "🔧 <b>Technical Specifications:</b>\n"
        "- Powered by Google Translate API\n"
        "- Supported languages: 100+\n"
        "- Response time: <1s\n"
        "- Uptime: 99.9%\n\n"
        "📌 <b>Core Features:</b>\n"
        "- Real-time text translation\n"
        "- Automatic language detection\n"
        "- Multi-language support\n"
        "- User session management\n\n"
        "👨💻 <b>Development Team:</b>\n"
        f"- Lead Developer: <a href='tg://user?id={CONFIG['OWNER_ID']}'>Contact</a>\n"
        "- Open Source Contributors: GitHub\n\n"
        "📜 <b>License:</b> MIT Open Source"
    )
    update.message.reply_text(about_text, parse_mode='HTML', disable_web_page_preview=True)

def show_popular_languages(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton(lang, callback_data=f"lang_{code}")]
        for lang, code in POPULAR_LANGUAGES.items()
    ]
    keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="start_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="🗺 <b>Popular Languages:</b>\nSelect your target language:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

def show_all_languages(update: Update, context: CallbackContext):
    query = update.callback_query
    page = int(query.data.split('_')[-1])
    
    all_langs = list(ALL_LANGUAGES.items())
    langs_per_page = 8
    total_pages = (len(all_langs) + langs_per_page - 1) // langs_per_page
    
    start_idx = page * langs_per_page
    end_idx = start_idx + langs_per_page
    current_langs = all_langs[start_idx:end_idx]

    keyboard = []
    for lang_name, lang_code in current_langs:
        keyboard.append([InlineKeyboardButton(lang_name, callback_data=f"lang_{lang_code}")])

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"all_lang_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"all_lang_{page+1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="start_menu")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"🌍 <b>Available Languages (Page {page+1}/{total_pages}):</b>",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

def language_selected(update: Update, context: CallbackContext):
    query = update.callback_query
    lang_code = query.data.split('_')[1]
    context.user_data["target_lang"] = lang_code
    lang_name = next((k for k, v in ALL_LANGUAGES.items() if v == lang_code), lang_code.upper())
    
    query.edit_message_text(
        text=f"✅ <b>Language Set:</b> {lang_name} ({lang_code.upper()})\n\n"
             "📩 Now send me any text to translate!\n"
             "🔄 Use /start to change language anytime.",
        parse_mode='HTML'
    )

def translate_text(update: Update, context: CallbackContext):
    user_text = update.message.text
    target_lang = context.user_data.get("target_lang", "en")
    
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
        response = (
            f"🌐 <b>Translation ({target_lang.upper()}):</b>\n\n"
            f"{translated}\n\n"
            f"🔁 <i>Translated from auto-detected source language</i>"
        )
        update.message.reply_text(response, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Translation error: {e}")
        update.message.reply_text(
            "❌ <b>Translation Failed</b>\n"
            "Please try again later or check if the text is valid.",
            parse_mode='HTML'
        )

# ================= MAIN APPLICATION =================
def main():
    if not CONFIG["TOKEN"]:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return

    updater = Updater(CONFIG["TOKEN"])
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('about', about))

    # Callback handlers
    dp.add_handler(CallbackQueryHandler(show_popular_languages, pattern='^popular_lang$'))
    dp.add_handler(CallbackQueryHandler(show_all_languages, pattern='^all_lang_'))
    dp.add_handler(CallbackQueryHandler(language_selected, pattern='^lang_'))
    dp.add_handler(CallbackQueryHandler(start, pattern='^start_menu$'))

    # Message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_text))

    # Start bot
    updater.start_polling()
    logger.info("Bot is now running...")
    updater.idle()

if __name__ == '__main__':
    main()