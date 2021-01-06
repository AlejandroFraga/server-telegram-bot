"""
File to store all the button's (reply_markup) of the bot, so they can be easily modified across the entire program
"""

from enum import Enum

import strings
from data_helper import get_value


class Callback(Enum):
    # General callbacks 1XX
    general = 1
    dismiss = 100
    block = 101
    shutdown = 102
    restart = 103
    stop = 104

    # Status callbacks 2XX
    status = 2
    info = 200
    cpus = 201
    temps = 202
    ram = 203
    processes = 204
    net = 205
    disks = 206


dismiss = [strings.dismiss_button_text, get_value(Callback.dismiss)]

stop = [strings.stop_button_text, get_value(Callback.stop.value)]

back_info = [strings.back_button_text, get_value(Callback.info)]

cpus = [strings.cpus_button_text, get_value(Callback.cpus)]
temps = [strings.temps_button_text, get_value(Callback.temps)]
ram = [strings.ram_button_text, get_value(Callback.ram)]
processes = [strings.proc_button_text, get_value(Callback.processes)]
net = [strings.net_button_text, get_value(Callback.net)]
disks = [strings.disks_button_text, get_value(Callback.disks)]

block = [strings.block_button_text, get_value(Callback.block)]

restart = [strings.restart_button_text, get_value(Callback.restart)]
shutdown = [strings.shutdown_button_text, get_value(Callback.shutdown)]
