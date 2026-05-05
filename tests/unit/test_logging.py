import logging as logging_module
from src.core.logging import configure_logging

def test_configure_logging_sets_expected_level():
    configure_logging("WARNING")
    root_logger = logging_module.getLogger()
    assert root_logger.level == logging_module.WARNING

def test_configure_logging_idempotent():
    configure_logging("INFO")
    configure_logging("DEBUG")
