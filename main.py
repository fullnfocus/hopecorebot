import os
import random
import requests

from keep_running import keep_running
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# folder for images
IMAGE_FOLDER = "hopecore_img"
all_images = [  # list of all image file paths in the folder
    os.path.join(IMAGE_FOLDER, img) for img in os.listdir(IMAGE_FOLDER)
    if img.lower().endswith(('.jpg', '.webp'))
]

BOT_TOKEN = "7795781192:AAGhh8EQJAY0eJwvyb0iuPSmGliAnNRmwC8"


def start(update: Update, context: CallbackContext):
    welcome = "hi bro 🌸\ni’m your hopecore bot\nclick below when you’re ready"
    buttons = [[
        InlineKeyboardButton("💌 hopeful quote", callback_data='quote')
    ], [InlineKeyboardButton("🖼️ peaceful image", callback_data='image')],
               [
                   InlineKeyboardButton("i need something uplifting",
                                        callback_data='support')
               ]]
    # send message with buttons
    update.message.reply_text(welcome,
                              reply_markup=InlineKeyboardMarkup(buttons))


# on button press
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'quote':
        quote = get_quote()  # gets quote from zenquote api
        query.edit_message_text(quote)  # print
    elif query.data == 'image':
        used = context.user_data.get('used_images', [])
        available = list(set(all_images) - set(used))

        # reset if all used
        if not available:
            used = []
            available = all_images.copy()

        img_path = random.choice(available)
        used.append(img_path)
        context.user_data['used_images'] = used

        context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=open(img_path, 'rb'),  # send image
            caption="a moment of peace for your heart 🌸")
    elif query.data == 'support':
        query.edit_message_text(
            "i’m here. you are loved. you are enough 💗")  # print


# bot starter
def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()


# gets quote from zenquote api
def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        data = response.json()
        quote = f"“{data[0]['q']}”\n– {data[0]['a']}"
        return quote
    except:
        # if api fails
        return "“you are stronger than you know.” 🕊️"


if __name__ == '__main__':
    keep_running()
    main()
