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
import subprocess

from cosbot.src.base.argv import argv_is_verbose
from cosbot.src.base.click import print_click
from cosbot.src.texts.texts import Texts


def aurora_cli_exec(route: str):
    return cli_exec(['aurora-cli', 'api', '--route', route])


def cosbot_exec(value: str):
    return cli_exec(['cosbot', value])


def cli_exec(arg: []):
    if argv_is_verbose():
        print_click(Texts.hint_italic().format(' '.join(arg)))
    try:
        result = subprocess.run(
            arg,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        try:
            return json.loads(result.stdout.decode())
        except (Exception,):
            return result.stdout.decode()
    except (Exception,):
        return None
