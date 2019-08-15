from bt_utils.console import Console
from bt_utils.config import cfg
import discord
import datetime
import pkgutil
import importlib
SHL = Console("BundestagsBot", cls=True)

"""

init script for the commands module
when adding a new command please specify your settings in a dictionary as in every other command file 

mandatory:
    name: the name of your command as a string
        example: 'test'
optional:
    channels: list of channels your command can be used in represented by strings specified in allowed channels
              (use "!" to blacklist specific channels)
        example: ['dm', 'bot']
        default value: ['bot']
    log: a boolean that specifies if your command will log to the console when used
        default: True
    mod: a boolean that specifies if your command can only be used by team members
        default: False

"""

commands = {}
mod_commands = {}

# TODO: implement cfg.options["mod_channel_ids"]
allowed_channels = {
    'dm': {"cond": lambda message: isinstance(message.channel, discord.DMChannel), "name": "Dm"},
    'dev': {"cond": lambda message: message.channel.id == 546247189794652170, "name": ""},
    'bot': {"cond": lambda message: message.channel.id == 533005337482100736, "name": "<#533005337482100736>"},
    'team': {"cond": lambda message: message.channel.id == 531818586105315355, "name": ""},
    'team2': {"cond": lambda message: message.channel.id == 545330367150817310, "name": ""},
}


def parse(content, mod_cmd):
    if mod_cmd:
        ret = content[len(cfg.options["invoke_mod"]):].split(" ")
    else:
        ret = content[len(cfg.options["invoke_normal"]):].split(" ")
    return [e for e in ret if e != ""]


def register(func, settings):
    name = settings.get('name')
    channels = settings.get('channels', ['bot'])  # if no channels are supplied the bot channel will be used
    log = settings.get('log', True)
    if "dev" not in channels: channels.append('dev')
    if "team" not in channels: channels.append('team')
    if "team2" not in channels: channels.append('team2')
    # use ['all'] to allow all channels
    mod_cmd = settings.get('mod_cmd', False)
    blacklisted = [channel[1:] for channel in channels if
                   channel[0] == '!']  # use '!' to blacklist a channel instead of whitelisting

    if len(blacklisted) != 0:  # if a channel is blacklisted
        channel_conds = [lambda message: not (any([allowed_channels[e]['cond'](message) for e in blacklisted]))]
        channel_names = []
        channels = [channel for channel in allowed_channels.keys() if channel not in blacklisted]
    elif channels[0] != 'all':
        channel_conds = [allowed_channels[channel]['cond'] for channel in channels]  # always allow in dev channel
        channel_names = [allowed_channels[channel]['name'] for channel in channels if
                         channel != 'dev']  # dont show devchannel as alternative
    else:
        channel_conds = [lambda x: True]
        channel_names = []

    if mod_cmd:
        async def wrapper(client, message, params):
            if user_in_team(message.author):
                await func(client, message, params)

            else:
                await message.channel.send(content='Du hast nicht genug Rechte um diesen Befehl zu benutzen!')

        mod_commands[name] = wrapper
    else:
        async def wrapper(client, message, params):
            if log:
                SHL.output(f"{message.author} used {message.content}")  # logging
            if any([e(message) for e in channel_conds]):  # check if any of the given channels were used
                await func(client, message, params)
            else:
                if len(channel_names) != 0:
                    await message.channel.send(content='Benutze einen dieser Kanäle: \n' + "\n".join(channel_names))
                else:
                    await message.channel.send(
                        content='Folgende Kanäle sind nicht zulässig: \n' + "\n".join(blacklisted))
        commands[name] = wrapper
    print('\033[92m' + (str(datetime.datetime.now())[:-7]) + f' \033[92m[BundestagsBot] registered {settings}')


def user_in_team(user):
    for role in user.roles:
        if role.id == cfg.options["team_role_id"]:
            return True
    return False


def register_all():
    pkgutil.extend_path(__path__, __name__)
    for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__ + '.'):
        # importing all files in directory and registering them
        command = importlib.import_module(modname)
        register(command.main, command.settings)


register_all()