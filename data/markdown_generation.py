def generate_markdown(data):
    # Format the date from ISO format to a more readable format
    date_str = data['date']
    try:
        # Parse the ISO date and reformat it
        from datetime import datetime
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        formatted_date = date_obj.strftime('%B %d, %Y')  # Example: "December 31, 2024"
    except:
        # Fallback if date parsing fails
        formatted_date = date_str

    markdown = f"""
# Financial Report

**Date:** {formatted_date}

## Assets
**Total Assets:** ${data['total_asset']:,.2f}

### Breakdown
"""
    for asset in data["asset_breakdown"]:
        markdown += f"- **{asset['name']}:** ${asset['value']:,.2f}\n"

    markdown += f"""

## Liabilities
**Total Liabilities:** ${data['total_liability']:,.2f}

### Breakdown
"""
    for liability in data["liability_breakdown"]:
        markdown += f"- **{liability['name']}:** ${liability['value']:,.2f}\n"

    markdown += f"""

## Equity
**Total Equity:** ${data['total_equity']:,.2f}

### Breakdown
"""
    for equity in data["equity_breakdown"]:
        if equity['value'] is not None:  # Check for None values
            markdown += f"- **{equity['name']}:** ${equity['value']:,.2f}\n"
        else:
            markdown += f"- **{equity['name']}:** N/A\n"

    markdown += f"""

## Net Income
**Net Income:** ${data['net_income']:,.2f}

## Ratios
"""
    for ratio, value in data["ratios"].items():
        # Format ratio values to 2 decimal places
        markdown += f"- **{ratio.replace('_', ' ').title()}:** {value:.2f}\n"

    return markdown
