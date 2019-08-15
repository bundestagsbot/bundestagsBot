from discord import Embed, Color
from datetime import datetime
from bt_utils.config import cfg

welcome_de = """
    __**Willkommen**__
    
    Unter <#{}> kannst du dir Rollen zuweisen. 
    Beispielsweise Themen, die dich interessieren oder deine politische Ausrichtung
    \n
    Oder sag doch einfach in <#{}> hallo :smiley:
    \n
    In <#{}> kannst du den Bot verwenden.
    Versuche doch mal `>umfrage`
    \n
    Gerne kannst du mir hier mit `>submit text` ein Feedback oder ein Hinweis hinterlassen, die ich anonym ans Serverteam weiterleite.
    Wenn du Themen öffentlich ansprechen willst,
    kannst du das aber auch gerne in <#{}> tun.
    
    Beteilige dich gerne an der Entwicklung des BundestagsBot:\n https://github.com/bundestagsBot/bundestagsBot
    """


def create_embed(lang="de"):
    embed = Embed(title=f'Willkommen!', color=Color.dark_red(),
                          url="https://github.com/bundestagsBot/bundestagsBot")
    embed.timestamp = datetime.utcnow()
    if lang == "de":
        embed.description = welcome_de.format(cfg.options["channel_ids"]["roles"][0],
                                              cfg.options["channel_ids"]["welcome"][0],
                                              cfg.options["channel_ids"]["dev"][0],
                                              cfg.options["channel_ids"]["suggestions"][0])
    return embed
