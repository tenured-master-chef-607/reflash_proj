import subprocess
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import os
from dotenv import load_dotenv
import openai

# Fetch data from JavaScript file
def fetch_data_from_js():
    try:
        result = subprocess.run(
            ['node', 'fetchAccountingData.js'], 
            capture_output=True, 
            text=True,  
            check=True
        )
        data = json.loads(result.stdout)
        return data
    except subprocess.CalledProcessError as e:
        print("Error running the JavaScript file:", e)
        print("Stderr:", e.stderr)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)

# Process balance sheet data
def balance_briefing(data_accounting_balance_sheets, output_file=None):
    output_data = []

    for balance_sheet in data_accounting_balance_sheets:
        date = balance_sheet.get("date")
        report_json = balance_sheet.get("report_json")

        assets = report_json.get("assets")[0]
        liabilities = report_json.get("liabilities")[0]
        equity = report_json.get("equity")[0]

        asset_sub = [
            {"name": item.get("name"), "value": item.get("value")}
            for item in assets.get("sub_items", [])
        ]
        liability_sub = [
            {"name": item.get("name"), "value": item.get("value")}
            for item in liabilities.get("sub_items", [])
        ]
        equity_sub = [
            {"name": item.get("name"), "value": item.get("value")}
            for item in equity.get("sub_items", [])
        ]

        net_income = next(
            (item.get("value") for item in equity_sub if item.get("name") == "Net Income"),
            None
        )

        total_assets = assets.get("value") or 1
        total_liabilities = liabilities.get("value") or 1
        total_equity = equity.get("value") or 1
        net_income = net_income or 0

        # Calculate financial ratios
        current_ratio = total_assets / total_liabilities
        debt_to_equity_ratio = total_liabilities / total_equity
        return_on_equity = net_income / total_equity
        equity_multiplier = total_assets / total_equity
        debt_ratio = total_liabilities / total_assets
        net_profit_margin = net_income / total_assets

        balance_sheet_output = {
            "date": date,
            "total_asset": total_assets,
            "asset_breakdown": asset_sub,
            "total_liability": total_liabilities,
            "liability_breakdown": liability_sub,
            "total_equity": total_equity,
            "equity_breakdown": equity_sub,
            "net_income": net_income,
            "ratios": {
                "current_ratio": current_ratio,
                "debt_to_equity_ratio": debt_to_equity_ratio,
                "return_on_equity": return_on_equity,
                "equity_multiplier": equity_multiplier,
                "debt_ratio": debt_ratio,
                "net_profit_margin": net_profit_margin,
            },
        }

        output_data.append(balance_sheet_output)

    if output_file:
        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=4)
        print(f"Balance sheet data has been written to {output_file}")

    return output_data

# Plot financial briefing
def plot_financial_briefing(output_data):
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

    fig = plt.figure(figsize=(18, 22))
    gs = gridspec.GridSpec(4, 2, height_ratios=[1.5, 1, 1, 1])

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
    fig.autofmt_xdate(rotation=45)

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
    plt.show()

# Generate financial summary
def financial_summary(balance_sheets, target_date):
    target_date = datetime.fromisoformat(target_date).replace(tzinfo=None)
    dates = [datetime.fromisoformat(sheet['date']).replace(tzinfo=None) for sheet in balance_sheets]

    nearest_date = min(dates, key=lambda x: abs(x - target_date))
    nearest_index = dates.index(nearest_date)
    nearest_sheet = balance_sheets[nearest_index]

    return nearest_sheet

# Main execution
if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    target_date = input("Enter the target date (YYYY-MM-DD): ").strip()

    data = fetch_data_from_js()
    if data:
        data_accounting_balance_sheets = data.get("accounting_balance_sheets")

    balance_sheets = balance_briefing(data_accounting_balance_sheets)

    try:
        balance_sheets.sort(key=lambda x: datetime.fromisoformat(x['date']))
    except KeyError:
        print("Error: Missing 'date' field in one or more records.")
        balance_sheets = [] 
    except ValueError as e:
        print(f"Error: Invalid date format in one or more records. {e}")
        balance_sheets = []  

    if balance_sheets:
        plot_financial_briefing(balance_sheets)

        summary = financial_summary(balance_sheets, target_date)

        prompt = f"""Financial data and calculated ratios:{summary}. Using the provided balance sheet data for the specified date, {target_date}, generate a concise financial analysis report evaluating the company's financial health. The report should be structured into the following six sections: \
        1. Financial Summary: Provide an overview of the key financial figures, including total assets, liabilities, equity, and net income, highlighting any significant observations. \
        2. Breakdown of Financial Components: Analyze and describe the composition of assets, liabilities, and equity, noting any dominant or missing components. \
        3. Key Financial Ratios Interpretation: Evaluate the company's financial health by interpreting relevant ratios (e.g., current ratio, debt-to-equity ratio, return on equity, equity multiplier, debt ratio, and net profit margin) in the context of standard benchmarks. \
        4. Key Findings: Highlight the most critical takeaways from the data, such as liquidity, solvency, profitability, or significant trends. \
        5. Key Insights: Summarize actionable insights that can be drawn from the analysis, focusing on areas of strength, risks, or opportunities. \
        6. Recommendations: Provide practical recommendations for improving financial performance, mitigating risks, or leveraging opportunities. \
        Ensure that the analysis is clear, precise, and easy to understand, using the data provided to support conclusions where applicable."""

        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        chat_completion = client.ChatCompletion.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": "You are a helpful professional financial analyst."},
                {"role": "user", "content": prompt},
            ]
        )

        print(chat_completion['choices'][0]['message']['content'])
    else:
        print("No valid balance sheet data to process.")
