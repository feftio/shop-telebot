from __future__ import annotations
import types as t
import telebot
from telebot import apihelper
from telebot import types
import json
import config


admins: t.List[int] = config.ADMINS
token: str = config.TOKEN
products: t.Dict[str, str] = config.PRODUCTS
views: t.Dict[str, str] = config.VIEWS


apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(token=token, parse_mode='HTML')
product_names = list(products.keys())
product_descriptions = list(products.values())
product_count = len(product_names)


def create_event(type: str, payload: str = '') -> str:
    return json.dumps({'type': type, 'payload': payload})


@bot.middleware_handler(update_types=['message'])
def modify_message(bot_instance, message: types.Message):
    if message.chat.id in admins:
        message.is_admin = True
    else:
        message.is_admin = False


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call: types.CallbackQuery):
    event = json.loads(call.data)
    if event['type'] == 'show_menu':
        product_names_formatted = ''
        for i in range(product_count):
            product_names_formatted += f'/{i + 1} {product_names[i]}\n'
        bot.send_message(call.message.chat.id, views['MENU'].format(
            product_names=product_names_formatted))
    if event['type'] == 'buy_product':
        for admin in admins:
            bot.send_message(admin, views['SENT_ADMIN'].format(
                user_id=call.from_user.id,
                user_name=call.from_user.full_name,
                product_name=product_names[event['payload'] - 1]))
        bot.send_message(call.from_user.id, views['SENT'])


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    menu_button = types.InlineKeyboardButton(
        text='Меню', callback_data=create_event('show_menu'))
    keyboard.add(menu_button)
    if message.is_admin:
        return bot.send_message(message.chat.id, views['START_ADMIN'], reply_markup=keyboard)
    bot.send_message(message.chat.id, views['START'], reply_markup=keyboard)


@bot.message_handler(regexp='^/(?!(0))(\d+)$')
def show_product(message: types.Message):
    product_index = int(message.text[1:])
    if product_index > len(products) or product_index <= 0:
        bot.reply_to(message, views['NO_PRODUCT'])
        return
    if message.is_admin:
        bot.reply_to(message, product_descriptions[product_index - 1])
        return
    keyboard = types.InlineKeyboardMarkup()
    buy_button = types.InlineKeyboardButton(
        text='Купить', callback_data=create_event('buy_product', product_index))
    keyboard.add(buy_button)
    bot.reply_to(
        message, product_descriptions[product_index - 1], reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def no_command(message: types.Message):
    if (message.text.lower()) == 'меню':
        product_names_formatted = ''
        for i in range(product_count):
            product_names_formatted += f'/{i + 1} {product_names[i]}\n'
        return bot.send_message(message.chat.id, views['MENU'].format(
            product_names=product_names_formatted))
    bot.reply_to(message, views['NO_COMMAND'])


bot.polling()
