from bt_utils import handleJson
from bt_utils.console import Console

PATHS = ["config/blacklist.json", "config/main.json", "config/messages.json",
         "config/role_table.json", "config/tokens.json"]
SHL = Console("ConfigLoader")


class Config:
    options = {}

    def reload(self, debug=False):
        SHL.output(f"Reloading config.")
        for path in PATHS:
            SHL.output(f"Reloading configfile {path}")
            data = handleJson.readjson(path)
            for key, value in data.items():
                self.options[key] = value
                if debug:
                    SHL.output(f"[{key}]: {value}")


cfg = Config()
