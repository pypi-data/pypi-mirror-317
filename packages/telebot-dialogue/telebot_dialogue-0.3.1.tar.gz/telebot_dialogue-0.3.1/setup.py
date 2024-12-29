from setuptools import setup, find_packages

setup(
    name="telebot_dialogue",  # Имя пакета на PyPI
    version="0.3.1",    # Версия
    author="tiver211",
    author_email="tiver@tiver211.ru",
    description="Library for managing Telegram dialogues using pyTelegramBotAPI.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tiver211/telebot-dialogue",  # Ссылка на репозиторий
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Минимальная версия Python
)