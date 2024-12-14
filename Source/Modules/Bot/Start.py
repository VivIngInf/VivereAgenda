import os
import random
from datetime import datetime
from telegram import Update, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from Source.Modules.Bot.Utility import *
from Source.Modules.Bot.SubMenu import SubMenu
from Source.Modules.Shared.Query import CheckUserExists, GetIsVerified, GetIsAdmin, GetUsername
from Source.Modules.Bot.Registration import Registration


from Source.Modules.Bot.ConversationManager import ConversationManager


class Start(SubMenu):

    def __init__(self):
        super().__init__()

    async def start_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        text = "📅 Benvenuto su Vivere Agenda! 📅\n\n"

        main_menu_keyboard = []
        classes_to_generate = {"ConversationManager": ConversationManager()}

        # ----- BUTTONS -----

        register = InlineKeyboardButton(text="📝 REGISTRATI 📝", callback_data="register")
        info = InlineKeyboardButton(text="❓ INFO ❓", callback_data="info")
        removeUser = InlineKeyboardButton(text="❌ ELIMINA RICHIESTA ❌",
                                          callback_data="delete_request_registration_account")
        stop = InlineKeyboardButton(text="🛑 STOP 🛑", callback_data="stop")

        # -------------------

        if (not CheckUserExists(idTelegram=update.effective_chat.id)):  # Non sei ancora registrato
            text = "👀 Hey, è la prima volta che visiti Vivere Agenda? 👀\n🔻 Registrati premendo il bottone sottostante! 🔻"

            classes_to_generate |= {"Registration": Registration()}
            main_menu_keyboard.append([register])
            main_menu_keyboard.append([stop])

        elif (not GetIsVerified(idTelegram=update.effective_chat.id)):  # Il tuo account non è attivato
            text = ("🛑 Ancora non ti è stato attivato l'account! 🛑\nAttendi oppure contatta un admin:\n"
                    "@Daniele_Susino --- @AndriDepis")

            main_menu_keyboard.append([info])
            main_menu_keyboard.append([removeUser])
            main_menu_keyboard.append([stop])

        elif (not GetIsAdmin(idTelegram=update.effective_chat.id)):  # Non sei amministratore
            username = GetUsername(idTelegram=update.effective_chat.id)
            text = f"👋🏽 {username}, è un piacere rivederti! 👋🏽\nChe vuoi fare? 👀"

            main_menu_keyboard.append([info])
            main_menu_keyboard.append([stop])

        else:  # Sei amministratore
            # Eventualmente proteggere il DB da eventuali SQL Injection
            # che darebbe accesso a tutte le funzioni di Admin
            username = GetUsername(idTelegram=update.effective_chat.id)
            text = f"👋🏽 {username}, è un piacere rivederti! 👋🏽\nChe vuoi fare? 👀"

            # classes_to_generate |= {"Admin": AdminMenu(), "AddAdmin": AddAdmin(), "RemoveAdmin": RemoveAdmin()}

            # main_menu_keyboard.append([saldo])
            # main_menu_keyboard.append([storico])
            # main_menu_keyboard.append([ricarica])
            # main_menu_keyboard.append([admin])
            # main_menu_keyboard.append([storage])
            main_menu_keyboard.append([info])
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
