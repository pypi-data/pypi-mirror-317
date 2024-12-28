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

from cosbot.src.feature.methods_app import MethodsApp
from cosbot.src.feature.methods_cli import MethodsCli


class Methods(Enum):
    # App
    CONNECTION = MethodsApp.connections,
    # CLI
    PSDK_INSTALLED = MethodsCli.psdk_installed,
    PSDK_AVAILABLE = MethodsCli.psdk_available,
    APP_INFO = MethodsCli.app_info,
    EMULATOR_START = MethodsCli.emulator_start,
