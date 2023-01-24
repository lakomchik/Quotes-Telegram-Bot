from web3 import Web3
import json
from decimal import Decimal
from utils.providers import BatchHTTPProvider
import utils.providers as providers
import utils.requests as requests
from decimal import Decimal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
import io


def div(a, b):
    return a / b


class Quoter:
    def __init__(self, uri) -> None:
        self.provider_uri = uri
        self.w3 = Web3(Web3.HTTPProvider(self.provider_uri))
        self.batch_w3 = providers.get_provider_from_uri(self.provider_uri, batch=True)
        sushiswap_adress = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
        uniswap_adress = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
        with open("const/json_abis/uniswapv2_factory.json", "r") as f:
            self.uniswap_abi = json.load(f)
        self.uniswap_contract = self.w3.eth.contract(
            address=sushiswap_adress, abi=self.uniswap_abi
        )
        with open("const/json_abis/erc20.json", "r") as f:
            self.erc20_abi = json.load(f)
        self.user_dict = {}
        with open("const/json_abis/uniswapv2_pair.json", "r") as f:
            self.uniswapv2_pair_abi = json.load(f)

    def regname(self, token_name, token_adress):
        self.user_dict[token_name] = token_adress

    def quote(
        self, foreign_token, domestic_token, start_block_id, end_block_id=0, step=1
    ):
        if len(foreign_token) < 10:
            foreign_token_adress = self.user_dict[foreign_token]
        else:
            foreign_token_adress = foreign_token
        if len(domestic_token) < 10:
            domestic_token_adress = self.user_dict[domestic_token]
        else:
            domestic_token_adress = domestic_token
        token_pair = self.uniswap_contract.functions.getPair(
            foreign_token_adress, domestic_token_adress
        ).call()
        pair_contract = self.w3.eth.contract(
            address=Web3.toChecksumAddress(token_pair), abi=self.uniswapv2_pair_abi
        )
        token0_adress = pair_contract.functions.token0().call()
        token1_adress = pair_contract.functions.token1().call()

        token0_contract = self.w3.eth.contract(
            address=Web3.toChecksumAddress(token0_adress), abi=self.erc20_abi
        )

        token1_contract = self.w3.eth.contract(
            address=Web3.toChecksumAddress(token1_adress), abi=self.erc20_abi
        )

        decimals0 = token0_contract.functions.decimals().call()
        decimals1 = token1_contract.functions.decimals().call()
        print(decimals0)
        print(decimals1)
        block = []

        if end_block_id == 0:
            end_block_id = start_block_id + 1

        idx = 0

        for block_id in range(start_block_id, end_block_id, step):
            block.append(
                requests.get_request_balanceof(
                    token0_adress, token_pair, block_id, idx * 2 + 0
                )
            )
            block.append(
                requests.get_request_balanceof(
                    token1_adress, token_pair, block_id, idx * 2 + 1
                )
            )
            idx += 1
        block_responses = self.batch_w3.make_batch_request(json.dumps(block))
        token0_amount = []
        token1_amount = []
        for i in range(len(block_responses) // 2):
            token0_amount.append(
                Decimal(int(block_responses[i * 2]["result"], base=16))
                / Decimal(10**decimals0)
            )
            token1_amount.append(
                Decimal(
                    (int(block_responses[i * 2 + 1]["result"], base=16))
                    / Decimal(10**decimals1)
                )
            )
        if domestic_token_adress == token1_adress:
            domestic_amount = token0_amount
            foreign_amount = token1_amount
        else:
            domestic_amount = token1_amount
            foreign_amount = token0_amount
        res = list(map(div, foreign_amount, domestic_amount))
        return res

    def make_plot(
        self, foreign_token, domestic_token, start_block_id, end_block_id, step
    ):
        data = self.quote(
            foreign_token, domestic_token, start_block_id, end_block_id, step
        )
        plt.locator_params(nbins=4)
        x_ax = list(map(str, [*range(start_block_id, end_block_id, step)]))
        my_dpi = 100
        plt.figure(figsize=(1000 / my_dpi, 700 / my_dpi), dpi=my_dpi)
        # plt.locator_params(axis="y", numticks=6)
        # plt.locator_params(axis="x", numticks=5)

        plt.style.use("dark_background")

        plt.plot(x_ax, data)
        plt.locator_params(axis="x", nbins=3)
        plt.xticks(rotation=45)
        plt.grid(c="cyan")

        plt.savefig("res.png")
        plt.draw()
        # data = self.quote(
        #     foreign_token, domestic_token, start_block_id, end_block_id, step
        # )
        # x_data = list(map(str, [*range(start_block_id, end_block_id, step)]))
        # figure, ax = plt.subplots()
        # ax.set_xticks(rotation=45)
        # ax.plot(x_data, data)

        # plt.savefig("res.png")

    def add_alert(self, foreign_token, domestic_token, quote_level, chat_id):
        # Collecting all data to form row in csv
        if len(foreign_token) < 10:
            foreign_name = foreign_token
            foreign_token_adress = self.user_dict[foreign_token]
        else:
            foreign_name = foreign_token
            foreign_token_adress = foreign_token

        if len(domestic_token) < 10:
            domestic_name = domestic_token
            domestic_token_adress = self.user_dict[domestic_token]
        else:
            domestic_name = domestic_token
            domestic_token_adress = domestic_token

        chat_id = chat_id
        level = quote_level
        pair_adress = self.uniswap_contract.functions.getPair(
            foreign_token_adress, domestic_token_adress
        ).call()

        pair_contract = self.w3.eth.contract(
            address=Web3.toChecksumAddress(pair_adress), abi=self.uniswapv2_pair_abi
        )

        token0_adress = pair_contract.functions.token0().call()
        token1_adress = pair_contract.functions.token1().call()

        token0_contract = self.w3.eth.contract(
            address=Web3.toChecksumAddress(token0_adress), abi=self.erc20_abi
        )

        token1_contract = self.w3.eth.contract(
            address=Web3.toChecksumAddress(token1_adress), abi=self.erc20_abi
        )
        decimals0 = token0_contract.functions.decimals().call()
        decimals1 = token1_contract.functions.decimals().call()

        # addin row to table
        alerts_table = pd.read_csv("alerts.csv")
        new_row = {
            "domestic_token": domestic_token_adress,
            "domestic_name": domestic_name,
            "foreign_token": foreign_token_adress,
            "foreign_name": foreign_name,
            "pair_adress": pair_adress,
            "token0_adress": token0_adress,
            "token1_adress": token1_adress,
            "level": level,
            "decimals0": decimals0,
            "decimals1": decimals1,
            "chat_id": chat_id,
        }
        alerts_table = alerts_table.append(new_row, ignore_index=True)
        alerts_table.to_csv("alerts.csv", index=False)
