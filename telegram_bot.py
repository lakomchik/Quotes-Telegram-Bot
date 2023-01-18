import argparse
from utils.providers import get_provider_from_uri
from web3 import Web3
import logging
from telegram.ext import Application, Updater, CommandHandler
from omegaconf import OmegaConf
import argparse
from web3 import Web3


parser = argparse.ArgumentParser(
    prog="Quotes Telegram Bot",
)
parser.add_argument("--bot-token", type=str, default=None, required=True)
parser.add_argument("--alerts-db", type=str, default=None, required=True)
parser.add_argument("--provider-uri", type=str, default=None, required=True)
args = parser.parse_args()


async def regname(update, context):
    if len(context.args) != 2:
        await update.message.reply_text("Error wrong input")
        return

    token_name, token_address = context.args

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

    # YOUR CODE GOES HERE

    await update.message.reply_text("Please, add reply message")


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
