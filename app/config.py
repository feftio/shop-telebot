from utils import _, get_token, get_admins
from os import environ as env, path
import sys

sys.append(path.abspath(path.join(path.dirname(__file__), '..')))

TOKEN =  get_token(env.get('TOKEN', ''))
ADMINS = get_admins(env.get('ADMINS', ''))
PRODUCTS = {
    'Брюки': _('views/products/брюки'),
    'Рубашки': _('views/products/рубашки')
}
VIEWS = {
    'START': _('views/start'),
    'START_ADMIN': _('views/start_admin'),
    'MENU': _('views/menu'),
    'SENT_ADMIN': _('views/sent_admin'),
    'SENT': _('views/sent'),
    'NO_PRODUCT': _('views/no_product'),
    'NO_COMMAND': _('views/no_command')
}
