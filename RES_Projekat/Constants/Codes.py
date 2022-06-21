from enum import Enum, auto


class Code(Enum):
    CODE_ANALOG = auto()
    CODE_DIGITAL = auto()
    CODE_CUSTOM = auto()
    CODE_LIMITSET = auto()
    CODE_SINGLENOE = auto()
    CODE_MULTIPLENODE = auto()
    CODE_CONSUMER = auto()
    CODE_SOURCE = auto()

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))


CODES = Code.list()