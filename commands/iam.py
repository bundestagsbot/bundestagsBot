from discord.utils import get

settings = {
    'name': 'iam',
    'channels': ['bot'],
}

roles = ['Liberal', 'Konservativ', 'Sozialdemokratisch', 'Sozialistisch', 'Nationalistisch', 'Nsfw', 'Sozialliberal',
         'Wirtschaftsliberal', 'Grün', 'Podcast', 'Patriotisch', "Finanzen", "Außenpolitik", "Justiz", "Militär",
         "Familie & Jugend", "Verkehr & Infrastruktur", "Bildung & Forschung", "Innenpolitik", "Wirtschaft",
         "Arbeit & Soziales", "Ernährung & Landwirtschaft", "Gesundheit", "Umwelt & Naturschutz", "Entwicklungshilfe"]
lower_roles = [e.lower() for e in roles]


async def main(client, message, params):
    want_role = ' '.join(params).strip().lower()
    if want_role in lower_roles:
        assign_role = roles[lower_roles.index(want_role)]
        role = get(client.get_guild(531445761733296130).roles, name=assign_role)
        if role not in message.author.roles:
            await message.author.add_roles(role)
            await message.channel.send(content=message.author.mention + ' Rolle ' + role.name + ' hinzugefügt.')
        else:
            await message.author.remove_roles(role)
            await message.channel.send(content=message.author.mention + ' Rolle ' + role.name + ' entfernt.')
    else:
        await message.channel.send(content='Bitte benutze eine dieser Rollen:'
                                           ' ```\n' + '\n'.join([e for e in roles if e != 'Nsfw']) + ' ```')
