from utils import handleJson
from discord.utils import get
import discord
import datetime

settings = {
    'name': 'respond',
    'channels': ['team'],
    'mod_cmd': True,
    'log': True
}

path = 'C:/server/settings/BoB/submits.json'


async def main(client, message, params):
    if len(str(message.content).split(' ')) >= 3:
        id = str(message.content).split(' ')[1][1:]
        if id.isdigit():
            data = handleJson.readjson(path)
            if id in data.keys():
                if data[id]["answer"] == "":
                    embed = createembed(id, data, message)
                    msg = await message.channel.send(embed=embed)
                    await msg.add_reaction('✅')
                    await msg.add_reaction('❌')

                    def check(reaction, user):
                        e = str(reaction.emoji)
                        return user == message.author and e.startswith(('✅', '❌'))

                    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                    if str(reaction.emoji).startswith('❌'):  return

                    authorID = data[id]["authorID"]
                    submitauthor = get(client.get_guild(531445761733296130).members, id=int(authorID))
                    await submitauthor.send(embed=embed)
                    await message.channel.send(content='Antwort abgeschickt!')

                    data[id]["answer"] = ' '.join(str(message.content).split(' ')[2:])
                    data[id]["answerfrom"] = str(message.author)
                    handleJson.saveasjson(path, data)

                else:
                    await message.channel.send(content=f'#{id} wurde schon von {data[id]["answerfrom"]} mit \n'+
                                               f'"{data[id]["answer"]}" beantwortet.')
            else:
                await message.channel.send(content=f'{id} konnte keiner Anfrage zugeordnet werden')
        else:
            await message.channel.send(content=f'{id} ist keine gültige ID')
    else:
        await message.channel.send(content='Ungültige Anzahl an Argumenten. Versuche +respond #id Antwort')


def createembed(id, data, message):

    embed = discord.Embed(title=f'Antwort auf Anfrage #{id}', color=discord.Color.dark_red())
    embed.timestamp = datetime.datetime.utcnow()
    embed.description = str(' '.join(str(message.content).split(' ')[2:])).strip()
    embed.set_footer(text=f'Antwort von {message.author.name}')

    return embed

    pass