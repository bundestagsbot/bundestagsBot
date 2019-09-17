from bt_utils.console import Console
from bt_utils.embed_templates import InfoEmbed
SHL = Console("BundestagsBot Help")

settings = {
    'name': 'help',
    'channels': ['dm', 'bot'],
}


async def main(client, message, params):
    if len(params) == 0:
        embed = help_embed()
    elif params[0] == 'survey':
        embed = survey_help_embed()
    else:
        embed = help_embed()
    await message.channel.send(embed=embed)


def help_embed():
    embed = InfoEmbed(title='Hilfe - BundestagsBot v1')
    embed.set_thumbnail(url='https://cdn0.iconfinder.com/data/icons/handdrawn-ui-elements/512/Question_Mark-512.png')
    embed.description = '-Benutze >survey Titel; Beschreibung; <Anzahl>\n' \
                        'um eine Umfrage zu erstellen. >help survey für mehr Details\n\n'\
                        '-Benutze >iam [Politik] um dir diese Rolle zuzuweisen.\n\n'\
                        '-Benutze >roles für eine Übersicht der Rollenverteilung.\n\n'\
                        '-Benutze >answer #id answer um auf eine Umfrage zu antworten.\n\n' \
                        '-Benutze >result #id um Ergebnisse einer Umfrage einzusehen.\n\n' \
                        '-Benutze >sub False um keine weiteren Umfragen mehr zu erhalten.\n\n' \
                        '-Benutze >submit Text um Anfragen ans Serverteam zu stellen.\n\n' \
                        '-Benutze >reactions [@user] um Reaktionen an Nachrichten von [@user] zu sehen.\n\n' \
                        '-Benutze >umfrage [Parlamentsnummer]\nKeine Nummer für Bundestag'\


    embed.add_field(name='Liste:',
                    value='0: Bundestag\n1: Baden-Württemberg\n2: Bayern\n3: Berlin\n4: Brandeburg\n5: Bremen\n'
                          '6: Hamburg\n7: Hessen\n8: Mecklenburg-Vorpommern\n9: Niedersachsen\n10: NRW\n'
                          '11: Rheinland-Pfalz\n12: Saarland\n13: Sachsen\n14: Sachsen-Anhalt\n'
                          '15: Schleswig-Holstein\n16: Thüringen\n17: Europäisches Parlament')
    return embed


def survey_help_embed():
    embed = InfoEmbed(title='Hilfe - BundestagsBot v1')
    embed.set_thumbnail(url='https://cdn0.iconfinder.com/data/icons/handdrawn-ui-elements/512/Question_Mark-512.png')

    embed.description = '>survey; Titel; Beschreibung; <Anzahl>\n\n'\
                        'Anzahl ist optional und beschreibt die Anzahl an Reactionmöglichkeiten.\n\n'\
                        'So erzeugt >survey; Titel; Beschreibung; 5 eine Umfrage mit 5 Antwortmöglichkeiten, die du\n'\
                        'dann in deiner Beschreibung erklären musst.\n'\
                        'Mit "|" erzeugst du eine neue Zeile in deiner Beschreibung.\n'\
                        '**Beachte bitte die Trennung der Argumente via Semikolon!**'
    return embed
