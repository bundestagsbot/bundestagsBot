from bt_utils.console import Console
from bt_utils.embed_templates import ErrorEmbed, InfoEmbed
from discord import Embed, Colour
import datetime
import os.path

SHL = Console("BundestagsBot Post")

settings = {
    'name': 'post',
    'mod_cmd': True,
    'channels': ['team'],
}

suffix_text = """
Bei Fragen lest euch bitte die Regeln durch. 
Rehabilitationen sind möglich, wendet euch hierfür bitte an einen Moderator. 
"""


async def main(client, message, params):
    try:
        target_channel = message.channel_mentions[0]
        text = " ".join(params[1:])
    except IndexError:
        embed = ErrorEmbed("Post", description="Syntax error\nUse `+post <#channel_id> text`")
        await message.channel.send(embed=embed)
        return

    embed = InfoEmbed(title="Moderation", description=f"{text}\n\n{suffix_text}")
    msg = await message.channel.send(content=f"Message will be sent to {target_channel.mention}",
                                     embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

    def reaction_check(reaction, user):
        e = str(reaction.emoji)
        return user == message.author and e.startswith(('✅', '❌')) and reaction.message.id == msg.id

    reaction, user = await client.wait_for('reaction_add', timeout=180.0, check=reaction_check)

    if not str(reaction.emoji).startswith('✅'):
        return

    try:
        await target_channel.send(embed=embed)
    except:
        embed = ErrorEmbed("Post", description="Error while sending message to target channel.")
        await message.channel.send(embed=embed)
