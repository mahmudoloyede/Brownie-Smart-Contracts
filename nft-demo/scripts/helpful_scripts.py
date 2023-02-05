from brownie import (
    accounts,
    network,
    config,
    LinkToken,
    VRFCoordinatorMock,
    network,
    Contract,
)


LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache", "mainnet-fork"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def get_account(index=None, _id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if _id:
        return accounts.load(_id)
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed!")


def fund_with_link(contract_address, account=None, link_token=None, amount=10**17):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Funded Contract!")
    return tx
