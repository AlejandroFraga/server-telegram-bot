import subprocess
import threading

from telegram import Update, Message, CallbackQuery
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler

import buttons
import messages
import strings
from data_helper import format_speedtest, get_value


class CommandManager:

    def __init__(self, bot_manager):
        self.bot_mng = bot_manager
        self.chat_id = bot_manager.chat_id
        self.updater = bot_manager.updater

        self.bot = bot_manager.updater.bot
        self.msg_mng: messages.MessageManager = bot_manager.msg_mng
        self.callback_mng = CallbackManager(bot_manager)
        self.waiting_speedtest = None

    def set_handlers(self):
        # Get the dispatcher to register handlers
        dispatcher = self.updater.dispatcher

        # On different commands
        dispatcher.add_handler(CommandHandler(strings.command_start, self.command_start))
        dispatcher.add_handler(CommandHandler(strings.command_stop, self.command_stop))
        dispatcher.add_handler(CommandHandler(strings.command_status, self.command_status))
        dispatcher.add_handler(CommandHandler(strings.command_speedtest, self.command_speedtest))
        dispatcher.add_handler(CommandHandler(strings.command_top, self.command_top))
        dispatcher.add_handler(CommandHandler(strings.command_restart, self.command_restart))
        dispatcher.add_handler(CommandHandler(strings.command_shutdown, self.command_shutdown))
        dispatcher.add_handler(CommandHandler(strings.command_help, self.command_help))

        # And on different callbacks
        dispatcher.add_handler(CallbackQueryHandler(self.callback_mng.process_callback))

    def command_start(self, update: Update, context: CallbackContext):

        # Check that the message came from the desired chat
        if update.effective_chat.id == self.chat_id:
            # Get the help message and send it
            self.msg_mng.send_message(messages.help_message(), update.message.message_id)

    def command_status(self, update: Update, context: CallbackContext):

        # Check that the message came from the desired chat
        if update.effective_chat.id == self.chat_id:
            # Get the info message and send it
            self.msg_mng.send_message(messages.info_message(), update.message.message_id)

    def command_speedtest(self, update: Update, context: CallbackContext):

        if update.effective_chat.id == self.chat_id:
            if self.waiting_speedtest:
                update.message.delete()
            else:

                self.waiting_speedtest = \
                    self.msg_mng.send_message(strings.speedtest_wait_test, update.message.message_id, False)

                thread = threading.Thread(target=self.make_speedtest)
                thread.start()

    def make_speedtest(self):
        command = subprocess.run([strings.speedtest_bash], stdout=subprocess.PIPE, encoding=strings.utf_8)
        result = format_speedtest(str(command.stdout))

        if self.waiting_speedtest is not None:
            self.msg_mng.edit_message(self.waiting_speedtest, result)
            self.waiting_speedtest = None

    def command_top(self, update: Update, context: CallbackContext):

        if update.effective_chat.id == self.chat_id:
            text = self.bot_mng.daemon_mng.top()
            self.msg_mng.send_message(messages.top_message(text), update.message.message_id)

    def command_restart(self, update: Update, context: CallbackContext):

        if update.effective_chat.id == self.chat_id:
            self.msg_mng.send_message(messages.restart_message(), update.message.message_id)

    def command_shutdown(self, update: Update, context: CallbackContext):

        if update.effective_chat.id == self.chat_id:
            self.msg_mng.send_message(messages.shutdown_message(), update.message.message_id)

    def command_stop(self, update: Update, context: CallbackContext):

        if update.effective_chat.id == self.chat_id:
            self.msg_mng.send_message(messages.stop_message(), update.message.message_id)

    def command_help(self, update: Update, context: CallbackContext):

        if update.effective_chat.id == self.chat_id:
            self.msg_mng.send_message(messages.help_message(), update.message.message_id)


class CallbackManager:

    def __init__(self, bot_manager):
        self.bot_mng = bot_manager
        self.msg_mng = bot_manager.msg_mng

    @staticmethod
    def __delete_message_and_reply(message: Message = None):

        if message is not None:
            if message.reply_to_message is not None:
                message.reply_to_message.delete()
            message.delete()

    def __dismiss_callback(self, query: CallbackQuery):

        self.__delete_message_and_reply(query.message)

    def __shutdown_callback(self, query: CallbackQuery):

        self.__delete_message_and_reply(query.message)

        self.msg_mng.send_message(strings.shutdown_callback_text)

        self.bot_mng.shutdown_server()

    def __restart_callback(self, query: CallbackQuery):

        self.__delete_message_and_reply(query.message)

        self.msg_mng.send_message(strings.restart_callback_text)

        self.bot_mng.restart_server()

    def __stop_callback(self, query: CallbackQuery):

        self.__delete_message_and_reply(query.message)

        self.msg_mng.send_message(strings.stop_callback_text)

        self.bot_mng.quit_bot()

    def __general_callback(self, query: CallbackQuery):

        if query.data == get_value(buttons.Callback.dismiss):
            self.__dismiss_callback(query)

        elif query.data == get_value(buttons.Callback.shutdown):
            self.__shutdown_callback(query)

        elif query.data == get_value(buttons.Callback.restart):
            self.__restart_callback(query)

        elif query.data == get_value(buttons.Callback.stop):
            self.__stop_callback(query)

    def __info_callback(self, query: CallbackQuery):

        self.msg_mng.edit_message(query.message, messages.info_message())

    def __cpus_callback(self, query: CallbackQuery):

        self.msg_mng.edit_message(query.message, messages.cpus_message())

    def __temps_callback(self, query: CallbackQuery):

        self.msg_mng.edit_message(query.message, messages.temps_message())

    def __ram_callback(self, query: CallbackQuery):

        self.msg_mng.edit_message(query.message, messages.ram_message())

    def __processes_callback(self, query: CallbackQuery):

        self.msg_mng.edit_message(query.message, messages.processes_message())

    def __net_callback(self, query: CallbackQuery):

        self.msg_mng.edit_message(query.message, messages.net_message())

    def __disks_callback(self, query: CallbackQuery):

        self.msg_mng.edit_message(query.message, messages.disks_message())

    def __status_callback(self, query: CallbackQuery):

        if query.data == get_value(buttons.Callback.info):
            self.__info_callback(query)

        elif query.data == get_value(buttons.Callback.cpus):
            self.__cpus_callback(query)

        elif query.data == get_value(buttons.Callback.temps):
            self.__temps_callback(query)

        if query.data == get_value(buttons.Callback.ram):
            self.__ram_callback(query)

        elif query.data == get_value(buttons.Callback.processes):
            self.__processes_callback(query)

        elif query.data == get_value(buttons.Callback.net):
            self.__net_callback(query)

        elif query.data == get_value(buttons.Callback.disks):
            self.__disks_callback(query)

    def process_callback(self, update: Update, context: CallbackContext):
        query = update.callback_query

        if update.effective_chat.id == self.bot_mng.chat_id:

            if query.data.startswith(get_value(buttons.Callback.general)):
                self.__general_callback(query)

            elif query.data.startswith(get_value(buttons.Callback.status)):
                self.__status_callback(query)
