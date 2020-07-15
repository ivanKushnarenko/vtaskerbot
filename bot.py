import telebot as tb
from telebot.types import Message

import config


bot = tb.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: Message):
    pass


@bot.message_handler(commands=['new_task'])
def new_task(message: Message):
    bot.reply_to(message, message.text)


@bot.message_handler(content_types=['text'])
def handle_message(message: Message):
    if 'привет' in (text := message.text):
        bot.reply_to(message, text[::-1])
        return 
    text = f"I've got message from user #{message.from_user.id}:\n{text}\nProcessing..."
    bot.send_message(message.chat.id, text)


def _handle_project_name(message: Message):
    projectname = message.text
    bot.send_message(message.chat.id, f'New project "{projectname}" was added')


if __name__ == '__main__':
    bot.polling(timeout=40)
