import os
from telegram import Update, Application
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from typing import Final


TOKEN: Final = "your_bot_token_here"
BOT_USERNAME: Final = "@anamenotusedyetbot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me. I am Anamenotusedyetbot!')

def handle_response(text: str) -> str:
    text = text.lower()
  
    if "hi" in text:
            return "Hey there!"
    
        elif "how are you" in text:
            return "I am good."
    
        else:
            return "I do not understand what you wrote."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text = str = update.message.text

    print(f'User ({update.message.chat.id})in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:   
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
        return
    else:
        response: str = handle_response(text)
    
    print('Bot:', response)
    await update.message.reply_text(response)



if __name__ == '__main__':
    print('Starting bot...')
    app =  Application.builder().token(TOKEN).build()

# Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    # application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(CommandHandler("custom", custom_command))
    
    # Message handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
  
    # Errors
    # app.add_error_handler(error)
    # Polls 
    print('Polling...')
    app.run_polling(poll_interval=5)
