import logging
import sched
import threading
import time

import emoji
from telegram.error import NetworkError

import buttons
import strings
from data_helper import format_table_row, format_link, get_first_ip
from messages import MessageManager


class DaemonManager:
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
    delay_print_threads = 30

    # A lower number represents a higher priority
    priority_safety = 1
    priority_try_polling = 1
    priority_print_threads = 2

    # Number of retries
    retries_polling: int = 0

    def __init__(self, bot_manager):
        self.bot_mng = bot_manager
        self.msg_mng: MessageManager = bot_manager.msg_mng
        self.start_printing_threads_daemon()

    def __printing_threads(self, s):
        logging.info(strings.number_threads_1 + str(threading.active_count()) + strings.number_threads_2)

        s.enter(self.delay_print_threads, self.priority_print_threads, self.__printing_threads, (s,))

    def __schedule_printing_threads(self):
        s = sched.scheduler(time.time, time.sleep)
        s.enter(0, self.priority_print_threads, self.__printing_threads, (s,))
        s.run()

    def start_printing_threads_daemon(self):
        x = threading.Thread(target=self.__schedule_printing_threads, daemon=True)
        x.start()

    def __start_polling(self, s):
        try:
            # Try to start polling updates from the Telegram API server
            self.bot_mng.updater.start_polling()

            # If the polling is working, continue in the bot manager
            self.bot_mng.polling_working()

        except NetworkError:
            # Stop the updater
            self.bot_mng.stop_bot()

            self.retries_polling += 1
            logging.error(strings.network_error + str(self.retries_polling) + strings.triple_dots)

            # Retry to start polling
            s.enter(self.delay_try_polling, self.priority_try_polling, self.__start_polling, (s,))

    def start_polling_scheduler(self):
        # Scheduler
        s = sched.scheduler(time.time, time.sleep)
        s.enter(0, self.priority_try_polling, self.__start_polling, (s,))
        s.run()

    def __warning(self, ip: str, line: str):
        text = emoji.emojize(strings.warning_title) + strings.break_line + strings.break_line \
               + format_table_row(ip, end_line=False) + strings.space \
               + format_link(strings.location_text, strings.iplocation_url + ip) + strings.break_line \
               + format_table_row(line, separator=False)

        block_button = buttons.block.copy()
        block_button[1] += strings.hyphen + ip

        self.msg_mng.send_message([text, [block_button, buttons.shutdown], [3, 3]])

    def __add_line(self, ip: str, line: str, warn: bool = True):

        if ip in self.__lines.keys():
            if line not in self.__lines[ip]:

                self.__lines[ip].append(line)
                self.__top[ip] += 1

                if warn:
                    self.__warning(ip, line)
        else:
            self.__lines[ip] = [line]
            self.__top[ip] = 1

            if warn:
                self.__warning(ip, line)

    def __ip_ignored(self, ip: str):

        if ip is None or ip in self.ignored_ips:
            return True

        for net in self.ignored_nets:
            if ip.startswith(net):
                return True

        return False

    def __safety(self, s: sched.scheduler = None, warn: bool = True):
        with open(strings.auth_log) as fh:
            lines = fh.readlines()

        for line in lines:

            line = line.rstrip()
            ip = get_first_ip(line)

            if not self.__ip_ignored(ip):
                self.__add_line(ip, line, warn)

        if s is not None:
            s.enter(self.delay_safety, self.priority_safety, self.__safety, (s, True))

    def __schedule_safety(self):
        s = sched.scheduler(time.time, time.sleep)
        s.enter(0, self.priority_safety, self.__safety, (s, False))
        s.run()

    def start_safety_daemon(self):
        x = threading.Thread(target=self.__schedule_safety, daemon=True)
        x.start()

    def top(self) -> str:
        text = strings.empty

        if self.__top.__len__() > 0:
            self.__top = dict(sorted(self.__top.items(), key=lambda x: x[1], reverse=True))
            for ip in self.__top.keys():
                text += format_table_row(ip, self.__top[ip], 20)
        else:
            text = format_table_row(strings.no_registers, separator=False)

        return text
