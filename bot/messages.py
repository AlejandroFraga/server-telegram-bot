"""

"""
import logging
import time

import emoji
import psutil
from requests import get
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Message

import buttons
import strings
from data_helper import is_list_of_min_size, format_table_row, is_tuple
from data_helper import is_str, is_list, is_list_of_size, get_date_hour, format_bytes, format_percent, format_temp


# MESSAGES


def info_message():
    text = ':information: Info' + '\n\n' \
           + format_table_row('Cores', str(psutil.cpu_count(True))) \
           + format_table_row('Threads', str(psutil.cpu_count())) \
           + format_table_row('Free RAM', format_bytes(psutil.virtual_memory().free)) \
           + format_table_row('Free Mem.', format_bytes(psutil.disk_usage('/').free))

    callbacks = [buttons.cpus, buttons.temps, buttons.ram,
                 buttons.processes, buttons.net, buttons.disks]

    sizes = [3, 3, 3, 3, 3, 3]

    return text, callbacks, sizes


def cpus_message():
    text = strings.cpus_text \
           + format_table_row('CPU', format_percent(psutil.cpu_percent()))

    i = 0
    for cpu_time in psutil.cpu_percent(percpu=True):
        i += 1
        text += format_table_row('Core' + str(i), format_percent(cpu_time))

    callbacks = [buttons.back_info, buttons.temps, buttons.ram,
                 buttons.processes, buttons.net, buttons.disks]

    sizes = [3, 3, 3, 3, 3, 3]

    return text, callbacks, sizes


def temps_message():
    text = strings.temps_text

    temps = psutil.sensors_temperatures()
    for tempKey in temps.keys():
        text += format_table_row(tempKey)

        for temp in temps.get(tempKey):
            label = temp.label if temp.label else strings.no_label
            text += format_table_row(label, format_temp(temp.current))

        text += '\n'

    callbacks = [buttons.cpus, buttons.back_info, buttons.ram,
                 buttons.processes, buttons.net, buttons.disks]

    sizes = [3, 3, 3, 3, 3, 3]

    return text, callbacks, sizes


def ram_message():
    total = psutil.virtual_memory().total
    used = psutil.virtual_memory().used
    used_p = format_percent(used / total, 1)
    avail = psutil.virtual_memory().available
    avail_p = format_percent(avail / total, 1)
    cached = psutil.virtual_memory().cached
    cached_p = format_percent(cached / total, 1)
    free = psutil.virtual_memory().free
    free_p = format_percent(free / total, 1)

    text = strings.ram_text \
           + format_table_row('Used', format_bytes(used)) \
           + format_table_row(format_percent('Used'), used_p) \
           + strings.break_line \
           + format_table_row('Free', format_bytes(free)) \
           + format_table_row(format_percent('Free'), avail_p) \
           + strings.break_line \
           + format_table_row('Cached', format_bytes(cached)) \
           + format_table_row(format_percent('Cached'), cached_p) \
           + strings.break_line \
           + format_table_row('Avail.', format_bytes(avail)) \
           + format_table_row(format_percent('Avail.'), free_p)

    callbacks = [buttons.cpus, buttons.temps, buttons.back_info,
                 buttons.processes, buttons.net, buttons.disks]

    sizes = [3, 3, 3, 3, 3, 3]

    return text, callbacks, sizes


def get_process_by_cpu_percent():
    """
    Get list of running process sorted by Memory Usage
    """

    processes = []
    # Iterate over the list
    for proc in psutil.process_iter():
        proc.cpu_percent()

    time.sleep(0.1)

    for proc in psutil.process_iter():
        try:
            attrs = [strings.process_pid, strings.process_name,
                     strings.process_username, strings.process_memory_percent,
                     strings.process_cpu_num, strings.process_cmdline]
            pinfo = proc.as_dict(attrs)
            pinfo[strings.process_cpu_percent] = proc.cpu_percent()

            processes.append(pinfo)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return sorted(processes, key=lambda process: process['cpu_percent'], reverse=True)


def processes_message():
    text = strings.proc_text

    processes = get_process_by_cpu_percent()

    cpu_count = max(psutil.cpu_count(), 1)

    for process in processes:
        if process['cpu_percent'] > 0:
            text += format_table_row('Pid', process['pid']) \
                    + format_table_row('Program', process['name'])

            if is_list_of_min_size(process['cmdline'], 2):
                text += format_table_row('Args', process['cmdline'][1])

            text += format_table_row('User', process['username']) \
                    + format_table_row('Mem%', format_percent(process['memory_percent'])) \
                    + format_table_row('Cpu%', format_percent(process['cpu_percent'] / cpu_count)) + '\n'

    callbacks = [buttons.cpus, buttons.temps, buttons.ram,
                 buttons.back_info, buttons.net, buttons.disks]

    sizes = [3, 3, 3, 3, 3, 3]

    return text, callbacks, sizes


def net_message():
    text = strings.net_text

    text += format_table_row('Public IP', get(strings.ipfy_url).text) + '\n'

    nets = psutil.net_io_counters(True)
    for netKey in nets.keys():
        if netKey != 'lo':
            net = nets.get(netKey)
            is_up = psutil.net_if_stats()[netKey].isup

            text += format_table_row(netKey)
            text += format_table_row('Is up', str(is_up))

            if is_up:
                text += format_table_row('Address', psutil.net_if_addrs()[netKey][0].address)
                text += format_table_row('Sent', format_bytes(net.bytes_sent))
                text += format_table_row('Recv', format_bytes(net.bytes_recv))

            text += '\n'

    callbacks = [buttons.cpus, buttons.temps, buttons.ram,
                 buttons.processes, buttons.back_info, buttons.disks]

    sizes = [3, 3, 3, 3, 3, 3]

    return text, callbacks, sizes


