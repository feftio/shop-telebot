from utils import _, get_token, get_admins

# Configuration
TOKEN = get_token('secret/token')
ADMINS = get_admins('secret/admins')
PRODUCTS = {
    'Брюки': _('views/products/брюки'),
    'Рубашки': _('views/products/рубашки'),
    'Галстуки': _('views/products/рубашки')
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
