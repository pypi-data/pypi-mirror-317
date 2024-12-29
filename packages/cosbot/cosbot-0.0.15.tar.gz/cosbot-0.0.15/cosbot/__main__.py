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

from cosbot.src.app.app import app_close, APP_VERSION, APP_NAME
from cosbot.src.app.app_command import app_command
from cosbot.src.app.app_connect import app_connect
from cosbot.src.app.app_search import app_search
from cosbot.src.base.click import print_click
from cosbot.src.rest.bot_rest_api import BotRestApi
from cosbot.src.texts.localization import localization
from cosbot.src.texts.texts import Texts
from cosbot.src.texts.texts_error import TextsError

# abort handler
signal.signal(signal.SIGINT, app_close)


@click.group(invoke_without_command=True, help=Texts.app_about())
@click.pass_context
@click.option('-s', is_flag=True, help=Texts.option_search(), default=False)
@click.option('-v', is_flag=True, help=Texts.option_verbose(), default=False)
@click.option('--connect', is_flag=True, help=Texts.option_command(), default=False)
@click.option('--token', help=Texts.option_token(), type=click.STRING, default=None)
@click.option('--version', is_flag=True, help=Texts.option_version(), default=False)
@click.option('--help', 'help_', is_flag=True, help=Texts.option_help(), default=False)
@click.argument('command', nargs=-1)
def main(ctx, s, v, connect, token, version, help_, command):
    # show version app
    if version:
        print_click('{}, версия {}'.format(APP_NAME, APP_VERSION))
        exit(0)
    # show help query
    if help_:
        print_click(localization(ctx.get_help()))
        exit(0)
    # connect to server
    if connect:
        if s or command:
            print_click(TextsError.error_connect_arg())
            exit(1)
        app_connect(token)
        exit(0)
    # search by Aurora Dataset
    if s:
        if not command:
            print_click(TextsError.error_empty_arg())
            exit(1)
        app_search(' '.join(command), BotRestApi(token))
        exit(0)
    # Fee AI command
    if command:
        app_command(' '.join(command), BotRestApi(token))
        exit(0)

    print_click(localization(ctx.get_help()))


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(ex)
