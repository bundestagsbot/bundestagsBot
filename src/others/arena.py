from random import shuffle
import os.path

from discord.utils import get

from bt_utils.console import Console
from bt_utils.config import cfg
from bt_utils import handleJson
from bt_utils.embed_templates import SuccessEmbed, InfoEmbed, NoticeEmbed
from bt_utils.get_content import content_dir

SHL = Console("Arena")
path = os.path.join(content_dir, "arena.json")


# start discussion
async def start_discussion(args):
    client = args[0]
    data = handleJson.read_json_raw(path)
    if data["arena_status"] == "wait_start":
        SHL.output("Started discussion")
        channel = client.get_channel(cfg.options["channel_ids"]["arena"])

        role = get(channel.guild.roles, id=cfg.options["arena_role"])
        embed = InfoEmbed(title="Arena",
                          description="Arena started. Be sure to participate in the discussion!")
        for m in data["participants"]:
            member = channel.guild.get_member(m)
            await member.add_roles(role)
            await member.send(embed=embed)

        data["arena_status"] = "running"
        handleJson.saveasjson(path, data)


# end discussion and start poll
async def end_discussion(args):
    client = args[0]
    data = handleJson.read_json_raw(path)
    if data["arena_status"] == "running":
        SHL.output("Ended discussion")
        SHL.output("Started poll")
        channel = client.get_channel(cfg.options["channel_ids"]["arena"])
        role = get(channel.guild.roles, id=cfg.options["arena_role"])
        embed = InfoEmbed(title="Arena - End",
                          description="Arena stopped. Thank you for your participation")
        for m in data["participants"]:
            try:
                member = channel.guild.get_member(m)
                await member.remove_roles(role)
                await member.send(embed=embed)
            except:
                pass

        embed = SuccessEmbed(title="Arena - End")
        if len(data["participants"]) == 2:
            embed.description = "Ended discussion.\n Please vote for:\n"\
                                f"1⃣  {data['participants_name'][0]}\n" \
                                f"2⃣  {data['participants_name'][1]}\n"
            emojis = ['1⃣', '2⃣']
        elif len(data["participants"]) == 4:
            embed.description = "Ended discussion.\n Please vote for:\n" \
                                f"1⃣  {data['participants_name'][0]}\n" \
                                f"2⃣  {data['participants_name'][1]}\n" \
                                f"3⃣  {data['participants_name'][2]}\n" \
                                f"4⃣  {data['participants_name'][3]}\n"
            emojis = ['1⃣', '2⃣', '3⃣', '4⃣']
        close = await channel.send(embed=embed)
        data["last_poll_msg"] = close.id
        for e in emojis:
            await close.add_reaction(e)

        data["arena_status"] = "poll"
        handleJson.saveasjson(path, data)


# end poll and announce result
async def end_poll(args):
    client = args[0]
    data = handleJson.read_json_raw(path)
    if data["arena_status"] == "poll":
        SHL.output("Ended poll")
        channel = client.get_channel(cfg.options["channel_ids"]["arena"])
        results = [0] * data["participant_count"]
        emojis = ['1⃣', '2⃣', '3⃣', '4⃣']

        msg = await channel.fetch_message(data["last_poll_msg"])
        reactions = msg.reactions
        for reaction in reactions:
            if str(reaction) in emojis:
                results[emojis.index(str(reaction))] = reaction.count
        max_votes = max(results)
        embed = SuccessEmbed(title="Arena")
        embed.description = f"{data['participants_name'][results.index(max_votes)]} won."
        if results.count(max_votes) > 1:
            all_max = [e for e, i in enumerate(results) if i == max_votes]
            embed.description = ", ".join([data["participants_name"][x] for x in all_max]) + \
                                f" won with {max_votes} votes."
        # TODO: reputation system?

        await channel.send(embed=embed)
        info = InfoEmbed(title="Arena - Results",
                         description=f'We got a winner! Be sure to check <#{cfg.options["channel_ids"]["arena"]}>')
        for m in data["participants"]:
            try:
                member = channel.guild.get_member(m)
                await member.send(embed=info)
            except:
                pass

        data["arena_status"] = "wait_topic"
        handleJson.saveasjson(path, data)


# announce topic and open queue
async def announce_topic(args):
    client = args[0]
    data = handleJson.read_json_raw(path)
    if data["arena_status"] == "wait_topic" and cfg.options.get("enable_arena", False) and data["topics"]:
        SHL.output("Announced topic")
        SHL.output("Started queue")

        channel = client.get_channel(cfg.options["channel_ids"]["arena"])
        topic = data['topics'].pop(0)
        info = InfoEmbed(title="Arena - Topic",
                         description=f"Next topic will be:\n{topic}\n\n"
                                     f"Use {cfg.options['invoke_normal']}queue to enter the queue.")
        await channel.send(embed=info)
        await channel.edit(topic="test1")

        data["arena_status"] = "wait_queue"
        handleJson.saveasjson(path, data)


async def announce_participant(args):
    client = args[0]
    data = handleJson.read_json_raw(path)
    if data["arena_status"] == "wait_queue":
        SHL.output("Announced participant")
        channel = client.get_channel(cfg.options["channel_ids"]["arena"])

        embed = InfoEmbed(title="Arena - Participation",
                          description="You are participating in the next discussion!")
        count = 0
        data["participants"] = []
        data["participants_name"] = []
        shuffle(data["queue"])
        for m in set(data["queue"]):
            if count >= data["participant_count"]:
                break
            try:
                member = channel.guild.get_member(m)
                await member.send(embed=embed)
                count += 1
                data["participants"].append(member.id)
                data["participants_name"].append(member.display_name)
            except:  # not a valid participant as he declined dm
                continue

        if len(data["participants"]) < data["participant_count"]:
            error = NoticeEmbed(title="Arena - Queue",
                                description="Could not find enough members in queue.")
            channel.send(error)
            return
        data["queue"] = []
        embed = SuccessEmbed(title="Arena - Participants",
                             description="Participants:\n" + ",\n".join(data["participants_name"]) +
                                         "\n\nStart: Saturday 17:00")
        await channel.send(embed=embed)

        data["arena_status"] = "wait_start"
        handleJson.saveasjson(path, data)
