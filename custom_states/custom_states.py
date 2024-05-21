import telebot  # telebot

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup  # States

user_states = {}


# States group.
class MyStates:
    name_latin = 1
    name_cyrill = 2
    birth_date = 3
    passport_number = 4
    passport_given = 5
    passport_ends = 6
    contract_begins = 7
    registration_address = 8
    telephone = 9
    contract_ends = 10
    dismissal = 11
    make_it_cool = 12
    zaebis = 13




