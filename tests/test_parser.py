import argparse

import pytest

from subparsers import account_menegment, budgets, categories, transactions
from subparsers.parser import PARSERS, ParserArgument, addparser, create_query


def test_addparser_registers_command_metadata_and_returns_original_function():
    parsers_before = PARSERS.copy()

    def command(db, amount: int = 3):
        return db, amount

    try:
        assert addparser(command) is command
        spec = PARSERS["command"]
        assert spec.function is command
        assert spec.arguments == (
            ParserArgument(
                name="amount",
                argument_type=int,
                description=None,
                choices=None,
                default=3,
            ),
        )
    finally:
        PARSERS.clear()
        PARSERS.update(parsers_before)


def test_addparser_rejects_duplicate_or_missing_database_parameter():
    parsers_before = PARSERS.copy()

    def command(db):
        return db

    def no_parameters():
        return None

    try:
        addparser(command)
        with pytest.raises(ValueError, match="already registered"):
            addparser(command)
        with pytest.raises(TypeError, match="database argument"):
            addparser(no_parameters)
    finally:
        PARSERS.clear()
        PARSERS.update(parsers_before)


def test_addparser_requires_annotations_for_cli_arguments():
    parsers_before = PARSERS.copy()

    def command(db, value):
        return value

    try:
        with pytest.raises(TypeError, match="must be annotated"):
            addparser(command)
    finally:
        PARSERS.clear()
        PARSERS.update(parsers_before)


def test_create_query_parses_registered_command_arguments_and_defaults():
    parser = create_query()
    args = vars(
        parser.parse_args(
            ["add_transaction", "daily", "Shop", "125", "food"]
        )
    )

    assert args["command"] == "add_transaction"
    assert args["sender"] == "daily"
    assert args["amount"] == 125
    assert args["details"] == ""
    assert args["handler"] is transactions.add_transaction


def test_create_query_enforces_required_arguments_and_account_choices():
    parser = create_query()

    with pytest.raises(SystemExit):
        parser.parse_args(["deposit", "daily"])

    with pytest.raises(SystemExit):
        parser.parse_args(["create_account", "daily", "invalid"])


def test_registered_commands_include_all_application_handlers():
    assert PARSERS["create_account"].function is account_menegment.create_account
    assert PARSERS["show_accounts"].function is account_menegment.show_accounts
    assert PARSERS["add_budget"].function is budgets.add_budget
    assert PARSERS["create_category"].function is categories.create_category
    assert PARSERS["deposit"].function is transactions.deposit


def test_create_query_requires_a_registered_subcommand():
    with pytest.raises(SystemExit):
        create_query().parse_args([])
