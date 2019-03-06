import discord
from utils import handleJson

settings = {
    'name': 'answer',
    'channels': ['dm'],
    'log': False
}

path = 'C:/server/settings/surveys.json'


async def main(client, message, params):

    params = str(message.content).split(' ')
    if subscribed(message.author.id):
        if len(params) == 3:
            if params[1][1:].isdigit():
                survey_id = params[1][1:]
                if surveyID_is_valid(survey_id):
                    surveyData = handleJson.readjson(path)[survey_id]
                    if message.author.id not in surveyData['voted']:
                        if int(str(params[2]).lower().strip()) in range(1, int(surveyData['answers']) + 1):
                            vote(message.author.id, survey_id, params[2].lower().strip())
                            await message.channel.send(content='Danke für deine Antwort!\nDu kannst die Ergebnisse mit\n>result #' + survey_id + ' sehen.')
                        else:
                            await message.channel.send(content='Keine gültige Antwort.\nMögliche Antworten:\n```\n' + '\n'.join(surveyData['answers']) + '\n```')
                    else:
                        await message.channel.send(content='Du kannst nicht nochmal abstimmen.')
                else:
                    await message.channel.send(content='#' + str(survey_id) + ' konnte keiner Umfrage zugeordnet werden.')
            else:
                await message.channel.send(content=str(params[1]) + ' ist keine gültige ID.')
        else:
            await message.channel.send(content='Ungültige Anzahl an Argumenten. Verwende:\n>answer #survey_id Antwort')
    else:
        await message.channel.send(content='Du musst die Umfragen abonniert haben, um abzustimmen. >sub True')


def vote(user_id, survey_id, answer):
    surveyData = handleJson.readjson(path)
    surveyData[survey_id]['voted'].append(user_id)
    surveyData[survey_id]['results'][answer] += 1
    handleJson.saveasjson(path, surveyData)

def surveyID_is_valid(survey_id):
    return str(survey_id) in [key for key in handleJson.readjson(path).keys() if key not in ['unsubs', 'latestID']]


def subscribed(user_id):
    return user_id not in handleJson.readjson(path)['unsubs']
