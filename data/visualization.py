import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
from datetime import datetime
import io
import base64

def plot_financial_briefing(output_data):
    """
    Plots financial ratios and major financial statistics from balance sheet data
    and returns the plot as a base64-encoded string for use in web applications.

    Parameters:
    - output_data: List of dictionaries containing balance sheet data and ratios.
      Each dictionary should include:
        - 'date'
        - 'total_asset'
        - 'total_liability'
        - 'total_equity'
        - 'net_income'
        - 'ratios': Dictionary containing financial ratios
    """
    # Extract data for plotting
    dates = [datetime.fromisoformat(item['date']) for item in output_data]
    total_assets = [item['total_asset'] for item in output_data]
    total_liabilities = [item['total_liability'] for item in output_data]
    total_equities = [item['total_equity'] for item in output_data]
    net_incomes = [item['net_income'] for item in output_data]

    current_ratios = [item['ratios']['current_ratio'] for item in output_data]
    debt_to_equity_ratios = [item['ratios']['debt_to_equity_ratio'] for item in output_data]
    return_on_equities = [item['ratios']['return_on_equity'] for item in output_data]
    equity_multipliers = [item['ratios']['equity_multiplier'] for item in output_data]
    debt_ratios = [item['ratios']['debt_ratio'] for item in output_data]
    net_profit_margins = [item['ratios']['net_profit_margin'] for item in output_data]

    # Plotting
    fig = plt.figure(figsize=(18, 22))
    gs = gridspec.GridSpec(4, 2, height_ratios=[1.5, 1, 1, 1])

    # Major Financial Statistics Plot
    ax_major_stats = fig.add_subplot(gs[0, :])
    ax_major_stats.plot(dates, total_assets, label='Total Assets', marker='o')
    ax_major_stats.plot(dates, total_liabilities, label='Total Liabilities', marker='o')
    ax_major_stats.plot(dates, total_equities, label='Total Equities', marker='o')
    ax_major_stats.plot(dates, net_incomes, label='Net Income', marker='o')
    ax_major_stats.set_title('Major Financial Statistics')
    ax_major_stats.set_xlabel('Date')
    ax_major_stats.set_ylabel('Value (USD)')
    ax_major_stats.legend()
    ax_major_stats.grid(True)
    ax_major_stats.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax_major_stats.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    axs = [
        fig.add_subplot(gs[1, 0]),
        fig.add_subplot(gs[1, 1]),
        fig.add_subplot(gs[2, 0]),
        fig.add_subplot(gs[2, 1]),
        fig.add_subplot(gs[3, 0]),
        fig.add_subplot(gs[3, 1]),
    ]

    ratio_titles = [
        'Current Ratio',
        'Debt to Equity Ratio',
        'Return on Equity',
        'Equity Multiplier',
        'Debt Ratio',
        'Net Profit Margin',
    ]
    ratio_data = [
        current_ratios,
        debt_to_equity_ratios,
        return_on_equities,
        equity_multipliers,
        debt_ratios,
        net_profit_margins,
    ]

    for ax, title, data in zip(axs, ratio_titles, ratio_data):
        ax.plot(dates, data, marker='o')
        ax.set_title(title)
        ax.set_xlabel('Date')
        ax.set_ylabel('Ratio')
        ax.grid(True)

        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    fig.subplots_adjust(hspace=0.4) 
    fig.autofmt_xdate(rotation=45)  
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close(fig)
    return f"data:image/png;base64,{plot_data}"
