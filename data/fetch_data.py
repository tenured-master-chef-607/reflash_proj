import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

def fetch_data_from_supabase():
    """
    Fetch balance sheet data directly from Supabase using the Python client.
    Replaces the Node.js subprocess approach.
    """
    try:
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("Error: Missing Supabase credentials in environment variables")
            return None
            
        # Initialize Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
        # Fetch balance sheets with the same query as the JS version
        response = supabase.table('accounting_balance_sheets').select('date, report_json').order('date').execute()
        
        if hasattr(response, 'error') and response.error:
            print(f"Error fetching data from Supabase: {response.error}")
            return None
            
        # Format the response to match the structure from the JS version
        return {
            "accounting_balance_sheets": response.data
        }
        
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return None

