from web3 import Web3

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/8d3cf26388f545a79b343adcfad4d0f2")
)

with open("abi.json", "r") as file:
    abi = file.read()

with open("contract", "r") as file:
    address = file.read()


contract = w3.eth.contract(
    address="0x6039348ad9203E60DaC8d13fC8190Efb37F7E58C", abi=abi
)

print(contract.functions.retrieve().call())
