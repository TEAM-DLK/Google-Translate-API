import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from deep_translator import GoogleTranslator
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import config

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DeepAI API URL and Key
DEEP_AI_API_KEY = os.getenv("DEEP_AI_API_KEY")
DEEP_AI_API_URL = "https://api.deepai.org/api/text2img"

# Function to generate an image using DeepAI
def generate_image(description: str):
    headers = {'api-key': DEEP_AI_API_KEY}
    data = {'text': description}
    response = requests.post(DEEP_AI_API_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()["output_url"]
    else:
        return "Sorry, I couldn't generate the image. Please try again."

# Start command with inline buttons
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🌍 Select Language", callback_data="select_lang")],
        [
         InlineKeyboardButton("📢 Channel", url=config.CHANNEL_LINK),
         InlineKeyboardButton("💬 Group", url=config.GROUP_LINK),
        ],
        [InlineKeyboardButton("👤 Owner", url=f"tg://user?id={config.OWNER_ID}")],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_main_menu")],
        [InlineKeyboardButton("🎨 Generate Image", callback_data="generate_image")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to the Google Translate Bot! 🌍\nSelect a language or generate an image:", reply_markup=reply_markup)

# Image generation command
def generate_image_command(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.message.reply_text("Send me a description for the image you want to generate!")

# Handle the image description
def handle_image_description(update: Update, context: CallbackContext):
    description = update.message.text
    update.message.reply_text("Generating your image... Please wait.")

    image_url = generate_image(description)
    update.message.reply_text(f"Here is your generated image: {image_url}")

# Back to main menu handler
def back_to_main_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🌍 Select Language", callback_data="select_lang")],
        [
         InlineKeyboardButton("📢 Channel", url=config.CHANNEL_LINK),
         InlineKeyboardButton("💬 Group", url=config.GROUP_LINK),
        ],
        [InlineKeyboardButton("👤 Owner", url=f"tg://user?id={config.OWNER_ID}")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text("Welcome back to the main menu!", reply_markup=reply_markup)

# Scheduler for Good Morning and Good Night messages
def send_good_morning(context: CallbackContext):
    context.bot.send_message(chat_id=config.GROUP_LINK, text="Good Morning! 🌞 Have a great day ahead!")

def send_good_night(context: CallbackContext):
    context.bot.send_message(chat_id=config.GROUP_LINK, text="Good Night! 🌙 Sleep tight!")

# Setup scheduler for periodic messages
def setup_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_good_morning, 'cron', hour=12, minute=0)
    scheduler.add_job(send_good_night, 'cron', hour=22, minute=0)
    scheduler.start()

# Main function to start the bot
def main():
    updater = Updater(config.TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(generate_image_command, pattern="^generate_image$"))
    dp.add_handler(CallbackQueryHandler(back_to_main_menu, pattern="^back_to_main_menu$"))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_image_description))  # Handle image description

    # Start scheduler
    setup_scheduler()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()