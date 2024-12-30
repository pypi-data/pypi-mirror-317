from difflib import unified_diff

from rich.console import Console


def diff_files(file1, file2):
    # Read the files
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()

    # Compute the differences
    diff = unified_diff(
        file1_lines, file2_lines,
        fromfile=file1, tofile=file2,
        lineterm=""
    )

    # Create a console with forced color support
    console = Console(force_terminal=True)

    # Print the differences with colors
    for line in diff:
        line = line.rstrip()  # Remove trailing spaces or newlines
        if line.startswith('---') or line.startswith('+++'):
            console.print(line, style="bold")
        elif line.startswith('-'):
            # Apply red to the entire line
            console.print(f"[red]{line}[/red]")
        elif line.startswith('+'):
            # Apply green to the entire line
            console.print(f"[green]{line}[/green]")
        elif line.startswith('@@'):
            console.print(line, style="yellow")
        else:
            console.print(f"[dim]{line}[/dim]")  # Default style for unchanged lines