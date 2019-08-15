from bt_utils.config import cfg


async def check_message(client, message):
    if cfg.options["bot_api_check"]:
        if message.channel.id == cfg.options["bot_api_channel"]:  # To check if bot is still running (needed for API)
            await message.delete()

    if message.author == client.user:
        return False

    if cfg.options["use_blacklist"]:
        if str(message.author.id) in cfg.options["blacklist"]:
            return False

    if len(str(message.content)) > 1999:
        return False

    return True
