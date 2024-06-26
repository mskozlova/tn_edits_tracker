import os
import time

import telebot

from bot.structure import create_bot
from database.ydb_settings import get_ydb_pool
from logs import logger
from telegram import send_messages
from tracker import get_updates, save_updates

YDB_ENDPOINT = os.getenv("YDB_ENDPOINT")
YDB_DATABASE = os.getenv("YDB_DATABASE")
TG_TOKEN = os.getenv("TG_TOKEN")
TG_SLEEP_S = 0.5


def cron_handler(event, _):
    logger.debug("Started execution")

    pool = get_ydb_pool(YDB_ENDPOINT, YDB_DATABASE)
    updates = get_updates(pool)

    logger.debug(f"Notifying: {len(updates)} updates")

    notified_updates = []
    for update in updates:
        status_code = send_messages(
            user_chat_id=update.db_entry["chat_id"],
            status=update,
            token=TG_TOKEN,
            sleep_s=TG_SLEEP_S
        )
        if status_code == 200:
            notified_updates.append(update)
        time.sleep(TG_SLEEP_S)

    logger.debug(f"Notified: {len(notified_updates)} updates")
    save_updates(pool, notified_updates)

    logger.debug("Finished execution")

    return {
        "statusCode": 200,
        "body": "!",
    }


def chat_handler(event, _):
    logger.debug(f"New chat event: {event}")

    pool = get_ydb_pool(YDB_ENDPOINT, YDB_DATABASE)
    bot = create_bot(TG_TOKEN, pool)

    message = telebot.types.Update.de_json(event["body"])

    bot.process_new_updates([message])

    return {
        "statusCode": 200,
        "body": "!",
    }
