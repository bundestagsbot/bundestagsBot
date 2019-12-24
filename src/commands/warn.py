from discord.utils import get
from discord import HTTPException

from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed, WarningEmbed, NoticeEmbed, InfoEmbed
from bt_utils.config import cfg

SHL = Console("BundestagsBot Warn")

settings = {
    'name': 'warn',
    'mod_cmd': True,
}


async def main(client, message, params):
    to_warn = message.mentions
    if not to_warn:
        except_embed = WarningEmbed(title="No users supplied",
                                   description=f"Usage: {cfg.options.get('invoke_normal')}warn @user")
        await message.channel.send(embed=except_embed)

    for user in to_warn:
        warned = get(message.guild.roles, id=cfg.options.get("warn_role_id", 0)) in user.roles
        if not warned:
            try:
                warn_role = get(message.guild.roles, id=cfg.options.get("warn_role_id", 0))
                await user.add_roles(warn_role)
            except HTTPException:
                if cfg.options.get("warn_role_id", 0):
                    except_embed = WarningEmbed(title="Role-assigment failed",
                                                description=f"Failed to assign role {cfg.options.get('warn_role_id', 0)}!")
                else:
                    except_embed = WarningEmbed(title="Role-assigment failed",
                                                description=f"No 'warn_role_id' defined!")
                await message.channel.send(embed=except_embed)
                return
            return_embed = SuccessEmbed(title="Warn", description=f"Warned {user.display_name}")
            try:
                pm_embed = InfoEmbed(title="Warn",
                                         description=f"You were warned by {message.author.display_name}\n"
                                                     f"Please read our server rules.\n"
                                                     f"If you do not understand this message, please ask a moderator.")
                await user.send(embed=pm_embed)
            except HTTPException:  # if users privacy settings do not allow dm
                pass
            await message.channel.send(embed=return_embed)
        else:
            warned_embed = NoticeEmbed(title="Warn", description=f"User {user.display_name} has already been warned once!")
            await message.channel.send(embed=warned_embed)
