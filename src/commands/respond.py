import os.path

from discord.utils import get

from bt_utils.console import Console
from bt_utils.embed_templates import SuccessEmbed, InfoEmbed, NoticeEmbed, ErrorEmbed
from bt_utils.config import cfg
from bt_utils import handleJson
from bt_utils.get_content import content_dir

SHL = Console("BundestagsBot Respond")

settings = {
    'name': 'respond',
    'channels': ['team'],
    'mod_cmd': True
}

path = os.path.join(content_dir, "submits.json")


async def main(client, message, params):
    error = NoticeEmbed(title="Respond")
    success = SuccessEmbed(title="Respond")
    if len(str(message.content).split(' ')) >= 3:
        submit_id = str(message.content).split(' ')[1][1:]
        if submit_id.isdigit():
            data = handleJson.read_json_raw(path)
            if submit_id in data.keys():
                if data[submit_id]["answer"] == "":
                    embed = create_embed(submit_id, message.author.name, params)
                    msg = await message.channel.send(embed=embed)
                    await msg.add_reaction('✅')
                    await msg.add_reaction('❌')

                    def check(reaction, user):
                        e = str(reaction.emoji)
                        return user == message.author and e.startswith(('✅', '❌'))

                    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                    if str(reaction.emoji).startswith('❌'): return

                    author_id = data[submit_id]["authorID"]
                    submit_author = get(client.get_guild(531445761733296130).members, id=int(author_id))
                    try:
                        await submit_author.send(embed=embed)
                        success.description = "Antwort abgeschickt!"
                        await message.channel.send(embed=success)
                    except:  # user does not allow dm
                        error = ErrorEmbed(title="Respond", description="User does not allow direct messages.")
                        message.channel.send(embed=error)
                    data[submit_id]["answer"] = ' '.join(str(message.content).split(' ')[2:])
                    data[submit_id]["answerfrom"] = str(message.author)
                    handleJson.saveasjson(path, data)

                else:
                    error.description = f"#{submit_id} wurde schon beantwortet:"
                    error.add_field(name=data[submit_id]["answerfrom"], value=data[submit_id]["answer"])
                    await message.channel.send(embed=error)
            else:
                error.description = f"#{submit_id} could not be assigned to a submit."
                await message.channel.send(embed=error)
        else:
            error.description = f"{submit_id} is an invalid ID."
            await message.channel.send(embed=error)
    else:
        error.description = f"Invalid syntax.\nPlease use {cfg.options['invoke_mod']}respond #id text"
        await message.channel.send(embed=error)


def create_embed(submit_id, author, params):
    info = InfoEmbed(title=f"Answer Submit #{submit_id}")
    info.description = ' '.join(params[1:]).strip()
    info.set_footer(text=f'Answer by {author}')
    return info
