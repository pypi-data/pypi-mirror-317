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
import pickle
import time
from pathlib import Path

import requests

from cosbot.src.base.click import print_click
from cosbot.src.base.exceptions import BotApiConnectException
from cosbot.src.texts.texts import Texts
from cosbot.src.texts.texts_error import TextsError


class BotRestApi:
    """Connect API"""
    # @todo debug
    # _route = 'http://0.0.0.0:3024/api'
    _route = 'https://aurora-bot.keygenqt.com/api'
    _session = requests.Session()
    _path_session = Path(Path.home() / '.cosbot.session')
    _deeplink = None
    _uuid = None
    _ping_count = 0

    def __init__(self, token: str):
        if not self.auth(token):
            raise Exception('Отсутствует подключение.')

    def query(self, path: str):
        result = self._session.get('{}{}'.format(self._route, path), timeout=5)
        if result.status_code == 200:
            try:
                return result.json()
            except (Exception,):
                return result.text
        else:
            return None

    def get_cookies(self):
        return "; ".join(["%s=%s" % (i, j) for i, j in self._session.cookies.get_dict().items()])

    def auth(self, token: str):
        try:
            if self._path_session.exists():
                with open(self._path_session, 'rb') as f:
                    self._session.cookies.update(pickle.load(f))
                result = self._session.get('{}{}'.format(self._route, '/user/info'), timeout=5)
                if result.status_code == 200:
                    return True
                else:
                    raise Exception('Необходима авторизация.')
            else:
                raise Exception('Необходима авторизация.')
        except (requests.exceptions.ConnectionError,):
            raise BotApiConnectException('Error connection.')
        except (Exception,):
            try:
                if token:
                    self._uuid = token
                    return self.ping_auth()
                else:
                    result = self._session.get('{}{}'.format(self._route, '/auth/deeplink'), timeout=5)
                    if result.status_code == 200:
                        self._deeplink = result.json()['message']
                        self._uuid = self._deeplink.split('=')[-1]
                        print_click(Texts.auth_deeplink().format(link=self._deeplink))
                        return self.ping_auth()
                    else:
                        return False
            except (Exception,):
                return False

    def ping_auth(self):
        time.sleep(1)
        result = self.query('/auth/token/{}'.format(self._uuid))
        if not result:
            self._ping_count += 1
            if self._ping_count > 60:
                print_click(TextsError.error_auth())
                exit(1)
            return self.ping_auth()
        else:
            with open(self._path_session, 'wb') as f:
                pickle.dump(self._session.cookies, f)
            return True
