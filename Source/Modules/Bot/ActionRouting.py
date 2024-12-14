from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler

from Source.Modules.Bot.Stop import stop, stop_to_restart_again
from Source.Modules.Bot.Start import Start
from Source.Modules.Bot.UserInfo import Info
from Source.Modules.Bot.Utility import *
from Source.Modules.Shared.Query import RemoveUser

import re


async def button_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Every time a button is pressed"""

    query = update.callback_query

    if "ConversationManager" not in context.user_data:
        message_id = query.message.message_id
        chat_id = query.message.chat_id
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Il Bot si è riavviato per aggiornarsi 😃.\nPremi /start e ricominciamooo!! 😊"
        )
        return

    if "first_start" in context.user_data:
        context.user_data['first_start'] = False

    # active_conversation = context.user_data["ConversationManager"].get_active_conversation()
    # current_batch = context.user_data["ConversationManager"].get_current_conversation_batch(context)
    # print("##################")
    # print(active_conversation, current_batch)
    # print("##################")

    match query.data:

        case 'back_main_menu':
            delete_all_conversations(context)
            await Start().start_conversation(update, context)

        case 'stop':
            delete_all_conversations_and_manager(context)
            await stop(update, context)

        case "info":
            await Info(update, context)

        case "delete_request_registration_account":
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("✔ Conferma",
                                       callback_data='remove_and_restart_registration_again')],
                 [InlineKeyboardButton("❌ Annulla",
                                       callback_data='back_main_menu')]])
            await query.edit_message_text(
                f"Sei sicuro di voler annullare la registrazione? Ti perderai tutti i nostri eventi 😤",
                reply_markup=keyboard)

        case "remove_and_restart_registration_again":
            RemoveUser(str(query.from_user.id))
            delete_all_conversations_and_manager(context)
            await stop_to_restart_again(update, context)

            ##### REGISTRATION #####

        case "register":
            context.user_data["ConversationManager"].set_active_conversation("Registration")
            await context.user_data["Registration"].start_conversation(update=None, context=context, query=query,
                                                                       current_batch="acquire_username")

        case "acquire_email":
            await context.user_data["Registration"].forward_conversation(query, context, current_batch="acquire_email")

        case "registration_done":
            await context.user_data["Registration"].end_conversation(update=update, context=context, query=query)

        # ----- ADMIN MENU -----

        case "main_admin":
            delete_all_conversations(context)
            # TODO

        case _:
            pass


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Every time something is typed"""
    active_conversation = context.user_data["ConversationManager"].get_active_conversation()
    current_batch = context.user_data["ConversationManager"].get_current_conversation_batch(context)

    # print("##################")
    # print(active_conversation, current_batch)
    # print("##################")

    conversation_id = safe_hash_name(active_conversation, current_batch)

    if conversation_id == ACQUIRE_USERNAME_REGISTRATION:
        username = update.message.text
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        valid_username = check_regex_username(username)
        await context.user_data["Registration"].acquire_conversation_param(context,
                                                                           previous_batch="register",
                                                                           current_batch="acquire_username",
                                                                           next_batch="acquire_email",
                                                                           chat_id=chat_id,
                                                                           message_id=message_id,
                                                                           typed_string=username,
                                                                           flag=valid_username)
    elif conversation_id == ACQUIRE_EMAIL_REGISTRATION:
        email = update.message.text
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        valid_email = check_mail(email)
        await context.user_data["Registration"].acquire_conversation_param(context,
                                                                           previous_batch="register",
                                                                           current_batch="acquire_email",
                                                                           next_batch="registration_done",
                                                                           chat_id=chat_id,
                                                                           message_id=message_id,
                                                                           typed_string=email,
                                                                           flag=valid_email)
    else:
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)



def delete_all_conversations(context: ContextTypes.DEFAULT_TYPE):
    """Every time user goes to main menu, the conversation manager will be empty automatically"""
    context.user_data["ConversationManager"].set_active_conversation('')


def delete_all_conversations_and_manager(context: ContextTypes.DEFAULT_TYPE):
    """User for stop the Bot"""
    for _class in CONVERSATION_CLASSES:
        if _class in context.user_data:
            context.user_data.pop(_class)


def check_regex_username(username: str) -> bool:
    """Controlla se l'username dell'utente rispetta lo standard Unipa 'Nome.Cognome{int}{int}' """
    pattern = r"^[A-Z][a-z-A-Z]+\.[A-Z][a-z-A-Z]+(([1-9][1-9])|0[1-9]|[1-9]0)?$"
    return re.match(pattern, username)


def check_mail(email: str) -> bool:
    """Controlla se l'email inserita è valida"""
    from validate_email import validate_email

    return validate_email(email, check_mx=True)
