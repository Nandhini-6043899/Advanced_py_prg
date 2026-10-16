"""
SET 1 - Q1: Bank Account Management System (OOP: classes, inheritance, polymorphism)
- Customer holds accounts.
- BankAccount (abstract base) -> SavingsAccount, CurrentAccount, each overrides withdraw rules
  and month-end processing (polymorphism).
- Bank handles deposit, withdraw, transfer.
"""
from abc import ABC, abstractmethod
from datetime import datetime


class InsufficientFundsError(Exception):
    pass


class Customer:
    def __init__(self, customer_id, name, phone):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def total_balance(self):
        return sum(a.balance for a in self.accounts)

    def __str__(self):
        return f"Customer {self.customer_id}: {self.name} ({len(self.accounts)} account(s))"


class BankAccount(ABC):
    def __init__(self, acc_no, owner, balance=0):
        self.acc_no = acc_no
        self.owner = owner
        self.balance = balance
        self.history = []
        owner.add_account(self)

    def _log(self, kind, amount):
        self.history.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), kind, amount, self.balance))

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount
        self._log("DEPOSIT", amount)

    @abstractmethod
    def min_balance(self):
        """Balance that must remain after a withdrawal (may be negative for overdraft)."""

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if self.balance - amount < self.min_balance():
            raise InsufficientFundsError(
                f"{self.account_type()} {self.acc_no}: balance {self.balance:.2f} insufficient for {amount:.2f}")
        self.balance -= amount
        self._log("WITHDRAW", amount)

    @abstractmethod
    def month_end(self):
        """Interest or charges applied at month-end."""

    def account_type(self):
        return self.__class__.__name__

    def statement(self):
        print(f"\nStatement for {self.account_type()} {self.acc_no} ({self.owner.name})")
        print(f"{'Time':<20}{'Type':<14}{'Amount':>12}{'Balance':>14}")
        for t, k, a, b in self.history:
            print(f"{t:<20}{k:<14}{a:>12,.2f}{b:>14,.2f}")

    def __str__(self):
        return f"{self.account_type()} #{self.acc_no} | {self.owner.name} | Balance: Rs {self.balance:,.2f}"


class SavingsAccount(BankAccount):
    RATE = 0.04  # annual

    def min_balance(self):
        return 1000  # minimum balance must be maintained

    def month_end(self):
        interest = self.balance * self.RATE / 12
        self.balance += interest
        self._log("INTEREST", interest)


class CurrentAccount(BankAccount):
    OVERDRAFT = 20000
    CHARGE = 100

    def min_balance(self):
        return -self.OVERDRAFT  # may go into overdraft

    def month_end(self):
        self.balance -= self.CHARGE
        self._log("SERVICE CHG", self.CHARGE)


class Bank:
    def __init__(self, name):
        self.name = name
        self.customers = {}
        self.accounts = {}
        self._next = 10001

    def add_customer(self, customer):
        self.customers[customer.customer_id] = customer

    def open_account(self, kind, customer, opening=0):
        cls = {"savings": SavingsAccount, "current": CurrentAccount}[kind]
        acc = cls(self._next, customer, opening)
        self.accounts[acc.acc_no] = acc
        self._next += 1
        return acc

    def transfer(self, from_no, to_no, amount):
        src, dst = self.accounts[from_no], self.accounts[to_no]
        src.withdraw(amount)       # raises if not allowed - nothing changes then
        dst.deposit(amount)
        return f"Transferred Rs {amount:,.2f} from #{from_no} to #{to_no}"


def demo():
    bank = Bank("Py Bank")
    asha, ravi = Customer(1, "Asha", "9876543210"), Customer(2, "Ravi", "9123456780")
    bank.add_customer(asha)
    bank.add_customer(ravi)
    s = bank.open_account("savings", asha, 5000)
    c = bank.open_account("current", ravi, 2000)

    print(s)
    print(c)
    s.deposit(2500)
    print(bank.transfer(s.acc_no, c.acc_no, 3000))
    c.withdraw(15000)  # overdraft allowed on current
    print(c)

    for label, fn in [("Savings below min balance", lambda: s.withdraw(5000)),
                      ("Negative deposit", lambda: s.deposit(-5)),
                      ("Beyond overdraft", lambda: c.withdraw(50000))]:
        try:
            fn()
        except (InsufficientFundsError, ValueError) as e:
            print(f"[Blocked] {label}: {e}")

    for acc in bank.accounts.values():
        acc.month_end()          # same call, different behaviour
    s.statement()
    c.statement()
    print("\nTotal balance (Asha):", asha.total_balance())
    print("Total balance (Ravi):", ravi.total_balance())


if __name__ == "__main__":
    demo()
