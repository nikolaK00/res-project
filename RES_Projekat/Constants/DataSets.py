from Constants.Codes import *


class DataSet(Enum):
    DataSet_1 = (Code.CODE_ANALOG, Code.CODE_DIGITAL)
    DataSet_2 = (Code.CODE_CUSTOM, Code.CODE_LIMITSET)
    DataSet_3 = (Code.CODE_SINGLENOE, Code.CODE_MULTIPLENODE)
    DataSet_4 = (Code.CODE_CONSUMER, Code.CODE_SOURCE)

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


DATASETS = DataSet.list()