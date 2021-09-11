from __future__ import annotations
import types as t
import telebot
from telebot import apihelper
from telebot import types
import config
from utils import Event


ADMINS: t.List[int] = config.ADMINS
TOKEN: str = config.TOKEN
PRODUCTS: t.Dict[str, str] = config.PRODUCTS
VIEWS: t.Dict[str, str] = config.VIEWS
PRODUCT_NAMES: t.List[str] = list(PRODUCTS.keys())
PRODUCT_DESCRIPTIONS: t.List[str] = list(PRODUCTS.values())
PRODUCT_COUNT: int = len(PRODUCT_NAMES)


apihelper.ENABLE_MIDDLEWARE = True
bot: telebot.TeleBot = telebot.TeleBot(token=TOKEN, parse_mode='HTML')


def buy_button(product_index: int):
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(
        text="Купить",
        callback_data=Event.dumps('buy', product_index)))


@bot.middleware_handler(update_types=['message'])
def modify_message(bot_instance, message: types.Message):
    if message.chat.id in ADMINS:
        message.is_admin = True
    else:
        message.is_admin = False


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call: types.CallbackQuery):
    event = Event.loads(call.data)
    if event.name == 'buy':
        for admin in ADMINS:
            bot.send_message(chat_id=admin, text=VIEWS['SENT_ADMIN'].format(
                user_id=call.from_user.id,
                user_name=call.from_user.full_name,
                product_name=PRODUCT_NAMES[event.data]))
        return bot.send_message(
            chat_id=call.from_user.id,
            text=VIEWS['SENT'])
    if event.name == 'description':
        return bot.send_message(
            chat_id=call.from_user.id,
            text=PRODUCT_DESCRIPTIONS[event.data],
            reply_markup=buy_button(event.data) if not (call.from_user.id in ADMINS) else None)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    for product_name in PRODUCT_NAMES:
        keyboard.add(product_name)
    if message.is_admin:
        return bot.send_message(
            chat_id=message.chat.id,
            text=VIEWS['START_ADMIN'],
            reply_markup=keyboard)
    bot.send_message(
        chat_id=message.chat.id,
        text=VIEWS['START'],
        reply_markup=keyboard)


@bot.message_handler(commands=['menu'])
def show_menu(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for product_name in PRODUCT_NAMES:
        keyboard.add(types.InlineKeyboardButton(
            text=product_name,
            callback_data=Event.dumps('description', PRODUCT_NAMES.index(product_name))))
    return bot.send_message(
        chat_id=message.chat.id,
        text=VIEWS['MENU'],
        reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_product(message: types.Message):
    if message.text in PRODUCT_NAMES:
        product_name = message.text
        product_description = PRODUCTS[product_name]
        product_index = PRODUCT_NAMES.index(product_name)
        return bot.send_message(
            chat_id=message.chat.id,
            text=product_description,
            reply_markup=buy_button(product_index) if not message.is_admin else None)
    if message.text.startswith('/'):
        return bot.reply_to(
            message=message,
            text=VIEWS['NO_COMMAND'])
    return bot.reply_to(
        message=message,
        text=VIEWS['NO_PRODUCT'])


bot.polling(none_stop=True)
