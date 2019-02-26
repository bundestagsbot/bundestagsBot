import discord
from discord.utils import get
from utils import handleJson
import requests
import json
import datetime


class prefixmgr():
    standard_prefix = ">"
    mod_cmd_prefix = "+"

roles = handleJson.readjson(path='C:/server/settings/roles.json')['roles']
roles.append('Grün')
# usable roles for >iam
commands = {}

allowed_channels = {
    'dm': {"cond": lambda message: isinstance(message.channel,discord.DMChannel), "name": "Dm"},
    'dev': {"cond": lambda message: message.channel.id == 546247189794652170, "name": ""},
    'bot': {"cond": lambda message: message.channel.id == 533005337482100736, "name": "<#533005337482100736>"},
}

def register(name, **kwargs):
    channels = kwargs.get("channels", ["bot"]) # if no channels are supplied the bot channel will be used
    if "dev" not in channels: channels.append("dev")
    #use ['all'] to allow all channels
    mod_cmd = kwargs.get("mod_cmd", False)
    prefix = prefixmgr.standard_prefix if not(mod_cmd) else prefixmgr.mod_cmd_prefix
    blacklisted = [channel[1:] for channel in channels if channel[0] == '!'] # use '!' to blacklist a channel instead of whitelisting
    if len(blacklisted) != 0: # if a channel is blacklisted
        channel_conds = [lambda message: not(any([allowed_channels[e]["cond"](message) for e in blacklisted]))]
        channel_names = []
        channels = [channel for channel in allowed_channels.keys() if channel not in blacklisted]

    elif channels[0] != 'all':
        channel_conds = [allowed_channels[channel]['cond'] for channel in channels]# always allow in dev channel
        channel_names = [allowed_channels[channel]['name'] for channel in channels if channel != 'dev'] # dont show devchannel as alternative
    else:
        channel_conds = [lambda x: True]
        channel_names = []
    def wrapper1(func):
        if mod_cmd:
            async def wrapper2(client, message):
                if user_in_team(message.author):
                    await func(client, message)
                else:
                    pass
        else:
            async def wrapper2(client, message):
                if any([e(message) for e in channel_conds]): # check if any of the given channels were used
                    await func(client, message)
                else:
                    if len(channel_names) != 0:
                        await message.channel.send(content='Benutze einen dieser Kanäle: ' + "".join(channel_names))
                    else:
                        await message.channel.send(content='Folgende Kanäle sind nicht zulässig: ' + "".join(blacklisted))
                print((str(datetime.datetime.now())[:-7]) + " " + str(message.author) + ' used ' + message.content) # logging
        commands[prefix + name] = wrapper2
        print('\033[92m' + (str(datetime.datetime.now())[:-7]) + f' \033[92m[BundestagsBot] registered {name} {kwargs}')
        return wrapper2
    return wrapper1

@register("roles", channels=["bot"])
async def roles_command(client, message): # 'roles' was taken
    embed = discord.Embed(title='Rollen Übersicht', color=discord.colour.Colour.orange())
    desc = 'Insgesamt hat der Server ' + str(client.get_guild(531445761733296130).member_count) + ' Mitglieder.\n\n'
    for r in [e for e in roles if e != 'nsfw']:
        role = get(client.get_guild(531445761733296130).roles, name=r[0].upper() + r[1:].lower())
        desc += role.name + ': ' + str(len(role.members)) + '.\n'
    embed.description = desc
    embed.timestamp = datetime.datetime.utcnow()
    await message.channel.send(embed=embed)

@register("iam")
async def iam(client, message):
    role = str(message.content)[len(prefixmgr.standard_prefix + "iam"):].strip()
    if role.lower() in [e.lower() for e in roles]:
        role = get(client.get_guild(531445761733296130).roles, name=role[0].upper()+role[1:].lower())
        await message.author.add_roles(role)
        await message.channel.send(content=message.author.mention + ' Rolle ' + role.name + ' hinzugefügt.')
    else:
        await message.channel.send(content='Please use one of the following roles: ```\n' + '\n'.join([e for e in roles if e != 'nsfw']) + ' ```')
        # nsfw verheimlichen ^.^

@register("umfrage", channels=['bot', 'dm'])
async def umfrage(client, message):
    if str(message.content)[len(prefixmgr.standard_prefix + "umfrage"):].strip() != '':
        embed = createembed(int(str(message.content)[len(prefixmgr.standard_prefix+"umfrage"):].strip()))
    else:
        embed = createembed()
    await message.channel.send(embed=embed)

@register("help", channel=["all"])
async def help(client, message):
    if str(message.content).strip() == prefixmgr.standard_prefix + 'help survey':
        embed = surveyhelpembed()
    else:
        embed = helpembed()
    await message.channel.send(embed=embed)

