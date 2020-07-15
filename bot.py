import os
import pickle

import telebot as tb
from telebot.types import Message

import config
import db
import exceptions as ex


bot = tb.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: Message):
    pass


@bot.message_handler(commands=['new_task'])
def new_task(message: Message):
    parsed = message.text.split(maxsplit=1)
    if len(parsed) == 1:
        bot.send_message(message.chat.id, 'Write a new task...')
        bot.register_next_step_handler(message, _adding_task_next)
    elif len(parsed) == 2:
        db.insert_task(parsed[1])
        bot.send_message(message.chat.id,
                         'Great, your task is written!')
    else:
        raise ex.ParseError()


def _adding_task_next(message: Message):
    db.insert_task(message.text)
    bot.send_message(message.chat.id,
                     'Great, your task is written!')


@bot.message_handler(commands=['list'])
def list_(message: Message):
    if not db.TASK_LIST:
        bot.send_message(message.chat.id, 'Your list is empty :(')
    else:
        msg = 'Your task list:'
        for i, task in enumerate(db.TASK_LIST):
            msg += f'\n{i+1}. {task}'
        bot.send_message(message.chat.id, msg)


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
    if 'list' in os.listdir(path='.'):
        with open('list', 'rb') as tasklist:
            db.TASK_LIST = pickle.load(tasklist)
    bot.polling(timeout=40)
