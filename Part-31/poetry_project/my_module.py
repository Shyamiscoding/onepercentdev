def print_separator(title):
    """Prints a nice visual separator in the terminal."""
    print(f"\n{'=' * 10} {title} {'=' * 10}\n")

def format_currency(amount):
    """Format a number as Indian Rupee currency."""
    return f"₹{amount:,.2f}"

def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}! Welcome to the project."


if __name__ == "__main__":
    print_separator("Module Test")
    print(greet("Shyam"))
    print(format_currency(150000))
    print("\nThis only runs when you execute: python my_module.py")
