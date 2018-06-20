# lambdagram

lambdagram is the library to help who want to create telegram bot with [official telegram bot api](https://core.telegram.org/bots/api) using webhook on AWS lambda.
   
## Introduction

Main target of this library is who want to create telegram bot using webhook simply and easily. Especially for AWS lambda platform. Because AWS lambda do not allow to use polling mechanism for infinite loops. Just sending and receiving message through webhook. Not a big deal. But I believe this pretty helpful for someone who telegram and AWS lambda newbies.

## Installing

~~~
pip install lambdagram
~~~  

## Telegram API support

- getMe
- setWebhook
- getWebhookInfo
- deleteWebhook

## Key function the lambdagram support

- send_message(self, event, msg, options...) - Efficient way, but you must set webhook before use this method using web browser.
  (https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOKURL}, remove '{' and '}')
- send_message(self, event, msg, webhook_url, options...) - Inefficient way, but it's useful for beginners.

## How to use

~~~
from lambdagram.bot import Bot


TOKEN = "THE TOKEN YOU GOT FROM @BotFather"
  
def lambda_handler(event, context): # Basic function signature on AWS lambda 
    
    bot = Bot(TOKEN)
    bot.send_message(event, "THE MESSAGE YOU WANT TO SEND")
~~~
  
or
  
~~~
from lambdagram.bot import Bot


WEBHOOK = "https://YOUR-WEBHOOK-URL"
TOKEN = "THE TOKEN YOU GOT FROM @BotFather"
  
def lambda_handler(event, context): # Basic function signature on AWS lambda 
    
    bot = Bot(TOKEN)
    bot.send_message(event, "THE MESSAGE YOU WANT TO SEND", WEBHOOK)
~~~

 
