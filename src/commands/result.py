from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed, ErrorEmbed, NoticeEmbed, InfoEmbed
from bt_utils.config import cfg
from bt_utils import handleJson
import os
SHL = Console("BundestagsBot Result")

settings = {
    'name': 'result',
    'channels': ['all'],
}

path = 'content/surveys.json'


async def main(client, message, params):
    error = NoticeEmbed(title="Result")
    success = SuccessEmbed(title="Result")

    if len(str(message.content).split(' ')) == 2:
        survey_id = params[0][1:]
        if survey_id.isdigit():
            if survey_id_is_valid(survey_id):
                try:
                    info = create_embed(survey_id)
                    await message.channel.send(embed=info)
                except:
                    error = ErrorEmbed(title="Result")
                    error.description = "Something went wrong. Please contact an admin."
                    await message.channel.send(embed=error)
            else:
                error.description = f"#{survey_id} could not be assigned to a survey."
                await message.channel.send(embed=error)
        else:
            error.description = f"{survey_id} is an invalid ID."
            await message.channel.send(embed=error)
    else:
        error.description = f"Invalid syntax.\nPlease use {cfg.options['invoke_normal']}result #surveyID"
        await message.channel.send(embed=error)


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
        SHL.output("Survey file not found. Creating it.")
        file_dir = os.path.join(handleJson.BASE_PATH, os.path.dirname(path))
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        handleJson.saveasjson(path, {})
        data = handleJson.read_json_raw(path)

    title = data[survey_id]["title"]
    text = data[survey_id]["text"]
    author = data[survey_id]["author"]
    url = data[survey_id]["url"]
    votes = len(data[survey_id]["voted"])
    answers = data[survey_id]["answers"]
    results = data[survey_id]["results"]

    embed = InfoEmbed(title='Umfrage #' + str(survey_id) + ': ' + title)
    embed.url = url
    embed.add_field(name='Frage:', value=text.replace('|', '\n'), inline=False)
    embed.add_field(name='Antwortmöglichkeiten:', value='1 - ' + str(answers))
    embed.add_field(name='Beteiligung: ', value='Insgesamt abgestimmt haben: ' + str(votes))
    embed.add_field(name='Ergebnis:', value='\n'.join([f"{results[e]} Stimmen für: {e}" for e in results.keys()
                                                       if results[e] != 0]), inline=False)
    embed.set_footer(text="Umfrage von " + author)

    return embed
