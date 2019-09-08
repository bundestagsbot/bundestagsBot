from bt_utils.console import Console
SHL = Console("BundestagsBot Template Command")

settings = {
    'name': 'template',  # name/invoke of your command
    'mod_cmd': True,  # if this cmd is only useable for users with the teamrole
    'channels': ['team'],  # allowed channels: [dm, bot, team, all]; use !dm to blacklist dm
    'log': True,  # if this cmd should be logged to the console, default: True
}

# global / changeable variables
PATH = "content/template.json"


# client, message object
# params is a list of the message content splitted at spaces
async def main(client, message, params):
    pass
