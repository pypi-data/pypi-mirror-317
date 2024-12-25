import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import timedelta
from decimal import Decimal

def format_large_numbers(value, _):
    """Format numbers in trillions, billions, millions, or thousands with dollar sign."""
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


def apply_chart_styles(ax, dates, closing_prices, company_name, start_date, end_date):
    """
    Apply reusable chart styles including grid, labels, and annotations.
    """
    # Set grid
    ax.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
    ax.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)

    # Format axes
    ax.set_xlabel('', fontsize=12, labelpad=10)
    ax.xaxis.set_label_position("bottom")
    ax.xaxis.set_tick_params(pad=2, labelbottom=True, bottom=True, labelsize=12, labelrotation=0)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator(2))

    ax.set_ylabel('Market Capitalization', fontsize=12, labelpad=10)
    ax.yaxis.set_label_position("left")
    ax.yaxis.set_major_formatter(FuncFormatter(format_large_numbers))  # Use custom formatting function
    ax.yaxis.set_tick_params(pad=2, labeltop=False, labelbottom=True, bottom=False, labelsize=12)

    # Remove spines
    ax.spines[['top', 'right', 'bottom']].set_visible(False)
    ax.spines['left'].set_linewidth(1.1)

    # Peak annotation
    max_value = max(closing_prices)
    max_idx = closing_prices.index(max_value)
    peak_y_position = max_value * 1.1  # Slightly above the peak
    ax.annotate(
        f'Peak: {format_large_numbers(max_value, None)}',  # Apply custom formatting
        xy=(dates[max_idx], max_value),
        xytext=(dates[max_idx] - timedelta(days=100), peak_y_position),
        ha='right', va='bottom', fontsize=10, fontweight='bold',
        bbox=dict(facecolor='lightgray', edgecolor='gray', alpha=0.7),
        arrowprops=dict(arrowstyle='-|>', connectionstyle="arc3,rad=-0.2")
    )

    # Low annotation
    min_value = min(closing_prices)
    min_idx = closing_prices.index(min_value)
    low_y_position = min_value * 0.9  # Slightly below the low
    ax.annotate(
        f'Low: {format_large_numbers(min_value, None)}',  # Apply custom formatting
        xy=(dates[min_idx], min_value),
        xytext=(dates[min_idx] + timedelta(days=100), low_y_position),
        ha='left', va='top', fontsize=10, fontweight='bold',
        bbox=dict(facecolor='lightgray', edgecolor='gray', alpha=0.7),
        arrowprops=dict(arrowstyle='-|>', connectionstyle="arc3,rad=0.2")
    )

    # Title and subtitle
    ax.set_title(f"{company_name} Market Cap ({start_date.year} - {end_date.year})", fontsize=14, fontweight='bold')
    ax.text(
        x=0.05, y=0.05,
        s=f"Source: Marketcap.Company | Data from {company_name}",
        transform=ax.transAxes, fontsize=10, alpha=0.7
    )


def plot_market_cap_chart(dates, closing_prices, company_name, start_date, end_date):
    """
    Function to plot market cap chart with reusable styles.
    """
    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=96)
    ax.plot(dates, closing_prices, color='#014f86', linestyle='-', linewidth=1.5)

    apply_chart_styles(ax, dates, closing_prices, company_name, start_date, end_date)

    return fig, ax
