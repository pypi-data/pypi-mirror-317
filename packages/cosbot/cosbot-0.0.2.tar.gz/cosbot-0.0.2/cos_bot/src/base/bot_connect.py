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
import time

from cos_bot.src.base.bot_connect_exceptions import BotWSConnectException, BotApiConnectException
from cos_bot.src.base.bot_reconnect import get_reconnect, clear_reconnect
from cos_bot.src.base.bot_rest_api import BotRestApi
from cos_bot.src.base.bot_websocket import BotWebsocket
from cos_bot.src.base.utils import is_app_close


def connect_sleep():
    rec = get_reconnect()
    # limit connects
    if rec >= 60:
        print('Отсутствует подключение.')
        exit(1)
    print('> Ошибка соединения, переподключение ({}s)...'.format(rec))
    time.sleep(rec)


def connect(token: str):
    try:
        BotWebsocket(BotRestApi(token).get_cookies(), lambda: clear_reconnect())
    except BotWSConnectException:
        connect_sleep()
        connect(token)
    except BotApiConnectException:
        connect_sleep()
        connect(token)
    except (Exception,):
        print('Отсутствует подключение.')
        exit(1)

    # reconnect if close
    if not is_app_close:
        connect(token)
