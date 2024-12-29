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

from cosbot.src.base.dataset import ds_clear_dataset
from cosbot.src.rest.bot_rest_api import BotRestApi


def rest_get_user_info(api: BotRestApi):
    return api.query('/user/info')


def rest_aurora_dataset_command(api: BotRestApi, search: str):
    return api.query('/cli-dataset/command/{}'.format(search))


def rest_aurora_dataset_search(api: BotRestApi, search: str):
    result = api.query('/aurora-dataset/search/{}'.format(search))
    return ds_clear_dataset(result)


def rest_aurora_dataset_get(api: BotRestApi, md5_hash):
    result = api.query('/aurora-dataset/get/{}'.format(md5_hash))
    return ds_clear_dataset(result)
