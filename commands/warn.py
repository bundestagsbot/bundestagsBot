from bt_utils.console import Console
from discord.utils import get
SHL = Console("BundestagsBot Warn")

settings = {
    'name': 'warn',
    'mod_cmd': True,
}


async def main(client, message, params):
    badbois = str(message.content)[5:].strip()
    for member in client.get_all_members():
        if member.mention == badbois:
            badboi = member
    warned = get(client.get_guild(531445761733296130).roles, name='ErsteVerwarnung') in badboi.roles
    if not warned:
        await message.channel.send(content=badboi.mention + ' verwarnt!')
        punishrole = get(client.get_guild(531445761733296130).roles, id=533336650139435021)
        await badboi.add_roles(punishrole)
    else:
        await message.channel.send(content='Benutzer wurde bereits einmal verwarnt!')
