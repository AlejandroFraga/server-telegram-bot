import logging

import emoji
from telegram.ext import Application, ContextTypes

import buttons
import strings
import messages
import data_helper


class ServerSafety:
    # Dictionary that will store all the ips with its respective __lines of the auth log file
    __lines = {}

    __top: {str, int} = {}

    # Ips that should be ignored as it doesn't represent a danger
    ignored_ips = [
        strings.unspecified,
        strings.localhost
    ]

    ignored_nets = [
        strings.local_net
    ]

    # Delay in seconds to execute the next processing of the auth log file
    delay_safety = 5
    delay_try_polling = 10

    # A lower number represents a higher priority
    priority_safety = 1
    priority_try_polling = 1

    # Number of retries
    retries_polling: int = 0

    def start(self, application: Application, chat_id: int) -> None:
        self.__first_safety_check()
        application.job_queue.run_repeating(self.__safety_check, interval=self.delay_safety, chat_id=chat_id)

    def top(self) -> str:
        text = strings.empty

        if self.__top.__len__() > 0:
            self.__top = dict(sorted(self.__top.items(), key=lambda x: x[1], reverse=True))
            for ip in self.__top.keys():
                text += data_helper.format_table_row(ip, self.__top[ip], 20)
        else:
            text = data_helper.format_table_row(strings.no_registers, separator=False)

        return text

    def __first_safety_check(self):
        try:
            file = open(strings.auth_log, 'r')
            with file:
                for line in file.readlines():
                    ip = data_helper.get_first_ip(line)
                    if not self.__ip_ignored(ip):

                        if ip in self.__lines.keys():
                            if line not in self.__lines[ip]:
                                self.__lines[ip].append(line)
                                self.__top[ip] += 1
                        else:
                            self.__lines[ip] = [line]
                            self.__top[ip] = 1
                file.close()

        except OSError:
            logging.log(logging.ERROR, 'Could not open/read file: %s', strings.auth_log)

    async def __safety_check(self, context: ContextTypes.DEFAULT_TYPE):
        try:
            file = open(strings.auth_log, 'r')
            with file:
                for line in file.readlines():
                    await self.__add_line(line, context)
                file.close()

        except OSError:
            logging.log(logging.ERROR, 'Could not open/read file: %s', strings.auth_log)

    async def __add_line(self, line: str, context: ContextTypes.DEFAULT_TYPE):
        ip = data_helper.get_first_ip(line)
        if not self.__ip_ignored(ip):

            if ip in self.__lines.keys():
                if line not in self.__lines[ip]:

                    self.__lines[ip].append(line)
                    self.__top[ip] += 1
                    await self.__warning(ip, line, context)
            else:
                self.__lines[ip] = [line]
                self.__top[ip] = 1
                await self.__warning(ip, line, context)

    def __ip_ignored(self, ip: str):
        if ip is None or ip in self.ignored_ips:
            return True

        for net in self.ignored_nets:
            if ip.startswith(net):
                return True

        return False

    @staticmethod
    async def __warning(ip: str, line: str, context: ContextTypes.DEFAULT_TYPE):
        text = emoji.emojize(strings.warning_title) + strings.break_line + strings.break_line \
               + data_helper.format_table_row(ip, end_line=False) + strings.space \
               + data_helper.format_link(strings.location_text, strings.iplocation_url + ip) + strings.break_line \
               + data_helper.format_table_row(line, separator=False)

        block_button = buttons.block.copy()
        block_button[1] += strings.hyphen + ip

        chat = await context.bot.get_chat(context.job.chat_id)
        await messages.send_message(chat, [text, [block_button, buttons.shutdown], [3, 3]])
