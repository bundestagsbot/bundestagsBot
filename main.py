import discord
from utils import webhooks, handleJson, pushedNotification
import datetime
import subprocess
from dhooks import Webhook, Embed

prefix = ' \033[92m[BundestagsBot] '
print('\033[92m' + (str(datetime.datetime.now())[:-7]) + prefix + 'started BundestagsBot')
subprocess.call('cls', shell=True)
import commands

blacklist = handleJson.readjson('C:/server/settings/botblacklist.json')["blacklist"]
data = handleJson.readjson('C:/server/settings/tokens.json')
TOKEN = data['TOKENS']['umfrageBot']
webhooklogs = webhooks.webhooks['logChannel']
webhooklogsBoB = webhooks.webhooks['logChannelBoB']
firstconnection = True
tries_torec = 0
client = discord.Client()

commands.prefix.standard = '>'
commands.prefix.mod = '+'

@client.event
async def on_message(message):
    if message.author == client.user:
        return 0

    if str(message.author.id) in blacklist:
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

    game1 = discord.Game(name='>umfrage')
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

    hook.send(embed=embed)
    print((str(datetime.datetime.now())[:-7]) + prefix + 'Webhook Server')
    hookBoB.send(embed=embed)
    print((str(datetime.datetime.now())[:-7]) + prefix + 'Webhook BoB-Server')
    pushedNotification.sendNot('BundestagBot: I am ready again!')
    print((str(datetime.datetime.now())[:-7]) + prefix + 'Mobil Notification')

    # script related
    # ================================================


client.run(TOKEN, reconnect=True)
