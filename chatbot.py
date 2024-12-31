import streamlit as st
import requests

'''def chatbot_ui():
    # Streamlit App Configuration
    st.set_page_config(page_title="HR Support Chatbot")
    st.header("HR Support Chatbot")

    with st.chat_message("user"):
        st.write("Hello 👋")
    
    # Input from user via chat_input (includes send button)
    question = st.chat_input("Input your question:")

    # FastAPI backend URL
    BACKEND_URL = "http://127.0.0.1:8000/query"

    if question:  # Triggered when the send button is clicked
        if question.strip():
            try:
                # Send the request to the backend
                response = requests.post(BACKEND_URL, json={"question": question})
                if response.status_code == 200:
                    data = response.json()
                    st.chat_message("assistant").write("Here is the SQL query and result:")
                    st.subheader("Generated SQL Query:")
                    st.code(data["sql_query"])
                    st.subheader("Query Result:")
                    for row in data["response"]:
                        st.text(row)
                else:
                    st.chat_message("assistant").write(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.chat_message("assistant").write(f"An error occurred: {e}")
        else:
            st.chat_message("assistant").write("Please enter a valid question.")'''

def chatbot_ui():

    # Streamlit App Configuration
    st.set_page_config(page_title="HR Support Chatbot")
    st.header("HR Support Chatbot")


    # Chat history to hold previous messages 
    chat_history = []

    #Always displays this message
    with st.chat_message("assistant"):
        st.write("Hello 👋, I am your HR-suppot chatbot")

    
    # Input from user via chat_input (includes send button)
    question = st.chat_input("Input your question:")

    # FastAPI backend URL
    BACKEND_URL = "http://127.0.0.1:8000/query"


    '''if question:  # Triggered when the send button is clicked
        if question.strip():
            try:
                # Send the request to the backend
                response = requests.post(BACKEND_URL, json={"question": question})
                if response.status_code == 200:
                    data = response.json()
                    if "sql_query" in data:
                        st.chat_message("assistant").write("Here is the SQL query and result:")
                        st.subheader("Generated SQL Query:")
                        st.code(data["sql_query"])
                        st.subheader("Query Result:")
                        for row in data["response"]:
                            st.text(row)
                    else:
                        st.chat_message("assistant").write(data["response"])
                else:
                    st.chat_message("assistant").write(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.chat_message("assistant").write(f"An error occurred: {e}")
        else:
            st.chat_message("assistant").write("Please enter a valid question.")'''
    

    if question:  # Triggered when the send button is clicked

        if question.strip():
            chat_history.append({"role": "user", "message": question})  # Add user question to chat history

            try:
                # Send the request to the backend
                response = requests.post(BACKEND_URL, json={"question": question})

                if response.status_code == 200:
                    data = response.json()
                    
                    if "sql_query" in data:
                        assistant_response = f"Here is the SQL query and result:\n\nGenerated SQL Query:\n\n{data['sql_query']}\n\nQuery Result:\n\n"
                        
                        for row in data["response"]:
                            assistant_response += f"{row}\n"

                    else:
                        assistant_response = data["response"]

                    chat_history.append({"role": "assistant", "message": assistant_response})  # Add assistant response to chat history

                else:
                    error_message = f"Error: {response.json().get('detail', 'Unknown error')}"
                    chat_history.append({"role": "assistant", "message": error_message})  # Add error message to chat history

            except Exception as e:
                error_message = f"An error occurred: {e}"
                chat_history.append({"role": "assistant", "message": error_message})  # Add exception message to chat history

        else:
            chat_history.append({"role": "assistant", "message": "Please enter a valid question."})  # Handle empty user input

    # Display chat history
    for chat in chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["message"])
