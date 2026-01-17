import streamlit as st
import auth

st.set_page_config(page_title="Admin Registration", layout="centered")

st.title(" Admin Registration")

with st.form("register_form"):
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    submit = st.form_submit_button("Register")

if submit:
    if new_password != confirm_password:
        st.error("Passwords do not match!")
    elif len(new_password) < 4:
        st.error("Password must be at least 4 characters.")
    elif auth.register_admin(new_username, new_password):
        st.success("Admin registered successfully! Please go to Login page.")
    else:
        st.error("Username already exists. Please choose another.")
