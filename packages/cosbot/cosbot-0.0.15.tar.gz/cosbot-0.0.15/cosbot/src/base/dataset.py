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
import hashlib
import re

import click


def ds_clear_dataset(text: str):
    # clear html
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = text.replace("\n⌫\n", "\n")
    text = text.replace(">⌫\n", ">")
    text = text.replace("⌫\n", " ")
    text = re.sub(r'\n{2,}', '\n', text)
    # colorize
    lines = text.split('\n')
    lines[0] = click.style(lines[0], fg='cyan')
    if '🔖' in text:
        lines[-1] = click.style(lines[-1], italic=True)
    return '\n'.join(lines)


def ds_get_size_dataset_variants(text: str):
    if '📚' in text:
        return len(text.split('\n')) - 1
    return 0


def ds_get_title_hash(index: int, text: str):
    title = [line.replace('{}. '.format(index), '') for line in text.split('\n') if '{}. '.format(index) in line]
    if title:
        return hashlib.md5(title[0].encode("utf")).hexdigest()
    return None
