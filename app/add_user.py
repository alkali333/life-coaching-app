import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash
from models import SessionLocal, Users

# Streamlit form for adding a new user
with st.form("new_user_form"):
    st.write("Add a New User")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit_button = st.form_submit_button("Create User")

    if submit_button:
        if password == confirm_password:
            # Hash the password
            hashed_password = generate_password_hash(password)
            # Create a new User instance
            new_user = Users(name=name, email=email, password=hashed_password)
            # Add to the session and commit
            with SessionLocal() as session:
                session.add(new_user)
                try:
                    session.commit()
                    st.success("User added successfully.")
                except Exception as e:
                    session.rollback()
                    st.error(f"An error occurred: {e}")
        else:
            st.error("Passwords do not match.")

# Run the streamlit app
if __name__ == "__main__":
    st.title("User Registration")
