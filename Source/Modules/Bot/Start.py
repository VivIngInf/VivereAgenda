import os
import random
from datetime import datetime
from telegram import Update, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
# from Modules.Bot.Utility import *
from Source.Modules.Bot.SubMenu import SubMenu


from Source.Modules.Bot.ConversationManager import ConversationManager


class Start(SubMenu):

    def __init__(self):
        super().__init__()

    async def start_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        text = "📅 Benvenuto su Vivere Agenda! 📅\n\n"

        main_menu_keyboard = []
        classes_to_generate = {"ConversationManager": ConversationManager()}

        # ----- BUTTONS -----

        admin = InlineKeyboardButton(text="👨🏽‍🔧 ADMIN MENU 🏽‍🔧", callback_data="main_admin")
        stop = InlineKeyboardButton(text="🛑 STOP 🛑", callback_data="stop")

        # -------------------

        # Eventualmente proteggere il DB da eventuali SQL Injection
        # che darebbe accesso a tutte le funzioni di Admin
        username = update.message.from_user.username
        text += f"👋🏽 {username}, è un piacere rivederti! 👋🏽\nChe vuoi fare? 👀"

        main_menu_keyboard.append([admin])
        main_menu_keyboard.append([stop])

        keyboard = InlineKeyboardMarkup(main_menu_keyboard)

        # Check if it is first start or not
        if "first_start" not in context.user_data:
            initial_message = await update.message.reply_text(text=text, reply_markup=keyboard)
            context.user_data['first_start'] = True
            context.user_data['initial_message'] = initial_message
            for key, value in classes_to_generate.items():
                context.user_data[key] = value
        else:
            await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
