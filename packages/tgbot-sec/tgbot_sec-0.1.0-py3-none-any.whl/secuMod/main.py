# Security library for Telegram bot

This
library
provides
security
features
for Telegram bots, including user authentication, registration, and spam protection.It is designed to simplify the integration of security mechanisms into your Python projects using the pyTelegramBotAPI library.

## Description

The
library
includes
the
following
modules:

- ** Authentication **: Allows
users
to
log in securely
using
their
phone
numbers.
- ** Registration **: Provides
the
registration
process
for new users.
    - ** Antispam **: Protects
    the
    bot
    from spam and abuse.

## Installation

### Preliminary requirements

- Python
3.7 or higher
- Python
library - telegram - bot
- Cryptography
Library

### Installation via pip

You
can
install
the
library
using
pip.To
do
this, run
the
following
command:

bash
pip
install
securityMod

### Installation from source

If
you
want
to
install
the
library
from source, follow

these
steps:

1.
Clone
the
repository

cd
securityMod

2.
Install
the
library

pip
install.

## Usage

### Importing a library

python
from tgbot_security.main import SecurityModule

### Usage example

import telebot
from datetime import datetime
import pytz
from telebot import types
from securityMod import SecurityModule

sec = SecurityModule()

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
API_TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения состояний пользователей
user_states = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 'Привет! Чтобы начать пользоваться ботом, пройдите регистрацию.\nВведите свой номер телефона в формате: 71231231234')
    user_states[message.chat.id] = 'waiting_for_phone'


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_phone')
def handle_text(message):
    phone_number = message.text.strip()
    user_id = message.from_user.id

    if not sec.is_valid_phone(phone_number):
        bot.send_message(message.chat.id, "Номер телефона введен неверно. Попробуйте снова!")
        return

    # Проверяем, зарегистрирован ли номер и кто его владелец
    registered_user_id = sec.get_user_id_by_phone(phone_number)

    if sec.register_user(phone_number) or (registered_user_id == user_id):
        bot.send_message(message.chat.id, "Вы успешно прошли регистрацию!")
        bot.reply_to(message,
                     "Выберите название страны, время которой хотите узнать:\nРоссия, США, Канада, Австралия, Германия, Франция, Италия, Япония, Корея, Казахстан, Турция.")
        user_states[message.chat.id] = 'waiting_for_country'
        sec.log_user_action(user_id)
    else:
        bot.reply_to(message, "Ошибка регистрации. Попробуйте снова.")

        # Проверка на спам после регистрации
    if sec.is_spam(user_id):
        bot.send_message(message.chat.id, "Вы отправляете сообщения слишком быстро! Пожалуйста, подождите.")


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_country')
def send_time(message):
    ...  # остальной код


# Запускаем бота
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"An error occurred: {e}")

## License

This
project is licensed
under
the
MIT
License - see
the[LICENSE](LICENSE)
file
for details.

## Contacts

If
you
have
any
questions or suggestions, you
can
contact
us
by
email: kvostrecova0207 @ mail.ru.