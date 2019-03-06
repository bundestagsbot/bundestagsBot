import discord
import datetime
from utils import handleJson

settings = {
    'name': 'result',
    'channels': ['all'],
}

path = 'C:/server/settings/surveys.json'


async def main(client, message, params):
    if len(str(message.content).split(' ')) == 2:
        survey_id = str(message.content).split(' ')[1][1:]
        if survey_id.isdigit():
            if surveyID_is_valid(survey_id):
                embed = createembed(survey_id)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(content='#' + survey_id + ' konnte keiner Umfrage zugeordnet werden.')
        else:
            await message.channel.send(content=survey_id + ' ist keine gültige ID.')
    else:
        await message.channel.send(content='Ungültige Anzahl an Argumenten. Verwende: >result #survey_id')


def surveyID_is_valid(survey_id):
    return str(survey_id) in [key for key in handleJson.readjson(path).keys() if key not in ['unsubs','latestID']]


def createembed(survey_id):
    data = handleJson.readjson(path)
    title = data[survey_id]["title"]
    text = data[survey_id]["text"]
    author = data[survey_id]["author"]
    url = data[survey_id]["url"]
    votes = len(data[survey_id]["voted"])
    answers = data[survey_id]["answers"]
    results = data[survey_id]["results"]

    embed = discord.Embed(title='Umfrage #' + str(survey_id) + ': ' + title, color=discord.Colour.green(), url=url)
    embed.timestamp = datetime.datetime.utcnow()
    embed.add_field(name='Frage:', value=text.replace('|', '\n'), inline=False)
    embed.add_field(name='Antwortmöglichkeiten:', value='1 - ' + str(answers))
    embed.add_field(name='Beteiligung: ', value='Insgesamt abgestimmt haben: ' + str(votes))
    embed.add_field(name='Ergebnis:', value='\n'.join([f"{results[e]} Stimmen für: {e}" for e in results.keys()
                                                       if results[e] != 0]), inline=False)
    embed.set_footer(text="Umfrage von " + author)

    return embed
