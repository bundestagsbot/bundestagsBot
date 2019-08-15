from bt_utils import handleJson
from bt_utils.console import Console

BASE_PATH = "config/"
PATHS = ["blacklist.json", "main.json", "messages.json",
         "role_table.json", "tokens.json"]
SHL = Console("ConfigLoader")


class Config:
    options = {}

    def reload(self, debug=False):
        SHL.output(f"Reloading config.")
        for path in PATHS:
            SHL.output(f"Reloading configfile {BASE_PATH + path}")
            data = handleJson.readjson(BASE_PATH + path)
            for key, value in data.items():
                self.options[key] = value
                if debug:
                    SHL.output(f"[{key}]: {value}")


cfg = Config()
