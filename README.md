# Bank_Managment_System

## Command-line interface

Run `python main.py --help` to see the registered commands. For example:

```sh
python main.py create_account savings bank_account
python main.py show_accounts
```

Commands are registered with `@addparser` from `subparsers.parser`. Annotate
the first command parameter with the database type; it is supplied by the CLI.
The remaining parameters become positional arguments. Use `Annotated` metadata
to provide help text and, optionally, a non-empty list of allowed choices.
`create_query()` builds the root `argparse` parser from the registered commands.

## Accounts, payments, and budgets

Deposit or pay using integer amounts in the account's smallest currency unit
(for example, `1000` is 10.00 when the account balance is displayed in hundredths):

```sh
python main.py create_account daily bank_account
python main.py deposit daily 10000
python main.py create_category groceries "Food and household items"
python main.py add_budget groceries 50000
python main.py add_transaction daily "Corner Shop" 1250 groceries "Weekly shop"
python main.py show_transactions
```

Create a category and its budget before recording a payment. Each new payment
must name exactly one existing budget by its category name; the amount is
withdrawn from the sender account and added to that budget's spent total.

## Logging

Application information and errors are written to `logs/bank_management.log`.
The file rotates at 1 MB and keeps up to five backup files. Command failures
are logged with their traceback and then re-raised so they remain visible to
the caller.
