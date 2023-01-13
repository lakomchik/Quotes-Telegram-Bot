# Quotes Telegram Bot

You need to write telegram bot that enable users extract quotes from UniswapV2 DEX and send alerts in case the quote reaches the specific level.

There is a [great lib](https://docs.python-telegram-bot.org/en/stable/examples.html) for creating telegram bots on python. Read the documentantion and understand the details of implementation.

## Functionality

The telegram bot should have the following functionality. 

### `/regname`

```
/regname <TOKEN NAME> <TOKEN ADDRESS>
``` 
should register `<TOKEN NAME>` for `<TOKEN ADDRESS>`. For instance, commands
```
/regname WETH 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
/regname USDT 0xdAC17F958D2ee523a2206206994597C13D831ec7
```
register 2 names WETH and USDT which enable users do not use addresses, but use names instead. 

### `/quote`
```
/quote <FOREIGN TOKEN ADDRESS/NAME> <DOMESTIC TOKEN ADDRESS/NAME> [<BLOCK INDENTIFIER>]
``` 
For instance, 
```
/quote WETH USDT 
```
should return the current quote in USDT and 
```
/quote WETH USDT 16000000 
```
should return quote in USDT as of 16000000 block. Note that the commands
```
\quote 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 0xdAC17F958D2ee523a2206206994597C13D831ec7
\quote 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 USDT 16000000
``` 
should be still valid, i.e. it should be indifferent for user to work either with adresses or with registered names  

### `/alert`
```
/alert <FOREIGN TOKEN ADDRESS/NAME> <DOMESTIC TOKEN ADDRESS/NAME> <QUOTE LEVEL>
``` 
should send alert to user if the price reaches the `<QUOTE LEVEL>`. For instance, current WETH/USDT quote equals 1300. You send the following command to bot
```
/alert WETH USDT 1350
```
In this case the first moment when WETH/USDT is greater than 1350 the telegram bot should send the alert message about the event.
 