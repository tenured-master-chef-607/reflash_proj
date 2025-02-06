import subprocess
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import openai

from openai import OpenAI
from dotenv import load_dotenv
import os

from flask import Flask, request, render_template_string

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

def balance_briefing(data_accounting_balance_sheets, output_file=None):
    output_data = []

    for balance_sheet in data_accounting_balance_sheets:
        date = balance_sheet.get("date")
        report_json = balance_sheet.get("report_json")

        assets = report_json.get("assets")[0]
        assets_subitems = assets.get("sub_items", [])
        asset_sub = [
            {"name": asset_item.get("name"), "value": asset_item.get("value")}
            for asset_item in assets_subitems
        ]

        liabilities = report_json.get("liabilities")[0]
        liabilities_subitems = liabilities.get("sub_items", [])
        liability_sub = [
            {"name": liability_item.get("name"), "value": liability_item.get("value")}
            for liability_item in liabilities_subitems
        ]

        equity = report_json.get("equity")[0]
        equity_subitems = equity.get("sub_items", [])
        equity_sub = [
            {"name": equity_item.get("name"), "value": equity_item.get("value")}
            for equity_item in equity_subitems
        ]

        net_income = next(
            (equity_item.get("value") for equity_item in equity_subitems if equity_item.get("name") == "Net Income"),
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

    # Optional: Write output to a file if specified
    if output_file:
        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=4)
        print(f"Balance sheet data has been written to {output_file}")

    return output_data

def plot_financial_briefing(output_data):
    """
    Plots financial ratios and major financial statistics from balance sheet data.

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

    # Adjust x-axis ticks for clarity
    ax_major_stats.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax_major_stats.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate(rotation=45)

    # Individual Ratio Plots
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

        # Adjust x-axis ticks for clarity
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Automatically adjust layout and add space between plots
    fig.subplots_adjust(hspace=0.4)  # Increase vertical spacing
    fig.autofmt_xdate(rotation=45)  # Rotate x-axis labels for readability
    plt.tight_layout()
    plt.show()

def get_terminal_subitems(items):
    terminal_items = []
    for item in items:
        subitems = item.get("sub_items", [])
        if subitems:
            terminal_items.extend(get_terminal_subitems(subitems))
        else:
            terminal_items.append(item)
    return terminal_items

def financial_summary(balance_sheets, target_date):
    nearest_date = None

    target_date = datetime.fromisoformat(target_date).replace(tzinfo=None)
    dates = [datetime.fromisoformat(sheet['date']).replace(tzinfo=None) for sheet in balance_sheets]
    
    if target_date in dates:
        nearest_date = target_date
    else:
        nearest_date = min(dates, key=lambda x: abs(x - target_date))
    nearest_index = dates.index(nearest_date)
    nearest_sheet = balance_sheets[nearest_index]

    return nearest_sheet

# Flask Application for User Interaction
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Financial Analysis</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            display: flex;
            flex-direction: row;
            width: 90%;
            margin-top: 20px;
        }
        .left, .right {
            flex: 1;
            padding: 20px;
            border: 1px solid #ccc;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin: 10px;
        }
        .form-container {
            margin-bottom: 20px;
            width: 100%;
        }
        h1 {
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>Financial Analysis Tool</h1>
    <form method=\"POST\" class=\"form-container\">
        <label for=\"target_date\">Enter Target Date (YYYY-MM-DD):</label>
        <input type=\"date\" id=\"target_date\" name=\"target_date\" required>
        <button type=\"submit\">Get Financial Summary</button>
    </form>
    <div class=\"container\">
        <div class=\"left\">
            <h2>Financial Stats & Ratios</h2>
            {% if stats %}
                <pre>{{ stats }}</pre>
            {% endif %}
        </div>
        <div class=\"right\">
            <h2>LLM Analysis</h2>
            {% if summary %}
                <pre>{{ summary }}</pre>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = None
    stats = None
    target_date = None

    if request.method == 'POST':
        target_date = request.form.get('target_date')
        if target_date and balance_sheets:
            summary_data = financial_summary(balance_sheets, target_date)

            stats = json.dumps(summary_data, indent=4)

            prompt = f"""Financial data and calculated ratios:{summary_data}. Using the provided balance sheet data for the specified date, {target_date}, generate a concise financial analysis report evaluating the company's financial health. The report should be structured into the following six sections: 
            1. Financial Summary: Provide an overview of the key financial figures, including total assets, liabilities, equity, and net income, highlighting any significant observations.
            2. Breakdown of Financial Components: Analyze and describe the composition of assets, liabilities, and equity, noting any dominant or missing components.
            3. Key Financial Ratios Interpretation: Evaluate the company's financial health by interpreting relevant ratios (e.g., current ratio, debt-to-equity ratio, return on equity, equity multiplier, debt ratio, and net profit margin) in the context of standard benchmarks.
            4. Key Findings: Highlight the most critical takeaways from the data, such as liquidity, solvency, profitability, or significant trends.
            5. Key Insights: Summarize actionable insights that can be drawn from the analysis, focusing on areas of strength, risks, or opportunities.
            6. Recommendations: Provide practical recommendations for improving financial performance, mitigating risks, or leveraging opportunities.
            Ensure that the analysis is clear, precise, and easy to understand, using the data provided to support conclusions where applicable."""

            load_dotenv()

            openai.api_key = os.getenv("OPENAI_API_KEY")

            client = OpenAI(
                api_key=os.environ.get("OPENAI_API_KEY"), 
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful professional financial analyst. Do not include verbal tics like 'certainly' or 'um'."},
                    {
                        "role": "user",
                        "content": f"{prompt}",
                    }
                ],
                model="gpt-4o",
            )


            summary = chat_completion.choices[0].message.content

    return render_template_string(HTML_TEMPLATE, summary=summary, stats=stats, target_date=target_date)

if __name__ == "__main__":
    data = fetch_data_from_js()
    balance_sheets = []

    if data:
        data_accounting_balance_sheets = data.get("accounting_balance_sheets")
        balance_sheets = balance_briefing(data_accounting_balance_sheets)

    try:
        balance_sheets.sort(key=lambda x: datetime.fromisoformat(x['date']))
    except KeyError:
        print("Error: Missing 'date' field in one or more records.")
    except ValueError as e:
        print(f"Error: Invalid date format in one or more records. {e}")

    app.run(debug=True)
