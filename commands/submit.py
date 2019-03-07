from discord.utils import get
import discord
import datetime

settings = {
    'name': 'submit',
    'channels': ['all'],
    'log': False
}

path = 'C:/server/settings/surveys.json'


async def main(client, message, params):

    channel = get(client.get_guild(531445761733296130).channels, id=545330367150817310)
    embed = createembed(''.join(str(message.content).split(' ')[1:]))
    await channel.send(embed=embed)
    await message.channel.send(content="Danke für deine Nachricht. Sie wurde anonym ans Team weitergeleitet.")


def createembed(content):
    embed = discord.Embed(title='Anfrage ans Serverteam', color=discord.Color.dark_red())
    embed.timestamp = datetime.datetime.utcnow()
    embed.description = content

    return embed
