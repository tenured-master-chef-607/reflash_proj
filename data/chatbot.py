import sys
import os
import json
import openai
from openai import OpenAI
from dotenv import load_dotenv
from get_all_tables import get_all_tables, fetch_table_data

def load_data():
    """Fetch all table names and their corresponding data."""
    data = {}
    table_names = get_all_tables()
    if not table_names:
        print("No tables found")
        sys.exit(1)
    
    for table in table_names:
        table_data = fetch_table_data(table)
        if table_data is not None:
            data[table] = table_data 
    
    return data

def get_relevant_tables(data, user_query):
    """Use LLM to determine which tables are relevant for answering the query."""
    prompt = f"""As a senior financial analyst, you have access to the following tables: {', '.join(data.keys())}. 
    The user has asked the following question: {user_query}.
    Your task is to carefully analyze the available tables and determine which ones contain relevant information to answer the user's question.
    Return only a list of table names that would be useful, formatted as follows: [table_name_1, table_name_2, ...]. 
    Do not include any explanations or additional text—only the list of relevant tables."""
    
    response = query_llm(prompt)
    response = response.strip("[]").split(",")
    return [table.strip().strip('"') for table in response]

def query_llm(prompt):
    """Query the LLM model with the provided prompt and return the response."""
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful professional financial analyst."},
            {"role": "user", "content": prompt},
        ],
        model="gpt-4o",
    )

    return chat_completion.choices[0].message.content.strip()

def generate_response(data, relevant_tables, user_query):
    """Generate a detailed response based on relevant data tables."""
    knowledge = {table: data[table] for table in relevant_tables if table in data}
    
    prompt = f"""As a senior financial analyst, you have access to the following knowledge: {', '.join(knowledge.keys())}. 
    The user has asked the following question: {user_query}.
    Based on your analysis of the available data, provide a detailed response to the user's question. 
    Be sure to include specific details and insights from the relevant tables to support your analysis. 
    Generate a paragraph-style response that is clear, concise, and informative."""
    
    response = query_llm(prompt)
    return response

def main():
    data = load_data()
    user_query = input("Enter a query: ")
    relevant_tables = get_relevant_tables(data, user_query)
    response = generate_response(data, relevant_tables, user_query)
    return response

if __name__ == "__main__":
    main()
