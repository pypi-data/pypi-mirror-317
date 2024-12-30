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


def localization(text: str):
    text = text.strip()
    text = ru_click_help(text)
    text = ru_click_usage_error(text)
    return text


def ru_click_help(text: str) -> str:
    return (text
            .replace('required', 'обязательно')
            .replace('default', 'по умолчанию')
            .replace('Usage:', 'Применение:')
            .replace('Options:', 'Параметры:')
            .replace('Commands:', 'Команды:'))


def ru_click_usage_error(text: str) -> str:
    return (text
            .replace('Usage:', 'Применение:')
            .replace('Try', 'Попробуй')
            .replace('for help', 'для помощи')
            .replace('Error: No such option', 'Ошибка: Нет такой опции')
            .replace('Error: Missing option', 'Ошибка: отсутствует опция')
            .replace('Error: Missing option', 'Ошибка: отсутствует опция')
            .replace('Choose from:', 'Выбери из:'))
