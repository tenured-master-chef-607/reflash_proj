def generate_markdown(data):
    markdown = f"""
# Financial Report

**Date:** {data['date']}

## Assets
**Total Assets:** ${data['total_asset']:,}

### Breakdown
"""
    for asset in data["asset_breakdown"]:
        markdown += f"- **{asset['name']}:** ${asset['value']:,}\n"

    markdown += f"""

## Liabilities
**Total Liabilities:** ${data['total_liability']:,}

### Breakdown
"""
    for liability in data["liability_breakdown"]:
        markdown += f"- **{liability['name']}:** ${liability['value']:,}\n"

    markdown += f"""

## Equity
**Total Equity:** ${data['total_equity']:,}

### Breakdown
"""
    for equity in data["equity_breakdown"]:
        markdown += f"- **{equity['name']}:** ${equity['value']:,}\n"

    markdown += f"""

## Net Income
**Net Income:** ${data['net_income']:,}

## Ratios
"""
    for ratio, value in data["ratios"].items():
        markdown += f"- **{ratio.replace('_', ' ').title()}:** {value}\n"

    return markdown
