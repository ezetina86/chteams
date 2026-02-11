"""UI components for the chteams utility using the rich library."""

from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live

console = Console()

BANNER = r"""
[bold purple]
   _____ _    _ _______ ______          __  __  _____ 
  / ____| |  | |__   __|  ____|   /\   |  \/  |/ ____|
 | |    | |__| |  | |  | |__     /  \  | \  / | (___  
 | |    |  __  |  | |  |  __|   / /\ \ | |\/| |\___ \ 
 | |____| |  | |  | |  | |____ / ____ \| |  | |____) |
  \_____|_|  |_|  |_|  |______/_/    \_\_|  |_|_____/ 
[/bold purple]
           [italic blue]Microsoft Teams Anti-Away Utility[/italic blue]
"""

def show_banner():
    """Displays the CHTEAMS ASCII banner."""
    console.print(BANNER)

def create_dashboard(status: str, uptime: str, last_act: str, interval: int) -> Panel:
    """Creates a dashboard panel with status information.

    Args:
        status: Current engine status.
        uptime: Formatted uptime string.
        last_act: Timestamp of the last interaction.
        interval: Configured interval in seconds.

    Returns:
        Panel: A rich Panel object containing the dashboard.
    """
    table = Table.grid(expand=True)
    table.add_column(style="bold cyan", justify="right")
    table.add_column(style="white", justify="left")

    table.add_row("Status: ", f"[bold green]{status}[/bold green]")
    table.add_row("Uptime: ", uptime)
    table.add_row("Last Action: ", last_act)
    table.add_row("Interval: ", f"{interval}s")

    return Panel(
        table,
        title="[bold white]Activity Dashboard[/bold white]",
        border_style="purple",
        subtitle="[dim]Press Ctrl+C to Exit[/dim]"
    )
