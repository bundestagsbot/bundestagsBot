from bt_utils.console import Console
from bt_utils.handle_sqlite import DatabaseHandler
from bt_utils.config import cfg

SHL = Console("BundestagsBot Reactions")
DB = DatabaseHandler()

settings = {
    'name': 'reactions',
    'channels': ['all'],
}


async def main(client, message, params):
    users = DB.get_all_users()
    if len(message.mentions) == 0:
        await message.channel.send(content=message.author.mention + 'Bitte einen Nutzer mit angeben')
        return

    for user in users:
        if message.mentions[0].id == user[0]:
            user_name = user[1]
            content = 'Reaktionen zu Nachrichten von ' + user_name + '\n'
            # skip name and id
            i = 2
            for role in cfg.options["roles"].items():
                if role[1] in cfg.options["roles_show"]:
                    if user[i] > 0:
                        content += "" + role[1] + ": " + str(user[i]) + "\n"
                    i = i + 1
            await message.channel.send(content=message.author.mention + content)
        return
    await message.channel.send(content=message.author.mention + 'Der Benutzer existiert nicht')
