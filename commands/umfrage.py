from bt_utils.console import Console
from bt_utils.config import cfg
from bt_utils import handleJson
from bt_utils.cache_handler import cache
from datetime import datetime
import requests
from discord import Embed, Colour
SHL = Console("BundestagsBot Umfrage")

settings = {
    'name': 'umfrage',
    'channels': ['dm', 'bot'],
}


async def main(client, message, params):
    api_cache = cache.get_data(key="dawum_api")
    data = api_cache.get("data", {})
    timestamp = api_cache.get("timestamp", "")
    # if cache invalid
    if timestamp != datetime.now().strftime("%Y.%m.%d") or data == {} or not cfg.options.get("use_cache", True):
        try:
            data = requests.get('https://api.dawum.de/').json()
        except:
            SHL.output("Something went wrong while loading the request.")
            data = {}
        # write in cache
        cache.write_to_cache(data, key="dawum_api")

    parliament = 0
    if len(params) != 0:
        if parliament in range(0, 18):
            parliament = int(params[0])
        else:
            parliament = 0

    embed = create_embed(data, parliament)

    if embed is None:
        # rewrite cache just to be sure
        try:
            data = requests.get('https://api.dawum.de/').json()
        except:
            SHL.output("Something went wrong while loading the request.")
            data = {}
        cache.write_to_cache(data, key="dawum_api")
        # TODO: Send a basic "Error occurred" embed here. That should be implemented everywhere
    else:
        await message.channel.send(embed=embed)


def create_embed(data, parl=0):
    try:
        for e in data['Surveys']:
            if int(data['Surveys'][e]['Parliament_ID']) == parl:
                last = e
                break

        embed = Embed(title='Aktuelle Umfrage ' + data['Parliaments'][str(parl)]['Name'],
                      color=Colour.dark_red())
        embed.description = 'Wahl: ' + data['Parliaments'][str(parl)]['Election'] +\
                            '\nUmfrage von: ' + data['Institutes'][data['Surveys'][last]['Institute_ID']]['Name'] + \
                            '\nUmfrage im Auftrag von: ' + data['Taskers'][data['Surveys'][last]['Tasker_ID']]['Name']
        embed.set_footer(text='Umfrage von: ' + str(data['Surveys'][last]['Date']))

        for e, party in enumerate(data['Surveys'][last]['Results']):
            embed.add_field(name=str(data['Parties'][party]['Name']),
                            value=str(data['Surveys'][last]['Results'][party])+'%\n',
                            inline=False)
    except KeyError:
        SHL.output("Got an invalid syntax. Perhaps the API is not available or deprecated")
        return
    except:
        SHL.output("Something went wrong while parsing the Embed. Perhaps the API is not available or deprecated")
        return
    return embed
