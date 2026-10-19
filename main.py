import logging

import subparsers.account_menegment
import subparsers.budgets
import subparsers.categories
import subparsers.transactions
from logger_config import configure_logging
from repositories.json_repository import load_db
from subparsers.parser import create_query


logger = logging.getLogger(__name__)


def main() -> None:
    """Parse the CLI command and run it with the loaded database."""
    configure_logging()
    command_name = None
    try:
        parser = create_query()
        arguments = vars(parser.parse_args())
        handler = arguments.pop("handler")
        command_name = arguments.pop("command")
        logger.info("Executing command: %s", command_name)
        handler(load_db(), **arguments)
        logger.info("Command completed successfully: %s", command_name)
    except SystemExit as error:
        if error.code not in (None, 0):
            logger.error("Command-line parsing exited with status %s", error.code)
        raise
    except Exception:
        if command_name is None:
            logger.exception("Application failed before command execution")
        else:
            logger.exception("Command failed: %s", command_name)
        raise


if __name__ == "__main__":
    main()
