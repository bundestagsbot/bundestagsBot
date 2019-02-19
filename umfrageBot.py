import discord
from utils import webhooks,handleJson,pushedNotification
import datetime
import json
import urllib
import subprocess
from dhooks import Webhook,Embed
import ssl
from discord.utils import get
import os

#testt

data = handleJson.readjson('Y:/settings/tokens.json')
TOKEN = data['TOKENS']['umfrageBot']
webhooklogs = webhooks.webhooks['logChannel']
prefix = '\033[92m[umfrageBot] '
firstconnection = True
tries_torec = 0

gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

client = discord.Client()

def helpembed():
    embed = discord.Embed(title='Hilfe - BundestagsBot v1', color=discord.colour.Colour.orange())
    embed.set_thumbnail(url='https://cdn0.iconfinder.com/data/icons/handdrawn-ui-elements/512/Question_Mark-512.png')
    embed.description = 'Benutze >umfrage [Parlamentsnummer]\nKeine Nummer für Bundestag'

    embed.add_field(name='Liste:', value='0: Bundestag\n1: Baden-Württemberg\n2: Bayern\n3: Berlin\n4: Brandeburg\n5: Bremen\n6: Hamburg\n7: Hessen\n8: Mecklenburg-Vorpommern\n9: Niedersachsen\n10: NRW\n11: Rheinland-Pfalz\n12: Saarland\n13: Sachsen\n14: Sachsen-Anhalt\n15: Schleswig-Holstein\n16: Thüringen\n17: Europäisches Parlament')
    return embed

def createembed(parl = 0):


    data = urllib.request.urlopen('https://api.dawum.de/',context=gcontext).read()

    for e in json.loads(data)['Surveys']:
        if int(json.loads(data)['Surveys'][e]['Parliament_ID']) == parl:
            last = e
            break


    embed = discord.Embed(title='Aktuelle Umfrage ' + json.loads(data)['Parliaments'][str(parl)]['Name'], color=discord.colour.Colour.dark_red())
    embed.description = 'Wahl: ' + json.loads(data)['Parliaments'][str(parl)]['Election'] +\
                        '\nUmfrage von: ' + json.loads(data)['Institutes'][json.loads(data)['Surveys'][last]['Institute_ID']]['Name'] + \
                        '\nUmfrage im Auftrag von: ' + json.loads(data)['Taskers'][json.loads(data)['Surveys'][last]['Tasker_ID']]['Name']
    embed.set_footer(text='Umfrage von: ' + str(json.loads(data)['Surveys'][last]['Date']))

    for e, party in enumerate(json.loads(data)['Surveys'][last]['Results']):
        embed.add_field(name=str(json.loads(data)['Parties'][party]['Name']),value=str(json.loads(data)['Surveys'][last]['Results'][party])+'%\n',inline=False)

    return embed

@client.event
async def on_message(message):
    if message.author == client.user:
        return 0
    if message.author.id == 272655001329991681:
        emoji = client.get_emoji(545649937598119936)
        await message.add_reaction(emoji)

    if str(message.content).startswith('>umfrage'):
        #absofort nur noch im botchannel amk xD
        if message.channel.id == 533005337482100736 or isinstance(message.channel,discord.DMChannel):
            print((str(datetime.datetime.now())[:-7]) + prefix + str(message.author) + ' used ' + message.content)
            if str(message.content)[8:].strip() != '': embed = createembed(int(str(message.content)[8:].strip()))
            else: embed = createembed()
            await message.channel.send(embed=embed)
        else:
            print((str(datetime.datetime.now())[:-7]) + prefix + str(message.author) + ' used ' + message.content)
            await message.channel.send(content='Please use <#533005337482100736>')


    if message.content == '>help':
        if message.channel.id == 533005337482100736 or isinstance(message.channel,discord.DMChannel):
            print((str(datetime.datetime.now())[:-7]) + prefix + str(message.author) + ' used ' + message.content)
            embed = helpembed()
            await message.channel.send(embed=embed)
        else:
            print((str(datetime.datetime.now())[:-7]) + prefix + str(message.author) + ' used ' + message.content)
            await message.channel.send(content='Please use <#533005337482100736>')

    if str(message.content).startswith('+warn'):

        for role in message.author.roles:
            if role.name == 'Team':
                badbois = str(message.content)[5:].strip()

                for member in client.get_all_members():
                    if member.mention == badbois:
                        badboi = member

                vorbestraft = False
                for role in badboi.roles:
                    if role.name == 'ErsteVerwarnung':
                        vorbestraft = True
                        await message.channel.send(content='Benutzer wurde bereits einmal verwarnt!')

                if not vorbestraft:
                    await message.channel.send(content=badboi.mention + ' verwarnt!')

                    punishrole = get(client.get_guild(531445761733296130).roles, id=533336650139435021)

                    await badboi.add_roles(punishrole)



    return

@client.event
async def on_ready():
    # console related
    # ================================================

    subprocess.call('cls', shell=True)
    print('\033[92m' + (str(datetime.datetime.now())[:-7]) + prefix + 'Logged in as')
    print((str(datetime.datetime.now())[:-7]) + prefix + client.user.name)
    print((str(datetime.datetime.now())[:-7]) + prefix + str(client.user.id))
    print((str(datetime.datetime.now())[:-7]) + prefix + '------')

    # discord related
    # ================================================

    game1 = discord.Game(name='>umfrage')
    await client.change_presence(activity=game1)

    # ================================================
    hook = Webhook(webhooklogs)

    # ================================================

    embed = Embed(
        title='umfrageBot - Status',
        description='I am ready again!',
        thumbnail_url='https://i0.wp.com/www.activate-the-beast.com/wp-content/uploads/2015/05/Ern%C3%A4hrung-Umfrage-Icon-e1432756685893.png?fit=300%2C300',
        color=0x6eff33
    )

    hook.send(embed=embed)
    pushedNotification.sendNot('BundestagBot: I am ready again!')

    # script related
    #================================================


client.run(TOKEN,reconnect=True)
