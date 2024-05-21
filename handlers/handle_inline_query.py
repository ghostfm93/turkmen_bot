from handlers.handler import Handler
from settings.message import MESSAGES
from custom_states.custom_states import MyStates


class HandlerInlineQuery(Handler):
    def __init__(self, bot):
        super().__init__(bot)
