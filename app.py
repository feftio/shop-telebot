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
menu_view: str = config.MENU_VIEW
start_view: str = config.START_VIEW
admin_view: str = config.ADMIN_VIEW
sent_view: str = config.SENT_VIEW

apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(token=token, parse_mode='HTML')
product_names = list(products.keys())
product_descriptions = list(products.values())
product_count = len(product_names)


def create_event(type: str, payload: str = '') -> str:
    return json.dumps({'type': type, 'payload': payload})


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call: types.CallbackQuery):
    event = json.loads(call.data)
    if event['type'] == 'show_menu':
        product_names_formatted = ''
        for i in range(product_count):
            product_names_formatted += f'\n/{i + 1} {product_names[i]}'
        bot.send_message(call.message.chat.id, menu_view.format(
            product_names=product_names_formatted))
    if event['type'] == 'buy_product':
        for admin in admins:
            bot.send_message(admin, admin_view.format(
                user_id=call.from_user.id,
                user_name=call.from_user.full_name,
                product_name=product_names[event['payload'] - 1]))
            bot.send_message(call.from_user.id, sent_view)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    menu_button = types.InlineKeyboardButton(
        text='Меню', callback_data=create_event('show_menu'))
    keyboard.add(menu_button)
    bot.send_message(message.chat.id, start_view, reply_markup=keyboard)


@bot.message_handler(regexp='^/(?!(0))(\d+)$')
def show_product(message: types.Message):
    product_index = int(message.text[1:])
    if product_index > len(products) or product_index <= 0:
        bot.reply_to(message, 'Данного товара не существует')
        return
    keyboard = types.InlineKeyboardMarkup()
    buy_button = types.InlineKeyboardButton(
        text='Купить', callback_data=create_event('buy_product', product_index))
    keyboard.add(buy_button)
    bot.send_message(
        message.chat.id, product_descriptions[product_index - 1], reply_markup=keyboard)


bot.polling()
