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
    rel_path = os.path.join(os.path.dirname(BASE_PATH), rel_path)
    try:
        with open(rel_path, 'r') as c:
            data = json.load(c)
    except FileNotFoundError:
        if debug: SHL.output(f"{rel_path} not found.")
        return
    except:
        if debug: SHL.output(f"Invalid JSON")
        return
    return data
