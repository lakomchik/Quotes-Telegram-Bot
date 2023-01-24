import argparse
from utils.providers import get_provider_from_uri
import pandas as pd


parser = argparse.ArgumentParser(
    prog="Alerts Handler",
)
parser.add_argument("--bot-token", type=str, default=None, required=True)
parser.add_argument("--alerts-db", type=str, default=None, required=True)
parser.add_argument("--provider-uri", type=str, default=None, required=True)
args = parser.parse_args()


# YOUR CODE GOES HERE
