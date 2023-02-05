from brownie import (
    accounts,
    config,
    network,
    Contract,
)

LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development", "ganache-local", "mainnet-fork"]
FORKED_LOCAL_ENVIRONMENT = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None, i_d=None):
    if index:
        return accounts[index]
    if i_d:
        return accounts.load(i_d)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT
        or network.show_active() in FORKED_LOCAL_ENVIRONMENT
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])
