from discord.utils import get

settings = {
    'name': 'iam',
    'channels': ['bot'],
}

roles = ['Liberal', 'Konservativ', 'Sozialdemokratisch', 'Sozialistisch', 'Nationalistisch', 'nsfw', 'Sozialliberal', 'Wirtschaftsliberal', 'Grün']

async def main(client, message, params):
    role = ''.join(params)
    if role.lower() in [e.lower() for e in roles]:
        role = get(client.get_guild(531445761733296130).roles, name=role[0].upper()+role[1:].lower())
        if role in message.author.roles:
            await message.author.add_roles(role)
            await message.channel.send(content=message.author.mention + ' Rolle ' + role.name + ' hinzugefügt.')
        else:
            await message.author.remove_roles(role)
            await message.channel.send(centent=message.author.mention + ' Rolle ' + role.name + ' entfernt.')
    else:
        await message.channel.send(content='Please use one of the following roles: ```\n' + '\n'.join([e for e in roles if e != 'nsfw']) + ' ```')
