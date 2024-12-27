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

from cosbot.src.base.click import click_prompt_int, print_click
from cosbot.src.base.dataset import ds_get_size_dataset_variants, ds_get_title_hash
from cosbot.src.rest.bot_rest_api import BotRestApi
from cosbot.src.rest.bot_rest_api_methods import rest_aurora_dataset_search, rest_aurora_dataset_get
from cosbot.src.texts.texts_prompt import TextsPrompt


def app_search(command: str, api: BotRestApi):
    result = rest_aurora_dataset_search(api, command)
    size = ds_get_size_dataset_variants(result)
    print_click(result)
    if size:
        index = click_prompt_int(TextsPrompt.search(), size)
        title = ds_get_title_hash(index, result)
        result = rest_aurora_dataset_get(api, title)
        print_click(result)
