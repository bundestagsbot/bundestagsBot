from bt_utils.console import Console
from bt_utils.config import cfg
from bt_utils import handleJson
from bt_utils.handle_sqlite import DatabaseHandler
import os
SHL = Console("Reset")
DB = DatabaseHandler()


def reset_file(path, data):
    try:
        handleJson.saveasjson(path, data)
    except FileNotFoundError:
        SHL.output("File not found. Creating it.")
        file_dir = os.path.join(handleJson.BASE_PATH, os.path.dirname(path))
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        handleJson.saveasjson(path, data)


def reset():
    # content folder
    # ================================================
    content = os.path.join(handleJson.BASE_PATH, "content")
    if not os.path.exists(content):
        SHL.output("Creating content folder.")
        os.makedirs(content)

        SHL.output("Resetting challenge.json")
        reset_file("content/challenge.json", {"arena_status": 0, "participants": []})
        SHL.output("Resetting submits.json")
        reset_file("content/submits.json", {"latestID": 0})
        SHL.output("Resetting subs.json")
        reset_file("content/subs.json", {"unsubs": []})
        SHL.output("Resetting surveys.json")
        reset_file("content/surveys.json", {"latestID": 0})

    # cache file
    # ================================================
    SHL.output("Resetting cache file.")
    reset_file(cfg.options.get("path_to_temp_cache", "temp/") + "cache.json", {})

    # database related
    # ================================================
    roles = cfg.options["roles_stats"].values()

    # creates basic table structures if not already present
    DB.create_structure(roles)

    # updates table structure, e.g. if a new role has been added
    DB.update_columns(roles)
    SHL.output("Setup database completed")
