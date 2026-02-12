"""Tests for the UI components of the chteams utility."""

from unittest.mock import patch, MagicMock
from chteams.ui import show_banner, create_dashboard, show_summary
from rich.panel import Panel

def test_show_banner():
    """Verifies that show_banner calls console.print."""
    with patch("chteams.ui.console.print") as mock_print:
        show_banner()
        mock_print.assert_called_once()

def test_create_dashboard():
    """Verifies that create_dashboard returns a Rich Panel."""
    panel = create_dashboard("Active", "00:01:00", "12:00:00", "30s", 240)
    assert isinstance(panel, Panel)
    assert "Activity Dashboard" in str(panel.title)
    # Just verify it's a Table object without checking internal string representation
    from rich.table import Table
    assert isinstance(panel.renderable, Table)

def test_show_summary():
    """Verifies that show_summary calls console.print with a summary panel."""
    with patch("chteams.ui.console.print") as mock_print:
        show_summary("00:05:00", 10)
        # Check that it was called multiple times (banner, panel, bye message)
        assert mock_print.call_count >= 3
