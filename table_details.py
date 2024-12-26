import pandas as pd
import mysql.connector  # Import MySQL connector
import streamlit as st
from operator import itemgetter
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
import google.generativeai as genai

# Configure Gemini (via Google Generative AI SDK)
genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key


@st.cache_data
def get_table_details_from_db():
    """
    Fetch table details dynamically from the MySQL database.
    """
    # Replace with your MySQL database connection details
    conn = mysql.connector.connect(
        host="localhost",  # Database host
        user="root",       # Database user
        password="password",  # Replace with your password
        database="classicmodels"  # MySQL sample database name
    )
    cursor = conn.cursor()

    # Fetch table names dynamically
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    table_details = ""
    for table in tables:
        table_name = table[0]
        # Fetch descriptions if available; otherwise, use placeholders
        table_details += f"Table Name: {table_name}\nTable Description: Add description here if available\n\n"

    conn.close()
    return table_details


class Table(BaseModel):
    """
    Table in SQL database, defined for extraction chain.
    """
    name: str = Field(description="Name of table in SQL database.")


def get_tables(tables: List[Table]) -> List[str]:
    """
    Extract table names from the Table class.
    """
    return [table.name for table in tables]


def query_gemini(prompt):
    """
    Query Gemini using Google Generative AI SDK.
    """
    response = genai.generate_text(
        model="models/text-bison-001",  # Replace with the appropriate Gemini model
        prompt=prompt,
        temperature=0,
        max_output_tokens=256
    )
    return response.result.strip()  # Extract the desired result


# Get table details dynamically from the MySQL database
table_details = get_table_details_from_db()
table_details_prompt = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables are:

{table_details}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""


def extract_relevant_tables(question):
    """
    Extract relevant tables for a given question using Gemini.
    """
    prompt = f"Question: {question}\n\n{table_details_prompt}"
    return query_gemini(prompt)


# Streamlit App UI
st.title("SQL Table Selector with Gemini")

st.write("This app dynamically fetches SQL table details and selects relevant tables using Gemini.")

# User input
user_question = st.text_input("Enter your SQL-related question:")

if user_question:
    with st.spinner("Identifying relevant tables..."):
        relevant_tables = extract_relevant_tables(user_question)
        st.success("Relevant tables identified!")
        st.write("Relevant Tables:")
        st.write(relevant_tables)
