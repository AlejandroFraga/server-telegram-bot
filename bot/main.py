import BotManager
import sys

if len(sys.argv) > 2:
    botManager = BotManager.BotManager(int(sys.argv[1]), sys.argv[2])
    BotManager.start_working()
