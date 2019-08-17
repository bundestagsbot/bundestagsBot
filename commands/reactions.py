from bt_utils.console import Console
SHL = Console("BundestagsBot Roles")

settings = {
    'name': 'reactions',
    'channels': ['all'],
}


async def main(client, message, params):
    # extract name argument from message
    # reactions = get role database for that name
    # create one big message which contains all numbers and reaction (emojis)
    await message.channel.send(content=message.author.mention + 'Reaktionen:')
