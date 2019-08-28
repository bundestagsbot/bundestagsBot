from bt_utils.console import Console
from bt_utils.handle_sqlite import DatabaseHandler
from bt_utils.config import cfg
from bt_utils.embed_templates import NoticeEmbed

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
            header = 'Reaktionen zu Nachrichten von ' + user_name + '\n'
            content = ''
            # skip name and id
            i = 2
            for role in cfg.options["roles_stats"].items():
                if user[i] > 0:
                    emoji_id = role[0]
                    emoji_obj = await message.guild.fetch_emoji(emoji_id)
                    emoji_str = "<:" + emoji_obj.name + ":" + emoji_id + ">"
                    content += "" + emoji_str + ": " + str(user[i]) + "\n"
                i = i + 1
            embed = NoticeEmbed(title=header, description=content)
            await message.channel.send(embed=embed)
        return
    await message.channel.send(content=message.author.mention + 'Der Benutzer existiert nicht')
