import discord
import datetime

settings = {
    "name": "survey;",
    "channels": ["!dm"],
}

async def main(client, message, params):
    # aufbau: survey title text answers
    # answers 0 für antwort ja/nein
    # >1 für zaheln von 0-10 damit man dann im text schreibt 1:x 2:y 3:z 4:a 5:b 6:c und die leute dann deutlich mehr zur auswahl haben
    args = str(message.content).split(';')

    if len(args) in range(3, 5):
        embed = createsurvey(args[1], args[2], message.author)
        if len(args) == 4 and args[3] != '':
            args[3] = args[3].strip()
            if args[3].isdigit():
                msg = await message.channel.send(embed=embed)
                if int(args[3]) in range(3, 10):
                    emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
                    for e in range(0, int(args[3])):
                        await msg.add_reaction(emojis[e])
                elif int(args[3]) in range(0, 3):
                    await msg.add_reaction('✅')
                    await msg.add_reaction('❌')
                else:
                    await message.channel.send(content='Bitte gib eine gültige Zahl ein (3-9)..')
            else:
                await message.channel.send(content='Bitte gib eine gültige Zahl ein (3-9).')
        elif len(args) == 3 or args[3] == '':
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction('✅')
            await msg.add_reaction('❌')
        else:
            await message.channel.send(content='Ungültige Anzahl an Argumenten. Benutze >survey; title; text; [answers]')
    else:
        await message.channel.send(content='Ungültige Anzahl an Argumenten. Benutze >survey; title; text; [answers]')


def createsurvey(title, text, author):
    embed = discord.Embed(title='Umfrage: ' + title,color=discord.Colour.green(),url='https://github.com/zaanposni/bundestagsBot')
    embed.timestamp = datetime.datetime.utcnow()
    embed.description = text.replace('|','\n')
    embed.set_footer(text="Umfrage von " + author.name)
    return embed