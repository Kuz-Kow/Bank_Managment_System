import json
from decimal import Decimal

import pytest

from accounts.bank_account import Bank_Account
from models.budget import Budget
from models.category import Category
from models.transaction import Transaction
from repositories import json_repository


def test_load_db_returns_empty_database_when_file_is_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(json_repository, "DB_PATH", tmp_path / "missing.json")

    assert json_repository.load_db() == {
        "accounts": {},
        "categories": [],
        "transactions": [],
        "budgets": [],
    }


def test_save_and_load_db_round_trip_preserves_objects_and_budget_links(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(json_repository, "DB_PATH", tmp_path / "db.json")
    category = Category("food", "Groceries")
    budget = Budget(category, Decimal("5000"), Decimal("250"))
    transaction = Transaction(
        sender="daily",
        reciever="Shop",
        amount=250,
        details="Groceries",
        transaction_time="2026-01-01T12:00:00+00:00",
        category=category,
        budget=budget,
    )
    database = {
        "accounts": {
            "daily": Bank_Account(
                ID="ACC123", balance={"amount": 10000, "currency": "PLN"}
            )
        },
        "categories": [category],
        "transactions": [transaction],
        "budgets": [budget],
    }

    json_repository.save_db(database)
    loaded = json_repository.load_db()

    assert loaded["accounts"]["daily"].balance == {
        "amount": 10000,
        "currency": "PLN",
    }
    assert loaded["categories"] == [category]
    assert loaded["budgets"] == [budget]
    assert loaded["transactions"][0] == transaction
    assert loaded["transactions"][0].budget is loaded["budgets"][0]
    assert not list(tmp_path.glob(".db.json.*.tmp"))


@pytest.mark.parametrize(
    ("account_id", "message"),
    [
        ("bad", "Invalid account ID"),
        ("XYZ123", "Unsupported account type prefix"),
    ],
)
def test_load_db_rejects_invalid_account_ids(
    tmp_path, monkeypatch, account_id, message
):
    path = tmp_path / "db.json"
    path.write_text(
        json.dumps(
            {
                "accounts": {"daily": {"ID": account_id, "balance": {}}},
                "categories": [],
                "transactions": [],
                "budgets": [],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(json_repository, "DB_PATH", path)

    with pytest.raises(ValueError, match=message):
        json_repository.load_db()


def test_find_budget_requires_one_matching_category():
    category = Category("food", "Groceries")
    budget = Budget(category, Decimal(5000), Decimal(0))

    assert json_repository._find_budget([budget], "food") is budget

    with pytest.raises(ValueError, match="found 0"):
        json_repository._find_budget([], "food")
    with pytest.raises(ValueError, match="found 2"):
        json_repository._find_budget([budget, budget], "food")
