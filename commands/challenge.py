from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed, InfoEmbed, NoticeEmbed
from bt_utils.config import cfg
from bt_utils import handleJson
from discord.utils import get
from others.scheduler import schedule_job, clear_tag
SHL = Console("BundestagsBot Challenge")

settings = {
    'name': 'challenge',
    'channels': ['!dm'],
}

path = "content/challenge.json"


async def close_channel(args):
    print(args)
    print(type(args))
    print(args[0])
    print(type(args[0]))
    client = args[0]
    data = handleJson.read_json_raw(path)
    data["arena_status"] = 0
    channel = client.get_channel(cfg.options["channel_ids"]["1v1"])
    role = get(channel.guild.roles, id=cfg.options["1v1_role"])

    for m in data["participants"]:
        m = channel.guild.get_member(m)
        info = SuccessEmbed(title="Challenge - Closed", description="Channel closed. Thank you for your discussion")
        await channel.send(embed=info)
        try:
            await m.remove_roles(role)
            await m.send(embed=info)
        except:
            pass
    clear_tag("challenge")
    handleJson.saveasjson(path, data)


async def main(client, message, params):
    data = handleJson.read_json_raw(path)
    if not data["arena_status"]:
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
            return user == participants[0] and e.startswith(('✅', '❌'))

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
        except TimeoutError:
            pass

        if str(reaction.emoji).startswith('❌'): return

        data["arena_status"] = 1
        try:
            info = InfoEmbed(title="Challenge",
                             description=f"{participants[0].display_name} accepted your challenge!\n" +
                                         f'<#{cfg.options["channel_ids"]["1v1"]}>')
            await message.author.send(embed=info)
        except:
            pass

        SHL.output(f"{participants[0].display_name} accepted {message.author.display_name}s challenge!")
        channel = client.get_channel(cfg.options["channel_ids"]["1v1"])
        role = get(channel.guild.roles, id=cfg.options["1v1_role"])

        await message.author.add_roles(role)
        await participants[0].add_roles(role)
        announce = SuccessEmbed(title="Challenge", description="Discussion duel started!")
        await channel.send(embed=announce)

        data["participants"].append(message.author.id)
        data["participants"].append(participants[0].id)
        handleJson.saveasjson(path, data)

        schedule_job(close_channel, "challenge", client)
    else:
        notice = NoticeEmbed(title="Challenge", description="There is already a discussion running!")
        await message.channel.send(embed=notice)
