'''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List  
from model import describe_table, execute_query, start_chat, print_chat_turns
import logging 
from fastapi.middleware.cors import CORSMiddleware
import re
import sqlite3

logging.basicConfig(level=logging.INFO)

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to only allow specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chat object to maintain conversation history
chat = None

# Pydantic model for user queries
class QueryRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the HR support system!"}

@app.post("/query")
def process_query(query_request: QueryRequest):
    global chat
    user_question = query_request.question
    logging.info(f"Received query: {user_question}")

    try:
        if chat is None:
            chat = start_chat()
            logging.info("Started new chat session.")

        response = chat.send_message(user_question)
        sql_query = response.text.strip()
        logging.info(f"Generated SQL query: {sql_query}")

        # Validate SQL query
        if not re.match(r"^SELECT|DESCRIBE", sql_query, re.IGNORECASE):
            logging.error(f"Invalid SQL query: {sql_query}")
            raise HTTPException(status_code=400, detail="Generated response is not a valid SQL query.")

        if "describe table" in user_question.lower():
            table_name = user_question.split("describe table")[-1].strip()
            schema = describe_table(table_name)
            logging.info(f"Schema: {schema}")
            return {"response": schema}
        else:
            results = execute_query(sql_query)
            logging.info(f"Query results: {results}")
            return {"sql_query": sql_query, "response": results}

    except sqlite3.Error as db_err:
        logging.error(f"SQLite error occurred: {db_err}")
        raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat-history")
def get_chat_history():
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat has not been initialized.")
    
    # Use the function from `model.py` to print chat history
    chat_history: List[dict] = []  # Specify the return type as a List of dictionaries
    print_chat_turns(chat)  # This will print the history to the console

    for event in chat.history:
        if event.role == "user":
            chat_history.append({"role": "user", "text": event.parts[0].text})
        elif event.role == "assistant":
            chat_history.append({"role": "assistant", "text": event.parts[0].text})
    
    return {"history": chat_history}'''

import sqlite3
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from model import describe_table, execute_query, start_chat, print_chat_turns

# FastAPI app
app = FastAPI()

logging.basicConfig(level=logging.INFO) #For logging information to debug

# Global chat object to maintain conversation history
chat = None

# Pydantic model for user queries
class QueryRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the HR support system!"} #servers running

@app.post("/query") #query end point
def process_query(query_request: QueryRequest):
    global chat
    user_question = query_request.question
    logging.info(f"Received query: {user_question}")

    try:
        if chat is None:
            chat = start_chat()
            logging.info("Started new chat session.")

        response = chat.send_message(user_question)
        response_text = response.text.strip()
        logging.info(f"Response: {response_text}")

        # Check if the response is a valid SQL query
        if "describe table" in user_question.lower():
            table_name = user_question.split("describe table")[-1].strip()
            schema = describe_table(table_name)
            logging.info(f"Schema: {schema}")
            return {"response": schema}
        else:
            # Check if the response is a valid SQL query or a natural language sentence
            if response_text.lower().startswith(("select", "describe")):
                results = execute_query(response_text)
                logging.info(f"Query results: {results}")
                return {"sql_query": response_text, "response": results}
            else:
                logging.info(f"Natural language response: {response_text}")
                return {"response": response_text}

    except sqlite3.Error as db_err:
        logging.error(f"SQLite error occurred: {db_err}")
        raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat-history") #Chat history endpoint
def get_chat_history():
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat has not been initialized.")
    
    chat_history: List[dict] = []
    print_chat_turns(chat)

    for event in chat.history:
        if event.role == "user":
            chat_history.append({"role": "user", "text": event.parts[0].text})
        elif event.role == "assistant":
            chat_history.append({"role": "assistant", "text": event.parts[0].text})
    
    return {"history": chat_history}
