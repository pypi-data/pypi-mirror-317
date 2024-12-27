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

from cosbot.src.texts.texts_error import TextsError
from cosbot.src.texts.texts_prompt import TextsPrompt


def click_prompt_int(text, max_size: int):
    index = click.prompt(TextsPrompt.search(), type=int)
    if index <= 0:
        print_click(TextsError.error_min_prompt())
        return click_prompt_int(text, max_size)
    if index > max_size:
        print_click(TextsError.error_max_prompt())
        return click_prompt_int(text, max_size)
    return index


def print_click(message: str):
    click.echo(message)
