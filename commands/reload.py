from bt_utils.console import Console
from bt_utils.config import cfg
from bt_utils.embed_templates import SuccessEmbed, WarningEmbed
from bt_utils.handle_sqlite import DatabaseHandler
SHL = Console('BundestagsBot Reload')
DB = DatabaseHandler()

settings = {
    'name': 'reload',
    'channels': ['team'],
    'mod_cmd': True
}


async def main(client, message, params):
    files_failed = cfg.reload(debug=True)
    if files_failed == 0:
        embed = SuccessEmbed('Success', 'All files reloaded')
    else:
        embed = WarningEmbed('Reloading failed', f'Failed to reload {files_failed} file(s)')

    roles = cfg.options["roles_stats"].values()

    # creates basic table structures if not already present
    DB.create_structure(roles)

    # updates table structure, e.g. if a new role has been added
    DB.update_columns(roles)

    await message.channel.send(embed=embed)
