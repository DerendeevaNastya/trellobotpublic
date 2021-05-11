import requests


class TelegramClient:
    def __init__(self, TOKEN, CHAT_ID):
        self.token = TOKEN
        self.chat_id = CHAT_ID

    def get_me(self):
        result = self._make_request_get_json_resp("GET", "getMe")
        return result

    def get_updates(self):
        result = self._make_request_get_json_resp("POST", "getUpdates")
        return result

    def send_message(self, text, params={}):
        params = {**params, **{"chat_id": self.chat_id, "text": text}}
        result = self._make_request_get_json_resp("POST", "sendMessage", params)
        return result

    def _make_request_get_json_resp(self, method_type, method_name, params={}):
        url = f"https://api.telegram.org/bot{self.token}/{method_name}"
        req = None

        if method_type == "POST":
            req = requests.post(url, data=params)
        elif method_type == "GET":
            req = requests.get(url, data=params)
        else:
            raise ValueError(f"Can't send request (type={method_type}, method_name={method_name})")

        jsonResponse = req.json()
        print(jsonResponse)
        return jsonResponse
