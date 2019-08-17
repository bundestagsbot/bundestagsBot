from bt_utils.console import Console
from bt_utils.config import cfg
SHL = Console('BundestagsBot reload')

settings = {
    'name': 'reload',
    'channels': ['team1'],
    'mod': True
}


async def main(client, message, params):
    files_failed = cfg.reload()
    if files_failed == 0:
        await message.channel.send(content='All files reloaded')
    else:
        await message.channel.send(content=f'Failed to reload {files_failed} file(s)')