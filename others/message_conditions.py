from bt_utils.config import cfg


async def check_message(client, message):
    if cfg.options.get("bot_api_check", False):
        if message.channel.id == cfg.options.get("bot_api_channel", 0):  # To check if bot is still running (needed for API)
            await message.delete()
            return False

    if message.author == client.user:
        return False

    if cfg.options.get("use_blacklist", False):
        if str(message.author.id) in cfg.options.get("blacklist", []):
            return False

    if len(str(message.content)) > cfg.options.get("message_limit", len(str(message.content))):
        return False

    return True
