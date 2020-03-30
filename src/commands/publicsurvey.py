from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed
from bt_utils.config import cfg
from bt_utils import handleJson
from discord import Embed, Colour
import datetime
import os.path

from bt_utils.get_content import content_dir

SHL = Console("BundestagsBot PublicSurvey")

settings = {
    'name': 'publicsurvey',
    'mod_cmd': True,
    'channels': ['team'],
}

path = os.path.join(content_dir, "surveys.json")
subs_path = os.path.join(content_dir, "subs.json")


async def main(client, message, params):

    def message_check(m):
        return m.channel == message.channel and message.author == m.author

    await message.channel.send('Title:')
    msg = await client.wait_for('message', check=message_check)
    title = msg.content

    await message.channel.send('Text:')
    msg = await client.wait_for('message', check=message_check)
    text = msg.content

    await message.channel.send('Do you want to supply a url?(y/n)')
    msg = await client.wait_for('message', check=message_check)
    choice = msg.content
    if choice.lower()[0] == 'y':
        await message.channel.send('Url:')
        msg = await client.wait_for('message', check=message_check)
        url = msg.content
    else:
        url = 'https://github.com/bundestagsBot/bundestagsBot'

    await message.channel.send('Type +finish once you\'re done')
    answers = []
    while True:
        await message.channel.send(f'Answer#{len(answers) + 1}:')
        msg = await client.wait_for('message', check=message_check)
        answer = msg.content.strip()
        if answer == "+finish":
            break
        else:
            answers.append(answer)

    await message.channel.send('How many answers is a user allowed to give?')
    while True:
        try:
            msg = await client.wait_for('message', check=message_check)
            max_answers = int(msg.content)
        except ValueError:
            await message.channel.send("Invalid input. Please try again")
        else:
            break

    answers = dict(enumerate(answers, 1))

    survey_id = get_survey_id()
    embed = create_survey(title, text, message.author, answers, max_answers, url, survey_id)
    msg = await message.channel.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

    def reaction_check(reaction, user):
        e = str(reaction.emoji)
        return user == message.author and e.startswith(('✅', '❌'))

    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=reaction_check)
    await msg.delete()

    if str(reaction.emoji).startswith('❌'):
        return
    # if approved add to json and send embed to all discord members who are not unsubscribed:

    data = handleJson.readjson(path)
    data[survey_id] = {}
    data[survey_id]['title'] = title.strip()
    data[survey_id]['text'] = text.strip()
    data[survey_id]['author'] = str(message.author.name)
    data[survey_id]['author_id'] = message.author.id
    data[survey_id]['url'] = url
    data[survey_id]['voted'] = []
    data[survey_id]['max_answers'] = max_answers
    data[survey_id]['answers'] = answers
    data[survey_id]['results'] = {}
    for a in range(1, len(data[survey_id]['answers']) + 1):  # so answers will be displayed sorted
        data[survey_id]['results'][a] = 0
    data['latestID'] += 1

    handleJson.saveasjson(path, data)

    # send to subscribers:
    members = client.get_guild(message.guild.id).members
    unsubs = handleJson.read_json_raw(subs_path)['unsubs']
    received, failed = 0, 0
    for m in [e for e in members if e.id not in unsubs]:
        try:
            received += 1
            await m.send(embed=embed)
        except:
            failed += 1

    success = SuccessEmbed(title='Publicsurvey')
    success.description = f'Umfrage an {received-failed} Personen gesendet.\n' \
                          f'{failed} Personen haben die Nachricht abgelehnt.'
    await message.channel.send(embed=success)


def create_survey(title, text, author, answers, max_answers, url, survey_id):
    answers_text = "\n".join([f'{e} - {answers[e]}' for e in answers])
    embed = Embed(title='Umfrage #' + str(survey_id) + ': ' + title, color=Colour.green(), url=url)
    embed.timestamp = datetime.datetime.utcnow()
    embed.add_field(name='Frage:', value=text, inline=False)
    embed.add_field(name='Antwortmöglichkeiten:', value=answers_text, inline=False)
    embed.add_field(name='Antwort:',
                    value=f'Beantworte diese Umfrage mit:\n'
                          f'{cfg.get("invoke_normal")}answer #{survey_id} 1-{len(answers)}\n'
                          f'Mehrfachantwort:\n'
                          f'{cfg.get("invoke_normal")}answer #{survey_id} 1 2\n'
                          f'Du kannst maximal {max_answers} Antworten angeben'
                    )
    embed.add_field(name='Ergebnisse:',
                    value=f'Ergebnisse erhälst du mit:\n{cfg.get("invoke_normal")}result #{survey_id}')
    embed.add_field(name='Keine weitere Umfrage:',
                    value=f'Wenn du keine weiteren Umfragen mehr erhalten willst, verwende: '
                          f'{cfg.get("invoke_normal")}sub False')
    embed.add_field(name='Information:',
                    value=f'Diskutiere über diese Umfrage in <#{cfg.get("channel_ids", dict()).get("main", 0)}>.\n'
                          'Du kannst deine Antwort nicht mehr ändern.\n'
                          'Diese Umfrage ist anonym.\n'
                          'Bei Fragen wende dich an die Developer.')
    embed.set_footer(text="Umfrage von " + author.name)
    return embed


def get_survey_id():
    return int(handleJson.readjson(path)['latestID']) + 1
