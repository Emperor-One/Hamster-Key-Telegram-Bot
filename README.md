# Hamster-Key-Telegram-Bot

This is a simple telegram bot you can host on your own computer to generate 
Hamster Kombat keys.

## Getting Started

The first thing you have to do is go talk to the [BotFather](https://t.me/BotFather) on telegram.
After you do _/newbot_, It will ask you a series of simple questions and all you
have to do is give it the name, and username of your bot and it will give you
an **API TOKEN**. This token is how you will access the telegram API. The bot
won't work without it.

Now, clone this repo:
```sh
git clone https://github.com/Emperor-One/Hamster-Key-Telegram-Bot.git
```
You will need to [download](https://www.python.org/downloads/) python if you don't have it on your system.

Next, you will open the bot.py file with your text editor of choice, and copy  
paste your **API TOKEN** to the following variable:
```python
TOKEN_INSECURE = "<PASTE YOUR TELEGRAM BOT TOKEN  HERE>"
```
It should look something like this:
```python
TOKEN_INSECURE = "7461996478:AAG7j04LJ8m6fmXLjarmyiRU9S2AhTg6Lot7iiw"
```
---
Warning: It is highly recommended that you do not save your API TOKEN in plain text
on the code. If you want to be secure you should save your Token in an environment
variable named HAMSTER\_KOMBAT\_TOKEN. See the saving your Token in an environment variable
section below.
---

Once you have saved your token to bot.py or to an , and install the required packages with this command:
```sh
pip install -r requirements.txt
```

Finally, you can run the bot, and enjoy your keys.
```sh
python bot.py
```


