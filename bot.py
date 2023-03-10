import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler,filters
from subprocess import STDOUT, check_output




logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def hack(cmd):
    try:
        result=check_output(["runasuser.exe","jail","jail","RestrictShutdown.exe","python.exe", "-c", cmd], stderr=STDOUT, timeout=5).decode("gbk")
    except Exception as e:
        result=str(e)
        
    return result
    

async def do_eval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info("%s: %s", user.username, update.message.text)
    result = await hack(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=result)


async def do_eval_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "@catcatworm_bot" in update.message.parse_entities("mention").values():
        user = update.message.from_user
        logger.info("%s: %s", user.username, update.message.text)
        result=await hack(update.message.text.replace("@catcatworm_bot",""))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    
if __name__ == "__main__":
    token=input("please input your token:")
    application = ApplicationBuilder().token(token).build()
    
    msg_handler = MessageHandler(filters.ChatType.PRIVATE, do_eval)
    grp_handler = MessageHandler(filters.ChatType.GROUPS & filters.Entity("mention"), do_eval_group)
    application.add_handler(msg_handler)
    application.add_handler(grp_handler)
    application.run_polling()