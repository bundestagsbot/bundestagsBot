import discord
import datetime
from discord.utils import get

settings = {
    'name': 'roles',
    'channels': ['bot'],
}

roles = ['Liberal', 'Konservativ', 'Sozialdemokratisch', 'Sozialistisch', 'Nationalistisch', 'nsfw', 'Sozialliberal', 'Wirtschaftsliberal', 'Grün']
# usable roles

async def main(client, message, params):
    embed = discord.Embed(title='Rollen Übersicht', color=discord.colour.Colour.orange())
    desc = 'Insgesamt hat der Server ' + str(client.get_guild(531445761733296130).member_count) + ' Mitglieder.\n\n'
    for r in [e for e in roles if e != 'nsfw']:
        role = get(client.get_guild(531445761733296130).roles, name=r.capitalize())
        desc += role.name + ': ' + str(len(role.members)) + '.\n'
    embed.description = desc
    embed.timestamp = datetime.datetime.utcnow()
    await message.channel.send(embed=embed)