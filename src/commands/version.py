import subprocess

from bt_utils.console import Console, blue2, white, red, yellow
from bt_utils.embed_templates import InfoEmbed, ErrorEmbed


SHL = Console("BundestagsBot Version")

settings = {
    'name': 'version',
    'channels': ['dm', 'bot'],
}

try:
    git_version_short_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    git_version_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
    git_remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url']).decode('ascii').strip().replace(".git", "")

    if git_remote_url.startswith("git@"):
        __git_remote_host = git_remote_url[4:git_remote_url.index(":")]
        __git_remote_repo = git_remote_url[git_remote_url.index(":")+1:]
        git_remote_url = "https://" + __git_remote_host + "/" + __git_remote_repo

        SHL.output(f"{blue2}Found local version: {git_version_short_hash}, Git over SSH{white}")

        __generated_link = git_remote_url + "/commits/" + git_version_hash
        __msg = f"Current Version is <a target=\"_blank\" rel=\"noopener noreferrer\" href=\"{__generated_link}\">{git_version_short_hash}</a>.<br />"

    elif git_remote_url.startswith("https://"):
        git_remote_url.replace(".git", "")

        SHL.output(f"{blue2}Found local version: {git_version_short_hash}, Git over HTTPS{white}")

        __generated_link = git_remote_url + "/commits/" + git_version_hash
        __msg = f"Current Version is <a target=\"_blank\" rel=\"noopener noreferrer\" href=\"{__generated_link}\">{git_version_short_hash}</a>.<br />"

    else:
        SHL.output(f"{red}Git remote URL could not be parsed, gitversion cannot link to the repo.{white}")

        SHL.output(f"{yellow}Found local version: {git_version_short_hash}, Git remote not found{white}")

        __msg = f"Current Version is {git_version_short_hash}.<br /> " \
                f"<a class=\"text-danger\">Error getting remote URL, cannot link to repo. Server owner messed up.</a>"


except subprocess.CalledProcessError:
    SHL.output(f"{red}Error getting git version{white}")
except UnicodeDecodeError:
    SHL.output(f"{red}Error parsing git version{white}")


async def main(client, message, params):
    if __msg is not None:
        embed = InfoEmbed(title="Version", description=__msg)
    else:
        embed = ErrorEmbed(title="Version", description="Error fetching version.")
    await message.channel.send(embed=embed)

