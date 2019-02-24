import discord
from utils import webhooks,handleJson,pushedNotification
import datetime
import subprocess
from dhooks import Webhook,Embed
import commands

data = handleJson.readjson('C:/server/settings/tokens.json')
TOKEN = data['TOKENS']['umfrageBot']
webhooklogs = webhooks.webhooks['logChannel']
webhooklogsBoB = webhooks.webhooks['logChannelBoB']
prefix = '\033[92m[umfrageBot] '
firstconnection = True
tries_torec = 0
client = discord.Client()

commands.prefixmgr.standard_prefix = ">"
commands.prefixmgr.mod_cmd_prefix = "+"

@client.event
async def on_message(message):
    if message.author == client.user:
        return 0
    if message.author.id == 272655001329991681:
        emoji = client.get_emoji(545649937598119936)
        await message.add_reaction(emoji)
    command = message.content.split(" ")[0]
    if command in commands.commands.keys() :
        await commands.commands[command](client, message)

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
    hookBoB = Webhook(webhooklogsBoB)

    # ================================================

    embed = Embed(
        title='umfrageBot - Status',
        description='I am ready again!',
        thumbnail_url='https://i0.wp.com/www.activate-the-beast.com/wp-content/uploads/2015/05/Ern%C3%A4hrung-Umfrage-Icon-e1432756685893.png?fit=300%2C300',
        color=0x6eff33
    )

    hook.send(embed=embed)
    hookBoB.send(embed=embed)
    pushedNotification.sendNot('BundestagBot: I am ready again!')

    # script related
    #================================================


client.run(TOKEN, reconnect=True)
