import pytest

from accounts.bank_account import Bank_Account
from accounts.checking_account import Checking_Account
from accounts.savings_account import Savings_Account
from models.account import Account
from models.budget import Budget
from models.category import Category
from models.transaction import Transaction


def test_category_serializes_and_formats_its_fields():
    category = Category("food", "Groceries")

    assert category.save_data() == {"name": "food", "description": "Groceries"}
    assert "food" in str(category)
    assert "Groceries" in str(category)


def test_budget_serializes_decimal_amounts_as_strings():
    budget = Budget(Category("food", "Groceries"), 1000, 250)

    assert budget.save_data() == {
        "category": {"name": "food", "description": "Groceries"},
        "limit_amount": "1000",
        "spent_amount": "250",
    }
    assert "Limit: 1000" in str(budget)


def test_transaction_serialization_includes_budget_category_when_present():
    category = Category("food", "Groceries")
    budget = Budget(category, 1000, 250)
    transaction = Transaction(
        sender="daily",
        reciever="Shop",
        amount=250,
        details="Lunch",
        transaction_time="2026-01-01T12:00:00+00:00",
        category=category,
        budget=budget,
    )

    assert transaction.save_data() == {
        "sender": "daily",
        "reciever": "Shop",
        "amount": 250,
        "details": "Lunch",
        "transaction_time": "2026-01-01T12:00:00+00:00",
        "category": {"name": "food", "description": "Groceries"},
        "budget_category": "food",
    }


def test_legacy_transaction_serialization_omits_budget_category():
    transaction = Transaction(
        sender="daily",
        reciever="Shop",
        amount=250,
        details="Lunch",
        transaction_time="2026-01-01T12:00:00+00:00",
        category=Category("food", "Groceries"),
    )

    assert "budget_category" not in transaction.save_data()


def test_account_deposit_and_withdraw_update_balance():
    account = Account({"amount": 1000, "currency": "PLN"})

    account.deposit(250)
    assert account.balance == {"amount": 1250, "currency": "PLN"}

    account.withdraw(500)
    assert account.balance == {"amount": 750, "currency": "PLN"}


@pytest.mark.parametrize("amount", [0, -1, 1.5, "10"])
def test_account_rejects_invalid_deposit_and_withdraw_amounts(amount):
    account = Account({"amount": 1000, "currency": "PLN"})

    with pytest.raises(ValueError):
        account.deposit(amount)
    with pytest.raises(ValueError):
        account.withdraw(amount)


def test_account_rejects_withdrawal_above_balance_and_direct_balance_changes():
    account = Account({"amount": 100, "currency": "PLN"})

    with pytest.raises(ValueError, match="Not enough money"):
        account.withdraw(101)
    with pytest.raises(ValueError, match="direct"):
        account.balance = {"amount": 200, "currency": "PLN"}


@pytest.mark.parametrize(
    ("account_type", "account_id"),
    [
        (Bank_Account, "ACC123"),
        (Checking_Account, "CAC123"),
        (Savings_Account, "SAC123"),
    ],
)
def test_account_subclasses_restore_and_serialize_account_fields(
    account_type, account_id
):
    account = account_type.create_class_object(
        ID=account_id,
        balance={"amount": 1234, "currency": "PLN"},
    )

    assert isinstance(account, account_type)
    assert account.account_id == account_id
    assert account.balance == {
        "amount": 1234,
        "currency": "PLN",
    }
    if account_type is Bank_Account:
        assert account.get_keys() == {
            "ID": account_id,
            "balance": {"amount": 1234, "currency": "PLN"},
        }


def test_checking_account_applies_commission_before_withdrawal():
    account = Checking_Account(
        ID="CAC123", balance={"amount": 10000, "currency": "PLN"}
    )

    account.withdraw(1000)

    assert account.balance["amount"] == 8980


def test_checking_account_rejects_invalid_withdrawal_amount():
    account = Checking_Account(
        ID="CAC123", balance={"amount": 10000, "currency": "PLN"}
    )

    with pytest.raises(ValueError):
        account.withdraw(0)
