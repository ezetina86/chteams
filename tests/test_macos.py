from unittest.mock import MagicMock, patch
from chteams.macos import MacOSController
import subprocess
import pytest


def test_start_caffeinate_success():
    controller = MacOSController()
    with patch("subprocess.Popen") as mock_popen:
        mock_popen.return_value = MagicMock()
        assert controller.start_caffeinate() is True
        mock_popen.assert_called_with(["caffeinate", "-di"])


def test_start_caffeinate_not_found():
    controller = MacOSController()
    with patch("subprocess.Popen", side_effect=FileNotFoundError):
        assert controller.start_caffeinate() is False


def test_stop_caffeinate():
    controller = MacOSController()
    mock_proc = MagicMock()
    controller._caffeinate_proc = mock_proc
    controller.stop_caffeinate()
    mock_proc.terminate.assert_called_once()


def test_focus_teams_success():
    controller = MacOSController()
    with patch("subprocess.run") as mock_run:
        controller.focus_teams_and_interact()
        assert mock_run.called
        # Check that osascript was called
        args, kwargs = mock_run.call_args
        assert args[0][0] == "osascript"


def test_focus_teams_failure():
    controller = MacOSController()
    with patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "cmd", stderr=b"error"),
    ), pytest.raises(RuntimeError) as excinfo:
        controller.focus_teams_and_interact()
    assert "Failed to interact with Teams: error" in str(excinfo.value)


def test_get_frontmost_app():
    controller = MacOSController()
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="Terminal\n")
        assert controller.get_frontmost_app() == "Terminal"
        mock_run.assert_called_once()
