from utils.console import Console
import requests
import json
import discord
SHL = Console("BundestagsBot Umfrage")

settings = {
    'name': 'umfrage',
    'channels': ['dm', 'bot'],
}


async def main(client, message, params):
    if len(params) != 0:
        embed = createembed(int(params[0]))
    else:
        embed = createembed()
    await message.channel.send(embed=embed)


def createembed(parl=0):
    data = json.loads(requests.get('https://api.dawum.de/').text)
    for e in data['Surveys']:
        if int(data['Surveys'][e]['Parliament_ID']) == parl:
            last = e
            break

    embed = discord.Embed(title='Aktuelle Umfrage ' + data['Parliaments'][str(parl)]['Name'], color=discord.colour.Colour.dark_red())
    embed.description = 'Wahl: ' + data['Parliaments'][str(parl)]['Election'] +\
                        '\nUmfrage von: ' + data['Institutes'][data['Surveys'][last]['Institute_ID']]['Name'] + \
                        '\nUmfrage im Auftrag von: ' + data['Taskers'][data['Surveys'][last]['Tasker_ID']]['Name']
    embed.set_footer(text='Umfrage von: ' + str(data['Surveys'][last]['Date']))

    for e, party in enumerate(data['Surveys'][last]['Results']):
        embed.add_field(name=str(data['Parties'][party]['Name']),value=str(data['Surveys'][last]['Results'][party])+'%\n',inline=False)
    return embed
