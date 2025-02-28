import subprocess
import json
import os

def get_all_tables():
    try:
        result = subprocess.run(
            ['node', 'tableNames.js'],
            capture_output=True,
            text=True,
            check=True
        )

        raw_output = result.stdout.strip()
        data = json.loads(raw_output)

        if not isinstance(data, list):
            print("Unexpected response format for table names:", raw_output)
            return None

        return data

    except subprocess.CalledProcessError as e:
        print("Error running the JavaScript file:", e)
        print("Stderr:", e.stderr)
        return None
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        print("Raw JSON Response:", result.stdout)
        return None



def fetch_table_data(table_name):
    try:
        if not isinstance(table_name, str):
            print("Error: table_name must be a string.")
            return None

        result = subprocess.run(
            ['node', os.path.join(os.getcwd(), 'fetchAllData.js'), table_name.strip()],  
            capture_output=True,
            text=True,
            check=True
        )

        raw_output = result.stdout.strip()

        if not raw_output:
            print(f"Error: JavaScript returned empty response for {table_name}.")
            return None
        
        return json.loads(raw_output)

    except subprocess.CalledProcessError as e:
        print(f"Error running JavaScript file: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        print("Raw JSON Response:", raw_output)
        return None
