from handlers.handler import Handler
from settings.message import MESSAGES
from custom_states.custom_states import MyStates


class HandlerInlineQuery(Handler):
    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_park(self, call, code):
        keys = get_keys(code)
        self.bot.answer_callback_query(call.id,f'Выбран парк {call.data}',
                                       show_alert = True)
        self.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.id)
        self.bot.send_message(call.message.chat.id, 'Выберите нужный парк',
                              reply_markup = self.keyboards.actions_menu())
        self.bot.set_state(call.message.from_user.id, MyStates.park, call.message.chat.id)
        return keys

    def handle(self):
        @self.bot.callback_query_handler(func = lambda call: True)
        def callback_inline(call):
            code = call.data
            self.pressed_btn_park(call,code)
