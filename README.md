## This is a simple Telegram bot that monitors how much water you drink per day.

There are three main command for interactive with the bot:

`/help` - this is a general information about bot

`/start` - this is a little hint what you need to do

`/statistic` - this is the average value of how much water you drink per day for all period of use this bot.

First of all fill in input field with the amount of water just drank for example `250`. As response you will get:
```
Now 2022-01-27 21:00 you was drank 250 ml of water!

<<<<<<< HEAD
Don`t give up, to norm left 1750 ml!!!
=======
Don`t give up, to norm left 250 ml!!!
>>>>>>> a63a037cfd017a7ecd3199f5633349b4a48c9372
```

When you repeat previous step your estimate update with current value.

When you make norm `2000` ml, you get a congratulations letter.
