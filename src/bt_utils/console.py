from datetime import datetime
import os

black = '\033[30m'
red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'
blue = '\033[34m'
violet = '\033[35m'
beige = '\033[36m'
white = '\033[37m'
grey = '\033[90m'
red2 = '\033[91m'
green2 = '\033[92m'
yellow2 = '\033[93m'
blue2 = '\033[94m'
violet2 = '\033[95m'
beige2 = '\033[96m'
white2 = '\033[97m'


class Console:
    def ts(self, c=False):
        if c:
            return f'{yellow2}[{str(datetime.now()).split(".", 1)[0]}]{white}'
        return f'[{str(datetime.now()).split(".", 1)[0]}]'

    def set_prefix(self, prefix):
        self.prefix = f'{green2}[{prefix}]{white}'

    def __init__(self, prefix, cls=False):
        if cls:
            os.system("cls" if os.name == "nt" else "clear")
        self.prefix = f'{green2}[{prefix}]{white}'

    def output(self, text):
        print(f'{self.ts(True)} {self.prefix} {str(text)}')
