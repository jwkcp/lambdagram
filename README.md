# lambdagram

lambdagram is the library to help who want to create telegram bot with [official telegram bot api](https://core.telegram.org/bots/api) using webhook on AWS lambda.
   
## Introduction

Main target of this library is who want to create telegram bot using webhook simply and easily. Especially for AWS lambda platform. Because AWS lambda do not allow to use polling mechanism for infinite loops. Just sending and receiving message through webhook. Not a big deal. But I believe this pretty helpful for someone who telegram and AWS lambda newbies.

## Installing

~~~
pip install lamdbgram
~~~  

## Telegram API support

- getMe
- setWebhook
- getWebhookInfo
- deleteWebhook

## Key function the lambdagram support

- send_message

## How to use

~~~
WEBHOOK = "https://YOUR-WEBHOOK-URL"
TOKEN = "THE TOKEN YOU GOT FROM @BotFather"
  
def lambda_handler(event, context): # Basic function signature on AWS lambda 
    
    l = Lambdagram(TOKEN)
    l.set_webhook(WEBHOOK)
    
    l.send_message(event, "THE MESSAGE YOU WANT TO SEND")
~~~

 