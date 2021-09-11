from utils import content_callback, dictify
from dotenv import dotenv_values
from os import path
import sys

ROOT_DIR = path.abspath(path.join(path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
env = {**dotenv_values('test.env')}  # Must be changed to 'config.env' for production mode

VIEWS_DIR = path.abspath(path.join(ROOT_DIR, env.get('VIEWS_DIR', 'views')))
PRODUCTS_DIR = path.abspath(
    path.join(ROOT_DIR, env.get('PRODUCTS_DIR', 'products')))

view = content_callback(VIEWS_DIR)

TOKEN = env.get('TOKEN', '').strip()
ADMINS = [int(i) for i in env.get('ADMINS', '').strip().split(',')]
PRODUCTS = dictify(PRODUCTS_DIR)
VIEWS = {
    'START': view('start'),
    'START_ADMIN': view('start_admin'),
    'MENU': view('menu'),
    'SENT_ADMIN': view('sent_admin'),
    'SENT': view('sent'),
    'NO_PRODUCT': view('no_product'),
    'NO_COMMAND': view('no_command')
}
