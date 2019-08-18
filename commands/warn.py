from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed, WarningEmbed, NoticeEmbed, InfoEmbed
from bt_utils.config import cfg
from discord.utils import get
SHL = Console("BundestagsBot Warn")

settings = {
    'name': 'warn',
    'mod_cmd': True,
}


async def main(client, message, params):
    badbois = str(message.content)[5:].strip()
    badboi = None
    for member in client.get_all_members():
        if member.mention == badbois:
            badboi = member
            break
    if not badboi:
        embed = WarningEmbed(title="Warn", description=f"Could not find '{str(message.content)[5:].strip()}'")
        await message.channel.send(embed=embed)
        return
    warned = get(client.get_guild(531445761733296130).roles, id=cfg.options.get("warn_role_id", 0)) in badboi.roles
    if not warned:
        try:
            punishrole = get(client.get_guild(531445761733296130).roles, id=cfg.options.get("warn_role_id", 0))
            await badboi.add_roles(punishrole)
        except:
            if cfg.options.get("warn_role_id", 0):
                except_embed = WarningEmbed(title="Role-assigment failed",
                                            description=f"Failed to assign role {cfg.options.get('warn_role_id', 0)}!")
            else:
                except_embed = WarningEmbed(title="Role-assigment failed",
                                            description=f"No `warn_role_id` defined!")
            await message.channel.send(embed=except_embed)
            return
        return_embed = SuccessEmbed(title="Warn", description="Warned " + badboi.mention)
        try:
            badboi_embed = InfoEmbed(title="Warn",
                                     description=f"You were warned by {message.author.display_name}\n"
                                                 f"Please read our server rules.\n"
                                                 f"If you do not understand this message, please ask a moderator.")
            await badboi.send(embed=badboi_embed)
        except:  # if users privacy settings do not allow dm
            pass
        await message.channel.send(embed=return_embed)
    else:
        warned_embed = NoticeEmbed(title="Warn", description="User has already been warned once!")
        await message.channel.send(embed=warned_embed)
