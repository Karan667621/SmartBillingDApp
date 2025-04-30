import tkinter as tk
from tkinter import messagebox, simpledialog
import sys, os
import smtplib
from email.message import EmailMessage
import csv
import os
from web3 import Web3
import json

# ensure project root is on PYTHONPATH so `backend` package is found
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.web3_utils import w3, contract, account  # now resolvable

class RetailBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Billing System")
        self.root.geometry("1000x600")
        self.root.config(bg="#074463")

        # Web3 / contract objects
        self.w3 = w3
        self.contract = contract
        self.account = account

        # UI state
        self.entries = {}
        self.total_vars = {"Cosmetics": 0.0, "Snacks": 0.0, "Household": 0.0}

        # Main frame
        self.main_frame = tk.Frame(root, bg="#074463")
        self.main_frame.pack(fill="both", expand=True)

        # Detect blockchain connection
        if self.w3.is_connected():
            self.blockchain_status = "🟢 Blockchain Connected"
        else:
            self.blockchain_status = "🔴 Blockchain Disconnected"

        # Show the menu
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()

        title = tk.Label(self.main_frame, text="SMART BILLING", font=("Arial", 24, "bold"), bg="#074463", fg="white")
        title.pack(pady=20)

        status = tk.Label(self.main_frame, text=self.blockchain_status, font=("Arial", 10), bg="#074463", fg="lightgreen")
        status.pack()

        button_frame = tk.Frame(self.main_frame, bg="#074463")
        button_frame.pack(pady=40)

        tk.Button(button_frame, text="Create Bill", command=self.create_bill_page,
                  bg="#0E4D92", fg="white", font=("Arial", 14),
                  width=15, height=2).grid(row=0, column=0, padx=20, pady=10)

        tk.Button(button_frame, text="Search Bill", command=self.search_bill,
                  bg="#0E4D92", fg="white", font=("Arial", 14),
                  width=15, height=2).grid(row=0, column=1, padx=20, pady=10)

        tk.Button(button_frame, text="Delete Cust Info", command=self.delete_customer_info,
                  bg="#0E4D92", fg="white", font=("Arial", 14),
                  width=15, height=2).grid(row=0, column=2, padx=20, pady=10)

        tk.Button(button_frame, text="View All Invoices", command=self.view_all_blockchain_invoices,
                  bg="#00796B", fg="white", font=("Arial", 14),
                  width=30, height=2).grid(row=1, column=0, columnspan=3, pady=10)

        tk.Button(button_frame, text="Verify Blockchain", command=self.verify_on_blockchain,
                  bg="#00796B", fg="white", font=("Arial", 14),
                  width=20, height=2).grid(row=2, column=0, columnspan=3, pady=10)

        tk.Button(self.main_frame, text="Exit", command=self.root.quit,
                  bg="#D32F2F", fg="white", font=("Arial", 14),
                  width=15, height=2).pack(pady=30)

        badge = tk.Label(self.main_frame, text="🛡️ Secured by Ethereum Smart Contract",
                         font=("Arial", 9), bg="#074463", fg="white")
        badge.pack(side="bottom", pady=5)

    def verify_on_blockchain(self):
        bill_id = simpledialog.askstring("Verify Blockchain", "Enter Bill Number to Verify:")
        if not bill_id:
            return

        try:
            bill_no = int(bill_id)
            name, phone, total = contract.functions.getInvoice(bill_no).call()

            if name == "" and phone == "" and total == 0:
                messagebox.showinfo("Not Found", f"❌ Invoice #{bill_no} not on blockchain.")
            else:
                messagebox.showinfo(
                    "Blockchain Verified",
                    f"✅ Invoice #{bill_no} on Blockchain:\n"
                    f"• Name: {name}\n"
                    f"• Phone: {phone}\n"
                    f"• Total: £{total}"
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to verify invoice.\n{e}")

    def clear_frame(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    def create_bill_page(self):
        self.clear_frame()
        title = tk.Label(self.main_frame, text="RETAIL BILLING SYSTEM",
                         font=("Arial", 20, "bold"), bg="#074463", fg="white")
        title.pack(fill="x")

        # Customer Details
        cf = tk.LabelFrame(self.main_frame, text="Customer Details",
                           bg="#074463", fg="gold", font=("Arial", 12, "bold"))
        cf.pack(fill="x", padx=10, pady=5)

        self.customer_name = tk.StringVar()
        self.phone_number = tk.StringVar()
        self.bill_number = tk.StringVar()

        tk.Label(cf, text="Customer Name", bg="#074463", fg="white").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(cf, textvariable=self.customer_name).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(cf, text="Phone Number", bg="#074463", fg="white").grid(row=0, column=2, padx=10, pady=5)
        tk.Entry(cf, textvariable=self.phone_number).grid(row=0, column=3, padx=10, pady=5)

        tk.Label(cf, text="Bill Number", bg="#074463", fg="white").grid(row=0, column=4, padx=10, pady=5)
        tk.Entry(cf, textvariable=self.bill_number).grid(row=0, column=5, padx=10, pady=5)

        # Products Grid
        pf = tk.Frame(self.main_frame, bg="#074463")
        pf.pack(padx=10, pady=10)
        categories = ["Cosmetics", "Snacks", "Household"]
        items = {
            "Cosmetics": ["Cream", "Scent", "Hair Gel", "Lotion", "Body Wash", "Soap"],
            "Snacks": ["Ice Cream", "Cake", "Samosa", "Chips", "Smoothies", "Mixture"],
            "Household": ["Cleaners", "Vessels", "Mattresses", "Oils", "Grains", "Flour"]
        }
        prices = {
            "Cream": 4.5, "Scent": 20, "Hair Gel": 3, "Lotion": 5,
            "Body Wash": 6, "Soap": 1.2, "Ice Cream": 2.5, "Cake": 3,
            "Samosa": 1, "Chips": 0.8, "Smoothies": 3.5, "Mixture": 2.2,
            "Cleaners": 2.5, "Vessels": 12, "Mattresses": 60,
            "Oils": 5.5, "Grains": 3, "Flour": 1.2
        }

        self.entries.clear()
        self.prices = prices

        for idx, cat in enumerate(categories):
            lf = tk.LabelFrame(pf, text=f"{cat} Essentials",
                               bg="#074463", fg="gold", font=("Arial", 12, "bold"))
            lf.grid(row=0, column=idx, padx=10)
            for jdx, itm in enumerate(items[cat]):
                tk.Label(lf, text=itm, bg="#074463", fg="white")\
                    .grid(row=jdx, column=0, padx=5, pady=5, sticky="w")
                ent = tk.Entry(lf, width=8)
                ent.insert(0, "0")
                ent.grid(row=jdx, column=1, padx=5, pady=5)
                self.entries[itm] = ent

        # Bill area text
        baf = tk.Frame(pf, bg="#074463")
        baf.grid(row=0, column=3, padx=10)
        tk.Label(baf, text="Bill Area", bg="white").pack(fill="x")
        self.bill_area_text = tk.Text(baf, width=30, height=15)
        self.bill_area_text.pack()

        # Bill menu buttons
        bmf = tk.LabelFrame(self.main_frame, text="Bill Menu",
                            bg="#074463", fg="gold", font=("Arial", 12, "bold"))
        bmf.pack(fill="x", padx=10, pady=5)

        self.cosmetic_price = tk.StringVar()
        self.snack_price = tk.StringVar()
        self.household_price = tk.StringVar()

        tk.Label(bmf, text="Cosmetics Price", bg="#074463", fg="white")\
            .grid(row=0, column=0, padx=10)
        tk.Entry(bmf, textvariable=self.cosmetic_price).grid(row=0, column=1)

        tk.Label(bmf, text="Snacks Price", bg="#074463", fg="white")\
            .grid(row=0, column=2, padx=10)
        tk.Entry(bmf, textvariable=self.snack_price).grid(row=0, column=3)

        tk.Label(bmf, text="Household Price", bg="#074463", fg="white")\
            .grid(row=0, column=4, padx=10)
        tk.Entry(bmf, textvariable=self.household_price).grid(row=0, column=5)

        tk.Button(bmf, text="Total", bg="cadetblue", fg="white",
                  command=self.generate_invoice).grid(row=0, column=6, padx=10)
        tk.Button(bmf, text="Print", bg="cadetblue", fg="white",
                  command=self.choose_print_option).grid(row=0, column=7, padx=10)
        tk.Button(bmf, text="Clear", bg="cadetblue", fg="white",
                  command=self.create_bill_page).grid(row=0, column=8, padx=10)
        tk.Button(bmf, text="Back", bg="red", fg="white",
                  command=self.create_main_menu).grid(row=0, column=9, padx=10)

        tk.Label(self.main_frame, text="🛡️ Secured by Ethereum Smart Contract",
                 font=("Arial", 10), bg="#074463", fg="white")\
            .pack(side="bottom", pady=5)

    def generate_invoice(self):
        cosmetics_total = snacks_total = household_total = 0.0
        self.bill_area_text.delete('1.0', tk.END)

        # Print header
        self.bill_area_text.insert(tk.END,
            f"Bill No: {self.bill_number.get()}\n"
            f"Customer: {self.customer_name.get()}\n"
            f"Phone: {self.phone_number.get()}\n\n"
            "Items:\n----------------------------\n"
        )

        # Compute totals
        for itm, ent in self.entries.items():
            try:
                qty = int(ent.get())
                if qty > 0:
                    price = self.prices[itm]
                    line_total = price * qty
                    self.bill_area_text.insert(tk.END, f"{itm} x {qty} = £{line_total:.2f}\n")
                    if itm in ["Cream","Scent","Hair Gel","Lotion","Body Wash","Soap"]:
                        cosmetics_total += line_total
                    elif itm in ["Ice Cream","Cake","Samosa","Chips","Smoothies","Mixture"]:
                        snacks_total += line_total
                    else:
                        household_total += line_total
            except ValueError:
                continue

        total = cosmetics_total + snacks_total + household_total
        self.cosmetic_price.set(f"£{cosmetics_total:.2f}")
        self.snack_price.set(f"£{snacks_total:.2f}")
        self.household_price.set(f"£{household_total:.2f}")

        self.bill_area_text.insert(tk.END, f"\n----------------------------\nTotal = £{total:.2f}\n")

        # Send to blockchain
        try:
            bill_no = int(self.bill_number.get())
            name = self.customer_name.get()
            phone = self.phone_number.get()
            total_amt = int(total)

            tx_hash = contract.functions.logInvoice(
                bill_no, name, phone, total_amt
            ).transact({'from': account})
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            self.bill_area_text.insert(tk.END, f"🔗 Blockchain TX: {tx_hash.hex()[:10]}...\n")

            messagebox.showinfo(
                "Blockchain Save Successful!",
                f"✅ Invoice sent to blockchain\n\n"
                f"• Bill No: {bill_no}\n"
                f"• Name: {name}\n"
                f"• Phone: {phone}\n"
                f"• Total: £{total_amt}\n\n"
                f"🔗 TX: {tx_hash.hex()}\n"
                f"Block: {receipt.blockNumber}"
            )
        except Exception as e:
            self.bill_area_text.insert(tk.END, "❌ Blockchain log failed.\n")
            messagebox.showerror("Blockchain Error", f"Failed to save invoice.\n{e}")

    def choose_print_option(self):
        option = messagebox.askquestion("Print Option", "Email this invoice?")
        if option == 'yes':
            email = simpledialog.askstring("Customer Email", "Enter customer email:")
            if email:
                self.send_email(email)
        else:
            messagebox.showinfo("Print", "Simulated print complete.")

    def send_email(self, recipient):
        content = self.bill_area_text.get("1.0", tk.END)
        try:
            msg = EmailMessage()
            msg['Subject'] = f"Invoice #{self.bill_number.get()}"
            msg['From'] = "modipmindia008@gmail.com"
            msg['To'] = recipient
            msg.set_content(content)

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login("modipmindia008@gmail.com", "your-app-password")
                server.send_message(msg)

            messagebox.showinfo("Email Sent", f"Invoice emailed to {recipient}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email.\n{e}")

    def search_bill(self):
        self.clear_frame()

        frame = tk.Frame(self.main_frame, bg="#074463")
        frame.pack(pady=40)

        tk.Label(frame, text="Search Bill", font=("Arial", 20, "bold"),
                 bg="#074463", fg="white").pack(pady=10)

        input_frame = tk.Frame(frame, bg="#074463")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Bill Number", bg="#074463",
                 fg="white").grid(row=0, column=0, padx=5, pady=5)
        bill_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=bill_var).grid(row=0, column=1, padx=5, pady=5)

        def find_bill():
            bill_no = bill_var.get().strip()
            if not bill_no.isdigit():
                messagebox.showerror("Error", "Please enter a valid bill number.")
                return
            bill_id = int(bill_no)

            # Call your smart contract
            try:
                name, phone, total = self.contract.functions.getInvoice(bill_id).call()
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    "Blockchain query failed:\n"
                    "Could not call getInvoice().\n"
                    "Make sure Ganache (or your node) is running,\n"
                    "your contract is deployed at the configured address,\n"
                    "and your ABI matches."
                    f"\n\nDetails: {e}"
                )
                return

            if name == "" and phone == "" and total == 0:
                messagebox.showinfo("Not Found", f"No invoice #{bill_id} on blockchain.")
                return

            # Show exactly one result block
            result_frame = tk.Frame(frame, bg="#074463")
            result_frame.pack(pady=20)

            tk.Label(result_frame, text="Result:", font=("Arial", 14, "bold"),
                     bg="#074463", fg="gold").pack()

            result_text = tk.Text(result_frame, height=6, width=60)
            result_text.pack()
            result_text.insert(tk.END, f"Bill No: {bill_id}\n")
            result_text.insert(tk.END, f"Customer: {name}\n")
            result_text.insert(tk.END, f"Phone: {phone}\n")
            result_text.insert(tk.END, f"Total: £{total}\n")

            # Optionally display the TX hash you logged in blockchain_log.csv
            try:
                with open("blockchain_log.csv", newline="") as logf:
                    reader = csv.reader(logf)
                    next(reader)  # skip header
                    for row in reader:
                        if int(row[0]) == bill_id:
                            txh, blk = row[4], row[5]
                            result_text.insert(tk.END,
                                               f"🔗 TX: {txh[:10]}...  Block: {blk}\n")
                            break
            except FileNotFoundError:
                pass

        tk.Button(input_frame, text="Search", command=find_bill,
                  bg="cadetblue", fg="white")\
          .grid(row=0, column=2, padx=10)
        tk.Button(input_frame, text="Back", command=self.create_main_menu,
                  bg="red", fg="white")\
          .grid(row=0, column=3, padx=10)

        # bottom badge
        tk.Label(self.main_frame,
                 text="🛡️ Secured by Ethereum Smart Contract",
                 font=("Arial", 10), bg="#074463", fg="white")\
          .pack(side="bottom", pady=5)



    def delete_customer_info(self):
        self.clear_frame()
        frame = tk.Frame(self.main_frame, bg="#074463")
        frame.pack(pady=40)

        tk.Label(frame, text="Delete Bill", font=("Arial", 20, "bold"),
                 bg="#074463", fg="white").pack(pady=10)

        tk.Label(frame, text="⚡ Invoices are permanently stored on blockchain.\nDeletion not possible.",
                 font=("Arial", 14), bg="#074463", fg="lightgreen").pack(pady=20)

        tk.Button(frame, text="Back", command=self.create_main_menu,
                  bg="red", fg="white").pack(pady=20)

        tk.Label(self.main_frame, text="🛡️ Secured by Ethereum Smart Contract",
                 font=("Arial", 10), bg="#074463", fg="white")\
            .pack(side="bottom", pady=5)

    def view_all_blockchain_invoices(self):
        self.clear_frame()
        frame = tk.Frame(self.main_frame, bg="#074463")
        frame.pack(pady=40)

        tk.Label(frame, text="All Blockchain Invoices", font=("Arial", 20, "bold"),
                 bg="#074463", fg="white").pack(pady=10)

        controls = tk.Frame(frame, bg="#074463")
        controls.pack(pady=5)

        start_var = tk.StringVar(value="1")
        end_var   = tk.StringVar(value="500")

        tk.Label(controls, text="Start Bill No", bg="#074463", fg="white")\
            .grid(row=0, column=0, padx=5)
        tk.Entry(controls, textvariable=start_var, width=10)\
            .grid(row=0, column=1, padx=5)

        tk.Label(controls, text="End Bill No", bg="#074463", fg="white")\
            .grid(row=0, column=2, padx=5)
        tk.Entry(controls, textvariable=end_var, width=10)\
            .grid(row=0, column=3, padx=5)

        result_frame = tk.Frame(frame, bg="#074463")
        result_frame.pack(pady=20)

        result_text = tk.Text(result_frame, height=20, width=100)
        result_text.pack()

        def load_invoices():
            result_text.delete('1.0', tk.END)
            start_id = int(start_var.get())
            end_id   = int(end_var.get())
            found = False
            for bill_id in range(start_id, end_id + 1):
                try:
                    name, phone, total = contract.functions.getInvoice(bill_id).call()
                    if name or phone or total:
                        found = True
                        result_text.insert(tk.END,
                            f"Bill No: {bill_id}\n"
                            f"Customer: {name}\n"
                            f"Phone: {phone}\n"
                            f"Total: £{total}\n"
                            "--------------------------------\n"
                        )
                except:
                    break
            if not found:
                result_text.insert(tk.END, "No invoices found in this range.\n")

        tk.Button(controls, text="Load Invoices", command=load_invoices,
                  bg="green", fg="white").grid(row=0, column=4, padx=10)
        tk.Button(frame, text="Back", command=self.create_main_menu,
                  bg="red", fg="white").pack(pady=10)

        load_invoices()

if __name__ == "__main__":
    root = tk.Tk()
    app = RetailBillingSystem(root)
    root.mainloop()
