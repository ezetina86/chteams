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

def create_dashboard(status: str, uptime: str, last_act: str, next_act: str, interval: int, message: str = "") -> Panel:
    """Creates a dashboard panel with status information.

    Args:
        status: Current engine status.
        uptime: Formatted uptime string.
        last_act: Timestamp of the last interaction.
        next_act: Formatted time until next action.
        interval: Configured interval in seconds.
        message: Optional message to display in the dashboard.

    Returns:
        Panel: A rich Panel object containing the dashboard.
    """
    table = Table.grid(expand=True)
    table.add_column(style="bold cyan", justify="right")
    table.add_column(style="white", justify="left")

    status_color = "green"
    if status.upper() == "PAUSED":
        status_color = "bold yellow"
    elif "ERROR" in status.upper():
        status_color = "bold red"
    elif status.upper() == "SIMULATING ACTIVITY":
        status_color = "bold green"

    table.add_row("Status: ", f"[{status_color}]{status}[/{status_color}]")
    table.add_row("Uptime: ", uptime)
    table.add_row("Last Action: ", last_act)
    table.add_row("Next Action in: ", f"[bold yellow]{next_act}[/bold yellow]")
    table.add_row("Interval: ", f"{interval}s")
    
    if message:
        table.add_row("", "") # Spacer
        table.add_row("Note: ", f"[italic magenta]{message}[/italic magenta]")

    return Panel(
        table,
        title="[bold white]Activity Dashboard[/bold white]",
        border_style="purple",
        subtitle="[dim]Ctrl+P: Pause/Resume | Ctrl+C: Exit[/dim]"
    )

def show_summary(uptime: str, total_actions: int):
    """Displays a summary of the session activity.

    Args:
        uptime: Total time the script was running.
        total_actions: Number of interactions performed.
    """
    console.print("\n")
    table = Table.grid(expand=False, padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column(style="white")
    
    table.add_row("Total Uptime:", uptime)
    table.add_row("Total Interactions:", str(total_actions))
    
    console.print(Panel(
        table,
        title="[bold green]Session Summary[/bold green]",
        border_style="green",
        expand=False
    ))
    console.print("[bold italic blue]Bye! Stay active![/bold italic blue]\n")
