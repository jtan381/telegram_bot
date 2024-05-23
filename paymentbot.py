import datetime
import os
from dotenv import load_dotenv
from telegram import LabeledPrice
from telegram.ext import PreCheckoutQueryHandler, CallbackContext
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, Application, ConversationHandler, CallbackQueryHandler, Updater
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,
                      InlineKeyboardButton, InlineKeyboardMarkup)
# from telegram.ext.messagehandler import MessageHandler
# from telegram.ext.updater import Updater
# from telegram.update import Update

# from database import get_collection
# from utils import print_col


load_dotenv()
GCP_PROJECT_ID = os.getenv('TOKEN')
SERVICE_ACCOUNT_FILE = os.getenv('BOT_USERNAME')
BOT_KEY = os.getenv('TOKEN')
STRIPE_TOKEN = os.getenv('STRIPE_TOKEN')
PRICE = 500

async def start(update: Update, context: CallbackContext):
    welcome_message = "Welcome to this bot!"
    await update.message.reply_text(welcome_message, parse_mode="html")

async def donate(update: Update, context: CallbackContext):
    out= await context.bot.send_invoice(
        chat_id=update.message.chat_id,
        title="Test donation",
        description="Give money here.",
        payload="test",
        provider_token="284685063:TEST:MWRhOGJhODIyMGQ2",
        currency="usd",
        prices=[LabeledPrice("Give",500)],
        need_name=False,
    )

async def pre_checkout_handler(update: Update, context: CallbackContext):
    """https://core.telegram.org/bots/api#answerprecheckoutquery"""
    query = update.pre_checkout_query
    await query.answer(ok=True)


async def successful_payment_callback(update: Update, context):
    # col = get_collection()
    receipt = update.message.successful_payment
    # col.insert_one({"telegram_uid": update.message.chat.username, 
    #                "donated_amount": receipt.total_amount,
    #                "currency": receipt.currency,
    #                "datetime": str(datetime.datetime.now())})
    # print_col(col)
    await update.message.reply_text("Thank you for your purchase!")

async def handle_update(update, context):
  # Check if the update matches the SuccessfulPayment filter
  if filters.SuccessfulPayment.check_update(update):
    successful_payment_callback(update, context)  # Pass the update object
  # Handle other updates here
  # ...

async def uid(update: Update, context: CallbackContext):
    uid = update.message.chat.username
    await update.message.reply_text(f"Your uid is {uid}", parse_mode="html")

async def unknown_text(update: Update, context: CallbackContext):
    await update.message.reply_text(f"If you need support please contact example@email.com.")

def _add_handlers(updater):
    updater.add_handler(CommandHandler("start", start))
    updater.add_handler(CommandHandler("give", donate))
    updater.add_handler(PreCheckoutQueryHandler(pre_checkout_handler))
    updater.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    updater.add_handler(CommandHandler("uid", uid))
    # updater.add_handler(MessageHandler(filters.TEXT, unknown_text))
    updater.add_handler(MessageHandler(filters.TEXT, handle_update))

if __name__ == "__main__":
    app =  Application.builder().token(BOT_KEY).build()
    # updater = Updater(BOT_KEY, use_context=True)
    _add_handlers(app)
    print("starting to poll...")
    app.run_polling()