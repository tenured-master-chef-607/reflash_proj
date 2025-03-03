import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

def get_all_tables():
    """
    Get all table names from Supabase using the Python client.
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
        
        # Fetch table names using system schema query
        response = supabase.rpc('get_tables').execute()
        
        if hasattr(response, 'error') and response.error:
            print(f"Error fetching tables from Supabase: {response.error}")
            return None
            
        return response.data
        
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return None

def fetch_table_data(table_name):
    """
    Fetch data from a specific table using the Python Supabase client.
    Replaces the Node.js subprocess approach.
    """
    try:
        if not isinstance(table_name, str):
            print("Error: table_name must be a string.")
            return None

        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("Error: Missing Supabase credentials in environment variables")
            return None
            
        # Initialize Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
        # Fetch data from the specified table
        response = supabase.table(table_name.strip()).select('*').execute()
        
        if hasattr(response, 'error') and response.error:
            print(f"Error fetching data from table {table_name}: {response.error}")
            return None
            
        return {table_name: response.data}
        
    except Exception as e:
        print(f"Error fetching table data: {e}")
        return None
