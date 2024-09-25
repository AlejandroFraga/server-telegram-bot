from telegram import CallbackQuery, Message

import commands
import data_helper
import messages
import strings
import buttons


async def callbacks(query: CallbackQuery):
    if query.data.startswith(data_helper.get_value(buttons.Callback.general)):
        await general_callback(query)

    elif query.data.startswith(data_helper.get_value(buttons.Callback.status)):
        await status_callback(query)


async def general_callback(query: CallbackQuery):
    if isinstance(query.message, Message):
        message: Message = query.message

        if query.data == data_helper.get_value(buttons.Callback.dismiss):
            await dismiss_callback(message)

        elif query.data.startswith(data_helper.get_value(buttons.Callback.block)):
            await block_callback(message, query.data)

        elif query.data == data_helper.get_value(buttons.Callback.shutdown):
            await shutdown_callback(message)

        elif query.data == data_helper.get_value(buttons.Callback.restart):
            await restart_callback(message)


async def dismiss_callback(message: Message):
    await messages.delete_message_and_reply(message)


async def block_callback(message: Message, data: str):
    await messages.delete_message_and_reply(message)
    ip = data_helper.get_first_ip(data)
    commands.block_ip(ip)
    await messages.send_message(message.chat, strings.block_callback_text + ip)


async def shutdown_callback(message: Message):
    await messages.delete_message_and_reply(message)
    await messages.send_message(message.chat, strings.shutdown_callback_text)
    commands.shutdown_server()


async def restart_callback(message: Message):
    await messages.delete_message_and_reply(message)
    await messages.send_message(message.chat, strings.restart_callback_text)
    commands.restart_server()


async def status_callback(query: CallbackQuery):
    if isinstance(query.message, Message):
        message: Message = query.message
        query_data = query.data

        if query_data == data_helper.get_value(buttons.Callback.info):
            await info_callback(message)

        elif query_data == data_helper.get_value(buttons.Callback.cpus):
            await cpus_callback(message)

        elif query_data == data_helper.get_value(buttons.Callback.temps):
            await temps_callback(message)

        elif query_data == data_helper.get_value(buttons.Callback.ram):
            await ram_callback(message)

        elif query_data == data_helper.get_value(buttons.Callback.processes):
            await processes_callback(message)

        elif query_data == data_helper.get_value(buttons.Callback.net):
            await net_callback(message)

        elif query_data == data_helper.get_value(buttons.Callback.disks):
            await disks_callback(message)


async def info_callback(message: Message):
    await messages.edit_message(message, messages.info_message())


async def cpus_callback(message: Message):
    await messages.edit_message(message, messages.cpus_message())


async def temps_callback(message: Message):
    await messages.edit_message(message, messages.temps_message())


async def ram_callback(message: Message):
    await messages.edit_message(message, messages.ram_message())


async def processes_callback(message: Message):
    await messages.edit_message(message, messages.processes_message())


async def net_callback(message: Message):
    await messages.edit_message(message, messages.net_message())


async def disks_callback(message: Message):
    await messages.edit_message(message, messages.disks_message())
