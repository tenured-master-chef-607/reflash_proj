from flask import Flask, request, render_template
import os
import json
import openai
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, render_template, request, jsonify
from data.fetch_data import fetch_data_from_js
from data.processing import balance_briefing, financial_summary
from data.visualization import plot_financial_briefing
from data.markdown_generation import generate_markdown
from datetime import datetime
import json
import subprocess
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = None
    stats = None
    target_date = None
    plot = None

    if request.method == 'POST':
        target_date = request.form.get('target_date')
        if target_date and balance_sheets:
            summary_data = financial_summary(balance_sheets, target_date)

            stats = json.dumps(summary_data, indent=4)
            stats = generate_markdown(summary_data)

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

        plot = plot_financial_briefing(balance_sheets)

    return render_template('template.html', summary=summary, stats=stats, target_date=target_date, plot_url=plot)

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
