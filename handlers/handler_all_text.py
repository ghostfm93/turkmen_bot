import re
from custom_scripts.format_message_info import make_it_beautiful
from settings.message import MESSAGES
from settings import config
from handlers.handler import Handler
from custom_states.custom_states import MyStates, user_states
from custom_scripts.script import user_data, MakeDocs


class HandlerAllText(Handler):
    def __init__(self,bot):
        super().__init__(bot)
        self.step = 0
        self.date_pattern = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d{2}$"
        self.name_latin_pattern = r"[A-Z][a-z]+\s[A-Z][a-z]+"
        self.name_cyrill_pattern = r"[А-Я][а-я]+\s[А-Я][а-я]+"
        self.telephone_number_pattern = r"\+375(33|29|25|44)\d{7}"
        self.passport_number_pattern = r"[АA]\d{7}"

    def pressed_btn_info(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['manage_bot'],
                              parse_mode = 'HTML',
                              reply_markup = self.keyboards.info_menu())

    def pressed_btn_back(self, message):
        self.bot.send_message(message.chat.id, 'Вы вернулись назад',
                              reply_markup = self.keyboards.start_menu())

    def pressed_btn_choose_action(self, message):
        self.bot.send_message(message.chat.id, 'Выберите действие',
                              reply_markup = self.keyboards.actions_menu())

    def action_selected(self, message):
        self.bot.send_message(message.chat.id, f'Выбрано {message.text}',
                              reply_markup = self.keyboards.info_menu())

    def cool_button(self, message):
        self.bot.send_message(message.chat.id, f'Сделать заебись?',
                              reply_markup = self.keyboards.make_it_great())

    def handle(self):
        @self.bot.message_handler(func = lambda message: message.text == 'Вернуться в начало')
        def handle_back(message):
            user_states[message.chat.id] = None
            self.pressed_btn_back(message)

        @self.bot.message_handler(func=lambda message: user_states.get(message.chat.id) is None)
        def handle_messages(message):
            if message.text == config.KEYBOARD['ABOUT']:
                self.pressed_btn_info(message)
            if message.text == config.KEYBOARD['Choose_action']:
                self.pressed_btn_choose_action(message)
            if message.text == config.KEYBOARD['Turkmen_invite']:
                self.action_selected(message)
                user_states[message.chat.id] = MyStates.name_latin
                user_data[message.chat.id] = {'choice' : 'turkmenistan'}
                self.bot.send_message(message.chat.id, "Введите ФИО работника латиницей через пробел:")
            if message.text == config.KEYBOARD['Recruitment']:
                self.action_selected(message)
                user_states[message.chat.id] = MyStates.name_latin
                user_data[message.chat.id] = {'choice' : 'recruitment'}
                self.bot.send_message(message.chat.id, "Введите ФИО работника латиницей через пробел:")
            if message.text == config.KEYBOARD['Recruitment_Minsk']:
                self.action_selected(message)
                user_states[message.chat.id] = MyStates.name_latin
                user_data[message.chat.id] = {'choice' : 'recruitment_minsk'}
                self.bot.send_message(message.chat.id, "Введите ФИО работника латиницей через пробел:")
            if message.text == config.KEYBOARD['Dismissal']:
                self.action_selected(message)
                user_states[message.chat.id] = MyStates.name_latin
                user_data[message.chat.id] = {'choice' : 'dismissal'}
                self.bot.send_message(message.chat.id, "Введите ФИО работника латиницей через пробел:")

        @self.bot.message_handler(func=lambda message: message.chat.id in user_states)
        def handle_stated_messages(message):
            docs = MakeDocs(user_data[message.chat.id])
            state = user_states[message.chat.id]
            if state == MyStates.name_latin:
                if re.fullmatch(self.name_latin_pattern, message.text):
                    user_data[message.chat.id]['name_latin'] = message.text
                    if docs.driver_exist():
                        self.bot.send_message(message.chat.id, "Данный водитель есть в базе, введите дату заключения контракта в формате ДД.ММ.ГГГГ:")
                        docs.get_context_from_existing_driver()
                        user_states[message.chat.id] = MyStates.contract_begins
                    else:
                        user_states[message.chat.id] = MyStates.name_cyrill
                        self.bot.send_message(message.chat.id, "Введите ФИО работника кириллицей через пробел:")
                else:
                    self.bot.send_message(message.chat.id, "Неверный формат имени!")
                    self.bot.send_message(message.chat.id, "Введите ФИО работника латиницей через пробел:")
            elif state == MyStates.name_cyrill:
                if re.fullmatch(self.name_cyrill_pattern, message.text):
                    user_data[message.chat.id]['name_cyrill'] = message.text
                    user_states[message.chat.id] = MyStates.birth_date
                    self.bot.send_message(message.chat.id, "Введите дату рождения работника в формате ДД.ММ.ГГГГ:")
                else:
                    self.bot.send_message(message.chat.id, "Неверный формат имени!")
                    self.bot.send_message(message.chat.id, "Введите ФИО работника кириллицей через пробел:")
            elif state == MyStates.birth_date:
                if re.fullmatch(self.date_pattern, message.text):
                    user_data[message.chat.id]['birth_date'] = message.text
                    user_states[message.chat.id] = MyStates.passport_number
                    self.bot.send_message(message.chat.id, "Введите номер паспорта работника в формате А1234567:")
                else:
                    self.bot.send_message(message.chat.id, "Неверный формат даты!")
                    self.bot.send_message(message.chat.id, "Введите дату рождения работника в формате ДД.ММ.ГГГГ:")
            elif state == MyStates.passport_number:
                if re.fullmatch(self.passport_number_pattern, message.text):
                    user_data[message.chat.id]['passport_number'] = message.text
                    user_states[message.chat.id] = MyStates.passport_given
                    self.bot.send_message(message.chat.id, "Введите дату выдачи паспорта в формате ДД.ММ.ГГГГ:")
                else:
                    self.bot.send_message(message.chat.id, "Неверный формат номера паспорта!")
                    self.bot.send_message(message.chat.id, "Введите номер паспорта работника в формате А1234567:")
            elif state == MyStates.passport_given:
                if re.fullmatch(self.date_pattern, message.text):
                    user_data[message.chat.id]['passport_given'] = message.text
                    user_states[message.chat.id] = MyStates.passport_ends
                    self.bot.send_message(message.chat.id, "Введите дату окончания действия паспорта в формате ДД.ММ.ГГГГ:")
                else:
                    self.bot.send_message(message.chat.id, "Неверный формат даты выдачи паспорта!")
                    self.bot.send_message(message.chat.id, "Введите дату выдачи паспорта в формате ДД.ММ.ГГГГ:")
            elif state == MyStates.passport_ends:
                if re.fullmatch(self.date_pattern, message.text):
                    user_data[message.chat.id]['passport_ends'] = message.text
                    user_states[message.chat.id] = MyStates.contract_begins
                    self.bot.send_message(message.chat.id, "Введите дату заключения контракта в формате ДД.ММ.ГГГГ:")
                else:
                    self.bot.send_message(message.chat.id, "Неверный формат даты окончания действия паспорта!")
                    self.bot.send_message(message.chat.id, "Введите дату окончания действия паспорта в формате ДД.ММ.ГГГГ:")
            elif state == MyStates.contract_begins:
                if re.fullmatch(self.date_pattern, message.text):
                    user_data[message.chat.id]['contract_begins'] = message.text
                    if  user_data[message.chat.id]['choice'] in ['recruitment', 'recruitment_minsk']:
                        user_states[message.chat.id] = MyStates.registration_address
                        self.bot.send_message(message.chat.id, "Введите адрес регистрации работника:")
                    elif user_data[message.chat.id]['choice'] == 'dismissal':
                        user_states[message.chat.id] = MyStates.contract_ends
                        self.bot.send_message(message.chat.id, "Введите дату расторжения контракта в формате ДД.ММ.ГГГГ::")
                    else:
                        self.bot.send_message(message.chat.id, make_it_beautiful(user_data[message.chat.id]), parse_mode='HTML', reply_markup=self.keyboards.make_it_great())
                        user_states[message.chat.id] = MyStates.make_it_cool
                else:
                    self.bot.send_message(message.chat.id, "Неверный формат даты заключения контракта!")
                    self.bot.send_message(message.chat.id, "Введите дату заключения контракта в формате ДД.ММ.ГГГГ:")
            elif state == MyStates.contract_ends:
                if re.fullmatch(self.date_pattern, message.text):
                    user_data[message.chat.id]['contract_ends'] = message.text
                    self.bot.send_message(message.chat.id, make_it_beautiful(user_data[message.chat.id]), parse_mode='HTML', reply_markup=self.keyboards.make_it_great())
                    user_states[message.chat.id] = MyStates.make_it_cool
                else:
                    self.bot.send_message(message.chat.id, "Неверный формат даты расторжения контракта!")
                    self.bot.send_message(message.chat.id, "Введите дату расторжения контракта в формате ДД.ММ.ГГГГ:")
            elif state == MyStates.registration_address and  user_data[message.chat.id]['choice'] in ['recruitment', 'recruitment_minsk']:
                user_data[message.chat.id]['registration_address'] = message.text
                user_states[message.chat.id] = MyStates.telephone
                self.bot.send_message(message.chat.id, "Введите номер телефона работника в формате +375123456789:")
            elif state == MyStates.telephone  and  user_data[message.chat.id]['choice'] in ['recruitment', 'recruitment_minsk']:
                if re.fullmatch(self.telephone_number_pattern, message.text):
                    user_data[message.chat.id]['telephone'] = message.text
                    self.bot.send_message(message.chat.id, "Введите название Отдела по гражданству и миграции:")
                    user_states[message.chat.id] = MyStates.ogim
                else:
                    self.bot.send_message(message.chat.id, "Неверный формат номера телефона работника!")
                    self.bot.send_message(message.chat.id, "Введите номер телефона работника в формате +375123456789:")
            elif state == MyStates.ogim  and  user_data[message.chat.id]['choice'] in ['recruitment', 'recruitment_minsk']:
                user_data[message.chat.id]['ogim'] = message.text
                self.bot.send_message(message.chat.id, make_it_beautiful(user_data[message.chat.id]), parse_mode='HTML', reply_markup=self.keyboards.make_it_great())
                user_states[message.chat.id] = MyStates.make_it_cool
            elif state == MyStates.make_it_cool:
                user_states[message.chat.id] = MyStates.zaebis
                print(len(user_data[message.chat.id].items()))
            if len(user_data[message.chat.id].items()) == 8 and \
                    not user_data[message.chat.id]['choice'] in ['recruitment', 'recruitment_minsk', 'dismissal']\
                    and user_states[message.chat.id] == MyStates.zaebis:
                print('делаем договор и ходатайство')
                if docs.make_turkmenistan_invite():
                    self.bot.send_message(message.chat.id, f"Созданы документы на имя {user_data[message.chat.id]['name_cyrill']}\nОтправляю...")
                    for filepath in docs.filepaths:
                        self.bot.send_document(message.chat.id, open(filepath, 'rb'), reply_markup=self.keyboards.info_menu())
                        user_states[message.chat.id] = None
            elif len(user_data[message.chat.id].items()) == 11 and user_states[message.chat.id] == MyStates.zaebis:
                if docs.make_recruitment_optional():
                    self.bot.send_message(message.chat.id, f"Созданы документы на имя {user_data[message.chat.id]['name_cyrill']}\nОтправляю...")
                    for filepath in docs.filepaths:
                        self.bot.send_document(message.chat.id, open(filepath, 'rb'), reply_markup=self.keyboards.info_menu())
                    user_states[message.chat.id] = None
            elif user_data[message.chat.id]['choice'] == 'dismissal' and len(user_data[message.chat.id]) == 9 \
                    and user_states[message.chat.id] == MyStates.zaebis:
                print('Увольняем к хуям')
                if docs.make_dismissal_notification():
                    self.bot.send_message(message.chat.id, f"Создано уведомление об увольнении на имя {user_data[message.chat.id]['name_cyrill']}\nОтправляю...")
                    for filepath in docs.filepaths:
                        self.bot.send_document(message.chat.id, open(filepath, 'rb'), reply_markup=self.keyboards.info_menu())
                    user_states[message.chat.id] = None