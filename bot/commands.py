import os
import subprocess

from telegram import Update

import messages
import strings
import data_helper


async def command_status(update: Update):
    await messages.send_message(update.effective_chat, messages.info_message(), update.message.id)


async def command_speedtest(update: Update):
    wait_message = await messages.send_message(update.effective_chat, strings.speedtest_wait_test, update.message.id, False)
    result = subprocess.run([strings.speedtest_bash], stdout=subprocess.PIPE, encoding=strings.utf_8)
    await messages.edit_message(wait_message, data_helper.format_speedtest(str(result.stdout)))


async def command_top(update: Update, top_result: str):
    await messages.send_message(update.effective_chat, messages.top_message(top_result), update.message.id)


async def command_block(update: Update):
    message = update.message
    ip = data_helper.get_first_ip(message.text)

    if ip is not None and ip.__len__() > 0:
        await messages.send_message(update.effective_chat, messages.block_message(ip), message.id)
    else:
        await messages.send_message(update.effective_chat, strings.block_help_text, message.id)


def block_ip(ip: str):
    if ip is not None and ip.__len__() > 0:
        os.system('sudo iptables -A INPUT -s ' + ip + ' -j DROP')


async def command_restart(update: Update):
    await messages.send_message(update.effective_chat, messages.restart_message(), update.message.id)


def restart_server():
    os.system(strings.restart_server_linux)


async def command_shutdown(update: Update):
    await messages.send_message(update.effective_chat, messages.shutdown_message(), update.message.id)


def shutdown_server():
    os.system(strings.shutdown_server_linux)


async def command_help(update: Update):
    await messages.send_message(update.effective_chat, messages.help_message(), update.message.id)
