import json
from solcx import compile_standard, install_solc
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

print("installing Solidity Compiler....")
install_solc("0.6.0")
compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compile_sol, file)


# get bytecode
bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get ABI
abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to blockchain
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/8d3cf26388f545a79b343adcfad4d0f2")
)

# other parameters needed
chain_id = 4
my_address = "0x7EBdfCd5311DB5a699d76029CE58b60b9AAc8275"
private_key = os.getenv("PRIVATE_KEY")

# creating the contract in python with the ABI and Bytecode
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# another parameter needed (for building the transaction)
nonce = w3.eth.getTransactionCount(my_address)

# steps for transacting with blockchain (any type of transaction including deploying contract)
# 0. Create Contract
# 1. Build Transaction
# 2. Sign Transanctiom
# 3. Finally send transaction

# build transaction with chain_id, address and nonce (with created contract)c
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# sign transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# send transaction
print("Deploying Contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# to interact with contract we need:
#   1. Contract Address
#   3. Contract ABI

# with open("contract", "w") as file:
#    file.write(tx_receipt.contractAddress)

# with open("abi.json", "w") as file:
#    json.dump(abi, file)

simple_storage_interact = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# You have to specify call or transact
# call -> doesn't make a state change (call and expects return)
# transact -> make state change
print(f"Initial stored value is {simple_storage_interact.functions.retrieve().call()}")

store_transaction = simple_storage_interact.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

store_txn_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)

print("Updating stored value...")
store_txn_reciept = w3.eth.wait_for_transaction_receipt(store_txn_hash)
print("Updated!")
