import argparse
from utils.providers import get_provider_from_uri
import pandas as pd
import requests as tg_requests
from web3 import Web3
import utils.providers as providers
import utils.requests as requests
import json
from decimal import Decimal
import time

parser = argparse.ArgumentParser(
    prog="Alerts Handler",
)
parser.add_argument("--bot-token", type=str, default=None, required=True)
parser.add_argument("--alerts-db", type=str, default=None, required=True)
parser.add_argument("--provider-uri", type=str, default=None, required=True)
args = parser.parse_args()


# Function to write message to chat
def telegram_bot_sendtext(message, chatID):
    bot_token = args.bot_token
    bot_chatID = chatID
    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + bot_chatID
        + "&parse_mode=Markdown&text="
        + message
    )
    response = tg_requests.get(send_text)
    return response.json()


class Alarmer:
    def __init__(self) -> None:
        self.table_name = "alerts.csv"
        alert_table = pd.read_csv(self.table_name)
        # check that table is not empty if not, creating new one
        if alert_table.shape[0] == 0:
            new_table = alerts_table = pd.DataFrame(
                [],
                columns=[
                    "domestic_token",
                    "domestic_name",
                    "foreign_token",
                    "foreign_name",
                    "pair_adress",
                    "token0_adress",
                    "token1_adress",
                    "level",
                    "decimals0",
                    "decimals1",
                    "chat_id",
                ],
            )
            new_table.to_csv(self.table_name, index=False)
        self.provider_uri = args.provider_uri
        self.w3 = Web3(Web3.HTTPProvider(self.provider_uri))
        self.batch_w3 = providers.get_provider_from_uri(self.provider_uri, batch=True)

    def spin(self):
        alerts_table = pd.read_csv(self.table_name)
        block = []
        # Prepating batch request
        last_block_number = self.w3.eth.block_number
        for i in range(alerts_table.shape[0]):
            block.append(
                requests.get_request_balanceof(
                    alerts_table["token0_adress"][i],
                    alerts_table["pair_adress"][i],
                    last_block_number,
                    i * 2 + 0,
                )
            )
            block.append(
                requests.get_request_balanceof(
                    alerts_table["token1_adress"][i],
                    alerts_table["pair_adress"][i],
                    last_block_number,
                    i * 2 + 1,
                )
            )
        block_responses = self.batch_w3.make_batch_request(json.dumps(block))
        values = []
        for i in range(len(block_responses) // 2):
            token_0_amount = Decimal(
                int(block_responses[i * 2]["result"], base=16)
            ) / Decimal(10 ** int(alerts_table["decimals0"][i]))
            token_1_amount = Decimal(
                int(block_responses[i * 2 + 1]["result"], base=16)
            ) / Decimal(10 ** int(alerts_table["decimals1"][i]))
            if alerts_table["domestic_token"][i] == alerts_table["token1_adress"][i]:
                values.append(token_1_amount / token_0_amount)
            else:
                values.append(token_0_amount / token_1_amount)
        del_ids = []  # list of row indexes that should be deleted in case alarm
        for i in range(len(values)):
            if values[i] > float(alerts_table["level"][i]):
                msg = (
                    "ACHTUNG!!!\n Level of "
                    + alerts_table["foreign_name"][i]
                    + "/"
                    + alerts_table["domestic_name"][i]
                    + " is higher than "
                    + str(alerts_table["level"][i])
                    + ".\n Current level is "
                    + str(values[i])[0:10]
                )
                del_ids.append(i)
                telegram_bot_sendtext(msg, str(alerts_table["chat_id"][i]))
        print(del_ids)
        alerts_table = alerts_table.drop(del_ids)
        alerts_table.to_csv(self.table_name, index=False)


def make_batch_response():

    pass


def main():
    alarmer = Alarmer()
    while True:
        alarmer.spin()
        time.sleep(10)


if __name__ == "__main__":
    main()
