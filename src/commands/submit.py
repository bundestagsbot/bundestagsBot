import os

from discord.utils import get

from bt_utils.console import Console
from bt_utils.embed_templates import WarningEmbed, SuccessEmbed, InfoEmbed
from bt_utils.config import cfg
from bt_utils import handleJson
from bt_utils.get_content import content_dir

SHL = Console("BundestagsBot Submit")

settings = {
    'name': 'submit',
    'channels': ['dm'],
    'log': False
}

path = os.path.join(content_dir, "submits.json")


async def main(client, message, params):
    try:
        last_id = save_json(message)
    except:
        SHL.output(f"Something went wrong while handling a submit.")
        error = WarningEmbed(title="Submit",
                             description="Something went wrong. Please contact an admin.")
        await message.channel.send(embed=error)
        return

    if not cfg.options["channel_ids"].get("suggestions", 0):
        error = WarningEmbed(title="Submit",
                             description="Your submit got saved. But could not be send.\nPlease contact an admin.")
        await message.channel.send(embed=error)
    else:
        embed = InfoEmbed(title=f"Submit #{last_id}", description=' '.join(params))
        channel = get(client.get_all_channels(), id=cfg.options["channel_ids"]["submits"])
        await channel.send(embed=embed)
        return_embed = SuccessEmbed(title=f"Submit #{last_id}",
                                    description="Thank your for your submission.\n"
                                                "If a team member answers it, I will forward the message :)")
        await message.channel.send(embed=return_embed)


def save_json(message):
    try:
        data = handleJson.read_json_raw(path)
    except FileNotFoundError:
        SHL.output("Submit file not found. Creating it.")
        file_dir = os.path.join(handleJson.BASE_PATH, os.path.dirname(path))
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        handleJson.saveasjson(path, {"latestID": 0})
        data = handleJson.read_json_raw(path)

    last_id = int(data.get("latestID", 0)) + 1
    data[last_id] = {}
    data[last_id]["author"] = str(message.author)
    data[last_id]["authorID"] = str(message.author.id)
    data[last_id]["text"] = ' '.join(str(message.content).split(' ')[1:])
    data[last_id]["answer"] = ""
    data[last_id]["answerfrom"] = ""
    data["latestID"] += 1

    handleJson.saveasjson(path, data)
    return last_id
