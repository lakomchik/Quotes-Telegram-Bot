import argparse
from telegram.ext import Application, Updater, CommandHandler
from quoter import Quoter

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

    await update.message.reply_text("Please, add reply message")


async def alert(update, context):
    if len(context.args) != 3:
        await update.message.reply_text("Error wrong input")
        return

    foreign, domestic, level = context.args

    # YOUR CODE GOES HERE

    await update.message.reply_text("Please, add reply message")


async def quote(update, context):

    if len(context.args) < 2:
        await update.message.reply_text("Error wrong input")
        return
    elif len(context.args) == 2:
        foreign, domestic = context.args
        block_start = 16_000_000
        block_end = 16_000_001
        step = 1
    elif len(context.args) == 3:
        foreign, domestic, block_start = context.args
        block_end = int(block_start) + 1
        step = 1
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
    for i in range(len(result)):
        await update.message.reply_text(float(result[i]))


def main():

    app = Application.builder().token(args.bot_token).build()

    # Adding commands
    app.add_handler(CommandHandler("regname", regname))
    app.add_handler(CommandHandler("alert", alert))
    app.add_handler(CommandHandler("quote", quote))

    # Start the Bot
    app.run_polling()


if __name__ == "__main__":
    main()
