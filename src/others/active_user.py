import os
import json
from datetime import datetime, timedelta

import discord
from discord.utils import get

from bt_utils.console import Console
from bt_utils.config import cfg
from bt_utils.embed_templates import InfoEmbed

SHL = Console("ActiveUserAssigment")
content_dir = "content" if os.path.isdir("content") else "content-default"


class UserStat:
    def __init__(self, user_obj: discord.Member):
        self.user_obj = user_obj
        self.count = 1

    def __str__(self):
        return f"{self.user_obj.display_name}: {self.count}"


async def assign_active_member(*args):
    SHL.info("Fetching last messages.")
    client = args[0]
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

    with open(os.path.join(content_dir, "unsubs.json"), "r") as fh:
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

    log_embed = InfoEmbed(title="Aktivste User", description="Für die Auswahl der Stammmitglieder.\n"
                                                             "Anzahl an Nachrichten in den letzten 31 Tagen.\n")
    for stat in sorted_list:  # active user
        try:
            member = await guild.fetch_member(stat.user_obj.id)
        except:  # if user left or got banned
            continue
        SHL.debug(f"Apply roles for {member}")
        log_embed.description += f"{member.mention}  {stat.count} Nachrichten.\n"
        for role in cfg.get("apply_roles"):
            assign_role = get(guild.roles, id=role)
            try:
                await member.add_roles(assign_role)
            except:
                SHL.debug(f"Failed for {stat.user_obj}")
                break

    await log_channel.send(embed=log_embed)
    await announcement_channel.send(embed=log_embed)
    SHL.info("Done.")
