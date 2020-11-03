
class BotManager(object):
    chat_id: int = 0
    token: str = ""

    def __init__(self,
                 chat_id: int,
                 token: str):

        BotManager.chat_id = chat_id
        BotManager.token = token

def start_working():

    import logging
    from telegram.ext import Updater

    updater = Updater(token=BotManager.token, use_context=True)

    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    from telegram.ext import CommandHandler
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('status', status))
    dispatcher.add_handler(CommandHandler('top', top))
    dispatcher.add_handler(CommandHandler('restart', restart))

    updater.start_polling()

def start(update, context):
    print("start called")

    if update.effective_chat.id == BotManager.chat_id:
        context.bot.send_message(chat_id=BotManager.chat_id, text="I'm a bot, please talk to me!")

def status(update, context):
    print("status called")

    if update.effective_chat.id == BotManager.chat_id:
        import PcStatus
        context.bot.send_message(chat_id=BotManager.chat_id, text=PcStatus.getStatus(), parse_mode="HTML")


def top(update, context):
    print("top called")

    if update.effective_chat.id == BotManager.chat_id:

        import LogReader, re, collections

        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

        with open('/var/auth.log') as fh:
            string = fh.readlines()

        lst = []

        for line in string:
            line = line.rstrip()
            result = re.search(pattern, line)
            if result:
                lst.append(result[0])

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

        context.bot.send_message(chat_id=BotManager.chat_id, text=LogReader.getMap(newMap, total))

def restart(update, context):
    print("restart called")

    if update.effective_chat.id == BotManager.chat_id:
        import os
        os.system("sudo shutdown -r now")