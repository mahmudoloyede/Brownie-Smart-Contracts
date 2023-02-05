from brownie import network, Box, ProxyAdmin, Contract, TransparentUpgradeableProxy
from scripts.helpful_scripts import (
    get_account,
    encode_function_data,
)


def test_proxy_delegates_calls():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    encoded_fuction = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        encoded_fuction,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    assert proxy_box.retrieve() == 0
    proxy_box.store(1, {"from": account})
    assert proxy_box.retrieve() == 1
