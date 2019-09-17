from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed, NoticeEmbed, ErrorEmbed
from bt_utils.config import cfg
from bt_utils import handleJson
import os
SHL = Console("BundestagsBot Sub")

settings = {
    'name': 'sub',
    'channels': ['dm', 'bot'],
}

path = 'content/subs.json'


async def main(client, message, params):
    error = NoticeEmbed(title="Sub")
    success = SuccessEmbed(title="Sub")
    try:
        if len(str(message.content).split(' ')) == 2:
            sub = str(message.content).split(' ')[1]
            if sub.lower() in ['yes', 'no', 'ja', 'nein', 'true', 'false']:
                if ['yes', 'no', 'ja', 'nein', 'true', 'false'].index(sub.lower()) % 2 == 0:  # resubs
                    subs(True, message.author.id)
                    success.description = "Done."
                    await message.channel.send(embed=success)
                else:  # unsubs
                    subs(False, message.author.id)
                    success.description = f"Done.\nYou can resubscribe by typing {cfg.options['invoke_normal']}sub True"
                    await message.channel.send(embed=success)
            else:
                error.description = f"Invalid syntax.\nPlease use {cfg.options['invoke_normal']}sub True|False"
                await message.channel.send(embed=error)
        else:
            error.description = f"Invalid syntax.\nPlease use {cfg.options['invoke_normal']}sub True|False"
            await message.channel.send(embed=error)
    except:
        error = ErrorEmbed(title="Sub")
        SHL.output(f"Something went wrong while handling a sub.")
        error.description = "Something went wrong. Please contact an admin."
        await message.channel.send(embed=error)


def subs(sub, user_id):
    try:
        data = handleJson.read_json_raw(path)
    except FileNotFoundError:
        SHL.output("Sub file not found. Creating it.")
        file_dir = os.path.join(handleJson.BASE_PATH, os.path.dirname(path))
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        handleJson.saveasjson(path, {})
        data = handleJson.read_json_raw(path)

    if sub:
        if user_id in data["unsubs"]:
            data["unsubs"].remove(user_id)
    else:
        if user_id not in data["unsubs"]:
            data["unsubs"].append(user_id)

    handleJson.saveasjson(path, data)
