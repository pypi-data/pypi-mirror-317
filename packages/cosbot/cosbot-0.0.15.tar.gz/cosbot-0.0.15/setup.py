import setuptools

long_description = """
![picture](https://drive.usercontent.google.com/download?id=1Hdcut9JaEAY4pV_YT9RWFHyBMcoW0ZZs)

**Cosbot** - клиент сервиса [Aurora Bot](https://aurora-bot.keygenqt.com/), приложение реализует умную командую строку для работы с Aurora CLI.
Отвечает на ваши вопросы из открытого проекта Aurora Dataset.

*Основной интерфейс приложения умный, просто скажи ему что делать!*

### Feature

- Соединение с сервером для режима команд Telegram.
- Отвечает на вопросы по ОС Аврора.
- Режим умных команд.
"""

setuptools.setup(
    name='cosbot',
    version='0.0.15',
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
        'click>=8.1.7',
    ],
    python_requires='>=3.8.10',
    entry_points="""
        [console_scripts]
        cosbot = cosbot.__main__:main
    """
)
