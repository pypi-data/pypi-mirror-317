import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import timedelta, datetime
from decimal import Decimal
from typing import Optional, Dict, Any, Tuple, List
from dataclasses import dataclass


@dataclass
class ChartConfig:
    """Configuration class for chart customization"""
    company_name: str
    metric_name: str = "Market Capitalization"
    metric_prefix: str = "$"  # Currency symbol or other prefix
    subtitle_template: str = "{company}'s historical {metric} trends over the years."
    title_template: str = "{company} {metric} Growth ({start_year} - {end_year})"
    source_template: str = "Source: Marketcap.Company | Data derived from {company}'s financial reports"
    peak_label: str = "Peak {metric}:"
    low_label: str = "Lowest {metric}:"
    latest_label: str = "Latest {metric}:"
    colors: Dict[str, str] = None
    annotation_style: Dict[str, Any] = None

    def __post_init__(self):
        if self.colors is None:
            self.colors = {
                'line': '#014f86',
                'grid': '#DAD8D7',
                'header_line': '#E3120B',
                'annotation_box': '#f5f5f5',
                'annotation_edge': '#36454F',
                'latest_point': 'red'
            }

        if self.annotation_style is None:
            self.annotation_style = {
                'fontsize': 10,
                'fontweight': 'bold',
                'fontname': 'DejaVu Sans',
                'bbox': {
                    'facecolor': '#f5f5f5',
                    'edgecolor': '#36454F',
                    'alpha': 0.9,
                    'pad': 6
                },
                'arrowprops': {
                    'arrowstyle': '-|>',
                    'facecolor': '#36454F',
                    'edgecolor': '#36454F',
                    'connectionstyle': "arc3,rad=-0.2",
                    'linewidth': 1.2
                }
            }


def format_large_numbers(value: float, _, prefix: str = "$") -> str:
    """Format numbers in trillions, billions, millions, or thousands with custom prefix."""
    if abs(value) == 0:
        return f"{prefix}0"

    # Convert Decimal to float if necessary
    if isinstance(value, Decimal):
        value = float(value)

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


def create_custom_formatter(prefix: str) -> FuncFormatter:
    """Create a custom formatter with the specified prefix"""
    return FuncFormatter(lambda x, p: format_large_numbers(x, p, prefix))


def plot_market_cap_chart(
        dates: List[datetime],
        values: List[float],
        config: ChartConfig
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Function to plot chart with fully customizable styling.
    """
    # Create figure with adjusted margins
    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=96)
    plt.subplots_adjust(left=0.12, bottom=0.2, right=0.95, top=0.85)

    # Plot main line
    line = ax.plot(dates, values,
                   color=config.colors['line'],
                   linestyle='-',
                   linewidth=1.5,
                   zorder=2)[0]

    # Grid settings
    ax.grid(which="major", axis='x', color=config.colors['grid'], alpha=0.5, zorder=1)
    ax.grid(which="major", axis='y', color=config.colors['grid'], alpha=0.5, zorder=1)

    # Axis formatting
    ax.set_xlabel('', fontsize=12, labelpad=10)
    ax.xaxis.set_label_position("bottom")
    ax.xaxis.set_tick_params(pad=2, labelbottom=True, bottom=True, labelsize=12, labelrotation=0)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator(2))

    ax.set_ylabel(config.metric_name, fontsize=12, labelpad=10)
    ax.yaxis.set_label_position("left")
    ax.yaxis.set_major_formatter(create_custom_formatter(config.metric_prefix))
    ax.yaxis.set_tick_params(pad=2, labeltop=False, labelbottom=True, bottom=False, labelsize=12)

    # Remove spines
    ax.spines[['top', 'right', 'bottom']].set_visible(False)
    ax.spines['left'].set_linewidth(1.1)

    # Find peak and low points
    max_value = max(values)
    min_value = min(values)
    max_idx = values.index(max_value)
    min_idx = values.index(min_value)

    # Calculate offsets for annotations
    ylim_min, ylim_max = ax.get_ylim()
    y_range = ylim_max - ylim_min
    x_offset = timedelta(days=int((dates[-1] - dates[0]).days * 0.05))
    y_offset = y_range * 0.1

    # Peak annotation with customized styling
    peak_y_position = min(max_value + y_offset, ylim_max - (y_range * 0.05))
    peak_label = config.peak_label.format(metric=config.metric_name)
    ax.annotate(
        f'$\\mathbf{{{peak_label}}}$\n{format_large_numbers(max_value, None, config.metric_prefix)}',
        xy=(dates[max_idx], max_value),
        xytext=(dates[max_idx] - x_offset, peak_y_position),
        ha='right', va='bottom',
        **config.annotation_style
    )

    # Low point annotation with customized styling
    low_y_position = max(min_value - y_offset, ylim_min + (y_range * 0.05))
    low_label = config.low_label.format(metric=config.metric_name)
    ax.annotate(
        f'$\\mathbf{{{low_label}}}$\n{format_large_numbers(min_value, None, config.metric_prefix)}',
        xy=(dates[min_idx], min_value),
        xytext=(dates[min_idx] + x_offset, low_y_position),
        ha='left', va='top',
        **{**config.annotation_style,
           'arrowprops': {**config.annotation_style['arrowprops'],
                          'connectionstyle': "arc3,rad=0.2"}}
    )

    # Add header line and rectangle
    ax.plot([0.05, 0.9], [0.98, 0.98],
            transform=fig.transFigure,
            clip_on=False,
            color=config.colors['header_line'],
            linewidth=0.6)
    ax.add_patch(plt.Rectangle((0.05, 0.98), 0.04, -0.02,
                               facecolor=config.colors['header_line'],
                               transform=fig.transFigure,
                               clip_on=False,
                               linewidth=0))

    # Title and subtitle with customized text
    title = config.title_template.format(
        company=config.company_name,
        metric=config.metric_name,
        start_year=dates[0].strftime('%Y'),
        end_year=dates[-1].strftime('%Y')
    )
    subtitle = config.subtitle_template.format(
        company=config.company_name,
        metric=config.metric_name.lower()
    )

    ax.text(x=0.05, y=0.93,
            s=title,
            transform=fig.transFigure,
            ha='left',
            fontsize=14,
            weight='bold',
            alpha=0.8)

    ax.text(x=0.05, y=0.90,
            s=subtitle,
            transform=fig.transFigure,
            ha='left',
            fontsize=12,
            alpha=0.8)

    # Source attribution
    source_text = config.source_template.format(company=config.company_name)
    ax.text(x=0.05, y=0.12,
            s=source_text,
            transform=fig.transFigure,
            ha='left',
            fontsize=10,
            alpha=0.7)

    # Company name as x-label
    ax.set_xlabel(config.company_name,
                  fontsize=10,
                  weight='bold',
                  color='gray',
                  labelpad=10)

    # Highlight the latest point
    latest_label = config.latest_label.format(metric=config.metric_name)
    ax.scatter(dates[-1], values[-1],
               color=config.colors['latest_point'],
               edgecolor=config.colors['latest_point'],
               s=100,
               zorder=5,
               label=f'{latest_label} {format_large_numbers(values[-1], None, config.metric_prefix)}')
    ax.legend(loc='upper left', fontsize=10)

    # Set white background
    fig.patch.set_facecolor('white')

    return fig, ax