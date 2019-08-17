from discord import Embed, Colour
from datetime import datetime


class SimpleEmbed(Embed):
    def __init__(self, title="", description=""):
        super().__init__()
        self.timestamp = datetime.utcnow()
        self.url = "https://github.com/bundestagsBot/bundestagsBot"
        self.title = title
        self.description = description


# Only use this when an interal error occurred. e.g. invalid config or HTTPError
class WarningEmbed(Embed):
    def __init__(self, title="", description=""):
        super().__init__()
        self.timestamp = datetime.utcnow()
        self.colour = Colour.red()
        self.url = "https://github.com/bundestagsBot/bundestagsBot"
        self.title = title
        self.description = description


# Only use this when all actions ran as the user would expect them to
class SuccessEmbed(Embed):
    def __init__(self, title="", description=""):
        super().__init__()
        self.timestamp = datetime.utcnow()
        self.colour = Colour.green()
        self.url = "https://github.com/bundestagsBot/bundestagsBot"
        self.title = title
        self.description = description


# Only use this to provide information that are not directly linked to the maintask. e.g. missing value but replacing it
class InfoEmbed(Embed):
    def __init__(self, title="", description=""):
        super().__init__()
        self.timestamp = datetime.utcnow()
        self.colour = Colour.light_grey()
        self.url = "https://github.com/bundestagsBot/bundestagsBot"
        self.title = title
        self.description = description


# Only use this to inform the user about something critical that changed the main outcome. (No error occurred)
class NoticeEmbed(Embed):
    def __init__(self, title="", description=""):
        super().__init__()
        self.timestamp = datetime.utcnow()
        self.colour = Colour.orange()
        self.url = "https://github.com/bundestagsBot/bundestagsBot"
        self.title = title
        self.description = description
