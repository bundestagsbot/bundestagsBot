from discord.utils import get

settings = {
    'name': 'iam',
    'channels': ['bot'],
}

roles = ['Liberal', 'Konservativ', 'Sozialdemokratisch', 'Sozialistisch', 'Nationalistisch', 'nsfw', 'Sozialliberal', 'Wirtschaftsliberal', 'Grün']

async def main(client, message, params):
    role = ''.join(params)
    if role.lower() in [e.lower() for e in roles]:
        role = get(client.get_guild(531445761733296130).roles, name=role.capitalize())
        if role not in message.author.roles:
            await message.author.add_roles(role)
            await message.channel.send(content=message.author.mention + ' Rolle ' + role.name + ' hinzugefügt.')
        else:
            await message.author.remove_roles(role)
            await message.channel.send(content=message.author.mention + ' Rolle ' + role.name + ' entfernt.')
    else:
        await message.channel.send(content='Bitte benutze eine dieser Rollen: ```\n' + '\n'.join([e for e in roles if e != 'nsfw']) + ' ```')
