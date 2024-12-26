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
import argparse
import hashlib
import signal

from aurora_bot.src.base.bot_connect import connect
from aurora_bot.src.base.bot_rest_api import BotRestApi
from aurora_bot.src.base.utils import close_app

if __name__ == '__main__':

    # init close
    signal.signal(signal.SIGINT, close_app)
    # init parser
    parser = argparse.ArgumentParser(
        prog='aurora-bot',
        add_help=False,
        description='Aurora Bot, интерфейс командной строки.',
    )
    parser.add_argument(
        '--connect',
        action='store_true',
        help='Подключитесь к серверу Aurora Bot для работы режима "/command".',
    )
    parser.add_argument(
        '--token',
        metavar='',
        help='Авторизация с помощью токена.',
    )
    parser.add_argument(
        '--search',
        metavar='',
        help='Поиск данных в Aurora Dataset.',
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help="Показать версию приложения и выйти.",
    )
    parser.add_argument(
        '--help',
        action='store_true',
        help="Показать справочное сообщение и выйти.",
    )

    args = parser.parse_args()
    if not [arg for arg in args.__dict__ if args.__dict__[arg]]:
        parser.print_help()
        exit(0)

    try:
        if args.search:
            api = BotRestApi(args.token)
            result = api.aurora_dataset_search(args.search)
            print(result)
            if '1. ' in result:
                print('=========================')
                index = input("Введите индекс ответа: ")
                title = [line.replace('{}. '.format(index), '') for line in result.split('\n') if '{}. '.format(index) in line]
                if title:
                    hash_title = hashlib.md5(title[0].encode("utf")).hexdigest()
                    print('=========================')
                    print(api.aurora_dataset_get(hash_title))
                else:
                    print("Не удалось получить ответ.")
            exit(0)
    except (Exception,):
        print('Отсутствует подключение.')

    if args.help:
        parser.print_help()
    elif args.version:
        print('aurora-bot 0.0.1')
    elif args.connect:
        connect(args.token)