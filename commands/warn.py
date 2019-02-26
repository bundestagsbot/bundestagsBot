from discord.utils import get

settings = {
    'name': 'warn',
    'mod_cmd': True,
}

async def main(client, message, params):
    badbois = str(message.content)[5:].strip()
    for member in client.get_all_members():
        if member.mention == badbois:
            badboi = member
    vorbestraft = False
    for role in badboi.roles:
        if role.name == 'ErsteVerwarnung':
            vorbestraft = True
            await message.channel.send(content='Benutzer wurde bereits einmal verwarnt!')
            break
    if not vorbestraft:
        await message.channel.send(content=badboi.mention + ' verwarnt!')
        punishrole = get(client.get_guild(531445761733296130).roles, id=533336650139435021)
        await badboi.add_roles(punishrole)