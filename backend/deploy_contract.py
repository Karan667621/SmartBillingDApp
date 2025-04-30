import os
from web3 import Web3
from solcx import compile_standard, install_solc
import json

install_solc("0.8.0")

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
w3.eth.default_account = w3.eth.accounts[0]

# Load Solidity Contract
sol_path = os.path.join(os.path.dirname(__file__), "../contracts/InvoiceLogger.sol")
with open(sol_path, "r") as file:
    source_code = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"InvoiceLogger.sol": {"content": source_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

# Extract ABI and bytecode
abi = compiled_sol["contracts"]["InvoiceLogger.sol"]["InvoiceLogger"]["abi"]
bytecode = compiled_sol["contracts"]["InvoiceLogger.sol"]["InvoiceLogger"]["evm"]["bytecode"]["object"]

# Save ABI for frontend
abi_path = os.path.join(os.path.dirname(__file__), "InvoiceLoggerABI.json")
with open(abi_path, "w") as abi_file:
    json.dump(abi, abi_file)

# Deploy contract
InvoiceLogger = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = InvoiceLogger.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("✅ Contract deployed at:", tx_receipt.contractAddress)
