from bt_utils import handle_sqlite as db
from bt_utils.config import cfg
from discord.utils import get
import commands
from bt_utils.console import *
from dhooks import Webhook, Embed
from bt_utils.handle_sqlite import DatabaseHandler
from others import welcome, role_assignment
from others.message_conditions import check_message
from others.scheduler import schedule_check
from others import scheduler
from discord.errors import LoginFailure
from threading import Thread
import discord
import asyncio

loop = asyncio.new_event_loop()
scheduler.main_loop = loop
client = discord.Client(loop=loop)
SHL = Console(prefix="BundestagsBot")
DB = DatabaseHandler()


@client.event
async def on_member_join(member):
    try:
        await member.send(embed=welcome.create_embed())
        SHL.output(f"Send Welcome to {member.display_name}.")
    except:  # if users privacy settings do not allow dm
        pass
    # member did not accept dm
    for role in cfg.options.get("roles_on_join", []):
        r = get(client.get_guild(member.guild.id).roles, id=int(role))
        await member.add_roles(r)


@client.event
async def on_reaction_add(reaction, user):
    # do not consider reactions on the users own messages
    if user.id == reaction.message.author.id:
        return

    roles = cfg.options["roles_stats"]
    is_custom_emoji = hasattr(reaction.emoji, 'id')
    is_role = str(reaction.emoji.id) in roles.keys()
    if is_custom_emoji and is_role:
        role_reaction = cfg.options["roles_stats"][str(reaction.emoji.id)]
        reaction_recipient = reaction.message.author
        users = DB.get_all_users()
        if reaction_recipient.id not in [item[0] for item in users]:
            # add new user to db
            DB.add_user(reaction_recipient.id, reaction_recipient.name, roles)
        if role_reaction in cfg.options["roles_stats"].values():
            DB.add_reaction(reaction_recipient, role_reaction)


@client.event
async def on_reaction_remove(reaction, user):
    # do not consider reactions on the users own messages
    if user.id == reaction.message.author.id:
        return

    roles = cfg.options["roles_stats"]
    is_custom_emoji = hasattr(reaction.emoji, 'id')
    is_role = str(reaction.emoji.id) in roles.keys()
    if is_custom_emoji and is_role:
        role_reaction = cfg.options["roles_stats"][str(reaction.emoji.id)]
        reaction_recipient = reaction.message.author
        users = DB.get_all_users()
        if reaction_recipient.id not in [item[0] for item in users]:
            # add new user to db
            DB.add_user(reaction_recipient.id, reaction_recipient.name, roles)
            # finished here, because new user is initialized with 0 anyway
            return
        if role_reaction in cfg.options["roles_stats"].values():
            DB.remove_reaction(reaction_recipient, role_reaction)


@client.event
async def on_raw_reaction_add(payload):
    await role_assignment.reaction_add(client, payload)


@client.event
async def on_raw_reaction_remove(payload):
    await role_assignment.reaction_remove(client, payload)


@client.event
async def on_message(message):
    if not await check_message(client, message):  # check basic conditions like length and not responding to himself
        return 0

    if message.content.lower().startswith(str(cfg.options["invoke_normal"]).lower()):
        params = commands.parse(message.content, False)
        if params[0].lower() in commands.commands.keys():
            await commands.commands[params[0].lower()](client, message, params[1:])

    elif message.content.lower().startswith(str(cfg.options["invoke_mod"]).lower()):
        params = commands.parse(message.content, True)
        if params[0].lower() in commands.mod_commands.keys():
            await commands.mod_commands[params[0].lower()](client, message, params[1:])


@client.event
async def on_ready():
    # console related
    # ================================================
    SHL.output(f"{red}========================{white}")
    SHL.output("Logged in as")
    SHL.output(client.user.name)
    SHL.output(f"Online in {len(client.guilds)} Guilds.")
    SHL.output(f"{red}========================{white}")

    # discord related
    # ================================================
    if cfg.options.get("use_game", False):
        game = discord.Game(name=cfg.options.get("game_name", "Hello world"))
        await client.change_presence(activity=game)
        SHL.output(f"Set game: {game.name}.")

    # database related
    # ================================================
    roles = cfg.options["roles_stats"].values()

    # creates basic table structures if not already present
    DB.create_structure(roles)

    # updates table structure, e.g. if a new role has been added
    DB.update_columns(roles)
    SHL.output("Setup database completed")

    # WebHooks
    # ================================================
    if cfg.options.get("use_webhooks", False):
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


def start_bot():
    try:
        SHL.output(f"Logging in.")
        client.run(cfg.options["BOT_TOKEN"], reconnect=cfg.options.get("use_reconnect", False))
    except LoginFailure:
        SHL.output(f"{red}========================{white}")
        SHL.output(f"{red}Login failure!{white}")
        SHL.output(f"{red}Please check your token.{white}")
    except KeyError:
        SHL.output(f"{red}========================{white}")
        SHL.output(f"{red}'BOT_TOKEN' not found in config files!")


thread_sched = Thread(target=schedule_check, name="sched", args=(client,))
thread_main = Thread(target=start_bot, name="main")
thread_sched.start()
thread_main.start()
