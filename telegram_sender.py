from telegram import Bot

from config import (
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID
)

bot = Bot(
    token=TELEGRAM_TOKEN
)

async def send_message(text):

    try:

        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text
        )

        print("Telegram message sent")

    except Exception as e:

        print(
            f"Telegram Error: {e}"
        )