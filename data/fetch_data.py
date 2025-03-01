import subprocess
import json
import os

def fetch_data_from_js():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir)) 
        js_file_path = os.path.join(parent_dir, "fetchAccountingData.js") 

        result = subprocess.run(
            ['node', js_file_path],
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

