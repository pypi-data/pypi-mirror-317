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
import click

from cosbot.src.base.click import print_click
from cosbot.src.feature.methods import Methods
from cosbot.src.rest.bot_rest_api import BotRestApi
from cosbot.src.rest.bot_rest_api_methods import rest_aurora_dataset_command
from cosbot.src.texts.texts_error import TextsError


def app_command(command: str, api: BotRestApi):
    result = rest_aurora_dataset_command(api, command)
    try:
        result = Methods[result['code']].value[0](None, result)
        # result output
        if isinstance(result, str):
            print_click(result.strip())
        else:
            if result['code'] == 500:
                print_click(click.style(result['message'], fg='red'))
            elif result['code'] == 100:
                print_click(click.style(result['message'], fg='yellow'))
            else:
                print_click(click.style(result['message'], fg='green'))
    except (Exception,):
        print_click(TextsError.error_message_from_server())
