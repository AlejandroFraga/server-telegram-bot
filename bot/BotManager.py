import logging
import PcStatus
import subprocess

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class BotManager(object):
    chat_id: int = 0
    token: str = ""
    updater = ""
    waiting_speedtest = 0

    def __init__(self,
                 chat_id: int,
                 token: str):
        BotManager.chat_id = chat_id
        BotManager.token = token


def start_working():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    BotManager.updater = Updater(token=BotManager.token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = BotManager.updater.dispatcher

    # on different commands
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('status', status))
    dispatcher.add_handler(CommandHandler('speedtest', speedtest))
    dispatcher.add_handler(CommandHandler('top', top))
    dispatcher.add_handler(CommandHandler('restart', restart))
    dispatcher.add_handler(CommandHandler('shutdown', shutdown))
    dispatcher.add_handler(CommandHandler('stop', stop))

    # CallbackQuery handler
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    BotManager.updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    BotManager.updater.idle()


def start(update: Update, context: CallbackContext):
    print("start called")

    if update.effective_chat.id == BotManager.chat_id:
        keyboard = [
            [
                InlineKeyboardButton("Option 1", callback_data='1'),
                InlineKeyboardButton("Option 2", callback_data='2'),
            ],
            [InlineKeyboardButton("Option 3", callback_data='3')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))


def status(update: Update, context: CallbackContext):
    print("status called")

    if update.effective_chat.id == BotManager.chat_id:
        update.message.reply_text(text=PcStatus.get_status(), parse_mode="HTML")


def speedtest(update: Update, context: CallbackContext):
    print("speedtest called")

    if update.effective_chat.id == BotManager.chat_id:
        if BotManager.waiting_speedtest != 0:
            BotManager.waiting_speedtest.edit_text("Wait for the result, please")
        else:
            BotManager.waiting_speedtest = update.message.reply_text("Wait for the result, it takes ~30-40 sec")

            command = subprocess.run(['speedtest'], stdout=subprocess.PIPE)
            result = str(command.stdout).replace("\\n", "\n").replace("\\r", "")
            if result.__sizeof__() > 3:
                result = result[2:-1]
            BotManager.waiting_speedtest.edit_text(result)


def top(update: Update, context: CallbackContext):
    print("top called")

    if update.effective_chat.id == BotManager.chat_id:

        import LogReader, re, collections

        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

        with open('/var/log/auth.log') as fh:
            string = fh.readlines()

        lst = []
        ignored_ips = ["192.168.1.151", "192.168.1.1", "0.0.0.0"]

        for line in string:
            line = line.rstrip()
            result = re.search(pattern, line)
            if result and result[0] not in ignored_ips:
                if re.search('Accepted', line):
                    lst.append(result[0])
                    print("Accepted: " + result[0])
                elif re.search('Failed', line):
                    lst.append(result[0])
                    print("Failed: " + result[0])
                else:
                    lst.append(result[0])
                    print(line)

        lst = sorted(lst, key=lambda ip: \
            (int(ip.split(".")[0]),
             int(ip.split(".")[1]),
             int(ip.split(".")[2]),
             int(ip.split(".")[3])))

        total = 0

        chainMap = collections.ChainMap()

        for ip in lst:
            if ip not in chainMap.keys():
                child = {ip: 1}
            else:
                i = chainMap.get(ip)
                chainMap.pop(ip)
                child = {ip: i + 1}

            total += 1
            chainMap = chainMap.new_child(child)

        newMap = collections.ChainMap()

        for chain in chainMap.maps:
            if chain and chain:
                newMap = newMap.new_child(chain)

        newMap = sorted(newMap.items(), key=lambda item: item[1], reverse=True)

        update.message.reply_text(text=LogReader.get_map(newMap, total))


def restart(update: Update, context: CallbackContext):
    print("restart called")

    if update.effective_chat.id == BotManager.chat_id:
        import os
        os.system("sudo shutdown -r now")


def shutdown(update: Update, context: CallbackContext):
    print("restart called")

    if update.effective_chat.id == BotManager.chat_id:
        import os
        os.system("sudo shutdown now")


def stop(update: Update, context: CallbackContext):
    BotManager.updater.stop()
