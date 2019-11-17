import json
import os

from .console import Console

SHL = Console(prefix="handleJSON")

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def writejson(path, data):
    saveasjson(path, data)


def saveasjson(rel_path, data):
    with open(os.path.join(BASE_PATH, rel_path), 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile)


def readjson(rel_path, debug=True):
    path = os.path.join(BASE_PATH, rel_path)
    try:
        with open(path, 'r', encoding="utf-8") as c:
            data = json.load(c)
    except FileNotFoundError:
        if debug: SHL.output(f"{path} not found.")
        return
    except:
        if debug: SHL.output(f"Invalid JSON")
        return
    return data


def read_json_raw(rel_path):
    """
    Warning: This function does not handle errors!
    :param rel_path: relative path which get combined with BASE_PATH
    :return: dict or None
    """
    rel_path = os.path.join(BASE_PATH, rel_path)
    with open(rel_path, 'r', encoding="utf-8") as c:
        data = json.load(c)
    return data
