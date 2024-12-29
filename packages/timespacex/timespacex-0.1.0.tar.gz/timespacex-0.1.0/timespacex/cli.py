#!/usr/bin/env python3

import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from .analyzer import analyze_file

console = Console()

def main():
    parser = argparse.ArgumentParser(
        description='TimeSpaceX - Calculate time and space complexity of Python code'
    )
    parser.add_argument('file', help='Python file to analyze')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    args = parser.parse_args()

    if args.no_color:
        console.no_color = True

    results = analyze_file(args.file)
    
    if "error" in results:
        console.print(f"[red]Error: {results['error']}[/red]")
        sys.exit(1)

    console.print("\n[bold blue]Time & Space Complexity Analysis[/bold blue]")
    console.print("=" * 50)
    
    for func_name, analysis in results.items():
        # Create a title with the function name
        title = Text(f"Function: {func_name}", style="bold cyan")
        
        # Create the content with the complexity analysis
        content = Text()
        content.append(analysis['explanation'])
        
        # Create a panel with the analysis
        panel = Panel(
            content,
            title=title,
            border_style="blue",
            padding=(1, 2)
        )
        console.print(panel)
        console.print()

if __name__ == "__main__":
    main() 