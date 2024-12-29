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

from cosbot.src.app.app import is_app_close
from cosbot.src.base.click import print_click
from cosbot.src.base.exceptions import BotWSConnectException, BotApiConnectException
from cosbot.src.rest.bot_rest_api import BotRestApi
from cosbot.src.texts.texts_error import TextsError
from cosbot.src.websocket.bot_reconnect import get_reconnect, clear_reconnect
from cosbot.src.websocket.bot_websocket import BotWebsocket


def connect_sleep():
    rec = get_reconnect()
    # limit connects
    if rec >= 60:
        print_click(TextsError.error_connect())
        exit(1)
    print_click(TextsError.error_reconnect().format(rec))
    time.sleep(rec)


def app_connect(token: str):
    try:
        BotWebsocket(BotRestApi(token).get_cookies(), lambda: clear_reconnect())
    except BotWSConnectException:
        connect_sleep()
        app_connect(token)
    except BotApiConnectException:
        connect_sleep()
        app_connect(token)
    except (Exception,):
        print_click(TextsError.error_connect())
        exit(1)

    # reconnect if close
    if not is_app_close:
        app_connect(token)
