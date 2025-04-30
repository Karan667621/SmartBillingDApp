// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InvoiceLogger {
    event InvoiceLogged(uint billNo, string customerName, string phone, uint totalAmount);

    struct Invoice {
        string customerName;
        string phone;
        uint totalAmount;
    }

    mapping(uint => Invoice) public invoices;

    function logInvoice(uint billNo, string memory name, string memory phone, uint totalAmount) public {
        invoices[billNo] = Invoice(name, phone, totalAmount);
        emit InvoiceLogged(billNo, name, phone, totalAmount);
    }

    function getInvoice(uint billNo) public view returns (string memory, string memory, uint) {
        Invoice memory inv = invoices[billNo];
        return (inv.customerName, inv.phone, inv.totalAmount);
    }
}
