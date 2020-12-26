"""
Some functions to help rest of the game process and treat data easily
"""
import re
import time
from enum import Enum

import strings

kb = 1024
mb = kb * kb
gb = mb * kb


def safe_cast(val, to_type, default=None):
    """
    Safe cast to the desired type, returning the default value if the
    cast can't be successfully done

    :param val: value to be casted
    :param to_type: type to be casted
    :param default: default value to return in case of can't cast the value to the type
    :return: The value casted to the type, default value if can't be done
    """

    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def is_(var: any, v_type: type = None):
    """

    :param var:
    :param v_type:
    :return:
    """

    return type(var) is v_type


def is_int(number):
    """
    Check if the given number is an int

    :param number: Number to check
    :return: The result of the check
    """
    return type(number) is int


def is_float(number):
    """
    Check if the given number is a float

    :param number: Number to check
    :return: The result of the check
    """
    return type(number) is float


def is_number(number):
    """
    Check if the given number is a number (int or float)

    :param number: Number to check
    :return: The result of the check
    """
    return is_int(number) or is_float(number)


def is_str(string):
    """
    Check if the given string is an str

    :param string: String to check
    :return: The result of the check
    """
    return type(string) is str


def is_tuple(var):
    """
    Check if the given variable is a tuple

    :param var: Variable to check
    :return: The result of the check
    """
    return type(var) is tuple


def is_list(var):
    """
    Check if the given variable is a list

    :param var: Variable to check
    :return: The result of the check
    """
    return type(var) is list


def is_list_of_min_size(var, min_size: int = 1):
    """
    Check if the given variable is a list with the given size

    :param var: Variable to check
    :param min_size: Minimal size of the list
    :return: The result of the check
    """
    return is_list(var) and is_number(min_size) and var.__len__() >= min_size


def is_list_of_size(var, size):
    """
    Check if the given variable is a list with the given size

    :param var: Variable to check
    :param size: Size of the list
    :return: The result of the check
    """
    return is_list(var) and is_number(size) and var.__len__() == size


def get_value(enum=None) -> str:
    return str(enum.value) if isinstance(enum, Enum) else enum


def get_hour(sp: str = strings.hour_separator):
    return time.strftime(strings.hour_sl + sp + strings.minute_sl + sp + strings.second_sl, time.localtime())


def get_date(sp: str = strings.date_separator):
    return time.strftime(strings.day_sl + sp + strings.month_sl + sp + strings.year_sl, time.localtime())


def get_date_hour():
    return '[' + get_date() + ' - ' + get_hour() + ']'


def format_temp(value: float):
    if is_number(value):
        return str(round(value, 2)) + strings.degrees
    return strings.none


def format_percent(value: any = None, base: int = 100):
    if is_number(value):
        return str(round(value / base * 100, 2)) + strings.space + strings.percent

    elif is_str(value):
        return value + strings.space + strings.percent

    return strings.none


def format_bytes(value: float = None):
    if is_number(value):
        if value <= kb:
            return to_b(value)
        elif value <= mb:
            return to_kb(value)
        elif value <= gb:
            return to_mb(value)
        else:
            return to_gb(value)
    return strings.none


def to_b(value):
    return str(round(value, 2)) + strings.space + strings.byte


def to_kb(value):
    return str(round(value / kb, 2)) + strings.space + strings.kibibyte


def to_mb(value):
    return str(round(value / mb, 2)) + strings.space + strings.mebibyte


def to_gb(value):
    return str(round(value / gb, 2)) + strings.space + strings.gibibyte


def format_table_row(text: str = None, values: any = None, col_size: int = 12,
                     separator: bool = True, end_line: bool = True):
    result = strings.code_open

    if text is not None:
        result += text + (strings.colon if separator else strings.empty)

    if is_list(values):
        i = 1
        for value in values:
            tab = col_size * i

            while result.__len__() - strings.code_open.__len__() < tab:
                result += strings.space

            result += str(value)
            i += 1
    elif values is not None:
        while result.__len__() - strings.code_open.__len__() < col_size:
            result += strings.space

        result += str(values)

    result += strings.code_close

    result += strings.break_line if end_line else ''

    return result


def format_link(text: str = None, link: str = None, end_line: bool = True) -> str:
    result = strings.empty

    if is_str(text) and is_str(link):
        result += strings.a_open + link + strings.a_close_1 + text + strings.a_close_2

    result += strings.break_line if end_line else ''

    return result


def get_first_ip(line: str):

    if line is not None:

        ip_pattern = re.compile(strings.ip_pattern)
        ips = re.search(ip_pattern, line)

        if ips is not None and ips.__sizeof__() > 0:
            return ips[0]

    return None


def __find_server(text: str) -> str:
    found = re.findall(strings.server_pattern, text)

    if is_list_of_min_size(found, 1):
        return found[0][1].strip()

    return strings.empty


def __find_isp(text: str) -> str:
    found = re.findall(strings.isp_pattern, text)

    if is_list_of_min_size(found, 1):
        return found[0][1].strip()

    return strings.empty


def __find_numbers(text: str) -> [str]:
    found = re.findall(strings.numbers_pattern, text)

    if is_list_of_min_size(found, 6):
        return [found[0][0].strip(), found[2][0].strip(), found[4][0].strip()]

    return []


def __find_loss(text: str) -> str:
    found = re.findall(strings.percent_pattern, text)

    if is_list_of_min_size(found, 1):
        return found[0][0].strip()

    return strings.empty


def __find_url(text: str) -> str:
    found = re.findall(strings.url_pattern, text)

    if is_list_of_min_size(found, 1):
        return found[0].strip()

    return strings.empty


def format_speedtest(text: str) -> str:
    result = ':chart_increasing: Speedtest by Ookla®\n\n'

    result += format_table_row('Server', __find_server(text))

    result += format_table_row('ISP', __find_isp(text))

    found = __find_numbers(text)

    if is_list_of_min_size(found, 3):
        result += format_table_row('Ping', found[0])
        result += format_table_row('Download', found[1])
        result += format_table_row('Upload', found[2])

    result += format_table_row('Loss', __find_loss(text)) + '\n'

    result += format_link('See result', __find_url(text), False)

    return result


def get_map(new_map, total):
    string = "\nTOP ACCESS TRIES\n----------------\n\n"

    i = 0
    limit = 25

    for chain in new_map:
        i += 1
        string += "TOP " + str(i) + " " + str(chain) + "\n"
        if i >= limit:
            break

    string += "\nTOTAL\n-----\n" + str(total) + "\n"
    return string
