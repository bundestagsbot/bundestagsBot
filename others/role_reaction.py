from bt_utils.config import cfg
from discord.utils import get


async def reaction_add(client, payload):
    if payload.channel_id in cfg.options["channel_ids"]["roles"]:
        if str(payload.emoji.id) in cfg.options["roles"].keys():
            role = get(client.get_guild(531445761733296130).roles, name=cfg.options["roles"][str(payload.emoji.id)])
            user = client.get_guild(531445761733296130).get_member(payload.user_id)
            if role not in user.roles:
                await user.add_roles(role)


async def reaction_remove(client, payload):
    if payload.channel_id in cfg.options["channel_ids"]["roles"]:
        if str(payload.emoji.id) in cfg.options["roles"].keys():
            role = get(client.get_guild(531445761733296130).roles, name=cfg.options["roles"][str(payload.emoji.id)])
            user = client.get_guild(531445761733296130).get_member(payload.user_id)
            if role in user.roles:
                await user.remove_roles(role)
