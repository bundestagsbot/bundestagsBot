from discord.utils import get
import commands
from bt_utils.console import Console
from bt_utils import handleJson
from bt_utils.config import cfg
from dhooks import Webhook, Embed
import discord
import datetime

SHL = Console(prefix="BundestagsBot", cls=True)
handleJson.BASE_PATH = __file__
cfg.reload()
client = discord.Client()


def create_embed():
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
    Wenn du Themen öffentlich ansprechen willst,
    kannst du das aber auch gerne in <#531816355608133632> tun.
    
    Beteilige dich gerne an der Entwicklung des BundestagsBot:\n https://github.com/bundestagsBot/bundestagsBot
    """
    return embed


@client.event
async def on_member_join(member):
    await member.send(embed=create_embed())
    roles = []
    roles.append(get(client.get_guild(531445761733296130).roles, id=607474719595298852))
    roles.append(get(client.get_guild(531445761733296130).roles, id=607474935132192797))
    roles.append(get(client.get_guild(531445761733296130).roles, id=607475066460176385))
    for r in roles:
        await member.add_roles(r)


@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id in cfg.options["role_channel_ids"]:
        if str(payload.emoji.id) in cfg.options["roles"].keys():
            role = get(client.get_guild(531445761733296130).roles, name=cfg.options["roles"][str(payload.emoji.id)])
            user = client.get_guild(531445761733296130).get_member(payload.user_id)
            if role not in user.roles:
                await user.add_roles(role)
    return 0


@client.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == cfg.options["role_channel_ids"]:
        if str(payload.emoji.id) in cfg.options["roles"].keys():
            role = get(client.get_guild(531445761733296130).roles, name=cfg.options["roles"][str(payload.emoji.id)])
            user = client.get_guild(531445761733296130).get_member(payload.user_id)
            if role in user.roles:
                await user.remove_roles(role)
    return 0


@client.event
async def on_message(message):
    if message.channel.id == 513355409021730816:
        await message.delete()
        return 0

    if message.author == client.user:
        return 0

    if str(message.author.id) in cfg.options["blacklist"]:
        return 0

    if len(str(message.content)) > 1999:
        return 0

    if message.content.startswith(cfg.options["invoke_normal"]):
        params = commands.parse(message.content, False)
        if params[0] in commands.commands.keys():
            await commands.commands[params[0]](client, message, params[1:])

    elif message.content.startswith(cfg.options["invoke_mod"]):
        params = commands.parse(message.content, True)
        if params[0] in commands.mod_commands.keys():
            await commands.mod_commands[params[0]](client, message, params[1:])


@client.event
async def on_ready():
    # console related
    # ================================================
    SHL.output("========================")
    SHL.output("Logged in as")
    SHL.output(client.user.name)
    SHL.output(client.user.id)
    SHL.output("========================")

    # discord related
    # ================================================
    if cfg.options["use_game"]:
        game = discord.Game(name=cfg.options["game_name"])
        await client.change_presence(activity=game)
        SHL.output(f"{game.name} als Status gesetzt.")

    # WebHooks
    # ================================================
    if cfg.options["use_webhooks"]:
        template = cfg.options["on_ready"]
        embed = Embed(
            title=template["title"],
            description=template["description"],
            thumbnail_url=template["thumbnail_url"],
            color=int(template["color"], 16)
        )
        for name, link in cfg.options["webhooks"].items():
            Webhook(link).send(embed=embed)
            SHL.output(f"Webhook {name} sent.")

client.run(cfg.options["BOT_TOKEN"], reconnect=cfg.options["use_reconnect"])
