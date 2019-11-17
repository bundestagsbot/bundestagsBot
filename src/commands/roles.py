from discord.utils import get

from bt_utils.console import Console
from bt_utils.embed_templates import InfoEmbed
from bt_utils.config import cfg

SHL = Console("BundestagsBot Roles")

settings = {
    'name': 'roles',
    'channels': ['bot'],
}


async def main(client, message, params):
    roles = cfg.options["roles_show"]
    info = InfoEmbed(title="Roles")
    desc = 'This server has ' + str(client.get_guild(message.guild.id).member_count) + ' members.\n\n'
    for r in roles:
        role = get(message.guild.roles, name=r)
        desc += role.name + ': ' + str(len(role.members)) + '.\n'
    info.description = desc
    await message.channel.send(embed=info)
