from bt_utils.console import Console
from bt_utils.embed_templates import NoticeEmbed
from bt_utils.config import cfg
import discord
import datetime
SHL = Console("BundestagsBot Survey")

settings = {
    "name": "survey",
    "channels": ["!dm"],
}


async def main(client, message, params):
    args = " ".join(params).split(';')  # used as discriminator is ";" here

    error = NoticeEmbed(title="Survey")
    if len(args) in range(2, 4):
        embed = create_survey(args[0], args[1], message.author)
        if len(args) == 3 and args[2] != '':
            args[2] = args[2].strip()
            if args[2].isdigit():
                msg = await message.channel.send(embed=embed)
                if int(args[2]) in range(3, 10):
                    emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
                    for e in emojis[:int(args[2])]:
                        await msg.add_reaction(emojis[e])
                elif int(args[2]) in range(0, 3):
                    await msg.add_reaction('✅')
                    await msg.add_reaction('❌')
                else:
                    error.description = "Please enter a valid digit (0-9)."
                await message.channel.send(embed=error)
            else:
                error.description = "Please enter a valid digit (0-9)."
                await message.channel.send(embed=error)
        elif len(args) == 2 or args[2] == '':
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction('✅')
            await msg.add_reaction('❌')
        else:
            error.description = f"Invalid syntax.\nPlease use {cfg.options['invoke_normal']}survey title; text; [answers]"
            await message.channel.send(embed=error)
    else:
        error.description = f"Invalid syntax.\nPlease use {cfg.options['invoke_normal']}survey title; text; [answers]"
        await message.channel.send(embed=error)


def create_survey(title, text, author):
    embed = discord.Embed(title='Umfrage: ' + title,
                          color=discord.Colour.green(),
                          url='https://github.com/bundestagsBot/bundestagsBot')
    embed.timestamp = datetime.datetime.utcnow()
    embed.description = text.replace('|', '\n')
    embed.set_footer(text="Umfrage von " + author.name)
    return embed
