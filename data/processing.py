from datetime import datetime
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

        #Calculations
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
        import json
        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=4)
        print(f"Balance sheet data has been written to {output_file}")

    return output_data

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