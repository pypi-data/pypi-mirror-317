from telebot import TeleBot
from telebot_dialogue import Dialogue, DialogueManager

# Инициализация бота
bot = TeleBot("TOKEN")

# Инициализация менеджера диалогов
dialogue_manager = DialogueManager()

# Обработчик сообщений для диалога
def dialogue_handler(message, dialogue):
    bot.send_message(dialogue.user_id, f"Вы сказали: {message.text} и вы {dialogue.get_context('username', 'незнакомец')}!")

# Команда для начала диалога
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    dialogue = Dialogue(user_id, dialogue_handler)
    dialogue.update_context("username", message.from_user.username)
    dialogue_manager.add_dialogue(dialogue)
    bot.reply_to(message, "Диалог начат! Напишите что-нибудь.")


@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    dialogue_manager.stop_dialogue(user_id)
    bot.reply_to(message, "Диалог остановлен.")


# Обработчик всех сообщений
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    dialogue_manager.handle_message(message)



# Запуск бота
bot.polling()