import argparse
from telegram.ext import Application, Updater, CommandHandler
from quoter import Quoter
import telegram
import asyncio
import numpy as np
import json
from plotter import Plot


class NumpyEncoder(json.JSONEncoder):
    """Special json encoder for numpy types"""

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


parser = argparse.ArgumentParser(
    prog="Quotes Telegram Bot",
)
parser.add_argument("--bot-token", type=str, default=None, required=True)
parser.add_argument("--alerts-db", type=str, default=None, required=True)
parser.add_argument("--provider-uri", type=str, default=None, required=True)
args = parser.parse_args()
quoter = Quoter(args.provider_uri)


async def regname(update, context):
    if len(context.args) != 2:
        await update.message.reply_text("Error wrong input")
        return

    token_name, token_address = context.args
    quoter.regname(token_name, token_address)
    # YOUR CODE GOES HERE

    await update.message.reply_text("Successfully registered the name for token")


async def start(update, context):
    await update.message.reply_text(
        'Wake the F"ck up, Samurai.\nWe have a crypto to earn.'
    )

    await update.message.reply_text(
        f"Next commands are available in this bot:\n \
        /start - Repeat all this bullshit for you again\n \
        /regname <TOKEN NAME> <TOKEN ADDRESS> - Register token name for specified token adress\n \
        /quote <FOREIGN TOKEN ADDRESS/NAME> <DOMESTIC TOKEN ADDRESS/NAME> [<BLOCK INDENTIFIER>] [<BLOCK IDENTIFIER>] [<DELTA BLOCKS>] - Get information about price of foreign token in domestic token\n \
        /alert <FOREIGN TOKEN ADDRESS/NAME> <DOMESTIC TOKEN ADDRESS/NAME> <QUOTE LEVEL> - Get information when price will overcome threshold you have designated"
    )


async def alert(update, context):
    if len(context.args) != 3:
        await update.message.reply_text("Error wrong input")
        return
    chat_id = update.message.chat_id
    foreign, domestic, level = context.args
    quoter.add_alert(foreign, domestic, level, chat_id)
    # YOUR CODE GOES HERE
    await update.message.reply_text("Successfully registered alert!!!!")


async def quote(update, context):

    if len(context.args) < 2:
        await update.message.reply_text("Error wrong input")
        return
    # returning current level
    elif len(context.args) == 2:
        foreign, domestic = context.args
        block_start = quoter.w3.eth.block_number
        block_end = block_start + 1
        step = 1
        result = quoter.quote(
            foreign, domestic, int(block_start), int(block_end), int(step)
        )
        msg = (
            "Current level in block "
            + str(block_start)
            + " of "
            + foreign
            + " / "
            + domestic
            + " "
            + str(result[0])[0:10]
        )
        await update.message.reply_text(msg)
        return
    elif len(context.args) == 3:
        foreign, domestic, block_start = context.args
        block_end = int(block_start) + 1
        step = 1
        result = quoter.quote(
            foreign, domestic, int(block_start), int(block_end), int(step)
        )
        msg = (
            "Level in block "
            + str(block_start)
            + " of "
            + foreign
            + " / "
            + domestic
            + " "
            + str(result[0])[0:10]
        )
        await update.message.reply_text(msg)
        return
    elif len(context.args) == 4:
        foreign, domestic, block_start, block_end = context.args
        step = 1
    elif len(context.args) == 5:
        foreign, domestic, block_start, block_end, step = context.args
    else:
        await update.message.reply_text("AUCHTUNG!!!! TO MUCH ARGUMENTS")
        return
    result = quoter.quote(
        foreign, domestic, int(block_start), int(block_end), int(step)
    )
    await update.message.reply_text("Quote request registered. Wait for response.")

    plotter = Plot()  ###
    block_list = range(int(block_start), int(block_end), int(step))
    data = [price for price in result]

    plotter.draw_data(block_list, data)
    await context.bot.send_photo(update.effective_chat.id, "quote_plot.png")

    plotter.delete_picture()
    # await update.message.reply_photo(dumped)

    # for i in range(len(result)):
    #     await update.message.reply_text(float(result[i]))


def main():
    app = Application.builder().token(args.bot_token).build()

    # Adding commands
    app.add_handler(CommandHandler("regname", regname))
    app.add_handler(CommandHandler("alert", alert))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()
