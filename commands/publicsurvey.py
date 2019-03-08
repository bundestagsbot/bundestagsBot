import discord
import datetime
from utils import handleJson, pushedNotification
from discord.utils import get

settings = {
    'name': 'publicsurvey;',
    'mod_cmd': True,
    'channels': ['team'],
}

'''

syntax:
>publicsurvey title text [answers] {url}
answers is a list of possible answers seperated by ','
url is optional and is autofilled with the github link

waits for approve via discord reaction
sends survey to all discord members

they will use 
>answer survey_id their_answer  

they can unsubscribe via: 
>sub False
or resubscribe:
>sub True

they can see the result via:
>result survey_id

all .json are stored in:
path: C:/server/settings/

'''

path = 'C:/server/settings/BoB/surveys.json'


async def main(client, message, params):

    params = [p for p in str(message.content).split(';')]
    if len(params) == 4 or params[4] == '':  params.append('https://github.com/zaanposni/bundestagsBot')
    survey_id = get_survey_id()
    embed = createsurvey(params[1], params[2], message.author, params[3], params[4], survey_id)
    msg = await message.channel.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

    def check(reaction, user):
        e = str(reaction.emoji)
        return user == message.author and e.startswith(('✅', '❌'))

    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    await msg.delete()

    if str(reaction.emoji).startswith('❌'):  return
    # if approved add to json and send embed to all discord members who are not unsubscribed:

    pushedNotification.sendNot(text="PublicSurvey: " + params[1].strip() + " von " + str(message.author.name))

    data = handleJson.readjson(path)
    data[survey_id] = {}
    data[survey_id]["title"] = params[1].strip()
    data[survey_id]["text"] = params[2].strip()
    data[survey_id]["author"] = str(message.author.name)
    data[survey_id]["url"] = params[4]
    data[survey_id]["voted"] = []
    data[survey_id]["answers"] = params[3].strip().lower()
    data[survey_id]["results"] = {}
    for a in range(1, int(data[survey_id]["answers"]) + 1):  # so answers will be displayed sorted
        data[survey_id]['results'][a] = 0
    data["latestID"] += 1

    handleJson.saveasjson(path, data)

    # send to subscribers:
    members = client.get_guild(531445761733296130).members
    unsubs = data['unsubs']
    received, failed = 0, 0
    for m in [e for e in members if e.id not in unsubs]:
        try:
            received += 1
            await m.send(embed=embed)
        except:
            failed += 1

    await message.channel.send(content='Done.\nUmfrage an ' + str(received-failed) + ' Personen gesendet.\n' + str(failed) + ' Personen haben die Nachricht abgelehnt.')


def createsurvey(title, text, author, answers, url, survey_id):
    embed = discord.Embed(title='Umfrage #' + str(survey_id) + ': ' + title, color=discord.Colour.green(), url=url)
    embed.timestamp = datetime.datetime.utcnow()
    embed.add_field(name='Frage:', value= text.replace('|', '\n'), inline=False)
    embed.add_field(name='Antwort:', value='Beantworte diese Umfrage mit:\n>answer #' + str(survey_id) + ' 1-' + answers.strip())
    embed.add_field(name='Ergebnisse:', value='Ergebnisse erhälst du mit:\n>result #' + str(survey_id))
    embed.add_field(name='Keine weitere Umfrage:', value='Wenn du keine weiteren Umfragen mehr erhalten willst, verwende: >sub False')
    embed.add_field(name='Information:', value='Du kannst deine Antwort nicht mehr ändern.\nDiese Umfrage ist anonym.\nBei Fragen wende dich an die Developer.')
    embed.set_footer(text="Umfrage von " + author.name)
    return embed


def get_survey_id():
    return int(handleJson.readjson(path)['latestID']) + 1
