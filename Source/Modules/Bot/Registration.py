from Source.Modules.Bot.SubMenu import SubMenu
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from Source.Modules.Bot.Utility import *
from Source.Modules.Shared.Query import InsertUser
from Source.Modules.Bot.Stop import stop_after_registration


class Registration(SubMenu):

    def __init__(self):
        super().__init__()

        # conversation_batches = ["acquire_username", "acquire_email", "registration_done"]

        self.user_params = {
            "telegramID": 0,

            'acquire_username': "",

            "acquire_email": "",
        }

        self.INTRO_MESSAGES = {

            "acquire_username": "Digita l'username rispettando lo stardard Unipa con iniziali grandi.\n"
                                "Es: Massimo.Midiri03",

            "acquire_email": "Digita il tuo indirizzo mail",

        }

        self.KEYBOARDS = {

            "acquire_username": InlineKeyboardMarkup([[InlineKeyboardButton("❌ Annulla", callback_data='back_main_menu')]]),

            "acquire_email": InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Torna indietro", callback_data='register')]]),

        }

        self.ERROR_MESSAGES = {

            "acquire_username": "Hai digitato un username che non rispetta lo stardard Unipa, "
                                "riprova.\nEs: Massimo.Midiri03",

            "acquire_email": "Hai digitato un indirizzo mail non valido, riprova",
        }

    async def start_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE, query=None, current_batch: str = None):
        self.query = query
        self.current_batch = current_batch
        await query.edit_message_text(self.INTRO_MESSAGES[current_batch], reply_markup=self.KEYBOARDS[current_batch])

    async def forward_conversation(self, query, context: ContextTypes.DEFAULT_TYPE, current_batch: str):
        self.query = query
        self.current_batch = current_batch
        self.user_params[current_batch] = query.data
        await query.edit_message_text(self.INTRO_MESSAGES[self.current_batch], reply_markup=self.KEYBOARDS[current_batch])

    async def acquire_conversation_param(self, context: ContextTypes.DEFAULT_TYPE, previous_batch: str,
                                         current_batch: str, next_batch: str, chat_id: int, message_id: int,
                                         typed_string: str, flag: bool):
        if flag:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✔ Conferma", callback_data=next_batch)],
                                             [InlineKeyboardButton("🔙 Torna indietro", callback_data=previous_batch)]])
            query = self.query
            self.user_params[current_batch] = typed_string
            self.current_batch = current_batch
            self.user_params["telegramID"] = chat_id
            await query.edit_message_text(text=f"Hai scritto {typed_string}, confermi?", reply_markup=keyboard)
        else:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            query = self.query
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Torna indietro", callback_data=previous_batch)]])
            await query.edit_message_text(self.ERROR_MESSAGES[current_batch], reply_markup=keyboard)

    async def end_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
        await self.insert_user(context)
        buttons = [[InlineKeyboardButton("🔙 Ritorna al menu principale", callback_data='back_main_menu')]]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(text=f"{self.user_params['acquire_username']} "
                                           f"benvenut* in Vivere Agenda!",
                                      reply_markup=keyboard)
        context.user_data.pop("Registration")
        self.current_batch = ""
        await stop_after_registration(update, context)

    async def insert_user(self, context: ContextTypes.DEFAULT_TYPE):
        """Memorizza nel DB e avvisa gli admin"""
        InsertUser(idTelegram=str(self.user_params["telegramID"]),
                   username=self.user_params["acquire_username"],
                   email=self.user_params["acquire_email"],
                   isAdmin=False,
                   isVerified=False)
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("✔ Verifica",
                                   callback_data=f'instant_verify:{self.user_params["acquire_username"]}')],
             [InlineKeyboardButton("✖ Elimina",
                                   callback_data=f'instant_delete:{self.user_params["acquire_username"]}')]])

        # TODO: await context.bot.send_message(chat_id=GetIdGruppoTelegram(GetAuletta(self.user_params[
        #  "select_auletta"])), text=f'Ciao ragazzi, {self.user_params["acquire_username"]} si è appena registrato',
        #  reply_markup=keyboard)


