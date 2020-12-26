import logging
import os
import signal
import sys

from telegram.ext import Updater
from telegram.message import Message

import strings
from commands import CommandManager, CallbackManager
from daemons import DaemonManager
from data_helper import is_list_of_size, get_date
from messages import MessageManager

# Create the log folder if it doesn't exist
try:
    os.mkdir(strings.log_folder)
except FileExistsError:
    pass

# Enable and configure logging
logging.basicConfig(
    filename=strings.log_folder + get_date(strings.hyphen),
    format=strings.log_format,
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class BotManager:
    chat_id: int = 0
    token: str = ''
    msg_mng: MessageManager = None
    daemon_mng: DaemonManager = None
    updater: Updater = None
    waiting_speedtest: [Message] = None

    def __init__(self, chat_id: int, token: str):
        self.chat_id = chat_id
        self.token = token
        self.updater = Updater(self.token)

        # Initiate the managers
        self.msg_mng = MessageManager(self)
        self.comm_mng = CommandManager(self)
        self.daemon_mng = DaemonManager(self)

    def start_working(self):
        """
        Start the bot_mng.
        """

        self.comm_mng.set_handlers()

        # Start the Bot
        self.daemon_mng.start_polling_scheduler()

    def polling_working(self):
        # Daemon thread that will ensure the safety of the server
        self.daemon_mng.start_safety_daemon()

        # Run the bot_mng until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # __start_polling() is non-blocking and will stop the bot_mng gracefully.
        self.updater.idle()

    def stop_bot(self):
        """
        Function that stops the bot
        """

        self.updater.stop()

    @staticmethod
    def quit_bot():
        """
        Function that stops the bot
        """

        os.kill(os.getpid(), signal.SIGINT)

    @staticmethod
    def shutdown_server():
        """
        Function that shutdowns the server
        """

        os.system("sudo shutdown now")

    @staticmethod
    def restart_server():
        """
        Function that restarts the server
        """

        os.system("sudo shutdown -r now")


def main(args):
    if is_list_of_size(args, 3):
        bot_manager = BotManager(int(args[1]), args[2])
        bot_manager.start_working()


if __name__ == "__main__":
    main(sys.argv)
