from bt_utils.console import Console
from bt_utils.config import cfg
from bt_utils.embed_templates import SuccessEmbed, WarningEmbed
SHL = Console('BundestagsBot Reload')

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
    await message.channel.send(embed=embed)
