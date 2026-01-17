import streamlit as st
import auth
import time

st.set_page_config(page_title="Admin Login", layout="centered")

st.title(" Admin Login")

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if st.session_state.admin_logged_in:
    st.success(f"Welcome back, {st.session_state.get('admin_username', 'Admin')}!")
    st.info("Go to the Dashboard page to view violations.")
    if st.button("Logout"):
        st.session_state.admin_logged_in = False
        st.session_state.admin_username = None
        st.rerun()
else:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if auth.login_admin(username, password):
            st.session_state.admin_logged_in = True
            st.session_state.admin_username = username
            st.success("Login Successful!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid Username or Password")
