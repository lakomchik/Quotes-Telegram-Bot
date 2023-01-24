import argparse
from telegram.ext import Application, Updater, CommandHandler
from quoter import Quoter
from plotter import Plot

parser = argparse.ArgumentParser(
    prog="Quotes Telegram Bot",
)
parser.add_argument("--bot-token", type=str, default=None, required=True)
parser.add_argument("--alerts-db", type=str, default=None, required=False)
parser.add_argument("--provider-uri", type=str, default=None, required=True)
args = parser.parse_args()

quoter = Quoter(args.provider_uri)
plotter = Plot()

async def regname(update, context):
    if len(context.args) != 2:
        await update.message.reply_text("Error: wrong input of /regname")
        return

    token_name, token_address = context.args
    quoter.regname(token_name, token_address)

    await update.message.reply_text(f"Successfully registered name {token_name} on address {token_address}")

async def alert(update, context):
    if len(context.args) != 3:
        await update.message.reply_text("Error wrong input")
        return
    chat_id = update.message.chat_id
    foreign, domestic, level = context.args
    quoter.add_alert(foreign, domestic, level, chat_id)

async def quote(update, context):

    if len(context.args) < 2:
        await update.message.reply_text("Error: wrong input of /quote \
                                        (length of token_name cannot be less than 2)")
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

async def start(update, context):
    await update.message.reply_text('Hi, there! It is time to have fun and do cryptoanalysis.')

    await update.message.reply_text(f'Next commands are available in this bot:\n \
        /start - Start working with me\n \
        /regname - Register token name for specific token address\n \
        /quote - Get information about price of foreign token in domestic token\n \
        /alert - Get information when price will overcome threshold you have designated')

    id = [1, 2, 3, 4]
    data = [10, 20, 40, 70]
    plotter.draw_data(id, data)

    await context.bot.send_photo(update.effective_chat.id, "multiple_quote.png")

def main():

    app = Application.builder().token(args.bot_token).build()

    # Adding commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler("regname", regname))
    app.add_handler(CommandHandler("alert", alert))
    app.add_handler(CommandHandler("quote", quote))

    # Start the Bot
    app.run_polling()


if __name__ == "__main__":
    main()
