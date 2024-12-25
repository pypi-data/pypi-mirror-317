from decimal import Decimal

def format_large_numbers(value, _):
    """
    Format numbers in trillions, billions, millions, or thousands with dollar sign.
    """
    if abs(value) == 0:
        return "$0"

    # Convert Decimal to float if necessary
    if isinstance(value, Decimal):
        value = float(value)

    prefix = "$"
    magnitude = abs(value)

    if magnitude >= 1e12:
        formatted = f"{prefix}{value / 1e12:.1f}T"
    elif magnitude >= 1e9:
        formatted = f"{prefix}{value / 1e9:.1f}B"
    elif magnitude >= 1e6:
        formatted = f"{prefix}{value / 1e6:.1f}M"
    elif magnitude >= 1e3:
        formatted = f"{prefix}{value / 1e3:.1f}K"
    else:
        formatted = f"{prefix}{value:.0f}"

    return formatted

# You can add other utility functions here that are used across your modules
