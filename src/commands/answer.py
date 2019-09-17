from bt_utils.console import Console
from bt_utils.config import cfg
from bt_utils.embed_templates import SuccessEmbed, NoticeEmbed, ErrorEmbed
from bt_utils import handleJson

SHL = Console("BundestagsBot Answer")

settings = {
    'name': 'answer',
    'channels': ['dm'],
    'log': False
}

path = 'content/surveys.json'


async def main(client, message, params):
    success = SuccessEmbed(title="Answer")
    error = NoticeEmbed(title="Answer")
    try:
        data = handleJson.read_json_raw(path)
    except:
        error = ErrorEmbed(title="Submit",
                           description="Something went wrong. Please contact an admin.")
        await message.channel.send(embed=error)
        return
    params = str(message.content).split(' ')
    if subscribed(data, message.author.id):
        if len(params) == 3:
            survey_id = params[1][1:]
            if survey_id.isdigit():
                if survey_id_is_valid(data, survey_id):
                    survey_data = handleJson.readjson(path)[survey_id]
                    if message.author.id not in survey_data['voted']:
                        if int(str(params[2]).lower().strip()) in range(1, int(survey_data['answers']) + 1):
                            vote(message.author.id, survey_id, params[2].lower().strip())
                            success.description = f'Danke für deine Antwort!\n' \
                                                  f'Du kannst die Ergebnisse mit\n' \
                                                  f'{cfg.options["invoke_normal"]}result #{survey_id} sehen.'
                            await message.channel.send(embed=success)
                        else:
                            error.description = f"Invalid answer.\nPossible answers: 1-{survey_data['answers']}"
                            await message.channel.send(embed=error)
                    else:
                        error.description = "You cannot vote twice."
                        await message.channel.send(embed=error)
                else:
                    error.description = f"#{survey_id} could not be assigned to a survey."
                    await message.channel.send(embed=error)
            else:
                error.description = f"{survey_id} is an invalid ID."
                await message.channel.send(embed=error)
        else:
            error.description = f"Invalid syntax.\nPlease use {cfg.options['invoke_normal']}answer #survey_id Answer"
            await message.channel.send(embed=error)
    else:
        error.description = f"You have to be subscribed to participate. Use {cfg.options['invoke_normal']}sub True"
        await message.channel.send(embed=error)


def vote(user_id, survey_id, answer):
    data = handleJson.read_json_raw(path)
    data[survey_id]['voted'].append(user_id)
    data[survey_id]['results'][answer] += 1
    handleJson.saveasjson(path, data)


def survey_id_is_valid(data, survey_id):
    return str(survey_id) in [key for key in data.keys() if key not in ['unsubs', 'latestID']]


def subscribed(data, user_id):
    return user_id not in data['unsubs']
