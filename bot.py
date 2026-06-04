import os
import sys
import logging
from telebot import TeleBot, types

# Setup logging to view outputs natively in Render logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Retrieve environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    logger.critical("CRITICAL ERROR: TELEGRAM_BOT_TOKEN variable is missing!")
    sys.exit("Exiting due to missing bot token configuration.")

# Initialize Bot
bot = TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **Welcome to TextForge Utility Bot!**\n\n"
        "I am a zero-dependency text tool processing items purely in-memory.\n\n"
        "**Available Commands:**\n"
        "🔹 `/upper <text>` - Transform text to ALL CAPS\n"
        "🔹 `/lower <text>` - Transform text to lowercase\n"
        "🔹 `/stats <text>` - Count characters, words, and lines\n"
        "🔹 `/reverse <text>` - Reverse your text string\n"
        "🔹 `/code <text>` - Wrap your text inside a markdown code block\n\n"
        "Simply type a command followed by your message!"
    )
    # Using markdown parsing natively for clear presentation
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['upper'])
def handle_upper(message):
    text_arg = message.text.split(maxsplit=1)
    if len(text_arg) > 1:
        bot.reply_to(message, text_arg[1].upper())
    else:
        bot.reply_to(message, "❌ Please provide text. Example: `/upper hello world`", parse_mode="Markdown")

@bot.message_handler(commands=['lower'])
def handle_lower(message):
    text_arg = message.text.split(maxsplit=1)
    if len(text_arg) > 1:
        bot.reply_to(message, text_arg[1].lower())
    else:
        bot.reply_to(message, "❌ Please provide text. Example: `/lower HELLO WORLD`", parse_mode="Markdown")

@bot.message_handler(commands=['reverse'])
def handle_reverse(message):
    text_arg = message.text.split(maxsplit=1)
    if len(text_arg) > 1:
        bot.reply_to(message, text_arg[1][::-1])
    else:
        bot.reply_to(message, "❌ Please provide text. Example: `/reverse text`", parse_mode="Markdown")

@bot.message_handler(commands=['stats'])
def handle_stats(message):
    text_arg = message.text.split(maxsplit=1)
    if len(text_arg) > 1:
        target = text_arg[1]
        chars = len(target)
        words = len(target.split())
        lines = len(target.splitlines())
        
        response = (
            f"📊 **Text Analytics:**\n"
            f"▪️ **Characters:** {chars}\n"
            f"▪️ **Words:** {words}\n"
            f"▪️ **Lines:** {lines}"
        )
        bot.reply_to(message, response, parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ Please provide text. Example: `/stats test content`", parse_mode="Markdown")

@bot.message_handler(commands=['code'])
def handle_code(message):
    text_arg = message.text.split(maxsplit=1)
    if len(text_arg) > 1:
        escaped_code = f"```\n{text_arg[1]}\n```"
        bot.reply_to(message, escaped_code, parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ Please provide text. Example: `/code print('hello')`", parse_mode="Markdown")

# Fallback echo behavior for text sent without explicit commands
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    fallback_prompt = "💡 Send me a specific command like `/upper your text` or type `/help` to see what I can do!"
    bot.reply_to(message, fallback_prompt, parse_mode="Markdown")

if __name__ == "__main__":
    logger.info("Starting Telegram Bot with Long Polling via Render Background Worker...")
    try:
        # non_stop keeps it running even if Telegram API times out momentarily
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        logger.error(f"An error occurred during polling execution: {e}")