@register("warn", mod_cmd=True)
async def warn(client, message):
    badbois = str(message.content)[5:].strip()
    for member in client.get_all_members():
        if member.mention == badbois:
            badboi = member
    vorbestraft = False
    for role in badboi.roles:
        if role.name == 'ErsteVerwarnung':
            vorbestraft = True
            await message.channel.send(content='Benutzer wurde bereits einmal verwarnt!')
            break
    if not vorbestraft:
        await message.channel.send(content=badboi.mention + ' verwarnt!')
        punishrole = get(client.get_guild(531445761733296130).roles, id=533336650139435021)
        await badboi.add_roles(punishrole)

@register("survey;", channels=["!dm"])
async def survey(client, message):
    # aufbau: survey title text answers
    # answers 0 für antwort ja/nein
    # >1 für zaheln von 0-10 damit man dann im text schreibt 1:x 2:y 3:z 4:a 5:b 6:c und die leute dann deutlich mehr zur auswahl haben
    args = str(message.content).split(';')

    if len(args) in range(3, 5):
        embed = createsurvey(args[1], args[2], message.author)
        if len(args) == 4 and args[3] != '':
            args[3] = args[3].strip()
            if args[3].isdigit():
                msg = await message.channel.send(embed=embed)
                if int(args[3]) in range(3, 10):
                    emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
                    for e in range(0, int(args[3])):
                        await msg.add_reaction(emojis[e])
                elif int(args[3]) in range(0, 3):
                    await msg.add_reaction('✅')
                    await msg.add_reaction('❌')
                else:
                    await message.channel.send(content="Bitte gib eine gültige Zahl ein (3-9)..")
            else:
                await message.channel.send(content="Bitte gib eine gültige Zahl ein (3-9).")
        elif len(args) == 3 or args[3] == '':
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction('✅')
            await msg.add_reaction('❌')
        else:
            await message.channel.send(content="Ungültige Anzahl an Argumenten. Benutze >survey; title; text; answers")
    else:
        await message.channel.send(content="Ungültige Anzahl an Argumenten. Benutze >survey; title; text; answers")

def createsurvey(title,text,author):
    embed = discord.Embed(title='Umfrage: ' + title,color=discord.Colour.green(),url='https://github.com/zaanposni/bundestagsBot')
    embed.timestamp = datetime.datetime.utcnow()
    embed.description = text.replace('|','\n')
    embed.set_footer(text="Umfrage von " + author.name)
    return embed

def helpembed():
    embed = discord.Embed(title='Hilfe - BundestagsBot v1', color=discord.colour.Colour.orange())
    embed.set_thumbnail(url='https://cdn0.iconfinder.com/data/icons/handdrawn-ui-elements/512/Question_Mark-512.png')
    embed.description = '-Benutze >survey; Titel; Beschreibung; <Anzahl> um eine Umfrage zu erstellen. >help survey für mehr Details\n\n'\
                        '-Benutze >iam [Politik] um dir diese Rolle zuzuweisen.\n\n'\
                        '-Benutze >roles für eine Übersicht der Rollenverteilung\n\n'\
                        '-Benutze >umfrage [Parlamentsnummer]\nKeine Nummer für Bundestag'\


    embed.add_field(name='Liste:', value='0: Bundestag\n1: Baden-Württemberg\n2: Bayern\n3: Berlin\n4: Brandeburg\n5: Bremen\n6: Hamburg\n7: Hessen\n8: Mecklenburg-Vorpommern\n9: Niedersachsen\n10: NRW\n11: Rheinland-Pfalz\n12: Saarland\n13: Sachsen\n14: Sachsen-Anhalt\n15: Schleswig-Holstein\n16: Thüringen\n17: Europäisches Parlament')
    return embed

def surveyhelpembed():
    embed = discord.Embed(title='Hilfe - BundestagsBot v1', color=discord.colour.Colour.orange())
    embed.set_thumbnail(url='https://cdn0.iconfinder.com/data/icons/handdrawn-ui-elements/512/Question_Mark-512.png')

    embed.description = '>survey Titel Beschreibung <Anzahl>\n'\
                        'Anzahl ist optional und beschreibt die Anzahl an Reactionmöglichkeiten.\n'\
                        'So erzeugt >survey; Titel; Beschreibung; 5 eine Umfrage mit 5 Antwortmöglichkeiten, die du\n'\
                        'dann in deiner Beschreibung erklären musst.\n'\
                        'Beachte bitte die Trennung der Argumente via Semikolon!'
    return embed

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

def user_in_team(user):
    for role in user.roles:
        if role.name == 'Team':
            return True
    return False


