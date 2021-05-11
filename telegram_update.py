
class UpdateStatus:
    DONE = 0,
    TOMORROW = 1


class CardUpdateInfo:
    def __init__(self, status, card_id):
        self.status = status
        self.card_id = card_id


class TelegramUpdate:
    def __init__(self, data):
        self.data = data
        self.is_callback = "callback_query" in self.data

    def get_card_info(self):
        data = self.data["callback_query"]["data"].split()
        return CardUpdateInfo(UpdateStatus.DONE if data[0] == "done" else UpdateStatus.TOMORROW, data[-1])
