from bt_utils.console import Console
from bt_utils.handle_sqlite import DatabaseHandler
from bt_utils.config import cfg
from bt_utils.embed_templates import NoticeEmbed, InfoEmbed

SHL = Console("BundestagsBot Reactions")
DB = DatabaseHandler()

settings = {
    'name': 'reactions',
    'channels': ['all'],
}


async def main(client, message, params):
    if not len(message.mentions):
        embed = NoticeEmbed(title="Reactions", description=message.author.mention + 'Bitte einen Nutzer angeben')
        await message.channel.send(embed=embed)
        return

    data = DB.get_specific_user(message.mentions[0].id)
    if data:
        header = 'Reaktionen zu Nachrichten von ' + message.mentions[0].display_name + '\n'
        content = ''
        # skip name and id
        for i, role in enumerate(cfg.options["roles_stats"].items(), 1):
            if data[i] > 0:
                emoji_id = role[0]
                emoji_obj = await message.guild.fetch_emoji(emoji_id)
                emoji_str = "<:" + emoji_obj.name + ":" + emoji_id + ">"
                content += "" + emoji_str + ": " + str(data[i]) + "\n"
        embed = InfoEmbed(title=header, description=content)
        await message.channel.send(embed=embed)
    else:
        embed = NoticeEmbed(title="Reactions",
                            description=message.author.mention + 'Dieser Benutzer hat noch keine Reaktionen erhalten.')
        await message.channel.send(embed=embed)
