"""
File to store all the 'strings' and patterns of the bot, so they can be easily modified across the entire program
"""
from re import Pattern

# FIXME
network_error: str = 'Network error when starting polling, retrying: #'
no_registers: str = 'No registers'
number_threads_1: str = 'Number of threads: #'
number_threads_2: str = ' (including this)'
localhost: str = '127.0.0.1'
unspecified: str = '0.0.0.0'
local_net: str = '192.168.'
process_pid: str = 'pid'
process_name: str = 'name'
process_username: str = 'username'
process_memory_percent: str = 'memory_percent'
process_cpu_num: str = 'cpu_num'
process_cmdline: str = 'cmdline'
process_cpu_percent: str = 'cpu_percent'

# General strings
empty: str = ''
space: str = ' '
none: str = 'None'
break_line: str = '\n'
colon: str = ':'
hyphen: str = '-'
triple_dots: str = '...'
question_mark: str = '?'

# Logs
log_folder: str = 'logs/'
log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Commands
command_start: str = 'start'
command_stop: str = 'stop'
command_status: str = 'status'
command_speedtest: str = 'speedtest'
command_top: str = 'top'
command_block: str = 'block'
command_restart: str = 'restart'
command_shutdown: str = 'shutdown'
command_help: str = 'help'

# Units indicators
degrees: str = '°'
percent: str = '%'
byte: str = 'B'
kibibyte: str = 'KiB'
mebibyte: str = 'MiB'
gibibyte: str = 'GiB'

# Date information
date_separator: str = '/'
year_sl: str = '%Y'
month_sl: str = '%m'
day_sl: str = '%d'

# Hour information
hour_separator: str = ':'
hour_sl: str = '%H'
minute_sl: str = '%M'
second_sl: str = '%S'

# Tags
code_open: str = '<code>'
code_close: str = '</code>'
a_open: str = '<a href="'
a_close_1: str = '">'
a_close_2: str = '</a>'

# Speedtest
speedtest_bash: str = 'speedtest'
utf_8: str = 'utf-8'

# SECTIONS

# Stop
stop_text: str = 'Are you sure you want to <b>stop the server bot</b>?'
stop_button_text: str = ':stop_sign: Stop'
stop_callback_text: str = 'Stopping...'

# Top
top_text: str = ':1st_place_medal: Top access tries' + break_line + break_line

# Safety
auth_log: str = '/var/log/auth.log'
warning_title: str = ':warning: WARNING'
location_text: str = 'Location'

# Dismiss
dismiss_button_text: str = ':cross_mark: Dismiss'

# Back
back_button_text: str = '🔙 Back'

# Info
info_text: str = ':information: Info'

# CPUs
cpus_text: str = ':desktop_computer: CPUs' + break_line + break_line
cpus_button_text: str = ':desktop_computer: CPUs'

# Temperatures
temps_text: str = ':thermometer: Temperatures' + break_line + break_line
temps_button_text: str = ':thermometer: Temps'
no_label: str = 'No label'

# RAM
ram_text: str = ':floppy_disk: RAM' + break_line + break_line
ram_button_text: str = ':floppy_disk: RAM'

# Processes
proc_text: str = ':bar_chart: Processes' + break_line + break_line
proc_button_text: str = ':bar_chart: Proc'

# Internet
net_text: str = ':chart_increasing: Internet' + break_line + break_line
net_button_text: str = ':chart_increasing: NET'

# Disks
disks_text: str = ':computer_disk: Disks' + break_line + break_line
disks_button_text: str = ':computer_disk: Disks'

# Speedtest
speedtest_wait_test: str = "Please, wait for the result"

# Block
block_text: str = 'Are you sure you want to <b>block the IP</b> '
block_button_text: str = ':shield: Block'
block_callback_text: str = 'IP Blocked: '

# Restart
restart_text: str = 'Are you sure you want to <b>restart the server</b>?'
restart_button_text: str = ':repeat_button: Restart'
restart_callback_text: str = 'Restarting...'

# Shutdown
shutdown_text: str = 'Are you sure you want to <b>shutdown the server</b>?'
shutdown_button_text: str = ':mobile_phone_off: Shutdown'
shutdown_callback_text: str = 'Shutting down...'

# Help
help_text: str = 'Server Telegram Bot' + break_line \
                 + break_line \
                 + 'Monitor the load, status and security of your server: ' \
                 + 'https://github.com/AlejandroFraga/server-telegram-bot' + break_line + break_line \
                 + 'This bot monitors the load, status and security of your server,' \
                 + 'and sends you messages informing about any problems or warnings' + break_line \
                 + break_line \
                 + 'Commands' + break_line \
                 + '/start - Start the bot after stopping or manual if already running' + break_line \
                 + '/stop - Stop the bot' + break_line \
                 + '/status - Status of the server (CPU, RAM...)' + break_line \
                 + '/speedtest - Internet speed test' + break_line \
                 + '/top - Top access tries to the server' + break_line \
                 + '/restart - Restart the server' + break_line \
                 + '/shutdown - Shutdown the server' + break_line \
                 + '/help - Bot manual' + break_line

# OTHERS

# Urls
iplocation_url: str = 'https://www.iplocation.net/ip-lookup?query='
ipfy_url: str = 'https://api.ipify.org'

# Patterns
ip_pattern: Pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
url_pattern: Pattern = r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
percent_pattern: Pattern = r'((\d*\.\d+|\d+)%)'
numbers_pattern: Pattern = r'((\d*\.\d+|\d+)[ ]*(?<![\"=\w])(?:[^\W_]+)(?![\"=\w]))'
isp_pattern: Pattern = r'(ISP:)[ ]*([\w=\-:()\t .]+)'
server_pattern: Pattern = r'(Server:)[ ]*([\w=\-:()\t .]+)'
