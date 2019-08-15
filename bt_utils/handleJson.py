import json
import os

BASE_PATH = ""


def writejson(path, data):
    saveasjson(path, data)


def saveasjson(rel_path, data):
    if not BASE_PATH:
        print("Please set the BASE_PATH before.")
        return
    with open(os.path.join(os.path.dirname(BASE_PATH), rel_path), 'w') as outfile:
        json.dump(data, outfile)


def readjson(rel_path, debug=True):
    if not BASE_PATH:
        print("Please set the BASE_PATH before.")
        return
    rel_path = os.path.join(os.path.dirname(BASE_PATH), rel_path)
    try:
        with open(rel_path, 'r') as c:
            data = json.load(c)
    except FileNotFoundError:
        if debug: print(rel_path, ' not found.')
        return
    except:
        if debug: print('invalid json')
        return
    return data
