from brownie import MyToken, accounts, config
from web3 import Web3


def deploy():
    initial = Web3.toWei(1000, "ether")
    account = accounts.add(config["wallets"]["from_key"])
    token = MyToken.deploy(initial, {"from": account}, publish_source=True)


def main():
    deploy()
