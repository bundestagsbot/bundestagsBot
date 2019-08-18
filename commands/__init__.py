from bt_utils.console import *
from bt_utils.config import cfg
import discord
import datetime
import pkgutil
import importlib
SHL = Console("CommandLoader")

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
    mod_cmd: a boolean that specifies if your command can only be used by team members
        default: False

"""

commands = {}
mod_commands = {}

allowed_channels = {
    'dm': {"cond": lambda message: isinstance(message.channel, discord.DMChannel), "name": "Dm"},
    'bot': {"cond": lambda message: message.channel.id in cfg.options["channel_ids"]["bot"], "name": f"<#{cfg.options['channel_ids']['bot']}>"},
    'team': {"cond": lambda message: message.channel.id in cfg.options["channel_ids"]["team"], "name": ""},
    'all': {"cond": lambda message: True, "name": ""}
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

    if 'team' not in channels: channels.append('team')  # every command should be accessible in the team, channels

    # use ['all'] to allow all channels
    mod_cmd = settings.get('mod_cmd', False)
    blacklisted = [channel[1:] for channel in channels if channel[0] == '!']  # use '!' to blacklist a channel instead of whitelisting

    if blacklisted:  # if a channel is blacklisted
        channel_conds = [lambda message: not (any([allowed_channels[e]['cond'](message) for e in blacklisted]))]
        channel_names = []
    else:
        channel_conds = [allowed_channels[channel]['cond'] for channel in channels]
        channel_names = [allowed_channels[channel]['name'] for channel in channels]

    if mod_cmd:
        async def wrapper(client, message, params):
            if log:
                SHL.set_prefix("CommandHandler")
                SHL.output(f"{message.author} used {message.content}")
            if user_in_team(message.author):
                await func(client, message, params)

            else:
                await message.channel.send(content='Du hast nicht genug Rechte um diesen Befehl zu benutzen!')

        mod_commands[name.lower()] = wrapper
    else:
        async def wrapper(client, message, params):
            if log:
                SHL.set_prefix("CommandHandler")
                SHL.output(f"{message.author} used {message.content}")  # logging
            if any([e(message) for e in channel_conds]):  # check if any of the given channels were used
                await func(client, message, params)
            else:
                if len(channel_names) != 0:
                    await message.channel.send(content='Benutze einen dieser Kanäle: \n' + "\n".join(channel_names))
                else:
                    await message.channel.send(
                        content='Folgende Kanäle sind nicht zulässig: \n' + "\n".join(blacklisted))
        commands[name.lower()] = wrapper
    SHL.output(f"Registered {settings.get('name', 'unknown command')}")


def user_in_team(user):
    for role in user.roles:
        if role.id == cfg.options["team_role_id"]:
            return True
    return False


def register_all():
    pkgutil.extend_path(__path__, __name__)
    for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__ + '.'):
        try:
            command = importlib.import_module(modname)
            register(command.main, command.settings)
        except:
            pass
    SHL.output(f"{red}========================{white}")


register_all()
