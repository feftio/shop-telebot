from utils import view_callback
from decouple import config
from os import path
import sys

ROOT_DIR = path.abspath(path.join(path.dirname(__file__), '..'))
VIEWS_DIR = path.join(ROOT_DIR, config('VIEWS_DIR', 'views'))
PRODUCTS_DIR = path.join(VIEWS_DIR, "products")
sys.path.append(ROOT_DIR)
view = view_callback(VIEWS_DIR)

TOKEN = config('TOKEN', '').strip()
ADMINS = config('ADMINS', '').strip()
PRODUCTS = {}
VIEWS = {
    'START': view('start'),
    'START_ADMIN': view('start_admin'),
    'MENU': view('menu'),
    'SENT_ADMIN': view('sent_admin'),
    'SENT': view('sent'),
    'NO_PRODUCT': view('no_product'),
    'NO_COMMAND': view('no_command')
}
