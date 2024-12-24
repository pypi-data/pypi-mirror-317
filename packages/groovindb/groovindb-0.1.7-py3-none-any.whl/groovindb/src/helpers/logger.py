import os
import json
from colorama import Fore, Style, init

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

def load_config():
    try:
        with open('groovindb.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Devuelve un diccionario vacío si el archivo no existe

class Logger:
    def __init__(self, name):
        config = load_config()
        # Usa "WARNING" como nivel de log predeterminado si no se encuentra la configuración
        self._name = name
        self._log_level = LOG_LEVELS.get(config.get('logger', {}).get('log_level', 'WARNING').upper(), 20)

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
