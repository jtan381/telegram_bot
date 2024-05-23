from dotenv import load_dotenv
import os
import logging
import random
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, Application, ConversationHandler, CallbackQueryHandler
from typing import Final

load_dotenv()
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN: Final = os.getenv('TOKEN') 
BOT_USERNAME: Final = os.getenv('BOT_USERNAME')

GAMETYPE, FIRSTTURN, RESULT= range(3)


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

async def startgame_command(update: Update, context: ContextTypes.DEFAULT_TYPE) ->int :
    # Define inline buttons for car color selection
    keyboard = [
        [InlineKeyboardButton('TIC TAC TOE', callback_data='0')],
        [InlineKeyboardButton('X-Game', callback_data='1')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('<b>Please choose a game:</b>', parse_mode='HTML', reply_markup=reply_markup)

    return GAMETYPE

async def playerorder_command(update: Update, context: ContextTypes.DEFAULT_TYPE) ->int:
    query = update.callback_query
    await query.answer()
    context.user_data['game_type'] = query.data

    # Define inline buttons for car color selection
    keyboard = [
        [InlineKeyboardButton('First', callback_data="0")],
        [InlineKeyboardButton('Second', callback_data="1")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text('<b>Would you like to go first or second?</b>', parse_mode='HTML', reply_markup=reply_markup)

    return FIRSTTURN

async def initmove_command(update: Update, context: ContextTypes.DEFAULT_TYPE) ->int:
    context.user_data['result'] =  '0,0,0,0,0,0,0,0,0'

    query = update.callback_query
    await query.answer()
    context.user_data['first_turn'] = query.data

    if(context.user_data['first_turn'] == '0'):
        await query.message.reply_text( genrateTTT()
                                 , parse_mode='HTML')
    else:
        move = random.randrange(0, 9)
        
        temp = context.user_data['result'].split(",")
        temp[move] = 2
        context.user_data['result'] = ",".join(str(x) for x in temp)
        await query.message.reply_text( genrateTTT(context.user_data['result'])
                                 , parse_mode='HTML')
        
    
    keyboard = [
        [   
            InlineKeyboardButton("1", callback_data='1'),
            InlineKeyboardButton("2", callback_data='2'),
            InlineKeyboardButton("3", callback_data='3'),
        ],
        [
            InlineKeyboardButton("4", callback_data='4'),
            InlineKeyboardButton("5", callback_data='5'),
            InlineKeyboardButton("6", callback_data='6'),
        ],
        [
            InlineKeyboardButton("7", callback_data='7'),
            InlineKeyboardButton("8", callback_data='8'),
            InlineKeyboardButton("9", callback_data='9')
        ],
        [InlineKeyboardButton("cancel", callback_data='0')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text('<b>Would you like to go first or second?</b>', parse_mode='HTML', reply_markup=reply_markup)


    return RESULT

def genrateTTT(result=''):
    display = ''
    if(result==''):
        display = ('<u>     |       |       </u>\n'
                                        '<u>     |       |       </u>\n'
                                        '     |       |       \n')
    else:
        temp = result.split(",")
        constring = ''
        for k, v in enumerate(temp):
            if(v ==0):
                constring += '   '
            else:
                constring += v
            if(k%3==2):
                if(k!=len(temp)-1):
                    display += '<u>'+constring+'</u>\n'
                else:
                    display += constring
                constring=''
            else:
                constring += "|"

    return display
                
def insertmove(result, move, user):
    temp = result.split(",")
    temp[move] = user

    return ",".join(str(x) for x in temp)

def checkwinner(result):
    
    return None

def botmove(result):
    temp = result.split(",")
    
    possiblemove =[]
    for k,v in enumerate(temp):
        if(v=='0'):
            possiblemove.append(k)

    move = random.choices(possiblemove)
    return insertmove(result, move[0], 2)

async def gameplay_command(update: Update, context: ContextTypes.DEFAULT_TYPE) ->int:
    query = update.callback_query
    await query.answer()

    if(query.data=='0'):
        await query.message.reply_text('Bye! Hope to talk to you again soon.', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    context.user_data['result'] = insertmove(context.user_data['result'], int(query.data)-1, 1)
    await query.message.reply_text( genrateTTT(context.user_data['result'])
                                , parse_mode='HTML')
    checkwinner(context.user_data['result'])
    context.user_data['result'] = botmove(context.user_data['result'])
    await query.message.reply_text( genrateTTT(context.user_data['result'])
                            , parse_mode='HTML')
    checkwinner(context.user_data['result'])


    # Define inline buttons for car color selection
    keyboard = [
        [   
            InlineKeyboardButton("1", callback_data='1'),
            InlineKeyboardButton("2", callback_data='2'),
            InlineKeyboardButton("3", callback_data='3'),
        ],
        [
            InlineKeyboardButton("4", callback_data='4'),
            InlineKeyboardButton("5", callback_data='5'),
            InlineKeyboardButton("6", callback_data='6'),
        ],
        [
            InlineKeyboardButton("7", callback_data='7'),
            InlineKeyboardButton("8", callback_data='8'),
            InlineKeyboardButton("9", callback_data='9')
        ],
        [InlineKeyboardButton("cancel", callback_data='0')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text('<b>Come on make a move!</b>', parse_mode='HTML', reply_markup=reply_markup)

    return RESULT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text('Bye! Hope to see you again soon.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    print('Starting bot...')
    app =  Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('startgame', startgame_command)],
        states={
            GAMETYPE: [CallbackQueryHandler (playerorder_command)],
            FIRSTTURN: [CallbackQueryHandler (initmove_command)],
            RESULT: [CallbackQueryHandler (gameplay_command)],
            # RESULT: [MessageHandler(filters.TEXT & ~filters.COMMAND, gameplay_command)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    
    # Message handler for all text messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
  
    # Errors
    # app.add_error_handler(error)
    # Polls 
    print('Polling...')
    app.run_polling()

if __name__ == '__main__':
    main()

