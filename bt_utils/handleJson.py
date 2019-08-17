from .console import Console
import json
import os
SHL = Console(prefix="handleJSON")

BASE_PATH = ""


def writejson(path, data):
    saveasjson(path, data)


def saveasjson(rel_path, data):
    if not BASE_PATH:
        SHL.output(f"Please set the BASE_PATH variable before.")
        return
    with open(os.path.join(os.path.dirname(BASE_PATH), rel_path), 'w') as outfile:
        json.dump(data, outfile)


def readjson(rel_path, debug=True):
    if not BASE_PATH:
        SHL.output(f"Please set the BASE_PATH variable before.")
        return
    path = os.path.join(os.path.dirname(BASE_PATH), rel_path)
    try:
        with open(path, 'r') as c:
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
    if not BASE_PATH:
        SHL.output(f"Please set the BASE_PATH variable before.")
        return
    rel_path = os.path.join(os.path.dirname(BASE_PATH), rel_path)
    with open(rel_path, 'r') as c:
        data = json.load(c)
    return data
