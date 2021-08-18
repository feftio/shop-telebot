def _(name: str) -> str:
    with open(f'{name}.html', 'r', encoding='utf-8') as f:
        return ''.join(f.readlines())


# Configuration
TOKEN = ''
ADMINS = []
PRODUCTS = {
    'Брюки': _('views/products/брюки'),
    'Рубашки': _('views/products/рубашки')
}
MENU_VIEW = _('views/menu')
START_VIEW = _('views/start')
ADMIN_VIEW = _('views/admin')
SENT_VIEW = _('views/sent')