def get_disk_info(route: str, title: str = None):
    text = ''

    try:
        disk_usage = psutil.disk_usage(route)

        text += format_table_row(title if is_str(title) else route)
        text += format_table_row('Used', format_bytes(disk_usage.used))
        text += format_table_row('Used%', format_percent(disk_usage.percent))
        text += format_table_row('Free', format_bytes(disk_usage.free))
        text += format_table_row('Free%', format_percent(100 - disk_usage.percent))

    except FileNotFoundError as e:
        logging.error(e.strerror)

    return text


def disks_message():
    text = strings.disks_text

    text += get_disk_info('/', 'root') + '\n'
    text += get_disk_info('/boot/firmware', 'firmware')

    callbacks = [buttons.cpus, buttons.temps, buttons.ram,
                 buttons.processes, buttons.net, buttons.back_info]

    sizes = [3, 3, 3, 3, 3, 3]

    return text, callbacks, sizes


def top_message(top_result: str = ''):
    return strings.top_text + top_result, None, None


def restart_message():
    return strings.restart_text, [buttons.restart], [2]


def shutdown_message():
    return strings.shutdown_text, [buttons.shutdown], [2]


def stop_message():
    return strings.stop_text, [buttons.stop], [2]


def help_message():
    return strings.help_text, None, None


class MessageManager:

    def __init__(self, bot_manager):
        self.bot_mng = bot_manager
        self.chat_id = bot_manager.chat_id
        self.bot = bot_manager.updater.bot

    @staticmethod
    def __append_dismiss_callback_callbacks(callbacks: list = None):

        # If callbacks is not a list, create an empty one
        if not is_list(callbacks):
            callbacks = []

        # Append the dismiss callback and return
        callbacks.append(buttons.dismiss)

        return callbacks

    @staticmethod
    def __append_dismiss_callback_sizes(sizes: list = None):

        # If sizes is a not empty list, append the last size at the end
        if is_list_of_min_size(sizes, 1):
            sizes.append(sizes[-1])

        # Otherwise, create a list with a 1 in it
        else:
            sizes = [1]

        return sizes

    @staticmethod
    def __append_dismiss_callback(callbacks: list = None, sizes: list = None):

        callbacks = MessageManager.__append_dismiss_callback_callbacks(callbacks)
        sizes = MessageManager.__append_dismiss_callback_sizes(sizes)

        return callbacks, sizes

    # TODO clean
    @staticmethod
    def __make_reply_markup(callbacks: list, sizes: list, add_dismiss: bool):

        if add_dismiss:
            callbacks, sizes = MessageManager.__append_dismiss_callback(callbacks, sizes)

        if is_list_of_min_size(callbacks) and is_list_of_min_size(sizes):
            keyboard = []
            line = []
            keyboard.append(line)

            #
            i, n = 0, 1
            for callback in callbacks:

                if is_list_of_size(callback, 2) and i < sizes.__len__() \
                        and is_str(callback[0]) and callback[1] is not None:

                    text = emoji.emojize(callback[0])
                    line.append(InlineKeyboardButton(text, callback_data=str(callback[1])))

                    #
                    if sizes[i] <= n:
                        n = 1
                        line = []
                        keyboard.append(line)

                    #
                    else:
                        n += 1

                i += 1

            return InlineKeyboardMarkup(keyboard)

        return None

    # TODO move
    @staticmethod
    def __split_message(message: any):

        if is_tuple(message):
            message = list(message)

        if is_list(message):
            text = MessageManager.__format_text(message[0]) if message.__len__() > 0 else None
            callbacks = message[1] if message.__len__() > 1 else None
            sizes = message[2] if message.__len__() > 2 else None
            return text, callbacks, sizes

        elif is_str(message):
            return MessageManager.__format_text(message), None, None

    # TODO move
    @staticmethod
    def __format_text(text: str):
        return format_table_row(get_date_hour(), separator=False) + '\n\n'\
               + emoji.emojize(str(text))

    @staticmethod
    def edit_message(original: Message, message: any, add_dismiss: bool = True):
        """

        :param original:
        :param message:
        :param add_dismiss:
        :return:
        """

        text, callbacks, sizes = MessageManager.__split_message(message)

        # Get Reply Markup
        reply_markup = MessageManager.__make_reply_markup(callbacks, sizes, add_dismiss)

        return original.edit_text(text=text, parse_mode='HTML', disable_web_page_preview=True,
                                  reply_markup=reply_markup)

    def send_message(self, message: any, reply_to: str = None, add_dismiss: bool = True):
        """

        :param message:
        :param reply_to:
        :param add_dismiss:
        :return:
        """

        text, callbacks, sizes = MessageManager.__split_message(message)

        # Get Reply Markup
        reply_markup = MessageManager.__make_reply_markup(callbacks, sizes, add_dismiss)

        return self.bot.send_message(self.chat_id, text, 'HTML', True, False, reply_to, reply_markup)
