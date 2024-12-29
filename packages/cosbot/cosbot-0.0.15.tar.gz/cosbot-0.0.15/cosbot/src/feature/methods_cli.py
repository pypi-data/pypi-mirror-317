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
from cosbot.src.base.cli_exec import aurora_cli_exec, cosbot_exec


class MethodsCli:
    @staticmethod
    def psdk_installed(bws, _):
        result = aurora_cli_exec('/psdk/installed')
        if bws:
            bws.send(fun=MethodsCli.psdk_installed, value=result)
        return result

    @staticmethod
    def psdk_available(bws, _):
        result = aurora_cli_exec('/psdk/available')
        if bws:
            bws.send(fun=MethodsCli.psdk_available, value=result)
        return result

    # @todo query to cosbot
    @staticmethod
    def app_info(bws, _):
        result = cosbot_exec('--version')
        if bws:
            bws.send(fun=MethodsCli.app_info, value=result)
        return result

    @staticmethod
    def emulator_start(bws, _):
        result = aurora_cli_exec('/emulator/start')
        if bws:
            bws.send(fun=MethodsCli.emulator_start, value=result)
        return result
