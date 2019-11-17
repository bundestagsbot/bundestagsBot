from datetime import datetime
import os

from . import handleJson
from .config import cfg
from .console import Console, red, white

SHL = Console("CacheHandler")


class Cache:
    def path(self):
        return os.path.join(cfg.options.get("path_to_temp_cache", "temp/"), "cache.json")

    def __init__(self):
        try:
            handleJson.saveasjson(self.path(), {})
            SHL.output("Cleared cache.")
        except FileNotFoundError:
            SHL.output("Cache file not found. Creating it.")
            cache_dir = os.path.join(handleJson.BASE_PATH,
                                     cfg.options.get('path_to_temp_cache', 'temp/'))
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
            handleJson.saveasjson(self.path(), {})

    def get_data(self, key=None):
        try:
            data = handleJson.read_json_raw(self.path())
            if key:
                if key in data.keys():
                    return data[key]
                else:
                    SHL.output(f"Key {key} not found.")
            return data
        except FileNotFoundError:
            SHL.output("Cache file not found. Creating it.")
            cache_dir = os.path.join(handleJson.BASE_PATH,
                                     cfg.options.get('path_to_temp_cache', 'temp/'))
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
            handleJson.saveasjson(self.path(), {})
            return {}
        except:
            SHL.output(f"Something went wrong while handling cache")
            return {}

    def write_to_cache(self, data, key=None, date=None):
        if key:
            SHL.output(f"Rewrite cache at key {key}")
        else:
            SHL.output(f"Rewrite cache")
        try:
            c = self.get_data()
            if key:
                c[key] = {}
                c[key]["data"] = data
                c[key]["timestamp"] = datetime.now().strftime("%Y.%m.%d")
                if date:
                    c[key]["timestamp"] = str(date)
            else:
                SHL.output(f"{red}Warning:{white} Rewriting whole cache!")
                c = data
            handleJson.saveasjson(self.path(), c)
        except:
            SHL.output("Something went wrong while writing the cache.")


cache = Cache()
SHL.output("Loaded CacheHandler")
SHL.output(f"{red}========================{white}")
