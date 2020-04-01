from bt_utils.config import cfg
from discord.utils import get
import commands
from bt_utils.console import *
from bt_utils.embed_templates import InfoEmbed
from dhooks import Webhook, Embed
from others import welcome
from others import role_assignment
from others.message_conditions import check_message
from others.reaction_assignment import handle_reaction
from others.scheduler import app_scheduler
from others import reset_temps
from discord.errors import LoginFailure
from threading import Thread
import discord
import asyncio
from datetime import datetime, timedelta
import json

loop = asyncio.new_event_loop()
app_scheduler.main_loop = loop
client = discord.Client(loop=loop)
SHL = Console(prefix="BundestagsBot")

CONTENT_PATH = "content" if os.path.isdir("content") else "content-default"
SHL.info(f"Using content path: {CONTENT_PATH}")


class UserStat:
    def __init__(self, user_obj: discord.Member):
        self.user_obj = user_obj
        self.count = 1

    def __str__(self):
        return f"{self.user_obj.display_name}: {self.count}"


async def assign_active_member(*args):
    SHL.info("Fetching last messages.")
    guild = await client.fetch_guild(cfg.get("guild_id"))
    SHL.debug(f"Guild: {guild}")

    # Remove all "active" members
    SHL.info("Remove active role from all users.")
    for role in cfg.get("apply_roles"):
        role = guild.get_role(role)
        async for member in guild.fetch_members():
            if role not in member.roles:
                continue
            SHL.debug(f"Remove {role} from {member}")
            try:
                await member.remove_roles(role)
            except:
                SHL.debug(f"Failed for {member}")

    # Find new active members
    channels = await guild.fetch_channels()

    announcement_channel = await client.fetch_channel(cfg.get("announce_channel"))
    log_channel = await client.fetch_channel(cfg.get("log_channel"))

    users = {}
    before = datetime.now()
    after = datetime.now() - timedelta(days=31)

    with open(os.path.join(CONTENT_PATH, "unsubs.json"), "r") as fh:
        unsubs = json.load(fh)["unsub_ids"]

    SHL.debug(f"{len(unsubs)} users unsubbed.")

    for channel in channels:
        if not isinstance(channel, discord.TextChannel):
            continue
        if channel.id in cfg.get("exclude_channels"):
            continue

        SHL.debug(f"Fetching {channel.name}")
        async for message in channel.history(limit=None, before=before, after=after):
            uid = message.author.id
            if uid in unsubs:  # filter opt-out user
                continue
            if uid in users:
                users[uid].count += 1
            else:
                users[uid] = UserStat(message.author)

    sorted_list = sorted([x for x in users.values() if x.count >= cfg.get("needed_messages")],
                         key=lambda item: item.count, reverse=True)
    SHL.debug(f"{len(sorted_list)} users sent enough messages.")

    log_embed = InfoEmbed(title="Aktivste User")
    for stat in sorted_list:  # active user
        try:
            member = await guild.fetch_member(stat.user_obj.id)
        except:  # if user left or got banned
            continue
        SHL.debug(f"Apply roles for {member}")
        log_embed.description += f"{member.mention} : {stat.count} Nachrichten.\n"
        for role in cfg.get("apply_roles"):
            assign_role = get(guild.roles, id=role)
            try:
                await member.add_roles(assign_role)
            except:
                SHL.debug(f"Failed for {stat.user_obj}")
                break
    await log_channel.send(embed=log_embed)

    announcement = InfoEmbed(title="Aktivste User", description="Für die Auswahl der Stammmitglieder.\n"
                                                                "Anzahl an Nachrichten in den letzten 31 Tagen.")
    for stat in sorted_list[:3]:  # most active user
        member = await guild.fetch_member(stat.user_obj.id)
        announcement.description += f"{member.mention} : {stat.count} Nachrichten.\n"

    await announcement_channel.send(embed=announcement)
    await log_channel.send(embed=announcement)
    SHL.info("Done.")


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
    await asyncio.sleep(600)
    for role in cfg.options.get("roles_on_10_minute", []):
        r = get(client.get_guild(member.guild.id).roles, id=int(role))
        await member.add_roles(r)


@client.event
async def on_raw_reaction_add(payload):
    await role_assignment.reaction_add(client, payload)

    channel = client.get_channel(payload.channel_id)
    is_private_channel = isinstance(channel, discord.DMChannel)
    if is_private_channel:
        return

    msg = await channel.fetch_message(payload.message_id)
    await handle_reaction(msg, payload, "add")


@client.event
async def on_raw_reaction_remove(payload):
    await role_assignment.reaction_remove(client, payload)

    channel = client.get_channel(payload.channel_id)
    is_private_channel = isinstance(channel, discord.DMChannel)
    if is_private_channel:
        return

    msg = await channel.fetch_message(payload.message_id)
    await handle_reaction(msg, payload, "remove")


@client.event
async def on_message(message):
    if not await check_message(client, message):  # check basic conditions like length and not responding to himself
        return 0

    if message.channel.id == cfg.get("channel_ids", dict()).get("suggestions"):
        await message.add_reaction('👍')
        await message.add_reaction('👎')

    if message.content.lower().startswith(str(cfg.options["invoke_normal"]).lower()):
        params = commands.parse(message.content, False)
        if params:
            if params[0].lower() in commands.commands.keys():
                await commands.commands[params[0].lower()](client, message, params[1:])

    elif message.content.lower().startswith(str(cfg.options["invoke_mod"]).lower()):
        params = commands.parse(message.content, True)
        if params:
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
        reset_temps.reset()
        token = cfg.options["BOT_TOKEN"]
    except KeyError:
        SHL.output(f"{red}========================{white}")
        SHL.output(f"{red}'BOT_TOKEN' not found in config files!{white}")
        return
    try:
        SHL.output(f"Logging in.")
        client.run(token, reconnect=cfg.options.get("use_reconnect", False))
    except LoginFailure:
        SHL.output(f"{red}========================{white}")
        SHL.output(f"{red}Login failure!{white}")
        SHL.output(f"{red}Please check your token.{white}")
        return


thread_sched = Thread(target=app_scheduler.schedule_check, name="sched")
thread_sched.start()
app_scheduler.schedule_daily(func=assign_active_member, tag="daily")
start_bot()
