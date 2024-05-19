from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from settings import config


class Keyboards:
    def __init__(self):
        self.markup = None

    def start_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('Choose_action')
        itm_btn_2 = self.set_btn('ABOUT')
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2)
        return self.markup

    def actions_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('Turkmen_invite')
        itm_btn_2 = self.set_btn('Recruitment')
        itm_btn_3 = self.set_btn('Recruitment_Minsk')
        itm_btn_4 = self.set_btn('Dismissal')
        itm_btn_5 = self.set_btn('<<')
        self.markup.row(itm_btn_1,itm_btn_2)
        self.markup.row(itm_btn_3, itm_btn_4)
        self.markup.row((itm_btn_5))
        return self.markup

    def set_btn(self, name, step=0, quantity=0):
        return KeyboardButton(config.KEYBOARD[name])

    @staticmethod
    def remove_menu():
        return ReplyKeyboardRemove()

    def info_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        self.markup.row(itm_btn_1)
        return self.markup
