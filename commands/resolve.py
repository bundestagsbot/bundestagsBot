from utils import handleJson

settings = {
    'name': 'resolve',
    'channels': ['team'],
    'mod_cmd': True,
    'log': True
}

path = 'C:/server/settings/BoB/submits.json'


async def main(client, message, params):
    if len(str(message.content).split(' ')) == 2:
        id = str(message.content).split(' ')[1][1:]
        if id.isdigit():
            data = handleJson.readjson(path)
            if id in data.keys():
                await message.channel.send(content=f'Anfrage #{id} ist von:\n{data[id]["author"]}\n{data[id]["authorID"]}')
            else:
                await message.channel.send(content=f'{id} konnte keiner Anfrage zugeordnet werden')
        else:
            await message.channel.send(content=f'{id} ist keine gültige ID')
    else:
        await message.channel.send(content='Ungültige Anzahl an Argumenten. Versuche +resolve #id')

