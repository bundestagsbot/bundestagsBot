from discord.utils import get
import discord
from utils import webhooks, handleJson, pushedNotification
import datetime
import subprocess
from dhooks import Webhook, Embed

prefix = ' \033[92m[BundestagsBot] '
print('\033[92m' + (str(datetime.datetime.now())[:-7]) + prefix + 'started BundestagsBot')
subprocess.call('cls', shell=True)
import commands

blacklist = handleJson.readjson('C:/server/settings/BoB/botblacklist.json')["blacklist"]
data = handleJson.readjson('C:/server/settings/tokens.json')
TOKEN = data['TOKENS']['umfrageBot']
webhooklogs = webhooks.webhooks['logChannel']
webhooklogsBoB = webhooks.webhooks['logChannelBoB']
firstconnection = True
tries_torec = 0
client = discord.Client()

commands.prefix.standard = '>'
commands.prefix.mod = '+'


roles = {
    "607450684673097780": "Finanzen",
    "607463294172659723": "Außenpolitik",
    "607450685054910465": "Justiz",
    "607451205266046976": "Militär",
    "607450684521971714": "Familie & Jugend",
    "607450686497488902": "Verkehr & Infrastruktur",
    "607450685146923009": "Bildung & Forschung",
    "607451624255913992": "Innenpolitik",
    "607450685788913664": "Wirtschaft",
    "607450685335666698": "Arbeit & Soziales",
    "607450685067231232": "Ernährung & Landwirtschaft",
    "607450684954116107": "Gesundheit",
    "607450685398712358": "Umwelt & Naturschutz",
    "607450684723560470": "Entwicklungshilfe",

    "607450685457563648": "Liberal",
    "607450685260431380": "Konservativ",
    "546318962632294420": "Sozialdemokratisch",
    "607453558031384576": "Sozialistisch",
    "607450685327278080": "Nationalistisch",
    "607463294805999616": "Sozialliberal",
    "607463295288344576": "Wirtschaftsliberal",
    "607463295741460480": "Grün",
    "607463295372361729": "Patriotisch",

    "607943313794007055": "Podcast"
}


def createembed():
    embed = discord.Embed(title=f'Willkommen!', color=discord.Color.dark_red(),
                          url="https://github.com/zaanposni/bundestagsBot")
    embed.timestamp = datetime.datetime.utcnow()
    embed.description = """
    __**Willkommen auf dem Communityserver von BestofBundestag**__
    
    Unter <#607294374900138022> kannst du dir Rollen zuweisen. 
    Beispielsweise Themen, die dich interessieren oder deine politische Ausrichtung
    \n
    Oder sag doch einfach in <#531445762157182986> hallo :smiley:
    \n
    In <#533005337482100736> kannst du den Bot verwenden.
    Versuche doch mal `>umfrage`
    \n
    Gerne kannst du mir hier mit `>submit text` ein Feedback oder ein Hinweis hinterlassen, die ich anonym ans Serverteam weiterleite.
    \n
    Wenn du Themen öffentlich ansprechen willst,
    kannst du das aber auch gerne in <#531816355608133632> tun.
    
    https://discord.gg/ezMtSwR
    """
    return embed


@client.event
async def on_member_join(member):
    await member.send(embed=createembed())
    roles = []
    roles.append(get(client.get_guild(531445761733296130).roles, id=607474719595298852))
    roles.append(get(client.get_guild(531445761733296130).roles, id=607474935132192797))
    roles.append(get(client.get_guild(531445761733296130).roles, id=607475066460176385))
    for r in roles:
        await member.add_roles(r)


@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 607294374900138022:
        if str(payload.emoji.id) in roles.keys():
            role = get(client.get_guild(531445761733296130).roles, name=roles[str(payload.emoji.id)])
            user = client.get_guild(531445761733296130).get_member(payload.user_id)
            if role not in user.roles:
                await user.add_roles(role)
    return 0


@client.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == 607294374900138022:
        if str(payload.emoji.id) in roles.keys():
            role = get(client.get_guild(531445761733296130).roles, name=roles[str(payload.emoji.id)])
            user = client.get_guild(531445761733296130).get_member(payload.user_id)
            if role in user.roles:
                await user.remove_roles(role)
    return 0


@client.event
async def on_message(message):
    if message.author == client.user:
        return 0

    if str(message.author.id) in blacklist:
        return 0

    if len(str(message.content)) > 1999:
        return 0

    if message.author.id == 272655001329991681:
        emoji = client.get_emoji(545649937598119936)
        await message.add_reaction(emoji)

    if message.content.startswith(commands.prefix.standard):
        params = commands.parse(message.content, False)
        if params[0] in commands.commands.keys():
            await commands.commands[params[0]](client, message, params[1:])

    elif  message.content.startswith(commands.prefix.mod):
        params = commands.parse(message.content, True)
        if params[0] in commands.mod_commands.keys():
            await commands.mod_commands[params[0]](client, message, params[1:])


@client.event
async def on_ready():
    # console related
    # ================================================

    print('\033[92m' + (str(datetime.datetime.now())[:-7]) + prefix + 'Logged in as')
    print((str(datetime.datetime.now())[:-7]) + prefix + client.user.name)
    print((str(datetime.datetime.now())[:-7]) + prefix + str(client.user.id))
    print((str(datetime.datetime.now())[:-7]) + prefix + '------')

    # discord related
    # ================================================

    game1 = discord.Game(name='>help')
    await client.change_presence(activity=game1)
    print((str(datetime.datetime.now())[:-7]) + prefix + game1.name + ' als Status gesetzt.')

    # ================================================
    hook = Webhook(webhooklogs)
    hookBoB = Webhook(webhooklogsBoB)

    # ================================================

    embed = Embed(
        title='BundestagBot - Status',
        description='I am ready again!',
        thumbnail_url='https://i0.wp.com/www.activate-the-beast.com/wp-content/uploads/2015/05/Ern%C3%A4hrung-Umfrage-Icon-e1432756685893.png?fit=300%2C300',
        color=0x6eff33
    )

    # hook.send(embed=embed)
    print((str(datetime.datetime.now())[:-7]) + prefix + 'Webhook Server')
    # hookBoB.send(embed=embed)
    print((str(datetime.datetime.now())[:-7]) + prefix + 'Webhook BoB-Server')
    # pushedNotification.sendNot('BundestagBot: I am ready again!')
    print((str(datetime.datetime.now())[:-7]) + prefix + 'Mobil Notification')

    # script related
    # ================================================


client.run(TOKEN, reconnect=True)
