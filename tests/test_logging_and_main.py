import argparse
import logging

import pytest
from logging.handlers import RotatingFileHandler

import logger_config
import main


@pytest.fixture
def isolated_root_logger():
    root_logger = logging.getLogger()
    previous_level = root_logger.level
    previous_handlers = root_logger.handlers[:]
    for handler in previous_handlers:
        root_logger.removeHandler(handler)

    yield root_logger

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()
    for handler in previous_handlers:
        root_logger.addHandler(handler)
    root_logger.setLevel(previous_level)


def test_configure_logging_adds_one_rotating_handler_and_is_idempotent(
    tmp_path, monkeypatch, isolated_root_logger
):
    monkeypatch.setattr(logger_config, "LOG_DIRECTORY", tmp_path)
    monkeypatch.setattr(logger_config, "LOG_FILE", tmp_path / "bank.log")

    logger_config.configure_logging()
    logger_config.configure_logging()

    handlers = [
        handler
        for handler in isolated_root_logger.handlers
        if handler.name == "bank_management_rotating_file"
    ]
    assert len(handlers) == 1
    assert isinstance(handlers[0], RotatingFileHandler)
    assert handlers[0].maxBytes == logger_config.MAX_LOG_SIZE
    assert handlers[0].backupCount == logger_config.BACKUP_COUNT
    assert handlers[0].encoding == "utf-8"


def test_main_runs_parsed_handler_with_loaded_database(monkeypatch):
    database = {"accounts": {}, "categories": [], "transactions": [], "budgets": []}
    calls = []
    handler = lambda db, name: calls.append((db, name))
    parser = argparse.ArgumentParser()
    parser.parse_args = lambda: argparse.Namespace(
        handler=handler, command="sample", name="value"
    )
    monkeypatch.setattr(main, "configure_logging", lambda: None)
    monkeypatch.setattr(main, "create_query", lambda: parser)
    monkeypatch.setattr(main, "load_db", lambda: database)

    main.main()

    assert calls == [(database, "value")]


def test_main_logs_and_reraises_handler_errors(monkeypatch, caplog):
    parser = argparse.ArgumentParser()
    parser.parse_args = lambda: argparse.Namespace(
        handler=lambda db: (_ for _ in ()).throw(RuntimeError("failed")),
        command="sample",
    )
    monkeypatch.setattr(main, "configure_logging", lambda: None)
    monkeypatch.setattr(main, "create_query", lambda: parser)
    monkeypatch.setattr(main, "load_db", lambda: {})

    with caplog.at_level(logging.ERROR, logger=main.__name__):
        with pytest.raises(RuntimeError, match="failed"):
            main.main()

    assert "Command failed: sample" in caplog.text
