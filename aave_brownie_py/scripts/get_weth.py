from web3 import Web3
from scripts.helpful_scripts import get_account
from brownie import interface, config, network


def main():
    get_weth()


def get_weth():
    accout = get_account()
    weth = interface.IWETH(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": accout, "value": Web3.toWei(0.1, "ether")})
    tx.wait(1)
    print("Received 0.1 WETH")
    return tx
