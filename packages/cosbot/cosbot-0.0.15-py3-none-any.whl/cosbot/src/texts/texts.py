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


class Texts(Enum):
    @staticmethod
    def app_about():
        return (f'{click.style('Cosbot', fg='blue')} - '
                'клиент сервиса Aurora Bot, приложение реализует умную командую строку для работы с Aurora CLI. '
                'Отвечает на ваши вопросы из открытого проекта Aurora Dataset.'
                '\n\n'
                f'{click.style('Основной интерфейс приложения умный, просто скажи ему что делать!', italic=True)}')

    @staticmethod
    def option_search():
        return 'Поиск данных в Aurora Dataset.'

    @staticmethod
    def option_verbose():
        return 'Вывод с дополнительной информацией.'

    @staticmethod
    def option_command():
        return 'Подключитесь к Aurora Bot для работы режима "/command".'

    @staticmethod
    def option_token():
        return 'Авторизация с помощью токена.'

    @staticmethod
    def option_version():
        return 'Вывести версию приложения.'

    @staticmethod
    def option_help():
        return 'Вывести основные команды приложения.'

    @staticmethod
    def hint_italic():
        return click.style('> {}', italic=True)

    @staticmethod
    def connect_success():
        return click.style('> {message}', fg="green")

    @staticmethod
    def auth_deeplink():
        return click.style('Перейдите по ссылке для авторизации: ', fg="blue") + '{link}'
