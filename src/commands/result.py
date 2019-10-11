from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed, ErrorEmbed, NoticeEmbed, InfoEmbed
from bt_utils.config import cfg
from bt_utils import handleJson
from bt_utils.custom_exceptions import *
import os
SHL = Console("BundestagsBot Result")

settings = {
    'name': 'result',
    'channels': ['all'],
}

path = 'content/surveys.json'


async def main(client, message, params):
    embed = ErrorEmbed(title="Result")
    embed.description = "Something went wrong. Please contact an admin."
    try:
        if len(str(message.content).split(' ')) != 2 or params[0][0] != '#':
            raise CommandSyntaxException()
        survey_id = params[0][1:]
        if not survey_id.isdigit():
            raise InvalidSurveyIdException(survey_id)
        if not survey_id_is_valid(survey_id):
            raise SurveyNotFoundException(survey_id)
        embed = create_embed(survey_id)
    except SurveyNotFoundException as e:
        embed.description = f"#{e.survey_id} could not be assigned to a survey."
    except InvalidSurveyIdException as e:
        embed.description = f"{e.survey_id} is an invalid ID."
    except CommandSyntaxException as e:
        embed.description = f"Invalid syntax.\nPlease use {cfg.options['invoke_normal']}result #surveyID"
    finally:
        await message.channel.send(embed=embed)


def survey_id_is_valid(survey_id):
    try:
        data = handleJson.read_json_raw(path)
    except FileNotFoundError:
        SHL.output("Survey file not found. Creating it.")
        file_dir = os.path.join(handleJson.BASE_PATH, os.path.dirname(path))
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        handleJson.saveasjson(path, {})
        data = handleJson.read_json_raw(path)
    return str(survey_id) in [key for key in data.keys() if key not in ['unsubs', 'latestID']]


def create_embed(survey_id):
    try:
        data = handleJson.read_json_raw(path)
    except FileNotFoundError:
        SHL.output('Survey file not found. Creating it.')
        file_dir = os.path.join(handleJson.BASE_PATH, os.path.dirname(path))
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        handleJson.saveasjson(path, {})
        data = handleJson.read_json_raw(path)

    title = data[survey_id]['title']
    text = data[survey_id]['text']
    author = data[survey_id]['author']
    url = data[survey_id]['url']
    votes = len(data[survey_id]['voted'])
    answers = data[survey_id]['answers']
    results = data[survey_id]['results']
    answers_text = []

    for e in sorted(results, key=lambda x: results[x])[::-1]:
        if sum(results.values()):
            answer_pct = round(results[e] * 100 / sum(results.values()), 2)
            answer_pct = str(answer_pct).replace(".", ",")
        else:
            answer_pct = "0"
        answers_text.append(f'{e} - {answers[e]}: {answer_pct}%({results[e]})')
    answers_text = '\n'.join(answers_text)

    embed = InfoEmbed(title='Umfrage #' + str(survey_id) + ': ' + title)
    embed.url = url
    embed.add_field(name='Frage:', value=text, inline=False)
    embed.add_field(name='Ergebnis:', value=answers_text)
    embed.add_field(name='Beteiligung: ', value='Insgesamt abgestimmt haben: ' + str(votes))
    embed.set_footer(text='Umfrage von ' + author)

    return embed
