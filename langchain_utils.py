import os
from dotenv import load_dotenv
import mysql.connector
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
import google.generativeai as genai  # For Gemini API

from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.memory import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from table_details import table_chain as select_table
from prompts import final_prompt, answer_prompt

import streamlit as st

# Load environment variables
load_dotenv()

# Database credentials from .env
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # You can still keep this if you need it for OpenAI
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# Configure Gemini (via Google Generative AI SDK)
genai.configure(api_key=OPENAI_API_KEY)  # Replace with your actual API key

# Set up the connection to your MySQL database
def get_db_connection():
    """
    Create and return a connection to the MySQL database.
    """
    conn = mysql.connector.connect(
        host=db_host,  # Database host
        user=db_user,  # Database user
        password=db_password,  # Replace with your password
        database=db_name  # MySQL sample database name
    )
    return conn


@st.cache_resource
def get_chain():
    print("Creating chain")
    
    # Initialize the database connection
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    
    # Replace OpenAI model with Gemini model
    generate_query = create_sql_query_chain(genai, db, final_prompt) 
    
    # Define the tool to execute the SQL query
    execute_query = QuerySQLDataBaseTool(db=db)
    
    # Use answer prompt to reformat the response
    rephrase_answer = answer_prompt | genai | StrOutputParser()

    # Final chain combining the table selection and query generation
    chain = (
        RunnablePassthrough.assign(table_names_to_use=select_table) |
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        ) |
        rephrase_answer
    )
    
    return chain


def create_history(messages):
    """
    Create a history of messages for the chat interface.
    """
    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history


def invoke_chain(question, messages):
    """
    Invoke the LangChain processing chain with the user's question and message history.
    """
    chain = get_chain()
    history = create_history(messages)
    
    # Invoke the chain and get the response from Gemini
    response = chain.invoke({
        "question": question,
        "top_k": 3,  # You can adjust top_k based on your needs
        "messages": history.messages
    })
    
    # Update history with the user's message and the AI's response
    history.add_user_message(question)
    history.add_ai_message(response)
    
    return response
