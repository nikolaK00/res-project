import threading

from Components.Writer import Writer


class Application:
    @staticmethod
    def Start():
        automatic_data_sending_thread = threading.Thread(target=Writer.RunDataSending, args=())
        automatic_data_sending_thread.start()
