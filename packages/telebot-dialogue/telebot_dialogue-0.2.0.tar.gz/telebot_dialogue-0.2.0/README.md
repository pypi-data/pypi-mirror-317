# telebot-dialogue

`telebot-dialogue` — это библиотека для упрощения управления диалогами в Telegram-ботах на основе [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI). Она предоставляет удобные классы для обработки сообщений, управления состояниями пользователей и работы с контекстом.

## Возможности

- Простое создание и управление диалогами.
- Хранение и обновление контекста для каждого пользователя.
- Лёгкая настройка и расширяемость.

## Установка

Установите библиотеку с помощью pip:

```bash
pip install telebot-dialogue
```

## Использование

### Быстрый старт

```python
from telebot import TeleBot
from telebot_dialogue import Dialogue, DialogueManager

# Инициализация бота
bot = TeleBot('YOUR_BOT_TOKEN')

# Инициализация менеджера диалогов
dialogue_manager = DialogueManager()

# Обработчик сообщений для диалога
def dialogue_handler(message, dialogue):
    bot.reply_to(message, f"Вы сказали: {message.text}")

# Команда для начала диалога
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    dialogue = Dialogue(user_id, dialogue_handler)
    dialogue_manager.add_dialogue(dialogue)
    bot.reply_to(message, "Диалог начат! Напишите что-нибудь.")

# Обработчик всех сообщений
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    dialogue_manager.handle_message(message)

# Запуск бота
bot.polling()
```

### Основные классы

#### `Dialogue`

Класс для представления диалога с пользователем.

- **Параметры:**

  - `user_id` — идентификатор пользователя.
  - `handler` — функция-обработчик сообщений.
  - `context` — словарь для хранения пользовательского контекста (опционально).

- **Методы:**

  - `stop_dialogue()` — завершает диалог.
  - `continue_dialogue()` — возобновляет диалог.
  - `update_context(key, value)` — добавляет или обновляет данные контекста.
  - `get_context(key, default=None)` — получает данные из контекста.
  - `init_handler(message)` — вызывает обработчик сообщения с передачей контекста.

#### `DialogueManager`

Класс для управления диалогами.

- **Методы:**
  - `add_dialogue(dialogue)` — добавляет новый диалог.
  - `stop_dialogue(user_id)` — завершает диалог для пользователя.
  - `handle_message(message)` — передаёт сообщение соответствующему диалогу.
  - `find_dialogue(user_id)` — находит диалог для пользователя.
  - `continue_dialogue(user_id)` — возобновляет диалог для пользователя.
  - `finish_dialogue(user_id)` — завершает и удаляет диалог для пользователя.

## Требования

- Python 3.7+

## Лицензия

Этот проект распространяется под лицензией MIT. Подробнее в файле [LICENSE](LICENSE).

## Контакты

tiver@tiver211.ru
