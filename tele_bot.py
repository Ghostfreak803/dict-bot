import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
from dfs import get_def

TOKEN = ''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def defs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    recieved_word = '-'.join(context.args).lower()
    if not context.args:
        await context.bot.send_message(reply_to_message_id=update._effective_message.id, chat_id=update.effective_chat.id, text='please enter a word')
    else:
        await context.bot.send_message(reply_to_message_id=update._effective_message.id, chat_id=update.effective_chat.id, text=f'{get_def(recieved_word)}', parse_mode='html')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    defs_handler = CommandHandler('def', defs)

    application.add_handler(start_handler)
    # application.add_handler(echo_handler)
    application.add_handler(defs_handler)

    application.run_polling()

    
    
