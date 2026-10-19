# Bank Management System

A lightweight, command-line banking and personal-finance application written in
Python. It lets you manage accounts, record deposits and payments, organize
spending with categories and budgets, and persist your data locally as JSON.

The project is designed as a small, easy-to-explore example of a Python
application with a command-line interface, domain models, and a JSON
repository.

## Features

- Create bank, checking, and savings accounts.
- Deposit funds and view the accounts stored in the database.
- Create spending categories and assign budgets to them.
- Record payments against an account and a category budget.
- Persist accounts, categories, budgets, and transactions in `db.json`.
- Log application activity and errors to a rotating log file.

## Requirements

- Python 3.11 or later.
- No third-party packages are required to run the application.
- `pytest` is required to run the test suite.

## Getting started

Clone the repository and change into the project directory, then check the
available commands:

```sh
python main.py --help
```

The database is created in the project directory the first time a command
changes data. It is stored in `db.json`, which is intentionally excluded from
version control.

## Usage

Commands use hyphens in their names. Account type arguments use the values
`bank_account`, `checking_account`, or `savings_account`.

### Create an account and deposit funds

```sh
python main.py create-account daily bank_account
python main.py deposit daily 10000
python main.py show-accounts
```

Money amounts are entered as integers in the currency's smallest unit. For
example, `10000` represents `100.00` when displayed as a PLN balance.

### Create a category and budget

```sh
python main.py create-category groceries "Food and household items"
python main.py add-budget groceries 50000
python main.py show-categories
python main.py show-budgets
```

Create the category before its budget. The budget amount is also expressed in
the smallest currency unit.

### Record and view a payment

```sh
python main.py add-transaction daily "Corner Shop" 1250 groceries "Weekly shop"
python main.py show-transactions
```

Each payment must refer to exactly one existing budget by category name. The
payment amount is withdrawn from the sender's account and added to the
budget's spent total. The receiver name cannot be blank, and the account must
have enough funds. A payment's details are optional:

```sh
python main.py add-transaction daily "Coffee Shop" 450 groceries
```

The budget limit is stored and displayed, but currently does not prevent
payments from exceeding that limit.

## Commands

| Command | Description |
| --- | --- |
| `create-account <name> <type>` | Create a bank, checking, or savings account. |
| `show-accounts` | List the saved accounts and balances. |
| `deposit <account> <amount>` | Deposit a positive amount into an account. |
| `create-category <name> <description>` | Create a spending category. |
| `show-categories` | List the saved categories. |
| `add-budget <category> <limit>` | Create a budget for an existing category. |
| `show-budgets` | List the saved budgets and spending totals. |
| `add-transaction <sender> <receiver> <amount> <budget-category> [details]` | Record a payment against an account and budget. |
| `show-transactions` | List recorded payments. |

Run `python main.py <command> --help` for command-specific argument help.

## Data and logging

- **Database:** `db.json` in the current working directory. The file is
  generated and updated when data-changing commands run.
- **Logs:** `logs/bank_management.log` in the project directory. The log
  rotates at 1 MB and keeps up to five backup files.

## Running the tests

Install pytest if it is not already available:

```sh
python -m pip install pytest
```

Run the full test suite from the project directory:

```sh
python -m pytest
```

The tests use temporary files for database operations and do not require
modifying your local `db.json`.

## Project layout

```text
accounts/       Account types and account behavior
models/         Account, category, budget, and transaction models
repositories/   JSON persistence
subparsers/     CLI commands and argument parser
utils/          Money-related utilities
tests/          Automated tests
main.py         Application entry point
logger_config.py Logging configuration
```

## Extending the CLI

CLI commands are registered with the `@addparser` decorator from
`subparsers.parser`. The first command parameter receives the loaded database;
the remaining parameters become command-line arguments. Use type annotations
to define argument types and `Annotated` metadata to provide help text or
allowed choices. Registered command names are derived from function names,
with underscores converted to hyphens.
