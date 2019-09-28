from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed
from bt_utils.config import cfg
from bt_utils import handleJson
from discord import Embed, Colour
import datetime
SHL = Console("BundestagsBot PublicSurvey")

settings = {
    'name': 'publicsurvey;',
    'mod_cmd': True,
    'channels': ['team'],
}
path = 'content/surveys.json'
subs_path = 'content/subs.json'


async def main(client, message, params):
    params = [p for p in str(message.content).split(';')]
    if len(params) == 4 or not params[4]:  params.append('https://github.com/bundestagsBot/bundestagsBot')
    survey_id = get_survey_id()
    embed = create_survey(params[1], params[2], message.author, params[3], params[4], survey_id)
    msg = await message.channel.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

    def check(reaction, user):
        e = str(reaction.emoji)
        return user == message.author and e.startswith(('✅', '❌'))

    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    await msg.delete()

    if str(reaction.emoji).startswith('❌'): return
    # if approved add to json and send embed to all discord members who are not unsubscribed:

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
    members = client.get_guild(message.guild.id).members
    unsubs = handleJson.read_json_raw(subs_path)["unsubs"]
    received, failed = 0, 0
    for m in [e for e in members if e.id not in unsubs]:
        try:
            received += 1
            await m.send(embed=embed)
        except:
            failed += 1

    success = SuccessEmbed(title="Publicsurvey")
    success.description = f"Umfrage an {received-failed} Personen gesendet.\n" \
                          f"{failed} Personen haben die Nachricht abgelehnt."
    await message.channel.send(embed=success)


def create_survey(title, text, author, answers, url, survey_id):
    embed = Embed(title='Umfrage #' + str(survey_id) + ': ' + title, color=Colour.green(), url=url)
    embed.timestamp = datetime.datetime.utcnow()
    embed.add_field(name='Frage:', value=text.replace('|', '\n'), inline=False)
    embed.add_field(name='Antwort:',
                    value=f'Beantworte diese Umfrage mit:\n'
                          f'{cfg.options["invoke_normal"]}answer #{survey_id} 1-{answers.strip()}')
    embed.add_field(name='Ergebnisse:',
                    value=f'Ergebnisse erhälst du mit:\n{cfg.options["invoke_normal"]}result #{survey_id}')
    embed.add_field(name='Keine weitere Umfrage:',
                    value=f'Wenn du keine weiteren Umfragen mehr erhalten willst, verwende: '
                          f'{cfg.options["invoke_normal"]}sub False')
    embed.add_field(name='Information:', value='Du kannst deine Antwort nicht mehr ändern.\n'
                                               'Diese Umfrage ist anonym.\n'
                                               'Bei Fragen wende dich an die Developer.')
    embed.set_footer(text="Umfrage von " + author.name)
    return embed


def get_survey_id():
    return int(handleJson.readjson(path)['latestID']) + 1
