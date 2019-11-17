import os.path
from asyncio import TimeoutError

from discord.utils import get

from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed, InfoEmbed, NoticeEmbed
from bt_utils.config import cfg
from bt_utils import handleJson
from bt_utils.get_content import content_dir
from others.scheduler import schedule_job, clear_tag


SHL = Console("BundestagsBot Challenge")

settings = {
    'name': 'challenge',
    'channels': ['!dm'],
}

path = os.path.join(content_dir, "challenge.json")


async def close_channel(args):
    client = args[0]
    data = handleJson.read_json_raw(path)
    data["arena_status"] = 0
    channel = client.get_channel(cfg.options["channel_ids"]["1v1"])
    role = get(channel.guild.roles, id=cfg.options["1v1_role"])

    for e, m in enumerate(data["participants"]):
        data["participants"][e] = channel.guild.get_member(m)

    info = SuccessEmbed(title="Challenge - Closed",
                        description="Channel closed. Thank you for your discussion.\n")
    for m in data["participants"]:
        try:
            await m.remove_roles(role)
            await m.send(embed=info)
        except:
            pass

    info.description += "Who won?:\n" \
                        f"1⃣  {data['participants'][0].mention}\n" \
                        f"2⃣  {data['participants'][1].mention}\n"
    msg = await channel.send(embed=info)
    for e in ['1⃣', '2⃣']:
        await msg.add_reaction(e)

    await channel.edit(topic="")
    SHL.output("Closed discussion")
    clear_tag("challenge")
    data["participants"] = []
    handleJson.saveasjson(path, data)


async def main(client, message, params):
    data = handleJson.read_json_raw(path)

    if not len(message.mentions):
        error = NoticeEmbed(title="Challenge",
                            description="Please mention someone.")
        await message.channel.send(embed=error)
        return

    if message.mentions[0].id == message.author.id:
        error = NoticeEmbed(title="Challenge",
                            description="You cannot challenge yourself.")
        await message.channel.send(embed=error)
        return

    if data["arena_status"]:
        notice = NoticeEmbed(title="Challenge", description="There is already a discussion running!")
        await message.channel.send(embed=notice)
        return

    data["participants"] = []
    try:
        participants = message.mentions
        challenge = InfoEmbed(title="Challenge",
                              description=f"Hey {participants[0].mention}"
                                          f"\n{message.author.mention} challenged you!")
        msg = await message.channel.send(embed=challenge)
    except:
        error = NoticeEmbed(title="Challenge",
                            description="Something went wrong. Please contact an admin.")
        await message.channel.send(embed=error)
        return

    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

    def check(reaction, user):
        e = str(reaction.emoji)
        return user == participants[0] and e.startswith(('✅', '❌')) and reaction.message.id == msg.id

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        return

    if str(reaction.emoji).startswith('❌'): return

    data["arena_status"] = 1
    try:
        info = InfoEmbed(title="Challenge",
                         description=f"{participants[0].display_name} accepted your challenge!\n" +
                                     f'Discuss here: <#{cfg.options["channel_ids"]["1v1"]}>\n'
                                     f"Channel will be closed in {cfg.options['1v1_time_minutes']} minutes.")
        await message.author.send(embed=info)
    except:
        pass
    try:
        info = InfoEmbed(title="Challenge",
                         description=f"You accepted {message.author.mention}s challenge.!\n" +
                                     f'Discuss here: <#{cfg.options["channel_ids"]["1v1"]}>\n'
                                     f"Channel will be closed in {cfg.options['1v1_time_minutes']} minutes.")
        await participants[0].send(embed=info)
    except:
        pass

    SHL.output(f"{participants[0].display_name} accepted {message.author.display_name}s challenge!")
    channel = client.get_channel(cfg.options["channel_ids"]["1v1"])
    role = get(channel.guild.roles, id=cfg.options["1v1_role"])

    await message.author.add_roles(role)
    await participants[0].add_roles(role)
    announce = SuccessEmbed(title="Challenge",
                            description="Discussion duel started!\n"
                                        f"Battle between {message.author.mention} - {message.mentions[0].mention}\n"
                                        f"Channel will be closed in {cfg.options['1v1_time_minutes']} minutes.")
    await channel.send(embed=announce)

    data["participants"] = [message.author.id, participants[0].id]
    handleJson.saveasjson(path, data)

    await channel.edit(topic=f"Battle between: {message.author.mention} - {message.mentions[0].mention}")
    schedule_job(close_channel, cfg.options["1v1_time_minutes"], "challenge", client)

