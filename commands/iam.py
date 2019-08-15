from bt_utils.console import Console
from bt_utils.config import cfg
from discord.utils import get
SHL = Console("BundestagsBot Iam")

settings = {
    'name': 'iam',
    'channels': ['bot'],
}


async def main(client, message, params):
    roles = cfg.options["roles"] + ["Nsfw"]
    lower_roles = [e.lower() for e in roles]

    want_role = ' '.join(params).strip().lower()
    if want_role in lower_roles:
        assign_role = roles[lower_roles.index(want_role)]
        role = get(client.get_guild(531445761733296130).roles, name=assign_role)
        if role not in message.author.roles:
            await message.author.add_roles(role)
            await message.channel.send(content=message.author.mention + ' Rolle ' + role.name + ' hinzugefügt.')
        else:
            await message.author.remove_roles(role)
            await message.channel.send(content=message.author.mention + ' Rolle ' + role.name + ' entfernt.')
    else:
        await message.channel.send(content='Bitte benutze eine dieser Rollen:'
                                           ' ```\n' + '\n'.join([e for e in roles if e != 'Nsfw']) + ' ```')
