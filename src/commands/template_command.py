import os.path

from bt_utils.console import Console
from bt_utils.get_content import content_dir

SHL = Console("BundestagsBot Template Command")  # Use SHL.output(text) for all console based output!

settings = {
    'name': 'template',  # name/invoke of your command
    'mod_cmd': True,  # if this cmd is only useable for users with the teamrole
    'channels': ['team'],  # allowed channels: [dm, bot, team, all]; use !dm to blacklist dm
    'log': True,  # if this cmd should be logged to the console, default: True
}

# global / changeable variables
PATH = os.path.join(content_dir, "template.json")


# client, message object
# params is a list of the message content splitted at spaces
async def main(client, message, params):
    pass
