from bt_utils.console import Console
from bt_utils.config import cfg
import discord
import datetime
from discord.utils import get
SHL = Console("BundestagsBot Roles")

settings = {
    'name': 'roles',
    'channels': ['bot'],
}


async def main(client, message, params):
    roles = cfg.options["roles_show"]
    embed = discord.Embed(title='Rollen Übersicht', color=discord.colour.Colour.orange())
    desc = 'Insgesamt hat der Server ' + str(client.get_guild(531445761733296130).member_count) + ' Mitglieder.\n\n'
    for r in [e for e in roles if e != 'nsfw']:
        role = get(client.get_guild(531445761733296130).roles, name=r.capitalize())
        desc += role.name + ': ' + str(len(role.members)) + '.\n'
    embed.description = desc
    embed.timestamp = datetime.datetime.utcnow()
    await message.channel.send(embed=embed)
