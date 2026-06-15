import os

from config import (
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID
)

BOT_ENABLED = True

try:

    from telegram import Bot

    if not TELEGRAM_TOKEN:

        BOT_ENABLED = False

        bot = None

        print(
            "TELEGRAM_TOKEN missing"
        )

    else:

        bot = Bot(
            token=TELEGRAM_TOKEN
        )

        print(
            "Telegram Bot Initialized"
        )

except Exception as e:

    BOT_ENABLED = False

    bot = None

    print(
        f"Telegram Init Error: {e}"
    )


# ========================================
# SEND MESSAGE
# ========================================

async def send_message(text):

    if not BOT_ENABLED:

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
            f"Telegram Send Error: {e}"
        )


# ========================================
# SEND STATS
# ========================================

async def send_stats():

    try:

        from performance import (
            get_stats
        )

        stats = get_stats()

        await send_message(
            stats
        )

    except Exception as e:

        print(
            f"Stats Error: {e}"
        )