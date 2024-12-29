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
import json
from typing import Callable

import websocket

from cosbot.src.base.click import print_click
from cosbot.src.texts.texts_error import TextsError
from cosbot.src.websocket.bot_received import BotReceived
from cosbot.src.feature.methods import Methods


class BotWebsocket:
    """Websocket"""
    # @todo debug
    # _route = 'ws://0.0.0.0:3024/api/connect'
    _route = 'wss://aurora-bot.keygenqt.com/api/connect'

    def __init__(self, cookie, connect: Callable[[], None]):
        self.ws = websocket.WebSocketApp(self._route,
                                         cookie=cookie,
                                         on_message=self._message,
                                         on_error=self._error,
                                         on_open=self._open)
        connect()
        self.ws.run_forever(reconnect=5)

    def _message(self, _, message):
        try:
            data = json.loads(message)
            Methods[data['code']].value[0](self, data)
        except (Exception,):
            print_click(TextsError.error_message_from_server())

    def _open(self, _):
        self.ws.send(BotReceived(Methods.CONNECTION).to_message())

    def _error(self, _, error):
        raise Exception(error)

    def send(self, fun, value: json):
        for item in enumerate(Methods):
            if item[1].value[0] == fun:
                self.ws.send(BotReceived(code=item[1], value=value).to_message())
                break
