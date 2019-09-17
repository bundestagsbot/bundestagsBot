from bt_utils.console import Console
from bt_utils.config import cfg
from bt_utils.embed_templates import InfoEmbed, NoticeEmbed
from bt_utils import handleJson

SHL = Console("BundestagsBot Resolve")

settings = {
    'name': 'resolve',
    'channels': ['team'],
    'mod_cmd': True,
    'log': True
}

path = 'content/submits.json'


async def main(client, message, params):
    error = NoticeEmbed(title="Resolve")
    info = InfoEmbed(title="Resolve")
    if len(str(message.content).split(' ')) == 2:
        submit_id = params[0][1:]
        if submit_id.isdigit():
            data = handleJson.read_json_raw(path)
            if submit_id in data.keys():
                info.description = f"Anfrage #{submit_id} ist von:\n" \
                                   f"{data[submit_id]['author']}\n" \
                                   f"{data[submit_id]['authorID']}"
                await message.channel.send(embed=info)
            else:
                error.description = f"#{submit_id} could not be assigned to a submit."
                await message.channel.send(embed=error)
        else:
            error.description = f"{submit_id} is an invalid ID."
            await message.channel.send(embed=error)
    else:
        error.description = f"Invalid syntax.\nPlease use {cfg.options['invoke_mod']}resolve #id"
        await message.channel.send(embed=error)

