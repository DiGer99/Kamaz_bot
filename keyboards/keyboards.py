from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_RU


def create_inline_keyboard(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(
                    text=LEXICON_RU[button] if button in LEXICON_RU else button,
                    callback_data=button
                )
            )
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=button
                )
            )
    kb_builder.row(width=width, *buttons)
    return kb_builder.as_markup()


def create_reply_keyboard(width: int, *args) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    buttons = []
    if args:
        for button in args:
            buttons.append(
                KeyboardButton(
                    text=button
                )
            )
    kb_builder.row(width=width, *buttons)
    return kb_builder.as_markup(resize_keyboard=True)
