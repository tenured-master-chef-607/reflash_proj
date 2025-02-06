import subprocess
import json

def fetch_data_from_js():
    try:
        result = subprocess.run(
            ['node', 'fetchAccountingData.js'], 
            capture_output=True, 
            text=True,  
            check=True
        )

        data = json.loads(result.stdout)

        print("Accounting Accounts Data:", data.get("accounting_accounts"))
        print("Accounting Balance Sheets Data:", data.get("accounting_balance_sheets"))

        return data
    except subprocess.CalledProcessError as e:
        print("Error running the JavaScript file:", e)
        print("Stderr:", e.stderr)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)

fetch_data_from_js()

"""

if data:
   with open("accounting_accounts.json", "w") as f:
      json.dump(data.get("accounting_accounts"), f, indent=4)

 with open("accounting_balance_sheets.json", "w") as f:
    json.dump(data.get("accounting_balance_sheets"), f, indent=4)
    print("Data saved locally!")

"""