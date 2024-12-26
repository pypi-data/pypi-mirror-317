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
import re

is_app_close = []


def close_app(_, __):
    is_app_close.append(True)
    print('До свидания!')
    exit(0)


def clear_dataset(text: str):
    text = text.replace("\n⌫\n", "\n")
    text = text.replace(">⌫\n", ">")
    text = text.replace("⌫\n", " ")
    text = re.sub(r'\n{2,}', '\n', text)
    return text
