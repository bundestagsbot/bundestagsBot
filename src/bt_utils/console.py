from datetime import datetime
import os

black = '\033[30m' if os.isatty(0) else ""
red = '\033[31m' if os.isatty(0) else ""
green = '\033[32m' if os.isatty(0) else ""
yellow = '\033[33m' if os.isatty(0) else ""
blue = '\033[34m' if os.isatty(0) else ""
violet = '\033[35m' if os.isatty(0) else ""
beige = '\033[36m' if os.isatty(0) else ""
white = '\033[37m' if os.isatty(0) else ""
grey = '\033[90m' if os.isatty(0) else ""
red2 = '\033[91m' if os.isatty(0) else ""
green2 = '\033[92m' if os.isatty(0) else ""
yellow2 = '\033[93m' if os.isatty(0) else ""
blue2 = '\033[94m' if os.isatty(0) else ""
violet2 = '\033[95m' if os.isatty(0) else ""
beige2 = '\033[96m' if os.isatty(0) else ""
white2 = '\033[97m' if os.isatty(0) else ""


class Console:
    def ts(self, c=False):
        if c:
            return f'{yellow2}[{str(datetime.now()).split(".", 1)[0]}]{white}'
        return f'[{str(datetime.now()).split(".", 1)[0]}]'

    def set_prefix(self, prefix):
        self.prefix = f'{green2}[{prefix}]{white}'

    def __init__(self, prefix, cls=False):
        if cls and os.isatty(0):
            os.system("cls" if os.name == "nt" else "clear")
        self.prefix = f'{green2}[{prefix}]{white}'

    def output(self, text):
        print(f'{self.ts(True)} {self.prefix} {str(text)}')
