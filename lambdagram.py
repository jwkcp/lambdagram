import requests
import json


_BASE_URL = "https://api.telegram.org/{}/"
_SENDMSG_URL = _BASE_URL + "sendmessage?text={}&chat_id={}"
_SET_WEBHOOK_URL = _BASE_URL + "setWebhook?url={}"
_GET_WEBHOOK_URL = _BASE_URL + "getWebhook"
_DELETE_WEBHOOK_URL = _BASE_URL + "deleteWebhook"

class Lambdagram:
    def __init__(self, token):
        self.__token = token
        self.__was_webhook_set = False

    # {"ok":true,"result":true,"description":"Webhook is deleted"}
    def set_webhook(self, url):
        if not self.__was_webhook_set:
            result = self.check_response(_SET_WEBHOOK_URL.format(url))
            self.__was_webhook_set = True
            return result
        else:
            return (True, "Webhook already has been set.")

    def get_webhook(self):
        return self.check_response(_GET_WEBHOOK_URL)

    # {"ok":true,"result":true,"description":"Webhook was deleted"}
    def delete_webhook(self):
        return self.check_response(_DELETE_WEBHOOK_URL)

    def _check_response(self, url):
        res = requests.get(url)
        dict = json.loads(res)

        if dict.get("ok") != "true" or dict.get("result") != "true":
            return False, dict.get("description")
        else:
            return True, dict.get("description")

