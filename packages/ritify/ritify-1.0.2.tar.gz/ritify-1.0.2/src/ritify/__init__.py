"""A rich console for Python"""

from ritify.rich.console import Console

print = Console().print

__all__ = ["Console", "print"]

# ----------------------------------------------------------------------
# |  Example Usage
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print(f"[bright_yellow]{"*".center(19)}[/]")
    print(f"[green]{"###".center(19)}[/]")
    print(f"[green]{"#####".center(19)}[/]")
    print(f"[green]{"#######".center(19)}[/]")
    print(f"[green]{"#########".center(19)}[/]")
    print(f"[green]{"###########".center(19)}[/]")
    print(f"[green]{"#############".center(19)}[/]")
    print(f"[green]{"###############".center(19)}[/]")
    print(f"[green]{"#################".center(19)}[/]")
    print(f"[sandy_brown]{"#".center(19)}[/]")
    print(f"[sandy_brown]{"#".center(19)}[/]")
    print(f"[sandy_brown]{"#".center(19)}[/]")
