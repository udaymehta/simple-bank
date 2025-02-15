import gradio as gr
import uuid
import datetime


class BankAccount:
    def __init__(
        self, account_holder_name, initial_balance=0.0, account_type="Savings"
    ):
        if not isinstance(initial_balance, (int, float)):
            raise TypeError("Initial balance must be a number.")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        self.account_number = str(uuid.uuid4())
        self.account_holder_name = account_holder_name
        self.balance = initial_balance
        self.account_type = account_type
        self.transactions = []
        self.creation_date = datetime.date.today()

    def deposit(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Deposit amount must be a number.")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self.balance += amount
        self._add_transaction("Deposit", amount)
        return f"Deposited ${amount:.2f} 💰. New balance: ${self.balance:.2f}"

    def withdraw(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Withdrawal amount must be a number.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")

        self.balance -= amount
        self._add_transaction("Withdrawal", -amount)
        return f"Withdrew ${amount:.2f} 💸. New balance: ${self.balance:.2f}"

    def get_balance(self):
        return f"Current balance: ${self.balance:.2f} ⚖️"

    def get_account_details(self):
        details = f"Account Number: {self.account_number}\n"
        details += f"Account Holder: {self.account_holder_name}\n"
        details += f"Account Type: {self.account_type}\n"
        details += f"Balance: ${self.balance:.2f}\n"
        details += f"Creation Date: {self.creation_date}\n"
        return details

    def _add_transaction(self, transaction_type, amount):
        timestamp = datetime.datetime.now()
        self.transactions.append(
            {"timestamp": timestamp, "type": transaction_type, "amount": amount}
        )

    def get_transaction_history(self):
        if not self.transactions:
            return "No transactions yet."

        history = "-" * 30 + "\nTransaction History 📜:\n" + "-" * 30 + "\n"
        for transaction in self.transactions:
            history += (
                f"{transaction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - "
                f"{transaction['type']:<10}: ${transaction['amount']:>8.2f}\n"
            )
        history += "-" * 30
        return history


class BankingSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(
        self, account_holder_name, initial_balance=0.0, account_type="Savings"
    ):
        try:
            account = BankAccount(account_holder_name, initial_balance, account_type)
            self.accounts[account.account_number] = account
            return f"Account created successfully 🏦. Account number: {account.account_number}"
        except (TypeError, ValueError) as e:
            return f"Account creation failed: {e}"

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            return f"Account {account_number} deleted successfully 🗑️."
        else:
            return f"Account {account_number} not found."

    def list_all_accounts(self):
        if not self.accounts:
            return "No accounts in the system."

        all_accounts_details = (
            "-" * 30 + "\nList of All Accounts 🧾:\n" + "-" * 30 + "\n"
        )
        for account_number, account in self.accounts.items():
            all_accounts_details += account.get_account_details() + "-" * 30 + "\n"
        return all_accounts_details


bank_system = BankingSystem()


def create_account_ui(account_holder_name, initial_balance, account_type):
    return bank_system.create_account(
        account_holder_name, initial_balance, account_type
    )


def deposit_ui(account_number, amount):
    account = bank_system.get_account(account_number)
    if account:
        try:
            return account.deposit(amount)
        except (TypeError, ValueError) as e:
            return str(e)
    else:
        return "Account not found."


def withdraw_ui(account_number, amount):
    account = bank_system.get_account(account_number)
    if account:
        try:
            return account.withdraw(amount)
        except (TypeError, ValueError) as e:
            return str(e)
    else:
        return "Account not found."


def check_balance_ui(account_number):
    account = bank_system.get_account(account_number)
    if account:
        return account.get_balance()
    else:
        return "Account not found."


def get_account_details_ui(account_number):
    account = bank_system.get_account(account_number)
    if account:
        return account.get_account_details()
    else:
        return "Account not found."


def get_transaction_history_ui(account_number):
    account = bank_system.get_account(account_number)
    if account:
        return account.get_transaction_history()
    else:
        return "Account not found."


def list_all_accounts_ui():
    return bank_system.list_all_accounts()


def delete_account_ui(account_number):
    return bank_system.delete_account(account_number)


with gr.Blocks(
    theme=gr.themes.Citrus(
        font=[gr.themes.GoogleFont("Poppins"), "Arial", "sans-serif"],
        text_size=gr.themes.sizes.text_lg,
    )
) as iface:
    gr.Markdown("# Simple Banking System 🏦")

    with gr.Tab("Create Account ➕"):
        with gr.Row():
            account_holder_name_input = gr.Textbox(label="Account Holder Name")
            initial_balance_input = gr.Number(label="Initial Balance", value=0.0)
            account_type_dropdown = gr.Dropdown(
                ["Savings", "Checking"], label="Account Type", value="Savings"
            )
        create_account_button = gr.Button("Create Account ➕")
        create_account_output = gr.Textbox(label="Output")
        create_account_button.click(
            create_account_ui,
            inputs=[
                account_holder_name_input,
                initial_balance_input,
                account_type_dropdown,
            ],
            outputs=create_account_output,
        )

    with gr.Tab("Deposit 💰"):
        account_number_deposit_input = gr.Textbox(label="Account Number")
        deposit_amount_input = gr.Number(label="Deposit Amount")
        deposit_button = gr.Button("Deposit 💰")
        deposit_output = gr.Textbox(label="Output")
        deposit_button.click(
            deposit_ui,
            inputs=[account_number_deposit_input, deposit_amount_input],
            outputs=deposit_output,
        )

    with gr.Tab("Withdraw 💸"):
        account_number_withdraw_input = gr.Textbox(label="Account Number")
        withdraw_amount_input = gr.Number(label="Withdraw Amount")
        withdraw_button = gr.Button("Withdraw 💸")
        withdraw_output = gr.Textbox(label="Output")
        withdraw_button.click(
            withdraw_ui,
            inputs=[account_number_withdraw_input, withdraw_amount_input],
            outputs=withdraw_output,
        )

    with gr.Tab("Check Balance ⚖️"):
        account_number_balance_input = gr.Textbox(label="Account Number")
        check_balance_button = gr.Button("Check Balance ⚖️")
        check_balance_output = gr.Textbox(label="Balance")
        check_balance_button.click(
            check_balance_ui,
            inputs=[account_number_balance_input],
            outputs=check_balance_output,
        )

    with gr.Tab("Account Details ℹ️"):
        account_number_details_input = gr.Textbox(label="Account Number")
        account_details_button = gr.Button("Get Account Details ℹ️")
        account_details_output = gr.Textbox(label="Account Details")
        account_details_button.click(
            get_account_details_ui,
            inputs=[account_number_details_input],
            outputs=account_details_output,
        )

    with gr.Tab("Transaction History 📜"):
        account_number_history_input = gr.Textbox(label="Account Number")
        transaction_history_button = gr.Button("Show Transaction History 📜")
        transaction_history_output = gr.Textbox(label="Transaction History")
        transaction_history_button.click(
            get_transaction_history_ui,
            inputs=[account_number_history_input],
            outputs=transaction_history_output,
        )

    with gr.Tab("List All Accounts 🧾"):
        list_accounts_button = gr.Button("List All Accounts 🧾")
        list_accounts_output = gr.Textbox(label="All Accounts Details")
        list_accounts_button.click(
            list_all_accounts_ui, inputs=[], outputs=list_accounts_output
        )

    with gr.Tab("Delete Account 🗑️"):
        account_number_delete_input = gr.Textbox(label="Account Number to Delete")
        delete_account_button = gr.Button("Delete Account 🗑️")
        delete_account_output = gr.Textbox(label="Output")
        delete_account_button.click(
            delete_account_ui,
            inputs=[account_number_delete_input],
            outputs=delete_account_output,
        )

iface.launch(pwa=True)
