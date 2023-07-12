class BankAccount:
    def __init__(self, account_number, initial_balance):
        self.account_number = account_number
        self.balance = initial_balance
        self.transaction_history = []

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposited: {amount}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawn: {amount}")
        else:
            print("Insufficient funds!")

    def transfer(self, amount, recipient_account):
        if self.balance >= amount:
            self.balance -= amount
            recipient_account.deposit(amount)
            self.transaction_history.append(f"Transferred: {amount} to account {recipient_account.account_number}")
        else:
            print("Insufficient funds!")

    def check_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transaction_history


class Bank:
    def __init__(self):
        self.accounts = {}
        self.total_balance = 0
        self.total_loan_amount = 0
        self.loan_feature_enabled = True

    def create_account(self, account_number, initial_balance):
        if account_number in self.accounts:
            print("Account already exists!")
        else:
            self.accounts[account_number] = BankAccount(account_number, initial_balance)
            self.total_balance += initial_balance
            print("Account created successfully!")

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def loan(self, account_number):
        if not self.loan_feature_enabled:
            print("Loan feature is currently disabled by the admin.")
            return

        account = self.get_account(account_number)
        if account:
            loan_amount = account.balance * 2
            account.deposit(loan_amount)
            self.total_loan_amount += loan_amount
            print(f"Loan of {loan_amount} credited to account {account_number}")
        else:
            print("Account not found!")

    def print_transaction_history(self, account_number):
        account = self.get_account(account_number)
        if account:
            history = account.get_transaction_history()
            print(f"Transaction history for account {account_number}:")
            for transaction in history:
                print(transaction)
        else:
            print("Account not found!")

    def get_total_balance(self):
        return self.total_balance

    def get_total_loan_amount(self):
        return self.total_loan_amount

    def enable_loan_feature(self):
        self.loan_feature_enabled = True
        print("Loan feature enabled.")

    def disable_loan_feature(self):
        self.loan_feature_enabled = False
        print("Loan feature disabled.")


class Admin:
    def __init__(self, bank):
        self.bank = bank

    def create_account(self, account_number, initial_balance):
        self.bank.create_account(account_number, initial_balance)

    def check_total_balance(self):
        return self.bank.get_total_balance()

    def check_total_loan_amount(self):
        return self.bank.get_total_loan_amount()

    def enable_loan_feature(self):
        self.bank.enable_loan_feature()

    def disable_loan_feature(self):
        self.bank.disable_loan_feature()


class User:
    def __init__(self, bank, account_number):
        self.bank = bank
        self.account_number = account_number

    def deposit(self, amount):
        account = self.bank.get_account(self.account_number)
        if account:
            account.deposit(amount)
            print(f"Amount {amount} deposited successfully.")
        else:
            print("Account not found!")

    def withdraw(self, amount):
        account = self.bank.get_account(self.account_number)
        if account:
            if account.balance >= amount:
                account.withdraw(amount)
                print(f"Amount {amount} withdrawn successfully.")
            else:
                print("Insufficient funds!")
        else:
            print("Account not found!")

    def transfer(self, amount, recipient_account_number):
        account = self.bank.get_account(self.account_number)
        recipient_account = self.bank.get_account(recipient_account_number)
        if account and recipient_account:
            if account.balance >= amount:
                account.transfer(amount, recipient_account)
                print(f"Amount {amount} transferred to account {recipient_account_number} successfully.")
            else:
                print("Insufficient funds!")
        else:
            print("One or both accounts not found!")

    def check_balance(self):
        account = self.bank.get_account(self.account_number)
        if account:
            return account.check_balance()
        else:
            print("Account not found!")

    def get_transaction_history(self):
        account = self.bank.get_account(self.account_number)
        if account:
            return account.get_transaction_history()
        else:
            print("Account not found!")


# Example usage:

bank = Bank()
admin = Admin(bank)

# Create accounts (Admin)
admin.create_account("123456789", 1000)
admin.create_account("987654321", 5000)

# Deposit money (User)
user1 = User(bank, "123456789")
user1.deposit(2000)

# Withdraw money (User)
user1.withdraw(500)
user1.withdraw(3000)  # Insufficient funds!

# Transfer money (User)
user2 = User(bank, "987654321")
user1.transfer(800, user2.account_number)

# Check balance (User)
print("User 1 balance:", user1.check_balance())
print("User 2 balance:", user2.check_balance())

# Get transaction history (User)
print("User 1 transaction history:", user1.get_transaction_history())

# Take a loan (User)
bank.loan(user1.account_number)
print("User 1 balance after loan:", user1.check_balance())

# Admin functionalities
print("Total bank balance:", admin.check_total_balance())
print("Total loan amount:", admin.check_total_loan_amount())

admin.disable_loan_feature()
bank.loan(user2.account_number)  # Loan feature disabled


# admin.enable_loan_feature()
# bank.loan(user1.account_number)  # enable loan feature