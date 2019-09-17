from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed, NoticeEmbed
from bt_utils.config import cfg
from discord.utils import get
SHL = Console("BundestagsBot Iam")

settings = {
    'name': 'iam',
    'channels': ['bot'],
}


async def main(client, message, params):
    success = SuccessEmbed(title="I am")
    error = NoticeEmbed(title="I am")

    roles = cfg.options["roles"]
    lower_roles = [e.lower() for e in list(roles.values())]

    want_role = ' '.join(params).strip().lower()
    if want_role in lower_roles:
        assign_role = list(roles.values())[lower_roles.index(want_role)]
        role = get(client.get_guild(message.guild.id).roles, name=assign_role)
        if role not in message.author.roles:
            await message.author.add_roles(role)
            success.description = f"Role {role.name} added."
            await message.channel.send(embed=success)
        else:
            await message.author.remove_roles(role)
            success.description = f"Role {role.name} removed."
            await message.channel.send(embed=success)
    else:
        error.description = "Please use one of these roles:"\
                            ' ```\n' + '\n'.join(list(roles.values())) + ' ```'
        await message.channel.send(embed=error)
