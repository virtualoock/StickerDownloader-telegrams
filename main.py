import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = Updater(token=TOKEN, use_context=True).bot

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Send me a sticker, and I'll try to download it for you.")

def download_sticker(update: Update, context: CallbackContext) -> None:
    sticker = update.message.sticker

    file_id = sticker.file_id
    file_path = bot.get_file(file_id).file_path
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    # Download the sticker file
    response = requests.get(file_url)
    if response.status_code == 200:
        # Save the sticker file
        with open(f"{file_id}.webp", "wb") as file:
            file.write(response.content)
        
        update.message.reply_text("Sticker downloaded successfully!")
    else:
        update.message.reply_text("Failed to download the sticker.")

if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.sticker, download_sticker))

    updater.start_polling()
    updater.idle()
