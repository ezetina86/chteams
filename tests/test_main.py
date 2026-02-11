"""Tests for the main entry point of the chteams utility."""

from unittest.mock import patch, MagicMock
from chteams.main import main, setup_logging


def test_setup_logging():
    """Verifies that logging is configured correctly."""
    with patch("logging.basicConfig") as mock_basic_config:
        setup_logging()
        mock_basic_config.assert_called_once()


def test_main_success():
    """Verifies the successful execution path of main."""
    with (
        patch("chteams.main.setup_logging"),
        patch("chteams.main.show_banner"),
        patch("chteams.main.MacOSController"),
        patch("chteams.main.ActivityEngine") as mock_engine_class,
        patch("chteams.main.show_summary") as mock_summary,
    ):
        mock_engine = MagicMock()
        mock_engine.run.return_value = ("00:01:00", 5)
        mock_engine_class.return_value = mock_engine

        main()

        mock_engine.run.assert_called_once()
        mock_summary.assert_called_with("00:01:00", 5)


def test_main_keyboard_interrupt():
    """Verifies that main handles KeyboardInterrupt gracefully."""
    with (
        patch("chteams.main.setup_logging"),
        patch("chteams.main.show_banner"),
        patch("chteams.main.MacOSController"),
        patch("chteams.main.ActivityEngine") as mock_engine_class,
        patch("sys.exit") as mock_exit,
    ):
        mock_engine = MagicMock()
        mock_engine.run.side_effect = KeyboardInterrupt
        mock_engine_class.return_value = mock_engine

        main()

        mock_exit.assert_called_with(0)