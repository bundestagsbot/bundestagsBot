from bt_utils.config import cfg
from bt_utils.handle_sqlite import DatabaseHandler
from bt_utils.console import *
SHL = Console("ReactionStats")
DB = DatabaseHandler()


async def handle_reaction(msg, payload, mode):
    user_id = msg.author.id
    if user_id == payload.user_id:
        return

    is_custom_emoji = hasattr(payload.emoji, 'id')
    if not is_custom_emoji:
        return

    roles = cfg.options["roles_stats"]
    emoji_id = payload.emoji.id
    is_emoji_none = emoji_id is None
    is_role = str(emoji_id) in roles.keys()
    if not is_role or is_emoji_none:
        return

    role_reaction = cfg.options["roles_stats"][str(emoji_id)]
    reaction_recipient = msg.author
    users = DB.get_all_users()
    if mode == "add":
        if reaction_recipient.id not in [item[0] for item in users]:
            # add new user to db
            SHL.output(f"Adding user {reaction_recipient.id} to the DB.")
            DB.add_user(reaction_recipient.id, roles)
        if role_reaction in cfg.options["roles_stats"].values():
            SHL.output(f"Added reaction {role_reaction} for user {reaction_recipient.display_name}")
            DB.add_reaction(reaction_recipient.id, role_reaction)
    elif mode == "remove":
        if reaction_recipient.id not in [item[0] for item in users]:
            SHL.output(f"Adding user {reaction_recipient.id} to the DB.")
            DB.add_user(reaction_recipient.id, roles)
            # finished here, because new user is initialized with 0 anyway
            return
        if role_reaction in cfg.options["roles_stats"].values():
            SHL.output(f"Removed reaction {role_reaction} for user {reaction_recipient.display_name}")
            DB.remove_reaction(reaction_recipient.id, role_reaction)
