import google.generativeai as genai
import sqlite3
import textwrap
import logging 
from dotenv import load_dotenv 
import os 


'''logging.basicConfig(level=logging.INFO)
#from dotenv import load_dotenv

# Load environment variables
#load_dotenv()

GOOGLE_API_KEY = " AIzaSyBKaXxZkyPZsq-Zcn57mCbGj-xPFUEbCNs" 
# Set up your Google API Key
genai.configure(api_key=GOOGLE_API_KEY)'''


logging.basicConfig(level=logging.INFO) 

# Load environment variables from .env file 
load_dotenv()

# Get the Google API Key from environment variable 
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 


if not GOOGLE_API_KEY: 
    raise ValueError("Google API Key is not set. Please check your .env file.") # Set up your Google API Key


genai.configure(api_key=GOOGLE_API_KEY)

# SQLite database file
DB_FILE = "employee.db"

# Database connection
db_conn = sqlite3.connect(DB_FILE,check_same_thread=False)

# Define database functions
def list_tables() -> list[str]:
    print(' - DB CALL: list_tables')
    cursor = db_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return [t[0] for t in tables]

def describe_table(table_name: str) -> list[tuple[str, str]]:
    print(' - DB CALL: describe_table')
    cursor = db_conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema = cursor.fetchall()
    return [(col[1], col[2]) for col in schema]

def execute_query(sql: str) -> list[list[str]]:
    print(' - DB CALL: execute_query')
    cursor = db_conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

# Instruction for the Gemini model
instruction = """You are a helpful chatbot that can interact with an SQL database 
containing employee information.
You will take the user's questions and turn them into SQL queries using the tools
available. Once you have the information you need, you will answer the user's question using
the data returned. Use list_tables to see what tables are present, describe_table to understand
the schema, and execute_query to issue an SQL SELECT query."""

# Set up the model
model = genai.GenerativeModel(
    "models/gemini-1.5-flash-latest", tools=[list_tables, describe_table, execute_query], system_instruction=instruction
)

# Start chat
def start_chat():
    return model.start_chat(enable_automatic_function_calling=True)

# Inspecting the conversation
def print_chat_turns(chat):
    for event in chat.history:
        print(f"{event.role.capitalize()}:")
        for part in event.parts:
            if txt := part.text:
                print(f'  "{txt}"')
            elif fn := part.function_call:
                args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
                print(f"  Function call: {fn.name}({args})")
            elif resp := part.function_response:
                print("  Function response:")
                print(textwrap.indent(str(resp), "    "))
        print()
