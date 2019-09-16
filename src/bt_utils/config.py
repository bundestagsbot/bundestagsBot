from . import handleJson
from .console import *

BASE_PATH = "config/"
PATHS = ["blacklist.json", "main.json", "messages.json",
         "role_table.json", "tokens.json"]
SHL = Console("ConfigLoader", cls=True)


class Config:
    def __init__(self):
        self.options = {}
        self.reload()

    def reload(self, debug=False):
        SHL.output(f"Reloading config.")
        files_failed = 0
        for path in PATHS:
            SHL.output(f"Reloading configfile {BASE_PATH + path}")
            data = handleJson.readjson(BASE_PATH + path)
            if data is None:
                files_failed += 1
                continue
            for key, value in data.items():
                self.options[key] = value
                if debug:
                    SHL.output(f"[{key}]: {value}")
        SHL.output(f"{red}========================{white}")
        return files_failed


cfg = Config()
