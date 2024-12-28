"""
Copyright 2025 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import signal

import click

from cosbot.src.app.app import app_close
from cosbot.src.app.app_command import app_command
from cosbot.src.app.app_connect import app_connect
from cosbot.src.app.app_search import app_search
from cosbot.src.rest.bot_rest_api import BotRestApi
from cosbot.src.texts.localization import localization
from cosbot.src.texts.texts import Texts
from cosbot.src.texts.texts_error import TextsError

# abort handler
signal.signal(signal.SIGINT, app_close)


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version='0.0.14', prog_name='cosbot')
@click.option('-c', '--connect', is_flag=True, help=Texts.option_command(), default=False)
@click.option('-s', '--search', is_flag=True, help=Texts.option_search(), default=False)
@click.option('-t', '--token', help=Texts.option_token(), type=click.STRING, default=None)
@click.argument('command', nargs=-1)
def main(ctx, connect, search, token, command):
    if connect:
        if search or command:
            print(TextsError.error_connect_arg())
            exit(1)
        app_connect(token)
        exit(0)

    if search:
        app_search(' '.join(command), BotRestApi(token))
        exit(0)

    if command:
        app_command(' '.join(command), BotRestApi(token))
        exit(0)

    print(localization(ctx.get_help()))


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(ex)
