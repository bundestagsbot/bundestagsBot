import discord

settings = {
    'name': 'help',
    'channels': ['dm', 'bot'],
}

async def main(client, message, params):

    if len(params) == 0:
        embed = helpembed()
    elif params[0] == 'survey':
        embed = surveyhelpembed()
    else:
        return
    await message.channel.send(embed=embed)

def helpembed():
    embed = discord.Embed(title='Hilfe - BundestagsBot v1', color=discord.colour.Colour.orange())
    embed.set_thumbnail(url='https://cdn0.iconfinder.com/data/icons/handdrawn-ui-elements/512/Question_Mark-512.png')
    embed.description = '-Benutze >survey; Titel; Beschreibung; <Anzahl> um eine Umfrage zu erstellen. >help survey für mehr Details\n\n'\
                        '-Benutze >iam [Politik] um dir diese Rolle zuzuweisen.\n\n'\
                        '-Benutze >roles für eine Übersicht der Rollenverteilung\n\n'\
                        '-Benutze >umfrage [Parlamentsnummer]\nKeine Nummer für Bundestag'\


    embed.add_field(name='Liste:', value='0: Bundestag\n1: Baden-Württemberg\n2: Bayern\n3: Berlin\n4: Brandeburg\n5: Bremen\n6: Hamburg\n7: Hessen\n8: Mecklenburg-Vorpommern\n9: Niedersachsen\n10: NRW\n11: Rheinland-Pfalz\n12: Saarland\n13: Sachsen\n14: Sachsen-Anhalt\n15: Schleswig-Holstein\n16: Thüringen\n17: Europäisches Parlament')
    return embed

def surveyhelpembed():
    embed = discord.Embed(title='Hilfe - BundestagsBot v1', color=discord.colour.Colour.orange())
    embed.set_thumbnail(url='https://cdn0.iconfinder.com/data/icons/handdrawn-ui-elements/512/Question_Mark-512.png')

    embed.description = '>survey Titel Beschreibung <Anzahl>\n'\
                        'Anzahl ist optional und beschreibt die Anzahl an Reactionmöglichkeiten.\n'\
                        'So erzeugt >survey; Titel; Beschreibung; 5 eine Umfrage mit 5 Antwortmöglichkeiten, die du\n'\
                        'dann in deiner Beschreibung erklären musst.\n'\
                        'Beachte bitte die Trennung der Argumente via Semikolon!'
    return embed