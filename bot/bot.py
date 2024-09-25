import logging
import os
import sys

from telegram import Update
from telegram.ext import ApplicationBuilder, Application, CommandHandler, CallbackQueryHandler, ContextTypes

import strings
import commands
import server_safety
import callbacks
from data_helper import is_list_of_size, get_date

# Create the log folder if it doesn't exist
try:
    os.mkdir(strings.log_folder)
except FileExistsError:
    pass

# Enable and configure logging
logging.basicConfig(
    filename=strings.log_folder + get_date(strings.hyphen) + strings.log_file_ext,
    format=strings.log_format,
    level=logging.WARNING
)

logger = logging.getLogger(__name__)


class ServerTelegramBot:
    __chat_id: int
    __application: Application
    __server_safety: server_safety.ServerSafety

    def __init__(self, chat_id: int, token: str):
        self.__chat_id = chat_id
        self.__application = ApplicationBuilder().token(token).build()
        self.__server_safety = server_safety.ServerSafety()

    def start(self):
        self.set_command_handlers()
        self.set_callback_handlers()

        self.__server_safety.start(self.__application, self.__chat_id)

        # Start the Bot
        self.__application.run_polling()

    def set_command_handlers(self):
        self.__application.add_handlers([CommandHandler(strings.command_start, self.command_start),
                                         CommandHandler(strings.command_status, self.command_status),
                                         CommandHandler(strings.command_speedtest, self.command_speedtest),
                                         CommandHandler(strings.command_top, self.command_top),
                                         CommandHandler(strings.command_block, self.command_block),
                                         CommandHandler(strings.command_restart, self.command_restart),
                                         CommandHandler(strings.command_shutdown, self.command_shutdown),
                                         CommandHandler(strings.command_help, self.command_help)])

    async def command_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.is_own_chat(update.effective_chat.id):
            await commands.command_help(update)

    async def command_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.is_own_chat(update.effective_chat.id):
            await commands.command_status(update)

    async def command_speedtest(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.is_own_chat(update.effective_chat.id):
            await commands.command_speedtest(update)

    async def command_top(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.is_own_chat(update.effective_chat.id):
            top_result: str = self.__server_safety.top()
            await commands.command_top(update, top_result)

    async def command_block(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.is_own_chat(update.effective_chat.id):
            await commands.command_block(update)

    async def command_restart(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.is_own_chat(update.effective_chat.id):
            await commands.command_restart(update)

    async def command_shutdown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.is_own_chat(update.effective_chat.id):
            await commands.command_shutdown(update)

    async def command_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.is_own_chat(update.effective_chat.id):
            await commands.command_help(update)

    def set_callback_handlers(self):
        self.__application.add_handler(CallbackQueryHandler(self.callbacks))

    async def callbacks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.is_own_chat(update.effective_chat.id):
            await callbacks.callbacks(update.callback_query)

    def is_own_chat(self, chat_id: int) -> bool:
        return self.__chat_id == chat_id


def main(args) -> None:
    if is_list_of_size(args, 3):
        bot = ServerTelegramBot(int(args[1]), args[2])
        bot.start()

    else:
        print('You are missing parameters, please check the README.md')


if __name__ == "__main__":
    main(sys.argv)
