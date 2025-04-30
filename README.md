# 🧾 Retail Billing System (Blockchain DApp)

A fully functional **Retail Billing Application** with:
- 📦 Python Tkinter GUI frontend
- 🛡️ Ethereum Smart Contract backend
- 🔗 Web3.py integration
- 💾 Data stored directly on Blockchain (no local database)
- 🖨️ Invoice creation, printing, email, and blockchain verification

---

## 🚀 Features

| Feature                                | Status |
|----------------------------------------|:------:|
| Create Retail Bill                     | ✅     |
| Save Invoice to Blockchain             | ✅     |
| Search Invoice by Bill Number          | ✅     |
| Verify Invoice on Blockchain           | ✅     |
| View All Blockchain Invoices           | ✅     |
| Print and Save Invoice                 | ✅     |
| Blockchain Connection Indicator        | ✅     |
| Full DApp Version Control (GitHub)     | ✅     |
| Ethereum Security Badge                | ✅     |

---

## 🛠 Technologies Used

- **Python 3.11**
- **Tkinter** (GUI Framework)
- **Solidity 0.8.0** (Smart Contract)
- **Ganache** (Local Ethereum Blockchain)
- **Web3.py** (Blockchain-Python Connector)
- **Git** (Version Control)

---

## 🛡️ Smart Contract Overview

**Contract Name:** `InvoiceLogger`

**Functions:**
- `logInvoice(uint billId, string memory customerName, string memory phoneNumber, uint totalAmount)`
- `getInvoice(uint billId) public view returns (string memory, string memory, uint)`

✅ This ensures invoices are saved immutably to the blockchain.

---

## 📦 Project Structure

```
SmartBillingDApp/
├── backend/
│   ├── deploy_contract.py       # Script to compile & deploy the smart contract
│   ├── InvoiceLogger.sol        # Solidity source
│   ├── InvoiceLoggerABI.json    # Contract ABI
│   └── web3_utils.py            # Web3 setup & contract instance
├── frontend/
│   ├── main.py                  # Tkinter GUI & blockchain interaction
│   └── blockchain_log.csv       # Optional TX log
├── .gitignore                   # Git ignore settings
└── requirements.txt             # Python dependencies
```

---

## ⚙️ How to Run

1. Clone the repo and `cd` into it:
   ```bash
   git clone <your-repo-url>.git
   cd SmartBillingDApp
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start Ganache on port 7545:
   ```bash
   ganache-cli -p 7545
   ```

4. Deploy the contract:
   ```bash
   python backend/deploy_contract.py
   ```

5. Run the frontend GUI:
   ```bash
   python frontend/main.py
   ```
