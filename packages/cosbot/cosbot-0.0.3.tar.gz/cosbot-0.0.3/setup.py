import setuptools

long_description = """
**Cosbot** предназначено для взаимодействия с [Aurora Bot](https://aurora-bot.keygenqt.com/).

> Приложение в разработке!

### Feature

- Позволяет реализовать в Telegram режим команд.
- Отвечать на вопросы.

### Roadmap

- Режим умных команд.
- Фреймворк click.
- Другие улучшения.
"""

setuptools.setup(
    name='cosbot',
    version='0.0.3',
    author='Vitaliy Zarubin',
    author_email='keygenqt@gmail.com',
    description='An application that simplifies the life of an application developer for the Aurora OS.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://aurora-bot.keygenqt.com/",
    packages=setuptools.find_packages(exclude=['*tests.*', '*tests']),
    include_package_data=True,
    py_modules=['colors'],
    install_requires=[
        'Telethon>=1.38.1',
        'setuptools>=75.6.0',
        'websocket-client>=1.8.0',
        'requests>=2.32.3',
        'aurora-cli>=3.2.10',
        'beautifulsoup4>=4.12.3',
    ],
    python_requires='>=3.8.10',
    entry_points="""
        [console_scripts]
        cosbot = cos_bot.__main__:main
    """
)
