import os.path
import json

from bt_utils.console import Console
from bt_utils.get_content import content_dir
from bt_utils.embed_templates import InfoEmbed, SuccessEmbed

SHL = Console("BundestagsBot Analyze")  # Use SHL.output(text) for all console based output!

settings = {
    'name': 'analyze',  # name/invoke of your command
    'mod_cmd': False,  # if this cmd is only useable for users with the teamrole
    'channels': ['all'],  # allowed channels: [dm, bot, team, all]; use !dm to blacklist dm
    'log': True,  # if this cmd should be logged to the console, default: True
}

about_embed = InfoEmbed(title="Help")
with open(os.path.join("static", "info.txt"), "r", encoding="utf-8") as fh:
    about_embed.description = fh.read()


async def main(client, message, params):
    if any([x in message.content.lower() for x in ["help", "info", "details", "about"]]):
        await message.channel.send(embed=about_embed)
        return

    if "true" in message.content.lower():
        with open(os.path.join(content_dir, "unsubs.json"), "r") as fh:
            data = json.load(fh)
        try:
            data["unsub_ids"].remove(message.author.id)
        except ValueError:
            pass
        with open(os.path.join(content_dir, "unsubs.json"), "w") as fh:
            json.dump(data, fh)
        await message.channel.send(embed=SuccessEmbed(title="Analyzer",
                                                      description="Deine Nachrichten werden nun wieder erfasst."))
        return

    if "false" in message.content.lower():
        with open(os.path.join(content_dir, "unsubs.json"), "r") as fh:
            data = json.load(fh)
        if message.author.id not in data["unsub_ids"]:
            data["unsub_ids"].append(message.author.id)
        with open(os.path.join(content_dir, "unsubs.json"), "w") as fh:
            json.dump(data, fh)
        await message.channel.send(embed=SuccessEmbed(title="Analyzer",
                                                      description="Deine Nachrichten werden nun nicht erfasst.\n"
                                                                  "Um diesen Vorgang rückgängig zu machen verwende `_analyze true`."))
        return
