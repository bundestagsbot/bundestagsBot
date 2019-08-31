from bt_utils.console import Console
from bt_utils.config import cfg
from bt_utils import handleJson
SHL = Console("Reset")


def reset():
    SHL.output("Resetting temp files.")
    # challenge json
    data = {"arena_status": 0, "participants": []}
    handleJson.saveasjson("content/challenge.json", data)

    # cache file
    handleJson.saveasjson(cfg.options.get("path_to_temp_cache", "temp/") + "cache.json", {})
