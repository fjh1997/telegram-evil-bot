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
        result=check_output(["runasuser.exe","jail","jail","RestrictShutdown.exe",
        # absolute path is needed I dont know why
        r"C:\Users\54930\AppData\Local\Programs\Python\Python310\python.exe", "-c", cmd], stderr=STDOUT, timeout=5).decode("gbk")
    except Exception as e:
        result=str(e)
        
    return result
    

async def do_eval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info("%s %s %s: %s",user.first_name ,user.last_name,user.username, update.message.text)
    result = await hack(update.message.text)
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))


async def do_eval_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "@catcatworm_bot" in update.message.parse_entities("mention").values():
        user = update.message.from_user
        logger.info("%s %s %s: %s",user.first_name ,user.last_name,user.username, update.message.text)
        result=await hack(update.message.text.replace("@catcatworm_bot",""))
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=result)
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
    
if __name__ == "__main__":
    token=input("please input your token:")
    application = ApplicationBuilder().token(token).build()
    
    msg_handler = MessageHandler(filters.ChatType.PRIVATE, do_eval)
    grp_handler = MessageHandler(filters.ChatType.GROUPS & filters.Entity("mention"), do_eval_group)
    application.add_handler(msg_handler)
    application.add_handler(grp_handler)
    application.run_polling()