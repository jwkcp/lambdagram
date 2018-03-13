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

    def send_message(self
                     , event
                     , msg
                     , chat_id=None
                     , webhook_url=None
                     , parse_mode=None
                     , disable_web_page_preview=None
                     , disable_notification=None
                     , reply_to_message_id=None
                     , reply_markup=None):
        """
        Send message to the user who has text to your bot.

        !NOTICE: To set the webhook_url parameter to None, you must set webhook url using web browser or somethong you can request to set webhook
        (https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOKURL}, remove '{' and '}')

        It is recommended...
        to use this method without webhook_url parameter. It is more efficient way. \
        If you pass webhook_url value, every single request will be sent to telegram server. It is quite inefficient.
        It is just provided for beginners who are new to the telegram bot program implementation.

        Refer to detail information about parameters: https://core.telegram.org/bots/api#sendmessage

        :param event: The object containing interaction information.
        Refer to https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/python-context-object.html
        Refer to https://jwkcp.github.io/2018/03/07/aws-lambda-event-object/ (In Korean)
        :param msg: The message you want to reply to user
        :param chat_id: Set this parameter to use push notification to channel you have created. When this value is set,
        'event' parameter will be ignored. (e.g. @CHANNEL_ID_YOU_HAVE_SET)
        :param webhook_url: The url you want to set before you send message.
        :param parse_mode: Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your bot's message.
        :param disable_web_page_preview: Disables link previews for links in this message
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param reply_to_message_id: If the message is a reply, ID of the original message
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :return: Dictionary type containing results.
        """
        if webhook_url:
            self.set_webhook(webhook_url)

        if chat_id:
            params = {'text': msg, 'chat_id': chat_id}
        else:
            params = {'text': msg, 'chat_id': event.get("message").get('chat').get('id')}

        if parse_mode:
            params['parse_mode'] = parse_mode
        if disable_web_page_preview:
            params['disable_web_page_preview'] = disable_web_page_preview
        if disable_notification:
            params['disable_notification'] = disable_notification
        if reply_to_message_id:
            params['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            params['reply_markup'] = reply_markup

        res = requests.get(_SEND_MSG_URL.format(token=self.__token), params=params)

        return res
