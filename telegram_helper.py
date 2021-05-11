from telegram_update import TelegramUpdate
import json


class TelegramHelper:
    def __init__(self, telegram_client):
        self.client = telegram_client

    def get_updated_cards(self):
        updates = self.client.get_updates()
        list_updates = updates["result"] if "result" in updates else []

        infos = []
        for update in list_updates:
            update_data = TelegramUpdate(update)
            if update_data.is_callback:
                infos.append(update_data.get_card_info())
        return infos

    def send_all_messages(self, messages):
        for message in messages:
            self.client.send_message(message.text, {"reply_markup": json.dumps(message.params)})
