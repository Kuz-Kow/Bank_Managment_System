from datetime import datetime
from decimal import Decimal

import pytest

from accounts.bank_account import Bank_Account
from models.budget import Budget
from models.category import Category
from models.transaction import Transaction
from subparsers import account_menegment, budgets, categories, transactions


def make_database():
    category = Category("food", "Groceries")
    return {
        "accounts": {
            "daily": Bank_Account(
                ID="ACC123", balance={"amount": 10000, "currency": "PLN"}
            )
        },
        "categories": [category],
        "transactions": [],
        "budgets": [],
    }


def test_create_account_creates_selected_type_and_persists(monkeypatch):
    database = make_database()
    saved = []
    monkeypatch.setattr(account_menegment, "save_db", saved.append)

    account_menegment.create_account(database, "savings", "savings_account")

    from accounts.savings_account import Savings_Account

    assert isinstance(database["accounts"]["savings"], Savings_Account)
    assert saved == [database]


def test_create_account_rejects_duplicate_name_and_unknown_type(monkeypatch):
    database = make_database()
    monkeypatch.setattr(
        account_menegment, "save_db", lambda _: pytest.fail("unexpected save")
    )

    with pytest.raises(ValueError, match="already exists"):
        account_menegment.create_account(database, "daily", "bank_account")
    with pytest.raises(ValueError, match="Unsupported account type"):
        account_menegment.create_account(database, "new", "unknown")


def test_show_accounts_prints_account_names(capsys):
    account_menegment.show_accounts(make_database())

    assert "daily :" in capsys.readouterr().out


def test_create_and_show_categories_persist_and_print(monkeypatch, capsys):
    database = make_database()
    saved = []
    monkeypatch.setattr(categories, "save_db", saved.append)

    categories.create_category(database, "travel", "Trips")

    assert database["categories"][-1] == Category("travel", "Trips")
    assert saved == [database]
    categories.show_categories(database)
    assert "travel" in capsys.readouterr().out


def test_add_budget_creates_and_persists_decimal_budget(monkeypatch):
    database = make_database()
    saved = []
    monkeypatch.setattr(budgets, "save_db", saved.append)

    budgets.add_budget(database, "food", 5000)

    assert database["budgets"] == [
        Budget(database["categories"][0], Decimal(5000), Decimal(0))
    ]
    assert saved == [database]


@pytest.mark.parametrize(
    "categories_for_budget",
    [[], [Category("food", "Other"), Category("food", "Groceries")]],
)
def test_add_budget_requires_one_matching_category(
    monkeypatch, categories_for_budget
):
    database = make_database()
    database["categories"] = categories_for_budget
    monkeypatch.setattr(budgets, "save_db", lambda _: pytest.fail("unexpected save"))

    with pytest.raises(ValueError, match="exactly one"):
        budgets.add_budget(database, "food", 5000)


def test_add_budget_rejects_duplicate_budget(monkeypatch):
    database = make_database()
    category = database["categories"][0]
    database["budgets"].append(Budget(category, Decimal(5000), Decimal(0)))
    monkeypatch.setattr(budgets, "save_db", lambda _: pytest.fail("unexpected save"))

    with pytest.raises(ValueError, match="already exists"):
        budgets.add_budget(database, "food", 6000)


def test_show_budgets_prints_budget(capsys):
    database = make_database()
    database["budgets"].append(
        Budget(database["categories"][0], Decimal(5000), Decimal(0))
    )

    budgets.show_budgets(database)

    assert "Limit: 5000" in capsys.readouterr().out


def test_deposit_updates_account_and_persists(monkeypatch):
    database = make_database()
    saved = []
    monkeypatch.setattr(transactions, "save_db", saved.append)

    transactions.deposit(database, "daily", 500)

    assert database["accounts"]["daily"].balance["amount"] == 10500
    assert saved == [database]


def test_deposit_rejects_missing_account(monkeypatch):
    database = make_database()
    monkeypatch.setattr(transactions, "save_db", lambda _: pytest.fail("unexpected save"))

    with pytest.raises(ValueError, match="does not exist"):
        transactions.deposit(database, "missing", 500)


def test_add_transaction_withdraws_updates_budget_and_persists(
    monkeypatch,
):
    database = make_database()
    category = database["categories"][0]
    budget = Budget(category, Decimal(5000), Decimal(0))
    database["budgets"].append(budget)
    saved = []
    monkeypatch.setattr(transactions, "save_db", saved.append)
    before = datetime.now().astimezone()

    transactions.add_transaction(
        database, "daily", "  Shop  ", 1200, "food", "Weekly groceries"
    )

    after = datetime.now().astimezone()
    transaction = database["transactions"][0]
    transaction_time = datetime.fromisoformat(transaction.transaction_time)
    assert database["accounts"]["daily"].balance["amount"] == 8800
    assert budget.spent_amount == Decimal(1200)
    assert transaction.sender == "daily"
    assert transaction.reciever == "Shop"
    assert transaction.category is category
    assert transaction.budget is budget
    assert (
        before.replace(microsecond=0)
        <= transaction_time
        <= after.replace(microsecond=0)
    )
    assert saved == [database]


@pytest.mark.parametrize(
    ("sender", "receiver", "amount", "budget_name", "error"),
    [
        ("missing", "Shop", 100, "food", "does not exist"),
        ("daily", "  ", 100, "food", "Receiver"),
        ("daily", "Shop", 0, "food", "positive"),
        ("daily", "Shop", 100, "missing", "exactly one"),
    ],
)
def test_add_transaction_validates_inputs_without_saving(
    monkeypatch, sender, receiver, amount, budget_name, error
):
    database = make_database()
    database["budgets"].append(
        Budget(database["categories"][0], Decimal(5000), Decimal(0))
    )
    monkeypatch.setattr(transactions, "save_db", lambda _: pytest.fail("unexpected save"))

    with pytest.raises(ValueError, match=error):
        transactions.add_transaction(
            database, sender, receiver, amount, budget_name
        )

    assert database["transactions"] == []


def test_show_transactions_prints_transactions(capsys):
    database = make_database()
    database["transactions"].append(
        Transaction(
            sender="daily",
            reciever="Shop",
            amount=250,
            details="Lunch",
            transaction_time="2026-01-01T12:00:00+00:00",
            category=database["categories"][0],
        )
    )

    transactions.show_transactions(database)

    output = capsys.readouterr().out
    assert "daily -> Shop" in output
    assert "budget=legacy" in output
