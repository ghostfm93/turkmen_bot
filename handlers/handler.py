import abc
from markup.markup import Keyboards


class Handler(metaclass=abc.ABCMeta):

    def __init__(self,bot):
        self.bot = bot
        self.keyboards = Keyboards()

    @abc.abstractmethod
    def handle(self):
        pass