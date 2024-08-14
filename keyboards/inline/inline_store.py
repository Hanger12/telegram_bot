from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_button_stores(name_stores: list, stores: list) -> [str, InlineKeyboardMarkup]:
    """Метод отображающий инлайн клавиатуру со ссылками на магазины игр"""
    keyboard_inline = InlineKeyboardMarkup()
    if name_stores is not None:
        for name_store in name_stores:
            for store in stores:
                if name_store['store']['id'] == store['store_id']:
                    button = InlineKeyboardButton(text=name_store['store']['name'], url=store['url'])
                    keyboard_inline.add(button, row_width=2)
        return keyboard_inline
    else:
        return None
