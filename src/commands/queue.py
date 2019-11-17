import os.path

from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed
from bt_utils import handleJson
from bt_utils.get_content import content_dir

SHL = Console("BundestagsBot Queue")

settings = {
    'name': 'queue',
    'channels': ['dm', 'bot'],
}

path = os.path.join(content_dir, "arena.json")


async def main(client, message, params):
    return  # not implemented right now
    data = handleJson.read_json_raw(path)
    success = SuccessEmbed(title="Queue")
    if message.author.id in data["queue"]:
        data["queue"].remove(message.author.id)
        success.description = "Removed you from queue"
    else:
        data["queue"].append(message.author.id)
        success.description = f"Added to queue. There are {len(data['queue'])} members in queue."
    await message.channel.send(embed=success)
    handleJson.saveasjson(path, data)
