import telebot as tb
from telebot.types import Message

TOKEN = '1351120944:AAEAeMPosCq5UsuqVsOVZ73J6VvwDrhKM_A'

bot = tb.TeleBot(TOKEN)


@bot.message_handler(commands=['new_project'])
def create_project(message: Message):
    msg = bot.reply_to(message, 'input a name of project')
    bot.register_next_step_handler(msg, _handle_project_name)


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
