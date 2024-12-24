import os

from colorama import Fore, Style, init
from dotenv import load_dotenv

load_dotenv()
init(autoreset=True)

LOG_LEVELS = {
    'DEBUG': 0,
    'INFO': 10,
    'WARNING': 20,
    'ERROR': 30,
    'CRITICAL': 40
}

LOG_COLORS = {
    'DEBUG': Fore.BLUE,
    'INFO': Fore.GREEN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
    'CRITICAL': Fore.MAGENTA
}


class Logger:
    def __init__(self, name):
        self._name = name
        self._log_level = LOG_LEVELS.get(os.getenv('LOG_LEVEL', 'INFO').upper(), 20)

    def _log(self, level, msg, *args, **kwargs):
        if level >= self._log_level:
            if args:
                msg = msg % args
            color = LOG_COLORS.get(list(LOG_LEVELS.keys())[list(LOG_LEVELS.values()).index(level)], "")
            print(f"{self._name} - {color}{msg}{Style.RESET_ALL}")

    def debug(self, message, *args, **kwargs):
        self._log(LOG_LEVELS["DEBUG"], f"DEBUG: {message}", *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self._log(LOG_LEVELS["INFO"], f"INFO: {message}", *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self._log(LOG_LEVELS["WARNING"], f"WARNING: {message}", *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self._log(LOG_LEVELS["ERROR"], f"ERROR: {message}", *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self._log(LOG_LEVELS["CRITICAL"], f"CRITICAL: {message}", *args, **kwargs)


logger = Logger("Colppy")
