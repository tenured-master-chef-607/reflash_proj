from flask import Flask, request, render_template, jsonify
from data.fetch_data import fetch_data_from_supabase
from data.processing import balance_briefing, financial_summary
from data.markdown_generation import generate_markdown
import importlib
from datetime import datetime, timedelta

app = Flask(__name__)

# Cache for balance sheets data
_balance_sheets_cache = {
    "data": None,
    "timestamp": None
}
_CACHE_EXPIRY = timedelta(hours=3)  # Cache expires after 3 hours

def get_balance_sheets():
    # Check if cache exists and is still valid
    now = datetime.now()
    if (_balance_sheets_cache["data"] is not None and 
        _balance_sheets_cache["timestamp"] is not None and
        now - _balance_sheets_cache["timestamp"] < _CACHE_EXPIRY):
        print("Using cached balance sheets data")
        return _balance_sheets_cache["data"]
    
    # Cache is empty or expired, fetch fresh data
    print("Fetching fresh balance sheets data")
    data = fetch_data_from_supabase()
    balance_sheets = []
    
    if data:
        data_accounting_balance_sheets = data.get("accounting_balance_sheets")
        balance_sheets = balance_briefing(data_accounting_balance_sheets)
        
    try:
        balance_sheets.sort(key=lambda x: datetime.fromisoformat(x['date']))
    except (KeyError, ValueError) as e:
        print(f"Error sorting balance sheets: {e}")
    
    # Update cache
    _balance_sheets_cache["data"] = balance_sheets
    _balance_sheets_cache["timestamp"] = now
        
    return balance_sheets

# Function removed/commented out
# def get_plot(balance_sheets):
#     return plot_financial_briefing(balance_sheets)

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = None
    stats = None
    target_date = None
    # We'll no longer generate a backend plot
    plot = None
    
    # Get balance sheets
    balance_sheets = get_balance_sheets()
    
    # Extract available dates for the dropdown
    available_dates = sorted([sheet['date'] for sheet in balance_sheets], reverse=True)
    
    if request.method == 'POST':
        target_date = request.form.get('target_date')
        
        if target_date and balance_sheets:
            # Get financial summary for the target date
            summary_data = financial_summary(balance_sheets, target_date)
            
            # Generate markdown for display
            stats = generate_markdown(summary_data)
            
            # Plot generation removed
            # plot = get_plot(balance_sheets)
            
            # We'll no longer create the summary here - it will be loaded async
            summary = "Loading analysis..."

    return render_template('template.html', 
                          summary=summary, 
                          stats=stats, 
                          target_date=target_date, 
                          plot_url=None,  # Always passing None for plot_url
                          balance_sheets=balance_sheets, 
                          available_dates=available_dates)

# Add an API endpoint to get balance sheet data as JSON if needed
@app.route('/api/balance_sheets', methods=['GET'])
def get_balance_sheets_api():
    balance_sheets = get_balance_sheets()
    return jsonify(balance_sheets)

# Add a new endpoint for async AI analysis
@app.route('/api/analysis', methods=['POST'])
def get_analysis():
    data = request.json
    target_date = data.get('target_date')
    
    if not target_date:
        return jsonify({"error": "No target date provided"}), 400
    
    balance_sheets = get_balance_sheets()
    summary_data = financial_summary(balance_sheets, target_date)
    
    prompt = f"""Financial data and calculated ratios:{summary_data}. Using the provided balance sheet data for the specified date, {target_date}, generate a concise financial analysis report evaluating the company's financial health. The report should be structured into the following six sections: 
    1. Financial Summary: Provide an overview of the key financial figures, including total assets, liabilities, equity, and net income, highlighting any significant observations.
    2. Breakdown of Financial Components: Analyze and describe the composition of assets, liabilities, and equity, noting any dominant or missing components.
    3. Key Financial Ratios Interpretation: Evaluate the company's financial health by interpreting relevant ratios (e.g., current ratio, debt-to-equity ratio, return on equity, equity multiplier, debt ratio, and net profit margin) in the context of standard benchmarks.
    4. Key Findings: Highlight the most critical takeaways from the data, such as liquidity, solvency, profitability, or significant trends.
    5. Key Insights: Summarize actionable insights that can be drawn from the analysis, focusing on areas of strength, risks, or opportunities.
    6. Recommendations: Provide practical recommendations for improving financial performance, mitigating risks, or leveraging opportunities.
    Ensure that the analysis is clear, precise, and easy to understand, using the data provided to support conclusions where applicable."""
    
    gpt_agent = importlib.import_module("agents.gpt_agent")
    summary = gpt_agent.call_gpt_agent(prompt)
    
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
