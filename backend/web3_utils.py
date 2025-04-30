from web3 import Web3
import json
import os
import sys

# --- Configure Connection ---
GANACHE_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "0x5CDAC278D5B242Df65A8fbe3214D95A8455A4C65"  # replace if redeployed

# --- Init Web3 ---
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
if not w3.is_connected():
    print("❌ Failed to connect to Ganache at", GANACHE_URL)
    sys.exit("Blockchain not connected.")

print("✅ Connected to Ganache:", GANACHE_URL)

# --- Load ABI ---
abi_path = os.path.join(os.path.dirname(__file__), "InvoiceLoggerABI.json")
if not os.path.exists(abi_path):
    sys.exit("❌ ABI file missing: InvoiceLoggerABI.json")

with open(abi_path, "r") as f:
    contract_abi = json.load(f)

# --- Set up contract ---
try:
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)
    print("✅ Contract loaded at address:", CONTRACT_ADDRESS)
except Exception as e:
    sys.exit(f"❌ Error loading contract: {e}")

# --- Get default account ---
try:
    account = w3.eth.accounts[0]
    print("✅ Using account:", account)
except Exception:
    sys.exit("❌ Failed to access Ganache accounts.")

# Expose for app use
__all__ = ["w3", "contract", "account"]
