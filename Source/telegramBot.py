import logging
import pytz
from Modules.Shared.Configs import LoadConfigs, get_token
from Source.Modules.Bot.Utility import *
from Modules.Bot.Start import Start
from Source.Modules.Bot.Stop import stop_command
from Source.Modules.Bot.ActionRouting import handle_messages, button_callbacks

import datetime

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters
)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main() -> None:
    """Run the bot"""
    # Create the Application and pass the bot's token
    LoadConfigs()
    application = Application.builder().token(get_token()).build()

    application.add_handler(CommandHandler("start", Start().start_conversation))
    application.add_handler(CommandHandler("stop", stop_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    application.add_handler(CallbackQueryHandler(button_callbacks))

    # job_queue = application.job_queue

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
