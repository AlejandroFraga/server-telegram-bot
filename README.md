# Server [Telegram Bot][python-telegram-bot]

A telegram bot to monitor the load, status and security of your server, that sends you messages informing about any problems or warnings

## Table of contents

- [Description](#description)
- [Download and Instalation](#download-and-instalation)
- [Project Goals](#project-goals)
- [Posible future improvements](#posible-future-improvements)
- [Tools and libraries](#tools-and-libraries)

## Description

After I manually configured my personal server, I thought about the best way to monitor it.
The first thing that came to my mind was the utopia that the server monitored itself.
It would tell me who (at least the IP direction) is trying to connect to the the server as it happens whitout me having to login in and checking every time.
It would even give me the option to turn off or restart remotely the server at any time, but specially when such fraudulent behaviour is detected.
I would be able to do internet speed tests, to test latency and bandwith.
I would be able to retrieve live information on running processes and system utilization (CPU, memory, disks, network, sensors).
And all of this, without having to create my own webpage, app or portal in which see this information.
Saving me a lot of time and work creating the 

## Download and Instalation

```sh
$ wget https://raw.githubusercontent.com/AlejandroFraga/server-telegram-bot/main/install.sh -O install.sh; sudo chmod u+x install.sh; ./install.sh
```

## Project Goals

WIP

## Posible future improvements

 - - [ ] Command to see the access tries in detail
 - - [ ] Control message length limits

## Tools and libraries

### [python-telegram-bot][python-telegram-bot]

This library provides a pure Python interface for the Telegram Bot API. It's compatible with Python versions 3.6+.

You can install or upgrade python-telegram-bot with:

```sh
$ pip install python-telegram-bot --upgrade
```

Or you can install from source with:

```sh
$ git clone https://github.com/python-telegram-bot/python-telegram-bot --recursive
$ cd python-telegram-bot
$ python setup.py install
```

### [psutil][psutil]

psutil (process and system utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python. It is useful mainly for system monitoring, profiling and limiting process resources and management of running processes. It implements many functionalities offered by classic UNIX command line tools such as ps, top, iotop, lsof, netstat, ifconfig, free and others. psutil currently supports the following platforms:

- Linux
- Windows
- macOS
- FreeBSD, OpenBSD, NetBSD
- Sun Solaris
- AIX
...both 32-bit and 64-bit architectures. Supported Python versions are 2.6, 2.7 and 3.4+, PyPy 2.7 and 3.X.

You can install or upgrade psutil with:

```sh
$ pip install psutil --upgrade
```

### [Speedtest CLI][speedtest-cli]

Speedtest CLI brings the trusted technology and global server network behind Speedtest to the command line. Built for software developers, system administrators and computer enthusiasts alike, Speedtest CLI is the first official Linux-native Speedtest application backed by Ookla®.

You can install Speedtest CLI with:

```sh
$ sudo apt-get install gnupg1 apt-transport-https dirmngr
$ export INSTALL_KEY=379CE192D401AB61
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys $INSTALL_KEY
$ echo "deb https://ookla.bintray.com/debian generic main" | sudo tee  /etc/apt/sources.list.d/speedtest.list
$ sudo apt-get update
# Other non-official binaries will conflict with Speedtest CLI
# Example how to remove using apt-get
# sudo apt-get remove speedtest-cli
$ sudo apt-get install speedtest
```


[//]: # (All links)

[python-telegram-bot]: <https://github.com/python-telegram-bot/python-telegram-bot>
[psutil]: <https://github.com/giampaolo/psutil>
[server]: <http://alejandrofraga.me>
[speedtest-cli]: <https://www.speedtest.net/apps/cli>
[telegram]: <https://en.wikipedia.org/wiki/Telegram_(software)>
