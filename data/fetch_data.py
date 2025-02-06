import subprocess
import json
import os

def fetch_data_from_js():
    
    try:
        
        result = subprocess.run(
            ['node', os.path.join(os.getcwd(),"fetchAccountingData.js")],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running Node.js script: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

