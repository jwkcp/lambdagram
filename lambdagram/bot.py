"""
This module has been created to help create telegram bot using pure telegram api on AWS lambda for serverless service.
You can also refer to the official documents through the links belows.

* Telegram bot api official documents: https://core.telegram.org/bots/api

You have to prepare two things before to use

1. Create your bot by @BotFather and get proper token you received.
2. Prepare an appreciate URL to handle the webhook behavior In this case we use lambda service on AWS.

* AWS lambda: https://ap-northeast-2.console.aws.amazon.com/lambda
"""
import requests


_BASE_URL = "https://api.telegram.org/bot{token}/"
_SEND_MSG_URL = _BASE_URL + "sendmessage"
_SET_WEBHOOK_URL = _BASE_URL + "setWebhook"
_GET_WEBHOOK_URL = _BASE_URL + "getWebhookInfo"
_DELETE_WEBHOOK_URL = _BASE_URL + "deleteWebhook"
_GETME_URL = _BASE_URL + "getMe"


class Bot:
    def __init__(self, token):
        """
        Create and initialize Lambdagram instance.

        :param token: The token you have issued from @BotFather
        """
        self.__token = token

    def get_me(self):
        """
        You can check bot information you have created.

        :return: User object(Dictionary type)
        Refer to https://core.telegram.org/bots/api#user
        Refer to https://jwkcp.github.io/2018/03/09/telegram-bot-api-response-json/ (In Korean)
        """
        return self._check_response(_GETME_URL)

    def set_webhook(self, webhook_url):
        """
        Set webhook url to lambda.

        :param webhook_url: The url will be received message from user who use your bot you created.
        :return: Dictionary type object containing the result will be returned.
        Refer to https://core.telegram.org/bots/api#setwebhook
        Refer to https://jwkcp.github.io/2018/03/09/telegram-bot-api-response-json/ (In Korean)
        """
        return self._check_response(_SET_WEBHOOK_URL, webhook_url)

    def get_webhook(self):
        """
        Get configurated webhook infomation.

        :return: WebhookInfo object(Dictionary type)
        Refer to https://core.telegram.org/bots/api#getwebhookinfo
        Refer to https://jwkcp.github.io/2018/03/09/telegram-bot-api-response-json/ (In Korean)
        """
        return self._check_response(_GET_WEBHOOK_URL)

    # {"ok":true,"result":true,"description":"Webhook was deleted"}
    def delete_webhook(self):
        """
        Delete the registered webhook from the telegram server.

        :return: Dictionary type object containing result.
        Refer to https://core.telegram.org/bots/api#deletewebhook
        Refer to https://jwkcp.github.io/2018/03/09/telegram-bot-api-response-json/ (In Korean)
        """
        return self._check_response(_DELETE_WEBHOOK_URL)

    def _check_response(self, url, webhook_url=None):
        """
        Utility function for other functions.

        :param url: The url you want to send message to.
        :param webhook_url: Webhook url you want to register
        :return: Dictionary type containing results or results that may contain information you request
        """
        if webhook_url:
            param = {'url': webhook_url}
            res = requests.get(url.format(token=self.__token), params=param).json()
        else:
            res = requests.get(url.format(token=self.__token)).json()

        return res

    def send_message(self, event, msg):
        """
        Send message to the user who has text to your bot. (Efficient)

        !NOTICE: you must set webhook url before use this method using web browser or somethong you can request to set webhook
        (https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOKURL}, remove '{' and '}')

        :param event: The object containing interaction information.
        Refer to https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/python-context-object.html
        Refer to https://jwkcp.github.io/2018/03/07/aws-lambda-event-object/ (In Korean)
        :param msg: The message you want to reply to user
        :return: Dictionary type containing results.
        """
        params = {'text': msg, 'chat_id': event.get("message").get('chat').get('id')}
        res = requests.get(_SEND_MSG_URL.format(token=self.__token), params=params)

        return res

    def send_message(self, event, msg, webhook_url):
        """
        Send message to the user who has text to your bot. (Inefficient)

        !NOTICE: I recommend you use 'send_message' method without webhook_url parameter.
        Because this method set webhook url every single request.
        This method just provided for beginners who are new to the telegram bot program implementation.

        :param event: The object containing interaction information.
        Refer to https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/python-context-object.html
        Refer to https://jwkcp.github.io/2018/03/07/aws-lambda-event-object/ (In Korean)
        :param msg: The message you want to reply to user
        :param webhook_url: The url you want to set before you send message.
        :return: Dictionary type containing results.
        """
        self.set_webhook(webhook_url)

        params = {'text': msg, 'chat_id': event.get("message").get('chat').get('id')}
        res = requests.get(_SEND_MSG_URL.format(token=self.__token), params=params)

        return res
