import streamlit as st
import bcrypt
import database #Import database module
from chatbot import chatbot_ui


ROLES = ["admin","employee"]

#Register the user with employee number,password and role 
def register():

    st.header("Register")
    role = st.selectbox("Choose role you want to register as:",ROLES)
    employee_no = st.text_input("Employee Number")
    plain_password = st.text_input("Password", type='password')
    
    salt = bcrypt.gensalt() # Generate a salt
    
    if st.button("Register"):

        if not employee_no or not plain_password:
            st.error("All fields are required!")
            return
        
        if database.user_exists(employee_no): #User has already registered 
            st.error("Employee number already registered. Please log in.")

        else:
            hashed_password = bcrypt.hashpw(plain_password.encode(), salt) # Hash the password with the salt
            database.add_user(employee_no,hashed_password,role) #Add user into the database

            st.success(f"Successfully registered as {role} with employee number: {employee_no}")
            st.session_state.page = "chatbot"
            #directs to chatbot page


#login with employee no,role and password 
def login():
    st.header("Log In")
    role = st.selectbox("Choose your role", ROLES)
    employee_no = st.text_input("Employee Number")
    entered_password = st.text_input("Password", type='password')

    if st.button("Log in"):
        user = database.get_user(employee_no)

        if user:
            stored_password, stored_role = user

            if bcrypt.checkpw(entered_password.encode(), stored_password):

                if role == stored_role:
                    st.success(f"You have Logged In as {role} by {employee_no}") #After verifying the password with password stored in database display the employee number
                    st.session_state.page = "chatbot"
                    #directs to chatbot page

                else:
                    print("Role mismatch, try again ")

            else:
                print("Incorrect password, try again")
            
            
        else:
            st.error("Employee number not found, please register")




def main():
    database.initialize()  # Initialize the database

    
    if "page" not in st.session_state:
        st.session_state.page = "login"

    
    if st.session_state.page == "login":
        st.sidebar.title("Navigation")
        action = st.sidebar.radio("Choose Action", ["Register", "Log In"])
        if action == "Register":
            register()
        elif action == "Log In":
            login()

    elif st.session_state.page == "chatbot":
        chatbot_ui()

if __name__ == "__main__":
    main()
