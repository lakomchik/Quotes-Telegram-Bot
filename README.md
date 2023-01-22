# Quotes Telegram Bot

You need to write telegram bot that enable users extract quotes from UniswapV2 DEX and send alerts in case the quote reaches the specific level.

There is a [great lib](https://docs.python-telegram-bot.org/en/stable/examples.html) for creating telegram bots on python. Read the documentantion and understand the details of implementation.

Follow [this guide](https://core.telegram.org/bots/tutorial) to create your telegram bot and understand the core functionality.

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

The command should send immediate response to the user about successful registering of the new name.

### `/quote`
```
/quote <FOREIGN TOKEN ADDRESS/NAME> <DOMESTIC TOKEN ADDRESS/NAME> [<BLOCK INDENTIFIER>] [<BLOCK IDENTIFIER>] [<DELTA BLOCKS>]
``` 
For instance, 
```
/quote WETH USDT 
```
should immediately return the current quote in USDT and 
```
/quote WETH USDT 16000000 
```
should immediately return quote in USDT as of 16000000 block. FYI the so called foreign and domestic notation is used in classical 
FX markets for pair identification. Thus, in the pair USDRUB USD is the foreign currency and RUB is domestic currency.

Note that the commands
```
/quote 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 0xdAC17F958D2ee523a2206206994597C13D831ec7
/quote 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 USDT 16000000
``` 
should be still valid, i.e. it should be indifferent for user to work either with adresses or with registered names  

If a user sends the quote command with 2 blocks like
```
/quote WETH USDT 16000000 16000100
```
then the user should receive the immediate response with a plot of WETH/USDT quote for block range [16000000, 16000100). The last 
optional argument `[<DELTA BLOCKS>]` is the analogue of the third argument in classical `range` Python function. Thus,
```
/quote WETH USDT 16000000 16010000 100
```
should return plot for every 100th block in range [16000000, 16010000). 
### `/alert`
```
/alert <FOREIGN TOKEN ADDRESS/NAME> <DOMESTIC TOKEN ADDRESS/NAME> <QUOTE LEVEL>
``` 
should send alert to user if the price reaches the `<QUOTE LEVEL>`. For instance, current WETH/USDT quote equals 1300. You send the following command to bot
```
/alert WETH USDT 1350
```
In this case the first moment when WETH/USDT is greater than 1350 the telegram bot should send the alert message about the event. Moreover, it should attach the
plot of the quote with the 2 levels: entry one and alert level.  

The command should send 2 responses. The first response is the immediate one about successful processed `/alert` request. The second response should be alert

## Architecture

It is reasonable to write 2 executable Python files for the project. The first one handles messages from users and sends immediate responses. 
```
python telegram_bot.py 
    --provider-uri http://localhost:8545 \
    --bot-token 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11 \
    --alerts-db alerts.csv  
```
The template for `telefram_bot.py` is already written. [Create bot token](https://core.telegram.org/bots/tutorial) 
and run the file via
```
python telegram_bot.py 
    --provider-uri empty \
    --bot-token <YOUR BOT TOKEN> \
    --alerts-db empty  
```
to see how it works. 

The other python script
```
python alert_handler.py
    --provider-uri http://localhost:8545 \
    --bot-token 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11 \
    --alerts-db alerts.csv
```
should parse `alerts.csv` file and extract quotes for the alert messages. The quotes should be extracted via batch responses.
## Provider URI
Unfortunately, [https://getblock.io/](https://getblock.io/) doesn't provide archive nodes in their free plan. For archive nodes one can use [https://www.infura.io/](https://www.infura.io/) or [https://www.alchemy.com/](https://www.alchemy.com/). Archive nodes provide the functionality for extracting any smart contract data as of any past block, while full nodes (as in [https://getblock.io/](https://getblock.io/)) keep this kind of data for the last 128 blocks.
 
 
