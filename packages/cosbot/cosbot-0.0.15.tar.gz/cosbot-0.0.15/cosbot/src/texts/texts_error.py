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

from enum import Enum

import click


class TextsError(Enum):
    @staticmethod
    def error_connect_arg():
        return click.style('Недопустимые аргументы.', fg='red')

    @staticmethod
    def error_empty_arg():
        return click.style('Нужно указать что вы хотите найти.', fg='yellow')

    @staticmethod
    def error_max_prompt():
        return click.style('Неверно указан индекс.', fg='red')

    @staticmethod
    def error_min_prompt():
        return click.style('Неверно указан индекс.', fg='red')

    @staticmethod
    def error_connect():
        return click.style('Отсутствует подключение.', fg='red')

    @staticmethod
    def error_reconnect():
        return click.style('Ошибка соединения, переподключение ({}s)...', fg='yellow')

    @staticmethod
    def error_auth():
        return click.style('Не удалось подключиться. Возможно токен устарел: он одноразовый и работает 5 минут.',
                           fg='red')

    @staticmethod
    def error_message_from_server():
        return click.style('Не удалось прочитать входящие сообщение.', fg='red')
