from bt_utils.console import Console
from bt_utils.config import cfg
from bt_utils.embed_templates import SuccessEmbed, NoticeEmbed, ErrorEmbed
from bt_utils import handleJson
from bt_utils.custom_exceptions import *
SHL = Console("BundestagsBot Answer")

settings = {
    'name': 'answer',
    'channels': ['dm'],
    'log': False
}

path_to_surveys = 'content/surveys.json'
path_to_unsubs = 'content/subs.json'


async def main(client, message, params):
    success = SuccessEmbed(title="Answer")
    error = NoticeEmbed(title="Answer")
    try:
        data = handleJson.read_json_raw(path_to_surveys)
        unsubs = handleJson.read_json_raw(path_to_unsubs)
    except:
        error = ErrorEmbed(title="Submit",
                           description="Something went wrong. Please contact an admin.")
        await message.channel.send(embed=error)
        return
    embed = error
    try:
        if not subscribed(unsubs, message.author.id):
            raise UserNotSubscribedException()
        if len(params) < 2 or params[0][0] != '#':
            raise CommandSyntaxException()
        survey_id = params[0][1:]
        if not survey_id.isdigit():
            raise InvalidSurveyIdException(survey_id)
        if not survey_id_is_valid(data, survey_id):
            raise InvalidSurveyIdException(survey_id)
        survey_data = data[survey_id]
        if message.author.id in survey_data['voted']:
            raise AlreadyVotedException()
        answers = [e.lower().strip() for e in params[1:]]
        invalid_answers = check_answers(answers, len(survey_data['answers']))
        if invalid_answers:
            raise AnswerNotFoundException(invalid_answers, survey_data['answers'])
        vote(message.author.id, survey_id, answers)
        embed = success
        embed.description = f'Danke für deine Teilnahme!\n' \
                            f'Du kannst die Ergebnisse mit\n' \
                            f'{cfg.options["invoke_normal"]}result #{survey_id} sehen.'

    except UserNotSubscribedException as e:
        embed.description = f"You have to be subscribed to participate. Use {cfg.options['invoke_normal']}sub True"
    except AnswerNotFoundException as e:
        embed.description = f"Invalid answers: {e.invalid_answers}\nPossible answers: 1-{e.max_index}"
    except AlreadyVotedException as e:
        embed.description = "You cannot vote twice."
    except SurveyNotFoundException as e:
        embed.description = f"#{e.survey_id} could not be assigned to a survey."
    except InvalidSurveyIdException as e:
        embed.description = f"{e.survey_id} is an invalid ID."
    except CommandSyntaxException as e:
        embed.description = f"Invalid syntax.\nPlease use {cfg.options['invoke_normal']}answer #survey_id Answer"
    finally:
        await message.channel.send(embed=embed)


def vote(user_id, survey_id, answers):
    data = handleJson.read_json_raw(path_to_surveys)
    data[survey_id]['voted'].append(user_id)
    for answer in set(answers):
        data[survey_id]['results'][answer] += 1
    handleJson.saveasjson(path_to_surveys, data)


def survey_id_is_valid(data, survey_id):
    return str(survey_id) in [key for key in data.keys() if key not in ['unsubs', 'latestID']]


def subscribed(data, user_id):
    return user_id not in data['unsubs']


def check_answers(answers, max_ind):
    invalid = []
    for answer in answers:
        try:
            if int(answer) not in range(1, int(max_ind) + 1):
                invalid.append(answer)
        except ValueError:
            invalid.append(answer)
    return invalid
