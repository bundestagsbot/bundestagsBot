from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed
from bt_utils import handleJson

SHL = Console("BundestagsBot Queue")

settings = {
    'name': 'queue',
    'channels': ['dm', 'bot'],
}

path = "content/arena.json"


async def main(client, message, params):
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
