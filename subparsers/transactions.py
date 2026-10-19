from datetime import datetime
from decimal import Decimal
from typing import Annotated

from models.transaction import Transaction
from repositories.json_repository import DataBase, save_db
from subparsers.parser import addparser


@addparser
def add_transaction(
    db: DataBase,
    sender: Annotated[str, "Name of the account to charge"],
    reciever: Annotated[str, "Receiver, such as a shop or service"],
    amount: Annotated[int, "Payment amount in the account's smallest currency unit"],
    budget_category: Annotated[str, "Category name of the existing budget to update"],
    details: Annotated[str, "Optional payment details"] = "",
) -> None:
    """Withdraw a payment, update its one selected budget, and save the transaction."""
    account = db["accounts"].get(sender)
    if account is None:
        raise ValueError(f"Account does not exist: {sender}")
    if not reciever.strip():
        raise ValueError("Receiver must not be empty")
    if amount <= 0:
        raise ValueError("Transaction amount must be positive")

    budgets = [
        budget
        for budget in db["budgets"]
        if budget.category.name == budget_category
    ]
    if len(budgets) != 1:
        raise ValueError(
            f"Expected exactly one existing budget for category "
            f"'{budget_category}', found {len(budgets)}"
        )
    budget = budgets[0]

    account.withdraw(amount)
    budget.spent_amount += Decimal(amount)
    db["transactions"].append(
        Transaction(
            sender=sender,
            reciever=reciever.strip(),
            amount=amount,
            details=details,
            transaction_time=datetime.now().astimezone().isoformat(timespec="seconds"),
            category=budget.category,
            budget=budget,
        )
    )
    save_db(db)


@addparser
def deposit(
    db: DataBase,
    account_name: Annotated[str, "Name of the account to top up"],
    amount: Annotated[int, "Deposit amount in the account's smallest currency unit"],
) -> None:
    """Deposit money into an existing account and save the database."""
    account = db["accounts"].get(account_name)
    if account is None:
        raise ValueError(f"Account does not exist: {account_name}")
    account.deposit(amount)
    save_db(db)


@addparser
def show_transactions(db: DataBase) -> None:
    """Print all recorded transactions."""
    for transaction in db["transactions"]:
        budget_name = (
            transaction.budget.category.name if transaction.budget is not None else "legacy"
        )
        print(
            f"{transaction.transaction_time}: {transaction.sender} -> "
            f"{transaction.reciever}, amount={transaction.amount}, "
            f"budget={budget_name}, details={transaction.details}"
        )
