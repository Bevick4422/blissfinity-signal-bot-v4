from telegram import Bot

from config import (
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID
)

# ==========================
# TELEGRAM BOT
# ==========================

bot = None

if TELEGRAM_TOKEN:

    try:

        bot = Bot(
            token=TELEGRAM_TOKEN
        )

        print(
            "Telegram Bot Initialized"
        )

    except Exception as e:

        print(
            f"Telegram Init Error: {e}"
        )

else:

    print(
        "TELEGRAM_TOKEN missing"
    )


# ==========================
# SEND MESSAGE
# ==========================

async def send_message(text):

    if bot is None:

        print(
            "Telegram disabled"
        )

        return

    try:

        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text
        )

        print(
            "Telegram message sent"
        )

    except Exception as e:

        print(
            f"Telegram Error: {e}"
        )